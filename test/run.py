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

import argparse
import os.path
import sys

import lib


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("modules", nargs="*")
    parser.add_argument("--override", action="store_true", help="override test files")
    return parser.parse_args()


DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

MODULES = []
for path in sorted(os.listdir(DIR)):
    if path.startswith("__") or not os.path.isdir(path):
        continue
    if os.path.exists(os.path.join(path, "run.py")):
        MODULES.append(path)
    else:
        sys.exit("test module %s does not contain run.py file" % path)

ARGS = parse_args()
lib.OVERRIDE = ARGS.override

if ARGS.modules:
    MODULES = sorted(set(ARGS.modules) & set(MODULES))

# Show which version is being tested
print("Testing txt2tags version", lib.get_output(lib.TXT2TAGS + ["-V"]))
print()
print("Base commands used for all tests:")
print(lib.TXT2TAGS)
print()

for module in MODULES:
    os.chdir(DIR)

    print("Entering module", module)
    if not os.path.isdir(module):
        sys.exit("ERROR: Invalid module %s" % module)

    # load test module
    sys.path.insert(0, module)
    import run

    os.chdir(module)
    run.run()

    # cleanup
    del sys.path[0]
    del run
    del sys.modules["run"]

# show report at the end
if lib.FAILED:
    stats = "%d ok / %d failed" % (lib.OK, lib.FAILED)
else:
    stats = "100% ok"
print()
print("Totals: %d tests (%s)" % (lib.OK + lib.FAILED, stats))

if lib.ERROR_FILES:
    print()
    print("Check out the files with errors:")
    print("\n".join(lib.ERROR_FILES))
    sys.exit(1)
