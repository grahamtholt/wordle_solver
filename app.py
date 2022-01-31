import solver
import pandas as pd
from re import sub

DEBUG = False


class Wordler:
    def __init__(self, datafile: str):
        self.word_length = 5
        self.datafile = datafile
        self.data = None

        # State will change on start
        self.observations = []
        self.sol_size = None
        self.partition = {}

        self.load_data()

    def start(self):
        self.loop()
        self.stop()

    def loop(self, max_guesses=6):
        counter = 0
        while self.sol_size > 2 and counter < max_guesses:
            # Generate guess based on internal state
            guess, entropy = self.generate_guess()
            print(f"Guess {guess} (entropy {entropy:.2f})")
            self.receive_observation(guess)
            self.generate_partition()

        part_string = ' or '.join([f"\"{w.upper()}\"" for w in self.partition])
        if self.sol_size == 2:
            print(f"Choose randomly from {part_string}")
        elif self.sol_size == 1:
            print(f"Choose {part_string}")
        else:
            print("No compatible words found.")

    @solver.timing(DEBUG)
    def load_data(self):
        print("Loading data...")
        self.data = pd.read_parquet(self.datafile)
        self.sol_size = self.data.shape[0]

    def reset(self):
        self.observations = []
        self.sol_size = self.data.shape[0]
        self.partition = {}

    def generate_guess(self):
        return solver.get_optimal_guess(self.data, self.observations)

    def receive_observation(self, guess, tries_remaining=3):
        raw = input((f"Enter Wordle response for \"{guess.upper()}\" "
                     "(0=gray, 1=yellow, 2=green):\t"))
        clean = sub("[^012]", "", raw.strip())
        if len(clean) == self.word_length:
            obs = int(clean, base=3)
            self.observations.append((guess, obs))
        elif tries_remaining > 0:
            print("Invalid input. Please try again...")
            self.receive_observation(guess, tries_remaining=tries_remaining-1)
        else:
            self.stop()

    def generate_partition(self):
        self.partition = set(solver.get_partition(
            self.data, self.observations).index)
        self.sol_size = len(self.partition)

    def stop(self):
        self.reset()