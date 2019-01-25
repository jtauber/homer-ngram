#!/usr/bin/env python3

"""
Converts a treebank XML file into the "ref token1 token2 token3" format used by
other tools in this repo.

To use, change the FILENAME and PREFIX.
"""


from lxml import etree


# FILENAME = "tlg0012.tlg001.perseus-grc1.tb.xml"
# PREFIX = "Il"

FILENAME = "tlg0012.tlg002.perseus-grc1.tb.xml"
PREFIX = "Od"


prev_ref = None
with open(FILENAME) as f:
    tree = etree.parse(f)
    for sentence in tree.xpath("//sentence"):
        sentence_id = sentence.attrib["id"]
        print(sentence_id, end="\t")
        subdoc = sentence.attrib["subdoc"]
        for word in sentence.xpath("word"):
            if "cite" in word.attrib:
                word_id = word.attrib["id"]
                form = word.attrib["form"]
                lemma = word.attrib["lemma"]
                postag = word.attrib["postag"]
                head = word.attrib["head"]
                relation = word.attrib["relation"]
                cite = word.attrib["cite"]
                ref = cite.split(":")[-1]
                if ref:
                    print(lemma, end=" ")
        print()
