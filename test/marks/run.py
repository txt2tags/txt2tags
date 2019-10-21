#
# txt2tags marks parsing tester (http://txt2tags.org)
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
    'numtitle': 'title',
    'raw'     : 'verbatim',
    'tagged'  : 'verbatim',
}

# smart filters to allow source inheritance
FILTERS = {
    'deflist' : [ ('pre', 'hyphen'  , 'colon' ), ('pre', '^( *)-', r'\1:') ],
    'numlist' : [ ('pre', 'hyphen'  , 'plus'  ), ('pre', '^( *)-', r'\1+') ],
    'numtitle': [ ('pre', 'equal'   , 'plus'  ), ('pre', '='     ,  '+'  ) ],
    'raw'     : [ ('pre', 'verbatim', 'raw'   ), ('pre', '`'     ,  '"'  ) ],
    'tagged'  : [ ('pre', 'verbatim', 'tagged'), ('pre', '`'     ,  "\'" ) ],
    'macro'   : [ ('post', os.path.abspath(""), '@DIRNAME@'),
                ('post', lib.getFileMtime('marks/macro.t2t'), '@MTIME@'),
                ('post', lib.getCurrentDate(), '@DATE@'),
                ('post', '^(Date.*)@MTIME@', r'\1@DATE@'),
                ('post', '^(Date.*)@MTIME@', r'\1@DATE@') ],
}

# convert FILTERS tuples to txt2tags pre/postproc rules
def addFilters(filters):
    if not filters: return []
    config = []
    cmdline = []
    for filter in filters:
        config.append("%%!%sproc: '%s' %s"%filter) # don't quote 2nd -- breaks tagged filter
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
            cmdline = addFilters(FILTERS.get(basename))
            cmdline.append(infile)
            lib.test(cmdline, outfile)
    # using smart filters, same files generate more than one output
    for alias in ALIASES:
        infile = ALIASES[alias] + '.t2t'
        outfile = alias + '.html'
        if lib.initTest(alias, infile, outfile):
            cmdline = addFilters(FILTERS.get(alias))
            cmdline.extend(['-o', outfile, infile])
            lib.test(cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)

    return lib.OK, lib.FAILED, lib.ERROR_FILES

