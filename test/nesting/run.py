#
# txt2tags nesting marks tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

# left files are generated from right ones (using smart filters)
ALIASES = {
    'numlist' : 'list',
    'deflist' : 'list',
}

# smart filters to allow source inheritance and macros normalization
FILTERS = {
    'deflist' : [ ('pre', '^-( |$)', r':\1') ],
    'numlist' : [ ('pre', '^-( |$)', r'+\1') ],
}

# convert FILTERS tuples to txt2tags pre/postproc rules
def addFilters(filters):
    if not filters: return []
    config = []
    cmdline = []
    for filter in filters:
        config.append("%%!%sproc: '%s' '%s'"%filter)
    if config:
        lib.WriteFile(lib.CONFIG_FILE, '\n'.join(config))
        cmdline = ['-C', lib.CONFIG_FILE]
    return cmdline

def run():
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'
        if lib.initTest(basename, infile, outfile):
            cmdline = [infile]
            lib.test(cmdline, outfile)
    # using smart filters, same files generate more than one output
    for alias in ALIASES.keys():
        infile = ALIASES[alias] + '.t2t'
        outfile = alias + '.html'
        if lib.initTest(alias, infile, outfile):
            cmdline = addFilters(FILTERS.get(alias))
            cmdline.append('-H')
            cmdline.extend(['-o', outfile, infile])
            lib.test(cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)

    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
