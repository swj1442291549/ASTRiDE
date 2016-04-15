import numpy as np


def moving_average(data, window_size=5):
    """
    Moving average.

    Parameters
    ----------
    data : (N,) array_like
        An array of values.
    window_size : int
        Moving average window size.

    Returns
    -------
    out : (N,) array_like
        Moving averaged array.
    """
    window = np.ones(int(window_size))/float(window_size)
    results = np.convolve(data, window, 'valid')

    return results