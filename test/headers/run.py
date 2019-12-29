#
# txt2tags headers tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# Note: The .t2t files are generated dynamicaly, based on 'tests' data.
#       Each character is expanded to a 'txt' dict text.
#

import os
import sys

sys.path.insert(0, "..")
import lib

del sys.path[0]

# text patterns to compose source files
txt = {
    "e": "",  # Empty line
    "1": "Header 1",  # Header line 1
    "2": "Header 2",  # Header line 2
    "3": "Header 3",  # Header line 3
    "c": "% comment",  # Comment line
    "k": "%%%\ncomment\n%%%",  # Comment block
    "b": "Text.",  # Body line
}

# the registered tests
tests = """
eb    ecb
1ee   1ec   1eeb   1e3b   1c3b    1ccb
12e   12eb  12cb
123   123b  123eb
1     c     1e     12
ce3b  cc3b  c2eb   c2cb   c23b
ekb   123kb ek     123k   ekkkb
"""


def run():
    for testid in tests.split():
        infile = testid + ".t2t"
        outfile = testid + ".html"
        cmdline = ["-t html -C test.conf", infile]
        if lib.initTest(testid, infile, outfile):
            # compose source file contents
            infile_txt = []
            for letter in testid:
                infile_txt.append(txt[letter])
            infile_txt = "\n".join(infile_txt)
            # create the source file
            lib.WriteFile(infile, infile_txt)
            # convert and check results
            lib.test(cmdline, outfile)
            # remove the trash
            os.remove(infile)
