"""Orquestador de seguridad en ducto (`duct-cnn-fsm`): CNN ONNX + DecisionTree + FSM Determinista.

Implementa la arquitectura explicable de 3 etapas descrita en `SPEC.md`:
1. Rama Optica: `OnnxFlameVisionModel` (`flame_cnn.onnx` verificado por SHA-256).
2. Rama Tabular: `SensorDecisionTreeModel` (`sensor_tree.joblib` con traza de reglas exacta).
3. Orquestador de Control: `DeterministicFsmController` (`NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA`)
   con histeresis temporal, bloqueo de rearme en Llama Fria NTC e interlock cableado (`comm_ok=False`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Sequence

import joblib
import numpy as np
import onnxruntime as ort

from backend.domain import (
    FLAME_CLASS_LABELS,
    OPTICAL_PRESET_TO_IDX,
    SENSOR_CLASS_LABELS,
    SENSOR_FEATURES,
    preset_to_input_tensor,
)
from backend.security import SecurityBoundaryGuard


class FsmState(str, Enum):
    """Estados discretos auditables del sistema de contencion en ducto."""

    NORMAL = "NORMAL"
    PRE_ALERTA = "PRE_ALERTA"
    CONTENCION = "CONTENCION"
    FALLA_SEGURA = "FALLA_SEGURA"


@dataclass(frozen=True)
class SensorTelemetryFrame:
    """Trama de sensores validada dentro de los limites fisicos de SPEC.md."""

    delta_t_dt: float
    co_ppm: float
    submicron_aerosol: float
    airflow_cm_s: float
    comm_ok: bool = True

    def __post_init__(self) -> None:
        if not (-5.0 <= self.delta_t_dt <= 100.0):
            raise ValueError("delta_t_dt debe estar entre -5 y 100 C/s.")
        if not (0.0 <= self.co_ppm <= 5000.0):
            raise ValueError("co_ppm debe estar entre 0 y 5000 ppm.")
        if not (0.0 <= self.submicron_aerosol <= 100.0):
            raise ValueError("submicron_aerosol debe estar entre 0 y 100.")
        if not (0.0 <= self.airflow_cm_s <= 60.0):
            raise ValueError("airflow_cm_s debe estar entre 0 y 60 cm/s.")

    def to_feature_array(self) -> np.ndarray:
        """Retorna el vector (1, 4) esperado por `sensor_tree.joblib`."""
        return np.array(
            [
                [
                    float(self.delta_t_dt),
                    float(self.co_ppm),
                    float(self.submicron_aerosol),
                    float(self.airflow_cm_s),
                ]
            ],
            dtype=np.float64,
        )


@dataclass(frozen=True)
class OpticalInput:
    """Entrada visual proveniente de camara del ducto (preset o vector 64-D)."""

    optical_preset: str | None = None
    optical_vector: Sequence[float] | None = None

    def __post_init__(self) -> None:
        if self.optical_preset is not None and self.optical_preset.lower() not in OPTICAL_PRESET_TO_IDX:
            raise ValueError(f"optical_preset invalido: {self.optical_preset}")
        if self.optical_vector is not None:
            if len(self.optical_vector) != 64:
                raise ValueError("optical_vector debe tener exactamente 64 flotantes.")


@dataclass(frozen=True)
class VisionPrediction:
    """Salida probabilistica acotada de la CNN optica ONNX."""

    cnn_class: str
    cnn_probs: tuple[float, float, float, float]


@dataclass(frozen=True)
class TreePrediction:
    """Salida auditable con la ruta exacta de decision del arbol fisico."""

    tree_class_idx: int
    tree_label: str
    rule_path: str


@dataclass(frozen=True)
class FsmTransitionResult:
    """Decision determinista y estado de actuadores HVAC/Compuerta/PFE."""

    fsm_state: FsmState
    fan_on: bool
    damper_closed: bool
    pfe_active: bool
    reason: str


@dataclass(frozen=True)
class DuctTwinSnapshot:
    """Instantanea completa compatible con `POST /api/v1/twin/step-fsm`."""

    cnn_class: str
    cnn_probs: tuple[float, float, float, float]
    tree_rule_path: str
    fsm_state: str
    fan_on: bool
    damper_closed: bool
    pfe_active: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "cnn_class": self.cnn_class,
            "cnn_probs": [round(float(p), 4) for p in self.cnn_probs],
            "tree_rule_path": self.tree_rule_path,
            "fsm_state": self.fsm_state,
            "fan_on": self.fan_on,
            "damper_closed": self.damper_closed,
            "pfe_active": self.pfe_active,
        }


class OnnxFlameVisionModel:
    """Envoltorio POO seguro de `onnxruntime.InferenceSession` con 1 hilo fijo."""

    def __init__(self, session: ort.InferenceSession) -> None:
        self._session = session
        self._input_name = session.get_inputs()[0].name

    @classmethod
    def from_artifact(
        cls,
        onnx_path: Path,
        manifest_path: Path,
        guard: SecurityBoundaryGuard,
    ) -> "OnnxFlameVisionModel":
        guard.verify_model_sha256(onnx_path, manifest_path)
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 1
        session = ort.InferenceSession(
            str(onnx_path),
            sess_options=sess_options,
            providers=["CPUExecutionProvider"],
        )
        return cls(session=session)

    @staticmethod
    def _softmax(logits: np.ndarray) -> np.ndarray:
        shifted = logits - np.max(logits)
        exps = np.exp(shifted)
        return exps / np.sum(exps)

    def classify(self, optical_input: OpticalInput) -> VisionPrediction:
        tensor = preset_to_input_tensor(
            preset=optical_input.optical_preset,
            optical_vector=optical_input.optical_vector,
        )
        raw_logits = self._session.run(None, {self._input_name: tensor})[0][0]
        probs = self._softmax(np.asarray(raw_logits, dtype=np.float64))
        best_idx = int(np.argmax(probs))
        return VisionPrediction(
            cnn_class=FLAME_CLASS_LABELS[best_idx],
            cnn_probs=(
                float(probs[0]),
                float(probs[1]),
                float(probs[2]),
                float(probs[3]),
            ),
        )


class SensorDecisionTreeModel:
    """Clasificador tabular explicable sobre dT/dt, CO, aerosol <0.1um y flujo."""

    def __init__(
        self,
        tree_model: Any,
        feature_names: tuple[str, ...] = SENSOR_FEATURES,
        class_labels: tuple[str, ...] = SENSOR_CLASS_LABELS,
    ) -> None:
        self._tree = tree_model
        self._feature_names = tuple(feature_names)
        self._class_labels = tuple(class_labels)

    @classmethod
    def from_artifact(
        cls,
        tree_path: Path,
        manifest_path: Path,
        guard: SecurityBoundaryGuard,
    ) -> "SensorDecisionTreeModel":
        guard.verify_model_sha256(tree_path, manifest_path)
        bundle = joblib.load(tree_path)
        return cls(
            tree_model=bundle["model"],
            feature_names=tuple(bundle.get("feature_names", SENSOR_FEATURES)),
            class_labels=tuple(bundle.get("class_labels", SENSOR_CLASS_LABELS)),
        )

    def predict_with_trace(self, telemetry: SensorTelemetryFrame) -> TreePrediction:
        X = telemetry.to_feature_array()
        cls_idx = int(self._tree.predict(X)[0])
        label = self._class_labels[cls_idx]

        tree_ = self._tree.tree_
        node_indicator = self._tree.decision_path(X)
        node_indices = node_indicator.indices[node_indicator.indptr[0] : node_indicator.indptr[1]]

        clauses: list[str] = []
        for node_id in node_indices:
            feat_idx = int(tree_.feature[node_id])
            if feat_idx < 0:
                continue
            feat_name = self._feature_names[feat_idx]
            threshold = float(tree_.threshold[node_id])
            val = float(X[0, feat_idx])
            op = "<=" if val <= threshold else ">"
            clauses.append(f"{feat_name} ({val:.1f}) {op} {threshold:.1f}")

        rule_path = (" & ".join(clauses) + f" -> {label}") if clauses else f"root -> {label}"
        return TreePrediction(tree_class_idx=cls_idx, tree_label=label, rule_path=rule_path)


class DeterministicFsmController:
    """Maquina de estados finitos con histeresis temporal e interlock EPLAN."""

    def __init__(self, hysteresis_ticks: int = 2) -> None:
        if hysteresis_ticks < 1:
            raise ValueError("hysteresis_ticks debe ser >= 1.")
        self._hysteresis_ticks = int(hysteresis_ticks)
        self._state = FsmState.NORMAL
        self._anomaly_streak = 0
        self._cool_down_streak = 0
        self._cool_flame_latched = False

    @property
    def current_state(self) -> FsmState:
        return self._state

    def reset(self) -> None:
        self._state = FsmState.NORMAL
        self._anomaly_streak = 0
        self._cool_down_streak = 0
        self._cool_flame_latched = False

    def evaluate(
        self,
        vision: VisionPrediction,
        tree: TreePrediction,
        telemetry: SensorTelemetryFrame,
    ) -> FsmTransitionResult:
        """Evalua fusion optica+tabular y aplica reglas de seguridad deterministas."""
        # 1. Interlock cableado prioritario ante perdida serial UART
        if not telemetry.comm_ok:
            self._state = FsmState.FALLA_SEGURA
            self._anomaly_streak = 0
            self._cool_down_streak = 0
            self._cool_flame_latched = True
            return FsmTransitionResult(
                fsm_state=self._state,
                fan_on=False,
                damper_closed=True,
                pfe_active=False,
                reason="Perdida de comunicacion serial -> Enclavamiento EPLAN FALLA_SEGURA.",
            )

        # 2. Severidad fusionada (0=Nominal, 1=Preventivo/LlamaFria, 2=Critico/Abierta)
        if vision.cnn_class == "Llama Fria NTC":
            self._cool_flame_latched = True

        severity = 0
        if tree.tree_class_idx == 2 or vision.cnn_class == "Propagacion Abierta":
            severity = 2
        elif tree.tree_class_idx == 1 or vision.cnn_class in ("Llama Fria NTC", "Llama Esferica Azul 0g"):
            severity = 1

        # 3. Maquina de estados con histeresis
        if severity == 2:
            self._anomaly_streak += 1
            self._cool_down_streak = 0
            if self._anomaly_streak >= self._hysteresis_ticks:
                self._state = FsmState.CONTENCION
                return FsmTransitionResult(
                    fsm_state=self._state,
                    fan_on=False,
                    damper_closed=True,
                    pfe_active=True,
                    reason="Anomalia critica sostenida -> CONTENCION (HVAC OFF, compuerta cerrada, PFE ON).",
                )
            self._state = FsmState.PRE_ALERTA
            return FsmTransitionResult(
                fsm_state=self._state,
                fan_on=True,
                damper_closed=False,
                pfe_active=False,
                reason="Pico critico inicial en confirmacion por histeresis -> PRE_ALERTA.",
            )

        if severity == 1:
            self._anomaly_streak = max(1, self._anomaly_streak + 1)
            self._cool_down_streak = 0
            if self._state != FsmState.CONTENCION:
                self._state = FsmState.PRE_ALERTA
            fan_on = self._state != FsmState.CONTENCION
            damper_closed = self._state == FsmState.CONTENCION
            pfe_active = self._state == FsmState.CONTENCION
            return FsmTransitionResult(
                fsm_state=self._state,
                fan_on=fan_on,
                damper_closed=damper_closed,
                pfe_active=pfe_active,
                reason="Firma de llama fria NTC o aerosol <0.1um -> vigilancia preventiva.",
            )

        # severity == 0: verificacion de enfriamiento antes de rearmar a NORMAL
        self._anomaly_streak = 0
        if self._state == FsmState.NORMAL and not self._cool_flame_latched:
            return FsmTransitionResult(
                fsm_state=FsmState.NORMAL,
                fan_on=True,
                damper_closed=False,
                pfe_active=False,
                reason="Operacion nominal en ducto.",
            )

        if self._cool_flame_latched and telemetry.delta_t_dt > 0.0:
            self._cool_down_streak = 0
            if self._state in (FsmState.NORMAL, FsmState.FALLA_SEGURA):
                self._state = FsmState.PRE_ALERTA
            return FsmTransitionResult(
                fsm_state=self._state,
                fan_on=self._state != FsmState.CONTENCION,
                damper_closed=self._state == FsmState.CONTENCION,
                pfe_active=False,
                reason="Rearme bloqueado por latch de Llama Fria NTC hasta dT/dt <= 0.",
            )

        self._cool_down_streak += 1
        if self._cool_down_streak >= self._hysteresis_ticks:
            self._cool_flame_latched = False
            self._state = FsmState.NORMAL
            return FsmTransitionResult(
                fsm_state=FsmState.NORMAL,
                fan_on=True,
                damper_closed=False,
                pfe_active=False,
                reason="Enfriamiento sostenido verificado -> retorno a NORMAL.",
            )

        if self._state in (FsmState.CONTENCION, FsmState.FALLA_SEGURA):
            self._state = FsmState.PRE_ALERTA
        return FsmTransitionResult(
            fsm_state=self._state,
            fan_on=True,
            damper_closed=False,
            pfe_active=False,
            reason="Verificando ticks de enfriamiento previo a rearme.",
        )


class DuctSafetyOrchestrator:
    """Fachada POO que integra rama optica ONNX, arbol fisico y controlador FSM."""

    def __init__(
        self,
        vision_model: OnnxFlameVisionModel,
        sensor_tree: SensorDecisionTreeModel,
        fsm: DeterministicFsmController,
    ) -> None:
        self._vision_model = vision_model
        self._sensor_tree = sensor_tree
        self._fsm = fsm

    @classmethod
    def from_artifacts(
        cls,
        artifacts_dir: Path,
        guard: SecurityBoundaryGuard,
        hysteresis_ticks: int = 2,
    ) -> "DuctSafetyOrchestrator":
        base = Path(artifacts_dir)
        manifest = base / "manifest.sha256.json"
        vision = OnnxFlameVisionModel.from_artifact(base / "flame_cnn.onnx", manifest, guard)
        tree = SensorDecisionTreeModel.from_artifact(base / "sensor_tree.joblib", manifest, guard)
        fsm = DeterministicFsmController(hysteresis_ticks=hysteresis_ticks)
        return cls(vision_model=vision, sensor_tree=tree, fsm=fsm)

    def reset_fsm(self) -> None:
        self._fsm.reset()

    def step(
        self,
        telemetry: SensorTelemetryFrame,
        optical_input: OpticalInput,
    ) -> DuctTwinSnapshot:
        vision_pred = self._vision_model.classify(optical_input)
        tree_pred = self._sensor_tree.predict_with_trace(telemetry)
        fsm_res = self._fsm.evaluate(vision=vision_pred, tree=tree_pred, telemetry=telemetry)
        return DuctTwinSnapshot(
            cnn_class=vision_pred.cnn_class,
            cnn_probs=vision_pred.cnn_probs,
            tree_rule_path=tree_pred.rule_path,
            fsm_state=fsm_res.fsm_state.value,
            fan_on=fsm_res.fan_on,
            damper_closed=fsm_res.damper_closed,
            pfe_active=fsm_res.pfe_active,
        )
