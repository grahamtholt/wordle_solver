import argparse
import importlib.resources as pkg_resources

import pandas as pd

from wordler.app import application
from wordler.utils import precompute_data
from wordler import resources


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--max-guesses',
                    type=int,
                    default=6,
                    help=("Maximum number of guesses allowed to the "
                          "player. Defaults to 6.")
                    )
parser.add_argument('-s', '--custom-start',
                    type=str,
                    help=("Force the solver to start with a specific guess"
                          "word, instead of choosing its own.")
                    )
args = parser.parse_args()

print("Reading precomputed data...")
try:
    with pkg_resources.path(resources, "data.parquet") as pq:
        data = pd.read_parquet(pq)
except FileNotFoundError:
    print("Cached result not found, calculating colorings...")
    data = precompute_data.run()

if args.custom_start:
    application.Wordler(data).start(max_guesses=args.max_guesses,
                                    custom_start=args.custom_start)
else:
    application.Wordler(data).start(max_guesses=args.max_guesses)
