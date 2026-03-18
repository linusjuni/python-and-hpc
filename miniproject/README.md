# Miniproject: Wall Heating

Simulate steady-state heat distribution across 4570 building floorplans using the Jacobi method, then optimise it.

## Structure

```
miniproject/
├── simulate.py             # reference implementation — verbatim from PDF, do not modify
├── exerciseX.py            # our exercises
├── jobs/
│   ├── exerciseX.sh        # our LSF batch job scripts
│   └── *.out / *.err       # job output — committed so results are shared (keep only relevant runs, delete the rest before committing)
├── results/                # output plots and CSVs
└── src/
    ├── data.py
    ├── jacobi.py
    ├── stats.py
    ├── visualization.py    
    └── utils/
        ├── settings.py
        └── logger.py
```

## Setup

All commands from the repo root:

```bash
uv sync
```

## Data

Located at `/dtu/projects/02613_2025/data/modified_swiss_dwellings/`. Each building has two files:
- `{bid}_domain.npy` — 512×512 grid with initial conditions (load bearing walls = 5°C, inside walls = 25°C, rooms = 0)
- `{bid}_interior.npy` — binary mask, 1 for interior (room) points that get updated each Jacobi iteration

Default path is set in `src/utils/settings.py` and can be overridden via a `.env` file.

## Loading data

```python
from src.data import load_building_ids, load_data

building_ids = load_building_ids()
u, interior_mask = load_data(building_ids[0])
```

## Running a job

```bash
bsub < miniproject/jobs/your_job.sh
```
