from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.governance import GovernanceAndSpinoffService, SuppressionRecommendation


@pytest.fixture
def isolated_governance_service(tmp_path: Path) -> GovernanceAndSpinoffService:
    """Fixture unitario aislado sin lectura de archivos reales del disco."""
    payload = {"fmea_modes": [], "spinoffs": [], "official_resources": []}
    json_path = tmp_path / "cases_empty.json"
    json_path.write_text(json.dumps(payload), encoding="utf-8")
    return GovernanceAndSpinoffService(json_path)


def test_suppression_recommendation_is_frozen_value_object() -> None:
    rec = SuppressionRecommendation(
        recommended_agent="PFE",
        rationale="Niebla fina certificada para cabina ISS.",
        eclss_safe=True,
    )
    with pytest.raises(FrozenInstanceError):
        rec.recommended_agent = "CO2"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("fire_type", "auto_oxidizing"),
    [
        ("auto_oxidizing", False),
        ("vika", False),
        ("liclo4", False),
        ("smoldering", False),
        ("laminar_diffusion", True),
        ("uncrewed_rack", True),
    ],
)
def test_auto_oxidizing_and_vika_force_pfe_override(
    isolated_governance_service: GovernanceAndSpinoffService,
    fire_type: str,
    auto_oxidizing: bool,
) -> None:
    """Reacciones auto-oxidantes (Vika/LiClO4) o latentes deben prescribir PFE."""
    rec = isolated_governance_service.select_suppression_protocol(
        fire_type=fire_type,
        habitable_crew=False,
        auto_oxidizing=auto_oxidizing,
    )
    assert rec.recommended_agent == "PFE"
    assert rec.eclss_safe is True
    assert "2,260 kJ/kg" in rec.rationale
    assert "20-100 um" in rec.rationale


@pytest.mark.parametrize("fire_type", ["laminar_diffusion", "electronic_clean", "efield"])
def test_efield_selected_for_clean_laminar_flames_without_auto_oxidizer(
    isolated_governance_service: GovernanceAndSpinoffService,
    fire_type: str,
) -> None:
    """Llamas laminares limpias usan campo electrico PSI-154 sin consumir agente."""
    rec = isolated_governance_service.select_suppression_protocol(
        fire_type=fire_type,
        habitable_crew=True,
        auto_oxidizing=False,
    )
    assert rec.recommended_agent == "E-FIELD"
    assert rec.eclss_safe is True
    assert "PSI-154" in rec.rationale
    assert "10 kV" in rec.rationale


def test_co2_blocked_when_habitable_crew_present(
    isolated_governance_service: GovernanceAndSpinoffService,
) -> None:
    """En volumen habitable con tripulacion nunca se permite CO2 por hipercapnia."""
    crewed = isolated_governance_service.select_suppression_protocol(
        fire_type="cargo_co2",
        habitable_crew=True,
        auto_oxidizing=False,
    )
    assert crewed.recommended_agent == "PFE"
    assert crewed.eclss_safe is True

    uncrewed = isolated_governance_service.select_suppression_protocol(
        fire_type="uncrewed_rack",
        habitable_crew=False,
        auto_oxidizing=False,
    )
    assert uncrewed.recommended_agent == "CO2"
    assert uncrewed.eclss_safe is False
    assert "hipercapnia" in uncrewed.rationale.lower()


@pytest.mark.parametrize("fire_type", ["halon", "halon_1301", "polymer_general"])
def test_halon_and_general_cabin_fires_prescribe_pfe_free_of_hf_hbr(
    isolated_governance_service: GovernanceAndSpinoffService,
    fire_type: str,
) -> None:
    """Todo incendio de cabina evita Halon 1301 (HF/HBr) prescribiendo PFE."""
    rec = isolated_governance_service.select_suppression_protocol(
        fire_type=fire_type,
        habitable_crew=True,
        auto_oxidizing=False,
    )
    assert rec.recommended_agent == "PFE"
    assert rec.eclss_safe is True
    assert "HF/HBr" in rec.rationale


@pytest.mark.parametrize("blank_fire_type", ["", "   ", "\t\n"])
def test_blank_fire_type_raises_value_error(
    isolated_governance_service: GovernanceAndSpinoffService,
    blank_fire_type: str,
) -> None:
    """Entrada vacia debe fallar de forma explicita (TDD guard clause)."""
    with pytest.raises(ValueError, match="fire_type"):
        isolated_governance_service.select_suppression_protocol(fire_type=blank_fire_type)
