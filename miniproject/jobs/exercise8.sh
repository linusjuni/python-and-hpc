#!/bin/bash
#BSUB -o miniproject/jobs/exercise8_static_%J.out
#BSUB -e miniproject/jobs/exercise8_static_%J.err
#BSUB -q gpuv100
#BSUB -J exercise8_static
#BSUB -W 24:00
#BSUB -n 4
#BSUB -R "rusage[mem=4GB]"
#BSUB -gpu "num=1:mode=exclusive_process"

N=20
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
python -u miniproject/exercise8.py $N
