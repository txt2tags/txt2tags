#!/bin/bash
# list-package-files.sh - List .tgz file contents sorted and cleaner
# by Aurelio Jargas

# Check if input file exists
test -n "$1" -a -e "$1" || {
	echo "$(basename $0) FILE.tgz"
	exit 1
}

LANG=C					# Dates in English
tar tvzf "$1" |				# Get file listing
	tr -s ' ' '\t' |		# Delimit fields by TABs
	cut -f 1,5- |			# Remove fields: node, owner, group
	sort -k 6 --ignore-case |	# Sort by file name, ignoring case
	while read LINE			# Format output
	do
		printf "%s %8s %s %2s %s %s\n" $LINE
	done
