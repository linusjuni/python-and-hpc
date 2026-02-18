#!/bin/bash
#BSUB -q hpc
#BSUB -W 5
#BSUB -J cache_effects
#BSUB -o cache_effects_%J.out
#BSUB -e cache_effects_%J.err
#BSUB -n 1
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=1GB]"

cd ~/projects/python-and-hpc
uv sync
uv run exercises/week3/cache_effects.py
