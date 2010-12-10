#!/bin/bash
# 2010-08-06 Aurelio Jargas
#
# Quick and dirty tests for Art target.
# NOT integrated into main test suite, you must run it alone.

cd $(dirname "$0")

t2t="python2.6 ../../txt2tags --no-rc"

$t2t -i sample.t2t -t art                                   -o default.art
$t2t -i sample.t2t -t art --slides                          -o slides.art
$t2t -i sample.t2t -t art --slides --width 60               -o slides-60.art
$t2t -i sample.t2t -t art --slides --width 60 --height 30   -o slides-60x30.art
$t2t -i sample.t2t -t art --toc                             -o toc.art
$t2t -i sample.t2t -t art --toc --slides --width 60         -o toc-slide.art
$t2t -i sample.t2t -t art --toc-only                        -o toc-only.art
$t2t -i sample.t2t -t art --toc-only --slides --width 60    -o toc-only-slides.art

$t2t -i sample.t2t -t art --no-headers                                   -o default-no-headers.art
$t2t -i sample.t2t -t art --no-headers --slides --width 60               -o slides-60-no-headers.art
$t2t -i sample.t2t -t art --no-headers --toc                             -o toc-no-headers.art
$t2t -i sample.t2t -t art --no-headers --toc --slides --width 60         -o toc-slide-no-headers.art

$t2t -i toc-macro.t2t -t art --width 60                     -o no-toc-macro.art
$t2t -i toc-macro.t2t -t art --toc --width 60               -o toc-macro.art
$t2t -i toc-macro.t2t -t art --slides --width 60            -o no-toc-macro-slides.art
$t2t -i toc-macro.t2t -t art --toc --slides --width 60      -o toc-macro-slides.art
# ^ bug: The "Table of Contents" is added together with custom TOC title

errors=0
for file in *.art
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
	ls -1 *.art
fi
