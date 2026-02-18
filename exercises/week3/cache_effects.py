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
        size_str = (index / 'size').read_text().strip()  # e.g. "32K" or "1024K"
        if cache_type == 'Instruction':
            continue
        size_kb = int(size_str[:-1]) * (1024 if size_str[-1] == 'M' else 1)
        name = f'L{level}' + ('' if cache_type == 'Unified' else 'd')
        caches[name] = size_kb
    return caches


N = 100000
SIZES = np.logspace(1, 4.5, num=20).astype(int)
results = []

for size in SIZES:
    mat = np.random.rand(size, size)
    matrix_kb = size * size * 8 / 1024

    with Timer() as t:
        for _ in range(N):
            2 * mat[:, 0]
    column_mflops = size * N / t.elapsed / 1e6

    with Timer() as t:
        for _ in range(N):
            2 * mat[0, :]
    row_mflops = size * N / t.elapsed / 1e6

    results.append((matrix_kb, column_mflops, row_mflops))

matrix_kbs = [r[0] for r in results]
column_mflops = [r[1] for r in results]
row_mflops = [r[2] for r in results]

print(f"{'Matrix (KB)':>12}  {'Column (MFLOP/s)':>16}  {'Row (MFLOP/s)':>14}")
for kb, col, row in results:
    print(f"{kb:>12.1f}  {col:>16.1f}  {row:>14.1f}")

cache_sizes = get_cache_sizes_kb()
print("\nCache sizes:", cache_sizes)

fig, ax = plt.subplots(figsize=(10, 6))
ax.loglog(matrix_kbs, column_mflops, 'o-', label='Column (2 * mat[:, 0])')
ax.loglog(matrix_kbs, row_mflops, 's-', label='Row (2 * mat[0, :])')

cache_colors = {'L1d': 'green', 'L2': 'orange', 'L3': 'red'}
for name, size_kb in cache_sizes.items():
    color = cache_colors.get(name, 'gray')
    ax.axvline(size_kb, color=color, linestyle='--', alpha=0.7, label=f'{name} ({size_kb:.0f} KB)')

ax.set_xlabel('Matrix size (KB)')
ax.set_ylabel('Performance (MFLOP/s)')
ax.set_title('Cache effects: row vs column access')
ax.legend()
ax.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig('exercises/week3/cache_effects.png', dpi=150)
print("Plot saved to exercises/week3/cache_effects.png")
