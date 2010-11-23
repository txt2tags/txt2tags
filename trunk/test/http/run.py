#
# txt2tags http loading tester (http://txt2tags.org)
# See also: ../run.py ../lib.py
#

import os, sys, re, glob

sys.path.insert(0, '..')
import lib
del sys.path[0]

# sux
lib.OK = lib.FAILED = 0
lib.ERROR_FILES = []

remote_root = 'http://txt2tags.org/test/'
remote_infiles = [
	'mtime.t2t',
	'not-found.t2t',
	]
remote_mapping = {
	'remote-outfile': 'simple.t2t',
	'stdout': 'simple.t2t',
	}

def run():
	# test all OK files found
	for outfile in glob.glob("ok/*"):
		basename = re.sub('\..*?$', '', outfile.replace('ok/', ''))
		target = re.sub('.*\.', '', outfile)
		infile = basename + ".t2t"
		if infile in remote_infiles:
			infile = remote_root + infile
		if basename in remote_mapping:
			infile = remote_root + remote_mapping[basename]
		outfile = outfile.replace('ok/', '')
		if lib.initTest(basename, infile, outfile):
			cmdline = []
			cmdline.extend(['-i', infile])
			if infile.startswith(remote_root) \
				and basename != 'remote-outfile':
				cmdline.extend(['-o', outfile])
			if basename == 'not-found':
				cmdline.append('>' + outfile)
				cmdline.append('2>&1')
			elif basename == 'stdout':
				cmdline.extend(['-o', '-'])
				cmdline.append('>' + outfile)
			elif basename == 'remote-outfile':
				cmdline.append('2>' + outfile)
			lib.convert(cmdline)
			lib.diff(outfile)
	# clean up
	if os.path.isfile(lib.CONFIG_FILE): os.remove(lib.CONFIG_FILE)
	
	return lib.OK, lib.FAILED, lib.ERROR_FILES

if __name__ == '__main__':
	print lib.MSG_RUN_ALONE
