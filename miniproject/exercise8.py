from os.path import join
import sys
from numba import cuda
import numpy as np


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


@cuda.jit
def jacobi_step(u, u_new, interior_mask):
    j, i = cuda.grid(2)

    if interior_mask[i, j]:
        u_new[i, j] = 0.25 * (
            u[i, j-1] +   
            u[i, j+1] +   
            u[i-1, j] +   
            u[i+1, j]     
        )
    else:
        u_new[i, j] = u[i, j]

def get_bpg(n, tpb):
    return (n+ (tpb - 1)) // tpb

def jacobi_cuda(u, interior_mask, max_iter, atol=1e-6):
    u_device = cuda.to_device(u)
    u_new_device = cuda.device_array_like(u)
    mask_device = cuda.to_device(interior_mask)

    tpb = (16, 16)

    bpg = (
        get_bpg(u.shape[0], tpb[0]),
        get_bpg(u.shape[1], tpb[1]),
    )

    for _ in range(max_iter):
        jacobi_step[bpg, tpb](u_device, u_new_device, mask_device)
        u_device, u_new_device = u_new_device, u_device

    return u_device.copy_to_host()


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

    import time
    
    start = time.time()
    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        print(f"Processing building {building_ids[i]} ({i+1}/{N})...")
        u = jacobi_cuda(u0, interior_mask, MAX_ITER, ABS_TOL)
        print(f"Finished building {building_ids[i]}.")
        print(u[1:-1, 1:-1][interior_mask].mean())  # Print mean temperature for debugging
        all_u[i] = u
    gpu_time = time.time() - start
    print(f"GPU Jacobi time for {N} buildings: {gpu_time:.2f} seconds")

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
