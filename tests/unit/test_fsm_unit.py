"""Pruebas unitarias (RED -> GREEN) para DeterministicFsmController (`backend.duct_twin`)."""

from dataclasses import FrozenInstanceError
import pytest

from backend.duct_twin import (
    DeterministicFsmController,
    FsmState,
    SensorTelemetryFrame,
    TreePrediction,
    VisionPrediction,
)


def _vision(cls_name: str, probs: tuple[float, float, float, float]) -> VisionPrediction:
    return VisionPrediction(cnn_class=cls_name, cnn_probs=probs)


def _tree(cls_idx: int, label: str = "Nominal", rule: str = "root -> Nominal") -> TreePrediction:
    return TreePrediction(tree_class_idx=cls_idx, tree_label=label, rule_path=rule)


def _telemetry(
    delta_t_dt: float = 0.2,
    co_ppm: float = 4.0,
    aerosol: float = 2.0,
    airflow: float = 20.0,
    comm_ok: bool = True,
) -> SensorTelemetryFrame:
    return SensorTelemetryFrame(
        delta_t_dt=delta_t_dt,
        co_ppm=co_ppm,
        submicron_aerosol=aerosol,
        airflow_cm_s=airflow,
        comm_ok=comm_ok,
    )


def test_telemetry_frame_is_frozen_and_validates_ranges() -> None:
    frame = _telemetry()
    with pytest.raises(FrozenInstanceError):
        frame.co_ppm = 999.0  # type: ignore[misc]

    with pytest.raises(ValueError):
        _telemetry(co_ppm=6000.0)


def test_fsm_deterministic_transitions_and_hysteresis() -> None:
    fsm = DeterministicFsmController(hysteresis_ticks=2)
    assert fsm.current_state == FsmState.NORMAL

    # Un pico transitorio unico no dispara CONTENCION inmediatamente (histéresis)
    res1 = fsm.evaluate(
        vision=_vision("Propagacion Abierta", (0.01, 0.02, 0.02, 0.95)),
        tree=_tree(2, "Contencion", "delta_t_dt > 12.0 -> Contencion"),
        telemetry=_telemetry(delta_t_dt=16.0, co_ppm=190.0),
    )
    assert res1.fsm_state == FsmState.PRE_ALERTA
    assert res1.fan_on is True
    assert res1.damper_closed is False

    # Confirmacion sostenida en segundo tick transiciona a CONTENCION y activa supresion PFE
    res2 = fsm.evaluate(
        vision=_vision("Propagacion Abierta", (0.01, 0.02, 0.02, 0.95)),
        tree=_tree(2, "Contencion", "delta_t_dt > 12.0 -> Contencion"),
        telemetry=_telemetry(delta_t_dt=18.0, co_ppm=220.0),
    )
    assert res2.fsm_state == FsmState.CONTENCION
    assert res2.fan_on is False
    assert res2.damper_closed is True
    assert res2.pfe_active is True


def test_cool_flame_ntc_prevents_premature_reset() -> None:
    fsm = DeterministicFsmController(hysteresis_ticks=2)

    # Deteccion de llama fria NTC activa latcheo de enfriamiento
    res_cool = fsm.evaluate(
        vision=_vision("Llama Fria NTC", (0.02, 0.05, 0.90, 0.03)),
        tree=_tree(0, "Nominal", "aerosol <= 18 -> Nominal"),
        telemetry=_telemetry(delta_t_dt=2.5, co_ppm=12.0, aerosol=6.0),
    )
    assert res_cool.fsm_state == FsmState.PRE_ALERTA

    # Aunque la camara vuelva a parecer nominal, si delta_t_dt > 0 no vuelve a NORMAL
    res_still_warm = fsm.evaluate(
        vision=_vision("Nominal", (0.95, 0.02, 0.02, 0.01)),
        tree=_tree(0, "Nominal", "aerosol <= 18 -> Nominal"),
        telemetry=_telemetry(delta_t_dt=1.2, co_ppm=5.0, aerosol=3.0),
    )
    assert res_still_warm.fsm_state == FsmState.PRE_ALERTA

    # Solo tras enfriamiento confirmado (delta_t_dt <= 0) durante hysteresis_ticks puede regresar a NORMAL
    fsm.evaluate(
        vision=_vision("Nominal", (0.95, 0.02, 0.02, 0.01)),
        tree=_tree(0, "Nominal", "aerosol <= 18 -> Nominal"),
        telemetry=_telemetry(delta_t_dt=0.0, co_ppm=2.0, aerosol=1.0),
    )
    res_cooled = fsm.evaluate(
        vision=_vision("Nominal", (0.95, 0.02, 0.02, 0.01)),
        tree=_tree(0, "Nominal", "aerosol <= 18 -> Nominal"),
        telemetry=_telemetry(delta_t_dt=-0.3, co_ppm=2.0, aerosol=1.0),
    )
    assert res_cooled.fsm_state == FsmState.NORMAL


def test_comm_failure_triggers_hardwired_falla_segura() -> None:
    fsm = DeterministicFsmController(hysteresis_ticks=2)
    res = fsm.evaluate(
        vision=_vision("Nominal", (0.95, 0.02, 0.02, 0.01)),
        tree=_tree(0),
        telemetry=_telemetry(comm_ok=False),
    )
    assert res.fsm_state == FsmState.FALLA_SEGURA
    assert res.fan_on is False
    assert res.damper_closed is True
