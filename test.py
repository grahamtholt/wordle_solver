import tree
import information as info

root = tree.Node()
tree.build_tree(root, 'resources/mystery_words.txt')

with open('resources/guessable_words.txt', 'r') as fi:
    all_words = [l.strip() for l in fi.readlines()]


# Assuming the word is "crimp"
first_guesses = info.get_best_words(all_words, root)
print(first_guesses)

first_part = root.get_partition("arets", [0, 1, 0, 0, 0])
first_part = [w for w in first_part if w[1] == 'r']

root2 = tree.Node()
tree.build_tree_from_list(root2, first_part)
second_guesses = info.get_best_words(all_words, root2)
print(second_guesses)

second_part = root2.get_partition("poind", [1, 0, 1, 0, 0])
second_part = [w for w in second_part if w[1]
               == 'r' and w[0] != 'p' and w[2] == 'i']
print(second_part)

root3 = tree.Node()
tree.build_tree_from_list(root3, second_part)
third_guesses = info.get_best_words(all_words, root3)
print(third_guesses)
