from __future__ import annotations

from pathlib import Path
import re

ROOT_DIR = Path(__file__).resolve().parents[2]
DECK_PATH = ROOT_DIR / "docs" / "pitch" / "deck_7_slides.md"

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


def test_pitch_deck_has_exact_7_slides_and_sections() -> None:
    assert DECK_PATH.is_file(), "Falta docs/pitch/deck_7_slides.md"
    content = DECK_PATH.read_text(encoding="utf-8")
    slides = re.findall(r"^## Slide (\d+):", content, flags=re.MULTILINE)
    assert slides == ["1", "2", "3", "4", "5", "6", "7"]
    assert len(re.findall(r"\*\*Composición Visual:\*\*", content)) == 7
    assert len(re.findall(r"\*\*Notas de Orador:\*\*", content)) == 7


def test_pitch_deck_covers_5_nasa_criteria_and_verified_metrics() -> None:
    content = DECK_PATH.read_text(encoding="utf-8")
    for criterion in ("Impact", "Creativity", "Validity", "Relevance", "Presentation"):
        assert criterion in content, f"Falta criterio oficial NASA: {criterion}"

    for token in (
        "24",
        "566",
        "Apollo 1",
        "Apollo 13",
        "Mir",
        "1901",
        "134",
        "92.95%",
        "9582",
        "9407",
        "9918",
        "PFE",
        "E-FIELD",
        "$0",
        "10.60555/",
    ):
        assert token in content, f"Falta metrica/referencia verificada en deck: {token}"


def test_pitch_deck_anti_slop_and_domain_c01() -> None:
    lowered = DECK_PATH.read_text(encoding="utf-8").lower()
    for slop in BANNED_AI_SLOP:
        assert slop not in lowered, f"AI slop detectado en deck_7_slides.md: {slop}"

    for forbidden in ("motor cohete", "motores cohete", "rocket engine", "thruster"):
        assert forbidden not in lowered, f"Violacion C-01 detectada en deck: {forbidden}"
