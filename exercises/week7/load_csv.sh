#!/bin/bash
#BSUB -q hpc
#BSUB -J ex1.1_load_csv
#BSUB -o exercises/week7/ex1.1_load_csv_%J.out
#BSUB -e exercises/week7/ex1.1_load_csv_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/load_csv.py
