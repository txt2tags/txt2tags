#
# txt2tags %!includeconf command tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

# Tests for the command line option -C
# Note: --config-file is also tested automatically from these tests
tests = [
    {
    'name'   : 'C',
    'cmdline': ["-C _config.inc"],
    'not-numbered': True,
    }, {
    'name'   : 'C-C',
    'cmdline': ["-C _config.inc -C _config.inc"],
    'not-numbered': True,
    }, {
    'name'   : 'C-C2',
    'cmdline': ["-C _config.inc -C _config2.inc"],
    }, {
    'name'   : 'C-default',
    'cmdline': ["-t html -C _config2.inc"],
    }, {
    'name'   : 'C-empty',
    'cmdline': ["-t html -C _empty.inc"],
    'not-numbered': True,
    }, {
    'name'   : 'C-not-found',
    'cmdline': ["-t html -C XXX.inc"],
    'not-numbered': True,
    }, {
    'name'   : 'C-text',
    'cmdline': ["-t html -C _text.inc"],
    'not-numbered': True,
    }, {
    'name'   : 'C-targeted-inside',
    'cmdline': ["-t html -C _targeted.inc"],
    }, {
    'name'   : 'C-nesting',
    'cmdline': ["-C _sub_include.inc"],
    }, {
    'name'   : 'C-nesting-folder',
    'cmdline': ["-C folder/_folder.inc"],
    }, {
    'name'   : 'C-nesting-folder-back',
    'cmdline': ["-C folder/subfolder/_folder-back.inc"],
    
    # This checking is never made because the infile may not be known without
    # reading the config file. In other words, you can set %!options: -i foo.t2t
    # inside the config file and just call: txt2tags -C config.t2t
    # Because of this feature, we can't compare config file and infile names
    # before reading the full config. But it will not loop, since the first body
    # line of the infile will raise a config error.
    # }, {
    # 'name'   : 'C-itself',             # t2t -C foo.t2t -i foo.t2t
    # 'cmdline': ["-C body-only"],
    }
]

def run():

    ### First test the %!includeconf command

    errors = [
        'includeconf-itself',
        'includeconf-not-found',
        'includeconf-targeted',
        'includeconf-text',
        ]
    unnumbered = [
        'includeconf-empty',
        ]

    # test all t2t files found
    for infile in glob.glob("includeconf-*.t2t"):
        basename = infile.replace('.t2t', '')
        outfile = basename + '.html'

        if basename in unnumbered:
            okfile = 'ok/not-numbered.html'
        else:
            okfile = 'ok/numbered.html'

        if basename in errors:
            outfile = basename + '.out'
            okfile = 'ok/' + outfile
            cmdline = ['-H', '-i', infile, '-o- >', outfile, '2>&1']
        else:
            cmdline = ['-H', '-i', infile, '-o', outfile]

        if lib.initTest(basename, infile, outfile, okfile):
            lib.convert(cmdline)
            lib.diff(outfile, okfile)

    ### Now test -C and --config-file command line options

    errors = ['C-not-found', 'C-text']
    default_cmdline = ['-H -i body-only.t2t']
    infile = 'body-only.t2t'
    for test in tests:

        # --enum-title is used by this test?
        if test.get('not-numbered'):
            okfile = 'ok/not-numbered.html'
        else:
            okfile = 'ok/numbered.html'

        # 1st turn (-C), 2nd turn (--config-file)
        for i in (1, 2):

            if i == 1:
                name = test['name']
                cmdline = test['cmdline']
            else:
                name = test['name'].replace('C', 'config-file')
                cmdline = map(lambda x: x.replace('-C', '--config-file'), test['cmdline'])

            outfile = name + '.html'

            if test['name'] in errors:
                outfile = name + '.out'
                okfile = 'ok/' + outfile
                cmdline = default_cmdline + cmdline + ['-o- >', outfile, '2>&1']
            else:
                cmdline = default_cmdline + cmdline + ['-o', outfile]

            # convert and check results
            if lib.initTest(name, infile, outfile, okfile):
                lib.convert(cmdline)
                lib.diff(outfile, okfile)

    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)

    return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
    print lib.MSG_RUN_ALONE
