"""Pruebas de integracion para entrenamiento local, artefactos <15MB, SHA-256 e inferencia ONNX/Joblib."""

from pathlib import Path
import time
import joblib
import onnxruntime as ort

from backend.security import SecurityBoundaryGuard
from backend.train_models import (
    EXPECTED_ARTIFACTS,
    generate_optical_frame,
    train_all_models,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT_DIR / "artifacts" / "models"


def test_trained_artifacts_exist_under_15mb_and_verified_sha256() -> None:
    start = time.perf_counter()
    manifest = train_all_models(
        data_dir=ROOT_DIR / "data",
        output_dir=ARTIFACTS_DIR,
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 15.0

    manifest_path = ARTIFACTS_DIR / "manifest.sha256.json"
    assert manifest_path.exists()
    assert set(EXPECTED_ARTIFACTS).issubset(set(manifest["models"].keys()))

    guard = SecurityBoundaryGuard()
    total_bytes = 0
    for artifact_name in EXPECTED_ARTIFACTS:
        artifact_path = ARTIFACTS_DIR / artifact_name
        assert artifact_path.exists()
        total_bytes += artifact_path.stat().st_size
        guard.verify_model_sha256(artifact_path, manifest_path)

    assert total_bytes < 15 * 1024 * 1024


def test_onnx_and_joblib_runtime_inference_integration() -> None:
    sess_opts = ort.SessionOptions()
    sess_opts.intra_op_num_threads = 1
    session = ort.InferenceSession(
        str(ARTIFACTS_DIR / "flame_cnn.onnx"),
        sess_options=sess_opts,
        providers=["CPUExecutionProvider"],
    )
    input_name = session.get_inputs()[0].name

    # Verifica que las 4 clases visuales se separan con latencia < 25 ms
    for expected_cls, preset in enumerate(
        ("nominal", "spherical_0g", "cool_flame_ntc", "open_propagation")
    ):
        frame = generate_optical_frame(preset=preset, noise_std=0.0, seed=42)[None, None, :, :]
        t0 = time.perf_counter()
        logits = session.run(None, {input_name: frame})[0]
        dt_ms = (time.perf_counter() - t0) * 1000.0
        assert dt_ms < 25.0
        assert int(logits[0].argmax()) == expected_cls

    # Verifica modelos joblib (RandomForest, GradientBoosting, DecisionTree, TF-IDF/PCA/KMeans)
    rf_bundle = joblib.load(ARTIFACTS_DIR / "flammability_rf.joblib")
    gbr_bundle = joblib.load(ARTIFACTS_DIR / "burntime_gbr.joblib")
    sensor_tree = joblib.load(ARTIFACTS_DIR / "sensor_tree.joblib")
    nlp_bundle = joblib.load(ARTIFACTS_DIR / "psi_tfidf_kmeans.joblib")

    assert hasattr(rf_bundle["model"], "predict_proba")
    assert hasattr(gbr_bundle["model"], "predict")
    assert hasattr(sensor_tree["model"], "decision_path")
    assert nlp_bundle["kmeans"].n_clusters == 4
    assert len(nlp_bundle["psi_ids"]) == 24
