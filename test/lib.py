# txt2tags test-suite library (http://txt2tags.org)

# TODO: Remove initTest().
# TODO: Don't write output to disk (easier code and faster execution)
# TODO: Only run http test module if --slow is passed to py.test

import os
import re
import subprocess
import sys
import time


DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(DIR)
PYTHON = sys.executable

# Path to txt2tags (change to '../txt2tagslite' for testing txt2tagslite)
TXT2TAGS = os.path.join(REPO, 'txt2tags')

CONFIG_FILE = 'config'
CSS_FILE = 'css'
DIR_OK = 'ok'

# Force absolute path and set default options.
TXT2TAGS = [os.path.abspath(TXT2TAGS), '-q', '--no-rc']

EXTENSION = {
    'aat': 'txt', 'aap': 'txt', 'aas': 'txt', 'txt': 'txt',
    'aatw': 'html', 'aapw': 'html', 'aasw': 'html', 'html5': 'html',
    'htmls': 'html', 'xhtml': 'html', 'xhtmls': 'html', 'csvs': 'csv',
    'texs': 'tex'}


def get_output(cmd):
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).communicate()[0].strip()


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename, content=''):
    with open(filename, 'w') as f:
        f.write(content)


def initTest(name, infile, outfile, okfile=None):
    return True


def getFileMtime(file):
    ret = "-NO-MTIME-"
    if os.path.isfile(file):
        ret = time.strftime('%Y%m%d', time.localtime(os.path.getmtime(file)))
    return ret


def getCurrentDate():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def _convert(options, module_dir):
    cmdline = ' '.join([PYTHON] + TXT2TAGS + options)
    print 'Calling "%s" in "%s"' % (cmdline, module_dir)
    return subprocess.call(cmdline, shell=True, cwd=module_dir)


def _diff(outfile, okfile):
    out = read_file(outfile)
    os.remove(outfile)
    out = remove_version(out)
    ok = read_file(okfile)
    ok = remove_version(ok)
    assert out == ok


def remove_version(text):
    version_re = r'\d+\.\d+\.?(\d+)?'
    for regex in [r'(Txt2tags) %(version_re)s',
                  r'(txt2tags version) %(version_re)s',
                  r'(%%%%appversion) "%(version_re)s"']:
        text = re.sub(regex % locals(), '\1', text)
    return text


def get_ok_files(module_dir):
    ok_dir = os.path.join(module_dir, DIR_OK)
    for filename in sorted(os.listdir(ok_dir)):
        name, extension = os.path.splitext(filename)
        target = extension.lstrip('.')
        stderr = False
        if target == 'out':
            target = 'txt'
            stderr = True
        infile = name + ".t2t"
        outfile = filename
        okfile = os.path.join(ok_dir, filename)
        yield name, target, infile, outfile, okfile, stderr


def test(module_dir, cmdline, outfile, okfile=None):
    assert os.path.isabs(module_dir), module_dir
    _convert(cmdline, module_dir)

    if not os.path.isabs(outfile):
        outfile = os.path.join(module_dir, outfile)
    assert os.path.isabs(outfile)

    if not okfile:
        dirname, basename = os.path.split(outfile)
        assert dirname == module_dir
        okfile = basename
    # Make path absolute if it isn't already.
    okfile = os.path.join(module_dir, DIR_OK, okfile)
    assert os.path.isabs(okfile)

    _diff(outfile, okfile)
