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
start_N = 2
end_N = 5

# filename = "iliad.txt"
# start_N = 4
# end_N = 74

# N descends from end_N to start_N inclusive
for N in range(end_N, start_N - 1, -1):
    with open(filename) as f:
        ngrams[N] = collections.Counter(ngram(f.read().split(), N, normalise))
        subgrams[N - 1] = collections.Counter()
        for X, naive_count in ngrams[N].items():
            subgram_count = subgrams.get(N, {}).get(X, 0)
            if naive_count > 1 and naive_count > subgram_count:
                print(f"{N} {naive_count} {subgram_count} | {' '.join(X)}")
            if naive_count > 1:
                for Y in ngram(X, N - 1):
                    subgrams[N - 1][Y] += naive_count
