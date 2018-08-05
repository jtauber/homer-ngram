# Homer n-grams

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

## Files

`iliad.txt` comes from https://scaife.perseus.org/library/passage/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1-24/text/
`iliad.xml` comes from https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml
`iliad2.txt` is the result of running `xml2line.py` (on `iliad.xml`)

`odyssey.xml` comes from https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml
`odyssey2.txt` is the result of running `xml2line.py` (on `odyssey.xml`)

`combined2.txt` is just the concatenation of `iliad2.txt` and `odyssey2.txt`.

`output.txt` is the output of running `ngram2.py` on `iliad.txt`.

`iliad2.txt` and `odyssey2.txt` have line references marked. `ngram3.py` is similar to (although slower than) `ngram2.py` except it can track these references.


`output-iliad.txt` is the output of running `ngram3.py` on `iliad2.txt`.

`output-odyssey.txt` is the output of running `ngram3.py` on `odyssey2.txt`.

`output-combined.txt` is the output of running `ngram3.py` on `combined2.txt`.

`output-intersection.txt` is the lines of `output-combined.txt` with both Iliad and Odyssey references.
