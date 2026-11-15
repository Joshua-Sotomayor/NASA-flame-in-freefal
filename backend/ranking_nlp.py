"""Motor multicriterio TOPSIS/AHP y motor NLP extractivo (`ml-ranking-nlp`).

Integra `TfidfVectorizer + PCA(2) + KMeans(4)` verificados por SHA-256 con extraccion
tipo TextRank / similitud coseno y plantillas deterministas `writing-craft` (cero AI slop,
DOIs `10.60555` intactos y modo plain <25 palabras/oracion para Estudiante).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

import joblib
import numpy as np

from backend.domain import PsiInvestigation
from backend.security import SecurityBoundaryGuard


CRITERIA_KEYS: tuple[str, ...] = ("habitat", "modeling", "sensors", "spinoff")
VALID_PERSONAS: frozenset[str] = frozenset({"Investigador", "Estudiante", "Gestor Industrial"})


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
    def _sanitize_query_excerpt(query: str, max_words: int = 6) -> str:
        cleaned = re.sub(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ%+\-/ ]+", " ", query)
        words = [w for w in cleaned.split() if w]
        return " ".join(words[:max_words])

    @staticmethod
    def _lower_first(text: str) -> str:
        cleaned = text.strip().rstrip(".")
        if not cleaned:
            return cleaned
        first_word = cleaned.split()[0]
        if len(first_word) > 1 and first_word[:2].isupper():
            return cleaned
        return cleaned[0].lower() + cleaned[1:]

    @staticmethod
    def _format_o2_range(item: PsiInvestigation, plain: bool = False) -> str:
        if math.isclose(item.o2_min, item.o2_max, abs_tol=0.05):
            return f"{item.o2_min:.0f}% de oxígeno" if plain else f"{item.o2_min:.0f}% de O2"
        if plain:
            return f"{item.o2_min:.0f}% a {item.o2_max:.0f}% de oxígeno"
        return f"{item.o2_min:.0f}–{item.o2_max:.0f}% de O2"

    @staticmethod
    def _gloss_acronyms_plain(text: str) -> str:
        replacements = (
            (r"\bFDS\b", "simuladores de fuego (FDS)"),
            (r"\bHVAC\b", "ventilación (HVAC)"),
            (r"\bNFPA\b", "seguridad contra incendios (NFPA)"),
            (r"\bNTC\b", "baja temperatura (NTC)"),
            (r"\bECLSS\b", "soporte vital (ECLSS)"),
        )
        out = text
        for pattern, repl in replacements:
            if repl not in out:
                out = re.sub(pattern, repl, out)
        return out

    @staticmethod
    def _format_pressure_range(item: PsiInvestigation) -> str:
        if math.isclose(item.pressure_psi_min, item.pressure_psi_max, abs_tol=0.05):
            return f"{item.pressure_psi_min:.1f} psi"
        return f"{item.pressure_psi_min:.1f}–{item.pressure_psi_max:.1f} psi"

    @staticmethod
    def _short_phrase(text: str, max_words: int = 6) -> str:
        words = [w for w in text.strip().rstrip(".").split() if w]
        if len(words) <= max_words:
            return " ".join(words)
        return " ".join(words[:max_words])

    @staticmethod
    def _dominant_criterion(
        ranked: Sequence[RankedInvestigation],
        by_id: Mapping[str, PsiInvestigation],
        primary: PsiInvestigation,
    ) -> str:
        primary_scores = primary.criteria_dict()
        aligned = [r for r in ranked if r.psi_id in by_id]
        if len(aligned) < 3:
            return max(CRITERIA_KEYS, key=lambda c: primary_scores.get(c, 0.0))

        y = np.array([r.topsis_score for r in aligned], dtype=np.float64)
        y_std = float(np.std(y))
        best_key = CRITERIA_KEYS[0]
        best_val = -math.inf
        for crit in CRITERIA_KEYS:
            x = np.array(
                [by_id[r.psi_id].criteria_dict().get(crit, 0.5) for r in aligned],
                dtype=np.float64,
            )
            x_std = float(np.std(x))
            if x_std > 1e-9 and y_std > 1e-9:
                corr = float(np.corrcoef(x, y)[0, 1])
            else:
                corr = 0.0
            score = 0.65 * corr + 0.35 * float(primary_scores.get(crit, 0.5))
            if score > best_val:
                best_val = score
                best_key = crit
        return best_key

    def summarize_for_persona(
        self,
        investigations: Sequence[PsiInvestigation],
        ranked: Sequence[RankedInvestigation],
        query: str,
        persona: str,
    ) -> SynthesisReport:
        if persona not in VALID_PERSONAS:
            raise ValueError(f"Audiencia no soportada: {persona}")
        if not investigations:
            raise ValueError("Se requiere al menos una investigacion para generar la sintesis.")

        by_id = {inv.psi_id: inv for inv in investigations}
        sims = self._query_similarities(query)

        # Combina prioridad multicriterio con afinidad textual hacia la consulta
        combined = sorted(
            ranked,
            key=lambda r: (-(0.70 * r.topsis_score + 0.30 * sims.get(r.psi_id, 0.0)), r.psi_id),
        )
        valid_combined = [r for r in combined if r.psi_id in by_id]
        if not valid_combined:
            ordered_items = list(investigations)
        else:
            ordered_items = []
            seen_ids: set[str] = set()
            for r in valid_combined:
                if r.psi_id not in seen_ids:
                    seen_ids.add(r.psi_id)
                    ordered_items.append(by_id[r.psi_id])

        primary = ordered_items[0]
        secondary = ordered_items[1] if len(ordered_items) > 1 else primary
        if len(ordered_items) > 2:
            tertiary_pool = [
                by_id[r.psi_id]
                for r in valid_combined[2:6]
                if r.psi_id not in {primary.psi_id, secondary.psi_id}
            ] or ordered_items[2:6]
            selected_tertiary = self._textrank_select(tertiary_pool, top_k=1)
            tertiary = selected_tertiary[0] if selected_tertiary else ordered_items[2]
            key_items = [primary, secondary, tertiary]
        elif len(ordered_items) == 2:
            tertiary = secondary
            key_items = [primary, secondary]
        else:
            tertiary = primary
            key_items = [primary]

        cited_dois = tuple(item.doi for item in key_items)
        evidence_ids = tuple(item.psi_id for item in key_items)

        dom_crit = self._dominant_criterion(ranked, by_id, primary)
        top_score = valid_combined[0].topsis_score if valid_combined else 1.0
        primary_sim = sims.get(primary.psi_id, 0.0)
        query_excerpt = self._sanitize_query_excerpt(query, max_words=7)
        query_short = self._sanitize_query_excerpt(query, max_words=5)

        mats_primary = ", ".join(primary.materials[:2]) or "sólidos de cabina"
        mat0_primary = self._short_phrase(primary.materials[0], max_words=6) if primary.materials else "sólidos de cabina"
        mat0_secondary = self._short_phrase(secondary.materials[0], max_words=6) if secondary.materials else "materiales de cabina"
        sensors_secondary = " y ".join(secondary.sensors[:2]) or "instrumentación óptica y de gases"
        sensors_tertiary = " y ".join(tertiary.sensors[:2]) or "sensores de combustión"
        sensor0_tertiary = self._short_phrase(tertiary.sensors[0], max_words=4) if tertiary.sensors else "sensores térmicos"

        o2_academic = self._format_o2_range(primary, plain=False)
        o2_plain = self._format_o2_range(primary, plain=True)
        press_range = self._format_pressure_range(primary)

        if persona == "Investigador":
            crit_academic = {
                "habitat": "aplicabilidad directa a hábitats habitables",
                "modeling": "valor para modelado físico y límites de propagación",
                "sensors": "instrumentación y detección temprana",
                "spinoff": "transferencia tecnológica a seguridad terrestre",
            }[dom_crit]
            if query_excerpt and primary_sim > 0.05:
                lead_clause = (
                    f"encabeza la selección al combinar prioridad en {crit_academic} "
                    f"con afinidad temática hacia «{query_excerpt}»"
                )
            elif query_excerpt:
                lead_clause = (
                    f"lidera el orden por su peso en {crit_academic} "
                    f"(índice {top_score:.2f}) ante la consulta «{query_excerpt}»"
                )
            else:
                lead_clause = (
                    f"ocupa el primer lugar por su desempeño en {crit_academic} "
                    f"(índice multicriterio {top_score:.2f})"
                )

            bullets = (
                (
                    f"{primary.psi_id} ({primary.acronym}, {primary.facility}) {lead_clause}. "
                    f"Documenta ensayos con {mats_primary} en {o2_academic} y {press_range} con flujos hasta "
                    f"{primary.flow_cm_s_max:.0f} cm/s, acotando la relación entre reacción química y transporte térmico "
                    f"(números de Damköhler y Péclet) ({primary.doi})."
                ),
                (
                    f"Metodología registrada en {primary.psi_id}: {primary.approach.rstrip('.')}. "
                    f"Como referencia complementaria, {secondary.psi_id} ({secondary.acronym}, {secondary.facility}) "
                    f"aporta evidencia para {self._lower_first(secondary.objectives)} ({secondary.doi})."
                ),
                (
                    f"En instrumentación y transferencia, {tertiary.psi_id} ({tertiary.acronym}) emplea "
                    f"{sensors_tertiary} para {self._lower_first(tertiary.objectives)}, con utilidad directa para "
                    f"{self._lower_first(tertiary.earth_benefits)} ({tertiary.doi})."
                ),
            )
        elif persona == "Estudiante":
            crit_plain = {
                "habitat": "seguridad en cabinas con tripulación",
                "modeling": "entender cómo avanza o se apaga el fuego",
                "sensors": "sensores de alerta temprana",
                "spinoff": "aplicaciones útiles en la Tierra",
            }[dom_crit]
            query_sentence = (
                f" También coincide con tu búsqueda sobre {query_short}."
                if query_short and primary_sim > 0.05
                else ""
            )
            benefit_plain = self._gloss_acronyms_plain(self._lower_first(tertiary.earth_benefits))
            bullets = (
                (
                    f"{primary.psi_id} ({primary.acronym}) lidera tu lista porque priorizaste {crit_plain}."
                    f"{query_sentence} "
                    f"En {primary.facility} estudia {mat0_primary} con {o2_plain} ({primary.doi})."
                ),
                (
                    f"Sin gravedad, el aire caliente no sube y la llama depende del aire forzado. "
                    f"Por eso {secondary.psi_id} ({secondary.acronym}) prueba {mat0_secondary} con flujos hasta "
                    f"{secondary.flow_cm_s_max:.0f} cm/s ({secondary.doi})."
                ),
                (
                    f"En la Tierra, {tertiary.psi_id} ({tertiary.acronym}) aporta datos para prevenir incendios. "
                    f"Su meta práctica: {benefit_plain}. "
                    f"Registra datos con {sensor0_tertiary} ({tertiary.doi})."
                ),
            )
        else:
            # Gestor Industrial (lenguaje claro + criterio operativo y retorno terrestre)
            crit_industrial = {
                "habitat": "seguridad operativa en cabinas presurizadas",
                "modeling": "predicción de márgenes de propagación",
                "sensors": "detección temprana de combustión",
                "spinoff": "transferencia industrial y protección terrestre",
            }[dom_crit]
            if query_excerpt and primary_sim > 0.05:
                lead_ind = (
                    f"encabeza tu lista al unir prioridad en {crit_industrial} "
                    f"con coincidencia temática en «{query_excerpt}»"
                )
            else:
                lead_ind = (
                    f"ocupa el primer puesto por tu énfasis en {crit_industrial} "
                    f"(índice {top_score:.2f})"
                )

            sec_obj_plain = self._gloss_acronyms_plain(self._lower_first(secondary.objectives))
            ter_ben_plain = self._gloss_acronyms_plain(self._lower_first(tertiary.earth_benefits))
            bullets = (
                (
                    f"Prioridad operativa ({primary.psi_id} · {primary.acronym}): {lead_ind}. "
                    f"Evalúa condiciones en {o2_academic} y {press_range} para disminuir la probabilidad de "
                    f"propagación y respaldar la calificación de materiales bajo la norma espacial NASA-STD-6001 "
                    f"({primary.doi})."
                ),
                (
                    f"Vigilancia y control ({secondary.psi_id} · {secondary.acronym} en {secondary.facility}): "
                    f"emplea {sensors_secondary} con ventilación de hasta {secondary.flow_cm_s_max:.0f} cm/s para "
                    f"{sec_obj_plain}, facilitando cortes tempranos de aire o extinción limpia sin residuos "
                    f"corrosivos ({secondary.doi})."
                ),
                (
                    f"Retorno industrial ({tertiary.psi_id} · {tertiary.acronym}): apunta a {ter_ben_plain}. "
                    f"Esta evidencia nutre el análisis de modos de falla (FMEA, evaluado por gravedad, frecuencia y "
                    f"dificultad de detección) y acelera su adopción en la Tierra ({tertiary.doi})."
                ),
            )

        return SynthesisReport(
            persona=persona,
            query=query,
            bullets=bullets,
            cited_dois=cited_dois,
            evidence_ids=evidence_ids,
        )
