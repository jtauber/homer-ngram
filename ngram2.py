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
        if "*" not in window:
            yield window

    # for i in range(n):
    #     window = window[1:] + ("*",)
    #     yield window


def summarise_counter(c):
    d = collections.Counter()
    for t, count in c.most_common():
        d[count] += 1
    return dict(d)

ngrams = {}
subgrams = {}

filename = "test.txt"
s = 1
e = 5

# filename = "iliad.txt"
# s = 70
# e = 74

for N in range(e, s - 1, -1):
    with open(filename) as f:
        ngrams[N] = collections.Counter(ngram(f.read().split(), N, normalise))
        print(N)
        subgrams[N - 1] = collections.Counter()
        for X, c in ngrams[N].items():
            d = subgrams.get(N, {}).get(X)
            if c > 1 and (d is None or c > d):
                print("\t", X, c, d)
            if c > 1:
                for Y in ngram(X, N - 1):
                    subgrams[N - 1][Y] += c
