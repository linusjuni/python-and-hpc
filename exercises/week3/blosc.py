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


if __name__ == "__main__":
    n = int(sys.argv[1])
    arr = np.zeros((n, n, n), dtype='uint8')

    with Timer() as t:
        write_numpy(arr, "tmp_array")
    print(t.elapsed)

    with Timer() as t:
        write_blosc(arr, "tmp_array")
    print(t.elapsed)

    with Timer() as t:
        read_numpy("tmp_array")
    print(t.elapsed)

    with Timer() as t:
        read_blosc("tmp_array")
    print(t.elapsed)
