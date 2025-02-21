#!python
import argparse
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

parser = argparse.ArgumentParser()
parser.add_argument("pattern")
# nargs: either 0 or 1 of this positional argument present, makes it optional
parser.add_argument("file", nargs="?", default=None)
# store_true - treats the opt as True/False based on present/absent only (just -i, not -i=True etc)
parser.add_argument("-i", "--ignore-case", action="store_true")

args = parser.parse_args()

@contextmanager
def line_reader(filepath: Optional[Path] = None):
    if filepath:
        if (not filepath.exists()) or (not filepath.is_file()):
            raise ValueError(f"Invalid filepath: {filepath}")
        with filepath.open("r") as f:
            yield f
    else:
        yield sys.stdin

try:
    if args.file:
        filepath = Path(args.file)
        lines_context = line_reader(filepath=filepath)
    else:
        lines_context = line_reader()

    with lines_context as lines:
        for line in lines.readlines():
            needle, haystack = (
                (args.pattern.lower(), line.lower())
                if args.ignore_case
                else (args.pattern, line)
            )
            if needle in haystack:
                print(line, end="")
except ValueError as e:
    print(e, file=sys.stderr)