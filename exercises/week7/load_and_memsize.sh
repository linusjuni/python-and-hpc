#!/bin/bash
#BSUB -q hpc
#BSUB -J ex1.2_memsize
#BSUB -o exercises/week7/ex1.2_memsize_%J.out
#BSUB -e exercises/week7/ex1.2_memsize_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/load_and_memsize.py
