#!/usr/bin/env python3

"""
Finds repeating n-grams in a file of whitespace-separated tokens.

```
$ cat ../data/test.txt
A B C D A B C A B C D
$ ./ngram.py 2-10 ../data/test.txt
2 3 | A B
2 3 | B C
2 2 | C D
3 3 | A B C
3 2 | B C D
4 2 | A B C D
```

The first number is the value of `n` and the second number the count of the
particular `n`-gram shown after the `|`.
"""


import argparse
import collections


def normalise(w):
    return w.strip("·.,")


def identity(w):
    return w


def ngram(tokens, n, norm_func=identity):
    """
    generates the n-grams (for given `n`) for a given iterator `tokens`,
    calling the optional given `norm_func` function on each item as well.
    """
    window = ["*"] * n

    for token in tokens:
        window = window[1:] + [norm_func(token)]
        yield tuple(window)

    for i in range(n):
        window = window[1:] + ["*"]
        yield tuple(window)


def print_repeated_ngrams(n, tokens, norm_func=identity):
    ngram_counter = collections.Counter(ngram(tokens, n, norm_func))
    for token_list, count in ngram_counter.most_common():
        if count > 1:
            print(f"{n} {count} | {' '.join(token_list)}")


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("range", help="n-gram range to calc, e.g. 6-100")
    argparser.add_argument("filename")

    args = argparser.parse_args()

    filename = args.filename
    start_n, end_n = (int(arg) for arg in args.range.split("-"))

    with open(filename) as f:
        tokens = f.read().split()

    # this is quite inefficient in that it goes over the tokens each time but,
    # for now, it's fast enough for our purposes
    for n in range(start_n, end_n + 1):
        print_repeated_ngrams(n, tokens, normalise)
