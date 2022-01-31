import tree
import information as info
import time

with open('resources/guessable_words.txt', 'r') as fi:
    guess_words = [l.strip() for l in fi.readlines()]
with open('resources/mystery_words.txt', 'r') as fi:
    hidden_words = [l.strip() for l in fi.readlines()]

print(f"Started with {len(hidden_words)} possible words.")


def build_tree(word_list):
    print("Building tree...")
    tree_start = time.perf_counter()
    root = tree.Node()
    tree.build_tree_from_list(root, word_list)
    tree_end = time.perf_counter()
    print(f"Built tree in {tree_end - tree_start:04f} seconds")
    return root


def guess(root):
    print("Finding best word...")
    entropy_start = time.perf_counter()
    guesses = info.get_best_words(guess_words, root)
    entropy_end = time.perf_counter()
    print(f"Found best word in {entropy_end - entropy_start:04f} seconds")
    return guesses[0]


root = build_tree(hidden_words)

# Assuming the word is "crimp"

# This step took me around 2 minutes, but the best word
#   (soare) will not change unless the wordlist does.
#   So it's really not worth actually performing this step in practice
#first_guess = guess(root)
#print((f"Start by guessing \"{first_guess[0]}\" "
       #f"with entropy {first_guess[1]:.2f}"))

first_partition = root.get_single_part("soare", [0, 0, 0, 1, 0])
print(("First guess reduced the number of"
       f" possible words to {len(first_partition)}"))


root = build_tree(first_partition)
second_guess = guess(root)
print(f"Next, guess \"{second_guess[0]}\" with entropy {second_guess[1]:.2f}")

second_partition = root.get_single_part("glint", [0, 0, 2, 0, 0])
print(("Second guess reduced the number of"
       f" possible words to {len(second_partition)}:"))
print(', '.join(second_partition))

root = build_tree(second_partition)
third_guess = guess(root)
print(f"Next, guess \"{third_guess[0]}\" with entropy {third_guess[1]:.2f}")

third_partition = root.get_single_part("becap", [0, 0, 1, 0, 2])
print(("Third guess reduced the number of"
       f" possible words to {len(third_partition)}:"))
print(', '.join(third_partition))
