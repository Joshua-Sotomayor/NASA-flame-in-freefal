"""Modulo de dominio POO y repositorio tipado de las 24 investigaciones NASA PSI.

Cumple con los contratos de `SPEC.md` (`psi-domain-repo`), inmutabilidad de objetos de valor,
paginacion acotada (`page_size <= 50`) y defensa anti-SSRF con fallback offline silencioso.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
from typing import Any, Callable, Sequence
from urllib.parse import urlsplit

import numpy as np
import requests


VALID_FACILITIES: frozenset[str] = frozenset({"ISS-CIR", "ISS-MSG", "Cygnus", "Otros"})
ALLOWED_OSDR_HOSTS: frozenset[str] = frozenset({"osdr.nasa.gov", "visualization.osdr.nasa.gov"})
_ACCESSION_PATTERN: re.Pattern[str] = re.compile(r"^(OSD|PSI)-(\d{1,5})$")
_MAX_PAGE_SIZE: int = 50
_MAX_PAGE_NUMBER: int = 10

FLAMMABILITY_FEATURES: tuple[str, ...] = (
    "o2_pct",
    "pressure_atm",
    "air_flow_cms",
    "gravity_g",
    "thickness_cm",
    "flow_concurrent",
    "material_reactivity",
)

MATERIAL_REACTIVITY_MAP: dict[str, float] = {
    "Algodon": 1.35,
    "PMMA": 1.15,
    "SIBAL": 1.05,
    "Nomex": 0.42,
    "Kapton": 0.35,
    "PTFE": 0.25,
}

FLAME_CLASS_LABELS: tuple[str, ...] = (
    "Nominal",
    "Llama Esferica Azul 0g",
    "Llama Fria NTC",
    "Propagacion Abierta",
)

OPTICAL_PRESET_TO_IDX: dict[str, int] = {
    "nominal": 0,
    "spherical_0g": 1,
    "cool_flame_ntc": 2,
    "open_propagation": 3,
}

SENSOR_FEATURES: tuple[str, ...] = (
    "delta_t_dt",
    "co_ppm",
    "submicron_aerosol",
    "airflow_cm_s",
)

SENSOR_CLASS_LABELS: tuple[str, ...] = (
    "Nominal",
    "Pre_Alerta",
    "Contencion",
)


def generate_optical_frame(
    preset: str,
    noise_std: float = 0.04,
    seed: int | None = None,
) -> np.ndarray:
    """Genera una imagen termica/optica sintetica 64x64 calibrada por regimen fisico."""
    key = preset.strip().lower()
    if key not in OPTICAL_PRESET_TO_IDX:
        raise ValueError(f"Preset optico desconocido: {preset}")

    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[-1:1:64j, -1:1:64j]
    rr = np.sqrt(xx**2 + yy**2)

    cls_idx = OPTICAL_PRESET_TO_IDX[key]
    if cls_idx == 0:
        base = np.full((64, 64), 0.08, dtype=np.float32)
    elif cls_idx == 1:
        base = (0.75 * np.exp(-(rr**2) / 0.14)).astype(np.float32)
    elif cls_idx == 2:
        base = (0.30 * np.exp(-((rr - 0.38) ** 2) / 0.045)).astype(np.float32)
    else:
        shift = xx + 0.35 * (yy**2)
        base = (0.95 * np.exp(-((shift - 0.15) ** 2 + (yy**2)) / 0.18)).astype(np.float32)

    if noise_std > 0.0:
        noise = rng.normal(0.0, noise_std, (64, 64)).astype(np.float32)
        base = base + noise
    return np.clip(base, 0.0, 1.0).astype(np.float32)


def preset_to_input_tensor(
    preset: str | None = None,
    optical_vector: Sequence[float] | None = None,
    seed: int = 42,
) -> np.ndarray:
    """Convierte un preset o vector de 64 floats en tensor float32 `(1, 1, 64, 64)`."""
    if optical_vector is not None:
        arr = np.asarray(optical_vector, dtype=np.float32)
        if arr.shape != (64,):
            raise ValueError("optical_vector debe tener exactamente 64 valores flotantes.")
        if not np.isfinite(arr).all():
            raise ValueError("optical_vector contiene valores no finitos.")
        grid_8x8 = np.clip(arr.reshape(8, 8), 0.0, 1.0)
        upscaled = np.kron(grid_8x8, np.ones((8, 8), dtype=np.float32))
        return upscaled[None, None, :, :].astype(np.float32)

    chosen = preset or "nominal"
    frame = generate_optical_frame(preset=chosen, noise_std=0.0, seed=seed)
    return frame[None, None, :, :].astype(np.float32)


class SecurityViolationError(ValueError):
    """Se lanza cuando una entrada o URL infringe las politicas de frontera segura (SSRF/formato)."""


@dataclass(frozen=True)
class PsiInvestigation:
    """Objeto de valor inmutable que representa una investigacion oficial NASA PSI."""

    psi_id: str
    acronym: str
    facility: str
    doi: str
    osdr_id: str
    o2_min: float
    o2_max: float
    pressure_psi_min: float
    pressure_psi_max: float
    flow_cm_s_max: float
    materials: tuple[str, ...]
    sensors: tuple[str, ...]
    objectives: str
    approach: str
    earth_benefits: str
    category: str
    criteria_scores: tuple[tuple[str, float], ...]

    def criteria_dict(self) -> dict[str, float]:
        """Retorna una copia mutable segura de los puntajes multicriterio."""
        return dict(self.criteria_scores)

    def to_dict(self) -> dict[str, Any]:
        """Serializa la entidad inmutable a un diccionario compatible con DTO REST."""
        return {
            "psi_id": self.psi_id,
            "acronym": self.acronym,
            "facility": self.facility,
            "doi": self.doi,
            "osdr_id": self.osdr_id,
            "o2_min": self.o2_min,
            "o2_max": self.o2_max,
            "pressure_psi_min": self.pressure_psi_min,
            "pressure_psi_max": self.pressure_psi_max,
            "flow_cm_s_max": self.flow_cm_s_max,
            "materials": list(self.materials),
            "sensors": list(self.sensors),
            "objectives": self.objectives,
            "approach": self.approach,
            "earth_benefits": self.earth_benefits,
            "category": self.category,
            "criteria_scores": self.criteria_dict(),
        }


@dataclass(frozen=True)
class PaginatedResult:
    """Resultado paginado e inmutable de consultas al repositorio PSI."""

    items: tuple[PsiInvestigation, ...]
    page: int
    page_size: int
    total: int
    total_pages: int

    def to_dict(self) -> dict[str, Any]:
        """Serializa la pagina actual y sus metadatos de paginacion."""
        return {
            "data": [item.to_dict() for item in self.items],
            "pagination": {
                "page": self.page,
                "page_size": self.page_size,
                "total": self.total,
                "total_pages": self.total_pages,
            },
        }


class OsdrApiClient:
    """Conector HTTP acotado por allowlist hacia NASA OSDR v2 con timeout estricto."""

    def __init__(self, timeout_s: float = 3.0) -> None:
        if timeout_s <= 0 or timeout_s > 5.0:
            raise ValueError("El timeout OSDR debe estar en (0, 5.0] segundos.")
        self._timeout_s = float(timeout_s)

    @property
    def timeout_s(self) -> float:
        """Retorna el timeout configurado en segundos."""
        return self._timeout_s

    def validate_url(self, url: str) -> str:
        """Valida que la URL use HTTPS y apunte exclusivamente a hosts OSDR autorizados."""
        parsed = urlsplit(url.strip())
        if parsed.scheme != "https":
            raise SecurityViolationError("Solo se permite el esquema HTTPS hacia NASA OSDR.")
        if parsed.username or parsed.password:
            raise SecurityViolationError("URL bloqueada por credenciales embebidas.")
        if parsed.port is not None:
            raise SecurityViolationError("No se permiten puertos personalizados en URLs OSDR.")
        if parsed.hostname not in ALLOWED_OSDR_HOSTS:
            raise SecurityViolationError(f"Host no autorizado por politica anti-SSRF: {parsed.hostname}")
        return parsed.geturl()

    def parse_accession(self, accession: str) -> tuple[str, str]:
        """Valida estrictamente el formato OSD-NN o PSI-NN contra inyecciones de ruta."""
        cleaned = accession.strip().upper()
        match = _ACCESSION_PATTERN.fullmatch(cleaned)
        if not match:
            raise SecurityViolationError(f"Identificador OSDR/PSI invalido: {accession}")
        return match.group(1), match.group(2)

    def fetch_study_metadata(
        self,
        accession: str,
        http_get: Callable[..., Any] | None = None,
    ) -> dict[str, Any] | None:
        """Consulta metadata en vivo sin redirecciones; retorna None si falla o expira."""
        _, numeric_id = self.parse_accession(accession)
        target_url = self.validate_url(f"https://osdr.nasa.gov/osdr/data/osd/meta/{numeric_id}")
        getter = http_get or requests.get
        try:
            response = getter(target_url, timeout=self._timeout_s, allow_redirects=False)
        except (requests.RequestException, TimeoutError, OSError):
            return None

        status_code = getattr(response, "status_code", None)
        if status_code != 200:
            return None
        try:
            payload = response.json()
        except ValueError:
            return None
        return payload if isinstance(payload, dict) else None


class PsiRepository:
    """Repositorio POO de solo lectura para las 24 investigaciones PSI y respaldo OSDR."""

    def __init__(self, data_path: Path, osdr_client: OsdrApiClient | None = None) -> None:
        self._data_path = Path(data_path)
        self._osdr_client = osdr_client or OsdrApiClient(timeout_s=3.0)
        self._investigations = self._load_investigations(self._data_path)
        self._by_id: dict[str, PsiInvestigation] = {item.psi_id: item for item in self._investigations}
        self._by_osdr: dict[str, PsiInvestigation] = {item.osdr_id: item for item in self._investigations}

    @staticmethod
    def _load_investigations(data_path: Path) -> tuple[PsiInvestigation, ...]:
        if not data_path.exists():
            raise FileNotFoundError(f"No se encontro el catalogo PSI en: {data_path}")
        raw = json.loads(data_path.read_text(encoding="utf-8"))
        entries = raw.get("investigations", [])
        loaded: list[PsiInvestigation] = []
        for entry in entries:
            facility = str(entry["facility"])
            if facility not in VALID_FACILITIES:
                raise ValueError(f"Instalacion no reconocida en {entry.get('psi_id')}: {facility}")
            scores_raw = entry.get("criteria_scores", {})
            scores_tuple = tuple(sorted((str(k), float(v)) for k, v in scores_raw.items()))
            loaded.append(
                PsiInvestigation(
                    psi_id=str(entry["psi_id"]),
                    acronym=str(entry["acronym"]),
                    facility=facility,
                    doi=str(entry["doi"]),
                    osdr_id=str(entry["osdr_id"]),
                    o2_min=float(entry["o2_min"]),
                    o2_max=float(entry["o2_max"]),
                    pressure_psi_min=float(entry["pressure_psi_min"]),
                    pressure_psi_max=float(entry["pressure_psi_max"]),
                    flow_cm_s_max=float(entry["flow_cm_s_max"]),
                    materials=tuple(str(m) for m in entry.get("materials", ())),
                    sensors=tuple(str(s) for s in entry.get("sensors", ())),
                    objectives=str(entry["objectives"]),
                    approach=str(entry["approach"]),
                    earth_benefits=str(entry["earth_benefits"]),
                    category=str(entry["category"]),
                    criteria_scores=scores_tuple,
                )
            )
        return tuple(loaded)

    def all_investigations(self) -> tuple[PsiInvestigation, ...]:
        """Retorna todas las investigaciones cargadas en una tupla inmutable."""
        return self._investigations

    def get_by_id(self, psi_id: str) -> PsiInvestigation:
        """Obtiene una investigacion por su psi_id o lanza KeyError."""
        key = psi_id.strip().upper()
        if key not in self._by_id:
            raise KeyError(f"Investigacion no encontrada: {psi_id}")
        return self._by_id[key]

    def list_investigations(
        self,
        facility: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 24,
    ) -> PaginatedResult:
        """Filtra y pagina investigaciones respetando limites anti-DDoS (`page_size <= 50`)."""
        if not (1 <= page <= _MAX_PAGE_NUMBER):
            raise ValueError(f"page debe estar entre 1 y {_MAX_PAGE_NUMBER}.")
        if not (1 <= page_size <= _MAX_PAGE_SIZE):
            raise ValueError(f"page_size debe estar entre 1 y {_MAX_PAGE_SIZE}.")
        if facility is not None and facility not in VALID_FACILITIES:
            raise ValueError(f"Instalacion invalida: {facility}")

        normalized_query = query.strip().lower() if query else ""
        filtered: list[PsiInvestigation] = []
        for item in self._investigations:
            if facility and item.facility != facility:
                continue
            if normalized_query:
                haystack = " ".join(
                    [
                        item.psi_id,
                        item.acronym,
                        item.facility,
                        item.category,
                        " ".join(item.materials),
                        item.objectives,
                    ]
                ).lower()
                if normalized_query not in haystack:
                    continue
            filtered.append(item)

        total = len(filtered)
        total_pages = max(1, math.ceil(total / page_size))
        start = (page - 1) * page_size
        end = start + page_size
        return PaginatedResult(
            items=tuple(filtered[start:end]),
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    def fetch_osdr_metadata_safe(
        self,
        accession_or_psi_id: str,
        http_get: Callable[..., Any] | None = None,
    ) -> dict[str, Any]:
        """Consulta OSDR v2 con fallback inmediato al catalogo local si no hay red."""
        self._osdr_client.parse_accession(accession_or_psi_id)
        key = accession_or_psi_id.strip().upper()
        local_item = self._by_id.get(key) or self._by_osdr.get(key)
        target_osdr = local_item.osdr_id if local_item else key

        live_payload = self._osdr_client.fetch_study_metadata(target_osdr, http_get=http_get)
        if live_payload is not None:
            result = local_item.to_dict() if local_item else {"osdr_id": target_osdr}
            result["source"] = "osdr_live"
            result["osdr_payload_keys"] = sorted(live_payload.keys())[:10]
            return result

        if local_item is None:
            raise KeyError(f"Estudio no encontrado ni en OSDR ni en respaldo local: {accession_or_psi_id}")

        fallback = local_item.to_dict()
        fallback["source"] = "local_fallback"
        return fallback
