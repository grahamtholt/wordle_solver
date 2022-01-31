import pandas as pd
import numpy as np
import time
from functools import wraps
from numba import njit

DEBUG = False


def timing(*args):
    def _timing(f):
        if debug:
            @wraps(f)
            def wrap(*args, **kw):
                ts = time.perf_counter()
                result = f(*args, **kw)
                te = time.perf_counter()
                print(f"{f.__name__} took {te-ts:2.4f} sec")
                return result
            return wrap
        else:
            return f
    if len(args) == 1 and callable(args[0]):
        # No optional argument to decorator
        debug = True
        return _timing(args[0])
    else:
        # Optional argument to decorator
        debug = args[0]
        return _timing


@timing(DEBUG)
@njit
def apply_count_values(arr, n_unique_vals=243):
    """Function equivalent to df.apply(pd.Series.count_values),
    but much, much faster.

    Probably only works as long as we already have the number of unique values
    and also integer values only.

    Args:
        arr: numpy array of a pandas dataframe
        n_unique_vals: the number of unique integer values in arr
    """
    counts = np.zeros((n_unique_vals, arr.shape[1]))
    for i in range(arr.shape[1]):
        for x in arr[:, i]:
            counts[x, i] = counts[x, i]+1
    return counts


@timing(DEBUG)
def get_entropies(data: pd.DataFrame):
    """
    Compute entropies for words in wide-format df
    """
    counts = pd.DataFrame(apply_count_values(
        data.to_numpy(copy=True)), columns=data.columns)
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


@timing(DEBUG)
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
    """Get the partition label for the mystery word given the guess.
    There are 3^n different partitions, where n is the number of characters in
    guess or mystery.

    Args:
        guess: word being guessed
        mystery: candidate for mystery word

    Returns:
        A base 10 integer based on the base 3 output digits of wordle.
        Considers a grey letter to be 0, a yellow letter to be 1, and a green
        letter to be 2.
    """
    output = []
    for i, char in enumerate(guess):
        if mystery[i] == char:
            output.append('2')
        elif mystery[i] != char and char in mystery:
            output.append('1')
        elif char not in mystery:
            output.append('0')
    return int(''.join(output), base=3)


def compute_known(guess, mystery):
    return np.base_repr(evaluate_guess(guess, mystery), 3).rjust(5, '0')
