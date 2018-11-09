# N-Gram Processing

*code for calculating the repeated n-grams in a token list*

## Files

* `ngram.py` finds repeating n-grams in a token list
* `ngram2.py` like `ngram.py` but removes trivial subsequences of larger n-grams (see Algorithm Note below)
* `ngram3.py` like `ngram2.py` but takes a token list with references and returns those references with the n-gram results
* `ngram4.py` like `ngram3.py` but returns offsets of token within the references as well

See `tutorial.md` for (the start of) a general walkthrough of this code.


## Algorithm Note

One problem with naïve n-gram generation for multiple n (like `ngram.py` does) is that all the subgrams of a repeated n-gram will show up as well and this generally not what is wanted.

For example, the string `A B C D A B C A B C D` has a repeated 4-gram `A B C D`. Naïve generation of 3-grams gives three `A B C` and two `B C D`. The `A B C` is helpful to know because it not only occurs as part of `A B C D` but also apart from it. In contrast, `B C D` is _only_ repeated because it forms part of the longer sequence `A B C D`.

`ngram2.py` attempts to generate a more nuanced list of n-grams based on discussions between Sophia Sklaviadis and myself.

The output of `ngram2.py` applies to `A B C D A B C A B C D` is:

```
4 2 0 | A B C D
3 3 2 | A B C
```

which should be read as following:

* the `4`-gram `A B C D` is repeated `2` times and, of those, `0` are the result of being subgrams of a 5-gram
* the `3`-gram `A B C` is repeated `3` times and, of those, `2` are the result of being subgrams of a 4-gram
* there are no repeated n-grams for any other n which aren't the result of being subgrams of n+1-grams

The heuristic developed by Sklaviadis and myself is that the n-gram will be shown iff the naïve n-gram count > 1 AND the naïve n-gram count > the count from subgrams of repeated n+1-grams.
