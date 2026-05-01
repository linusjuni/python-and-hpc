#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise12
#BSUB -o miniproject/jobs/exercise12_%J.out
#BSUB -e miniproject/jobs/exercise12_%J.err
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 120

N=4570

uv sync
mkdir -p miniproject/results/exercise12

echo "Processing all $N buildings with 16 workers (static scheduling)..."
time uv run python miniproject/exercise5.py $N 16 \
    > miniproject/results/exercise12/output.csv

echo "Running analysis..."
uv run python miniproject/exercise12.py miniproject/results/exercise12/output.csv
