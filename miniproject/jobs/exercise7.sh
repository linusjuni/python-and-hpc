#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise7
#BSUB -o miniproject/jobs/exercise7_%J.out
#BSUB -e miniproject/jobs/exercise7_%J.err
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 30

N=20

export PATH="$HOME/.local/bin:$PATH"

uv sync
mkdir -p miniproject/results/exercise7

time uv run python miniproject/exercise7.py $N > miniproject/results/exercise7/output.csv