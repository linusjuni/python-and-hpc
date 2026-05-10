#!/bin/bash
#BSUB -q c02613
#BSUB -J cuda_vector_addition
#BSUB -o exercises/week10/cuda_vector_addition_%J.out
#BSUB -e exercises/week10/cuda_vector_addition_%J.err
#BSUB -n 4
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=4GB] span[hosts=1]"
#BSUB -W 10

module load cuda

uv run exercises/week10/cuda_vector_addition.py
