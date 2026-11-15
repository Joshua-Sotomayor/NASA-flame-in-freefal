"""Pruebas de integracion Web, arranque directo, requisitos, Mini Museo, Glosario y auditoria de redaccion."""

import ast
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient

from backend.main import create_app

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
BACKEND_DIR = ROOT_DIR / "backend"
REQUIREMENTS_DIR = ROOT_DIR / "requirements"

BANNED_AI_SLOP = (
    "en el panorama actual",
    "sin fisuras",
    "piedra angular",
    "cambio de paradigma",
    "revolucionario",
    "revolucionaria",
    "demuestra universalmente",
)

BANNED_PUBLIC_DEV_JARGON = (
    "fastapi",
    "cero llm",
    "cero apis",
    "costo $0",
    "sha-256",
    "randomforest",
    "decisiontree",
    "tf-idf",
    "flame_cnn.onnx",
    "writing-craft",
)


def test_backend_direct_execution_from_backend_dir_and_requirements() -> None:
    # Verifica que main.py registra la raiz del repo en sys.path (evita ModuleNotFoundError en `cd backend && py main.py`)
    main_src = (BACKEND_DIR / "main.py").read_text(encoding="utf-8")
    assert "sys.path.insert(0, str(DEFAULT_ROOT_DIR))" in main_src
    assert 'if __name__ == "__main__":' in main_src

    train_src = (BACKEND_DIR / "train_models.py").read_text(encoding="utf-8")
    assert "sys.path.insert(0, str(ROOT_DIR))" in train_src

    # Subproceso liviano desde backend/ validando resolucion de paquetes backend.* sin recargar PyTorch/SciPy en pytest
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import pathlib, sys; "
                "root = pathlib.Path('main.py').resolve().parents[1]; "
                "sys.path = [p for p in sys.path if pathlib.Path(p or '.').resolve() != root]; "
                "sys.path.insert(0, str(root)); "
                "from backend.domain import PsiRepository; "
                "from backend.security import SecurityBoundaryGuard; "
                "assert PsiRepository is not None and SecurityBoundaryGuard is not None"
            ),
        ],
        cwd=str(BACKEND_DIR),
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert proc.returncode == 0, f"Fallo al resolver paquete backend desde backend/: {proc.stderr}"

    assert (ROOT_DIR / "requirements.txt").is_file()
    base_req = (REQUIREMENTS_DIR / "base.txt").read_text(encoding="utf-8")
    dev_req = (REQUIREMENTS_DIR / "dev.txt").read_text(encoding="utf-8")
    assert "fastapi" in base_req.lower()
    assert "uvicorn" in base_req.lower()
    assert "pytest" in dev_req.lower()


