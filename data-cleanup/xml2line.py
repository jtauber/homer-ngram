#!/usr/bin/env python3

import re

from lxml import etree

# filename = "iliad.xml"
# subtype = "Book"
# prefix = "Il"

filename = "odyssey.xml"
subtype = "book"
prefix = "Od"

with open(filename) as f:
    tree = etree.parse(f)
    for book in tree.xpath(f"//TEI:div[@subtype='{subtype}']", namespaces={"TEI": "http://www.tei-c.org/ns/1.0"}):
        book_num = book.attrib["n"]
        for line in book.xpath(".//TEI:l", namespaces={"TEI": "http://www.tei-c.org/ns/1.0"}):
            line_num = line.attrib["n"]
            text = re.sub("\s+", " ", line.xpath("string()").strip())
            print(f"{prefix}.{book_num}.{line_num} {text}")
