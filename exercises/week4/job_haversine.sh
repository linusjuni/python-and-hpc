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
uv run -m exercises.week4.haversine input.csv
