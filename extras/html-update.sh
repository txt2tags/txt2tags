#!/bin/bash
# html-update.sh - converts to HTML all .t2t files that has changed
#
# Author: Aurelio Jargas
# Requires: bash, find, txt2tags
# Debut: June, 2004
# Last Update: 27 Sep 2005
#
# Based on Guaracy Monteiro's t2tmake.rb program.
# Implemented some ideas from Mauricio Teixeira (netmask).
#
# This file is part of the txt2tags (http://txt2tags.sf.net) project.
# Its license is the same as the program: GPL. See txt2tags COPYING
# file for a detailed explanation of the GPL license.
#
# INSTRUCTIONS
#
#   With no options, it searches recursively the current directory and
#   prints on the screen all the filenames that needs to be converted.
#
#   With the '-c' option, it performs the conversion of the found
#   files.
#
#   With a directory path as the last argument, it searches that
#   directory instead the current dir.
#
#   Use the --help option for more information.
#
# NOTES
#
#   The condition to a file be considered 'needed' to be converted is
#   that the .t2t file is newer than its respective .html. In other
#   words, you edited the .t2t after the last conversion, so it needs
#   to be converted again. You can ignore this checking using the
#   --force option.
#
#   It assumes that the .html file uses the same basename as the .t2t
#   file. If you used the txt2tags' --outfile option to change the
#   default output filename ou extension, it will not be detected by
#   this script. You can force this detection using the --missing
#   option.
#
# CONFIG
#
#   If you call txt2tags any other way, change here
PROGRAM=txt2tags
#
#   If you use another extension for your txt2tags files, change here
IN_EXT=.t2t
#
#   If you want to use this script for other formats than HTML
OUT_EXT=.html
TARGET=html
#
#   The default message for --interative question
QUESTION="   Convert? [yn] "
#
#   The --verbose messages
VERB_DIR="Will scan this dir:"
VERB_FILE="Scanning this file:"
#
#####################################################################

# Atention: program code starts here, do not edit from this point

PROGNAME=${0##*/}
USAGE="
$PROGNAME - part of the txt2tags project

Usage: $PROGNAME [-c] [-f] [-m] [-i] [directory]

  -c, --convert       Perform the conversion of the marked files
  -f, --force         Mark all .t2t files, even if up-to-date
  -m, --missing       Mark .t2t files that has no .html
  -i, --interative    Ask before convert
  -e, --in-ext        Set other source extension than .t2t
  -E, --out-ext       Set other target extension than .html
  -t, --target        Force a target type when converting (default: html)
  -p, --program       Set an alternative way to call txt2tags
  -v, --verbose       Show all scanned file names
  -h, --help          Show this help screen

Common use: $PROGNAME -c /path/to/dir
Stress use: $PROGNAME -c -f -m -i /path/to/dir
"

# Flags reset status
f_help=0
f_force=0
f_convert=0
f_missing=0
f_verbose=0
f_interative=0

# Command line options parsing
while [ "$1" ] ; do
	case "$1" in
		-h|--help      ) f_help=1 ;;
		-f|--force     ) f_force=1 ;;
		-m|--missing   ) f_missing=1 ;;
		-c|--convert   ) f_convert=1 ;;
		-v|--verbose   ) f_verbose=1 ;;
		-i|--interative) f_interative=1 ;;
		-e|--in-ext    ) IN_EXT="$2" ; shift;;
		-E|--out-ext   ) OUT_EXT="$2"; shift;;
		-t|--target    ) TARGET="$2" ; shift;;
		-p|--program   ) PROGRAM="$2"; shift;;
		*) break ;;
	esac
	shift
done

# Show help screen and exit
if [ "$f_help" = 1 ]; then
	echo "$USAGE"
	exit 0
fi

# Set directory to user passed parameter or current one
udir="${1:-.}"

# The directory is valid (does exist)?
if [ ! -d "$udir" ] ; then
	echo "$PROGNAME: Sorry, '$udir' is not a valid directory"
	exit 1
fi

# The default message showed before the filename
MESSAGE="$TARGET needs update:"

# Show scanned directory name
[ "$f_verbose" = 1 ] && echo "$VERB_DIR $udir"

# IFS+for trick try to avoid "find | while read" that mess -i
IFS="
"

# Search for all .t2t files on the specified (or current) dir
for t2t in $(find "$udir" -name "*$IN_EXT"); do

	# Show scanned file name
	[ "$f_verbose" = 1 ] && echo "$VERB_FILE $t2t"
	
	# Set the out file name as <file>.TARGET
	out=${t2t%$IN_EXT}$OUT_EXT

	# Flag that will tell if the conversion should be done
	f_ok=0

	# Force flag
	if [ -f "$out" -a "$f_force" = 1 ]; then
		f_ok=1

	# Missing flag
	elif [ ! -f "$out" -a "$f_missing" = 1 ] ; then
		f_ok=1
	
	# If the .t2t is newer than the .TARGET...
	elif [ -f "$out" -a "$t2t" -nt "$out" ] ; then
		f_ok=1
	fi

	# Okay, the conversion may be done
	if [ "$f_ok" = 1 ]; then
		echo -n "$MESSAGE $t2t"
		
		# Last chance to give up
		if [ "$f_convert" = 1 -a "$f_interative" = 1 ]; then
			echo -n "$QUESTION"
			read -n 1 ans
			[ "$ans" = y -o "$ans" = Y ] || f_ok=0
		fi	
		echo

		# Yes, we will
		if [ "$f_convert" = 1 -a "$f_ok" = 1 ]; then
			$PROGRAM -t $TARGET $t2t
		fi
	fi	
done
