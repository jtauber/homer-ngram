#!/usr/bin/env python3

import re

from lxml import etree

# filename = "tlg0012.tlg001.perseus-grc1.tb.xml"
# prefix = "Il"

filename = "tlg0012.tlg002.perseus-grc1.tb.xml"
prefix = "Od"

prev_ref = None
with open(filename) as f:
    tree = etree.parse(f)
    for sentence in tree.xpath("//sentence"):
        sentence_id = sentence.attrib["id"]
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
                    if ref != prev_ref:
                        if prev_ref:
                            print()
                        print(f"{prefix}.{ref}", end=" ")
                        prev_ref = ref
                    print(lemma, end=" ")
