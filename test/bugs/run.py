#
# txt2tags fatal errors tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# All these bugs are already fixed on the current version.
# In older releases they dump an ugly Error Traceback.
#
# I think popen() don't work in some Windows, so these tests
# may not work on it.
#

import os, sys, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

def syscommand(cmd):
    fd = os.popen(cmd)
    output = []
    for line in fd.readlines():
        output.append(line.rstrip()) # stripping \s*\n
    ret = fd.close()
    if ret: ret = ret/256  # 16bit number
    return ret, output

def run():
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'
        print '  Testing %s ...' % basename,
        cmdline = lib.TXT2TAGS + ' ' + infile
        code, output = syscommand(cmdline)
        if not output:
            print "OK"
            lib.OK = lib.OK + 1
            os.remove(outfile)
        else:
            print "FAILED"
            lib.FAILED = lib.FAILED + 1
            continue
        cmdline = lib.TXT2TAGSLITE + ' ' + infile
        code, output = syscommand(cmdline)
        if not output:
            print "OK"
            lib.OK = lib.OK + 1
            os.remove(outfile)
        else:
            print "FAILED"
            lib.FAILED = lib.FAILED + 1
            continue
    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
