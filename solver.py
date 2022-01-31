import pandas as pd
import numpy as np
import time
from functools import wraps
from numba import njit


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.perf_counter()
        result = f(*args, **kw)
        te = time.perf_counter()
        print(f"{f.__name__} took {te-ts:2.4f} sec")
        return result
    return wrap


@timing
@njit
def get_counts(arr):
    counts = np.empty((243, arr.shape[1]))
    for i in range(arr.shape[1]):
        for x in arr[:, i]:
            counts[x, i] = counts[x, i]+1
    return counts


@timing
def get_entropies(data: pd.DataFrame):
    """
    Compute entropies for words in wide-format df
    """
    counts = pd.DataFrame(get_counts(data.to_numpy()), columns=data.columns)
    probs = (counts / counts.sum(axis=0)).replace(0, np.nan)
    nplogp = -probs * np.log2(probs)
    return nplogp.sum()


def get_optimal_guess(data: pd.DataFrame, obs: list = []):
    """Get the optimal guess given previous observations.

    Args:
        data: a DataFrame containing all possible function outputs
        obs: a list of observed guess, value pairs

    Returns:
        The word that maximizes the partition entropy over the remaining
        possible hidden words
        The partition entropy of the returned word
    """
    if obs:
        entropies = get_entropies(get_partition(data, obs))
    else:
        entropies = get_entropies(data)
    return entropies.idxmax(), entropies.max()


@timing
def get_partition(data: pd.DataFrame, obs: list):
    """Get the possible partition of hidden words given previous observations

    Args:
        data: a DataFrame containing all possible function outputs
        obs: a list of observed guess, value pairs

    Returns:
        A subframe of <data> that represents all hidden words consistent with
        the observations.
    """
    indexer = pd.DataFrame([data[o[0]] == o[1] for o in obs]).all()
    return data[indexer]


def evaluate_guess(guess: str, mystery: str):
    output = []
    for i, char in enumerate(guess):
        if mystery[i] == char:
            output.append('2')
        elif mystery[i] != char and char in mystery:
            output.append('1')
        elif char not in mystery:
            output.append('0')
    return int(''.join(output), base=3)
