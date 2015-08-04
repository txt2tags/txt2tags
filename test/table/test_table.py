# txt2tags target code tester (http://txt2tags.org)

import glob
import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))


all_targets = 'aap aapw aas aasw aat aatw adoc bbcode creole dbk doku gwiki html html5 htmls lout man md mgp moin pm6 pmw csv csvs ods red rst rtf sgml spip tex texs txt txt2t wiki xhtml xhtmls'.split()

tableable = 'aat aatw aas aasw aap aapw creole doku gwiki html html5 htmls lout man md moin pmw csv csvs ods red rst rtf sgml spip tex texs wiki xhtml xhtmls'.split()


def run():
    os.chdir(DIR)
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')

        targets = tableable if basename == 'table' else all_targets

        for target in targets:
            outfile = basename + '.' + target
            testname = '%s in %s' % (basename, target)
            if lib.initTest(testname, infile, outfile):
                cmdline = []
                cmdline.extend(['-i', infile])
                cmdline.extend(['-t', target])
                if target == 'aap':
                    cmdline.extend(['--width', '80'])
                lib.test(DIR, cmdline, outfile)


if __name__ == '__main__':
    run()
