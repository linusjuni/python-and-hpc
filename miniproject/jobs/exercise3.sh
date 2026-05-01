#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise3
#BSUB -o miniproject/jobs/exercise3_%J.out
#BSUB -e miniproject/jobs/exercise3_%J.err
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 30

N=20

export PATH="$HOME/.local/bin:$PATH"

uv sync
mkdir -p miniproject/results/exercise3

time uv run python miniproject/exercise3.py $N > miniproject/results/exercise3/output.csv
