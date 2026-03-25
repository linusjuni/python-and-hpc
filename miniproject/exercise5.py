"""
Task 5 — Static parallel scheduling over floorplans.
Each worker is assigned the same number of floorplans (static scheduling).
Usage: python simulate_static.py <N> [num_workers]
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
        # Compute average of left, right, up and down neighbors, see eq. (1)
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


def process_chunk(bids):
    """Process a static chunk of building IDs and return list of (bid, stats) tuples."""
    results = []
    for bid in bids:
        u0, interior_mask = load_data(bid)
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        stats = summary_stats(u, interior_mask)
        results.append((bid, stats))
    return results


if __name__ == '__main__':
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    N = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    num_workers = int(sys.argv[2]) if len(sys.argv) >= 3 else cpu_count()

    building_ids = building_ids[:N]

    # Static scheduling: split building_ids into num_workers equal-sized chunks
    chunks = [building_ids[i::num_workers] for i in range(num_workers)]
    # Remove empty chunks if N < num_workers
    chunks = [c for c in chunks if c]

    with Pool(processes=num_workers) as pool:
        chunk_results = pool.map(process_chunk, chunks)

    # Flatten results in original order (round-robin interleave → sort by building_ids index)
    flat = [item for chunk in chunk_results for item in chunk]
    order = {bid: idx for idx, bid in enumerate(building_ids)}
    flat.sort(key=lambda x: order[x[0]])

    # Print CSV
    print('building_id, ' + ', '.join(STAT_KEYS))
    for bid, stats in flat:
        print(f"{bid},", ", ".join(str(stats[k]) for k in STAT_KEYS))
