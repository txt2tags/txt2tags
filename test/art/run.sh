# 2010-08-06
# Quick and dirty tests for Art target.
# TODO Rewrite in Python, integrate into test-suite (run.py)

txt2tags -i sample.t2t -t art                                   -o default.art
txt2tags -i sample.t2t -t art --slides                          -o slides.art
txt2tags -i sample.t2t -t art --slides --width 60               -o slides-60.art
txt2tags -i sample.t2t -t art --slides --width 60 --height 30   -o slides-60x30.art
txt2tags -i sample.t2t -t art --toc                             -o toc.art
txt2tags -i sample.t2t -t art --toc-only                        -o toc-only.art
txt2tags -i sample.t2t -t art --toc-only --slides --width 60    -o toc-only-slides.art
txt2tags -i sample.t2t -t art --toc --slides --width 60         -o toc-slide.art

errors=0
for file in *.art
do
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
