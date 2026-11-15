"""Pruebas unitarias (RED -> GREEN) para TOPSIS, Gobernanza FMEA/Spinoffs y writing-craft."""

from pathlib import Path
import re
import time

import pytest

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


def test_topsis_scale_invariance_and_edge_cases() -> None:
    repo = PsiRepository(PSI_JSON)
    investigations = repo.all_investigations()
    ranker = TopsisMultiCriteriaRanker()

    # Lista vacia devuelve vacio de forma segura
    assert ranker.rank([], weights={"habitat": 1.0}) == []

    # Pesos nulos o negativos deben rechazarse
    with pytest.raises(ValueError):
        ranker.rank(investigations, weights={"habitat": 0.0, "modeling": 0.0, "sensors": 0.0, "spinoff": 0.0})
    with pytest.raises(ValueError):
        ranker.rank(investigations, weights={"habitat": -1.0, "modeling": 0.0})

    # Invariancia ante escalado positivo de pesos (por ejemplo w vs 100*w)
    w_unit = {"habitat": 0.5462, "modeling": 0.2323, "sensors": 0.1377, "spinoff": 0.0838}
    w_scaled = {k: v * 100.0 for k, v in w_unit.items()}
    res_unit = ranker.rank(investigations, weights=w_unit)
    res_scaled = ranker.rank(investigations, weights=w_scaled)

    assert [r.psi_id for r in res_unit] == [r.psi_id for r in res_scaled]
    for a, b in zip(res_unit, res_scaled):
        assert abs(a.topsis_score - b.topsis_score) < 1e-9
        assert 0.0 <= a.topsis_score <= 1.0

    # Orden monotono no creciente
    scores = [r.topsis_score for r in res_unit]
    assert scores == sorted(scores, reverse=True)


def test_topsis_ahp_profiles_sensitivity_and_consistency() -> None:
    repo = PsiRepository(PSI_JSON)
    investigations = repo.all_investigations()
    ranker = TopsisMultiCriteriaRanker()

    # 1. Seguridad en Habitats (CR=0.0189 < 0.10): SAFFIRE-V (#1)
    r_hab = ranker.rank(
        investigations,
        weights={"habitat": 0.5462, "modeling": 0.2323, "sensors": 0.1377, "spinoff": 0.0838},
    )
    assert r_hab[0].psi_id == "PSI-104"

    # 2. Modelado Fisico y Simulacion (CR=0.0189 < 0.10): BASS-II (#1)
    r_mod = ranker.rank(
        investigations,
        weights={"habitat": 0.2323, "modeling": 0.5462, "sensors": 0.1377, "spinoff": 0.0838},
    )
    assert r_mod[0].psi_id == "PSI-25"

    # 3. Deteccion Temprana e Instrumentacion (CR=0.0170 < 0.10): MSC (#1), SPICE (#2)
    r_sen = ranker.rank(
        investigations,
        weights={"habitat": 0.2257, "modeling": 0.1235, "sensors": 0.5166, "spinoff": 0.1341},
    )
    assert r_sen[0].psi_id == "PSI-110"
    assert r_sen[1].psi_id == "PSI-129"

    # 4. Transferencia Dual-Use Spinoffs (CR=0.0076 < 0.10): SPICE (#1), MSC (#2)
    r_spi = ranker.rank(
        investigations,
        weights={"habitat": 0.1894, "modeling": 0.1054, "sensors": 0.1894, "spinoff": 0.5158},
    )
    assert r_spi[0].psi_id == "PSI-129"
    assert r_spi[1].psi_id == "PSI-110"

