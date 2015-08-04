#
# txt2tags test-suite library (http://txt2tags.org)
# See also: run.py, */run.py
#

import os
import platform
import re
import subprocess
import sys
import time

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(DIR)
PYTHON = sys.executable

print "Testing txt2tags on", platform.python_implementation(), platform.python_version()

# Path to txt2tags (change to '../txt2tagslite' for testing txt2tagslite)
TXT2TAGS = os.path.join(REPO, 'txt2tags')

CONFIG_FILE = 'config'
CSS_FILE = 'css'
DIR_OK = 'ok'
DIR_ERROR = 'error'

OK = FAILED = 0
ERROR_FILES = []

MSG_RUN_ALONE = "No No No. Call me with ../run.py\nI can't be run alone."

# force absolute path to avoid problems, set default options
TXT2TAGS = [os.path.abspath(TXT2TAGS), '-q', '--no-rc']

EXTENSION = {'aat': 'txt', 'aap': 'txt', 'aas': 'txt', 'txt': 'txt', 'aatw': 'html', 'aapw': 'html', 'aasw': 'html', 'html5': 'html', 'htmls': 'html', 'xhtml': 'html', 'xhtmls': 'html', 'csvs': 'csv', 'texs': 'tex'}

def get_output(cmd):
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).communicate()[0].strip()

#
# file tools
#
def ReadFile(filename):
    with open(filename, 'r') as f:
        return f.read()

def WriteFile(filename, content=''):
    with open(filename, 'w') as f:
        f.write(content)

def MoveFile(orig, target):
    if os.path.isfile(target):
        os.remove(target)
    os.link(orig, target)
    os.remove(orig)

def initTest(name, infile, outfile, okfile=None):
    if not okfile:
        okfile  = os.path.join(DIR_OK, outfile)
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

def _convert(options):
    txt2tags = TXT2TAGS
    cmdline = ' '.join([PYTHON] + txt2tags + options)
    return subprocess.call(cmdline, shell=True)

def remove_version(text):
    version_re = r'\d+\.\d+\.?(\d+)?'
    for regex in [r'(Txt2tags) %(version_re)s',
                  r'(txt2tags version) %(version_re)s',
                  r'(%%%%appversion) "%(version_re)s"']:
        text = re.sub(regex % locals(), '\1', text)
    return text

def _diff(outfile, okfile=None):
    global OK, FAILED, ERROR_FILES
    if not okfile:
        okfile = os.path.join(DIR_OK, outfile)
    out = ReadFile(outfile)
    os.remove(outfile)
    out = remove_version(out)
    ok = ReadFile(okfile)
    ok = remove_version(ok)
    assert out == ok

def test(cmdline, outfile, okfile=None):
    _convert(cmdline)
    if not okfile:
        okfile = os.path.join(DIR_OK, outfile)
    _diff(outfile, okfile=okfile)
