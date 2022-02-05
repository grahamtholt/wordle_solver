import pandas as pd
import time
import multiprocessing
from random import randint
import numpy as np
import argparse
import importlib.resources as pkg_resources
from functools import partial
from math import floor

from wordler.utils import solver, precompute_data
from wordler import resources

FIRST_GUESS = "soare"
CORRECT = 242

print("Reading precomputed data...")
try:
    with pkg_resources.path(resources, "data.parquet") as pq:
        DATA = pd.read_parquet(pq)
except FileNotFoundError:
    print("Cached result not found, calculating colorings...")
    DATA = precompute_data.run()
try:
    with pkg_resources.open_text(resources, 'mystery_words.txt') as fi:
        HIDDEN_WORDS = [line.strip() for line in fi.readlines()]
except FileNotFoundError:
    print("Error: Hidden-word list not found. Exiting...")
    exit()

SOLS = DATA.shape[0]


def find_wordle(mystery, randomize=False, max_guesses=6):
    start = time.perf_counter()
    counter = 0
    observations = []
    guesses = []
    guess_entropies = []
    sol_size = SOLS
    sizes = [SOLS]
    gotitright = False
    while sol_size > 2 and counter < max_guesses:
        # Generate guess based on internal state
        guess, entropy = solver.get_optimal_guess(DATA, observations)
        counter = counter + 1
        guesses.append(guess)
        guess_entropies.append(entropy)
        observations.append((guess, solver.evaluate_guess(guess, mystery)))
        partition = list(solver.get_partition(DATA, observations).index)
        sol_size = len(partition)
        sizes.append(sol_size)

    # Down to two or one words
    if sol_size == 2:
        counter = counter + 1
        if randomize:
            choice = randint(0, 1)
        else:
            choice = 0
        guess = partition[choice]
        guesses.append(guess)
        guess_entropies.append(np.nan)
        val = solver.evaluate_guess(guess, mystery)
        observations.append((guess, val))
        if val == CORRECT:
            gotitright = True
            sizes.append(0)
        else:
            sizes.append(1)
            counter = counter + 1
            guess = partition[1-choice]
            guesses.append(guess)
            guess_entropies.append(np.nan)
            val = solver.evaluate_guess(guess, mystery)
            observations.append((guess, val))
            if val == CORRECT:
                sizes.append(0)
                gotitright = True

    elif sol_size == 1:
        counter = counter + 1
        guess = partition[0]
        guesses.append(guess)
        guess_entropies.append(np.nan)
        val = solver.evaluate_guess(guess, mystery)
        observations.append((guess, val))
        if val == CORRECT:
            gotitright = True

    end = time.perf_counter()
    runtime = end-start

    guesses = pad(guesses)
    guess_entropies = pad(guess_entropies)
    values = pad([t[1] for t in observations])

    stats = {}
    stats["hidden_word"] = mystery
    stats["runtime_s"] = runtime
    stats["num_guesses"] = counter
    stats["correct"] = gotitright
    for i, g in enumerate(guesses):
        stats[f"guess_{i}"] = g
    for i, e in enumerate(guess_entropies):
        stats[f"entropy_{i}"] = e
    for i, v in enumerate(values):
        stats[f"partition_label_{i}"] = v
    return stats


def pad(x: list, list_len=6):
    return x + [np.nan] * (list_len - len(x))


def main(args):
    pool = multiprocessing.Pool(floor(0.5*multiprocessing.cpu_count()))
    allstart = time.perf_counter()

    wordle_withargs = partial(find_wordle,
                              randomize=args.randomize,
                              max_guesses=args.max_guesses,
                              )
    stats = pool.map(wordle_withargs, HIDDEN_WORDS)
    #stats = [wordle_withargs(word) for word in HIDDEN_WORDS]

    allstop = time.perf_counter()

    data = pd.DataFrame(stats)
    data.to_csv(args.output)
    print(f'took {allstop-allstart} sec')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--randomize',
                        action='store_true',
                        help=('Randomize selection when there are only two '
                              'possible words.'),
                        )
    parser.add_argument('-g', '--max_guesses',
                        type=int,
                        default=6,
                        help=('Maximum number of allowed guesses.'),
                        )
    parser.add_argument('-o', '--output',
                        type=str,
                        default='test_guessing_all_wordles.csv',
                        help=('Output file for statistics.')
                        )
    args = parser.parse_args()
    main(args)
