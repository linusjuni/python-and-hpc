#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J sleepjob
#BSUB -o sleepjob_%J.out
#BSUB -e sleepjob_%J.err
#BSUB -B
#BSUB -N

/bin/sleep 180
