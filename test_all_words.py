import information as info
import tree
import pandas as pd
import time

FIRST_GUESS = "soare"
with open('resources/guessable_words.txt', 'r') as fi:
    GUESS_WORDS = [l.strip() for l in fi.readlines()]
with open('resources/mystery_words.txt', 'r') as fi:
    HIDDEN_WORDS = [l.strip() for l in fi.readlines()]


def evaluate_guess(guess, mystery):
    output = []
    for i, char in enumerate(guess):
        if mystery[i] == char:
            output.append(2)
        elif mystery[i] != char and char in mystery:
            output.append(1)
        else:
            output.append(0)
    return output


def find_wordle(mystery, root):
    """
    Returns the number of total word entries required to get the wordle
    """
    start = time.perf_counter()
    counter = 1
    first_output = evaluate_guess(FIRST_GUESS, mystery)
    partition = root.get_single_part(FIRST_GUESS, first_output)
    possible_words = len(partition)
    new_root = tree.Node()
    while possible_words > 1:
        new_root.clear()
        tree.build_tree_from_list(new_root, partition)
        guess = info.get_best_words(GUESS_WORDS, new_root)[0][0]
        output = evaluate_guess(guess, mystery)
        partition = new_root.get_single_part(guess, output)
        counter = counter + 1
        possible_words = len(partition)
    assert(list(partition)[0] == mystery)
    end = time.perf_counter()
    return counter + 1, end-start


def main():
    root = tree.Node()
    tree.build_tree_from_list(root, HIDDEN_WORDS)

    num_guesses, times = zip(*[find_wordle(word, root)
                             for word in HIDDEN_WORDS])
    data = pd.DataFrame(
        {"Words": HIDDEN_WORDS[:2],
         "Guesses": num_guesses,
         "Runtime(s)": times})
    data.to_csv('guessing_all_wordles.csv')


if __name__ == '__main__':
    main()
