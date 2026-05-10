#!/bin/bash
#BSUB -q hpc
#BSUB -W 30
#BSUB -J matmuls_8core
#BSUB -o matmuls_8core_%J.out
#BSUB -e matmuls_8core_%J.err
#BSUB -n 8
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=20GB]"
#BSUB -R "span[hosts=1]"

uv sync
uv run python exercises/week13/matmuls.py
