# txt2tags %!csv command tester (http://txt2tags.org)

import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))


def run():
    os.chdir(DIR)
    for name, target, infile, outfile, okfile, stderr in lib.get_ok_files(DIR):
        if lib.initTest(name, infile, outfile):
            cmdline = ['-H']
            cmdline.extend(['-t', target])
            cmdline.extend(['-i', infile])
            if stderr:
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            lib.test(DIR, cmdline, outfile, okfile=okfile)


if __name__ == '__main__':
    run()
