#!/usr/bin/env python3

print("var ngrams = [")

with open("output-iliad4.txt") as f:
    gram_num = 0
    for line in f:
        gram_num += 1
        counts, refs, words = line.strip().split(" | ")
        n, _, _ = counts.split()
        refs = refs.split()
        for ref in refs:
            start_ref, end_ref = ref.split("-")
            start_book = start_ref.split(".")[1]
            start_line = start_ref.split(".")[2].split(":")[0]
            start_word = int(start_ref.split(":")[1].split("/")[0])
            start_length = int(start_ref.split(":")[1].split("/")[1])
            start_offset = str(int(1000 * start_word / start_length))
            end_book = end_ref.split(".")[1]
            end_line = end_ref.split(".")[2].split(":")[0]
            end_word = int(end_ref.split(":")[1].split("/")[0])
            end_length = int(end_ref.split(":")[1].split("/")[1])
            end_offset = str(int(1000 * (end_word + 1) / end_length))
            print("  [" + ", ".join([str(gram_num), str(n), start_book, start_line, start_offset, end_book, end_line, end_offset]) + "],")

print("];")
