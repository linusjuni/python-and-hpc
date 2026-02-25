import numpy as np

def outer(v, u):
    result = []
    for i in range(len(v)):
        row = []
        for j in range(len(u)):
            row.append(v[i] * u[j])
        result.append(row)
    return np.array(result)