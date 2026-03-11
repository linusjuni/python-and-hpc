#!/bin/bash
#BSUB -q hpc
#BSUB -n 24
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "span[hosts=1]"
#BSUB -W 30
#BSUB -J pi_speedup
#BSUB -o pi_speedup_%J.out
#BSUB -e pi_speedup_%J.err

uv sync
uv run python exercises/week5/pi/speedup.py
