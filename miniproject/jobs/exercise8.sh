#!/bin/bash
#BSUB -o miniproject/jobs/exercise8_static_%J.out
#BSUB -e miniproject/jobs/exercise8_static_%J.err
#BSUB -q c02613
#BSUB -J exercise8_static
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model == XeonGold6126]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=4GB]"

N=20
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
python -u miniproject/exercise8.py $N
