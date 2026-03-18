#!/bin/bash
#BSUB -q hpc
#BSUB -J ex2.2_pyarrow_to_pandas
#BSUB -o exercises/week7/ex2.2_pyarrow_to_pandas_%J.out
#BSUB -e exercises/week7/ex2.2_pyarrow_to_pandas_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/pyarrow_to_pandas.py
