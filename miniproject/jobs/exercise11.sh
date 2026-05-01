#!/bin/bash
#BSUB -o miniproject/jobs/exercise11_static_%J.out
#BSUB -e miniproject/jobs/exercise11_static_%J.err
#BSUB -q gpuv100
#BSUB -W 24:00
#BSUB -J exercise11_static

#BSUB -n 6
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=4GB]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
python -u miniproject/exercise11.py 