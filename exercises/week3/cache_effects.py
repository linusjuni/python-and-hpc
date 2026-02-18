import numpy as np
from time import perf_counter

SIZE = 100
N = 1000

mat = np.random.rand(SIZE, SIZE)

start = perf_counter()
for _ in range(N):
    double_column = 2 * mat[:, 0]
column_time = (perf_counter() - start) / N

start = perf_counter()
for _ in range(N):
    double_row = 2 * mat[0, :]
row_time = (perf_counter() - start) / N

print(f"Column: {column_time:.6f} s")
print(f"Row:    {row_time:.6f} s")

