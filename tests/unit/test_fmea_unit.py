"""Pruebas unitarias TDD para la Matriz FMEA/AMFE basada en NASA-STD-6001 (Hito I-04)."""

from pathlib import Path

from backend.domain import PsiRepository
from backend.governance import GovernanceAndSpinoffService

ROOT_DIR = Path(__file__).resolve().parents[2]
CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"
PSI_JSON = ROOT_DIR / "data" / "psi_combustion_24.json"
BANNED_ROCKET_TERMS = ("rocket", "cohete", "thruster", "propulsor", "bipropellant")


def test_fmea_nasa_std_6001_bounds_and_npr_math() -> None:
    gov = GovernanceAndSpinoffService(CASES_JSON)
    raw = gov.evaluate_fmea(mitigated=False)
    mit = gov.evaluate_fmea(mitigated=True)

    assert len(raw.rows) == 6
    assert [r.mode_id for r in raw.rows] == ["FM-01", "FM-02", "FM-03", "FM-04", "FM-05", "FM-06"]

    assert raw.total_baseline_npr == 1901
    assert raw.total_active_npr == 1901
    assert mit.total_baseline_npr == 1901
    assert mit.total_active_npr == 134
    assert round(mit.average_npr_reduction_pct, 2) == 92.95

    for r_base, r_mit in zip(raw.rows, mit.rows):
        assert 1 <= r_base.severity <= 10
        assert 1 <= r_base.occurrence <= 10
        assert 1 <= r_base.detection <= 10
        assert r_base.baseline_npr == r_base.severity * r_base.occurrence * r_base.detection
        assert r_base.active_npr == r_base.baseline_npr

        assert 1 <= r_mit.severity <= 10
        assert 1 <= r_mit.occurrence <= 10
        assert 1 <= r_mit.detection <= 10
        assert r_mit.mitigated_npr == r_mit.severity * r_mit.occurrence * r_mit.detection
        assert r_mit.active_npr == r_mit.mitigated_npr
        assert r_mit.mitigated_npr < r_base.baseline_npr


def test_fmea_psi_traceability_and_domain_scope_c01() -> None:
    repo = PsiRepository(PSI_JSON)
    valid_psi_ids = {inv.psi_id for inv in repo.all_investigations()}

    gov = GovernanceAndSpinoffService(CASES_JSON)
    report = gov.evaluate_fmea(mitigated=False)

    for row in report.rows:
        assert row.linked_psi in valid_psi_ids, f"ID PSI invalido en {row.mode_id}: {row.linked_psi}"
        blob = f"{row.subsystem} {row.failure_mode} {row.effect} {row.mitigation}".lower()
        for banned in BANNED_ROCKET_TERMS:
            assert banned not in blob, f"Termino prohibido C-01 '{banned}' en {row.mode_id}"
