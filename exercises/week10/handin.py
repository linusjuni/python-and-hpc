import sys
import numpy as np
from numba import cuda

TPB = 64

@cuda.jit
def reduce_kernel(data, out, n):
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    s = 1
    while s < cuda.blockDim.x:
        if tid % (2 * s) == 0 and i + s < n:
            data[i] += data[i + s]
        s *= 2
        cuda.syncthreads()

    if tid == 0:
        out[cuda.blockIdx.x] = data[i]

def get_grid(n, tpb):
    return (n + (tpb - 1)) // tpb

def reduce(x):
    n = len(x)
    bpg = get_grid(n, TPB)
    out = cuda.device_array(bpg, dtype=x.dtype)
    while bpg > 1:
        reduce_kernel[bpg, TPB](x, out, n)
        n = bpg
        bpg = get_grid(n, TPB)
        x[:n] = out[:n]
    reduce_kernel[bpg, TPB](x, out, n)
    return out

n = int(sys.argv[1])
data = np.random.rand(n).astype(np.float32)
d_data = cuda.to_device(data)
result = reduce(d_data)
print(result[0])
