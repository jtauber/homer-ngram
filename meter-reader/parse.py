#!/usr/bin/env python3

import csv


def pad_list(lst, n):
    # pads the given list to be exactly length n (truncating or adding None)
    return (lst + [None] * n)[:n]


START_LINE = 0
def lines(filename):
    with open(filename, newline="") as f:
        book_reader = csv.reader(f)
        book_reader.__next__()  # skip first line
        prev_line = START_LINE
        for row in book_reader:
            line, text, length, word, foot, half_line, speaker, newpara, speech, extra = pad_list(row, 10)

            line = int(line)
            if line != prev_line:
                # new line

                if prev_line > START_LINE:
                    if line_data[-1]["length"] == "long":
                        foot_code += "b"
                    else:
                        foot_code += "a"

                    if line_data[-1]["word_pos"] == "c":
                        line_data[-1]["word_pos"] = "l"
                    else:
                        line_data[-1]["word_pos"] = None

                    yield (prev_line, foot_code, line_data)

                assert line == prev_line + 1

                prev_word = 0
                prev_foot = 0
                prev_half_line = 0

                line_data = []
                foot_code = ""

            assert length in ["long", "short"]

            word = int(word)
            if word != prev_word:
                # new word
                assert word == prev_word + 1
                word_pos = "r"
                if word > 1:
                    if line_data[-1]["word_pos"] == "c":
                        line_data[-1]["word_pos"] = "l"
                    else:
                        line_data[-1]["word_pos"] = None
            else:
                word_pos = "c"

            foot = int(foot)
            if foot != prev_foot:
                assert foot == prev_foot + 1
                if foot > 1:
                    if line_data[-1]["length"] == "long":
                        foot_code += "b"
                    else:
                        foot_code += "a"

            half_line = {"hemi1": 1, "hemi2": 2}[half_line]
            caesura = False
            if half_line != prev_half_line:
                assert half_line == prev_half_line + 1
                if half_line == 2:
                    caesura = True

            assert speaker in ["", "Achilles", "Agamemnon", "Nestor", "Thetis", "Zeus", "Hephaistos", "Hera", "Chryses", "Kalchas", "Athena", "Odysseus"]
            assert newpara in [None, "newpara"]
            assert speech in [None, "speech"]
            assert extra in [None, "Chryses"]  # what is this?

            line_data.append({
                "text": text,
                "length": length,
                "word_pos": word_pos,
                "caesura": caesura,
            })

            prev_line = line
            prev_word = word
            prev_foot = foot
            prev_half_line = half_line

        if line_data[-1]["word_pos"] == "c":
            line_data[-1]["word_pos"] = "l"
        else:
            line_data[-1]["word_pos"] = None

        if line_data[-1]["length"] == "long":
            foot_code += "b"
        else:
            foot_code += "a"
        yield (line, foot_code, line_data)


print("""<!DOCTYPE html>
<html>
  <head>
    <title>Iliad Book 1</title>
    <meta charset="utf-8">
    <link href="style.css" rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <h1>Iliad Book 1</h1>
      <p>Designed and developed by <a href="https://jktauber.com/">James Tauber</a> and Sophia Sklaviadis.<br>
      Scansion data © 2016, 2017 <a href="http://hypotactic.com">David Chamberlain</a> licensed as CC-BY.</p>
      <div class="toggles">
        <h2>Toggles</h2>
        <div class="toggle" data-target="foot-syll"><span class="foot-syll">&#x25CF;</span>&nbsp;show foot and syllable divisions</div>
        <div class="toggle" data-target="syll-length"><span class="syll-length">&#x25CF;</span>&nbsp;show syllable length</div>
        <div class="toggle" data-target="align-feet"><span class="align-feet">&#x25CF;</span>&nbsp;align feet and syllables</div>
        <div class="toggle" data-target="hide-words"><span class="hide-words">&#x25CF;</span>&nbsp;hide-words</div>
      </div>
      <p>Hover over a line to see other lines with same metrical pattern.</p>

      <ol class="verse">""")

for line_num, foot_code, line_data in lines("iliad1.csv"):
    print(f'        <li class="line {foot_code}" id="line-{line_num}" data-meter="{foot_code}">')
    print(f'          <div>', end="")
    index = 0
    for foot in foot_code:
        if foot == "a":
            syllables = line_data[index:index+3]
            index += 3
        else:
            syllables = line_data[index:index+2]
            index += 2
        if syllables[0]["word_pos"] in [None, "r"]:
            print("\n            ", end="")
        print(f'<span class="foot">', end="")
        for i, syllable in enumerate(syllables):
            if i > 0 and syllable["word_pos"] in [None, "r"]:
                print("\n            ", end="")
            syll_classes = ["syll"]
            if syllable["length"] == "long":
                syll_classes.append("long")
            if syllable["caesura"]:
                syll_classes.append("caesura")
            if syllable["word_pos"] is not None:
                syll_classes.append(syllable["word_pos"])
            syll_class_string = " ".join(syll_classes)
            print(f'<span class="{syll_class_string}">{syllable["text"]}</span>', end="")
        print(f'</span>', end="")
    print(f'\n          </div>')
    print(f'        </li>')

print("""      </ol>
    </div>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
      $(function() {
        $(".toggle").on("click", function() {
          $("body").toggleClass($(this).data("target"));
          return false;
        });
        $(".line").hover(function() {
          $("body").addClass($(this).data("meter"));
          return false;
        }, function() {
          $("body").removeClass($(this).data("meter"));
        });
      });
    </script>
  </body>
</html>""")
