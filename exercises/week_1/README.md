# LSF Job Script Cheatsheet

## Basic Options
```bash
#BSUB -q hpc              # Queue name
#BSUB -W 2                # Walltime (minutes)
#BSUB -J jobname          # Job name
#BSUB -o output_%J.out    # Output file (%J = job ID)
#BSUB -e output_%J.err    # Error file
```

## Notifications
```bash
#BSUB -B                  # Email when job begins
#BSUB -N                  # Email with job report when job finishes
```

## Request Specific CPU Type
```bash
#BSUB -R "select[model == XeonE5_2660v3]"
```
Check available types: `nodestat -F`

**Note:** LSF uses underscore (`XeonE5_2660v3`), env vars use hyphen (`$CPUTYPEV` = `XeonE5-2660v3`)

## Commands
```bash
bsub < script.sh          # Submit job
bstat                     # Check job status
bjobs -l <jobid>          # Detailed job info (shows walltime limit)
nodestat -F               # Show nodes with CPU types and features
```
