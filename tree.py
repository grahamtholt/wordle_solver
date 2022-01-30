import string
from collections import defaultdict
from collections.abc import Iterable
from itertools import groupby

# TODO: try doing this without the tree and just with set logic


class Node:
    def __init__(self, key="", alpha=string.ascii_lowercase):
        self.key = key
        self.children = dict(zip(alpha, [None]*len(alpha)))
        self.wordset = set()

    def insert(self, word, suffix):
        self.wordset.add(word)
        for char in set(suffix):
            # If there is no node, create one
            if not self.children[char]:
                self.children[char] = Node(char)
            # Remove the character from the suffix
            new_suffix = suffix.replace(char, "")
            # Continue on adding the word down the tree
            self.children[char].insert(word, new_suffix)

    def __str__(self):
        return f"{self.key}: {len(self.wordset)} words"

    def clear(self, alpha=string.ascii_lowercase):
        self.key = ""
        self.children = dict(zip(alpha, [None]*len(alpha)))
        self.wordset = set()

    def count_partition(self, word, vec, offset=0):
        # Check for duplicates and ensure that the indices match
        for dup in sorted(list_duplicates(word)):
            flags = [vec[i] for i in dup[1]]
            if not all_equal(flags):
                return 0

        vecdict = dict(zip(word, vec))
        w_order = sorted(
            set(word), key=lambda char: vecdict[char], reverse=True)

        flag_order = [vecdict[char] for char in w_order]

        if offset >= len(flag_order):
            return len(self.wordset)
        elif flag_order[offset] == 1:
            if not self.children[w_order[offset]]:
                return 0
            return self.children[w_order[offset]].count_partition(
                    word, vec, offset=offset+1)
        else:
            # otherwise the rest of the letters should not be in the word
            exclist = [self.children[k].wordset for k in w_order[offset:]
                       if self.children[k]
                       ]
            if not exclist:
                return len(self.wordset)
            return len(self.wordset) - len(set.union(*exclist))

    def get_partition(self, word, vec, offset=0):
        # Check for duplicates and ensure that the indices match
        for dup in sorted(list_duplicates(word)):
            flags = [vec[i] for i in dup[1]]
            if not all_equal(flags):
                return {}
        vecdict = dict(zip(word, vec))
        w_order = sorted(
            set(word), key=lambda char: vecdict[char], reverse=True)

        flag_order = [vecdict[char] for char in w_order]

        if offset >= len(flag_order):
            return self.wordset
        elif flag_order[offset] == 1:
            if not self.children[w_order[offset]]:
                return {}
            return self.children[w_order[offset]].get_partition(
                    word, vec, offset=offset+1)
        else:
            # otherwise the rest of the letters should not be in the word
            exclist = [self.children[k].wordset for k in w_order[offset:]
                       if self.children[k]
                       ]
            if not exclist:
                return self.wordset
            return self.wordset.difference(set.union(*exclist))


def build_tree(root: Node, file: str):
    with open(file, 'r') as fi:
        while True:
            word = fi.readline()
            if not word:
                break
            root.insert(word.strip(), word.strip())


def build_tree_from_list(root: Node, wordlist: Iterable):
    for word in wordlist:
        root.insert(word.strip(), word.strip())


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items()
            if len(locs) > 1)


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
