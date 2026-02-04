#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J multicore_job
#BSUB -o multicore_%J.out
#BSUB -e multicore_%J.err
#BSUB -n 4
#BSUB -R "span[hosts=1]"

# -n 4: Request 4 cores
# -R "span[hosts=1]": All cores on the same node

echo "Running on host: $(hostname)"
echo "Number of cores allocated: $LSB_DJOB_NUMPROC"

/bin/sleep 30

echo "Done sleeping."
