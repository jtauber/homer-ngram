# Homer n-grams

*calculation and visualisation of repeating n-grams in Homer and beyond*


## Directories

* `data-cleanup/` contains raw source files and code for cleaning up and transforming those files into the format the tools will work best with.
* `data/` contains cleaned and transformed data ready for processing.
* `ngram-processing/` contains code for calculating the repeated n-grams in a token list
* `ngram-data/` contains the results of running various n-gram scripts on the data


## Files

`iliad-lemma.txt` is the lemmatised Iliad by line.

`odyssey-lemma.txt` is the lemmatised Odyssey by line.

`output-iliad-lemma.txt` is the output of running `ngram3.py` on `iliad-lemma.txt`.

`output-odyssey-lemma.txt` is the output of running `ngram3.py` on `odyssey-lemma.txt`.
