# Homer n-grams

*calculation and visualisation of repeating n-grams in Homer and beyond*


## Directories

* `data-cleanup/` contains raw source files and code for cleaning up and transforming those files into the format the tools will work best with.
* `data/` contains cleaned and transformed data ready for processing.
* `ngram-processing/` contains code for calculating the repeated n-grams in a token list


## Files

`output.txt` is the output of running `ngram2.py` on `iliad.txt`.

`iliad2.txt` and `odyssey2.txt` have line references marked. `ngram3.py` is similar to (although slower than) `ngram2.py` except it can track these references.

`output-iliad.txt` is the output of running `ngram3.py` on `iliad2.txt`.

`output-odyssey.txt` is the output of running `ngram3.py` on `odyssey2.txt`.

`output-combined.txt` is the output of running `ngram3.py` on `combined2.txt`.

`output-intersection.txt` is the lines of `output-combined.txt` with both Iliad and Odyssey references.

`iliad-lemma.txt` is the lemmatised Iliad by line.

`odyssey-lemma.txt` is the lemmatised Odyssey by line.

`output-iliad-lemma.txt` is the output of running `ngram3.py` on `iliad-lemma.txt`.

`output-odyssey-lemma.txt` is the output of running `ngram3.py` on `odyssey-lemma.txt`.
