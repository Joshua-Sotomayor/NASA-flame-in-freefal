"""Pruebas de integracion para DuctSafetyOrchestrator (ONNX CNN + DecisionTree + FSM)."""

from pathlib import Path

from backend.duct_twin import (
    DuctSafetyOrchestrator,
    FsmState,
    OpticalInput,
    SensorTelemetryFrame,
)
from backend.security import SecurityBoundaryGuard

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT_DIR / "artifacts" / "models"


def test_duct_safety_orchestrator_onnx_and_tree_integration() -> None:
    guard = SecurityBoundaryGuard()
    orchestrator = DuctSafetyOrchestrator.from_artifacts(
        artifacts_dir=ARTIFACTS_DIR,
        guard=guard,
        hysteresis_ticks=2,
    )

    # 1. Tick nominal
    snap_nom = orchestrator.step(
        telemetry=SensorTelemetryFrame(
            delta_t_dt=0.1,
            co_ppm=3.0,
            submicron_aerosol=2.0,
            airflow_cm_s=20.0,
            comm_ok=True,
        ),
        optical_input=OpticalInput(optical_preset="nominal"),
    )
    assert snap_nom.cnn_class == "Nominal"
    assert len(snap_nom.cnn_probs) == 4
    assert abs(sum(snap_nom.cnn_probs) - 1.0) < 1e-3
    assert "->" in snap_nom.tree_rule_path
    assert snap_nom.fsm_state == FsmState.NORMAL.value
    assert snap_nom.fan_on is True

    # 2. Aerosol submicronico temprano (Spinoff 9407 / SPICE) -> PRE_ALERTA
    snap_pre = orchestrator.step(
        telemetry=SensorTelemetryFrame(
            delta_t_dt=2.5,
            co_ppm=45.0,
            submicron_aerosol=28.0,
            airflow_cm_s=18.0,
            comm_ok=True,
        ),
        optical_input=OpticalInput(optical_preset="cool_flame_ntc"),
    )
    assert snap_pre.cnn_class == "Llama Fria NTC"
    assert snap_pre.fsm_state == FsmState.PRE_ALERTA.value

    # 3. Combusion abierta sostenida -> CONTENCION con supresion PFE y corte HVAC
    snap_cont = orchestrator.step(
        telemetry=SensorTelemetryFrame(
            delta_t_dt=18.5,
            co_ppm=240.0,
            submicron_aerosol=65.0,
            airflow_cm_s=25.0,
            comm_ok=True,
        ),
        optical_input=OpticalInput(optical_preset="open_propagation"),
    )
    assert snap_cont.cnn_class == "Propagacion Abierta"
    assert snap_cont.fsm_state == FsmState.CONTENCION.value
    assert snap_cont.fan_on is False
    assert snap_cont.damper_closed is True
    assert snap_cont.pfe_active is True

    # 4. Perdida de comunicacion serial UART -> FALLA_SEGURA inmediata (interlock EPLAN)
    snap_fail = orchestrator.step(
        telemetry=SensorTelemetryFrame(
            delta_t_dt=0.5,
            co_ppm=5.0,
            submicron_aerosol=2.0,
            airflow_cm_s=0.0,
            comm_ok=False,
        ),
        optical_input=OpticalInput(optical_vector=[0.08] * 64),
    )
    assert snap_fail.fsm_state == FsmState.FALLA_SEGURA.value
    assert snap_fail.fan_on is False
    assert snap_fail.damper_closed is True
