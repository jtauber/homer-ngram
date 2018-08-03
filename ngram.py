#!/usr/bin/env python3

import collections


def normalise(w):
    return w.strip("·.,")


def ngram(it, n, norm_func=None):
    """
    generates the n-grams (for given `n`) for a given iterator `it`, calling
    the optional given `norm_func` function on each item as well.
    """
    if norm_func is None:
        norm_func = lambda w: w  # identity function

    window = ("*",) * n

    for current in it:
        window = window[1:] + (norm_func(current),)
        yield window

    for i in range(n):
        window = window[1:] + ("*",)
        yield window


for N in range(6, 75):
    with open("iliad.txt") as f:
        c = collections.Counter(ngram(f.read().split(), N, normalise))
    d = collections.Counter()
    for t, count in c.most_common():
        d[count] += 1

    print(N, d)
