# Tutorial

This is intended to be a tutorial walk-through of the various versions of the n-gram code.

## ngram.py

The overall approach is:
* loop over `N` for different values
* calculate all the `N`-grams in a given list of tokens
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
def ngram(it, n):
    """generates the n-grams (for given `n`) for a given iterator `it`"""

    window = ("*",) * n

    for current in it:
        window = window[1:] + (current,)
        yield window

    for i in range(n):
        window = window[1:] + ("*",)
        yield window
```

The only different in `ngram.py` is we support the passing in of a normalisation function that will be called on each token before adding it to the window.

So our function signature becomes

```
ngram(it, n, norm_func=None)
```

and we handle the default case with

```
if norm_func is None:
    norm_func = lambda w: w  # identity function
```

We then call this function on the current token before adding it to the window:

```
window = window[1:] + (norm_func(current),)
```

The normalise function used in `ngram.py` just strips punctuations:

```
def normalise(w):
    return w.strip("·.,")
```

So we end up calling `ngram` like

```
ngram(f.read().split(), N, normalise)
```

where `f` is the file object we read and split into tokens.

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
c = collections.Counter(ngram(f.read().split(), N, normalise))
for t, count in c.most_common():
    if count > 1:
        print(f"{N} {count} | {' '.join(t)}")
```

If this were run on `A B C D A B C A B C D` with `N = 2`, we'd get output like:

```
2 3 | A B
2 3 | B C
2 2 | C D
```

The first number is the value of `N` and the second number the count of the `N`-gram shown after the `|`.

### Looping values of N

We don't just want the results for a single `N`, we want to try lots of different values of `N` and so this is all wrapped in a loop over the value of `N`. Hence we have:

```
FILENAME = "../data-cleanup/iliad.txt"
START_N = 6
END_N = 75

for N in range(START_N, END_N + 1):
    with open(FILENAME) as f:
        ...
```
