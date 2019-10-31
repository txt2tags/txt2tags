#
# txt2tags fatal errors tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# All these bugs are already fixed on the current version.
# In older releases they dump an ugly Error Traceback.
#

from __future__ import print_function

import glob
import os
import sys

sys.path.insert(0, "..")
import lib

del sys.path[0]

lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []


def run():
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace(".t2t", "")
        outfile = basename + ".html"
        print("  Testing %s ..." % basename, end=" ")
        cmdline = lib.TXT2TAGS + [infile]
        output = lib.get_output(cmdline)
        if not output:
            print("OK")
            lib.OK += 1
            os.remove(outfile)
        else:
            print("FAILED")
            lib.FAILED += 1
            continue
    return lib.OK, lib.FAILED, lib.ERROR_FILES
