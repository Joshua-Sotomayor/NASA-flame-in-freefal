"""Pruebas unitarias (RED -> GREEN) para fisica adimensional y presets forenses (`backend.physics_ml`)."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import pytest

from backend.physics_ml import (
    AtmosphericState,
    DimensionlessPhysicsCalculator,
    PhysicsMetrics,
    load_forensic_presets,
)

ROOT_DIR = Path(__file__).resolve().parents[2]


def test_atmospheric_state_is_frozen_and_validates_ranges() -> None:
    state = AtmosphericState(
        o2_pct=34.0,
        pressure_psi=8.2,
        flow_cm_s=12.0,
        gravity_g=0.16,
        material="SIBAL",
        thickness_mm=0.8,
        flow_dir="concurrent",
    )
    with pytest.raises(FrozenInstanceError):
        state.o2_pct = 21.0  # type: ignore[misc]

    with pytest.raises(ValueError):
        AtmosphericState(
            o2_pct=105.0,
            pressure_psi=14.7,
            flow_cm_s=10.0,
            gravity_g=0.0,
            material="SIBAL",
            thickness_mm=1.0,
            flow_dir="concurrent",
        )


def test_damkohler_and_peclet_equations() -> None:
    calc = DimensionlessPhysicsCalculator()

    # Flujo muy bajo en 0g -> Peclet < 1 y Extincion Radiativa (Quenching)
    low_flow = AtmosphericState(
        o2_pct=21.0,
        pressure_psi=14.7,
        flow_cm_s=0.6,
        gravity_g=0.0,
        material="PMMA",
        thickness_mm=0.8,
        flow_dir="opposed",
    )
    m_low: PhysicsMetrics = calc.compute_dimensionless(low_flow)
    assert m_low.peclet < 1.0
    assert m_low.regime == "Extinción Radiativa (Quenching)"

    # Flujo intermedio en 0g con O2 nominal/enriquecido -> Propagacion Estable 0g
    mid_flow = AtmosphericState(
        o2_pct=24.0,
        pressure_psi=14.7,
        flow_cm_s=14.0,
        gravity_g=0.0,
        material="SIBAL",
        thickness_mm=0.8,
        flow_dir="concurrent",
    )
    m_mid = calc.compute_dimensionless(mid_flow)
    assert m_mid.peclet >= 1.0
    assert m_mid.regime == "Propagación Estable 0g"

    # Flujo muy alto con bajo Da -> Extincion por Soplado (Blowoff)
    high_flow = AtmosphericState(
        o2_pct=19.0,
        pressure_psi=14.7,
        flow_cm_s=52.0,
        gravity_g=0.0,
        material="Nomex",
        thickness_mm=1.5,
        flow_dir="opposed",
    )
    m_high = calc.compute_dimensionless(high_flow)
    assert m_high.damkohler < 1.2
    assert m_high.regime == "Extinción por Soplado (Blowoff)"


def test_monotonic_risk_with_oxygen() -> None:
    calc = DimensionlessPhysicsCalculator()
    spreads = []
    ext_probs = []
    for o2 in (18.0, 34.0, 100.0):
        metrics = calc.compute_dimensionless(
            AtmosphericState(
                o2_pct=o2,
                pressure_psi=14.7,
                flow_cm_s=15.0,
                gravity_g=0.0,
                material="SIBAL",
                thickness_mm=0.8,
                flow_dir="concurrent",
            )
        )
        spreads.append(metrics.flame_spread_mm_s)
        ext_probs.append(metrics.extinguished_prob_prior)

    assert spreads[0] < spreads[1] < spreads[2]
    assert ext_probs[0] > ext_probs[1] > ext_probs[2]


def test_forensic_presets_apollo1_apollo13_mir() -> None:
    presets = load_forensic_presets(ROOT_DIR / "data" / "cases_and_spinoffs.json")
    assert presets["apollo_1"]["o2_pct"] == 100.0
    assert presets["apollo_1"]["pressure_psi"] == 16.7
    assert "PTFE" in presets["apollo_1"]["material"]

    assert presets["apollo_13"]["o2_pct"] == 100.0
    assert presets["apollo_13"]["pressure_psi"] == 30.0
    assert "1,000 psi" in presets["apollo_13"]["pressure_note"]

    assert presets["mir_1997"]["o2_pct"] == 21.0
    assert "LiClO4" in presets["mir_1997"]["material"]
