#!/bin/bash
# 2010-11-11 Aurelio Jargas
#
# Quick and dirty tests for path related features.
# NOT integrated into main test suite, you must run it alone.


cd $(dirname "$0")

t2t=../../txt2tags
t=creole


# Automatic relative PATH adjustment for images and local URIs.
# See issues 62, 63.
#
# RULES:
#
# We just make the path adjustment when BOTH source and output files
# are real files, not STDIN/STDOUT or MODULE execution. The final path
# will be relative from source folder to output folder.
#
# We could use PWD as the path for STDIN/STDOUT, and make the adjustments,
# but it would confuse the user, giving different results depending on
# what's the current execution folder. Also, the current rule is simplier
# to explain and understand. KISS.
# 
# Maybe in the future this could be a setting or a command line option.


test -d folder || mkdir folder

########################################################################
# Execution from source file folder

# Regular files
$t2t -H -t $t -i relative-path.t2t -o        from-source-same-folder.$t
$t2t -H -t $t -i relative-path.t2t -o folder/from-source-diff-folder.$t

# STDIN
cat relative-path.t2t | $t2t -H -t $t -i - -o        from-source-same-folder-stdin.$t
cat relative-path.t2t | $t2t -H -t $t -i - -o folder/from-source-diff-folder-stdin.$t

# STDOUT
$t2t -H -t $t -i relative-path.t2t -o - >        from-source-same-folder-stdout.$t
$t2t -H -t $t -i relative-path.t2t -o - > folder/from-source-diff-folder-stdout.$t

# STDIN + STDOUT
cat relative-path.t2t | $t2t -H -t $t -i - -o - >        from-source-same-folder-stdinout.$t
cat relative-path.t2t | $t2t -H -t $t -i - -o - > folder/from-source-diff-folder-stdinout.$t

########################################################################
# Execution from output folder

cd folder
t2t=../$t2t

# Regular files
$t2t -H -t $t -i ../relative-path.t2t -o ../from-output-same-folder.$t
$t2t -H -t $t -i ../relative-path.t2t -o    from-output-diff-folder.$t

# STDIN
cat ../relative-path.t2t | $t2t -H -t $t -i - -o ../from-output-same-folder-stdin.$t
cat ../relative-path.t2t | $t2t -H -t $t -i - -o    from-output-diff-folder-stdin.$t

# STDOUT
$t2t -H -t $t -i ../relative-path.t2t -o - > ../from-output-same-folder-stdout.$t
$t2t -H -t $t -i ../relative-path.t2t -o - >    from-output-diff-folder-stdout.$t

# STDIN + STDOUT
cat ../relative-path.t2t | $t2t -H -t $t -i - -o - > ../from-output-same-folder-stdinout.$t
cat ../relative-path.t2t | $t2t -H -t $t -i - -o - >    from-output-diff-folder-stdinout.$t

########################################################################

cd ..
mv folder/* .
rmdir folder

errors=0
for file in *.$t
do
	if ! test -f ok/$file
	then
		# touch ok/$file
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

# Statistics
nr_tests=$(ls -1 ok/ | wc -l)
module=${PWD##*/}

echo
echo "Module $module," $nr_tests "tests made."

if test $errors -eq 0
then
	echo "All files are OK"
else
	echo
	echo "Found errors here (compare with 'ok' folder):"
	ls -1 | egrep -v '(t2t|sh|ok)$'
fi
