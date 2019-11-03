#
# txt2tags %!include command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import glob
import os
import re
import sys

sys.path.insert(0, "..")
import lib

del sys.path[0]


def run():
    # test all OK files found
    for outfile in glob.glob("ok/*"):
        stderr = 0
        basename = re.sub(r"\..*?$", "", outfile.replace("ok/", ""))
        target = re.sub(r".*\.", "", outfile)
        if target == "out":
            target = "txt"
            stderr = 1
        infile = basename + ".t2t"
        outfile = outfile.replace("ok/", "")
        if lib.initTest(basename, infile, outfile):
            cmdline = ["-H"]
            cmdline.extend(["-t", target])
            cmdline.extend(["-i", infile])
            if stderr:
                cmdline.extend(["-o", "-"])
                cmdline.append(">" + outfile)
                cmdline.append("2>&1")
            lib.test(cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)
