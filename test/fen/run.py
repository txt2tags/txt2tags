#
# txt2tags %!fen command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, re, glob

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
        basename = re.sub('\..*?$', '', outfile.replace('ok/', ''))
        target = re.sub('.*\.', '', outfile)
        outfilelite = basename + '.' + (lib.EXTENSION.get(target) or target)
        if target == 'out':
            target = 'txt'
            stderr = 1
        infile = basename + ".t2t"
        outfile = outfile.replace('ok/', '')

        if lib.initTest(basename, infile, outfile):
            cmdline = ['-t', target]
            cmdline.extend(['-i', infile])
            if stderr:
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            lib.convert(cmdline)
            lib.diff(outfile)
            lib.convert(cmdline, True)
            lib.diff(outfilelite, os.path.join(lib.DIR_OK, outfile))
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)
    
    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
