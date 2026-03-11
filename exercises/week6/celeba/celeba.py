import ctypes
import glob
import multiprocessing as mp
import re
import sys
from time import perf_counter as time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def init(shared_arr_):
    global shared_arr
    shared_arr = shared_arr_


def tonumpyarray(mp_arr):
    return np.frombuffer(mp_arr, dtype='float32')


def reduce_step(args):
    b, e, s, elemshape = args
    arr = tonumpyarray(shared_arr).reshape((-1,) + elemshape)
    if b + s < len(arr):
        arr[b] += arr[b + s]


def plot_speedup(out_glob):
    results = {}
    for path in glob.glob(out_glob):
        with open(path) as f:
            content = f.read()
        m = re.search(r'n_processes=(\d+)', content)
        if not m:
            continue
        n = int(m.group(1))
        times = [float(x) for x in re.findall(r'^(\d+\.\d+)$', content, re.MULTILINE)]
        if times:
            results[n] = times

    processes = sorted(results)
    avg_times = [np.mean(results[p]) for p in processes]
    baseline  = avg_times[0]
    speedups  = [baseline / t for t in avg_times]

    print(f"{'processes':>10}  {'avg time (s)':>12}  {'speedup':>8}")
    for p, t, s in zip(processes, avg_times, speedups):
        print(f"{p:>10}  {t:>12.3f}  {s:>8.2f}x")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.plot(processes, avg_times, 'o-')
    ax1.set_xlabel('Number of processes')
    ax1.set_ylabel('Time (s)')
    ax1.set_title('Runtime vs processes')
    ax1.set_xticks(processes)
    ax2.plot(processes, speedups, 'o-', label='Measured')
    ax2.plot(processes, processes, 'k--', label='Ideal')
    ax2.set_xlabel('Number of processes')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup vs processes')
    ax2.set_xticks(processes)
    ax2.legend()
    plt.tight_layout()
    plt.savefig('exercises/week6/celeba/speedup.png', dpi=150)
    print("Saved speedup.png")


if __name__ == '__main__':
    if sys.argv[1] == 'plot':
        plot_speedup(sys.argv[2])
        sys.exit(0)

    n_processes = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    chunksize   = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    # Create shared array
    data = np.load(sys.argv[1])
    n = len(data)
    elemshape = data.shape[1:]
    shared_arr = mp.RawArray(ctypes.c_float, data.size)
    arr = tonumpyarray(shared_arr).reshape(data.shape)
    np.copyto(arr, data)
    del data

    # Run full parallel reduction
    t = time()
    pool = mp.Pool(n_processes, initializer=init, initargs=(shared_arr,))
    stride = 1
    while stride < n:
        stride *= 2
        pool.map(reduce_step,
                 [(i, i + stride, stride // 2, elemshape) for i in range(0, n, stride)],
                 chunksize=chunksize)

    print(time() - t)
    final_image = arr[0]
    final_image /= n
    Image.fromarray(
        (255 * final_image.astype(float)).astype('uint8')
    ).save('result.png')