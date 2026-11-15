"""Pruebas de integracion FastAPI para blindaje OWASP (413, 422, 429 y cabeceras HTTP)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict

from backend.security import (
    SecurityBoundaryGuard,
    SlidingWindowRateLimiter,
    install_security_handlers,
)


class _StrictDemoDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str


def _create_secured_test_app() -> FastAPI:
    app = FastAPI()
    limiter = SlidingWindowRateLimiter(bucket_limits={"general": 60, "ml": 20}, window_seconds=60.0)
    guard = SecurityBoundaryGuard(max_payload_bytes=16384, rate_limiter=limiter)
    install_security_handlers(app, guard)

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/v1/sandbox/predict-flammability")
    def ml_route(dto: _StrictDemoDto) -> dict[str, str]:
        clean = guard.sanitize_query(dto.query)
        return {"sanitized": clean}

    return app


def test_fastapi_security_middlewares_integration() -> None:
    app = _create_secured_test_app()
    client = TestClient(app)

    # 1. Cabeceras obligatorias en respuestas
    resp_ok = client.get("/api/v1/health")
    assert resp_ok.status_code == 200
    assert "default-src 'self'" in resp_ok.headers["Content-Security-Policy"]
    assert resp_ok.headers["X-Frame-Options"] == "DENY"
    assert resp_ok.headers["X-Content-Type-Options"] == "nosniff"
    assert resp_ok.headers["Referrer-Policy"] == "no-referrer"

    # 2. Extra field -> 422 VALIDATION_ERROR con formato unificado
    resp_extra = client.post(
        "/api/v1/sandbox/predict-flammability",
        json={"query": "BASS-II", "unexpected_admin": True},
    )
    assert resp_extra.status_code == 422
    assert resp_extra.json()["error"]["code"] == "VALIDATION_ERROR"

    # 3. Payload XSS -> 422 VALIDATION_ERROR
    resp_xss = client.post(
        "/api/v1/sandbox/predict-flammability",
        json={"query": "<script>alert(1)</script>"},
    )
    assert resp_xss.status_code == 422
    assert resp_xss.json()["error"]["code"] == "VALIDATION_ERROR"

    # 4. Payload > 16384 bytes -> 413 PAYLOAD_TOO_LARGE
    huge_query = "A" * 17000
    resp_large = client.post(
        "/api/v1/sandbox/predict-flammability",
        json={"query": huge_query},
    )
    assert resp_large.status_code == 413
    assert resp_large.json()["error"]["code"] == "PAYLOAD_TOO_LARGE"

    # 5. Rafaga > 20 req/min en ruta ML -> 429 RATE_LIMITED
    app_rl = _create_secured_test_app()
    client_rl = TestClient(app_rl)
    for _ in range(20):
        r = client_rl.post("/api/v1/sandbox/predict-flammability", json={"query": "SAFFIRE-V"})
        assert r.status_code == 200
    r_blocked = client_rl.post("/api/v1/sandbox/predict-flammability", json={"query": "SAFFIRE-V"})
    assert r_blocked.status_code == 429
    assert r_blocked.json()["error"]["code"] == "RATE_LIMITED"
