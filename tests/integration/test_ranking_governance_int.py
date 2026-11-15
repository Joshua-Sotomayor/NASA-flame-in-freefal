"""Pruebas de integracion para clusters TF-IDF/PCA/KMeans y servicio de gobernanza."""

from pathlib import Path
from backend.domain import PsiRepository
from backend.governance import GovernanceAndSpinoffService
from backend.ranking_nlp import ExtractiveNlpEngine, TopsisMultiCriteriaRanker
from backend.security import SecurityBoundaryGuard

ROOT_DIR = Path(__file__).resolve().parents[2]


def test_ranking_clustering_and_governance_integration() -> None:
    guard = SecurityBoundaryGuard()
    repo = PsiRepository(ROOT_DIR / "data" / "psi_combustion_24.json")
    nlp = ExtractiveNlpEngine.from_artifacts(ROOT_DIR / "artifacts" / "models", guard=guard)
    ranker = TopsisMultiCriteriaRanker()
    gov = GovernanceAndSpinoffService(ROOT_DIR / "data" / "cases_and_spinoffs.json")

    items = repo.all_investigations()
    ranked = ranker.rank(items, weights={"habitat": 0.4, "modeling": 0.2, "sensors": 0.2, "spinoff": 0.2})
    clusters = nlp.get_clusters_2d(items)

    assert len(clusters) == 24
    assert {c.cluster_id for c in clusters} == {0, 1, 2, 3}
    for persona in ("Investigador", "Estudiante", "Gestor Industrial"):
        rep = nlp.summarize_for_persona(items, ranked, query="BASS-II quenching", persona=persona)
        assert rep.persona == persona
        assert len(rep.cited_dois) >= 1

    fmea = gov.evaluate_fmea(mitigated=True)
    spinoff = gov.calculate_dual_use(spinoff_id="9407", units=50)
    assert fmea.average_npr_reduction_pct > 50.0
    assert spinoff.spinoff_id == "9407"
