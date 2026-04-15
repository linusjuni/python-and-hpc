"""
Task 6 — Dynamic parallel scheduling over floorplans.
Each worker picks up one floorplan at a time from a shared queue (dynamic scheduling).
Usage: python exercise6.py <N> [num_workers]
"""

from os.path import join
import sys

import numpy as np
from multiprocessing import Pool, cpu_count


LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
MAX_ITER = 20_000
ABS_TOL = 1e-4
STAT_KEYS = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']


def load_data(bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(LOAD_DIR, f"{bid}_domain.npy"))
    interior_mask = np.load(join(LOAD_DIR, f"{bid}_interior.npy"))
    return u, interior_mask


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }


def process_single(bid):
    """Process one building and return (bid, stats). Dynamic: one task per building."""
    u0, interior_mask = load_data(bid)
    u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
    stats = summary_stats(u, interior_mask)
    return bid, stats


if __name__ == '__main__':
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    N = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    num_workers = int(sys.argv[2]) if len(sys.argv) >= 3 else cpu_count()

    building_ids = building_ids[:N]

    # Dynamic scheduling: chunksize=1 means each worker fetches one building at a time.
    # Workers with shorter floorplans finish faster and pick up the next task immediately,
    # avoiding the load imbalance that static chunking causes when iteration counts vary.
    with Pool(processes=num_workers) as pool:
        results = list(pool.imap_unordered(process_single, building_ids, chunksize=1))

    # Sort back to original order for reproducible CSV output
    order = {bid: idx for idx, bid in enumerate(building_ids)}
    results.sort(key=lambda x: order[x[0]])

    print('building_id, ' + ', '.join(STAT_KEYS))
    for bid, stats in results:
        print(f"{bid},", ", ".join(str(stats[k]) for k in STAT_KEYS))
