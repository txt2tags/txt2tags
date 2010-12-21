#!/bin/bash
# 2010-08-06 Aurelio Jargas
#
# Quick and dirty tests for Ascii Art Text target.
# NOT integrated into main test suite, you must run it alone.

cd $(dirname "$0")

t2t="../../txt2tags --no-rc"

$t2t -i sample.t2t -t aat                                   -o default.aat
$t2t -i sample.t2t -t aat --slides                          -o slides.aat
$t2t -i sample.t2t -t aat --slides --width 60               -o slides-60.aat
$t2t -i sample.t2t -t aat --slides --width 60 --height 30   -o slides-60x30.aat
$t2t -i sample.t2t -t aat --toc                             -o toc.aat
$t2t -i sample.t2t -t aat --toc --slides --width 60         -o toc-slide.aat
$t2t -i sample.t2t -t aat --toc-only                        -o toc-only.aat
$t2t -i sample.t2t -t aat --toc-only --slides --width 60    -o toc-only-slides.aat

$t2t -i sample.t2t -t aat --no-headers                                   -o default-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --slides --width 60               -o slides-60-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --toc                             -o toc-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --toc --slides --width 60         -o toc-slide-no-headers.aat

$t2t -i toc-macro.t2t -t aat --width 60                     -o no-toc-macro.aat
$t2t -i toc-macro.t2t -t aat --toc --width 60               -o toc-macro.aat
$t2t -i toc-macro.t2t -t aat --slides --width 60            -o no-toc-macro-slides.aat
$t2t -i toc-macro.t2t -t aat --toc --slides --width 60      -o toc-macro-slides.aat
# ^ bug: The "Table of Contents" is added together with custom TOC title

errors=0
for file in *.aat
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
	ls -1 *.aat
fi
