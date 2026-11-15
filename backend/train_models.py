"""Pipeline de entrenamiento reproducible en CPU local para los 3 modelos ML/DL propios.

Sincronizado con `notebooks/AERO_IGNIS_Colab_Training.ipynb`. Genera pesos ligeros (<15 MB)
y el manifiesto criptografico `artifacts/models/manifest.sha256.json` para verificacion OWASP.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
import torch
import torch.nn as nn

from backend.domain import (
    FLAME_CLASS_LABELS,
    FLAMMABILITY_FEATURES,
    MATERIAL_REACTIVITY_MAP,
    OPTICAL_PRESET_TO_IDX,
    SENSOR_CLASS_LABELS,
    SENSOR_FEATURES,
    generate_optical_frame,
    preset_to_input_tensor,
)
from backend.security import SecurityBoundaryGuard


SEED: int = 42

EXPECTED_ARTIFACTS: tuple[str, ...] = (
    "flammability_rf.joblib",
    "burntime_gbr.joblib",
    "flame_cnn.onnx",
    "sensor_tree.joblib",
    "psi_tfidf_kmeans.joblib",
)


class FlameCnnNet(nn.Module):
    """CNN compacta PyTorch para clasificacion optica de regimenes de llama en microgravedad."""

    def __init__(self, num_classes: int = 4) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AvgPool2d(kernel_size=8, stride=8),
            nn.Flatten(),
            nn.Linear(16 * 4 * 4, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def _train_flammability_models(csv_path: Path, out_dir: Path) -> dict[str, float]:
    df = pd.read_csv(csv_path)
    features_df = pd.DataFrame(
        {
            "o2_pct": df["o2_pct"].astype(float),
            "pressure_atm": df["pressure_psi"].astype(float) / 14.7,
            "air_flow_cms": df["flow_cm_s"].astype(float),
            "gravity_g": df["gravity_g"].astype(float),
            "thickness_cm": df["thickness_mm"].astype(float) / 10.0,
            "flow_concurrent": (df["flow_dir"] == "concurrent").astype(float),
            "material_reactivity": df["material"].map(MATERIAL_REACTIVITY_MAP).fillna(1.0).astype(float),
        }
    )
    X = features_df[list(FLAMMABILITY_FEATURES)].to_numpy(dtype=np.float64)
    y_cls = df["extinguished"].to_numpy(dtype=int)
    y_burn = df["burn_time_s"].to_numpy(dtype=np.float64)
    y_spread = df["flame_spread_mm_s"].to_numpy(dtype=np.float64)

    rf_cls = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=SEED, n_jobs=1)
    cv_acc = float(cross_val_score(rf_cls, X, y_cls, cv=5).mean())
    rf_cls.fit(X, y_cls)

    burn_gbr = GradientBoostingRegressor(n_estimators=120, max_depth=4, random_state=SEED)
    spread_gbr = GradientBoostingRegressor(n_estimators=120, max_depth=4, random_state=SEED)
    burn_gbr.fit(X, y_burn)
    spread_gbr.fit(X, y_spread)

    joblib.dump(
        {
            "model": rf_cls,
            "feature_names": list(FLAMMABILITY_FEATURES),
            "material_map": dict(MATERIAL_REACTIVITY_MAP),
            "cv_accuracy": round(cv_acc, 4),
        },
        out_dir / "flammability_rf.joblib",
        compress=3,
    )
    joblib.dump(
        {
            "model": burn_gbr,
            "burn_time_model": burn_gbr,
            "spread_model": spread_gbr,
            "feature_names": list(FLAMMABILITY_FEATURES),
        },
        out_dir / "burntime_gbr.joblib",
        compress=3,
    )
    return {"rf_cv_accuracy": round(cv_acc, 4)}


def _train_duct_cnn_and_tree(out_dir: Path) -> dict[str, float]:
    torch.manual_seed(SEED)
    presets = ("nominal", "spherical_0g", "cool_flame_ntc", "open_propagation")
    imgs: list[np.ndarray] = []
    labels: list[int] = []
    for cls_idx, preset in enumerate(presets):
        for sample_idx in range(45):
            frame = generate_optical_frame(
                preset=preset,
                noise_std=0.035,
                seed=SEED * 100 + cls_idx * 100 + sample_idx,
            )
            imgs.append(frame)
            labels.append(cls_idx)

    X_img = torch.tensor(np.asarray(imgs)[:, None, :, :], dtype=torch.float32)
    y_img = torch.tensor(labels, dtype=torch.long)

    cnn = FlameCnnNet(num_classes=4)
    optimizer = torch.optim.Adam(cnn.parameters(), lr=4e-3)
    loss_fn = nn.CrossEntropyLoss()

    cnn.train()
    for _ in range(45):
        optimizer.zero_grad()
        logits = cnn(X_img)
        loss = loss_fn(logits, y_img)
        loss.backward()
        optimizer.step()

    cnn.eval()
    with torch.no_grad():
        preds = cnn(X_img).argmax(dim=1)
        cnn_acc = float((preds == y_img).float().mean().item())

    dummy_input = torch.zeros((1, 1, 64, 64), dtype=torch.float32)
    onnx_path = out_dir / "flame_cnn.onnx"
    torch.onnx.export(
        cnn,
        dummy_input,
        str(onnx_path),
        input_names=["frame"],
        output_names=["logits"],
        opset_version=14,
        dynamo=False,
    )

    # Entrenamiento del arbol tabular explicable de sensores
    rng = np.random.default_rng(SEED)
    n_samples = 600
    delta_t_dt = rng.uniform(-1.0, 35.0, n_samples)
    co_ppm = rng.uniform(0.0, 420.0, n_samples)
    aerosol = rng.uniform(0.0, 90.0, n_samples)
    airflow = rng.uniform(1.0, 50.0, n_samples)
    X_sens = np.column_stack([delta_t_dt, co_ppm, aerosol, airflow])
    y_sens = np.where(
        (delta_t_dt >= 12.0) | (co_ppm >= 150.0) | (aerosol >= 55.0),
        2,
        np.where((aerosol >= 18.0) | (co_ppm >= 35.0) | (delta_t_dt >= 4.0), 1, 0),
    )

    sensor_tree = DecisionTreeClassifier(max_depth=4, random_state=SEED)
    sensor_tree.fit(X_sens, y_sens)
    tree_acc = float(sensor_tree.score(X_sens, y_sens))

    joblib.dump(
        {
            "model": sensor_tree,
            "feature_names": list(SENSOR_FEATURES),
            "class_labels": list(SENSOR_CLASS_LABELS),
            "train_accuracy": round(tree_acc, 4),
        },
        out_dir / "sensor_tree.joblib",
        compress=3,
    )
    return {"cnn_train_accuracy": round(cnn_acc, 4), "sensor_tree_accuracy": round(tree_acc, 4)}


def _train_psi_nlp_clusters(psi_json_path: Path, out_dir: Path) -> dict[str, int]:
    payload = json.loads(psi_json_path.read_text(encoding="utf-8"))
    investigations = payload["investigations"]
    psi_ids: list[str] = []
    corpus: list[str] = []
    for item in investigations:
        psi_ids.append(str(item["psi_id"]))
        text = " ".join(
            [
                str(item["acronym"]),
                str(item["facility"]),
                str(item["category"]),
                " ".join(item.get("materials", [])),
                " ".join(item.get("sensors", [])),
                str(item["objectives"]),
                str(item["approach"]),
                str(item["earth_benefits"]),
            ]
        )
        corpus.append(text)

    vectorizer = TfidfVectorizer(max_features=320, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus).toarray()
    pca = PCA(n_components=2, random_state=SEED)
    coords_2d = pca.fit_transform(tfidf_matrix)
    kmeans = KMeans(n_clusters=4, n_init=10, random_state=SEED)
    labels = kmeans.fit_predict(tfidf_matrix)

    joblib.dump(
        {
            "vectorizer": vectorizer,
            "pca": pca,
            "kmeans": kmeans,
            "psi_ids": psi_ids,
            "tfidf_matrix": tfidf_matrix,
            "coords_2d": coords_2d,
            "labels": labels,
        },
        out_dir / "psi_tfidf_kmeans.joblib",
        compress=3,
    )
    return {"psi_clustered": len(psi_ids), "clusters": 4}


def train_all_models(data_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Entrena todos los modelos locales y genera el manifiesto SHA-256."""
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    flam_metrics = _train_flammability_models(data_dir / "bass_saffire_runs.csv", output_dir)
    duct_metrics = _train_duct_cnn_and_tree(output_dir)
    nlp_metrics = _train_psi_nlp_clusters(data_dir / "psi_combustion_24.json", output_dir)

    models_manifest: dict[str, dict[str, Any]] = {}
    for artifact_name in EXPECTED_ARTIFACTS:
        artifact_path = output_dir / artifact_name
        digest = SecurityBoundaryGuard.compute_sha256(artifact_path)
        models_manifest[artifact_name] = {
            "sha256": digest,
            "size_bytes": artifact_path.stat().st_size,
        }

    manifest_payload = {
        "schema_version": "1.0.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "metrics": {**flam_metrics, **duct_metrics, **nlp_metrics},
        "models": models_manifest,
    }
    (output_dir / "manifest.sha256.json").write_text(
        json.dumps(manifest_payload, indent=2),
        encoding="utf-8",
    )
    return manifest_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrenamiento ML/DL local AERO-IGNIS SI.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/models"))
    args = parser.parse_args()

    manifest = train_all_models(data_dir=args.data_dir, output_dir=args.output_dir)
    total_kb = sum(entry["size_bytes"] for entry in manifest["models"].values()) / 1024.0
    print(f"Artefactos ML/DL generados OK ({total_kb:.1f} KB total):")
    print(json.dumps(manifest["metrics"], indent=2))


if __name__ == "__main__":
    main()
