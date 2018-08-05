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


def ngram_with_ref(it, n, norm_func=None):
    if norm_func is None:
        norm_func = lambda w: w  # identity function

    ref_window = ("*",) * n
    item_window = ("*",) * n

    for ref, item in it:
        ref_window = ref_window[1:] + (ref,)
        item_window = item_window[1:] + (norm_func(item),)
        if "*" not in item_window:
            yield ref_window[0], ref_window[-1], item_window

ngrams = {}
subgrams = {}

# filename = "test3.txt"
# start_N = 2
# end_N = 5

# filename = "iliad2.txt"
# start_N = 4
# end_N = 100

# filename = "odyssey2.txt"
# start_N = 4
# end_N = 100

filename = "combined2.txt"
start_N = 4
end_N = 100

def deref(f):
    for line in f:
        ref, content = line.strip().split(maxsplit=1)
        for item in content.split():
            yield ref, item

# N descends from end_N to start_N inclusive
for N in range(end_N, start_N - 1, -1):
    with open(filename) as f:
        for start_ref, end_ref, seq in ngram_with_ref(deref(f), N, normalise):
            ngrams.setdefault(N, {}).setdefault(seq, []).append((start_ref, end_ref))
            subgrams[N - 1] = collections.Counter()
    for X, refs in ngrams[N].items():
        naive_count = len(refs)
        subgram_count = subgrams.get(N, {}).get(X, 0)
        if naive_count > 1 and naive_count > subgram_count:
            print(f"{N} {naive_count} {subgram_count} | {' '.join(X)} | {' '.join(f'{start_ref}-{end_ref}' for start_ref, end_ref in refs)}")
        if naive_count > 1:
            for Y in ngram(X, N - 1):
                subgrams[N - 1][Y] += naive_count
