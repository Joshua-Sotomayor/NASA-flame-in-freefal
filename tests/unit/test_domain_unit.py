"""Pruebas unitarias (RED -> GREEN) para backend.domain (PsiInvestigation, PsiRepository, OsdrApiClient)."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import json
import re
import pytest

from backend.domain import (
    OsdrApiClient,
    PaginatedResult,
    PsiInvestigation,
    PsiRepository,
    SecurityViolationError,
)


def _sample_investigation(psi_id: str = "PSI-25", facility: str = "ISS-MSG") -> PsiInvestigation:
    return PsiInvestigation(
        psi_id=psi_id,
        acronym="BASS-II",
        facility=facility,
        doi="10.60555/psi-25",
        osdr_id="OSD-98",
        o2_min=17.0,
        o2_max=28.0,
        pressure_psi_min=10.2,
        pressure_psi_max=14.7,
        flow_cm_s_max=50.0,
        materials=("PMMA", "SIBAL", "Nomex", "Kapton"),
        sensors=("Radiometer", "HD Camera", "Thermocouple"),
        objectives="Cuantificar limites de extincion radiativa y por soplado en solidos en microgravedad.",
        approach="Ensayos en ducto MSG con variaciones de flujo forzado y porcentaje de O2.",
        earth_benefits="Mejorar modelado de retardantes textiles y seguridad en recintos cerrados.",
        category="Solidos en Microgravedad",
        criteria_scores=(("habitat", 0.92), ("modeling", 0.98), ("sensors", 0.78), ("spinoff", 0.74)),
    )


def test_psi_investigation_is_frozen_dataclass() -> None:
    psi = _sample_investigation()
    with pytest.raises(FrozenInstanceError):
        psi.acronym = "MUTATED"  # type: ignore[misc]


def test_osdr_client_ssrf_allowlist() -> None:
    client = OsdrApiClient(timeout_s=3.0)
    assert client.validate_url("https://osdr.nasa.gov/osdr/data/osd/meta/98").startswith("https://osdr.nasa.gov")
    assert client.validate_url("https://visualization.osdr.nasa.gov/biodata/api/study/OSD-98").startswith(
        "https://visualization.osdr.nasa.gov"
    )

    blocked_urls = [
        "http://osdr.nasa.gov/osdr/data/osd/meta/98",
        "http://169.254.169.254/latest/meta-data/",
        "https://evil.com/osdr.nasa.gov",
        "file:///etc/passwd",
        "https://user:pass@osdr.nasa.gov/api",
        "https://localhost:8000/api/v1/health",
    ]
    for bad_url in blocked_urls:
        with pytest.raises(SecurityViolationError):
            client.validate_url(bad_url)


def test_pagination_and_filtering_bounds(tmp_path: Path) -> None:
    items = []
    for idx in range(1, 7):
        items.append(
            {
                "psi_id": f"PSI-{97 + idx}",
                "acronym": f"SAFFIRE-{idx}",
                "facility": "Cygnus",
                "doi": f"10.60555/psi-{97 + idx}",
                "osdr_id": f"OSD-{97 + idx}",
                "o2_min": 21.0,
                "o2_max": 34.0,
                "pressure_psi_min": 8.2,
                "pressure_psi_max": 14.7,
                "flow_cm_s_max": 30.0,
                "materials": ["SIBAL"],
                "sensors": ["Anemometer", "Thermocouple"],
                "objectives": "Combustion a escala real en cabina Cygnus.",
                "approach": "Ignicion controlada post-desacople.",
                "earth_benefits": "Seguridad contra incendios en recintos ventilados.",
                "category": "Campanas Saffire",
                "criteria_scores": {"habitat": 0.95, "modeling": 0.85, "sensors": 0.88, "spinoff": 0.80},
            }
        )
    data_file = tmp_path / "psi.json"
    data_file.write_text(json.dumps({"investigations": items}), encoding="utf-8")

    repo = PsiRepository(data_path=data_file)
    res = repo.list_investigations(facility="Cygnus", page=1, page_size=4)
    assert isinstance(res, PaginatedResult)
    assert res.total == 6
    assert len(res.items) == 4
    assert res.total_pages == 2

    with pytest.raises(ValueError):
        repo.list_investigations(page_size=51)
    with pytest.raises(ValueError):
        repo.list_investigations(page=0)
    with pytest.raises(ValueError):
        repo.list_investigations(facility="RocketEnginePad")


def test_osdr_client_rejects_invalid_accession_format() -> None:
    client = OsdrApiClient()
    with pytest.raises(SecurityViolationError):
        client.fetch_study_metadata("../../../etc/passwd")


def test_psi_taxonomy_validation_and_objective_invariants() -> None:
    data_path = Path(__file__).resolve().parents[2] / "data" / "psi_combustion_24.json"
    assert data_path.exists(), "Archivo maestro data/psi_combustion_24.json inexistente"

    repo = PsiRepository(data_path=data_path)
    all_items = repo.all_investigations()
    assert len(all_items) == 24, "Debe contener exactamente 24 investigaciones PSI"

    facilities_count = {"Cygnus": 0, "ISS-MSG": 0, "ISS-CIR": 0, "Otros": 0}
    categories = set()
    banned_keywords = ("rocket", "cohete", "thruster", "propulsor", "bipropellant")
    doi_pattern = re.compile(r"^10\.60555/psi-\d+$")

    for item in all_items:
        assert doi_pattern.match(item.doi), f"DOI inválido en {item.psi_id}: {item.doi}"
        assert item.facility in facilities_count, f"Instalación no reconocida en {item.psi_id}: {item.facility}"
        facilities_count[item.facility] += 1

        assert 10.0 <= item.o2_min <= item.o2_max <= 100.0, f"Rango O2 inválido en {item.psi_id}"
        assert 5.0 <= item.pressure_psi_min <= item.pressure_psi_max <= 35.0, f"Presión inválida en {item.psi_id}"
        assert 0.0 <= item.flow_cm_s_max <= 100.0, f"Velocidad de flujo anormal en {item.psi_id}"

        scores_dict = dict(item.criteria_scores)
        for criterion in ("habitat", "modeling", "sensors", "spinoff"):
            assert criterion in scores_dict, f"Falta criterio {criterion} en {item.psi_id}"
            score = scores_dict[criterion]
            assert 0.0 <= score <= 1.0, f"Puntuación fuera de rango [0, 1] en {item.psi_id}: {score}"

        blob = f"{item.acronym} {item.objectives} {item.approach} {item.earth_benefits}".lower()
        for banned in banned_keywords:
            assert banned not in blob, f"Término prohibido C-01 '{banned}' hallado en {item.psi_id}"

        categories.add(item.category)

    assert facilities_count["Cygnus"] == 6
    assert facilities_count["ISS-MSG"] == 6
    assert facilities_count["ISS-CIR"] == 10
    assert facilities_count["Otros"] == 2

    expected_categories = {
        "Campanas Saffire (Cabina Real)",
        "Solidos en Microgravedad",
        "Llamas Gaseosas y Campos Electricos",
        "Gotas y Llamas Frias",
        "Termofluidos Interfaciales",
    }
    assert categories == expected_categories

