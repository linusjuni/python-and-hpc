#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J 64core_job
#BSUB -o 64core_%J.out
#BSUB -e 64core_%J.err
#BSUB -n 64
#BSUB -R "span[hosts=1]"

# -n 64: Request 64 cores
# -R "span[hosts=1]": All cores on the same node

echo "Running on host: $(hostname)"
echo "Number of cores allocated: $LSB_DJOB_NUMPROC"
echo "CPU Type: $CPUTYPEV"

/bin/sleep 60
