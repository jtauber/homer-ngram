import collections

from flask import Flask
from flask import abort, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


ILIAD = "urn:cts:greekLit:tlg0012.tlg001.perseus-grc2"
ODYSSEY = "urn:cts:greekLit:tlg0012.tlg002.perseus-grc2"


# maps a CTS URN for an edition to a list of lines
# e.g. LINES[ILIAD][1000] will store the 1000th line of the Iliad or,
#   actually, (ref, line)
LINES = collections.defaultdict(list)

# maps a CTS URN for an edition to a list of lines per book
# e.g. BOOK_LENGTH[ODYSSEY][5] will store the number of lines in Odyssey Book 5
BOOK_LENGTH = collections.defaultdict(lambda: collections.defaultdict(int))

# maps a CTS URN for an edition to a dictionary that maps book.line references
#   to an index into LINES[CTS_URN]
# e.g. REF_INDEX[ILIAD["2.389"]] = 1000 because 2.389 is
#   LINES[ILIAD][1000]
REF_INDEX = collections.defaultdict(dict)


def load(filename, work_urn):
    with open(filename) as f:
        for line in f:
            ref, tokens = line.strip().split(maxsplit=1)
            work, passage_ref = ref.split(".", maxsplit=1)
            REF_INDEX[work_urn][passage_ref] = len(LINES[work_urn])
            LINES[work_urn].append((ref.split(".", maxsplit=1)[1], tokens))
            book = passage_ref.split(".")[0]
            BOOK_LENGTH[work_urn][book] += 1

load("../data/iliad2.txt", ILIAD)
load("../data/odyssey2.txt", ODYSSEY)


# get lines given CTS URN
def get_lines(urn):
    if ":" in urn:
        edition, reference = urn.rsplit(":", maxsplit=1)
        if edition in REF_INDEX:
            if "-" in reference:
                start_ref, end_ref = reference.split("-")
                start_index = REF_INDEX.get(edition, {}).get(start_ref)
                end_index = REF_INDEX.get(edition, {}).get(end_ref)
            else:
                start_index = REF_INDEX.get(edition, {}).get(reference)
                end_index = start_index

            if start_index is not None and end_index is not None:
                return LINES.get(edition)[start_index:end_index+1]


# serves everything up
@app.route("/<urn>/")
def text(urn):
    lines = get_lines(urn)
    if lines:
        return jsonify(lines)
    else:
        abort(404)
