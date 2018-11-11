#!/usr/bin/env python3

"""
Find repeating n-grams like `ngram3.py` but also returns offsets of tokens
within the references.

```
$ cat ../data/test3.txt
1 A B C
2 D A B
3 C A B
4 C D
$ ./ngram4.py 2-5 ../data/test3.txt
4 2 0 | 1:0/3-2:0/3 3:1/3-4:1/2 | A B C D
3 3 2 | 1:0/3-1:2/3 2:1/3-3:0/3 3:1/3-4:0/2 | A B C
```

where `1:0/3-2:0/3` (for example) means this n-gram goes from token `0` out of
`3` in ref `1` (the first `A`) though to token `0` out of `3` in ref `2` (the
first `D`).
"""

import argparse
import collections


def normalise(w):
    return w.strip("·.,")


def identity(w):
    return w


def ngram(tokens, n, norm_func=identity, pad=False):
    """
    generates the n-grams (for given `n`) for a given iterator `tokens`,
    calling the optional given `norm_func` function on each item as well.
    If `pad` is true the first n-1 and last n-1 n-grams will be padded.
    """
    window = ["*"] * n

    for token in tokens:
        window = window[1:] + [norm_func(token)]
        if pad or "*" not in window:
            yield tuple(window)

    if pad:
        for i in range(n):
            window = window[1:] + ["*"]
            yield tuple(window)


def ngram_with_ref(tokens_with_ref, n, norm_func=identity):
    """
    generates the n-grams (for given `n`) for a given iterator
    `tokens_with_ref` (which iterates over pairs of `(ref, token)`).
    The optional given `norm_func` function is called on each token.

    Each result yielded by this generator is of the form
    `((start_ref, end_ref), ngram)`.
    """

    ref_window = ["*"] * n
    token_window = ["*"] * n

    for ref, token in tokens_with_ref:
        ref_window = ref_window[1:] + [ref]
        token_window = token_window[1:] + [norm_func(token)]
        if "*" not in token_window:
            yield (ref_window[0], ref_window[-1]), tuple(token_window)


def deref(f):
    """
    takes an iterator over lines consisting of a reference followed by
    whitespace-separated tokens and yields `("{ref}:{offset}/{length}", token)`
    for each token.
    """
    for line in f:
        ref, content = line.strip().split(maxsplit=1)
        tokens = content.split()
        length = len(tokens)
        for offset, token in enumerate(tokens):
            yield f"{ref}:{offset}/{length}", token


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("range", help="n-gram range to calc, e.g. 6-100")
    argparser.add_argument("filename")

    args = argparser.parse_args()

    filename = args.filename
    start_n, end_n = (int(arg) for arg in args.range.split("-"))

    higher_subgram_counter = collections.Counter()

    # n descends from end_n to start_n inclusive
    for n in range(end_n, start_n - 1, -1):

        # In ngram2.py we had a `ngram_counter` that merely counted n-grams
        # Here we maintain a list of references for each n-gram. The count
        # is then just the lngth of this list.

        # keys are ngram_tokens, values are lists of (start_ref, end_ref)
        ngram_refs = collections.defaultdict(list)

        with open(filename) as f:
            for ref_range, ngram_tokens in ngram_with_ref(
                deref(f), n, normalise
            ):
                ngram_refs[ngram_tokens].append(ref_range)

        subgram_counter = collections.Counter()

        for ngram_tokens, refs in ngram_refs.items():
            naive_count = len(refs)
            subgram_count = higher_subgram_counter[ngram_tokens]

            if naive_count > 1 and naive_count > subgram_count:
                counts = f"{n} {naive_count} {subgram_count}"
                ref_list = " ".join(f"{r[0]}-{r[1]}" for r in refs)
                tokens = " ".join(ngram_tokens)
                print(f"{counts} | {ref_list} | {tokens}")

            if naive_count > 1:
                for subgram_tokens in ngram(ngram_tokens, n - 1):
                    subgram_counter[subgram_tokens] += naive_count

        higher_subgram_counter = subgram_counter
