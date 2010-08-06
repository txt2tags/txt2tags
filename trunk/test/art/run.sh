# 2010-08-06
# Quick and dirty tests for Art target.
# TODO Rewrite in Python, integrate into test-suite (run.py)

txt2tags -i sample.t2t -t art                                   -o default.art
txt2tags -i sample.t2t -t art --slides                          -o slides.art
txt2tags -i sample.t2t -t art --slides --width 60               -o slides-60.art
txt2tags -i sample.t2t -t art --slides --width 60 --height 30   -o slides-60x30.art
txt2tags -i sample.t2t -t art --toc                             -o toc.art
txt2tags -i sample.t2t -t art --toc --slides --width 60         -o toc-slide.art
txt2tags -i sample.t2t -t art --toc-only                        -o toc-only.art
txt2tags -i sample.t2t -t art --toc-only --slides --width 60    -o toc-only-slides.art

txt2tags -i sample.t2t -t art --no-headers                                   -o default-no-headers.art
txt2tags -i sample.t2t -t art --no-headers --slides --width 60               -o slides-60-no-headers.art
txt2tags -i sample.t2t -t art --no-headers --toc                             -o toc-no-headers.art
txt2tags -i sample.t2t -t art --no-headers --toc --slides --width 60         -o toc-slide-no-headers.art

txt2tags -i toc-macro.t2t -t art --toc --width 60               -o toc-macro.art
txt2tags -i toc-macro.t2t -t art --toc --slides --width 60      -o toc-macro-slides.art
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
