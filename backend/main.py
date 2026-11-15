"""Ensamblaje FastAPI POO de AERO-IGNIS SI (`SPEC.md` Seccion 3).

Expone exactamente los 6 contratos `/api/v1/*` con DTOs Pydantic v2 `extra="forbid"`,
inyeccion de dependencias en `app.state.services` y blindaje OWASP (`SecurityBoundaryGuard`).
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import sys
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

DEFAULT_ROOT_DIR = Path(__file__).resolve().parents[1]
if str(DEFAULT_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(DEFAULT_ROOT_DIR))

from backend.domain import PsiRepository
from backend.duct_twin import (
    DuctSafetyOrchestrator,
    OpticalInput,
    SensorTelemetryFrame,
)
from backend.governance import GovernanceAndSpinoffService
from backend.physics_ml import AtmosphericState, FlammabilityPredictor
from backend.ranking_nlp import ExtractiveNlpEngine, TopsisMultiCriteriaRanker
from backend.security import (
    SecurityBoundaryGuard,
    SlidingWindowRateLimiter,
    install_security_handlers,
)


class CriteriaWeightsDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    habitat: float = Field(ge=0.0, le=100.0)
    modeling: float = Field(ge=0.0, le=100.0)
    sensors: float = Field(ge=0.0, le=100.0)
    spinoff: float = Field(ge=0.0, le=100.0)


class RankAndInterpretRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weights: CriteriaWeightsDto
    persona: Literal["Investigador", "Estudiante", "Gestor Industrial"]
    query: str = Field(default="", max_length=120)


class FlammabilityRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    o2_pct: float = Field(ge=10.0, le=100.0)
    pressure_psi: float = Field(ge=1.0, le=30.0)
    flow_cm_s: float = Field(ge=0.0, le=60.0)
    gravity_g: Literal[0, 0.0, 0.16, 0.38, 1, 1.0]
    material: Literal["Algodon", "PMMA", "SIBAL", "Nomex", "Kapton", "PTFE"]
    thickness_mm: float = Field(ge=0.1, le=50.0)
    flow_dir: Literal["concurrent", "opposed"]


class TwinStepRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    optical_preset: Literal["nominal", "spherical_0g", "cool_flame_ntc", "open_propagation"] | None = None
    optical_vector: list[float] | None = Field(default=None, min_length=64, max_length=64)
    delta_t_dt: float = Field(ge=-5.0, le=100.0)
    co_ppm: float = Field(ge=0.0, le=5000.0)
    submicron_aerosol: float = Field(ge=0.0, le=100.0)
    airflow_cm_s: float = Field(ge=0.0, le=60.0)
    comm_ok: bool = True


@dataclass(frozen=True)
class AeroIgnisServices:
    """Contenedor inmutable de dependencias POO para rutas FastAPI."""

    guard: SecurityBoundaryGuard
    repository: PsiRepository
    ranker: TopsisMultiCriteriaRanker
    nlp_engine: ExtractiveNlpEngine
    predictor: FlammabilityPredictor
    orchestrator: DuctSafetyOrchestrator
    governance: GovernanceAndSpinoffService
    models_verified_sha256: bool


def create_app(
    data_dir: Path | None = None,
    artifacts_dir: Path | None = None,
    frontend_dir: Path | None = None,
    rate_limiter: SlidingWindowRateLimiter | None = None,
) -> FastAPI:
    """Factoria principal FastAPI ensamblando capas unidireccionales POO."""
    resolved_data = Path(data_dir or (DEFAULT_ROOT_DIR / "data"))
    resolved_artifacts = Path(artifacts_dir or (DEFAULT_ROOT_DIR / "artifacts" / "models"))
    resolved_frontend = Path(frontend_dir or (DEFAULT_ROOT_DIR / "frontend"))

    guard = SecurityBoundaryGuard(
        max_payload_bytes=16384,
        rate_limiter=rate_limiter or SlidingWindowRateLimiter(bucket_limits={"general": 60, "ml": 20}),
    )
    repository = PsiRepository(data_path=resolved_data / "psi_combustion_24.json")
    ranker = TopsisMultiCriteriaRanker()
    nlp_engine = ExtractiveNlpEngine.from_artifacts(artifacts_dir=resolved_artifacts, guard=guard)
    predictor = FlammabilityPredictor.from_artifacts(artifacts_dir=resolved_artifacts, guard=guard)
    orchestrator = DuctSafetyOrchestrator.from_artifacts(artifacts_dir=resolved_artifacts, guard=guard)
    governance = GovernanceAndSpinoffService(cases_json_path=resolved_data / "cases_and_spinoffs.json")

    app = FastAPI(
        title="AERO-IGNIS SI API",
        version="1.1.0",
        description="Plataforma ML/DL propia para seguridad contra incendios en microgravedad (NASA PSI).",
    )
    app.state.services = AeroIgnisServices(
        guard=guard,
        repository=repository,
        ranker=ranker,
        nlp_engine=nlp_engine,
        predictor=predictor,
        orchestrator=orchestrator,
        governance=governance,
        models_verified_sha256=True,
    )
    install_security_handlers(app, guard)
    allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "").strip()
    allowed_origins = [origin.strip() for origin in allowed_origins_raw.split(",") if origin.strip()]
    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
            allow_headers=["Content-Type", "Accept"],
        )

    @app.api_route("/api/v1/health", methods=["GET", "HEAD"])
    def health(request: Request) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        return {
            "status": "ok",
            "models_verified_sha256": svc.models_verified_sha256,
            "psi_count": len(svc.repository.all_investigations()),
        }

    @app.get("/api/v1/psi/investigations")
    def list_psi(
        request: Request,
        facility: Literal["ISS-CIR", "ISS-MSG", "Cygnus", "Otros"] | None = None,
        q: str | None = Query(default=None, max_length=120),
        page: int = Query(default=1, ge=1, le=10),
        pageSize: int = Query(default=24, ge=1, le=50),
    ) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        clean_q = svc.guard.sanitize_query(q, max_len=120) if q else None
        result = svc.repository.list_investigations(
            facility=facility,
            query=clean_q,
            page=page,
            page_size=pageSize,
        )
        return result.to_dict()

    @app.post("/api/v1/psi/rank-and-interpret")
    def rank_and_interpret(request: Request, body: RankAndInterpretRequestDto) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        clean_q = svc.guard.sanitize_query(body.query, max_len=120) if body.query else ""
        investigations = svc.repository.all_investigations()
        weights_dict = body.weights.model_dump()
        ranked = svc.ranker.rank(investigations=investigations, weights=weights_dict)
        clusters_2d = svc.nlp_engine.get_clusters_2d(investigations)
        synthesis = svc.nlp_engine.summarize_for_persona(
            investigations=investigations,
            ranked=ranked,
            query=clean_q,
            persona=body.persona,
        )
        return {
            "ranked": [item.to_dict() for item in ranked],
            "clusters_2d": [pt.to_dict() for pt in clusters_2d],
            "synthesis": synthesis.to_dict(),
        }

    @app.post("/api/v1/sandbox/predict-flammability")
    def predict_flammability(request: Request, body: FlammabilityRequestDto) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        state = AtmosphericState(
            o2_pct=body.o2_pct,
            pressure_psi=body.pressure_psi,
            flow_cm_s=body.flow_cm_s,
            gravity_g=float(body.gravity_g),
            material=body.material,
            thickness_mm=body.thickness_mm,
            flow_dir=body.flow_dir,
        )
        prediction = svc.predictor.predict(state)
        return prediction.to_dict()

    @app.post("/api/v1/twin/step-fsm")
    def step_fsm(request: Request, body: TwinStepRequestDto) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        telemetry = SensorTelemetryFrame(
            delta_t_dt=body.delta_t_dt,
            co_ppm=body.co_ppm,
            submicron_aerosol=body.submicron_aerosol,
            airflow_cm_s=body.airflow_cm_s,
            comm_ok=body.comm_ok,
        )
        optical = OpticalInput(
            optical_preset=body.optical_preset or ("nominal" if body.optical_vector is None else None),
            optical_vector=body.optical_vector,
        )
        snapshot = svc.orchestrator.step(telemetry=telemetry, optical_input=optical)
        return snapshot.to_dict()

    @app.get("/api/v1/governance/fmea-and-spinoffs")
    def fmea_and_spinoffs(
        request: Request,
        mitigated: bool = False,
        spinoff_id: Literal["9582", "9407", "9918", "PFE"] | None = None,
        units: int = Query(default=1, ge=1, le=10000),
    ) -> dict[str, Any]:
        svc: AeroIgnisServices = request.app.state.services
        fmea = svc.governance.evaluate_fmea(mitigated=mitigated)
        dual_use = svc.governance.calculate_dual_use(spinoff_id=spinoff_id, units=units)
        return {
            "fmea_rows": fmea.to_dict()["rows"],
            "fmea_summary": {
                "mitigated": fmea.mitigated,
                "total_baseline_npr": fmea.total_baseline_npr,
                "total_active_npr": fmea.total_active_npr,
                "average_npr_reduction_pct": round(fmea.average_npr_reduction_pct, 2),
            },
            "spinoff_metrics": dual_use.to_dict(),
        }

    def _serve_frontend_asset(asset_name: str) -> FileResponse:
        allowed_assets = {"index.html", "styles.css", "app.js", "GeistPixel-Square.woff2"}
        if asset_name not in allowed_assets:
            raise HTTPException(status_code=404, detail="Recurso no encontrado.")
        safe_path = guard.resolve_within_root(resolved_frontend / asset_name, resolved_frontend)
        if not safe_path.is_file():
            raise HTTPException(status_code=404, detail="Archivo frontend aun no disponible.")
        return FileResponse(path=safe_path)

    @app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
    def serve_dashboard_root() -> FileResponse:
        return _serve_frontend_asset("index.html")

    @app.get("/styles.css", include_in_schema=False)
    def serve_dashboard_css_root() -> FileResponse:
        return _serve_frontend_asset("styles.css")

    @app.get("/app.js", include_in_schema=False)
    def serve_dashboard_js_root() -> FileResponse:
        return _serve_frontend_asset("app.js")

    @app.get("/GeistPixel-Square.woff2", include_in_schema=False)
    def serve_dashboard_font_root() -> FileResponse:
        return _serve_frontend_asset("GeistPixel-Square.woff2")

    @app.get("/assets/museum/{image_name}", include_in_schema=False)
    def serve_museum_image(image_name: str) -> FileResponse:
        allowed_images = {
            "flame_0g.jpg",
            "bass_ii_iss.jpg",
            "saffire_cygnus.jpg",
            "cir_rack_iss.jpg",
            "apollo_1_crew.jpg",
            "mir_station.jpg",
        }
        if image_name not in allowed_images:
            raise HTTPException(status_code=404, detail="Fotografia de museo no encontrada.")
        museum_root = resolved_frontend / "assets" / "museum"
        safe_path = guard.resolve_within_root(museum_root / image_name, museum_root)
        if not safe_path.is_file():
            raise HTTPException(status_code=404, detail="Archivo de fotografia aun no disponible.")
        return FileResponse(path=safe_path)

    @app.get("/frontend/{asset_name}", include_in_schema=False)
    def serve_dashboard_asset(asset_name: str) -> FileResponse:
        return _serve_frontend_asset(asset_name)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
