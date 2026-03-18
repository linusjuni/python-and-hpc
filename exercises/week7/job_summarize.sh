#!/bin/bash
#BSUB -q hpc
#BSUB -J summarize
#BSUB -o exercises/week7/summarize_%J.out
#BSUB -e exercises/week7/summarize_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 10

uv sync
uv run python exercises/week7/summarize.py
