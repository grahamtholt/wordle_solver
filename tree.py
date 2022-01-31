import string
from collections import defaultdict
from collections.abc import Iterable
from itertools import groupby, chain, combinations

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

    def get_max_partitions(self, word, vec, offset=0):
        # Check for duplicates and ensure that the indices match
        for dup in sorted(list_duplicates(word)):
            flags = [vec[i] for i in dup[1]]
            if not all_equal(flags):
                return [{}]
        vecdict = dict(zip(word, vec))
        w_order = sorted(
            set(word), key=lambda char: vecdict[char], reverse=True)

        flag_order = [vecdict[char] for char in w_order]

        if offset >= len(flag_order):
            return get_extraparts(self.wordset, word, vec)
        elif flag_order[offset] >= 1:
            if not self.children[w_order[offset]]:
                return [{}]
            return self.children[w_order[offset]].get_max_partitions(
                                      word, vec, offset=offset+1)
        else:
            # otherwise the rest of the letters should not be in the word
            exclist = [self.children[k].wordset for k in w_order[offset:]
                       if self.children[k]
                       ]
            if not exclist:
                return get_extraparts(self.wordset, word, vec)
            return get_extraparts(self.wordset.difference(set.union(*exclist)),
                                  word, vec)

    def get_single_part(self, word, vec):
        to_return = self.wordset

        def helper(word, char, flag, idx):
            if flag == 2 and char == word[idx]:
                return True
            elif flag == 1 and char in word and char != word[idx]:
                return True
            elif flag == 0 and char not in word:
                return True
            else:
                return False

        for index, tup in enumerate(zip(word, vec)):
            char = tup[0]
            flag = tup[1]
            to_return = set(
                [w for w in to_return if helper(w, char, flag, index)])
        return to_return


def get_extraparts(wordlist, word, vec):
    pos_index = [i for i, ele in enumerate(vec) if ele > 0]
    extra_partitions = []
    for partition in powerset(pos_index):
        extra_partitions.append(extraparts_helper(
            wordlist, word, pos_index, partition))
    return extra_partitions


def extraparts_helper(wordlist, word, pos_index, sameset):
    diffset = set(pos_index).difference(set(sameset))
    return set([w for w in wordlist if difference(word, w, diffset)
                and same(word, w, sameset)])


def difference(word, x, diffset):
    return all([word[idx] != x[idx] for idx in diffset])


def same(word, x, sameset):
    return all([word[idx] == x[idx] for idx in sameset])


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


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
