"""Pruebas de integracion para preparacion de despliegue en Render Free y UptimeRobot (M-12)."""

from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import create_app
from backend.security import SlidingWindowRateLimiter

ROOT_DIR = Path(__file__).resolve().parents[2]


def test_health_and_root_support_head_and_get_for_uptimerobot() -> None:
    app = create_app(
        data_dir=ROOT_DIR / "data",
        artifacts_dir=ROOT_DIR / "artifacts" / "models",
        frontend_dir=ROOT_DIR / "frontend",
    )
    client = TestClient(app)

    r_get = client.get("/api/v1/health")
    assert r_get.status_code == 200
    assert r_get.json()["status"] == "ok"

    # UptimeRobot Free envia HEAD cada 5 min por defecto
    r_head_health = client.head("/api/v1/health")
    assert r_head_health.status_code == 200
    assert r_head_health.headers["X-Frame-Options"] == "DENY"
    assert r_head_health.headers["X-Content-Type-Options"] == "nosniff"

    r_head_root = client.head("/")
    assert r_head_root.status_code == 200


def test_proxy_x_forwarded_for_isolates_rate_limit_buckets() -> None:
    limiter = SlidingWindowRateLimiter(bucket_limits={"general": 10, "ml": 1}, window_seconds=60.0)
    app = create_app(
        data_dir=ROOT_DIR / "data",
        artifacts_dir=ROOT_DIR / "artifacts" / "models",
        frontend_dir=ROOT_DIR / "frontend",
        rate_limiter=limiter,
    )
    client = TestClient(app)

    payload = {
        "o2_pct": 34.0,
        "pressure_psi": 8.2,
        "flow_cm_s": 12.0,
        "gravity_g": 0.16,
        "material": "SIBAL",
        "thickness_mm": 0.8,
        "flow_dir": "concurrent",
    }

    r1 = client.post("/api/v1/sandbox/predict-flammability", json=payload, headers={"X-Forwarded-For": "203.0.113.10, 10.0.0.1"})
    assert r1.status_code == 200

    # Mismo cliente en segundo intento excede limite ml=1 -> 429
    r2 = client.post("/api/v1/sandbox/predict-flammability", json=payload, headers={"X-Forwarded-For": "203.0.113.10, 10.0.0.2"})
    assert r2.status_code == 429

    # Cliente distinto detras del reverse proxy de Render mantiene su propio cupo -> 200
    r3 = client.post("/api/v1/sandbox/predict-flammability", json=payload, headers={"X-Forwarded-For": "203.0.113.25"})
    assert r3.status_code == 200


def test_render_docker_and_requirements_lightweight_contract() -> None:
    render_yaml = (ROOT_DIR / "render.yaml").read_text(encoding="utf-8")
    dockerfile = (ROOT_DIR / "Dockerfile").read_text(encoding="utf-8")
    dockerignore = (ROOT_DIR / ".dockerignore").read_text(encoding="utf-8")
    netlify_toml = (ROOT_DIR / "netlify.toml").read_text(encoding="utf-8")
    base_req = (ROOT_DIR / "requirements" / "base.txt").read_text(encoding="utf-8").lower()
    dev_req = (ROOT_DIR / "requirements" / "dev.txt").read_text(encoding="utf-8").lower()

    assert "healthCheckPath: /api/v1/health" in render_yaml
    assert "--port $PORT" in render_yaml
    assert "plan: free" in render_yaml
    assert "backend.main:app" in dockerfile
    assert "/api/v1/health" in dockerfile
    assert "USER appuser" in dockerfile
    assert "graphify-out" in dockerignore
    assert 'publish = "frontend"' in netlify_toml

    # Produccion (Render 512 MB RAM) excluye torch/pandas/pytest y mantiene runtime ONNX/sklearn
    for forbidden_prod in ("torch", "pandas", "pytest"):
        assert forbidden_prod not in base_req
        assert forbidden_prod in dev_req
    for required_prod in ("fastapi", "uvicorn", "onnxruntime", "scikit-learn", "joblib", "numpy"):
        assert required_prod in base_req
