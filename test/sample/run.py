from __future__ import print_function

import os.path
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(DIR))

sys.path.insert(0, "..")
import lib

del sys.path[0]

sys.path.insert(0, REPO)
import txt2tags

del sys.path[0]


def run():
    infile = os.path.join(REPO, "samples", "sample.t2t")
    for target in txt2tags.TARGETS:
        outfile = "sample." + target
        cmdline = ["-t", target, "-o", outfile, infile]
        okfile = os.path.join(REPO, "samples", outfile)
        print(" ", target, end=" ")
        lib.test(cmdline, outfile, okfile=okfile)
