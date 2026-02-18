import os
import sys

import blosc
import numpy as np
from time import perf_counter


class Timer:
    def __enter__(self):
        self._start = perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = perf_counter() - self._start


def write_numpy(arr, file_name):
    np.save(f"{file_name}.npy", arr)
    os.sync()


def write_blosc(arr, file_name, cname="lz4"):
    b_arr = blosc.pack_array(arr, cname=cname)
    with open(f"{file_name}.bl", "wb") as w:
        w.write(b_arr)
    os.sync()


def read_numpy(file_name):
    return np.load(f"{file_name}.npy")


def read_blosc(file_name):
    with open(f"{file_name}.bl", "rb") as r:
        b_arr = r.read()
    return blosc.unpack_array(b_arr)


def benchmark(arr, label, file_name):
    with Timer() as t:
        write_numpy(arr, file_name)
    t_wn = t.elapsed

    with Timer() as t:
        write_blosc(arr, file_name)
    t_wb = t.elapsed

    with Timer() as t:
        read_numpy(file_name)
    t_rn = t.elapsed

    with Timer() as t:
        read_blosc(file_name)
    t_rb = t.elapsed

    npy_mb = os.path.getsize(f"{file_name}.npy") / 1024**2
    bl_mb = os.path.getsize(f"{file_name}.bl") / 1024**2

    print(f"{label}: {t_wn:.4f} {t_wb:.4f} {t_rn:.4f} {t_rb:.4f} | npy={npy_mb:.2f}MB bl={bl_mb:.2f}MB")


if __name__ == "__main__":
    n = int(sys.argv[1])
    print(f"n={n}  [write_numpy write_blosc read_numpy read_blosc | file sizes]")

    zeros = np.zeros((n, n, n), dtype='uint8')
    benchmark(zeros, "zeros ", "tmp_array")

    tiled = np.tile(
        np.arange(256, dtype='uint8'),
        (n // 256) * n * n,
    ).reshape(n, n, n)
    benchmark(tiled, "tiled ", "tmp_array")

    random = np.random.randint(0, 256, size=(n, n, n), dtype='uint8')
    benchmark(random, "random", "tmp_array")
