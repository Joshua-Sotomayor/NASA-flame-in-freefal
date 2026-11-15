"""Motor multicriterio TOPSIS/AHP y motor NLP extractivo (`ml-ranking-nlp`).

Integra `TfidfVectorizer + PCA(2) + KMeans(4)` verificados por SHA-256 con extraccion
tipo TextRank / similitud coseno y plantillas deterministas `writing-craft` (cero AI slop,
DOIs `10.60555` intactos y modo plain <25 palabras/oracion para Estudiante).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np

from backend.domain import PsiInvestigation
from backend.security import SecurityBoundaryGuard


CRITERIA_KEYS: tuple[str, ...] = ("habitat", "modeling", "sensors", "spinoff")
VALID_PERSONAS: frozenset[str] = frozenset({"Investigador", "Estudiante", "Gestor Industrial"})
FEATURE_LABELS: dict[str, str] = {
    "o2_pct": "concentracion de O2",
    "pressure_psi": "presion de cabina",
    "flow_cm_s": "flujo de ventilacion",
    "gravity_g": "nivel de gravedad",
    "thickness_mm": "espesor de muestra",
}
CRITERIA_LABELS: dict[str, str] = {
    "habitat": "seguridad en cabina habitable",
    "modeling": "calibracion adimensional",
    "sensors": "deteccion de llama y humo",
    "spinoff": "impacto dual-use",
}


@dataclass(frozen=True)
class RankedInvestigation:
    """Investigacion ordenada por puntuacion de cercania relativa TOPSIS."""

    rank: int
    psi_id: str
    acronym: str
    facility: str
    doi: str
    topsis_score: float
    category: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "psi_id": self.psi_id,
            "acronym": self.acronym,
            "facility": self.facility,
            "doi": self.doi,
            "topsis_score": round(self.topsis_score, 4),
            "category": self.category,
        }


@dataclass(frozen=True)
class ClusterPoint2D:
    """Coordenada PCA 2D y asignacion K-Means auditable."""

    psi_id: str
    acronym: str
    x: float
    y: float
    cluster_id: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "psi_id": self.psi_id,
            "acronym": self.acronym,
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "cluster_id": self.cluster_id,
        }


@dataclass(frozen=True)
class SynthesisReport:
    """Resumen extractivo adaptado a la audiencia sin alucinaciones ni muletillas."""

    persona: str
    query: str
    bullets: tuple[str, ...]
    cited_dois: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "persona": self.persona,
            "query": self.query,
            "bullets": list(self.bullets),
            "cited_dois": list(self.cited_dois),
            "evidence_ids": list(self.evidence_ids),
        }


class TopsisMultiCriteriaRanker:
    """Implementacion vectorial determinista de TOPSIS sobre las 24 PSI."""

    def __init__(self, criteria_names: tuple[str, ...] = CRITERIA_KEYS) -> None:
        self._criteria = tuple(criteria_names)

    def rank(
        self,
        investigations: Sequence[PsiInvestigation],
        weights: Mapping[str, float],
    ) -> list[RankedInvestigation]:
        if not investigations:
            return []

        raw_w = np.array([max(0.0, float(weights.get(c, 0.0))) for c in self._criteria], dtype=np.float64)
        total_w = float(raw_w.sum())
        if total_w <= 0.0:
            raise ValueError("Al menos un peso de criterio TOPSIS debe ser positivo.")
        w_norm = raw_w / total_w

        matrix = np.zeros((len(investigations), len(self._criteria)), dtype=np.float64)
        for row_idx, inv in enumerate(investigations):
            scores = inv.criteria_dict()
            for col_idx, crit in enumerate(self._criteria):
                matrix[row_idx, col_idx] = float(scores.get(crit, 0.5))

        col_norms = np.sqrt(np.sum(matrix**2, axis=0))
        col_norms = np.where(col_norms > 0.0, col_norms, 1.0)
        weighted = (matrix / col_norms) * w_norm

        ideal_best = np.max(weighted, axis=0)
        ideal_worst = np.min(weighted, axis=0)

        dist_best = np.sqrt(np.sum((weighted - ideal_best) ** 2, axis=1))
        dist_worst = np.sqrt(np.sum((weighted - ideal_worst) ** 2, axis=1))
        denom = dist_best + dist_worst
        scores_ci = np.where(denom > 0.0, dist_worst / denom, 0.5)

        paired = sorted(
            zip(investigations, scores_ci),
            key=lambda pair: (-float(pair[1]), pair[0].psi_id),
        )
        return [
            RankedInvestigation(
                rank=idx + 1,
                psi_id=inv.psi_id,
                acronym=inv.acronym,
                facility=inv.facility,
                doi=inv.doi,
                topsis_score=float(score),
                category=inv.category,
            )
            for idx, (inv, score) in enumerate(paired)
        ]


class ExtractiveNlpEngine:
    """Motor NLP local (TF-IDF + PCA + K-Means + TextRank) con reglas `writing-craft`."""

    def __init__(
        self,
        vectorizer: Any,
        pca: Any,
        kmeans: Any,
        psi_ids: Sequence[str],
        tfidf_matrix: np.ndarray,
        coords_2d: np.ndarray,
        labels: Sequence[int],
    ) -> None:
        self._vectorizer = vectorizer
        self._pca = pca
        self._kmeans = kmeans
        self._psi_ids = list(psi_ids)
        self._tfidf_matrix = np.asarray(tfidf_matrix, dtype=np.float64)
        self._coords_2d = np.asarray(coords_2d, dtype=np.float64)
        self._labels = [int(lbl) for lbl in labels]
        self._index_by_id = {pid: idx for idx, pid in enumerate(self._psi_ids)}

    @classmethod
    def from_artifacts(
        cls,
        artifacts_dir: Path,
        guard: SecurityBoundaryGuard | None = None,
    ) -> "ExtractiveNlpEngine":
        base = Path(artifacts_dir)
        model_path = base / "psi_tfidf_kmeans.joblib"
        manifest_path = base / "manifest.sha256.json"
        if guard is not None:
            guard.verify_model_sha256(model_path, manifest_path)
        else:
            SecurityBoundaryGuard().verify_model_sha256(model_path, manifest_path)

        bundle = joblib.load(model_path)
        return cls(
            vectorizer=bundle["vectorizer"],
            pca=bundle["pca"],
            kmeans=bundle["kmeans"],
            psi_ids=bundle["psi_ids"],
            tfidf_matrix=bundle["tfidf_matrix"],
            coords_2d=bundle["coords_2d"],
            labels=bundle["labels"],
        )

    def get_clusters_2d(self, investigations: Sequence[PsiInvestigation]) -> list[ClusterPoint2D]:
        points: list[ClusterPoint2D] = []
        for inv in investigations:
            idx = self._index_by_id.get(inv.psi_id)
            if idx is not None:
                x_val, y_val = float(self._coords_2d[idx, 0]), float(self._coords_2d[idx, 1])
                cluster_id = int(self._labels[idx])
            else:
                vec = self._vectorizer.transform([f"{inv.acronym} {inv.objectives}"]).toarray()
                xy = self._pca.transform(vec)[0]
                x_val, y_val = float(xy[0]), float(xy[1])
                cluster_id = int(self._kmeans.predict(vec)[0])
            points.append(
                ClusterPoint2D(
                    psi_id=inv.psi_id,
                    acronym=inv.acronym,
                    x=x_val,
                    y=y_val,
                    cluster_id=cluster_id,
                )
            )
        return points

    def _query_similarities(self, query: str) -> dict[str, float]:
        if not query.strip():
            return {pid: 0.0 for pid in self._psi_ids}
        q_vec = self._vectorizer.transform([query]).toarray()[0]
        q_norm = float(np.linalg.norm(q_vec))
        if q_norm <= 0.0:
            return {pid: 0.0 for pid in self._psi_ids}
        sims: dict[str, float] = {}
        for idx, pid in enumerate(self._psi_ids):
            doc_vec = self._tfidf_matrix[idx]
            d_norm = float(np.linalg.norm(doc_vec))
            sims[pid] = float(np.dot(q_vec, doc_vec) / (q_norm * d_norm)) if d_norm > 0.0 else 0.0
        return sims

    def _textrank_select(self, candidate_items: Sequence[PsiInvestigation], top_k: int = 3) -> list[PsiInvestigation]:
        if len(candidate_items) <= top_k:
            return list(candidate_items)

        indices = [self._index_by_id[item.psi_id] for item in candidate_items if item.psi_id in self._index_by_id]
        if len(indices) != len(candidate_items):
            return list(candidate_items[:top_k])

        sub = self._tfidf_matrix[indices]
        norms = np.linalg.norm(sub, axis=1, keepdims=True)
        norms = np.where(norms > 0.0, norms, 1.0)
        sim_matrix = (sub / norms) @ (sub / norms).T
        np.fill_diagonal(sim_matrix, 0.0)

        # Iteracion simple de centralidad TextRank (PageRank no dirigido)
        n = len(candidate_items)
        scores = np.full(n, 1.0 / n, dtype=np.float64)
        row_sums = sim_matrix.sum(axis=1, keepdims=True)
        trans = np.where(row_sums > 0.0, sim_matrix / np.where(row_sums > 0.0, row_sums, 1.0), 1.0 / n)
        for _ in range(12):
            scores = 0.15 / n + 0.85 * (trans.T @ scores)

        ordered = sorted(
            zip(candidate_items, scores),
            key=lambda pair: (-float(pair[1]), pair[0].psi_id),
        )
        return [pair[0] for pair in ordered[:top_k]]

    @staticmethod
    def _resolve_topsis_and_driver(
        primary: PsiInvestigation,
        ranked: Sequence[RankedInvestigation],
        feature_importance: Mapping[str, float] | None,
    ) -> tuple[float, str, str]:
        score_by_id = {item.psi_id: item.topsis_score for item in ranked}
        topsis_val = float(score_by_id.get(primary.psi_id, ranked[0].topsis_score))
        if feature_importance:
            key, raw_val = max(feature_importance.items(), key=lambda kv: (float(kv[1]), kv[0]))
            pct = float(raw_val) * 100.0 if float(raw_val) <= 1.0 else float(raw_val)
            label = FEATURE_LABELS.get(key, key)
            return topsis_val, label, f"{min(100.0, max(0.0, pct)):.0f}%"
        crit_key, crit_val = max(primary.criteria_dict().items(), key=lambda kv: (float(kv[1]), kv[0]))
        return topsis_val, CRITERIA_LABELS.get(crit_key, crit_key), f"{float(crit_val) * 100.0:.0f}%"

    def summarize_for_persona(
        self,
        investigations: Sequence[PsiInvestigation],
        ranked: Sequence[RankedInvestigation],
        query: str,
        persona: str,
        feature_importance: Mapping[str, float] | None = None,
    ) -> SynthesisReport:
        if persona not in VALID_PERSONAS:
            raise ValueError(f"Audiencia no soportada: {persona}")
        if not investigations or not ranked:
            raise ValueError("Se requieren investigaciones y ranking TOPSIS no vacios para sintetizar.")

        by_id = {inv.psi_id: inv for inv in investigations}
        sims = self._query_similarities(query)

        # Combina TOPSIS con similitud coseno hacia la consulta cuando existe texto
        combined = sorted(
            ranked,
            key=lambda r: (-(0.70 * r.topsis_score + 0.30 * sims.get(r.psi_id, 0.0)), r.psi_id),
        )
        top_pool = [by_id[r.psi_id] for r in combined[:6] if r.psi_id in by_id]
        if not top_pool:
            raise ValueError("Ranking TOPSIS sin correspondencia valida en catalogo PSI.")
        key_items = self._textrank_select(top_pool, top_k=3)
        cited_dois = tuple(item.doi for item in key_items)
        evidence_ids = tuple(item.psi_id for item in key_items)

        primary = key_items[0]
        secondary = key_items[1] if len(key_items) > 1 else key_items[0]
        tertiary = key_items[2] if len(key_items) > 2 else secondary
        mats_primary = ", ".join(primary.materials[:2]) or "solidos de cabina"
        sensor_hint = primary.sensors[0] if primary.sensors else "camaras opticas"
        topsis_val, driver_label, driver_pct = self._resolve_topsis_and_driver(
            primary, ranked, feature_importance
        )

        if persona == "Investigador":
            bullets = (
                (
                    f"La evidencia de {primary.psi_id} ({primary.acronym}, {primary.facility}) indica un indice "
                    f"TOPSIS {topsis_val:.2f} en rango {primary.o2_min:.0f}-{primary.o2_max:.0f}% O2 y flujo hasta "
                    f"{primary.flow_cm_s_max:.0f} cm/s; su enfoque en {mats_primary} es consistente con limites Da/Pe ({primary.doi})."
                ),
                (
                    f"El analisis extractivo cruza {secondary.psi_id} ({secondary.acronym}) y {tertiary.psi_id} ({tertiary.acronym}), "
                    f"identificando como predictor dominante {driver_label} ({driver_pct}) bajo presion "
                    f"{primary.pressure_psi_min:.1f}-{primary.pressure_psi_max:.1f} psi ({secondary.doi}, {tertiary.doi})."
                ),
                (
                    f"Metodologia observada en {primary.psi_id}: {primary.approach} Los resultados sugieren validez "
                    f"experimental acotada a condiciones analogas de microgravedad ({primary.doi})."
                ),
            )
        elif persona == "Estudiante":
            bullets = (
                (
                    f"{primary.psi_id} ({primary.acronym}) lidera con TOPSIS {topsis_val:.2f} usando {mats_primary}. "
                    f"Opera entre {primary.o2_min:.0f}% y {primary.o2_max:.0f}% de O2 ({primary.doi})."
                ),
                (
                    f"En {secondary.psi_id} ({secondary.acronym}), la falta de gravedad quita la conveccion caliente. "
                    f"La llama depende del flujo a {primary.flow_cm_s_max:.0f} cm/s ({secondary.doi})."
                ),
                (
                    f"En Tierra ({tertiary.psi_id}): {tertiary.earth_benefits} "
                    f"Factor principal: {driver_label} ({driver_pct}); sensor clave: {sensor_hint} ({tertiary.doi})."
                ),
            )
        else:
            # Gestor Industrial (plain + proposal medible)
            bullets = (
                (
                    f"Prioridad operativa {primary.psi_id} ({primary.acronym}, TOPSIS {topsis_val:.2f}): valida riesgos en "
                    f"{primary.o2_min:.0f}-{primary.o2_max:.0f}% O2 y {primary.pressure_psi_min:.1f} psi para reducir "
                    f"NPR antes de certificar cabinas ({primary.doi})."
                ),
                (
                    f"Accion preventiva sobre {driver_label} ({driver_pct}): cruzar {secondary.psi_id} ({secondary.acronym}) "
                    f"y {tertiary.psi_id} alinea sensores tempranos con el protocolo PFE ({secondary.doi})."
                ),
                (
                    f"Retorno terrestre medible: {primary.earth_benefits} Trazabilidad directa con matriz FMEA "
                    f"NASA-STD-6001 y transferencia Spinoff ({tertiary.doi})."
                ),
            )

        return SynthesisReport(
            persona=persona,
            query=query,
            bullets=bullets,
            cited_dois=cited_dois,
            evidence_ids=evidence_ids,
        )
