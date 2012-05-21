#
# txt2tags-as-module tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# Checks whether both scripts that use txt2tags as a module return 0.
#

import os
import shutil
import subprocess
import sys

FILE = os.path.abspath(__file__)
MODULE_TEST_DIR = os.path.abspath(os.path.join(FILE, '..'))
REPO = os.path.abspath(os.path.join(MODULE_TEST_DIR, '..', '..'))
TXT2TAGS = os.path.join(REPO, 'txt2tags')

SCRIPTS_DIR = os.path.join(REPO, 'samples', 'module')
SCRIPTS = ['module-full.py', 'module-body.py']
REQUIREMENTS = [(TXT2TAGS, 'txt2tags.py')] + [(os.path.join(SCRIPTS_DIR, script), script)
                                              for script in SCRIPTS]

# Copy all required files into this directory.
for src, dst in REQUIREMENTS:
    shutil.copy2(src, os.path.join(MODULE_TEST_DIR, dst))

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

def run():
    for script in SCRIPTS:
        print '  Testing %s ...' % script,
        retcode = subprocess.call(['python', script], cwd=MODULE_TEST_DIR,
                                  stdout=subprocess.PIPE)
        if retcode == 0:
            lib.OK += 1
            print 'OK'
        else:
            lib.FAILED += 1
            print 'FAILED'

    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
