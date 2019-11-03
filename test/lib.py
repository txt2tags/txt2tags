#
# txt2tags test-suite library (http://txt2tags.org)
# See also: run.py, */run.py
#

from __future__ import print_function

import os
import platform
import re
import subprocess
import sys
import time

PYTHON = sys.executable

print("Testing txt2tags on Python", platform.python_version())

# Path for txt2tags (change here if your txt2tags is in a different location)
TXT2TAGS = "../txt2tags.py"

CONFIG_FILE = "config"
CSS_FILE = "css"
DIR_OK = "ok"
DIR_ERROR = "error"

OK = FAILED = 0
ERROR_FILES = []

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


def remove_version(text):
    version_re = r"\d+\.\d+\.?(\d+)?"
    for regex in [
        r"(Txt2tags) %(version_re)s",
        r"(txt2tags version) %(version_re)s",
        r'(%%%%appversion) "%(version_re)s"',
    ]:
        text = re.sub(regex % locals(), "\1", text)
    return text


def mark_ok(outfile):
    global OK
    print("OK")
    OK += 1
    os.remove(outfile)


def mark_failed(outfile):
    global FAILED
    print("FAILED")
    FAILED += 1
    if not os.path.isdir(DIR_ERROR):
        os.mkdir(DIR_ERROR)
    if os.path.exists(outfile):
        MoveFile(outfile, os.path.join(DIR_ERROR, outfile))
        module = os.path.basename(os.getcwd())
        ERROR_FILES.append(os.path.join(module, DIR_ERROR, outfile))


def _diff(outfile, okfile=None):
    global OK, FAILED, ERROR_FILES
    if not okfile:
        okfile = os.path.join(DIR_OK, outfile)
    out = ReadFile(outfile)
    out = remove_version(out)
    ok = ReadFile(okfile)
    ok = remove_version(ok)
    if out != ok:
        mark_failed(outfile)
    else:
        mark_ok(outfile)


def test(cmdline, outfile, okfile=None):
    okfile = okfile or os.path.join(DIR_OK, outfile)
    _convert(cmdline)
    _diff(outfile, okfile=okfile)
