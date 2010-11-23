#!/bin/bash
# check-code.sh - Checks txt2tags code
# by Aurelio Jargas

t2t=../txt2tags

hecho(){ echo -e "\033[36;1mCode: $*\033[m"; }

cd $(dirname "$0")

hecho 'checking shebang'
[ "$(head -1 $t2t)" != "#!/usr/bin/env python" ] && echo FAIL

hecho "checking if executable"
ls -l $t2t | grep -qs '^-rwxr-xr-x' || echo FAIL

hecho "checking year of Copyright"
grep -qs "Copyright.*$(date +%Y)" $t2t || echo FAIL

hecho "searching for !ASCII chars"
grep -v '^[	-~]*$' $t2t  # [TAB-~]

hecho "searching for useless blanks"
egrep '[^ 	][ 	]+$' $t2t | sed -n l  # \S\s$
egrep ' 	' $t2t | sed -n l             # space+TAB
# grep '^ ' $t2t                                # leading space

hecho "searching for lines >80 columns"
# sed "s/$(echo -ne '\t')/        /g" $t2t | egrep '.{81}'
echo DISABLED

hecho "checking PEP-8 compliance"
if pep8 --version >/dev/null 2>&1
then
    pep8 --ignore E203,E221,E241,E501 -r $t2t
else
    echo "pep8 command not installed"
    echo "See http://pypi.python.org/pypi/pep8"
fi
        
hecho 'checking version'
$t2t -V | sed 's/<.*//'

