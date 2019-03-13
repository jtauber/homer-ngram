#!/usr/bin/env python3

patterns = [
    f"{i:05b}".replace("0", "a").replace("1", "b") + "b"
    for i in range(32)
]


for pattern in patterns[:-1]:
    print(f"body.{pattern} li,")
pattern = patterns[-1]
print(f"body.{pattern} li")
print("{ color: #EEE; }")

for pattern in patterns[:-1]:
    print(f"body.{pattern} li.{pattern},")
pattern = patterns[-1]
print(f"body.{pattern} li.{pattern}")
print("{ color: #000; }")

for pattern in patterns[:-1]:
    print(f"body.syll-length.{pattern} li span.syll,")
pattern = patterns[-1]
print(f"body.syll-length.{pattern} li span.syll")
print("{ background-color: transparent; }")

for pattern in patterns[:-1]:
    print(f"body.syll-length.{pattern} li.{pattern} span.syll.long,")
pattern = patterns[-1]
print(f"body.syll-length.{pattern} li.{pattern} span.syll.long")
print("{ background-color: #CCC; }")

for pattern in patterns[:-1]:
    print(f"body.syll-length.{pattern} li.{pattern} span.syll:not(.long),")
pattern = patterns[-1]
print(f"body.syll-length.{pattern} li.{pattern} span.syll:not(.long)")
print("{ background-color: #EEE; }")
