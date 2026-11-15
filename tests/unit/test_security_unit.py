"""Pruebas unitarias (RED -> GREEN) para backend.security (OWASP / STRIDE)."""

import hashlib
import json
from pathlib import Path
import pytest

from backend.security import (
    IntegrityError,
    InputValidationError,
    PayloadTooLargeError,
    RateLimitExceededError,
    SecurityBoundaryGuard,
    SlidingWindowRateLimiter,
)


def test_sliding_window_rate_limiter() -> None:
    fake_now = [100.0]
    limiter = SlidingWindowRateLimiter(
        bucket_limits={"general": 60, "ml": 20},
        window_seconds=60.0,
        clock=lambda: fake_now[0],
    )

    for _ in range(20):
        limiter.check("10.0.0.5", bucket="ml")

    with pytest.raises(RateLimitExceededError):
        limiter.check("10.0.0.5", bucket="ml")

    # Otra IP sigue permitida
    limiter.check("10.0.0.6", bucket="ml")

    # Despues de 61 segundos la ventana se limpia
    fake_now[0] += 61.0
    limiter.check("10.0.0.5", bucket="ml")

    # Bucket general permite 60
    for _ in range(60):
        limiter.check("10.0.0.8", bucket="general")
    with pytest.raises(RateLimitExceededError):
        limiter.check("10.0.0.8", bucket="general")


def test_payload_size_validation() -> None:
    guard = SecurityBoundaryGuard(max_payload_bytes=16384)
    guard.validate_request_size(16384)
    with pytest.raises(PayloadTooLargeError):
        guard.validate_request_size(16385)
    with pytest.raises(InputValidationError):
        guard.validate_request_size(-1)


def test_sanitize_query_blocks_xss_and_sqli() -> None:
    guard = SecurityBoundaryGuard()
    assert guard.sanitize_query("  BASS-II PMMA 21% O2  ") == "BASS-II PMMA 21% O2"

    with pytest.raises(InputValidationError):
        guard.sanitize_query("x" * 121, max_len=120)

    malicious_inputs = [
        "<script>alert(1)</script>",
        "javascript:alert(document.cookie)",
        "<img src=x onerror=alert(1)>",
        "BASS-II; DROP TABLE psi_investigations;--",
        "' OR 1=1 --",
        "Saffire\x00nullbyte",
    ]
    for bad in malicious_inputs:
        with pytest.raises(InputValidationError):
            guard.sanitize_query(bad)


def test_verify_model_sha256_detects_tampering(tmp_path: Path) -> None:
    guard = SecurityBoundaryGuard()

    # Rechazo estricto de .pkl / .pickle
    bad_pickle = tmp_path / "unsafe.pkl"
    bad_pickle.write_bytes(b"pickle-bytes")
    manifest_path = tmp_path / "manifest.sha256.json"
    manifest_path.write_text(json.dumps({"models": {}}), encoding="utf-8")

    with pytest.raises(IntegrityError):
        guard.verify_model_sha256(bad_pickle, manifest_path)

    # Archivo valido .joblib
    model_file = tmp_path / "dummy.joblib"
    model_file.write_bytes(b"AERO-IGNIS-MODEL-V1")
    expected_sha = hashlib.sha256(b"AERO-IGNIS-MODEL-V1").hexdigest()
    manifest_path.write_text(
        json.dumps({"models": {"dummy.joblib": {"sha256": expected_sha, "size_bytes": 19}}}),
        encoding="utf-8",
    )
    assert guard.verify_model_sha256(model_file, manifest_path) == expected_sha

    # Alterar 1 byte invalida la verificacion
    model_file.write_bytes(b"AERO-IGNIS-MODEL-V2")
    with pytest.raises(IntegrityError):
        guard.verify_model_sha256(model_file, manifest_path)
