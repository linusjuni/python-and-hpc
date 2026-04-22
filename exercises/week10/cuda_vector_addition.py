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

x = np.random.rand(N).astype(np.float32)
y = np.random.rand(N).astype(np.float32)

x_dev = cuda.to_device(x)
y_dev = cuda.to_device(y)
a_dev = cuda.device_array(N, dtype=np.float32)

t = time()
add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
cuda.synchronize()
t_warmup = time() - t

t = time()
add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
cuda.synchronize()
elapsed = time() - t

a = a_dev.copy_to_host()

print(f"Warmup: {t_warmup:.6f}s")
print(f"Time:   {elapsed:.6f}s")
print(f"Correct: {np.allclose(a, x + y)}")
