# txt2tags http loading tester (http://txt2tags.org)

import os

import py.test

import lib


DIR = os.path.dirname(os.path.abspath(__file__))

remote_root = 'http://txt2tags.org/test/'
remote_infiles = [
    'mtime.t2t',
    'not-found.t2t',
    'relative-path.t2t',
    ]
remote_mapping = {
    'remote-outfile': 'simple.t2t',
    'stdout': 'simple.t2t',
    }


@py.test.mark.slow
def run():
    os.chdir(DIR)
    for name, target, infile, outfile, okfile, stderr in lib.get_ok_files(DIR):
        if infile in remote_infiles:
            infile = remote_root + infile
        if name in remote_mapping:
            infile = remote_root + remote_mapping[name]
        if lib.initTest(name, infile, outfile):
            cmdline = []
            cmdline.extend(['-i', infile])
            if (infile.startswith(remote_root) and
                    name != 'remote-outfile'):
                cmdline.extend(['-o', outfile])
            if name == 'not-found':
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            elif name == 'stdout':
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
            elif name == 'remote-outfile':
                cmdline.append('2>' + outfile)
            elif name == 'relative-path':
                cmdline.extend(['-t', 'html'])
                cmdline.append('--fix-path')
            lib.test(DIR, cmdline, outfile)


if __name__ == '__main__':
    run()
