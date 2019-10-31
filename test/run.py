#!/usr/bin/env python
#
# txt2tags test-suite (http://txt2tags.org)
# See also: lib.py, */run.py
#
# Just run this file without parameters at it will perform
# all the tests. At the end a report will be printed, and
# if any error is found, the program will tell you.
#
# Inside each test module (the subdirs) there is a run.py
# script, that will make the tests. The expected results
# are on the module's "ok" subdir. If any error is found,
# it will be stored on the "error" subdir.
#
# TIP: To quickly check the errors, run:
#      for f in */error/*; do diff -u ${f/error/ok} $f; done

from __future__ import print_function

import os.path
import sys

import lib

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

PYTHON_TEST_MODULES = []
BASH_TEST_MODULES = []
for path in sorted(os.listdir(DIR)):
    if path.startswith("__") or not os.path.isdir(path):
        continue
    if os.path.exists(os.path.join(path, "run.py")):
        PYTHON_TEST_MODULES.append(path)
    elif os.path.exists(os.path.join(path, "run.sh")):
        BASH_TEST_MODULES.append(path)
    else:
        sys.exit("test module %s contains neither run.py nor run.sh" % path)

TOTAL_OK = TOTAL_FAILED = 0
ERRORS = []

if len(sys.argv) > 1:
    PYTHON_TEST_MODULES = sorted(set(sys.argv[1:]) & set(PYTHON_TEST_MODULES))
    BASH_TEST_MODULES = sorted(set(sys.argv[1:]) & set(BASH_TEST_MODULES))

# Show which version is being tested
print("Testing txt2tags version", lib.get_output(lib.TXT2TAGS + ["-V"]))
print()
print("Base commands used for all tests:")
print(lib.TXT2TAGS)
print()

for module in PYTHON_TEST_MODULES:
    os.chdir(DIR)

    print("Entering module", module)
    if not os.path.isdir(module):
        sys.exit("ERROR: Invalid module %s" % module)

    # load test module
    sys.path.insert(0, module)
    import run

    os.chdir(module)
    ok, failed, errors = run.run()

    # update count
    TOTAL_OK += ok
    TOTAL_FAILED += failed
    for err in errors:
        ERRORS.append(os.path.join(module, lib.DIR_ERROR, err))

    # cleanup
    del sys.path[0]
    del run
    del sys.modules["run"]

# show report at the end
if TOTAL_FAILED:
    stats = "%d ok / %d failed" % (TOTAL_OK, TOTAL_FAILED)
else:
    stats = "100% ok"
print()
print("Totals: %d tests (%s)" % (TOTAL_OK + TOTAL_FAILED, stats))

if ERRORS:
    print()
    print("Check out the files with errors:")
    print("\n".join(ERRORS))
    sys.exit(1)

if BASH_TEST_MODULES:
    print()
    print("Don't forget to run the extra tests:")
    for module in BASH_TEST_MODULES:
        print("%s/run.sh" % module)
