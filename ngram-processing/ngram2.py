#!/usr/bin/env python3

import collections


# FILENAME = "../data/test.txt"
# START_N = 2
# END_N = 5

FILENAME = "../data-cleanup/iliad.txt"
START_N = 4
END_N = 100


def normalise(w):
    return w.strip("·.,")


def identity(w):
    return w


def ngram(it, n, norm_func=identity, pad=False):
    """
    generates the n-grams (for given `n`) for a given iterator `it`, calling
    the optional given `norm_func` function on each item as well.
    If `pad` is true the first n-1 and last n-1 n-grams will be padded.
    """
    window = ("*",) * n

    for current in it:
        window = window[1:] + (norm_func(current),)
        if pad or "*" not in window:
            yield window

    if pad:
        for i in range(n):
            window = window[1:] + ("*",)
            yield window


ngrams = {}
subgrams = {}

# N descends from END_N to START_N inclusive
for N in range(END_N, START_N - 1, -1):
    with open(FILENAME) as f:
        ngrams[N] = collections.Counter(ngram(f.read().split(), N, normalise))
    subgrams[N - 1] = collections.Counter()
    for X, naive_count in ngrams[N].items():
        subgram_count = subgrams.get(N, {}).get(X, 0)
        if naive_count > 1 and naive_count > subgram_count:
            print(f"{N} {naive_count} {subgram_count} | {' '.join(X)}")
        if naive_count > 1:
            for Y in ngram(X, N - 1):
                subgrams[N - 1][Y] += naive_count
