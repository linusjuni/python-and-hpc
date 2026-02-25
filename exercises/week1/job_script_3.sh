#!/bin/bash
#BSUB -q hpc
#BSUB -W 2
#BSUB -J cputype_job
#BSUB -o cputype_%J.out
#BSUB -e cputype_%J.err
#BSUB -R "select[model == XeonE5_2660v3]"

echo "Running on host: $(hostname)"

echo "CPU Model from lscpu:"
lscpu | grep "Model name"

echo ""
echo "Environment variables with 'model' or 'type':"
env | grep -iE "model|type"

/bin/sleep 60
