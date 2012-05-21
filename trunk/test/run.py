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

import os, sys
import lib

MODULES = 'headers marks options nesting crossing gotchas bugs include csv includeconf macro target module'.split()
MODULES.append('http')  # should always be the last, requires internet connection
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
TOTAL_OK = TOTAL_FAILED = 0
ERRORS = []

if len(sys.argv) > 1:
    MODULES = sys.argv[1:]

# Show which version is being tested
os.system(lib.TXT2TAGS + " -V")
print
print 'Base command used for all tests:\n  ' + lib.TXT2TAGS
print

for module in MODULES:
    print 'Entering on module', module

    # loading test module
    os.chdir(SCRIPT_DIR)
    sys.path.insert(0, module)
    import run

    # do what you have to do
    if not os.path.isdir(module):
        print 'ERROR: Invalid module %s' % module
        sys.exit()
    os.chdir(module)
    ok, failed, errors = run.run()

    # update count
    TOTAL_OK = TOTAL_OK + ok
    TOTAL_FAILED = TOTAL_FAILED + failed
    for err in errors:
        ERRORS.append(os.path.join(module, lib.DIR_ERROR, err))

    # cleaning the house
    del sys.path[0]
    del run
    del sys.modules['run']

# show report at the end
if TOTAL_FAILED:
    stats = "%d ok / %d failed" % (TOTAL_OK, TOTAL_FAILED)
else:
    stats = "100% ok"
print
print "Totals: %d tests (%s)" % (TOTAL_OK + TOTAL_FAILED, stats)

if ERRORS:
    print
    print "Check out the files with errors:"
    print '\n'.join(ERRORS)
    sys.exit(1)

if len(sys.argv) == 1:
    print
    print "Don't forget to run the extra tests:"
    print 'sample/run.sh'
    print 'art/run.sh'
    print 'path/run.sh'
    print 'outfile/run.sh'
