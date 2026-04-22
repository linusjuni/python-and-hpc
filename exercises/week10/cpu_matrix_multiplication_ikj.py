import numpy as np
from numba import jit
from time import perf_counter as time


@jit(nopython=True)
def matmul_ijk(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(nopython=True)
def matmul_ikj(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for k in range(A.shape[1]):
            for j in range(B.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


X = np.random.rand(100, 100)
Y = np.random.rand(100, 100)

# Warmup both
matmul_ijk(X, Y)
matmul_ikj(X, Y)

t = time()
matmul_ijk(X, Y)
t_ijk = time() - t

t = time()
matmul_ikj(X, Y)
t_ikj = time() - t

print(f"ijk (original): {t_ijk:.4f}s")
print(f"ikj (cache):    {t_ikj:.4f}s")
print(f"Speedup:        {t_ijk / t_ikj:.1f}x")
