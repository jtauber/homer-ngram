#!/usr/bin/env python3

from lxml import etree

with open("iliad.xml") as f:
    tree = etree.parse(f)
    for book in tree.xpath("//TEI:div[@subtype='Book']", namespaces={"TEI": "http://www.tei-c.org/ns/1.0"}):
        book_num = book.attrib["n"]
        for line in book.xpath(".//TEI:l", namespaces={"TEI": "http://www.tei-c.org/ns/1.0"}):
            line_num = line.attrib["n"]
            text = line.xpath("string()").strip()
            print(f"{book_num}.{line_num} {text}")
