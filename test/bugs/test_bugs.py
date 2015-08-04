#
# txt2tags fatal errors tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# All these bugs are already fixed on the current version.
# In older releases they dump an error traceback.
#

import glob
import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))


def run():
    os.chdir(DIR)
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'
        print '  Testing %s ...' % basename,
        cmdline = lib.TXT2TAGS + [infile]
        output = lib.get_output(cmdline)
        if not output:
            os.remove(outfile)
        assert not output


if __name__ == '__main__':
    run()
