#!/bin/bash
# 2010-11-11 Aurelio Jargas
#
# Quick and dirty tests for images.
# NOT integrated into main test suite, you must run it alone.

cd $(dirname "$0")

t2t=../../txt2tags

$t2t -H -t creole -i relative-path.t2t -o relative-path-same-folder.creole

test -d folder || mkdir folder
$t2t -H -t creole -i relative-path.t2t -o folder/relative-path-diff-folder.creole
mv folder/relative-path-diff-folder.creole .
rmdir folder

errors=0
for file in *.creole
do
	if ! test -f ok/$file
	then
		echo "File not found: ok/$file (test skipped)"
		continue
	fi
	
	differences=$(diff $file ok/$file)
	if test -z "$differences"
	then
		rm $file
	else
		errors=1
	fi
done

if test $errors -eq 0
then
	echo
	echo "All files are OK"
else
	echo
	echo "Found errors here (compare with 'ok' folder):"
	ls -1 *.creole
fi
