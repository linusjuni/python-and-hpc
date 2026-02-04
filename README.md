# 02613 Fast Python and HPC - UV Environment

This is a UV port of the course conda environment.

## Setup

Instead of:
```bash
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
```

Simply:
```bash
uv sync  # First time only
uv run your_script.py
```

## Migration Notes

This environment was migrated from the course conda environment on 2025-02-04.

Minor version bumps were required for MKL packages (mkl-fft, mkl-random, mkl-service) because PyPI wheels for the original versions lacked Python 3.11 support. Conda's build infrastructure had Python 3.11 builds of these older versions, but PyPI did not. NumPy was also bumped from 1.26.2 to 1.26.4 to satisfy MKL dependencies.

All functionality should be preserved.