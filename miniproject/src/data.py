from os.path import join
from pathlib import Path

import numpy as np

from src.utils.settings import settings


def load_data(bid: str, load_dir: Path = settings.DATA_DIR) -> tuple[np.ndarray, np.ndarray]:
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


def load_building_ids(load_dir: Path = settings.DATA_DIR) -> list[str]:
    with open(join(load_dir, "building_ids.txt"), "r") as f:
        return f.read().splitlines()
