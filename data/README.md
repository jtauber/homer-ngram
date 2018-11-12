# Data

*cleaned and transformed data ready for processing*

## File Formats

In most of these files, the first (white-space delimited) token on each line is a reference for the sequence of tokens the make up the rest of the line.

For example

```
Il.1.1 μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος
```

is simplying saying that `Il.1.1` is made up of the tokens `["μῆνιν", "ἄειδε", "θεὰ", "Πηληϊάδεω", "Ἀχιλῆος"]`.

In principle, these tokens may not be words, they could be lemmas, part-of-speech tags, metrical patterns or anything we want to do a repeated-ngram analysis of.


## Files

* `test*.txt` are just very short test input files
* `iliad2.txt` is the result of running `data-cleanup/xml2line.py` on `data-cleanup/iliad.xml`
* `odyssey2.txt` is the result of running `data-cleanup/xml2line.py` on `data-cleanup/odyssey.xml`
* `combined2.txt` is just the concatenation of `iliad2.txt` and `odyssey2.txt`.
* `iliad-lemma.txt` is the lemmatised Iliad by line.
* `odyssey-lemma.txt` is the lemmatised Odyssey by line.
