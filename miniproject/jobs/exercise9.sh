#!/bin/bash
#BSUB -q c02613
#BSUB -J exercise9
#BSUB -o miniproject/jobs/exercise9_%J.out
#BSUB -e miniproject/jobs/exercise9_%J.err
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=4GB]"
#BSUB -W 30

N=20

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python miniproject/exercise9.py $N > miniproject/results/exercise9/output.csv