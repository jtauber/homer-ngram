# Homer n-grams

`iliad.txt` comes from https://scaife.perseus.org/library/passage/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1-24/text/

One problem with naïve n-gram generation for multiple n (like `ngram.py` does) is that all the subgrams of a repeated n-gram will show up as well and this generally not what is wanted.

For example, the string `A B C D A B C A B C D` has a repeated 4-gram `A B C D`. Naïve generation of 3-grams gives three `A B C` and two `B C D`. The `A B C` is helpful to know because it not only occurs as part of `A B C D` but also apart of it. In contrast, `B C D` is _only_ repeated because it forms part of the longer sequence `A B C D`.

`ngram2.py` attempts to generate a more nuanced list of n-grams based on discussions between Sophia Sklaviadis and myself.

The output of `ngram2.py` applies to `A B C D A B C A B C D` is:

```
5
4
    2 0 | A B C D
3
    3 2 | A B C
2
```

which should be read as following:

* there are no repeated `5`-grams
* the `4`-gram `A B C D` is repeated `2` times and, of those, `0` are the result of being subgrams of a 5-gram
* the `3`-gram `A B C` is repeated `3` times and, of those, `2` are the result of being subgrams of a 4-gram
* there are no repeated `2`-grams that are not merely subgrams of the repeated 3-grams

The heuristic developed by Sklaviadis and myself is that the n-gram will be shown iff the naïve n-gram count > 1 AND the naïve n-gram count > the count from subgrams of repeated n+1-grams.

`output.txt` is the output of running `ngram2.py` on `iliad.txt`.
