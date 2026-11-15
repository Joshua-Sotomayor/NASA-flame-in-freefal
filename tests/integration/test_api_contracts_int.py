"""Pruebas de integracion de contratos REST de SPEC.md y proteccion OWASP en FastAPI."""

from pathlib import Path
from fastapi.testclient import TestClient

from backend.main import create_app

ROOT_DIR = Path(__file__).resolve().parents[2]


def test_all_6_fastapi_endpoints_and_owasp_defenses() -> None:
    app = create_app(data_dir=ROOT_DIR / "data", artifacts_dir=ROOT_DIR / "artifacts" / "models")
    client = TestClient(app)

    # 1. GET /api/v1/health
    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200
    h_json = r_health.json()
    assert h_json == {"status": "ok", "models_verified_sha256": True, "psi_count": 24}
    assert r_health.headers["X-Frame-Options"] == "DENY"
    assert r_health.headers["X-Content-Type-Options"] == "nosniff"

    # 2. GET /api/v1/psi/investigations
    r_psi = client.get("/api/v1/psi/investigations", params={"facility": "Cygnus", "page": 1, "pageSize": 10})
    assert r_psi.status_code == 200
    p_json = r_psi.json()
    assert p_json["pagination"]["total"] == 6
    assert len(p_json["data"]) == 6

    # 3. POST /api/v1/psi/rank-and-interpret
    r_rank = client.post(
        "/api/v1/psi/rank-and-interpret",
        json={
            "weights": {"habitat": 0.4, "modeling": 0.25, "sensors": 0.2, "spinoff": 0.15},
            "persona": "Investigador",
            "query": "SAFFIRE lunar 34% O2",
        },
    )
    assert r_rank.status_code == 200
    rank_json = r_rank.json()
    assert len(rank_json["ranked"]) == 24
    assert len(rank_json["clusters_2d"]) == 24
    assert len(rank_json["synthesis"]["bullets"]) >= 3
    assert len(rank_json["synthesis"]["cited_dois"]) >= 2

    # 4. POST /api/v1/sandbox/predict-flammability
    r_flam = client.post(
        "/api/v1/sandbox/predict-flammability",
        json={
            "o2_pct": 34.0,
            "pressure_psi": 8.2,
            "flow_cm_s": 12.0,
            "gravity_g": 0.16,
            "material": "SIBAL",
            "thickness_mm": 0.8,
            "flow_dir": "concurrent",
        },
    )
    assert r_flam.status_code == 200
    flam_json = r_flam.json()
    for key in ("extinguished_prob", "burn_time_s", "flame_spread_mm_s", "damkohler", "peclet", "regime", "feature_importance"):
        assert key in flam_json

    # 5. POST /api/v1/twin/step-fsm
    r_twin = client.post(
        "/api/v1/twin/step-fsm",
        json={
            "optical_preset": "spherical_0g",
            "delta_t_dt": 3.5,
            "co_ppm": 25.0,
            "submicron_aerosol": 22.0,
            "airflow_cm_s": 15.0,
            "comm_ok": True,
        },
    )
    assert r_twin.status_code == 200
    twin_json = r_twin.json()
    assert twin_json["cnn_class"] == "Llama Esferica Azul 0g"
    assert len(twin_json["cnn_probs"]) == 4
    assert "->" in twin_json["tree_rule_path"]
    assert twin_json["fsm_state"] in {"NORMAL", "PRE_ALERTA", "CONTENCION", "FALLA_SEGURA"}

    # 6. GET /api/v1/governance/fmea-and-spinoffs
    r_gov = client.get(
        "/api/v1/governance/fmea-and-spinoffs",
        params={"mitigated": True, "spinoff_id": "9582", "units": 25},
    )
    assert r_gov.status_code == 200
    gov_json = r_gov.json()
    assert len(gov_json["fmea_rows"]) >= 6
    assert gov_json["spinoff_metrics"]["spinoff_id"] == "9582"
    assert gov_json["spinoff_metrics"]["weight_saved_lb_total"] == 325.0

    # Contratos negativos OWASP (extra="forbid" -> 422, XSS -> 422, >16KB -> 413)
    r_extra = client.post(
        "/api/v1/sandbox/predict-flammability",
        json={
            "o2_pct": 21.0,
            "pressure_psi": 14.7,
            "flow_cm_s": 10.0,
            "gravity_g": 0.0,
            "material": "PMMA",
            "thickness_mm": 1.0,
            "flow_dir": "concurrent",
            "injected_extra": "boom",
        },
    )
    assert r_extra.status_code == 422
    assert r_extra.json()["error"]["code"] == "VALIDATION_ERROR"

    r_xss = client.post(
        "/api/v1/psi/rank-and-interpret",
        json={
            "weights": {"habitat": 1.0, "modeling": 1.0, "sensors": 1.0, "spinoff": 1.0},
            "persona": "Estudiante",
            "query": "<script>alert(1)</script>",
        },
    )
    assert r_xss.status_code == 422

    r_413 = client.post(
        "/api/v1/psi/rank-and-interpret",
        json={
            "weights": {"habitat": 1.0, "modeling": 1.0, "sensors": 1.0, "spinoff": 1.0},
            "persona": "Estudiante",
            "query": "A" * 17000,
        },
    )
    assert r_413.status_code == 413
