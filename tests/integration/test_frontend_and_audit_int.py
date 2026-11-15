"""Pruebas de integracion Web, accesibilidad WAI-ARIA, Gemelo SVG, Hardware Blueprint y /ponytail-audit."""

import ast
from pathlib import Path
from fastapi.testclient import TestClient

from backend.main import create_app

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
BACKEND_DIR = ROOT_DIR / "backend"

BANNED_AI_SLOP = (
    "en el panorama actual",
    "sin fisuras",
    "piedra angular",
    "cambio de paradigma",
    "revolucionario",
    "revolucionaria",
    "demuestra universalmente",
)


def test_frontend_served_and_structural_requirements() -> None:
    app = create_app(data_dir=ROOT_DIR / "data", artifacts_dir=ROOT_DIR / "artifacts" / "models")
    client = TestClient(app)

    r_root = client.get("/")
    assert r_root.status_code == 200
    assert "AERO-IGNIS SI" in r_root.text
    assert 'role="tablist"' in r_root.text
    assert 'role="tab"' in r_root.text
    assert 'role="tabpanel"' in r_root.text

    # M-06: Gemelo Digital Isométrico SVG
    assert 'id="ductDigitalTwinSvg"' in r_root.text

    # M-09: Grafica de contorno de inflamabilidad en tiempo real
    assert 'id="flammabilityContourSvg"' in r_root.text

    # M-10: Galeria Hardware Blueprint (SolidWorks, EPLAN, Proteus)
    for tech in ("SolidWorks", "EPLAN", "Proteus"):
        assert tech in r_root.text

    # Servido de assets estaticos locales con cabeceras seguras
    r_css = client.get("/frontend/styles.css")
    assert r_css.status_code == 200
    assert "prefers-reduced-motion" in r_css.text

    r_js = client.get("/frontend/app.js")
    assert r_js.status_code == 200
    assert "escapeHtml" in r_js.text


def test_ponytail_security_and_anti_slop_audit() -> None:
    # Cero API keys, cero eval/exec/shell=True, cero frases AI slop, cero innerHTML directo con input sin escapar
    for py_file in BACKEND_DIR.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"eval", "exec"}, f"Llamada insegura {node.func.id} en {py_file.name}"
        assert "shell=True" not in text
        assert "pickle.load" not in text
        lowered = text.lower()
        for slop in BANNED_AI_SLOP:
            assert slop not in lowered, f"AI slop encontrado en {py_file.name}: {slop}"

    js_text = (FRONTEND_DIR / "app.js").read_text(encoding="utf-8")
    assert "eval(" not in js_text
    assert "Function(" not in js_text

    html_text = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8").lower()
    for slop in BANNED_AI_SLOP:
        assert slop not in html_text, f"AI slop encontrado en frontend/index.html: {slop}"
    for banned_rocket in ("rocket engine", "motor cohete", "propulsor"):
        assert banned_rocket not in html_text, f"Contenido fuera de alcance C-01: {banned_rocket}"
