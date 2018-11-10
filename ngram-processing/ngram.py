#!/usr/bin/env python3

import collections


FILENAME = "../data-cleanup/iliad.txt"
START_N = 6
END_N = 75


def normalise(w):
    return w.strip("·.,")


def identity(w):
    return w


def ngram(it, n, norm_func=identity):
    """
    generates the n-grams (for given `n`) for a given iterator `it`, calling
    the optional given `norm_func` function on each item as well.
    """
    window = ("*",) * n

    for current in it:
        window = window[1:] + (norm_func(current),)
        yield window

    for i in range(n):
        window = window[1:] + ("*",)
        yield window


for N in range(START_N, END_N + 1):
    with open(FILENAME) as f:
        c = collections.Counter(ngram(f.read().split(), N, normalise))
    for t, count in c.most_common():
        if count > 1:
            print(f"{N} {count} | {' '.join(t)}")
