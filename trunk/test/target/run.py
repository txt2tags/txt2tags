#
# txt2tags target code tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, re, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

all_targets = 'adoc art bbcode creole dbk doku gwiki html html5 lout man md mgp moin pm6 pmw red rtf sgml spip tex txt wiki xhtml xhtmls'.split()

tableable = 'art creole doku gwiki html html5 man md moin pmw red rtf sgml spip tex wiki xhtml xhtmls'.split()

def run():
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        
        # Choose targets
        targets = all_targets
        if basename == 'table':
            targets = tableable
        
        for target in targets:
            outfile = basename + '.' + target
            testname = '%s in %s' % (basename, target)
            if lib.initTest(testname, infile, outfile):
                cmdline = []
                cmdline.extend(['-i', infile])
                cmdline.extend(['-t', target])
                lib.convert(cmdline)
                lib.diff(outfile)
    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
