import numpy as np
from numba import jit
from time import perf_counter as time


def matmul(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(nopython=True)
def matmul_jit(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


X = np.random.rand(100, 100)
Y = np.random.rand(100, 100)

# Warmup: trigger JIT compilation before timing
matmul_jit(X, Y)

t = time()
matmul(X, Y)
t_original = time() - t

t = time()
matmul_jit(X, Y)
t_jit = time() - t

print(f"Original: {t_original:.4f}s")
print(f"JIT:      {t_jit:.4f}s")
print(f"Speedup:  {t_original / t_jit:.1f}x")
