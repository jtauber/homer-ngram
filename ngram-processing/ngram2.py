#!/usr/bin/env python3

"""
Finds repeating n-grams in a file of whitespace-separated tokens like
`ngram.py` but removes trivial subsequences of larger n+1-grams.

See `subgram_removal.md` for more explanationself.

```
$ cat ../data/test.txt
A B C D A B C A B C D
$ ./ngram2.py 2-10 ../data/test.txt
4 2 0 | A B C D
3 3 2 | A B C
```

The first number is the value of `n`, the second number is the naive count,
and the third number is the number of counts that are just the result of being
a subgram of a longer ngram.
"""


import argparse
import collections


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


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("range", help="n-gram range to calc, e.g. 6-100")
    argparser.add_argument("filename")

    args = argparser.parse_args()

    filename = args.filename
    start_n, end_n = (int(arg) for arg in args.range.split("-"))

    with open(filename) as f:
        tokens = f.read().split()

    higher_subgram_counter = collections.Counter()

    # N descends from END_N to START_N inclusive
    for n in range(end_n, start_n - 1, -1):
        ngram_counter = collections.Counter(ngram(tokens, n, normalise))
        subgram_counter = collections.Counter()

        for ngram_tokens, naive_count in ngram_counter.items():
            subgram_count = higher_subgram_counter[ngram_tokens]

            # our heuristic is to only care if the naïve n-gram count > 1 (as
            # before) AND the naïve n-gram count is strictly great than the
            # count from subgrams of repeated n+1-grams.
            if naive_count > 1 and naive_count > subgram_count:
                print(f"{n} {naive_count} {subgram_count} | {' '.join(ngram_tokens)}")

            if naive_count > 1:
                for subgram_tokens in ngram(ngram_tokens, n - 1):
                    subgram_counter[subgram_tokens] += naive_count

        higher_subgram_counter = subgram_counter
