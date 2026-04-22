# 02613 Fast Python and HPC - UV Environment

This is a UV port of the course conda environment.

## Setup

Instead of:
```bash
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
```

Simply:
```bash
uv sync  # First time only
uv run your_script.py
```

## Migration Notes

This environment was migrated from the course conda environment `02613_2026` on 2026-04-22.

The project is pinned to `==3.12.*` (matching the conda env exactly) to avoid numpy/pandas compatibility conflicts on future Python versions.

**Differences from the conda environment:**

- **OpenBLAS instead of MKL** — `mkl-fft`, `mkl-random`, and `mkl-service` are not available on PyPI for this Python version; the conda env uses OpenBLAS anyway.
- **CuPy** — PyPI `cupy-cuda12x==13.6.0` is used in place of conda's `cupy==13.6.0` (which bundles CUDA 13 libraries directly). If the HPC nodes expose CUDA 13 but not 12, switch to the generic `cupy` package.
- **`tzdata`** — Pinned loosely (`>=2025.1`) since conda uses a different version scheme (`2025c`) than PyPI (`2026.1`).