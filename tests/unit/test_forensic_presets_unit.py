"""Pruebas unitarias TDD para Fichas Forenses y Escenarios de Sensibilidad (Hito I-05)."""

from pathlib import Path

from backend.domain import MATERIAL_REACTIVITY_MAP, PsiRepository
from backend.governance import GovernanceAndSpinoffService
from backend.physics_ml import (
    AtmosphericState,
    DimensionlessPhysicsCalculator,
    load_forensic_presets,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"
PSI_JSON = ROOT_DIR / "data" / "psi_combustion_24.json"
BANNED_ROCKET_TERMS = ("rocket", "cohete", "thruster", "propulsor", "bipropellant")


def test_forensic_presets_schema_and_simulator_mapping() -> None:
    presets = load_forensic_presets(CASES_JSON)
    repo = PsiRepository(PSI_JSON)
    valid_psi_ids = {inv.psi_id for inv in repo.all_investigations()}

    expected_ids = ("apollo_1", "apollo_13", "mir_1997", "lunar_artemis")
    for cid in expected_ids:
        assert cid in presets, f"Falta preset forense requerido: {cid}"
        item = presets[cid]

        # Campo explicito de material compatible con AtmosphericState / RF
        sim_mat = item.get("simulator_material")
        assert sim_mat in MATERIAL_REACTIVITY_MAP, f"simulator_material invalido en {cid}: {sim_mat}"
        assert isinstance(item.get("auto_oxidizing"), bool), f"Falta bandera bool auto_oxidizing en {cid}"

        # Construccion valida de estado termofisico inmutable segun SPEC.md
        state = AtmosphericState(
            o2_pct=float(item["o2_pct"]),
            pressure_psi=float(item["pressure_psi"]),
            flow_cm_s=float(item["flow_cm_s"]),
            gravity_g=float(item["gravity_g"]),
            material=str(sim_mat),
            thickness_mm=float(item["thickness_mm"]),
            flow_dir=str(item["flow_dir"]),
        )
        assert state.o2_pct == float(item["o2_pct"])

        # Trazabilidad hacia las 24 PSI y cumplimiento C-01
        linked = item.get("linked_psi", [])
        assert len(linked) >= 3, f"Se requieren al menos 3 PSI vinculadas en {cid}"
        for pid in linked:
            assert pid in valid_psi_ids, f"PSI inexistente {pid} en {cid}"

        blob = f"{item['name']} {item['material']} {item['pressure_note']} {item['lesson']}".lower()
        for banned in BANNED_ROCKET_TERMS:
            assert banned not in blob, f"Termino prohibido C-01 '{banned}' en {cid}"


def test_forensic_physics_and_mir_auto_oxidizing_rule() -> None:
    presets = load_forensic_presets(CASES_JSON)
    calc = DimensionlessPhysicsCalculator()
    gov = GovernanceAndSpinoffService(CASES_JSON)

    metrics = {}
    for cid, item in presets.items():
        st = AtmosphericState(
            o2_pct=float(item["o2_pct"]),
            pressure_psi=float(item["pressure_psi"]),
            flow_cm_s=float(item["flow_cm_s"]),
            gravity_g=float(item["gravity_g"]),
            material=str(item["simulator_material"]),
            thickness_mm=float(item["thickness_mm"]),
            flow_dir=str(item["flow_dir"]),
        )
        metrics[cid] = calc.compute_dimensionless(st)

    # Condiciones hiperoxicas Apollo 1/13 y lunar Artemis (34% O2) superan el frente de propagacion de 21% O2
    assert metrics["apollo_1"].flame_spread_mm_s > metrics["lunar_artemis"].flame_spread_mm_s > metrics["mir_1997"].flame_spread_mm_s
    assert metrics["apollo_1"].regime == "Propagación Acelerada"
    assert metrics["lunar_artemis"].regime == "Propagación Acelerada"

    # Mir 1997 es el unico caso auto-oxidante (LiClO4) -> PFE obligatorio en gobernanza
    assert presets["mir_1997"]["auto_oxidizing"] is True
    assert presets["apollo_1"]["auto_oxidizing"] is False
    supp = gov.select_suppression_protocol(
        fire_type="auto_oxidizing",
        habitable_crew=True,
        auto_oxidizing=presets["mir_1997"]["auto_oxidizing"],
    )
    assert supp.recommended_agent == "PFE"
    assert supp.eclss_safe is True
