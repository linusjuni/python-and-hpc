#!/bin/bash
#BSUB -q hpc
#BSUB -J ex1.4_optimize_dtypes
#BSUB -o exercises/week7/ex1.4_optimize_dtypes_%J.out
#BSUB -e exercises/week7/ex1.4_optimize_dtypes_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/optimize_dtypes.py
