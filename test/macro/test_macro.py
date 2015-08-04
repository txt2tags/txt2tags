# txt2tags %%macro command tester (http://txt2tags.org)

import os

import lib


DIR = os.path.dirname(os.path.abspath(__file__))

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
        lib.write_file(lib.CONFIG_FILE, '\n'.join(config))
        cmdline = ['-C', lib.CONFIG_FILE]
    return cmdline


def run():
    os.chdir(DIR)
    for name, target, infile, outfile, okfile, stderr in lib.get_ok_files(DIR):
        if name.endswith('-H'):
            infile = name[:-2] + ".t2t"

        if lib.initTest(name, infile, outfile):
            cmdline = []
            cmdline = addFilters(FILTERS)
            if name == 'path':
                cmdline.extend(['--width', '200'])
            if name.endswith('-H'):
                cmdline.append('-H')
                cmdline.extend(['-o', outfile])
            cmdline.extend(['-t', target])
            cmdline.extend(['-i', infile])
            if stderr:
                cmdline.extend(['-o', '-'])
                cmdline.append('>' + outfile)
                cmdline.append('2>&1')
            lib.test(DIR, cmdline, outfile)
    # clean up
    if os.path.isfile(lib.CONFIG_FILE):
        os.remove(lib.CONFIG_FILE)


if __name__ == '__main__':
    run()
