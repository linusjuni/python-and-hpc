#!/bin/bash
#BSUB -q hpc
#BSUB -W 15
#BSUB -J blosc
#BSUB -o blosc_%J.out
#BSUB -e blosc_%J.err
#BSUB -n 1
#BSUB -R "rusage[mem=4GB]"

uv sync
uv run exercises/week3/blosc.py 256
uv run exercises/week3/blosc.py 512
uv run exercises/week3/blosc.py 1024
