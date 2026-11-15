from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.duct_twin import SensorTelemetryFrame
from backend.physics_ml import AtmosphericState, VALID_GRAVITIES

PSI_TO_KPA = 6.894757
LB_TO_KG = 0.45359237

PSI_JSON = ROOT_DIR / "data" / "psi_combustion_24.json"
RUNS_CSV = ROOT_DIR / "data" / "bass_saffire_runs.csv"
CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"

FORBIDDEN_PROPULSION_TERMS = (
    "motor cohete",
    "motores cohete",
    "rocket engine",
    "thruster",
    "tobera",
    "solid rocket",
    "liquid propellant",
)


def test_atmospheric_unit_conversions_and_bounds() -> None:
    """Verifica coherencia psi -> atm -> kPa, mm -> cm y cm/s en AtmosphericState."""
    iss = AtmosphericState(
        o2_pct=21.0,
        pressure_psi=14.7,
        flow_cm_s=20.0,
        gravity_g=0.0,
        material="SIBAL",
        thickness_mm=10.0,
        flow_dir="concurrent",
    )
    vec = iss.to_feature_array()[0]
    assert vec[0] == pytest.approx(21.0)
    assert vec[1] == pytest.approx(1.0, rel=1e-6)  # 14.7 psi == 1.0 atm
    assert vec[2] == pytest.approx(20.0)  # cm/s
    assert vec[3] == pytest.approx(0.0)  # 0g
    assert vec[4] == pytest.approx(1.0, rel=1e-6)  # 10 mm == 1.0 cm

    lunar_kpa = 8.2 * PSI_TO_KPA
    assert lunar_kpa == pytest.approx(56.537, abs=0.01)


def test_psi_24_and_bass_saffire_csv_unit_consistency() -> None:
    """Valida unidades y rangos fisicos en las 24 PSI y 566 corridas BASS-II/Saffire."""
    psi_data = json.loads(PSI_JSON.read_text(encoding="utf-8"))
    investigations = psi_data["investigations"]
    assert len(investigations) == 24
    for inv in investigations:
        assert 10.0 <= float(inv["o2_min"]) <= float(inv["o2_max"]) <= 100.0
        assert 1.0 <= float(inv["pressure_psi_min"]) <= float(inv["pressure_psi_max"]) <= 30.0
        assert 0.0 <= float(inv["flow_cm_s_max"]) <= 60.0
        p_kpa_max = float(inv["pressure_psi_max"]) * PSI_TO_KPA
        assert 50.0 <= p_kpa_max <= 210.0

    with RUNS_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) >= 500
    for row in rows:
        o2 = float(row["o2_pct"])
        psi = float(row["pressure_psi"])
        flow = float(row["flow_cm_s"])
        grav = float(row["gravity_g"])
        thick = float(row["thickness_mm"])
        da = float(row["damkohler"])
        pe = float(row["peclet"])
        burn = float(row["burn_time_s"])
        vf = float(row["flame_spread_mm_s"])
        assert 10.0 <= o2 <= 100.0
        assert 1.0 <= psi <= 30.0
        assert 0.0 <= flow <= 60.0
        assert any(math.isclose(grav, g, abs_tol=1e-4) for g in VALID_GRAVITIES)
        assert 0.1 <= thick <= 50.0
        assert da >= 0.0 and pe >= 0.0 and burn > 0.0 and vf >= 0.0


def test_cases_spinoffs_and_telemetry_unit_consistency() -> None:
    """Valida unidades historicas en casos forenses, Spinoffs lb->kg y trama de ducto."""
    cases = json.loads(CASES_JSON.read_text(encoding="utf-8"))
    presets = {item["case_id"]: item for item in cases["forensic_cases"]}
    assert presets["apollo_1"]["o2_pct"] == pytest.approx(100.0)
    assert presets["apollo_1"]["pressure_psi"] == pytest.approx(16.7)
    assert presets["apollo_13"]["pressure_psi"] == pytest.approx(30.0)
    assert presets["mir_1997"]["o2_pct"] == pytest.approx(21.0)
    assert presets["lunar_artemis"]["pressure_psi"] == pytest.approx(8.2)
    assert presets["lunar_artemis"]["o2_pct"] == pytest.approx(34.0)

    for sp in cases["spinoffs"]:
        lb = float(sp["weight_saved_lb_per_unit"])
        assert lb >= 0.0
        assert lb * LB_TO_KG >= 0.0
        assert 0.0 < float(sp["risk_reduction_pct"]) <= 100.0

    frame = SensorTelemetryFrame(delta_t_dt=2.5, co_ppm=35.0, submicron_aerosol=15.0, airflow_cm_s=12.0)
    assert frame.to_feature_array().shape == (1, 4)


def test_domain_scope_c01_excludes_rocket_propulsion() -> None:
    """Audita C-01: cero terminologia de motores cohete o propulsores en app, datos y UI."""
    targets = [
        PSI_JSON,
        RUNS_CSV,
        CASES_JSON,
        ROOT_DIR / "backend" / "domain.py",
        ROOT_DIR / "backend" / "physics_ml.py",
        ROOT_DIR / "backend" / "duct_twin.py",
        ROOT_DIR / "backend" / "ranking_nlp.py",
        ROOT_DIR / "backend" / "governance.py",
        ROOT_DIR / "frontend" / "index.html",
        ROOT_DIR / "frontend" / "app.js",
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_PROPULSION_TERMS:
            assert term not in text, f"Violacion de alcance C-01 ({term}) en {path.name}"
