import multiprocessing
from itertools import product
import importlib.resources as pkg_resources
from pathlib import Path

import pandas as pd

from wordler.utils.solver import evaluate_guess
from wordler import resources


def run():
    with pkg_resources.open_text(resources, "guessable_words.txt") as fi:
        GUESS_WORDS = [line.strip() for line in fi.readlines()]
    with pkg_resources.open_text(resources, "mystery_words.txt") as fi:
        HIDDEN_WORDS = [line.strip() for line in fi.readlines()]

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    combos = list(product(GUESS_WORDS, HIDDEN_WORDS))
    guesses = [t[0] for t in combos]
    hiddens = [t[1] for t in combos]
    values = pool.starmap(evaluate_guess, combos)

    data = pd.DataFrame({
        "Hidden Word": hiddens,
        "Guess Word": guesses,
        "Value": values
    })
    wide = data.pivot(index="Hidden Word",
                      columns="Guess Word", values="Value")

    resource_dir = Path(resources.__file__).parent.absolute()
    wide.to_parquet(resource_dir / "data.parquet")
    return wide
