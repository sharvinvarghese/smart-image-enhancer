from pathlib import Path

import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not read image: {path}")
    return img


def save_image(path: str, img: np.ndarray) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(out_path), img):
        raise ValueError(f"Could not write image: {path}")
