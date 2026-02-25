#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J bigcore_job
#BSUB -o bigcore_%J.out
#BSUB -e bigcore_%J.err
#BSUB -n 16
#BSUB -R "span[hosts=1]"

# -n 16: Request 16 cores
# -R "span[hosts=1]": All cores on the same node

echo "Running on host: $(hostname)"
echo "Number of cores allocated: $LSB_DJOB_NUMPROC"

/bin/sleep 60
