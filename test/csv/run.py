#
# txt2tags %!csv command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

def run():
    # test all OK files found
    # Note: txt target is to test the table-to-verbatim mapping
    for outfile in glob.glob("ok/*"):
        stderr = 0
        basename, extension = os.path.splitext(os.path.basename(outfile))
        target = extension.lstrip('.')
        if target == 'out':
            target = 'txt'
            stderr = 1
        infile = basename + ".t2t"
        outfile = outfile.replace('ok/', '')
        if lib.initTest(basename, infile, outfile):
            cmdline = ['-H']
            cmdline.extend(['-t', target])
            cmdline.extend(['-i', infile])
            if stderr:
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            lib.test(cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)

    return lib.OK, lib.FAILED, lib.ERROR_FILES

