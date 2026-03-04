#!/bin/bash
#BSUB -q hpc
#BSUB -n 10
#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "span[hosts=1]"
#BSUB -W 30
#BSUB -J pi
#BSUB -o pi_%J.out
#BSUB -e pi_%J.err

uv sync

echo "=== fully_serial.py ==="
time uv run python exercises/week5/pi/fully_serial.py

echo "=== fully_parallel.py ==="
time uv run python exercises/week5/pi/fully_parallel.py

echo "=== chunked_parallel.py ==="
time uv run python exercises/week5/pi/chunked_parallel.py
