# txt2tags marks parsing tester (http://txt2tags.org)

import glob
import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))

# left files are generated from right ones (using smart filters)
ALIASES = {
    'numlist' : 'list',
    'deflist' : 'list',
    'numtitle': 'title',
    'raw'     : 'verbatim',
    'tagged'  : 'verbatim',
    'tagged-inline': 'raw-inline',
    'verbatim-inline': 'raw-inline',
}

# XXX Known bug (issue 167): ``verbatim`` is parsed inside [image.png] and [link url] marks.

# smart filters to allow source inheritance
FILTERS = {
    'deflist' : [ ('pre', 'hyphen'  , 'colon' ), ('pre', '^( *)-', r'\1:') ],
    'numlist' : [ ('pre', 'hyphen'  , 'plus'  ), ('pre', '^( *)-', r'\1+') ],
    'numtitle': [ ('pre', 'equal'   , 'plus'  ), ('pre', '='     ,  '+'  ) ],
    'raw'     : [ ('pre', 'verbatim', 'raw'   ), ('pre', '`'     ,  '"'  ) ],
    'tagged'  : [ ('pre', 'verbatim', 'tagged'), ('pre', '`'     ,  "\'" ) ],
    'tagged-inline':
                [ ('pre', 'raw'     , 'tagged'), ('pre', '"'     ,  "'"  ) ],
    'verbatim-inline':
                [ ('pre', 'raw'   , 'verbatim'), ('pre', '"'     ,  "`"  ) ],
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
    os.chdir(DIR)
    # test all .t2t files found
    for infile in glob.glob("*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'
        if lib.initTest(basename, infile, outfile):
            cmdline = addFilters(FILTERS.get(basename))
            cmdline.append(infile)
            lib.test(DIR, cmdline, outfile)
    # using smart filters, same files generate more than one output
    for alias in ALIASES.keys():
        infile = ALIASES[alias] + '.t2t'
        outfile = alias + '.html'
        if lib.initTest(alias, infile, outfile):
            cmdline = addFilters(FILTERS.get(alias))
            cmdline.extend(['-o', outfile, infile])
            lib.test(DIR, cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)


if __name__ == '__main__':
    run()
