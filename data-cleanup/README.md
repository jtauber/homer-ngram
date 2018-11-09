# Raw Files and Data Cleanup

*raw source files and code for cleaning up and transforming those files into the format the tools will work best with*


## Raw File Sources

* `iliad.txt` comes from https://scaife.perseus.org/library/passage/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1-24/text/
* `iliad.xml` comes from https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml
* `odyssey.xml` comes from https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml
* `tlg0012.tlg001.perseus-grc1.tb.xml` and `tlg0012.tlg002.perseus-grc1.tb.xml` come from https://github.com/PerseusDL/treebank_data/tree/master/v2.1/Greek


## Python Scripts

* `xml2line.py` converts the TEI/EpiDoc XML from Perseus into a line-based format.
* `tb2line.py` converts the Treebank XML into a line based format.
