#!/bin/bash
# 2010-08-06 Aurelio Jargas
#
# Quick and dirty tests for Ascii Art Text target.
# NOT integrated into main test suite, you must run it alone.

cd $(dirname "$0")

echo
echo "Running txt2tags"

t2t="../../txt2tags --no-rc"

$t2t -i sample.t2t -t aat                                   -o default.aat
$t2t -i sample.t2t -t aat --slides --width 80               -o slides.aat
$t2t -i sample.t2t -t aat --slides --width 60               -o slides-60.aat
$t2t -i sample.t2t -t aat --slides --width 60 --height 30   -o slides-60.30.aat
$t2t -i sample.t2t -t aat --toc                             -o toc.aat
$t2t -i sample.t2t -t aat --toc --slides --width 60         -o toc-slide.aat
$t2t -i sample.t2t -t aat --toc-only                        -o toc-only.aat
$t2t -i sample.t2t -t aat --toc-only --slides --width 60    -o toc-only-slides.aat

$t2t -i sample.t2t -t aat --no-headers                                   -o default-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --slides --width 60               -o slides-60-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --toc                             -o toc-no-headers.aat
$t2t -i sample.t2t -t aat --no-headers --toc --slides --width 60         -o toc-slide-no-headers.aat

$t2t -i toc-macro.t2t -t aat --width 60                     -o no-toc-macro.aat
$t2t -i toc-macro.t2t -t aat --toc --width 60 --toc-title "My Own TOC, the title 1 above is not"   -o toc-macro.aat
$t2t -i toc-macro.t2t -t aat --slides --width 60            -o no-toc-macro-slides.aat
$t2t -i toc-macro.t2t -t aat --toc --slides --width 60      -o toc-macro-slides.aat

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

echo
echo
echo "Running txt2tagslite"

t2tlite="../../txt2tagslite --no-rc"

$t2tlite -i sample.t2t -t aat                                   -o default.txt
$t2tlite -i sample.t2t -t aap          --width 80               -o slides.txt
$t2tlite -i sample.t2t -t aap          --width 60               -o slides-60.txt
$t2tlite -i sample.t2t -t aap          --width 60 --height 30   -o slides-60.30.txt
$t2tlite -i sample.t2t -t aat --toc                             -o toc.txt
$t2tlite -i sample.t2t -t aap --toc          --width 60         -o toc-slide.txt
$t2tlite -i sample.t2t -t aat --toc-only                        -o toc-only.txt
$t2tlite -i sample.t2t -t aap --toc-only          --width 60    -o toc-only-slides.txt

$t2tlite -i sample.t2t -t aat --no-headers                                   -o default-no-headers.txt
$t2tlite -i sample.t2t -t aap --no-headers          --width 60               -o slides-60-no-headers.txt
$t2tlite -i sample.t2t -t aat --no-headers --toc                             -o toc-no-headers.txt
$t2tlite -i sample.t2t -t aap --no-headers --toc          --width 60         -o toc-slide-no-headers.txt

$t2tlite -i toc-macro.t2t -t aat --width 60                     -o no-toc-macro.txt
$t2tlite -i toc-macro.t2t -t aat --toc --width 60 --toc-title "My Own TOC, the title 1 above is not"   -o toc-macro.txt
$t2tlite -i toc-macro.t2t -t aap          --width 60            -o no-toc-macro-slides.txt
$t2tlite -i toc-macro.t2t -t aap --toc          --width 60      -o toc-macro-slides.txt

errors=0
for file in *.txt
do
        fileok=${file:0:-3}aat
	if ! test -f ok/$fileok
	then
		echo "File not found: ok/$fileok (test skipped)"
		continue
	fi
	
	differences=$(diff $file ok/$fileok)
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
