# Wordle Solver

Code to generate optimal guesses for the [Wordle](https://www.powerlanguage.co.uk/wordle/) puzzle game.
The game asks the player to guess a hidden word by making repeated, one-word guesses and then incorporating feedback.

Uses a word-list (currently a subset of the `words_alpha.txt` wordlist from the [dwyl/english-words](https://github.com/dwyl/english-words) git repo) and finds the guesses that provide the highest expected information content based on the word-list.

This code is in progress and very rough.

## Usage
```
import tree
import information as info
```
The first guess:
```
root = tree.Node()
# The following two steps may take a few seconds to a minute, because
# they are currently almost completely unoptimized
tree.build_tree(root, 'resources/words_5l.txt')
first_guesses = info.get_best_words(root)
```

Pick a guess and enter it into Wordle.
Encode the output as a list of length 5, where `0` represents a miss (gray box) and `1` represents a hit (green or yellow box).
For example, I chose "arise" as my first guess.
```
output = [0,1,0,0,0]
first_partition = root.get_partition("arise", output)

# Now the second guess
root.clear()
tree.build_tree_from_list(root, first_partition)
second_guesses = info.get_best_words(root)
```
And so on and so forth.
