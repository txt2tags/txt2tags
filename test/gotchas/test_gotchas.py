# txt2tags marks gotchas tester (http://txt2tags.org)

import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))


def run():
    os.chdir(DIR)
    for name, target, infile, outfile, okfile, stderr in lib.get_ok_files(DIR):
        if lib.initTest(name, infile, outfile):
            cmdline = ['-H']
            cmdline.extend(['-t', target])
            cmdline.append(infile)
            lib.test(DIR, cmdline, outfile)


if __name__ == '__main__':
    run()
