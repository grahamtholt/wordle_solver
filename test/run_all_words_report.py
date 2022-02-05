import pandas as pd
import time
from source import solver
import multiprocessing
from random import randint
import numpy as np
import time

FIRST_GUESS = "soare"
with open('resources/mystery_words.txt', 'r') as fi:
    HIDDEN_WORDS = [l.strip() for l in fi.readlines()]

DATA = pd.read_parquet('resources/data.parquet')
SOLS = DATA.shape[0]
CORRECT = 242


def test_find_wordle(mystery, max_guesses=6):
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
        choice = randint(0, 1)
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


def pad(x: list, l=6):
    return x + [np.nan] * (l - len(x))


def main():
    pool = multiprocessing.Pool(8)
    stats = pool.map(test_find_wordle, HIDDEN_WORDS)

    data = pd.DataFrame(stats)
    data.to_csv('guessing_all_wordles.csv')


if __name__ == '__main__':
    main()
