#!/usr/bin/env python3

import collections


def normalise(w):
    return w.strip("·.,")


def ngram(it, n, norm_func=None, pad=False):
    """
    generates the n-grams (for given `n`) for a given iterator `it`, calling
    the optional given `norm_func` function on each item as well.
    If `pad` is true the first n-1 and last n-1 n-grams will be padded.
    """
    if norm_func is None:
        norm_func = lambda w: w  # identity function

    window = ("*",) * n

    for current in it:
        window = window[1:] + (norm_func(current),)
        if pad or "*" not in window:
            yield window

    if pad:
        for i in range(n):
            window = window[1:] + ("*",)
            yield window


def summarise_counter(c):
    d = collections.Counter()
    for t, count in c.most_common():
        d[count] += 1
    return dict(d)

ngrams = {}
subgrams = {}

filename = "test.txt"
s = 2
e = 5

# filename = "iliad.txt"
# s = 4
# e = 74

for N in range(e, s - 1, -1):
    with open(filename) as f:
        ngrams[N] = collections.Counter(ngram(f.read().split(), N, normalise))
        print(N)
        subgrams[N - 1] = collections.Counter()
        for X, naive_count in ngrams[N].items():
            subgram_count = subgrams.get(N, {}).get(X, 0)
            if naive_count > 1 and naive_count > subgram_count:
                print("   ", naive_count, subgram_count, "|", " ".join(X))
            if naive_count > 1:
                for Y in ngram(X, N - 1):
                    subgrams[N - 1][Y] += naive_count
