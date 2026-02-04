#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J myjob
#BSUB -o myjob_%J.out
#BSUB -e myjob_%J.err

/bin/sleep 60