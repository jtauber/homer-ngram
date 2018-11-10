#!/usr/bin/env python3

import collections


FILENAME = "../data/iliad2.txt"
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

    for ref, word_offset, line_length, item in it:
        ref_window = ref_window[1:] + ((ref, word_offset, line_length),)
        item_window = item_window[1:] + (norm_func(item),)
        if "*" not in item_window:
            start_ref = (
                ref_window[0][0] + ":" +
                str(ref_window[0][1]) + "/" + str(ref_window[0][2]))
            end_ref = (
                ref_window[-1][0] + ":" +
                str(ref_window[-1][1]) + "/" + str(ref_window[-1][2]))
            yield start_ref, end_ref, item_window


def deref(f):
    for line in f:
        ref, content = line.strip().split(maxsplit=1)
        tokens = content.split()
        line_length = len(tokens)
        for word_offset, item in enumerate(tokens):
            yield ref, word_offset, line_length, item


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
