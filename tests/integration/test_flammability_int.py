"""Pruebas de integracion para FlammabilityPredictor con RandomForest/GBR verificados SHA-256."""

from pathlib import Path
from backend.physics_ml import AtmosphericState, FlammabilityPredictor
from backend.security import SecurityBoundaryGuard

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT_DIR / "artifacts" / "models"


def test_flammability_predictor_integration_with_sha256() -> None:
    guard = SecurityBoundaryGuard()
    predictor = FlammabilityPredictor.from_artifacts(
        artifacts_dir=ARTIFACTS_DIR,
        guard=guard,
    )

    # 1. Habitat Lunar Artemis (34% O2, 8.2 psi, SIBAL)
    lunar_pred = predictor.predict(
        AtmosphericState(
            o2_pct=34.0,
            pressure_psi=8.2,
            flow_cm_s=12.0,
            gravity_g=0.16,
            material="SIBAL",
            thickness_mm=0.8,
            flow_dir="concurrent",
        )
    )
    assert 0.0 <= lunar_pred.extinguished_prob <= 1.0
    assert lunar_pred.burn_time_s > 0.0
    assert lunar_pred.flame_spread_mm_s > 0.0
    assert len(lunar_pred.feature_importance) >= 5
    importances = [item.importance for item in lunar_pred.feature_importance]
    assert importances == sorted(importances, reverse=True)
    assert abs(sum(importances) - 1.0) < 1e-2

    # 2. Escenario forense Apollo 1 (100% O2, 16.7 psi) vs 18% O2
    apollo1_pred = predictor.predict(
        AtmosphericState(
            o2_pct=100.0,
            pressure_psi=16.7,
            flow_cm_s=5.0,
            gravity_g=1.0,
            material="PMMA",
            thickness_mm=2.0,
            flow_dir="concurrent",
        )
    )
    hypoxic_pred = predictor.predict(
        AtmosphericState(
            o2_pct=18.0,
            pressure_psi=10.2,
            flow_cm_s=1.0,
            gravity_g=0.0,
            material="Nomex",
            thickness_mm=2.0,
            flow_dir="opposed",
        )
    )
    assert apollo1_pred.flame_spread_mm_s > lunar_pred.flame_spread_mm_s > hypoxic_pred.flame_spread_mm_s
    assert apollo1_pred.extinguished_prob < hypoxic_pred.extinguished_prob
