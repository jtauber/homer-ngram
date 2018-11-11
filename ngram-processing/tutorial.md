# Tutorial

This is intended to be a tutorial walk-through of the various versions of the n-gram code.


## ngram.py

The overall approach is:
* loop over `n` for different values
* calculate all the `n`-grams in a given list of tokens
* count how many times each of those occurs
* print out those occurring more than once


### Calculating n-grams

Here's a simple walkthrough of how to calculate the trigrams (i.e `N = 3`) of the token list `["A", "B", "C", "D"]`.

We start with a tuple of length `N` of some dummy token like `*`:

`("*", "*", "*")`

We'll call this tuple the `window`.

We then drop the item at the start of the window and add the first token, `"A"`, from our token list to the end:

`("*", "*", "A")`

This is our first n-gram. We continue to do this for all the items in our token list:

`("*", "A", "B")` `("A", "B", "C")` `("B", "C", "D")`

Finally we clear out the window by adding a dummy token N-1 more times.

`("C", "D", "*")` `("D", "*", "*")`


In implementing this, we make use of iterators and generators. Here's some code very similar to what's in `ngram.py`:

```
def ngram(tokens, n):
    """generates the n-grams (for given `n`) for a given iterator `token`"""

    window = ["*"] * n

    for token in tokens:
        window = window[1:] + [token]
        yield tuple(window)

    for i in range(n):
        window = window[1:] + ["*"]
        yield tuple(window)
```

The only different in `ngram.py` is we support the passing in of a normalisation function that will be called on each token before adding it to the window.

So our function signature becomes

```
def ngram(tokens, n, norm_func=identity):
```

and we handle the default case with

```
def identity(w):
    return w
```

We then call this function on the current token before adding it to the window:

```
window = window[1:] + [norm_func(token)]
```

The normalise function used in `ngram.py` just strips punctuations:

```
def normalise(w):
    return w.strip("·.,")
```

So we end up calling `ngram` like

```
ngram(tokens, n, normalise)
```


### Counting n-grams

So far, this code calculated *all* the n-grams and we only want the ones that occur more than once. The way we do this in `ngram.py` is to count n-gram occurences with `collections.Counter`.

If you construct a `Counter` with a list (or an iterator), it will keep count of the occurences of each item. You can then query the counter for various information, such as all the items in order of occurence count.

```
>>> import collections
>>> c = collections.Counter(["X", "X", "Y", "Z", "X", "Y"])
>>> c.most_common()
[('X', 3), ('Y', 2), ('Z', 1)]
```

And so we count our n-grams, loop over the counter and display those occurring more than one:

```
def print_repeated_ngrams(n, tokens, norm_func=identity):
    ngram_counter = collections.Counter(ngram(tokens, n, norm_func))
    for token_list, count in ngram_counter.most_common():
        if count > 1:
            print(f"{n} {count} | {' '.join(token_list)}")
```

If this were run on `A B C D A B C A B C D` with `n = 2`, we'd get output like:

```
2 3 | A B
2 3 | B C
2 2 | C D
```

The first number is the value of `n` and the second number the count of the `n`-gram shown after the `|`.


### Looping values of n

We don't just want the results for a single `n`, we want to try lots of different values of `n` and so this is all wrapped in a loop over the value of `n`. Hence we have:

```
for n in range(start_n, end_n + 1):
    with open(filename) as f:
        print_repeated_ngrams(n, f.read().split(), normalise)
```

Note that this is quite inefficient in that it goes over the file for ever value of n. While a more efficient algorithm could be used, it's fast enough for our purposes.


### Turning into a command-line tool

Finally, we use the `argparser` module to parse command-line arguments to get `filename`, `start_n`, and `end_n`:

```
import argparse

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("range", help="n-gram range to calc, e.g. 6-100")
    argparser.add_argument("filename")

    args = argparser.parse_args()

    filename = args.filename
    start_n, end_n = (int(arg) for arg in args.range.split("-"))
```

The script can now be run like

```
./ngram.py 2-10 ../data/test.txt
```

or

```
./ngram.py 6-75 ../data-cleanup/iliad.txt
```
