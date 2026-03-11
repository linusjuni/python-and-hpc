#!/bin/bash
#BSUB -q hpc
#BSUB -J "celeba_numa[1-5]"
#BSUB -o exercises/week6/celeba/celeba_numa_%J_%I.out
#BSUB -e exercises/week6/celeba/celeba_numa_%J_%I.err
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8GB]"
#BSUB -W 30

DATA=/dtu/projects/02613_2025/data/celeba/celeba_100K.npy
N_PROCESSES_LIST=(1 2 4 8 16)
N_PROCESSES=${N_PROCESSES_LIST[$LSB_JOBINDEX - 1]}

uv sync
echo "n_processes=$N_PROCESSES"
for i in 1 2 3; do
    numactl --interleave=all uv run python exercises/week6/celeba/celeba.py $DATA $N_PROCESSES
done
