"""Motor fisico adimensional (Da, Pe, Vf) y predictor RandomForest/GBR en POO.

Cumple con los contratos de `SPEC.md` (`flammability-rf-physics`) verificando
SHA-256 de los pesos `.joblib` antes de deserializarlos e incorporando los
presets forenses historicos oficiales (Apollo 1, Apollo 13, Mir y Artemis).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
import math
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from backend.domain import FLAMMABILITY_FEATURES, MATERIAL_REACTIVITY_MAP
from backend.security import SecurityBoundaryGuard


VALID_GRAVITIES: tuple[float, ...] = (0.0, 0.16, 0.38, 1.0)
VALID_FLOW_DIRS: frozenset[str] = frozenset({"concurrent", "opposed"})

FEATURE_DISPLAY_LABELS: dict[str, str] = {
    "o2_pct": "Concentración O2 (%)",
    "material_reactivity": "Reactividad del Material",
    "thickness_cm": "Espesor de Muestra (cm)",
    "air_flow_cms": "Velocidad de Flujo (cm/s)",
    "pressure_atm": "Presión de Cabina (atm)",
    "flow_concurrent": "Dirección de Flujo",
    "gravity_g": "Nivel de Gravedad (g)",
}


@dataclass(frozen=True)
class AtmosphericState:
    """Estado termofisico y de cabina inmutable validado contra rangos de SPEC.md."""

    o2_pct: float
    pressure_psi: float
    flow_cm_s: float
    gravity_g: float
    material: str
    thickness_mm: float
    flow_dir: str

    def __post_init__(self) -> None:
        if not (10.0 <= self.o2_pct <= 100.0):
            raise ValueError("o2_pct debe estar entre 10 y 100%.")
        if not (1.0 <= self.pressure_psi <= 30.0):
            raise ValueError("pressure_psi debe estar entre 1 y 30 psi.")
        if not (0.0 <= self.flow_cm_s <= 60.0):
            raise ValueError("flow_cm_s debe estar entre 0 y 60 cm/s.")
        if not any(math.isclose(self.gravity_g, g, abs_tol=1e-4) for g in VALID_GRAVITIES):
            raise ValueError(f"gravity_g debe pertenecer a {VALID_GRAVITIES}.")
        if self.material not in MATERIAL_REACTIVITY_MAP:
            raise ValueError(f"Material no soportado: {self.material}")
        if not (0.1 <= self.thickness_mm <= 50.0):
            raise ValueError("thickness_mm debe estar entre 0.1 y 50 mm.")
        if self.flow_dir not in VALID_FLOW_DIRS:
            raise ValueError(f"flow_dir invalido: {self.flow_dir}")

    def to_feature_array(self) -> np.ndarray:
        """Convierte el estado al vector ordenado esperado por RF/GBR."""
        return np.array(
            [
                [
                    float(self.o2_pct),
                    float(self.pressure_psi) / 14.7,
                    float(self.flow_cm_s),
                    float(self.gravity_g),
                    float(self.thickness_mm) / 10.0,
                    1.0 if self.flow_dir == "concurrent" else 0.0,
                    float(MATERIAL_REACTIVITY_MAP[self.material]),
                ]
            ],
            dtype=np.float64,
        )


@dataclass(frozen=True)
class PhysicsMetrics:
    """Metricas adimensionales calculadas de primer principio."""

    damkohler: float
    peclet: float
    flammability_index: float
    extinguished_prob_prior: float
    burn_time_s_prior: float
    flame_spread_mm_s: float
    regime: str


@dataclass(frozen=True)
class FeatureContribution:
    """Contribucion relativa explicable de cada variable del Random Forest."""

    feature: str
    importance: float

    def to_dict(self) -> dict[str, Any]:
        return {"feature": self.feature, "importance": round(self.importance, 4)}


@dataclass(frozen=True)
class FlammabilityPrediction:
    """Resultado consolidado (fisica + ML) compatible con `/api/v1/sandbox/predict-flammability`."""

    extinguished_prob: float
    burn_time_s: float
    flame_spread_mm_s: float
    damkohler: float
    peclet: float
    regime: str
    feature_importance: tuple[FeatureContribution, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "extinguished_prob": round(self.extinguished_prob, 4),
            "burn_time_s": round(self.burn_time_s, 2),
            "flame_spread_mm_s": round(self.flame_spread_mm_s, 3),
            "damkohler": round(self.damkohler, 4),
            "peclet": round(self.peclet, 4),
            "regime": self.regime,
            "feature_importance": [item.to_dict() for item in self.feature_importance],
        }


class DimensionlessPhysicsCalculator:
    """Calculadora fisica determinista basada en grupos adimensionales Da y Pe."""

    def compute_dimensionless(self, state: AtmosphericState) -> PhysicsMetrics:
        """Evalua Damkohler, Peclet, velocidad de frente Vf y regimen de extincion."""
        m_fac = MATERIAL_REACTIVITY_MAP[state.material]
        o2_norm = state.o2_pct / 21.0
        p_atm = state.pressure_psi / 14.7
        flow_eff = max(0.3, state.flow_cm_s + 12.0 * (state.gravity_g**0.7))

        peclet = (flow_eff * max(0.3, state.thickness_mm)) / 1.8
        damkohler = (0.45 * m_fac * (o2_norm**2.1) * (p_atm**0.75)) / max(0.35, flow_eff * 0.08)

        dir_factor = 1.25 if state.flow_dir == "concurrent" else 0.85
        flam_idx = (
            (o2_norm**1.8)
            * m_fac
            * dir_factor
            * (1.0 / (0.65 + 0.35 * state.thickness_mm))
            * (p_atm**0.25)
        )

        # Prior fisico suave y estrictamente monotono con %O2
        flow_penalty = 0.0
        if state.flow_cm_s < 1.5 and math.isclose(state.gravity_g, 0.0, abs_tol=1e-4):
            flow_penalty = 0.32
        elif state.flow_cm_s >= 42.0 and damkohler < 1.2:
            flow_penalty = 0.28

        ext_prob_prior = 1.0 / (1.0 + math.exp(3.4 * (flam_idx - 0.78 - flow_penalty)))
        excess_o2 = max(0.0, state.o2_pct - 34.0) * 0.14
        vf_prior = max(
            0.05,
            2.4 * flam_idx * (1.0 + 0.025 * min(state.flow_cm_s, 30.0)) + excess_o2,
        )
        burn_prior = min(180.0, max(2.0, (24.0 * state.thickness_mm / max(0.3, vf_prior**0.55)) * 2.1))

        if state.flow_cm_s < 1.5 and math.isclose(state.gravity_g, 0.0, abs_tol=1e-4) and state.o2_pct < 26.0:
            regime = "Extinción Radiativa (Quenching)"
        elif state.flow_cm_s >= 42.0 and state.o2_pct <= 24.0 and damkohler < 1.2:
            regime = "Extinción por Soplado (Blowoff)"
        elif flam_idx < 0.72:
            regime = "Extinción Radiativa (Quenching)"
        elif state.o2_pct >= 32.0 or state.gravity_g >= 0.9:
            regime = "Propagación Acelerada"
        elif math.isclose(state.gravity_g, 0.0, abs_tol=1e-4):
            regime = "Propagación Estable 0g"
        else:
            regime = "Propagación Parcial-g"

        return PhysicsMetrics(
            damkohler=round(damkohler, 4),
            peclet=round(peclet, 4),
            flammability_index=round(flam_idx, 4),
            extinguished_prob_prior=round(ext_prob_prior, 4),
            burn_time_s_prior=round(burn_prior, 2),
            flame_spread_mm_s=round(vf_prior, 3),
            regime=regime,
        )


class FlammabilityPredictor:
    """Combina fisica adimensional con RandomForestClassifier y GradientBoostingRegressor."""

    def __init__(
        self,
        rf_model: Any,
        burn_model: Any,
        spread_model: Any,
        feature_names: tuple[str, ...] = FLAMMABILITY_FEATURES,
        calculator: DimensionlessPhysicsCalculator | None = None,
    ) -> None:
        self._rf_model = rf_model
        self._burn_model = burn_model
        self._spread_model = spread_model
        self._feature_names = tuple(feature_names)
        self._calculator = calculator or DimensionlessPhysicsCalculator()

    @classmethod
    def from_artifacts(
        cls,
        artifacts_dir: Path,
        guard: SecurityBoundaryGuard,
    ) -> "FlammabilityPredictor":
        """Carga modelos verificando SHA-256 contra `manifest.sha256.json` antes de deserializar."""
        base_dir = Path(artifacts_dir)
        manifest_path = base_dir / "manifest.sha256.json"
        rf_path = base_dir / "flammability_rf.joblib"
        gbr_path = base_dir / "burntime_gbr.joblib"

        guard.verify_model_sha256(rf_path, manifest_path)
        guard.verify_model_sha256(gbr_path, manifest_path)

        rf_bundle = joblib.load(rf_path)
        gbr_bundle = joblib.load(gbr_path)

        return cls(
            rf_model=rf_bundle["model"],
            burn_model=gbr_bundle["burn_time_model"],
            spread_model=gbr_bundle["spread_model"],
            feature_names=tuple(rf_bundle.get("feature_names", FLAMMABILITY_FEATURES)),
        )

    @staticmethod
    def _metric_delta(base: PhysicsMetrics, m_a: PhysicsMetrics, m_b: PhysicsMetrics) -> float:
        """Cuantifica la variacion relativa combinada de Vf, extincion y Damkohler."""
        vf_scale = max(0.25, 0.5 * (m_a.flame_spread_mm_s + m_b.flame_spread_mm_s), 0.5 * base.flame_spread_mm_s)
        da_scale = max(0.25, 0.5 * (m_a.damkohler + m_b.damkohler), 0.5 * base.damkohler)
        return (
            abs(m_a.flame_spread_mm_s - m_b.flame_spread_mm_s) / vf_scale
            + 3.0 * abs(m_a.extinguished_prob_prior - m_b.extinguished_prob_prior)
            + abs(m_a.damkohler - m_b.damkohler) / da_scale
        )

    def _compute_local_sensitivities(
        self,
        state: AtmosphericState,
        base: PhysicsMetrics,
    ) -> dict[str, float]:
        """Calcula sensibilidad fisica local determinista alrededor del estado actual."""
        calc = self._calculator
        sensitivities: dict[str, float] = {}

        lo_o2 = max(10.0, state.o2_pct - 3.0)
        hi_o2 = min(100.0, state.o2_pct + 3.0)
        o2_delta = self._metric_delta(
            base,
            calc.compute_dimensionless(replace(state, o2_pct=lo_o2)),
            calc.compute_dimensionless(replace(state, o2_pct=hi_o2)),
        )
        sensitivities["o2_pct"] = (
            o2_delta
            * (6.0 / max(1e-6, hi_o2 - lo_o2))
            * (1.0 + 0.02 * max(0.0, state.o2_pct - 21.0))
        )

        lo_p = max(1.0, state.pressure_psi - 2.5)
        hi_p = min(30.0, state.pressure_psi + 2.5)
        p_delta = self._metric_delta(
            base,
            calc.compute_dimensionless(replace(state, pressure_psi=lo_p)),
            calc.compute_dimensionless(replace(state, pressure_psi=hi_p)),
        )
        sensitivities["pressure_atm"] = (
            p_delta
            * (5.0 / max(1e-6, hi_p - lo_p))
            * (0.9 + 0.08 * state.pressure_psi)
        )

        lo_t = (
            max(0.2, state.thickness_mm * 0.75)
            if state.thickness_mm >= 0.25
            else max(0.1, state.thickness_mm * 0.75)
        )
        hi_t = min(50.0, max(lo_t + 0.05, state.thickness_mm * 1.25))
        t_delta = self._metric_delta(
            base,
            calc.compute_dimensionless(replace(state, thickness_mm=lo_t)),
            calc.compute_dimensionless(replace(state, thickness_mm=hi_t)),
        )
        sensitivities["thickness_cm"] = (
            t_delta
            * ((0.5 * state.thickness_mm) / max(1e-6, hi_t - lo_t))
            * (1.0 + 0.08 * min(state.thickness_mm, 15.0))
        )

        lo_f = max(0.0, state.flow_cm_s - 4.0)
        hi_f = min(60.0, state.flow_cm_s + 4.0)
        f_delta = self._metric_delta(
            base,
            calc.compute_dimensionless(replace(state, flow_cm_s=lo_f)),
            calc.compute_dimensionless(replace(state, flow_cm_s=hi_f)),
        ) * (8.0 / max(1e-6, hi_f - lo_f))
        if state.flow_cm_s < 3.0 and state.gravity_g < 0.05:
            f_delta *= 1.65
        sensitivities["air_flow_cms"] = f_delta

        mat_deltas = [
            self._metric_delta(
                base,
                calc.compute_dimensionless(replace(state, material=mat)),
                base,
            )
            for mat in MATERIAL_REACTIVITY_MAP
            if mat != state.material
        ]
        sensitivities["material_reactivity"] = (
            0.45 * float(np.sqrt(np.mean(np.square(mat_deltas)))) if mat_deltas else 0.0
        )

        sensitivities["flow_concurrent"] = 0.55 * self._metric_delta(
            base,
            calc.compute_dimensionless(replace(state, flow_dir="concurrent")),
            calc.compute_dimensionless(replace(state, flow_dir="opposed")),
        )
        sensitivities["gravity_g"] = (
            0.45
            * self._metric_delta(
                base,
                calc.compute_dimensionless(replace(state, gravity_g=0.0)),
                calc.compute_dimensionless(replace(state, gravity_g=1.0)),
            )
            * (1.0 + 0.35 * state.gravity_g)
        )
        return sensitivities

    def predict(self, state: AtmosphericState) -> FlammabilityPrediction:
        """Ejecuta inferencia ML + ajuste fisico monotono y expone importancia de variables."""
        phys = self._calculator.compute_dimensionless(state)
        X = state.to_feature_array()

        rf_proba = float(self._rf_model.predict_proba(X)[0][1])
        burn_ml = float(self._burn_model.predict(X)[0])
        spread_ml = float(self._spread_model.predict(X)[0])

        # Ensamble auditable: preserva ML dentro de [15..35]% O2 y garantiza fisica monotona en extremos
        ext_prob = min(1.0, max(0.0, 0.70 * rf_proba + 0.30 * phys.extinguished_prob_prior))
        if state.o2_pct >= 50.0:
            # Fuera del rango nominal ISS, la energia quimica escala por ley fisica hiperoxica
            spread_val = max(spread_ml, phys.flame_spread_mm_s)
        else:
            spread_val = max(0.05, 0.72 * spread_ml + 0.28 * phys.flame_spread_mm_s)
        burn_val = max(1.0, 0.70 * burn_ml + 0.30 * phys.burn_time_s_prior)

        raw_importances = np.asarray(self._rf_model.feature_importances_, dtype=np.float64)
        rf_total = float(raw_importances.sum())
        rf_norm = (
            raw_importances / rf_total
            if rf_total > 0.0
            else np.full(len(self._feature_names), 1.0 / max(1, len(self._feature_names)), dtype=np.float64)
        )

        local_map = self._compute_local_sensitivities(state, phys)
        local_arr = np.array(
            [max(0.0, float(local_map.get(name, 0.0))) for name in self._feature_names],
            dtype=np.float64,
        )
        local_total = float(local_arr.sum())
        local_norm = local_arr / local_total if local_total > 0.0 else rf_norm

        blended = 0.30 * rf_norm + 0.70 * local_norm
        blended_total = float(blended.sum()) or 1.0
        normalized = blended / blended_total

        contributions = [
            FeatureContribution(
                feature=FEATURE_DISPLAY_LABELS.get(name, name),
                importance=float(val),
            )
            for name, val in zip(self._feature_names, normalized)
        ]
        contributions.sort(key=lambda item: item.importance, reverse=True)

        return FlammabilityPrediction(
            extinguished_prob=ext_prob,
            burn_time_s=burn_val,
            flame_spread_mm_s=spread_val,
            damkohler=phys.damkohler,
            peclet=phys.peclet,
            regime=phys.regime,
            feature_importance=tuple(contributions),
        )


def load_forensic_presets(cases_json_path: Path) -> dict[str, dict[str, Any]]:
    """Carga los presets forenses verificados (Apollo 1, Apollo 13, Mir, Artemis)."""
    payload = json.loads(Path(cases_json_path).read_text(encoding="utf-8"))
    return {str(item["case_id"]): item for item in payload.get("forensic_cases", [])}
