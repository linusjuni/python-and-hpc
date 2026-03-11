import random
import multiprocessing
from time import perf_counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Timer:
    def __enter__(self):
        self._start = perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = perf_counter() - self._start


def plot_speedup(n_procs, speedups):
    _, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_procs, speedups, 'o-', label='Measured speedup')
    ax.plot(n_procs, n_procs, '--', color='gray', label='Ideal (linear) speedup')
    ax.set_xlabel('Number of processes')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup of chunked parallel Monte Carlo π estimation')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('exercises/week5/pi/speedup.png', dpi=150)
    print("Plot saved to exercises/week5/pi/speedup.png")


def sample_multiple(samples_partial):
    hits = 0
    for _ in range(samples_partial):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        if x**2 + y**2 <= 1:
            hits += 1
    return hits


if __name__ == '__main__':
    samples = 1_000_000
    max_procs = multiprocessing.cpu_count()
    n_procs = list(range(1, max_procs + 1))
    print(f"Running with up to {max_procs} processes...")

    times = []
    for n_proc in n_procs:
        chunk_size = samples // n_proc
        with Timer() as t:
            pool = multiprocessing.Pool(n_proc)
            results = [pool.apply_async(sample_multiple, (chunk_size,)) for _ in range(n_proc)]
            hits = sum(r.get() for r in results)
            pool.close()
            pool.join()
        times.append(t.elapsed)
        print(f"n_proc={n_proc:2d}  time={t.elapsed:.3f}s  pi≈{4.0*hits/samples:.5f}")

    baseline = times[0]
    speedups = [baseline / t for t in times]

    plot_speedup(n_procs, speedups)
