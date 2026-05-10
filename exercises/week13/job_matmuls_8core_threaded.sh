#!/bin/bash
#BSUB -q hpc
#BSUB -W 30
#BSUB -J matmuls_8core_threaded
#BSUB -o matmuls_8core_threaded_%J.out
#BSUB -e matmuls_8core_threaded_%J.err
#BSUB -n 8
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=20GB]"
#BSUB -R "span[hosts=1]"

export MPI_NUM_THREADS=8
export OMP_NUM_THREADS=8

uv sync
uv run python exercises/week13/matmuls.py
