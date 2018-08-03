#!/usr/bin/env python3

import collections


def normalise(w):
    return w.strip("·.,")


def ngram(it, n, norm_func):
    """
    generates the n-grams (for given `n`) for a given iterator `it`, calling
    the given `norm_func` function on each item as well.
    """
    window = ("*",) * n

    for current in it:
        window = window[1:] + (norm_func(current),)
        yield window

    for i in range(n):
        window = window[1:] + ("*",)
        yield window


for N in range(6, 75):
    c = collections.Counter()
    d = collections.Counter()
    with open("iliad.txt") as f:
        for x in ngram(f.read().split(), N, normalise):
            c[x] += 1
    for t, count in c.most_common():
        d[count] += 1

    print(N, d)
