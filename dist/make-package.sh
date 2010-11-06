#!/bin/bash
# make-package.sh - Create the txt2tags .tgz for the new release
# by Aurelio Jargas

cd $(dirname "$0")/..  # enter into SVN root dir

ROOT="$PWD"
DIST="$PWD/dist"
t2t="$ROOT/txt2tags"

YEAR=$(date +%Y)
VERSION=$(LANG= $t2t -V | sed '/txt2tags/!d; s/.*sion //; s/ <.*//')
NAME=txt2tags-$VERSION

OUTDIR="/tmp/$NAME"
TGZ="$OUTDIR.tgz"
FILES=$DIST/files/$NAME.txt

# Flags to turn ON (1) or OFF (0) steps. Default is 1 to all.
f_doc_update=1
f_doc_check=1
f_code_check=1
f_cleanup=1
f_copy=1
f_tgz=1
f_tgz_check=1

##############################################################################

diffc(){ # Diff output with green/red lines instead +/-
 	local esc=$(printf "\033")
	sed "
		s/^-\(.*\)/$esc[31;1m\1$esc[m/;
		s/^+\(.*\)/$esc[32;1m\1$esc[m/
	"
}
hecho(){ echo -e "\033[36;1m$*\033[m"; }

##############################################################################


echo "SVN ROOT: $ROOT"
echo "FILES   : $FILES"
echo "PACKAGE : $OUTDIR"
echo "TGZ     : $TGZ"
echo
echo "--------- Continue? --------- [^C to cancel]"
read

hecho ------------------------------------------------------------------------
hecho ---- UPDATE DOCS

if test $f_doc_update != 1
then
	echo "Skipping conversion."
else
	hecho "Converting Changelog"
	$t2t -t txt ChangeLog.t2t

	# OK
	hecho "Converting Man Pages" # -f !
	extras/html-update.sh -f -c -p $t2t -t man -E .man doc |
		grep -v 'man needs update:'

	### removed from package
	# hecho "Converting HTML docs"
	# extras/html-update.sh -c -p $t2t doc

	### removed from package
	# hecho "Converting Markup Demo"
	# [ "doc/markup/" -nt "doc/markup.html" ] &&
	# 	$t2t doc/markup/markup.t2t
	# for dir in doc/[A-Z][a-z]*/markup-*/; do
	# 	[ "$dir" -nt "${dir%/}.html" ] &&
	# 		$t2t ${dir}markup-*.t2t
	# done

	### removed from package
	# hecho "Converting Markup Rules"
	# cd doc/rules && ./gensource && cd -
	# cd doc/rules && ../../txt2tags rules.t2t && cd -
	
	### removed from package
	# hecho "Converting User Guides"
	# for dir in doc/[A-Z][a-z]*/userguide-*/; do
	# 	[ "$dir"/userguide*.t2t -nt "${dir%/}.pdf" ] && {
	# 		cd "$dir" && ./pdfgen && cd - ; }
	# done

	hecho "Converting User Guide"
	cd doc/English/userguide/ && ./pdfgen && cd -

	hecho "Converting samples"
	rm -fv samples/sample.{out,aux,log,toc,tex.bak,pdf}
	for t in $($t2t --targets | cut -f 1); do
		$t2t -t $t samples/sample.t2t
	done
	$t2t -t art --slides -i samples/sample.t2t -o samples/sample-slides-80x25.art

	hecho "Converting CSS samples"
	samples/css/gen
fi


hecho ------------------------------------------------------------------------
hecho ---- CHECK UP

if test $f_doc_check != 1
then
	echo "Skipping docs checking."
else
	# ChangeLog
	hecho "ChangeLog: searching for lines >80 columns"
	sed "s/$(echo -ne '\t')/        /g" ChangeLog | egrep '.{81}'

	# Man page
	hecho "Man Page: checking year in header"
	sed -n 3p doc/English/manpage.t2t | grep -qs "$YEAR$" || echo FAIL
	hecho "Man Page: checking year of Copyright"
	grep -qs "Copyright.*$YEAR" doc/English/manpage.man || echo FAIL

	# Man page - Portuguese
	hecho "Man Page (pt): checking year in header"
	sed -n 3p doc/Portuguese/manpage-pt.t2t | grep -qs "$YEAR$" || echo FAIL
	hecho "Man Page (pt): checking year of Copyright"
	grep -qs "Copyright.*$YEAR" doc/Portuguese/manpage-pt.man || echo FAIL
fi


if test $f_code_check != 1
then
	echo "Skipping code checking."
else
	hecho "Web interface: checking if is_standalone is turned ON"
	grep -qs '^\$is_standalone = 1;$' extras/txt2tags.php || echo FAIL

	# test-suite
	hecho "Test-suite: searching for error files"
	ls -1 test/*/error/* 2>/dev/null

	# Source code
	$DIST/check-code.sh
fi


hecho ------------------------------------------------------------------------
hecho ---- CLEAN UP

if test $f_cleanup != 1
then
	echo "Skipping clean up."
else
	hecho "Removing .DS_Store files (Mac)"
	find . -type f -name .DS_Store -exec rm -v {} \;

	hecho "Removing .pyc files"
	find . -type f -name *.pyc -exec rm -v {} \;

	hecho "Removing temporary PO files"
	rm -fv po/*.{new,old,mo}
	rm -fv po/messages

	hecho "Removing empty error folders in test-suite"
	rmdir test/*/error/ 2>&1 | grep -v 'No such file or directory'
fi


hecho ------------------------------------------------------------------------
hecho ---- COPY FILES

if test $f_copy != 1
then
	echo "Skipping copy."
else
	hecho "Create the empty package folder"
	test -d $OUTDIR && rm -r ${OUTDIR:-XXXNOTFOUNDXXX}
	mkdir $OUTDIR || { echo FAIL; exit 1; }

	# XXX use rsync instead cp (attention to -X)
	hecho "Copy files and folders, except /doc"
	cp -Rp -X \
		extras samples po test \
		COPYING README ChangeLog \
		txt2tags \
		$OUTDIR

	hecho "Create /doc in package"
	mkdir $OUTDIR/doc/ || { echo FAIL; exit 1; }

	hecho "Copy files to package /doc"
	cp -Xp doc/English/*.pdf $OUTDIR/doc/       # PDF: User Guide and quickref
	cp -Xp doc/English/manpage.man $OUTDIR/doc/ # manpage
	cp -Xp doc/English/manpage.t2t $OUTDIR/doc/ # manpage sources
	cp -Xp doc/*/manpage*.man $OUTDIR/doc/      # manpage translations

	# remove private files
	# rm -r  $OUTDIR/po/tools
	rm     $OUTDIR/samples/css/gen
	rm     $OUTDIR/test/escaping.t2t
	rm     $OUTDIR/po/tools/pygettext.py
	cp -Xp po/tools/pygettext.py $OUTDIR/po/tools/
	
	# remove SVN folders
	find $OUTDIR -type d -name .svn -exec rm -rf {} \; 2>/dev/null
fi


hecho ------------------------------------------------------------------------
hecho ---- MAKE PACKAGE

if test $f_tgz != 1
then
	echo "Skipping package creation."
else
	hecho "Making tgz"
	(cd $OUTDIR/.. && tar czf $NAME.tgz $NAME)
fi


hecho ------------------------------------------------------------------------
hecho ---- CHECK PACKAGE

if test $f_tgz_check != 1
then
	echo "Skipping package check."
	exit
fi

#-----------------------------------------------------------------------------
hecho "Extract information from the package"

cd $OUTDIR
tgz_size=$(   du -hs "$TGZ" | cut -f1)
folder_size=$(du -hs .      | cut -f1)
nr_files=$(   find . -type f | wc -l | tr -d ' ')
nr_folders=$( find . -type d -mindepth 1 | wc -l | tr -d ' ')


echo -n "$tgz_size .tgz, $folder_size dir, $nr_files files, "
echo "$nr_folders folders"

#-----------------------------------------------------------------------------
hecho "Check permissions (chmod)"

# Find files with wrong permissions
chmod_folder=$(find . -type d -not -perm 0755 -mindepth 1)
chmod_file=$(  find . -type f -not -perm 0644)
chmod_file2=$( find . -type f -not -perm 0644 -and -not -perm 0755)

# Exclude known executables from file permission check
chmod_file=$(echo "$chmod_file" | egrep -vw \
'\./(extras/(html-update.sh|t2tmake.rb|t2tconv|gensite|dynartslides)|txt2tags|test/run.py|test/(art|sample)/run.sh|po/tools/(pygettext.py|(update-pot?|stats).sh))$')

# Show results
hecho '--- !644 files'      ; test -n "$chmod_file"   && echo "$chmod_file"
hecho '--- !755 folders'    ; test -n "$chmod_folder" && echo "$chmod_folder"
hecho '--- !644 !755 files' ; test -n "$chmod_file2"  && echo "$chmod_file2"


#-----------------------------------------------------------------------------
hecho "List added/removed files"

# Save package contents listing
$DIST/list-package-files.sh "$TGZ" > $FILES

# Save the file names from the package listings
this_version_files=$(sed 's|.* txt2tags-.../||' "$FILES")
prev_version_files=$(sed 's|.* txt2tags-.../||' $(find $DIST/files | tail -n 2 | sed -n 1p))

# Discover new and removed files for this release
files_diff=$(
	diff -U 0 <(echo "$prev_version_files") <(echo "$this_version_files") |
	grep '^[+-][^+-]' |
	diffc
)

# Show results
test -n "$files_diff" && echo "$files_diff"


#-----------------------------------------------------------------------------
hecho '--- Search Mac hidden files'
grep -F ._ $FILES


