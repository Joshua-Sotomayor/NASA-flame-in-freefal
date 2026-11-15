"""Pruebas de integracion para datos maestros PSI, BASS-II/Saffire CSV y fallback OSDR."""

import csv
import json
from pathlib import Path
import requests

from backend.domain import OsdrApiClient, PsiRepository

ROOT_DIR = Path(__file__).resolve().parents[2]
PSI_JSON_PATH = ROOT_DIR / "data" / "psi_combustion_24.json"
BASS_SAFFIRE_CSV_PATH = ROOT_DIR / "data" / "bass_saffire_runs.csv"
CASES_SPINOFFS_PATH = ROOT_DIR / "data" / "cases_and_spinoffs.json"

FORBIDDEN_ROCKET_TERMS = ("rocket engine", "thruster", "propulsor", "motor cohete", "bipropellant")


def test_psi_repository_loads_exact_24_investigations() -> None:
    repo = PsiRepository(data_path=PSI_JSON_PATH)
    all_items = repo.all_investigations()
    assert len(all_items) == 24
    assert len({item.psi_id for item in all_items}) == 24

    valid_facilities = {"ISS-CIR", "ISS-MSG", "Cygnus", "Otros"}
    for item in all_items:
        assert item.doi.startswith("10.60555/")
        assert item.facility in valid_facilities
        combined_text = f"{item.acronym} {item.objectives} {item.approach} {item.earth_benefits}".lower()
        for banned in FORBIDDEN_ROCKET_TERMS:
            assert banned not in combined_text, f"Contenido fuera de alcance C-01 en {item.psi_id}: {banned}"

    cygnus_res = repo.list_investigations(facility="Cygnus", page=1, page_size=50)
    assert cygnus_res.total == 6


def test_osdr_client_offline_fallback_integration() -> None:
    def failing_http_get(url: str, timeout: float, allow_redirects: bool) -> object:
        assert allow_redirects is False
        assert timeout <= 3.0
        raise requests.Timeout("Simulated NASA OSDR network timeout")

    client = OsdrApiClient(timeout_s=3.0)
    repo = PsiRepository(data_path=PSI_JSON_PATH, osdr_client=client)
    metadata = repo.fetch_osdr_metadata_safe("PSI-25", http_get=failing_http_get)

    assert metadata["source"] == "local_fallback"
    assert metadata["psi_id"] == "PSI-25"
    assert metadata["acronym"] == "BASS-II"
    assert metadata["doi"].startswith("10.60555/")


def test_bass_saffire_csv_and_cases_json_integrity() -> None:
    assert BASS_SAFFIRE_CSV_PATH.exists()
    with BASS_SAFFIRE_CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) >= 140
    required_cols = {
        "run_id",
        "campaign",
        "facility",
        "material",
        "o2_pct",
        "pressure_psi",
        "flow_cm_s",
        "gravity_g",
        "thickness_mm",
        "flow_dir",
        "extinguished",
        "burn_time_s",
        "flame_spread_mm_s",
        "regime",
    }
    assert required_cols.issubset(set(rows[0].keys()))

    assert CASES_SPINOFFS_PATH.exists()
    payload = json.loads(CASES_SPINOFFS_PATH.read_text(encoding="utf-8"))
    forensic_ids = {item["case_id"] for item in payload["forensic_cases"]}
    assert {"apollo_1", "apollo_13", "mir_1997"}.issubset(forensic_ids)

    spinoff_ids = {item["spinoff_id"] for item in payload["spinoffs"]}
    assert {"9582", "9407", "9918", "PFE"} == spinoff_ids
    assert len(payload["official_resources"]) == 10
    assert len(payload["fmea_modes"]) >= 6
