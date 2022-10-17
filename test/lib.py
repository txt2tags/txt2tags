#
# txt2tags test-suite library (http://txt2tags.org)
# See also: run.py, */run.py
#

from __future__ import print_function

import difflib
import os
import platform
import re
import subprocess
import sys
import time

PYTHON = sys.executable
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

print("Testing txt2tags on Python", platform.python_version())

# Path for txt2tags (change here if your txt2tags is in a different location)
TXT2TAGS = os.path.join(TEST_DIR, "..", "txt2tags.py")

CONFIG_FILE = "config"
CSS_FILE = "css"
DIR_OK = "ok"
DIR_ERROR = "error"

OK = FAILED = 0
ERROR_FILES = []

OVERRIDE = False

# force absolute path to avoid problems, set default options
TXT2TAGS = [os.path.abspath(TXT2TAGS), "-q", "--no-rc"]


def get_output(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()


#
# file tools
#
def ReadFile(filename):
    with open(filename, "r") as f:
        return f.read()


def WriteFile(filename, content=""):
    with open(filename, "w") as f:
        f.write(content)


def MoveFile(orig, target):
    if os.path.isfile(target):
        os.remove(target)
    os.link(orig, target)
    os.remove(orig)


def initTest(name, infile, outfile, okfile=None):
    if not okfile:
        okfile = os.path.join(DIR_OK, outfile)
    print("  %s" % name, end=" ")
    if not os.path.isfile(okfile):
        print("Skipping test (missing %s)" % okfile)
        return False
    return True


def getFileMtime(file):
    ret = "-NO-MTIME-"
    if os.path.isfile(file):
        ret = time.strftime("%Y%m%d", time.localtime(os.path.getmtime(file)))
    return ret


def getCurrentDate():
    return time.strftime("%Y%m%d", time.localtime(time.time()))


def _convert(options):
    cmdline = " ".join([PYTHON] + TXT2TAGS + options)
    return subprocess.call(cmdline, shell=True)


def remove_version_and_dates(text):
    version_re = r"\d+\.\d+(\.\d+)?"
    for regex in [
        r"txt2tags version {version_re}",
        # Remove date from header.
        r"\d{{2}}/\d{{2}}/\d{{4}}",
        # lout escapes / with "/" in headers
        r'\d{{2}}"/"\d{{2}}"/"\d{{4}}',
        # Remove dates.
        r"today is \d{{8}}",
        r"which gives: \d{{2}}-\d{{2}}-\d{{4}}",
        # man escapes - with \-
        r"which gives: \d{{2}}\\-\d{{2}}\\-\d{{4}}",
    ]:
        text = re.sub(regex.format(**locals()), "", text)
    return text


def mark_ok(outfile):
    global OK
    print("OK")
    OK += 1
    os.remove(outfile)


def mark_failed(outfile, okfile=None):
    global FAILED
    print("FAILED")
    FAILED += 1
    if not os.path.isdir(DIR_ERROR):
        os.mkdir(DIR_ERROR)
    module = os.path.basename(os.getcwd())
    errfile = os.path.join(TEST_DIR, module, DIR_ERROR, outfile)
    MoveFile(outfile, errfile)
    ERROR_FILES.append(errfile)
    print("meld {okfile} {errfile}".format(**locals()))


def override(okfile, outfile):
    global FAILED
    print("OVERRIDE")
    FAILED += 1
    if os.path.exists(outfile):
        MoveFile(outfile, okfile)


def _grep(okfile, outfile):
    """grep if the okfile snippet is contained in outfile"""
    ok = ReadFile(okfile)
    out = ReadFile(outfile)
    if ok not in out:
        if OVERRIDE:
            override(okfile, outfile)
        else:
            mark_failed(outfile, okfile=okfile)
            print("_grep: {okfile} contents not found in {outfile}".format(**locals()))
    else:
        mark_ok(outfile)


def _diff(outfile, okfile):
    out = ReadFile(outfile)
    out = remove_version_and_dates(out)
    ok = ReadFile(okfile)
    ok = remove_version_and_dates(ok)
    if out != ok:
        if OVERRIDE:
            override(okfile, outfile)
        else:
            mark_failed(outfile, okfile=okfile)
            for line in difflib.unified_diff(ok.splitlines(), out.splitlines()):
                print(line)
    else:
        mark_ok(outfile)


def test(cmdline, outfile, okfile=None):
    okfile = okfile or os.path.join(DIR_OK, outfile)
    _convert(cmdline)
    _diff(outfile, okfile)
