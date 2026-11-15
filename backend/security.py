"""Capa de seguridad de frontera OWASP/STRIDE para AERO-IGNIS SI (`security-guard`).

Provee limitacion de tasa por ventana deslizante (`60 req/min` general, `20 req/min` ML),
tope de carga util (`16384` bytes), sanitizacion anti-XSS/SQLi, proteccion contra Path Traversal,
verificacion criptografica SHA-256 antes de cargar modelos `.joblib`/`.onnx` y cabeceras HTTP seguras.
"""

from __future__ import annotations

from collections import deque
import hashlib
import hmac
import json
from pathlib import Path
import re
import threading
import time
from typing import Any, Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


MAX_PAYLOAD_BYTES: int = 16384
ALLOWED_MODEL_SUFFIXES: frozenset[str] = frozenset({".joblib", ".onnx"})
FORBIDDEN_MODEL_SUFFIXES: frozenset[str] = frozenset({".pkl", ".pickle"})

_XSS_SQLI_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"<\s*/?\s*(script|iframe|svg|object|embed|style)", re.IGNORECASE),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"\bon\w+\s*=", re.IGNORECASE),
    re.compile(r";\s*(drop|delete|insert|update|union|alter|exec)\b", re.IGNORECASE),
    re.compile(r"(--|/\*|\*/)"),
    re.compile(r"('\s+or\s+['\d]|\"\s+or\s+[\"\d])", re.IGNORECASE),
)

_ML_ROUTE_PREFIXES: tuple[str, ...] = (
    "/api/v1/psi/rank-and-interpret",
    "/api/v1/sandbox/",
    "/api/v1/twin/",
)


class SecurityError(Exception):
    """Clase base para violaciones de seguridad en frontera."""

    code: str = "SECURITY_ERROR"
    status_code: int = 400


class RateLimitExceededError(SecurityError):
    """Se lanza al superar el limite de peticiones por ventana deslizante (HTTP 429)."""

    code = "RATE_LIMITED"
    status_code = 429


class PayloadTooLargeError(SecurityError):
    """Se lanza cuando la carga util excede `MAX_PAYLOAD_BYTES` (HTTP 413)."""

    code = "PAYLOAD_TOO_LARGE"
    status_code = 413


class IntegrityError(SecurityError):
    """Se lanza cuando falla la validacion SHA-256 o se detecta extension prohibida."""

    code = "INTEGRITY_ERROR"
    status_code = 500


class InputValidationError(SecurityError):
    """Se lanza cuando una cadena de entrada infringe sanitizacion o limites (HTTP 422)."""

    code = "VALIDATION_ERROR"
    status_code = 422


def error_payload(code: str, message: str) -> dict[str, dict[str, str]]:
    """Construye el formato uniforme de error declarado en SPEC.md sin trazas internas."""
    return {"error": {"code": code, "message": message}}


