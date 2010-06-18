#
# txt2tags command line options tester (http://txt2tags.sf.net)
# See also: ../run.py ../lib.py
#
# Note: The .t2t files are generated dynamicaly, based on 'tests' dict data
#

import sys, os

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

# text patterns to compose source files
EMPTY_HEADER    = "\n"
FULL_HEADER     = "Header 1\nHeader 2\nHeader 3\n"
SIMPLE_BODY     = "Text.\n"
TITLED_BODY     = "= Title 1 =\nText.\n== Title 2 ==\nText.\n"
EMAIL           = 'user@domain.com\n'
CONFIG_FILE_TXT = '%!target: html\n'
CSS_FILE_TXT    = 'p { color: blue; }\n'

# a nice postproc to rip off version information from output
VERSION_GOTCHA = "%!postproc: '(generated by txt2tags) [^ ]+' '\\1'\n"

# the registered tests
# missing: --rc, --no-rc (used), --gui, --quiet, -q (used),
#          --verbose, -v, --help, -h, --version, -V, --dump-config
#          --no-dump-config, --dump-source, --no-dump-source
tests = [
  {
  'name'   : 'target',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --target html"],
  'extra'  : ['notarget']
  }, {
  'name'   : 't',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H -t html"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'infile',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --infile"],
  }, {
  'name'   : 'no-infile-1',                 # useless
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --no-infile"],
  }, {
  'name'   : 'no-infile-2',                 # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --infile fake --no-infile"],
  }, {
  'name'   : 'no-infile-3',                 # turning OFF multiple
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --infile fake1 --infile fake2 --no-infile"],
  }, {
  'name'   : 'i',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H -i"],
  }, {
  'name'   : 'outfile-1',                   # same name as default
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --outfile outfile-1.html"],
  }, {
  'name'   : 'outfile-2',                   # different name
  'target' : 'foo',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H -t html --outfile outfile-2.foo"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'no-outfile-1',                # useless
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --no-outfile"],
  }, {
  'name'   : 'no-outfile-2',                # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --outfile fake --no-outfile"],
  }, {
  'name'   : 'o',                           # same name as default
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H -o o.html"],
  }, {
  'name'   : 'enum-title-1',
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --enum-title"],
  }, {
  'name'   : 'enum-title-2',                # with --toc
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc --enum-title"],
  }, {
  'name'   : 'enum-title-3',                # no title to enumerate
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --enum-title"],
  }, {
  'name'   : 'no-enum-title-1',             # useless
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --no-enum-title"],
  }, {
  'name'   : 'no-enum-title-2',             # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --enum-title --no-enum-title"],
  }, {
  'name'   : 'n',
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H -n"],
  }, {
  'name'   : 'toc-1',
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc"],
  }, {
  'name'   : 'toc-2',                       # empty toc (no title)
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --toc"],
  }, {
  'name'   : 'toc-3',                       # empty body
  'target' : 'html',
  'content': EMPTY_HEADER,
  'cmdline': ["-H --toc"],
  }, {
  'name'   : 'no-toc-1',                    # useless
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --no-toc"],
  }, {
  'name'   : 'no-toc-2',                    # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc --no-toc"],
  }, {
  'name'   : 'toc-level-1',
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc --toc-level 1"],
  }, {
  'name'   : 'toc-level-2',                 # very deep
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc --toc-level 999"],
  }, {
  'name'   : 'toc-level-3',                 # useless (no --toc)
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc-level 1"],
  }, {
  'name'   : 'toc-only-1',
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["--toc-only -o toc-only-1.html"],
  }, {
  'name'   : 'toc-only-2',                  # empty toc (no title)
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["--toc-only -o toc-only-2.html"],
  }, {
  'name'   : 'toc-only-3',                  # no target, defaults to txt
  'target' : 'out',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["--toc-only -o toc-only-3.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'toc-only-4',                  # with --toc-level
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["--toc-only --toc-level 1 -o toc-only-4.html"],
  }, {
  'name'   : 'toc-only-5',                  # with --enum-title
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["--toc-only --enum-title -o toc-only-5.html"],
  }, {
  'name'   : 'no-toc-only-1',               # useless
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --no-toc-only"],
  }, {
  'name'   : 'no-toc-only-2',               # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+TITLED_BODY,
  'cmdline': ["-H --toc-only --no-toc-only"],
  }, {
  'name'   : 'mask-email',
  'target' : 'html',
  'content': EMPTY_HEADER+EMAIL,
  'cmdline': ["-H --mask-email"],
  }, {
  'name'   : 'no-mask-email-1',             # useless
  'target' : 'html',
  'content': EMPTY_HEADER+EMAIL,
  'cmdline': ["-H --no-mask-email"],
  }, {
  'name'   : 'no-mask-email-2',             # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+EMAIL,
  'cmdline': ["-H --mask-email --no-mask-email"],
  }, {
  'name'   : 'headers-1',                   # useless
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--headers"],
  }, {
  'name'   : 'headers-2',                   # turning OFF --no-headers
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--no-headers --headers"],
  }, {
  'name'   : 'no-headers',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["--no-headers"],
  }, {
  'name'   : 'H',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H"],
  }, {
  'name'   : 'encoding-1',
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--encoding iso-8859-1"],
  }, {
  'name'   : 'encoding-2',                  # normalization
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--encoding ISO88591"],
  }, {
  'name'   : 'encoding-3',                  # customized
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--encoding fake-999"],
  }, {
  'name'   : 'encoding-4',                  # LaTeX translation
  'target' : 'tex',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--encoding iso-8859-1"],
  }, {
  'name'   : 'no-encoding-1',               # useless
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--no-encoding"],
  }, {
  'name'   : 'no-encoding-2',               # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--encoding iso-8859-1 --no-encoding"],
  }, {
  'name'   : 'style-1',
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style", lib.CSS_FILE],
  }, {
  'name'   : 'style-2',                     # multiple declaration
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style other.css --style", lib.CSS_FILE],
  }, {
  'name'   : 'style-3',                     # LaTeX package
  'target' : 'tex',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style mypackage"],
  }, {
  'name'   : 'style-4',                     # LaTeX multiple package
  'target' : 'tex',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style mypackage,otherpackage,another"],
  }, {
  'name'   : 'style-5',                     # LaTeX module no .sty
  'target' : 'tex',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style foo.sty --style bar.STY --style baz"],
  }, {
  'name'   : 'no-style-1',                  # useless
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--no-style"],
  }, {
  'name'   : 'no-style-2',                  # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--style fake.css --no-style"],
  }, {
  'name'   : 'css-sugar-1',                 # just body
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --css-sugar"],
  }, {
  'name'   : 'css-sugar-2',                 # empty toc & body
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --toc --css-sugar"],
  }, {
  'name'   : 'css-sugar-3',                 # headers, toc & body
  'target' : 'html',
  'content': FULL_HEADER+VERSION_GOTCHA+TITLED_BODY,
  'cmdline': ["--toc --css-sugar"],
  }, {
  'name'   : 'no-css-sugar-1',              # useless
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --no-css-sugar"],
  }, {
  'name'   : 'no-css-sugar-2',              # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --css-sugar --no-css-sugar"],
  }, {
  'name'   : 'css-inside-1',
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-inside --style", lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'css-inside-2',                # with --css-sugar
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-sugar --css-inside --style", lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'css-inside-3',                # missing CSS file
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-inside --style", lib.CSS_FILE],
  }, {
  'name'   : 'css-inside-4',                # no --style
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-sugar --css-inside"],
  }, {
  'name'   : 'css-inside-5',                # two CSS files
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-inside --style "+ lib.CSS_FILE +" --style "+ lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'css-inside-6',                # two CSS files, one missing
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-inside --style missing.css --style "+ lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'no-css-inside-1',             # useless
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--no-css-inside --style", lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'no-css-inside-2',             # turning OFF
  'target' : 'html',
  'content': EMPTY_HEADER+VERSION_GOTCHA+SIMPLE_BODY,
  'cmdline': ["--css-inside --no-css-inside --style", lib.CSS_FILE],
  'extra'  : ['css']
  }, {
  'name'   : 'config-file',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H --config-file", lib.CONFIG_FILE],
  'extra'  : ['config', 'notarget']
  }, {
  'name'   : 'C',
  'target' : 'html',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["-H -C", lib.CONFIG_FILE],
  'extra'  : ['config', 'notarget']
  }, {
  'name'   : 'dump-config',
  'content': EMPTY_HEADER+CONFIG_FILE_TXT+SIMPLE_BODY,
  'cmdline': ["--dump-config"],
  'redir'  : ["> dump-config.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'no-dump-config',
  'content': EMPTY_HEADER+CONFIG_FILE_TXT+SIMPLE_BODY,
  'cmdline': ["-H -o- --dump-config --no-dump-config"],
  'redir'  : ["> no-dump-config.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'dump-source',
  'content': FULL_HEADER+CONFIG_FILE_TXT+SIMPLE_BODY,
  'cmdline': ["--dump-source"],
  'redir'  : ["> dump-source.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'no-dump-source',
  'content': EMPTY_HEADER+CONFIG_FILE_TXT+SIMPLE_BODY,
  'cmdline': ["-H -o- --dump-source --no-dump-source"],
  'redir'  : ["> no-dump-source.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'list-targets',
  'content': EMPTY_HEADER+SIMPLE_BODY,
  'cmdline': ["--list-targets"],
  'redir'  : ["> list-targets.out"],
  'extra'  : ['notarget']
  }, {
  'name'   : 'no-list-targets',
  'content': EMPTY_HEADER+CONFIG_FILE_TXT+SIMPLE_BODY,
  'cmdline': ["-H -o- --list-targets --no-list-targets"],
  'redir'  : ["> no-list-targets.out"],
  'extra'  : ['notarget']
  }
]

def run():
	for test in tests:
		infile  = test['name'] + '.t2t'
		outfile = test['name'] + '.' + (test.get('target') or 'out')
		cmdline = test['cmdline'] + [infile]
		extra   = test.get('extra') or []
		if lib.initTest(test['name'], infile, outfile):
			# create the extra files (if needed for this test)
			if 'config' in extra:
				lib.WriteFile(lib.CONFIG_FILE, CONFIG_FILE_TXT)
			if 'css' in extra:
				lib.WriteFile(lib.CSS_FILE, CSS_FILE_TXT)
			if not 'notarget' in extra:
				cmdline = ['-t', test['target']] + cmdline
			if test.get('redir'):
				cmdline = cmdline + test['redir']
			# create the source file
			lib.WriteFile(infile, test['content'])
			# convert and check results
			lib.convert(cmdline)
			lib.diff(outfile)
			# remove the trash
			os.remove(infile)
			if os.path.isfile(lib.CSS_FILE): os.remove(lib.CSS_FILE)
			if os.path.isfile(lib.CONFIG_FILE): os.remove(lib.CONFIG_FILE)
	return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
	print lib.MSG_RUN_ALONE
