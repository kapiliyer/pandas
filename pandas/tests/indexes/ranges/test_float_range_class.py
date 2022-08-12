# length tests
import numpy as np


def b(i, j, k):
    estimate = (j - i) // k
    if not np.isclose(i + estimate * k, j):
        estimate += 1
    return int(estimate)


steps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
starts = [1.0, 1.3, 1.7, 2.0, 2.1, 2.6, 2.9]
for step in steps:
    step = -step
    for i in range(len(starts)):
        for j in range(i + 1, len(starts)):
            print((starts[j], starts[i], step), b(starts[j], starts[i], step))
