#!/bin/bash
#BSUB -q hpc
#BSUB -J "job_array[1-10]"
#BSUB -o exercises/week11/job_array_%J_%I.out
#BSUB -e exercises/week11/job_array_%J_%I.err
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 1

echo "Job index: $LSB_JOBINDEX"