class SlidingWindowRateLimiter:
    """Limitador de tasa por IP en ventana deslizante thread-safe para mitigacion DDoS L7."""

    def __init__(
        self,
        bucket_limits: dict[str, int] | None = None,
        window_seconds: float = 60.0,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._bucket_limits = dict(bucket_limits or {"general": 60, "ml": 20})
        if window_seconds <= 0:
            raise ValueError("window_seconds debe ser positivo.")
        self._window_seconds = float(window_seconds)
        self._clock = clock or time.monotonic
        self._hits: dict[tuple[str, str], deque[float]] = {}
        self._lock = threading.Lock()

    def check(self, client_ip: str, bucket: str = "general") -> None:
        """Verifica e incrementa el contador para `(client_ip, bucket)` o lanza RateLimitExceededError."""
        limit = self._bucket_limits.get(bucket, self._bucket_limits.get("general", 60))
        ip_key = (client_ip or "unknown").strip() or "unknown"
        now = float(self._clock())
        cutoff = now - self._window_seconds
        key = (ip_key, bucket)

        with self._lock:
            window = self._hits.setdefault(key, deque())
            while window and window[0] <= cutoff:
                window.popleft()
            if len(window) >= limit:
                raise RateLimitExceededError(
                    f"Limite de tasa excedido para ruta '{bucket}' ({limit} req/{int(self._window_seconds)}s)."
                )
            window.append(now)

            # Evita crecimiento ilimitado de entradas inactivas en escenarios de fuzzing
            if len(self._hits) > 4096:
                stale_keys = [k for k, dq in self._hits.items() if not dq or dq[-1] <= cutoff]
                for sk in stale_keys:
                    del self._hits[sk]


class SecurityBoundaryGuard:
    """Frontera unica de seguridad: tamano de carga, rate limit, sanitizacion y verificacion SHA-256."""

    def __init__(
        self,
        max_payload_bytes: int = MAX_PAYLOAD_BYTES,
        rate_limiter: SlidingWindowRateLimiter | None = None,
    ) -> None:
        if max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes debe ser positivo.")
        self._max_payload_bytes = int(max_payload_bytes)
        self._rate_limiter = rate_limiter or SlidingWindowRateLimiter()

    @property
    def max_payload_bytes(self) -> int:
        """Retorna el tope maximo de bytes por solicitud."""
        return self._max_payload_bytes

    def validate_request_size(self, content_length: int) -> None:
        """Verifica que la longitud del cuerpo no supere `max_payload_bytes`."""
        if content_length < 0:
            raise InputValidationError("Longitud de carga util invalida.")
        if content_length > self._max_payload_bytes:
            raise PayloadTooLargeError(
                f"Carga util excede el maximo permitido de {self._max_payload_bytes} bytes."
            )

    def check_rate_limit(self, client_ip: str, bucket: str = "general") -> None:
        """Delega verificacion al limitador por IP."""
        self._rate_limiter.check(client_ip=client_ip, bucket=bucket)

    def sanitize_query(self, text: str, max_len: int = 120) -> str:
        """Valida y normaliza entradas textuales bloqueando XSS, SQLi y caracteres de control."""
        if not isinstance(text, str):
            raise InputValidationError("El texto de consulta debe ser una cadena.")
        stripped = text.strip()
        if len(stripped) > max_len:
            raise InputValidationError(f"La consulta excede la longitud maxima de {max_len} caracteres.")

        for ch in stripped:
            code = ord(ch)
            if code < 32 and ch not in ("\t",):
                raise InputValidationError("Caracter de control no permitido en consulta.")

        for pattern in _XSS_SQLI_PATTERNS:
            if pattern.search(stripped):
                raise InputValidationError("Patron potencialmente malicioso bloqueado en entrada.")
        return stripped

    @staticmethod
    def resolve_within_root(target: Path, allowed_root: Path) -> Path:
        """Previene ataques Path Traversal verificando que `target` viva dentro de `allowed_root`."""
        root_resolved = allowed_root.resolve()
        target_resolved = target.resolve()
        try:
            target_resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise IntegrityError("Acceso fuera del directorio permitido bloqueado.") from exc
        return target_resolved

    @staticmethod
    def compute_sha256(file_path: Path) -> str:
        """Calcula el digest SHA-256 en streaming de 64 KB."""
        digest = hashlib.sha256()
        with file_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def verify_model_sha256(self, model_path: Path, manifest_path: Path) -> str:
        """Verifica integridad criptografica SHA-256 antes de deserializar `.joblib` o `.onnx`."""
        path = Path(model_path)
        manifest = Path(manifest_path)

        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_MODEL_SUFFIXES or suffix not in ALLOWED_MODEL_SUFFIXES:
            raise IntegrityError(f"Formato de modelo prohibido o no autorizado: {path.name}")
        if not path.is_file():
            raise IntegrityError(f"Artefacto de modelo inexistente: {path.name}")
        if not manifest.is_file():
            raise IntegrityError("Manifiesto SHA-256 de modelos no encontrado.")

        try:
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise IntegrityError("Manifiesto SHA-256 corrupto o ilegible.") from exc

        models_map = manifest_data.get("models", manifest_data)
        entry = models_map.get(path.name)
        if not isinstance(entry, dict) or "sha256" not in entry:
            raise IntegrityError(f"El modelo {path.name} no esta registrado en el manifiesto SHA-256.")

        expected_sha = str(entry["sha256"]).lower()
        actual_sha = self.compute_sha256(path).lower()
        if not hmac.compare_digest(actual_sha, expected_sha):
            raise IntegrityError(f"Fallo de verificacion SHA-256 para {path.name}.")
        return actual_sha


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inyecta cabeceras defensivas OWASP (CSP, X-Frame-Options, nosniff, Referrer-Policy)."""

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Response:
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class PayloadAndRateLimitMiddleware(BaseHTTPMiddleware):
    """Aplica tope de tamano de payload (`413`) y rate limiting (`429`) antes de validar DTOs."""

    def __init__(self, app: Any, guard: SecurityBoundaryGuard) -> None:
        super().__init__(app)
        self._guard = guard

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Response:
        path = request.url.path
        bucket = "ml" if any(path.startswith(prefix) for prefix in _ML_ROUTE_PREFIXES) else "general"
        client_ip = request.client.host if request.client else "unknown"

        try:
            content_length_raw = request.headers.get("content-length")
            if content_length_raw is not None:
                try:
                    declared_len = int(content_length_raw)
                except ValueError as exc:
                    raise InputValidationError("Cabecera Content-Length invalida.") from exc
                self._guard.validate_request_size(declared_len)

            if request.method in {"POST", "PUT", "PATCH"}:
                body = await request.body()
                self._guard.validate_request_size(len(body))

            self._guard.check_rate_limit(client_ip=client_ip, bucket=bucket)
        except SecurityError as exc:
            return JSONResponse(status_code=exc.status_code, content=error_payload(exc.code, str(exc)))

        return await call_next(request)


def install_security_handlers(app: FastAPI, guard: SecurityBoundaryGuard) -> None:
    """Registra middlewares y manejadores uniformes de errores OWASP sobre la aplicacion FastAPI."""

    # LIFO en Starlette: PayloadAndRateLimit corre dentro, SecurityHeaders envuelve todas las salidas.
    app.add_middleware(PayloadAndRateLimitMiddleware, guard=guard)
    app.add_middleware(SecurityHeadersMiddleware)

    @app.exception_handler(RequestValidationError)
    async def handle_pydantic_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        summary = "; ".join(str(err.get("msg", "Entrada invalida")) for err in exc.errors()[:3])
        return JSONResponse(
            status_code=422,
            content=error_payload("VALIDATION_ERROR", summary or "Error de validacion en frontera."),
        )

    @app.exception_handler(SecurityError)
    async def handle_security_error(_: Request, exc: SecurityError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=error_payload(exc.code, str(exc)))
