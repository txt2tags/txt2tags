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


def run():
    ok = failed = 0
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace(".t2t", "")
        outfile = basename + ".html"
        print("  Testing %s ..." % basename, end=" ")
        cmdline = lib.TXT2TAGS + [infile]
        output = lib.get_output(cmdline)
        if not output:
            print("OK")
            ok += 1
            os.remove(outfile)
        else:
            print("FAILED")
            failed += 1
            continue
    return ok, failed, []
