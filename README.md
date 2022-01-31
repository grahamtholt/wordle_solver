# Wordle Solver

Code to generate optimal guesses for the [Wordle](https://www.powerlanguage.co.uk/wordle/) puzzle game.
The game asks the player to guess a hidden word by making repeated, one-word guesses and then incorporating feedback.

Uses a word-list (currently from the wordle source code) and finds the guesses that provide the highest expected information gain based on the word-list.

This code is in progress and very rough.

## Usage
See the included `example.py` for an example of guessing the hidden word "crimp".
