#
# txt2tags test-suite library (http://txt2tags.org)
# See also: run.py, */run.py
#

import os, time

# Python 2.7 or 2.6 needed

if os.system('python2.7 --version') == 0:
    PYTHON = 'python2.7'
elif os.system('python2.6 --version') == 0:
    PYTHON = 'python2.6'
else:
    print "You need Python 2.6 or 2.7 to successfully all the test suite."
    PYTHON = 'python default'

print "Running " + PYTHON

# Path for txt2tags (change here if your txt2tags is in a different location)
TXT2TAGS = '../txt2tags'
TXT2TAGSLITE = '../txt2tagslite'

CONFIG_FILE = 'config'
CSS_FILE = 'css'
DIR_OK = 'ok'
DIR_ERROR = 'error'

OK = FAILED = 0
ERROR_FILES = []

MSG_RUN_ALONE = "No No No. Call me with ../run.py\nI can't be run alone."

# force absolute path to avoid problems, set default options
TXT2TAGS = os.path.abspath(TXT2TAGS) + ' -q --no-rc'
TXT2TAGSLITE = os.path.abspath(TXT2TAGSLITE) + ' -q --no-rc'

EXTENSION = {'aat': 'txt', 'aap': 'txt', 'aas': 'txt', 'txt': 'txt', 'aatw': 'html', 'aapw': 'html', 'aasw': 'html', 'html5': 'html', 'htmls': 'html', 'xhtml': 'html', 'xhtmls': 'html', 'csvs': 'csv', 'texs': 'tex'} 

#
# file tools
#
def ReadFile(filename):
    return open(filename, 'r').read()

def WriteFile(filename, content=''):
    f = open(filename, 'w')
    f.write(content)
    f.close()

def MoveFile(orig, target):
    if os.path.isfile(target):
        os.remove(target)
    os.link(orig, target)
    os.remove(orig)

#
# auxiliar tools
#
def initTest(name, infile, outfile, okfile=None):
    if not okfile:
        okfile  = os.path.join(DIR_OK, outfile)
    print '  Testing %s ...' % name,
    if not os.path.isfile(okfile):
        print 'Skipping test (missing %s)' % okfile
        return False
    return True

def getFileMtime(file):
    ret = "-NO-MTIME-"
    if os.path.isfile(file):
        ret = time.strftime('%Y%m%d', time.localtime(os.path.getmtime(file)))
    return ret

def getCurrentDate():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

#
# the hot tools
#
def convert(options, lite=False):
    if type(options) in [type(()), type([])]:
        options = ' '.join(options)
    if lite:
        cmdline = PYTHON + ' ' + TXT2TAGSLITE + ' ' + options
    else:
        cmdline = PYTHON + ' ' + TXT2TAGS + ' ' + options
    # print "\n**Executing: %s" % cmdline
    return os.system(cmdline)

def diff(outfile, okfile=None):
    global OK, FAILED, ERROR_FILES
    if not okfile:
        okfile = os.path.join(DIR_OK, outfile)
    # print "\n**Diff: %s %s" % (outfile, okfile)
    out = ReadFile(outfile)
    ok = ReadFile(okfile)
    if out != ok:
        print 'FAILED'
        FAILED = FAILED + 1
        if not os.path.isdir(DIR_ERROR):
            os.mkdir(DIR_ERROR)
        MoveFile(outfile, os.path.join(DIR_ERROR, outfile))
        ERROR_FILES.append(outfile)
    else:
        print 'OK'
        OK = OK + 1
        os.remove(outfile)
