from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.governance import DualUseImpact, GovernanceAndSpinoffService

CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"
PSI_JSON = ROOT_DIR / "data" / "psi_combustion_24.json"


@pytest.fixture
def isolated_dual_use_service(tmp_path: Path) -> GovernanceAndSpinoffService:
    """Fixture unitario aislado con los 4 spinoffs oficiales para pruebas rapidas."""
    payload = {
        "fmea_modes": [],
        "official_resources": [],
        "spinoffs": [
            {
                "spinoff_id": "9582",
                "name": "Fireman's Air Tanks (COPV / PLSS)",
                "origin_nasa": "Tanques compuestos PLSS del programa Apollo",
                "earth_impact": "Elevo presion de 2,216 a 4,500 psi reduciendo peso del SCBA de 33 lb a 20 lb (-40%).",
                "weight_saved_lb_per_unit": 13.0,
                "risk_reduction_pct": 40.0,
                "linked_psi": "PSI-104",
                "url": "https://spinoff.nasa.gov/node/9582",
            },
            {
                "spinoff_id": "9407",
                "name": "Incipient Fire Detector (Space Shuttle / SAME)",
                "origin_nasa": "Discriminador de particulas en bahias de avionica del Transbordador",
                "earth_impact": "Detecta aerosoles submicronicos <0.1 um por pirolisis temprana antes de llama visible.",
                "weight_saved_lb_per_unit": 0.0,
                "risk_reduction_pct": 58.0,
                "linked_psi": "PSI-129",
                "url": "https://spinoff.nasa.gov/node/9407",
            },
            {
                "spinoff_id": "9918",
                "name": "New Technology for the Fire Attire (Project FIRES / PBI)",
                "origin_nasa": "Textiles ignifugos desarrollados tras Apollo 1",
                "earth_impact": "Trajes estructurales PBI + Nomex reduciendo peso total en >30% sin encoger ni emitir gases toxicos.",
                "weight_saved_lb_per_unit": 11.5,
                "risk_reduction_pct": 35.0,
                "linked_psi": "PSI-101",
                "url": "https://spinoff.nasa.gov/node/9918",
            },
            {
                "spinoff_id": "PFE",
                "name": "ISS Portable Fire Extinguisher (Fine Water Mist)",
                "origin_nasa": "Supresion limpia sin Halon ni asfixia por CO2 en la ISS",
                "earth_impact": "Atomiza microgotas Sauter 20-100 um seguras para electronica critica con expansion 1,700x.",
                "weight_saved_lb_per_unit": 4.2,
                "risk_reduction_pct": 65.0,
                "linked_psi": "PSI-107",
                "url": "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/",
            },
        ],
    }
    json_path = tmp_path / "dual_use_fixture.json"
    json_path.write_text(json.dumps(payload), encoding="utf-8")
    return GovernanceAndSpinoffService(json_path)


def test_dual_use_impact_is_frozen_and_rounds_dict() -> None:
    impact = DualUseImpact(
        spinoff_id="PFE",
        name="ISS PFE",
        units=3,
        origin_nasa="ISS",
        earth_impact="Fine water mist",
        weight_saved_lb_total=12.6000001,
        risk_reduction_pct=65.0,
        linked_psi="PSI-107",
        url="https://www.nasa.gov/",
    )
    with pytest.raises(FrozenInstanceError):
        impact.units = 10  # type: ignore[misc]
    assert impact.to_dict()["weight_saved_lb_total"] == 12.6


@pytest.mark.parametrize(
    ("spinoff_id", "units", "expected_lb", "expected_risk", "expected_psi"),
    [
        ("9582", 1, 13.0, 40.0, "PSI-104"),
        ("9582", 250, 3250.0, 40.0, "PSI-104"),
        ("9407", 500, 0.0, 58.0, "PSI-129"),
        ("9918", 40, 460.0, 35.0, "PSI-101"),
        ("PFE", 10, 42.0, 65.0, "PSI-107"),
    ],
)
def test_dual_use_linear_scaling_and_psi_links(
    isolated_dual_use_service: GovernanceAndSpinoffService,
    spinoff_id: str,
    units: int,
    expected_lb: float,
    expected_risk: float,
    expected_psi: str,
) -> None:
    result = isolated_dual_use_service.calculate_dual_use(spinoff_id=spinoff_id, units=units)
    assert result.spinoff_id == spinoff_id
    assert result.units == units
    assert result.weight_saved_lb_total == pytest.approx(expected_lb, rel=1e-6)
    assert result.risk_reduction_pct == expected_risk
    assert result.linked_psi == expected_psi


def test_dual_use_normalizes_whitespace_case_and_default_id(
    isolated_dual_use_service: GovernanceAndSpinoffService,
) -> None:
    default_res = isolated_dual_use_service.calculate_dual_use(spinoff_id=None, units=1)
    assert default_res.spinoff_id == "9582"

    normalized_pfe = isolated_dual_use_service.calculate_dual_use(spinoff_id=" pfe ", units=2)
    assert normalized_pfe.spinoff_id == "PFE"
    assert normalized_pfe.weight_saved_lb_total == pytest.approx(8.4, rel=1e-6)

    with pytest.raises(KeyError, match="9999"):
        isolated_dual_use_service.calculate_dual_use(spinoff_id="9999", units=1)


@pytest.mark.parametrize("bad_units", [0, -1, 10001, True, False])
def test_dual_use_rejects_out_of_range_or_bool_units(
    isolated_dual_use_service: GovernanceAndSpinoffService,
    bad_units: int | bool,
) -> None:
    with pytest.raises(ValueError, match="units"):
        isolated_dual_use_service.calculate_dual_use(spinoff_id="9582", units=bad_units)  # type: ignore[arg-type]


def test_real_spinoffs_json_matches_psi_links_and_domain_c01() -> None:
    cases = json.loads(CASES_JSON.read_text(encoding="utf-8"))
    psi_payload = json.loads(PSI_JSON.read_text(encoding="utf-8"))
    valid_psi_ids = {item["psi_id"] for item in psi_payload["investigations"]}

    spinoffs = cases["spinoffs"]
    assert [sp["spinoff_id"] for sp in spinoffs] == ["9582", "9407", "9918", "PFE"]
    forbidden = ("cohete", "propulsor", "rocket engine", "thruster")
    for sp in spinoffs:
        assert sp["linked_psi"] in valid_psi_ids
        assert sp["url"].startswith("https://")
        assert sp["weight_saved_lb_per_unit"] >= 0.0
        assert 0.0 < sp["risk_reduction_pct"] <= 100.0
        joined = f"{sp['name']} {sp['origin_nasa']} {sp['earth_impact']}".lower()
        assert not any(term in joined for term in forbidden)
