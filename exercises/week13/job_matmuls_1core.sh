#!/bin/bash
#BSUB -q hpc
#BSUB -W 30
#BSUB -J matmuls_1core
#BSUB -o matmuls_1core_%J.out
#BSUB -e matmuls_1core_%J.err
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=20GB]"

uv sync
uv run python exercises/week13/matmuls.py
