#!/bin/bash
#BSUB -q hpc
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 30
#BSUB -J haversine
#BSUB -o haversine_%J.out
#BSUB -e haversine_%J.err

uv sync
uv run python -m cProfile -o profile.prof exercises/week4/haversine.py input.csv
uv run python -c "
import pstats
p = pstats.Stats('profile.prof')
p.sort_stats('cumulative')
p.print_stats(20)
"
