#!/bin/bash
# 2010-12-03 Aurelio Jargas
#
# Quick and dirty tests for the outfile path.
# NOT integrated into main test suite, you must run it alone.
#

cd $(dirname "$0")
mypath=$PWD
out="out.txt"
t2t="$mypath/../../txt2tags --no-rc -t txt -H"

set -e  # Abort if txt2tags returned an error

reset() {
	rm -f $out folder/$out folder/subfolder/$out.txt
}
new() {
	echo "---- $*"
}
check() {
	if ! test -f "$1"
	then
		echo "FAIL! expected $1"
		exit 1
	else
		rm "$1"
	fi
}

cd "$mypath"

test -d folder || mkdir folder
test -d folder/subfolder || mkdir folder/subfolder

reset

new '(1) from current folder'
$t2t -i current.t2t                             ; check $out
$t2t -i folder.t2t                              ; check folder/$out
$t2t -i subfolder.t2t                           ; check folder/subfolder/$out
$t2t -i folder/folder.t2t                       ; check folder/$out
$t2t -i folder/subfolder/subfolder.t2t          ; check folder/subfolder/$out

new '(2) from parent folder'
cd ..
$t2t -i outfile/current.t2t                     ; check outfile/$out
$t2t -i outfile/folder.t2t                      ; check outfile/folder/$out
$t2t -i outfile/subfolder.t2t                   ; check outfile/folder/subfolder/$out
$t2t -i outfile/folder/folder.t2t               ; check outfile/folder/$out
$t2t -i outfile/folder/subfolder/subfolder.t2t  ; check outfile/folder/subfolder/$out
cd outfile

new '(3) from subfolder'
cd folder/subfolder
$t2t -i ../../current.t2t                       ; check ../../$out
$t2t -i ../../folder.t2t                        ; check ../../folder/$out
$t2t -i ../../subfolder.t2t                     ; check ../../folder/subfolder/$out
$t2t -i ../../folder/folder.t2t                 ; check ../../folder/$out
$t2t -i ../../folder/subfolder/subfolder.t2t    ; check ../../folder/subfolder/$out
cd ../..

new '(4) from current folder using -o'  #  overrides %!option
$t2t -i folder.t2t                      -o $out ; check $out
$t2t -i subfolder.t2t                   -o $out ; check $out
$t2t -i folder/folder.t2t               -o $out ; check $out
$t2t -i folder/subfolder/subfolder.t2t  -o $out ; check $out
$t2t -i current.t2t -o folder/$out              ; check folder/$out
$t2t -i current.t2t -o folder/subfolder/$out    ; check folder/subfolder/$out

new '(5) from parent folder using -o'
cd ..
$t2t -i outfile/current.t2t -o outfile/$out        ; check outfile/$out
$t2t -i outfile/current.t2t -o outfile/folder/$out ; check outfile/folder/$out
cd outfile

new '(6) from subfolder using -o'
cd folder/subfolder
$t2t -i ../../current.t2t -o $out               ; check $out
$t2t -i ../../current.t2t -o ../$out            ; check ../$out
$t2t -i ../../current.t2t -o ../../$out         ; check ../../$out
cd ../../

# If we got here, everything is OK

nr_tests=$(grep 'check ' "$mypath/run.sh" | wc -l | tr -d ' \t')
echo
echo Module outfile, $nr_tests tests made.
echo All files are OK
