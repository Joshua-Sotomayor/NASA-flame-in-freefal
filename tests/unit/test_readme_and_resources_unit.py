from __future__ import annotations

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
README_PATH = ROOT_DIR / "README.md"
CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"

BANNED_AI_SLOP = (
    "en el panorama actual",
    "sin fisuras",
    "piedra angular",
    "cambio de paradigma",
    "revolucionario",
    "revolucionaria",
    "demuestra universalmente",
    "game-changer",
    "paradigm shift",
)


def test_readme_cites_all_10_official_nasa_resources() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    cases = json.loads(CASES_JSON.read_text(encoding="utf-8"))
    resources = cases["official_resources"]
    assert len(resources) == 10
    for item in resources:
        assert item["url"] in readme, f"Falta recurso oficial NASA {item['tag']} en README.md"


def test_readme_covers_spinoffs_forensic_cases_licenses_and_reproducibility() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    for token in ("9582", "9407", "9918", "PFE", "Apollo 1", "Apollo 13", "Mir", "MIT", "CC0-1.0", "$0"):
        assert token in readme, f"Falta elemento clave en README.md: {token}"
    for cmd in ("requirements/dev.txt", "py main.py", "pytest"):
        assert cmd in readme, f"Falta instruccion reproducible en README.md: {cmd}"


def test_readme_anti_slop_and_valid_repo_paths() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    lowered = readme.lower()
    for slop in BANNED_AI_SLOP:
        assert slop not in lowered, f"AI slop detectado en README.md: {slop}"

    for rel in ("LICENSE", "SPEC.md", "AGENTS.md", "tasks/todo.md", "planning/index.html", "backend/main.py"):
        assert (ROOT_DIR / rel).is_file()
        assert rel in readme
