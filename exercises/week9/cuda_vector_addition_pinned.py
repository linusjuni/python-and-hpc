import numpy as np
from numba import cuda
from time import perf_counter as time


@cuda.jit
def add_kernel(x, y, a):
    i = cuda.grid(1)
    if i < x.shape[0]:
        a[i] = x[i] + y[i]


N = 1_000_000
threads_per_block = 256
blocks = (N + threads_per_block - 1) // threads_per_block


def run(x, y):
    a = np.empty(N, dtype=np.float32)

    x_dev = cuda.to_device(x)
    y_dev = cuda.to_device(y)
    a_dev = cuda.device_array(N, dtype=np.float32)

    # Warmup
    add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
    cuda.synchronize()

    t = time()
    x_dev = cuda.to_device(x)
    y_dev = cuda.to_device(y)
    add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
    cuda.synchronize()
    a_dev.copy_to_host(a)
    elapsed = time() - t

    return elapsed, a


# Regular memory
x = np.random.rand(N).astype(np.float32)
y = np.random.rand(N).astype(np.float32)
t_regular, a_regular = run(x, y)

# Pinned memory
x_pinned = cuda.pinned_array_like(x)
y_pinned = cuda.pinned_array_like(y)
x_pinned[:] = x
y_pinned[:] = y
t_pinned, a_pinned = run(x_pinned, y_pinned)

print(f"Regular: {t_regular:.6f}s")
print(f"Pinned:  {t_pinned:.6f}s")
print(f"Speedup: {t_regular / t_pinned:.2f}x")
print(f"Correct: {np.allclose(a_regular, a_pinned)}")
