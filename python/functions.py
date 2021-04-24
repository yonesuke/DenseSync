import math

import numpy as np


def b(x):
    """eq. (A3)

    Parameters
    ----------
    x: numpy array (float)
    """
    return -np.cos(x) * (1 - np.cos(x))


def db(x):
    """db(x)/dx

    Parameters
    ----------
    x: numpy array (float)
    """
    return np.sin(x) - 2 * np.sin(x) * np.cos(x)


def t(x):
    """Right hand side of eq. (A4)

    Parameters
    ----------
    x: numpy array (float)
    """
    return 4 * np.pi * x - 4 * np.sin(2 * np.pi * x) + np.sin(4 * np.pi * x)


def critical_index(N):
    """Return an index that the sum is not exceeded when p=1 (Figure 2.)

    Parameters
    ----------
    N: int
      The number of oscillators
    
    Returns
    kc: int
      critical index
    ys: np.array(float)
      b(x) at each point obtained by dividing 0 to 2pi into N equal parts
    sk: np.array(float)
      accumulated array of b(x)
    """

    xs = np.array([2 * np.pi * l / N for l in range(1, N)])
    ys = b(xs)
    sk = np.cumsum(ys)
    kc = np.argmax(sk >= 0) + 1
    return kc, ys, sk


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
    kc, ys, sk = critical_index(nt)
    additional = 2 * math.ceil(-m * sk[kc - 2] / ys[kc - 1] - 1)
    return additional


def sup_m(N):
    """Computation of Eq. (39), a_{\widetilde{N}} / \widetilde{N}

    Parameters
    ----------
    N: int
      the number of oscillators
    """
    kc, ys, sk = critical_index(N)
    return (2 * kc - 1 - 2 * sk[kc - 2] / ys[kc - 1]) / N


def binary_search(f, xl, xr, eps=1e-8):
    """Implementation of binary search algorithm

    Parameters
    ----------
    f: Func
    xl: float
      left point of the search interval in the initial state
    xr: float
      right point of the search interval in the initial state
    eps: float
    """

    while (xr - xl) > eps:
        xm = (xl + xr) * 0.5
        if f(xm) > 0:
            xr = xm
        else:
            xl = xm
    return xl
   
