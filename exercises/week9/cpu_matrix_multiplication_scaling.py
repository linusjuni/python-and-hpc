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


# Warmup
X = np.random.rand(10, 10)
matmul_ijk(X, X)
matmul_ikj(X, X)

sizes = [200, 400, 600, 800, 1000]

print(f"{'N':>6}  {'ijk (s)':>10}  {'ikj (s)':>10}  {'speedup':>8}")
for N in sizes:
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    t = time()
    matmul_ijk(A, B)
    t_ijk = time() - t

    t = time()
    matmul_ikj(A, B)
    t_ikj = time() - t

    print(f"{N:>6}  {t_ijk:>10.3f}  {t_ikj:>10.3f}  {t_ijk/t_ikj:>8.1f}x")
