#!/bin/bash
#BSUB -q hpc
#BSUB -W 15
#BSUB -J bloscing
#BSUB -o bloscing_%J.out
#BSUB -e bloscing_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=8GB]"

uv sync
uv run exercises/week3/bloscing.py 256
uv run exercises/week3/bloscing.py 512
uv run exercises/week3/bloscing.py 1024
