import numpy as np
from pathlib import Path
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


def get_cache_sizes_kb():
    caches = {}
    cache_dir = Path('/sys/devices/system/cpu/cpu0/cache')
    for index in sorted(cache_dir.glob('index*')):
        level = (index / 'level').read_text().strip()
        cache_type = (index / 'type').read_text().strip()
        size_str = (index / 'size').read_text().strip()
        if cache_type == 'Instruction':
            continue
        size_kb = int(size_str[:-1]) * (1024 if size_str[-1] == 'M' else 1)
        name = f'L{level}' + ('' if cache_type == 'Unified' else 'd')
        caches[name] = size_kb
    return caches


N = 100
SIZES = np.logspace(2, 8, num=20).astype(int)
results = []

for size in SIZES:
    mat = np.random.rand(1, size)
    vector_kb = size * 8 / 1024

    with Timer() as t:
        for _ in range(N):
            2 * mat
    mflops = size * N / t.elapsed / 1e6

    results.append((vector_kb, mflops))

vector_kbs = [r[0] for r in results]
mflops = [r[1] for r in results]

print(f"{'Vector (KB)':>12}  {'MFLOP/s':>10}")
for kb, mfl in results:
    print(f"{kb:>12.1f}  {mfl:>10.1f}")

cache_sizes = get_cache_sizes_kb()
print("\nCache sizes:", cache_sizes)

fig, ax = plt.subplots(figsize=(10, 6))
ax.loglog(vector_kbs, mflops, 'o-', label='2 * mat')

cache_colors = {'L1d': 'green', 'L2': 'orange', 'L3': 'red'}
for name, size_kb in cache_sizes.items():
    color = cache_colors.get(name, 'gray')
    ax.axvline(size_kb, color=color, linestyle='--', alpha=0.7, label=f'{name} ({size_kb:.0f} KB)')

ax.set_xlabel('Vector size (KB)')
ax.set_ylabel('Performance (MFLOP/s)')
ax.set_title('Cache effects: row vector doubling')
ax.legend()
ax.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig('exercises/week3/cache_effects_2.png', dpi=150)
print("Plot saved to exercises/week3/cache_effects_2.png")
