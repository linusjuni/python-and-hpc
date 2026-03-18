#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise2
#BSUB -o miniproject/jobs/exercise2_%J.out
#BSUB -e miniproject/jobs/exercise2_%J.err
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 30

N=20

uv sync
mkdir -p miniproject/results

time uv run python miniproject/simulate.py $N > miniproject/results/exercise2/output.csv
