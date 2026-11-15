"""Pruebas unitarias (RED -> GREEN) para el pipeline ML/DL propio (`backend.train_models`)."""

import numpy as np
import torch

from backend.train_models import (
    FLAME_CLASS_LABELS,
    FlameCnnNet,
    generate_optical_frame,
    preset_to_input_tensor,
)


def test_flame_cnn_architecture_and_feature_extractor() -> None:
    assert len(FLAME_CLASS_LABELS) == 4
    model = FlameCnnNet(num_classes=4)
    model.eval()

    x = torch.zeros((2, 1, 64, 64), dtype=torch.float32)
    with torch.no_grad():
        logits = model(x)
    assert tuple(logits.shape) == (2, 4)

    for preset in ("nominal", "spherical_0g", "cool_flame_ntc", "open_propagation"):
        frame = generate_optical_frame(preset=preset, seed=42)
        assert frame.shape == (64, 64)
        assert np.all(frame >= 0.0) and np.all(frame <= 1.0)
        tensor = preset_to_input_tensor(preset=preset)
        assert tensor.shape == (1, 1, 64, 64)
        assert tensor.dtype == np.float32


def test_vector64_to_input_tensor_shape_and_bounds() -> None:
    vec = [float(i) / 64.0 for i in range(64)]
    tensor = preset_to_input_tensor(optical_vector=vec)
    assert tensor.shape == (1, 1, 64, 64)
    assert np.isfinite(tensor).all()
