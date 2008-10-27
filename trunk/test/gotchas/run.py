#
# txt2tags marks gotchas tester (http://txt2tags.sf.net)
# See also: ../run.py ../lib.py
#

import os, sys, string, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

def run():
	# test all .t2t files found
	for infile in glob.glob("*.t2t"):
		basename = string.replace(infile, '.t2t', '')
		outfile = glob.glob("ok/%s.*" % basename)
		if outfile:
			outfile = string.replace(outfile[0], 'ok/', '')
		else:
			outfile = basename + '.html'
		if lib.initTest(basename, infile, outfile):
			cmdline = ['-H']
			cmdline.append(infile)
			lib.convert(cmdline)
			lib.diff(outfile)
	# clean up
	if os.path.isfile(lib.CONFIG_FILE): os.remove(lib.CONFIG_FILE)
	
	return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
	print lib.MSG_RUN_ALONE
