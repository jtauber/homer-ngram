#!/usr/bin/env python3

"""
Converts a TEI/EpiDoc file into the "ref token1 token2 token3" format used by
other tools in this repo.

To use, change the FILENAME, SUBTYPE and PREFIX.
"""


import re

from lxml import etree


# SUBTYPE is specified due to the inconsistent subtype naming between the
# Iliad and Odyssey files

# FILENAME = "iliad.xml"
# SUBTYPE = "Book"
# PREFIX = "Il"

FILENAME = "odyssey.xml"
SUBTYPE = "book"
PREFIX = "Od"


ns = {"TEI": "http://www.tei-c.org/ns/1.0"}
with open(FILENAME) as f:
    tree = etree.parse(f)
    for book in tree.xpath(f"//TEI:div[@subtype='{SUBTYPE}']", namespaces=ns):
        book_num = book.attrib["n"]
        for line in book.xpath(".//TEI:l", namespaces=ns):
            line_num = line.attrib["n"]
            text = re.sub(r"\s+", " ", line.xpath("string()").strip())
            print(f"{PREFIX}.{book_num}.{line_num} {text}")
