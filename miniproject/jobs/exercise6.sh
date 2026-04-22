#!/bin/bash
#BSUB -q hpc
#BSUB -J exercise6_dynamic
#BSUB -o miniproject/jobs/exercise6_dynamic_%J.out
#BSUB -e miniproject/jobs/exercise6_dynamic_%J.err
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 60

N=100

uv sync
mkdir -p miniproject/results/exercise6

# Time with increasing number of workers to measure speed-up
for W in 1 2 4 8 16; do
    echo "=== Workers: $W ==="
    time uv run python miniproject/exercise6.py $N $W \
        > miniproject/results/exercise6/output_w${W}.csv
done
