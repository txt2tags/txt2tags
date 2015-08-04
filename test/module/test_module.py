#
# txt2tags-as-module tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#
# Checks whether both scripts that use txt2tags as a module return 0.
#

import os.path
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.dirname(DIR)
sys.path.insert(0, TEST_DIR)
import lib

os.chdir(DIR)

SCRIPTS_DIR = os.path.join(lib.REPO, 'samples', 'module')
SCRIPTS = ['module-full.py', 'module-body.py']

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

def run():
    for script in SCRIPTS:
        print '  Testing %s ...' % script,
        retcode = subprocess.call(['python', script], cwd=SCRIPTS_DIR,
                                  stdout=subprocess.PIPE)
        assert retcode == 0

    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
