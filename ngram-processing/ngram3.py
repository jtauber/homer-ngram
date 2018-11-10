#!/usr/bin/env python3

import collections


# FILENAME = "../data/test3.txt"
# START_N = 2
# END_N = 5
#
# FILENAME = "../data/iliad2.txt"
# START_N = 4
# END_N = 100
#
# FILENAME = "../data/odyssey2.txt"
# START_N = 4
# END_N = 100
#
# FILENAME = "../data/combined2.txt"
# START_N = 4
# END_N = 100
#
# FILENAME = "../iliad-lemma.txt"
# START_N = 4
# END_N = 100

FILENAME = "../odyssey-lemma.txt"
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


def ngram_with_ref(it, n, norm_func=identity):
    ref_window = ("*",) * n
    item_window = ("*",) * n

    for ref, item in it:
        ref_window = ref_window[1:] + (ref,)
        item_window = item_window[1:] + (norm_func(item),)
        if "*" not in item_window:
            yield ref_window[0], ref_window[-1], item_window


def deref(f):
    for line in f:
        ref, content = line.strip().split(maxsplit=1)
        for item in content.split():
            yield ref, item


ngrams = {}
subgrams = {}

# N descends from END_N to START_N inclusive
for N in range(END_N, START_N - 1, -1):
    with open(FILENAME) as f:
        for start_ref, end_ref, seq in ngram_with_ref(deref(f), N, normalise):
            ngrams.setdefault(N, {}).setdefault(seq, []).append(
                (start_ref, end_ref))
    subgrams[N - 1] = collections.Counter()
    for X, refs in ngrams[N].items():
        naive_count = len(refs)
        subgram_count = subgrams.get(N, {}).get(X, 0)
        if naive_count > 1 and naive_count > subgram_count:
            ref_list = " ".join(
                f"{start_ref}-{end_ref}" for start_ref, end_ref in refs)
            tokens = " ".join(X)
            print(f"{N} {naive_count} {subgram_count} | {ref_list} | {tokens}")
        if naive_count > 1:
            for Y in ngram(X, N - 1):
                subgrams[N - 1][Y] += naive_count
