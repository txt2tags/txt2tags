# txt2tags-as-module tester (http://txt2tags.org)
#
# Checks whether both scripts that use txt2tags as a module return 0.

import os.path
import subprocess

import lib


SCRIPTS_DIR = os.path.join(lib.REPO, 'samples', 'module')
SCRIPTS = ['module-full.py', 'module-body.py']


def run():
    for script in SCRIPTS:
        print 'Testing %s ...' % script,
        retcode = subprocess.call(['python', script], cwd=SCRIPTS_DIR)
        assert retcode == 0


if __name__ == '__main__':
    run()
