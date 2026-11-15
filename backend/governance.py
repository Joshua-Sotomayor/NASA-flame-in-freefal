"""Servicio de gobernanza FMEA (NASA-STD-6001), supresion y Spinoffs Dual-Use."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FmeaRowResult:
    """Fila de modo de fallo evaluada con NPR inicial y mitigado."""

    mode_id: str
    subsystem: str
    failure_mode: str
    effect: str
    severity: int
    occurrence: int
    detection: int
    active_npr: int
    baseline_npr: int
    mitigated_npr: int
    mitigation: str
    linked_psi: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode_id": self.mode_id,
            "subsystem": self.subsystem,
            "failure_mode": self.failure_mode,
            "effect": self.effect,
            "severity": self.severity,
            "occurrence": self.occurrence,
            "detection": self.detection,
            "active_npr": self.active_npr,
            "baseline_npr": self.baseline_npr,
            "mitigated_npr": self.mitigated_npr,
            "mitigation": self.mitigation,
            "linked_psi": self.linked_psi,
        }


@dataclass(frozen=True)
class FmeaReport:
    """Evaluacion completa de riesgos bajo NASA-STD-6001."""

    mitigated: bool
    rows: tuple[FmeaRowResult, ...]
    total_baseline_npr: int
    total_active_npr: int
    average_npr_reduction_pct: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "mitigated": self.mitigated,
            "total_baseline_npr": self.total_baseline_npr,
            "total_active_npr": self.total_active_npr,
            "average_npr_reduction_pct": round(self.average_npr_reduction_pct, 2),
            "rows": [row.to_dict() for row in self.rows],
        }


@dataclass(frozen=True)
class DualUseImpact:
    """Calculadora cuantitativa de impacto terrestre de tecnologias Spinoff NASA."""

    spinoff_id: str
    name: str
    units: int
    origin_nasa: str
    earth_impact: str
    weight_saved_lb_total: float
    risk_reduction_pct: float
    linked_psi: str
    url: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "spinoff_id": self.spinoff_id,
            "name": self.name,
            "units": self.units,
            "origin_nasa": self.origin_nasa,
            "earth_impact": self.earth_impact,
            "weight_saved_lb_total": round(self.weight_saved_lb_total, 2),
            "risk_reduction_pct": round(self.risk_reduction_pct, 2),
            "linked_psi": self.linked_psi,
            "url": self.url,
        }


@dataclass(frozen=True)
class SuppressionRecommendation:
    """Resultado del arbol determinista de seleccion PFE vs CO2 vs E-FIELD."""

    recommended_agent: str
    rationale: str
    eclss_safe: bool


class GovernanceAndSpinoffService:
    """Servicio POO de riesgo FMEA, supresion ECLSS e impacto Dual-Use."""

    def __init__(self, cases_json_path: Path) -> None:
        path = Path(cases_json_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        self._fmea_raw: tuple[dict[str, Any], ...] = tuple(payload.get("fmea_modes", []))
        self._spinoffs: dict[str, dict[str, Any]] = {
            str(item["spinoff_id"]): item for item in payload.get("spinoffs", [])
        }
        self._official_resources: tuple[dict[str, Any], ...] = tuple(payload.get("official_resources", []))

    def evaluate_fmea(self, mitigated: bool = False) -> FmeaReport:
        rows: list[FmeaRowResult] = []
        total_base = 0
        total_active = 0
        for raw in self._fmea_raw:
            s_base = int(raw["severity"])
            o_base = int(raw["occurrence"])
            d_base = int(raw["detection"])
            base_npr = s_base * o_base * d_base

            s_mit = int(raw["mitigated_severity"])
            o_mit = int(raw["mitigated_occurrence"])
            d_mit = int(raw["mitigated_detection"])
            mit_npr = s_mit * o_mit * d_mit

            active_npr = mit_npr if mitigated else base_npr
            total_base += base_npr
            total_active += active_npr

            rows.append(
                FmeaRowResult(
                    mode_id=str(raw["mode_id"]),
                    subsystem=str(raw["subsystem"]),
                    failure_mode=str(raw["failure_mode"]),
                    effect=str(raw["effect"]),
                    severity=s_mit if mitigated else s_base,
                    occurrence=o_mit if mitigated else o_base,
                    detection=d_mit if mitigated else d_base,
                    active_npr=active_npr,
                    baseline_npr=base_npr,
                    mitigated_npr=mit_npr,
                    mitigation=str(raw["mitigation"]),
                    linked_psi=str(raw["linked_psi"]),
                )
            )

        reduction = ((total_base - total_active) / total_base * 100.0) if total_base > 0 else 0.0
        return FmeaReport(
            mitigated=mitigated,
            rows=tuple(rows),
            total_baseline_npr=total_base,
            total_active_npr=total_active,
            average_npr_reduction_pct=reduction,
        )

    def select_suppression_protocol(
        self,
        fire_type: str,
        habitable_crew: bool = True,
        auto_oxidizing: bool = False,
    ) -> SuppressionRecommendation:
        """Arbol de decision PFE vs CO2 vs E-FIELD segun toxicidad ECLSS y fisica 0g."""
        kind = fire_type.strip().lower()
        if not kind:
            raise ValueError("fire_type no puede estar vacio.")
        if auto_oxidizing or kind in {"auto_oxidizing", "vika", "liclo4", "smoldering"}:
            return SuppressionRecommendation(
                recommended_agent="PFE",
                rationale=(
                    "Niebla de agua fina (20-100 um) enfria superficie con calor latente 2,260 kJ/kg "
                    "e inunda frente auto-oxidante donde cortar ventilacion o aplicar CO2 resulta insuficiente."
                ),
                eclss_safe=True,
            )
        if kind in {"laminar_diffusion", "electronic_clean", "efield"}:
            return SuppressionRecommendation(
                recommended_agent="E-FIELD",
                rationale=(
                    "Campo electrico +/-10 kV (ACME PSI-154) deforma y extingue llamas laminares mediante "
                    "viento ionico sin consumir agente ni recargar depuradores ECLSS."
                ),
                eclss_safe=True,
            )
        if not habitable_crew and kind in {"uncrewed_rack", "cargo_co2"}:
            return SuppressionRecommendation(
                recommended_agent="CO2",
                rationale="Aplicable solo en volumen aislado sin tripulacion por riesgo de hipercapnia en ECLSS.",
                eclss_safe=False,
            )
        return SuppressionRecommendation(
            recommended_agent="PFE",
            rationale="Extintor estandar ISS PFE seguro para avionica y libre de HF/HBr corrosivos.",
            eclss_safe=True,
        )

    def calculate_dual_use(self, spinoff_id: str | None = None, units: int = 1) -> DualUseImpact:
        if isinstance(units, bool) or not isinstance(units, int) or not (1 <= units <= 10000):
            raise ValueError("units debe ser un entero entre 1 y 10000.")
        cleaned = spinoff_id.strip().upper() if spinoff_id is not None else ""
        key = cleaned or "9582"
        if key not in self._spinoffs:
            raise KeyError(f"Spinoff no encontrado: {key}")

        sp = self._spinoffs[key]
        saved_per_unit = float(sp["weight_saved_lb_per_unit"])
        return DualUseImpact(
            spinoff_id=key,
            name=str(sp["name"]),
            units=units,
            origin_nasa=str(sp["origin_nasa"]),
            earth_impact=str(sp["earth_impact"]),
            weight_saved_lb_total=saved_per_unit * float(units),
            risk_reduction_pct=float(sp["risk_reduction_pct"]),
            linked_psi=str(sp["linked_psi"]),
            url=str(sp["url"]),
        )
