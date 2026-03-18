#!/bin/bash
#BSUB -q hpc
#BSUB -J ex2.1_pyarrow_load
#BSUB -o exercises/week7/ex2.1_pyarrow_load_%J.out
#BSUB -e exercises/week7/ex2.1_pyarrow_load_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/pyarrow_load.py
