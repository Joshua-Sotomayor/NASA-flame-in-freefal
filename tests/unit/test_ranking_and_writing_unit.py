"""Pruebas unitarias (RED -> GREEN) para TOPSIS, Gobernanza FMEA/Spinoffs y writing-craft."""

from pathlib import Path
import re
import time

from backend.domain import PsiRepository
from backend.governance import GovernanceAndSpinoffService
from backend.ranking_nlp import ExtractiveNlpEngine, TopsisMultiCriteriaRanker

ROOT_DIR = Path(__file__).resolve().parents[2]
PSI_JSON = ROOT_DIR / "data" / "psi_combustion_24.json"
CASES_JSON = ROOT_DIR / "data" / "cases_and_spinoffs.json"

BANNED_AI_SLOP = (
    "en el panorama actual",
    "sin fisuras",
    "piedra angular",
    "cambio de paradigma",
    "revolucionario",
    "revolucionaria",
    "demuestra universalmente",
    "game-changer",
    "paradigm shift",
)


def test_topsis_determinism_and_latency() -> None:
    repo = PsiRepository(PSI_JSON)
    investigations = repo.all_investigations()
    ranker = TopsisMultiCriteriaRanker()

    t0 = time.perf_counter()
    ranked_a = ranker.rank(
        investigations,
        weights={"habitat": 0.6, "modeling": 0.2, "sensors": 0.1, "spinoff": 0.1},
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    assert elapsed_ms < 50.0
    assert len(ranked_a) == 24

    ranked_b = ranker.rank(
        investigations,
        weights={"habitat": 0.6, "modeling": 0.2, "sensors": 0.1, "spinoff": 0.1},
    )
    assert [r.psi_id for r in ranked_a] == [r.psi_id for r in ranked_b]
    # Con peso dominante en habitat, SAFFIRE-V (habitat=0.99) y SAFFIRE-IV (0.98) deben liderar
    assert ranked_a[0].psi_id in {"PSI-104", "PSI-103", "PSI-105"}


def test_writing_craft_rules_across_personas() -> None:
    repo = PsiRepository(PSI_JSON)
    investigations = repo.all_investigations()
    valid_psi_ids = {item.psi_id for item in investigations}
    valid_dois = {item.doi for item in investigations}

    ranker = TopsisMultiCriteriaRanker()
    ranked = ranker.rank(
        investigations,
        weights={"habitat": 0.35, "modeling": 0.30, "sensors": 0.20, "spinoff": 0.15},
    )
    nlp = ExtractiveNlpEngine.from_artifacts(ROOT_DIR / "artifacts" / "models")

    for persona in ("Investigador", "Estudiante", "Gestor Industrial"):
        report = nlp.summarize_for_persona(
            investigations=investigations,
            ranked=ranked,
            query="lunar 34% O2 quenching",
            persona=persona,
        )
        assert len(report.bullets) >= 3
        assert len(report.cited_dois) >= 2
        for doi in report.cited_dois:
            assert doi in valid_dois

        full_text = " ".join(report.bullets)
        lowered = full_text.lower()
        for slop in BANNED_AI_SLOP:
            assert slop not in lowered, f"AI slop detectado en {persona}: {slop}"

        # Ningun ID PSI alucinado
        mentioned_psi = re.findall(r"PSI-\d+", full_text)
        assert all(pid in valid_psi_ids for pid in mentioned_psi)

        # Perfil Estudiante usa lenguaje claro (oraciones < 25 palabras)
        if persona == "Estudiante":
            for bullet in report.bullets:
                for sent in re.split(r"[.!?]+", bullet):
                    words = [w for w in sent.strip().split() if w]
                    assert len(words) < 25, f"Oracion muy larga para Estudiante: {sent}"


def test_governance_fmea_and_dual_use_formulas() -> None:
    gov = GovernanceAndSpinoffService(CASES_JSON)

    fmea_raw = gov.evaluate_fmea(mitigated=False)
    fmea_mit = gov.evaluate_fmea(mitigated=True)
    assert len(fmea_raw.rows) == len(fmea_mit.rows) >= 6
    assert all(m.active_npr < r.active_npr for r, m in zip(fmea_raw.rows, fmea_mit.rows))

    # Spinoff 9582: ahorro de 13 lb por unidad (-40% peso SCBA)
    impact_100 = gov.calculate_dual_use(spinoff_id="9582", units=100)
    assert impact_100.spinoff_id == "9582"
    assert impact_100.weight_saved_lb_total == 1300.0
    assert impact_100.risk_reduction_pct == 40.0

    # Supresion auto-oxidante tipo Mir -> PFE obligatorio (cortar HVAC no apaga LiClO4)
    proto = gov.select_suppression_protocol(fire_type="auto_oxidizing", habitable_crew=True, auto_oxidizing=True)
    assert proto.recommended_agent == "PFE"


def test_writing_craft_injects_topsis_and_feature_importance_deterministically() -> None:
    import pytest

    repo = PsiRepository(PSI_JSON)
    investigations = repo.all_investigations()
    ranker = TopsisMultiCriteriaRanker()
    ranked = ranker.rank(
        investigations,
        weights={"habitat": 0.5, "modeling": 0.2, "sensors": 0.2, "spinoff": 0.1},
    )
    nlp = ExtractiveNlpEngine.from_artifacts(ROOT_DIR / "artifacts" / "models")
    fi = {"o2_pct": 0.48, "pressure_psi": 0.31, "flow_cm_s": 0.21}

    for persona in ("Investigador", "Estudiante", "Gestor Industrial"):
        report = nlp.summarize_for_persona(
            investigations=investigations,
            ranked=ranked,
            query="lunar 34% O2 quenching",
            persona=persona,
            feature_importance=fi,
        )
        full_text = " ".join(report.bullets)
        assert "TOPSIS" in full_text
        assert "O2" in full_text or "o2" in full_text.lower()
        assert "48" in full_text
        if persona == "Investigador":
            assert any(v in full_text.lower() for v in ("indica", "sugiere", "identifica"))
        if persona == "Estudiante":
            for bullet in report.bullets:
                for sent in re.split(r"[.!?]+", bullet):
                    words = [w for w in sent.strip().split() if w]
                    assert len(words) < 25, f"Oracion >24 palabras para Estudiante: {sent}"

    with pytest.raises(ValueError, match="no vacios"):
        nlp.summarize_for_persona(investigations=investigations, ranked=[], query="lunar", persona="Investigador")
    with pytest.raises(ValueError, match="Audiencia"):
        nlp.summarize_for_persona(investigations=investigations, ranked=ranked, query="lunar", persona="Robot")

