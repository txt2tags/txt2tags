#
# txt2tags %!fen command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, re, glob

import lib


def run():
    # test all OK files found
    # Note: txt target is to test the table-to-verbatim mapping
    for outfile in glob.glob("ok/*"):
        stderr = 0
        basename = re.sub('\..*?$', '', outfile.replace('ok/', ''))
        target = re.sub('.*\.', '', outfile)
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


if __name__ == '__main__':
    run()
