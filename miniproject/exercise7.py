import numpy as np
from numba import jit
from simulate import load_data, summary_stats
import sys
from os.path import join

@jit(nopython=True)
def jacobi_numba(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)
    u_new = np.copy(u)
    for i in range(max_iter):
        delta = 0.0
        # iterating over the region u[1:-1, 1:-1]
        for row in range(1, u.shape[0] - 1): 
            for col in range(1, u.shape[1] - 1):
                if interior_mask[row-1, col-1]: # interior_mask is two rows and columns smaller than u
                    val = 0.25 * (u[row, col-1] + u[row, col+1] + u[row-1, col] + u[row+1, col])
                    if abs(u[row, col] - val) > delta:
                        delta = abs(u[row, col] - val)
                    u_new[row, col] = val
        if delta < atol:
            break
        u, u_new = u_new, u
    return u

# copied from simulate.py, but with jacobi replaced by jacobi_numba
if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_numba(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
