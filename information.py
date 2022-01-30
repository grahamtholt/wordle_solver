import string
import numpy as np
from tree import Node
from itertools import product

ALPHABET = string.ascii_lowercase


def get_char_freqs(file, alpha=ALPHABET):
    counts = dict(zip(alpha, [0]*len(alpha)))
    total = 0
    with open(file, 'r') as fi:
        while True:
            word = fi.readline()
            if not word:
                break
            total = total + 1
            for char in set(word.strip()):
                counts[char] = counts[char] + 1

    p = [counts[k]/total for k in counts]
    probs = dict(zip(counts.keys(), p))
    return probs


def get_char_entropy(file, alpha=ALPHABET):
    probs = get_char_freqs(file, alpha)
    ent = [-probs[k]*np.log2(probs[k]) for k in probs]
    return dict(zip(probs.keys(), ent))


def get_entropy_ordering(file, alpha=ALPHABET):
    ent = get_char_entropy(file, alpha)
    return sorted(ent.keys(), key=lambda k: ent[k], reverse=True)


def get_entropy_of_word(root: Node, word, wordlength=5):
    counts = [root.count_partition(word, v)
              for v in product([0, 1], repeat=wordlength)]
    probs = [c / len(root.wordset) for c in counts]
    return -1*sum([p*np.log2(p) for p in probs if p > 0])


def get_best_words(wordlist, root, n=10):
    entropies = list(map(
        lambda x: get_entropy_of_word(root, x), wordlist))
    return sorted(zip(wordlist, entropies),
                  key=lambda x: x[1], reverse=True)[0:n]
