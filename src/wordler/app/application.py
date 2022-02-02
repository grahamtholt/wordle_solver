from re import sub

import pandas as pd

from wordler.utils import solver

DEBUG = False


class Wordler:
    def __init__(self, data: pd.DataFrame):
        self.word_length = 5
        self.data = data

        # State that will change
        self.observations = []
        self.sol_size = data.shape[0]
        self.partition = {}

    def start(self, max_guesses=6, custom_start=None):
        self.loop(max_guesses, custom_start)
        self.stop()

    def loop(self, max_guesses, custom_start):
        counter = 0
        while self.sol_size > 2 and counter < max_guesses:
            # Generate guess based on internal state
            if custom_start and counter == 0:
                guess, entropy = self.custom_guess(custom_start)
            else:
                guess, entropy = self.generate_guess()
            counter = counter + 1
            print(f"Guess {guess.upper()} (entropy {entropy:.2f})")
            valid = self.receive_observation(guess)
            if not valid:
                return
            self.generate_partition()

        part_string = ' or '.join([f"\"{w.upper()}\"" for w in self.partition])
        if self.sol_size == 2:
            print(f"Choose randomly from {part_string}")
        elif self.sol_size == 1:
            print(f"Choose {part_string}")
        else:
            print("No compatible words found.")

    def reset(self):
        self.observations = []
        self.sol_size = self.data.shape[0]
        self.partition = {}

    def generate_guess(self):
        return solver.get_optimal_guess(self.data, self.observations)

    def custom_guess(self, word):
        return word, solver.get_entropy(word, self.data, self.observations)

    def receive_observation(self, guess, tries_remaining=3):
        raw = input((f"Enter Wordle response for \"{guess.upper()}\" "
                     "(0=gray, 1=yellow, 2=green):\t"))
        clean = sub("[^012]", "", raw.strip())
        if len(clean) == self.word_length:
            obs = int(clean, base=3)
            self.observations.append((guess, obs))
            return True
        elif tries_remaining > 0:
            print("Invalid input. Please try again...")
            self.receive_observation(guess, tries_remaining=tries_remaining-1)
            return True
        else:
            return False

    def generate_partition(self):
        self.partition = set(solver.get_partition(
            self.data, self.observations).index)
        self.sol_size = len(self.partition)

    def stop(self):
        self.reset()
