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

# Transfer to GPU once, outside timing
x_dev = cuda.to_device(x)
y_dev = cuda.to_device(y)
a_dev = cuda.device_array(N, dtype=np.float32)

# Warmup
add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
cuda.synchronize()

# Time kernel only (data already on GPU)
t = time()
add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
cuda.synchronize()
t_kernel = time() - t

# Time full pipeline (transfer + kernel + transfer back)
t = time()
x_dev = cuda.to_device(x)
y_dev = cuda.to_device(y)
add_kernel[blocks, threads_per_block](x_dev, y_dev, a_dev)
cuda.synchronize()
a_dev.copy_to_host(x)  # reuse x buffer
t_full = time() - t

print(f"Kernel only (data on GPU): {t_kernel:.6f}s")
print(f"Full pipeline (w/ transfer): {t_full:.6f}s")
print(f"Transfer time: {t_full - t_kernel:.6f}s")
print(f"Transfer is {(t_full - t_kernel) / t_full * 100:.1f}% of total time")
