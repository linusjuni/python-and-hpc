import numpy as np


def standardize_rows(data, mean, std):
    return np.array([[(row[j] - mean[j]) / std[j] for j in range(len(row))] for row in data])


if __name__ == "__main__":
    data = np.array([[1, 2, 3], [4, 5, 6]])
    mean = np.array([0.5, 1, 3])
    std = np.array([1, 2, 3])

    standardized_rows = standardize_rows(data=data, mean=mean, std=std)
    print(standardized_rows)
