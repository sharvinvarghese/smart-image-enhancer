import cv2
import numpy as np


def to_gray(img: np.ndarray) -> np.ndarray:
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def smart_clahe(img: np.ndarray, auto_params: bool = False) -> np.ndarray:
    gray = to_gray(img)
    mean = float(gray.mean())
    std = float(gray.std())

    if auto_params:
        # Simple heuristic: darker + flatter images get stronger CLAHE
        if mean < 80:
            clip_limit = 4.0
        elif mean < 150:
            clip_limit = 2.5
        else:
            clip_limit = 1.5

        if std < 40:
            tile_size = 8
        else:
            tile_size = 16
    else:
        clip_limit = 2.0
        tile_size = 8

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))

    if len(img.shape) == 2:
        enhanced = clahe.apply(img)
    else:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l_clahe = clahe.apply(l)
        lab_clahe = cv2.merge((l_clahe, a, b))
        enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

    return enhanced


# Placeholder implementations for future algorithms

def ahe(img: np.ndarray, auto_params: bool = False) -> np.ndarray:
    # For now, reuse smart_clahe as a stand-in; to be replaced with true AHE.
    return smart_clahe(img, auto_params=auto_params)


def gamma_auto(img: np.ndarray, auto_params: bool = False) -> np.ndarray:
    gray = to_gray(img)
    mean = float(gray.mean())

    # Estimate gamma from mean brightness (simple heuristic)
    gamma = 1.0
    if auto_params:
        if mean < 60:
            gamma = 0.6
        elif mean < 120:
            gamma = 0.8
        elif mean < 180:
            gamma = 1.1
        else:
            gamma = 1.3

    inv_gamma = 1.0 / gamma if gamma != 0 else 1.0
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(img, table)


AVAILABLE_ALGOS = {
    "clahe": smart_clahe,
    "ahe": ahe,
    "gamma_auto": gamma_auto,
}
