import math

import numpy as np


def b(x):
    """eq. (A3)

    Parameters
    ----------
    x: numpy array (float)
    """
    return -np.cos(x) * (1 - np.cos(x))


def t(x):
    """eq. (A2)

    Parameters
    ----------
    x: numpy array (float)
    """
    return 4 * np.pi * x - 4 * np.sin(2 * np.pi * x) + np.sin(4 * np.pi * x)


def critical_index(N):
    """
    Parameters
    ----------
    N: int
      The number of oscillators
    """

    xs = np.array([2 * np.pi * l / N for l in range(1, N)])
    ys = b(xs)
    sk = np.cumsum(ys)
    kc = np.argmax(sk >= 0) + 1
    return kc


def additional_one(N, p):
    """
    Parameters
    ----------
    N: int
      The number of oscillators
    p: int
      p-twisted state
    """

    m = math.gcd(N, p)
    nt, pt = int(N / m), int(p / m)
    xs = np.array([2 * np.pi * l / nt for l in range(1, nt)])
    ys = b(xs)
    sk = np.cumsum(ys)
    kc = np.argmax(sk >= 0) + 1
    additional = 2 * math.ceil(-m * sk[kc - 2] / ys[kc - 1] - 1)
    return additional
