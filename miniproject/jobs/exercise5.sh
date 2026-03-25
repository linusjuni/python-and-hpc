#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise5_static
#BSUB -o miniproject/jobs/exercise5_static_%J.out
#BSUB -e miniproject/jobs/exercise5_static_%J.err
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 60

N=100

uv sync
mkdir -p miniproject/results/exercise5

# Time with increasing number of workers to measure speed-up
for W in 1 2 4 8 16; do
    echo "=== Workers: $W ==="
    time uv run python miniproject/exercise5.py $N $W \
        > miniproject/results/exercise5/output_w${W}.csv
done