def test_frontend_served_and_structural_requirements() -> None:
    app = create_app(data_dir=ROOT_DIR / "data", artifacts_dir=ROOT_DIR / "artifacts" / "models")
    client = TestClient(app)

    r_root = client.get("/")
    assert r_root.status_code == 200
    assert "AERO-IGNIS SI" in r_root.text
    assert "NASA" in r_root.text
    assert "ENREDADOS" in r_root.text
    assert 'role="tablist"' in r_root.text
    assert 'role="tab"' in r_root.text
    assert 'role="tabpanel"' in r_root.text

    # M-06 / M-09 / M-10 / Mini Museo & Glosario
    assert 'id="ductDigitalTwinSvg"' in r_root.text
    assert 'id="flammabilityContourSvg"' in r_root.text
    assert 'id="panel-museum"' in r_root.text
    assert 'id="museumGallery"' in r_root.text
    assert 'id="glossaryGrid"' in r_root.text
    assert "/assets/museum/flame_0g.jpg" in r_root.text
    for tech in ("SolidWorks", "EPLAN", "Proteus"):
        assert tech in r_root.text

    # M-13 / M-14: Tema claro permanente (sin #themeBtn), sin badges tecnicos de encabezado y Museo primero
    assert 'id="themeBtn"' not in r_root.text
    assert 'data-theme="dark"' not in r_root.text
    assert "runtimeModeBadge" not in r_root.text
    assert "shaBadge" not in r_root.text
    assert "Catálogo Local Autónomo" not in r_root.text
    assert "Registros NASA Verificados" not in r_root.text
    assert '<select id="psiQueryInput">' in r_root.text
    assert 'id="fmeaCompareBanner"' in r_root.text
    assert 'id="suppAgentOut"' in r_root.text
    assert 'id="tab-museum" class="tab-btn" role="tab" aria-selected="true"' in r_root.text
    assert '<section id="panel-museum" class="tabpanel is-active"' in r_root.text
    assert r_root.text.index('id="tab-museum"') < r_root.text.index('id="tab-explorer"')

    # M-15 / M-16: Favicon NASA, sin tarjetas laterales, cuadrantes claros, Mermaid claro y botones uniformes
    assert '<link rel="icon"' in r_root.text
    assert 'id="tab-models"' in r_root.text
    assert 'id="panel-models"' in r_root.text
    assert 'id="orbitalBackdropCanvas"' in r_root.text
    assert "mission-decal-strip" in r_root.text
    assert "retro-decal-rail" not in r_root.text
    assert "quadrant-legend-grid" in r_root.text
    assert "flowchart LR" in r_root.text
    assert r_root.text.count("btn btn-cobalt") == 3
    assert "/api/v1/models/download/" in r_root.text

    r_fav_svg = client.get("/favicon.svg")
    assert r_fav_svg.status_code == 200
    assert "<svg" in r_fav_svg.text

    r_fav_ico = client.get("/favicon.ico")
    assert r_fav_ico.status_code == 200
    assert "<svg" in r_fav_ico.text

    for graph_name in ("ml_dl_colab_pipeline.svg", "psi_knowledge_graph.svg"):
        r_graph = client.get(f"/assets/graphs/{graph_name}")
        assert r_graph.status_code == 200
        assert "<svg" in r_graph.text
        assert "#F4F7FB" in r_graph.text

    for slug, expected_file in (
        ("flammability-rf", "flammability_rf.joblib"),
        ("flame-cnn", "flame_cnn.onnx"),
        ("code-train-local", "train_models.py"),
    ):
        r_dl = client.get(f"/api/v1/models/download/{slug}")
        assert r_dl.status_code == 200
        assert expected_file in r_dl.headers.get("content-disposition", "")

    assert client.get("/api/v1/models/download/nonexistent-slug").status_code == 404

    # Cero jerga interna de programacion o LLM en textos visibles de HTML
    lowered_html = r_root.text.lower()
    for term in BANNED_PUBLIC_DEV_JARGON:
        assert term not in lowered_html, f"Termino tecnico interno visible en UI: {term}"

    # Servido de assets estaticos locales y fotografia real NASA
    r_css = client.get("/frontend/styles.css")
    assert r_css.status_code == 200
    assert "prefers-reduced-motion" in r_css.text
    assert "Geist Pixel" in r_css.text
    assert "attr(data-label)" in r_css.text

    r_font = client.get("/GeistPixel-Square.woff2")
    assert r_font.status_code == 200
    assert r_font.content[:4] == b"wOF2"

    r_img = client.get("/assets/museum/flame_0g.jpg")
    assert r_img.status_code == 200
    assert r_img.content[:3] == b"\xff\xd8\xff"

    r_js = client.get("/frontend/app.js")
    assert r_js.status_code == 200
    assert "escapeHtml" in r_js.text
    assert "toggleTheme" not in r_js.text
    assert "data-label=" in r_js.text
    assert "initOrbitalBackdrop" in r_js.text
    assert "PSI_PLAIN_GUIDE" in r_js.text
    lowered_js = r_js.text.lower()
    for term in BANNED_PUBLIC_DEV_JARGON:
        assert term not in lowered_js, f"Termino tecnico interno visible en app.js: {term}"


def test_ponytail_security_and_anti_slop_audit() -> None:
    # Cero API keys, cero eval/exec/shell=True, cero frases AI slop
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
