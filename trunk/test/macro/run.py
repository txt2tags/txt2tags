#
# txt2tags %%macro command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, re, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

# smart filters to perform macros normalization
FILTERS = [
    ('post', os.path.abspath('..'), '/ABSOLUTE-PATH-TO-TEST-FOLDER'),
    ('post', lib.getFileMtime('macro/syntax.t2t'), '@MTIME@'),
    ('post', lib.getCurrentDate(), '@DATE@'),
    ('post', '^(Date.*)@MTIME@', r'\1@DATE@'),
    ('post', '^(Date.*)@MTIME@', r'\1@DATE@'),
    ('post', '^(..appversion +"\d\.\d+)\.\d+', r'\1'),  # Remove SVN release
]

# convert FILTERS tuples to txt2tags pre/postproc rules
def addFilters(filters):
    config = []
    cmdline = []
    for filter_ in filters:
        config.append("%%!%sproc: '%s' %s" % filter_)
    if config:
        lib.WriteFile(lib.CONFIG_FILE, '\n'.join(config))
        cmdline = ['-C', lib.CONFIG_FILE]
    return cmdline

def run():
    # test all OK files found
    for outfile in glob.glob("ok/*"):
        stderr = 0
        basename = re.sub('\..*?$', '', outfile.replace('ok/', ''))
        target = re.sub('.*\.', '', outfile)
        if target == 'out':
            target = 'txt'
            stderr = 1
        infile = basename + ".t2t"
        # Using filename -H suffix to run new tests using -H option
        if basename.endswith('-H'):
            infile = basename.replace('-H', '') + ".t2t"
        outfile = outfile.replace('ok/', '')

        if lib.initTest(basename, infile, outfile):
            cmdline = []
            cmdline = addFilters(FILTERS)
            if basename.endswith('-H'):
                cmdline.append('-H')
                cmdline.extend(['-o', outfile])
            cmdline.extend(['-t', target])
            cmdline.extend(['-i', infile])
            if stderr:
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            lib.convert(cmdline)
            lib.diff(outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)

    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
