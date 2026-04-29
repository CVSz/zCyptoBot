import numpy as np


def ks_stat(x, y):
    x = np.sort(x)
    y = np.sort(y)
    nx, ny = len(x), len(y)
    i = j = 0
    cdf_x = cdf_y = 0.0
    d = 0.0
    while i < nx and j < ny:
        if x[i] <= y[j]:
            i += 1
            cdf_x = i / nx
        else:
            j += 1
            cdf_y = j / ny
        d = max(d, abs(cdf_x - cdf_y))
    return d


class DriftMonitor:
    def __init__(self, threshold: float = 0.2):
        self.th = threshold

    def drifted(self, recent, baseline):
        if len(recent) < 30 or len(baseline) < 30:
            return False, 0.0
        d = ks_stat(np.array(recent), np.array(baseline))
        return d > self.th, d
