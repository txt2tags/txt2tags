#!/bin/bash
# update-pot.sh
# 2004-05-30 Aurelio Jargas
# 2010-06-18 now using pygettext instead home-made sed, charset:utf-8 instead iso-8859-1

src=../../txt2tags
pot=../txt2tags.pot
version=$(LANG= "$src" -V | sed '/txt2tags/!d;s/.*sion //;s/ .*//')

# get pygettext.py from http://svn.python.org/projects/python/trunk/Tools/i18n/pygettext.py
#
python pygettext.py -a --no-location -o - "$src" |
	sed "
		/^# SOME DESCRIPTIVE TITLE./ s/SOME.*/txt2tags messages/
		/^# Copyright (C) YEAR ORGANIZATION/ d
		/^# FIRST AUTHOR <EMAIL@ADDRESS>/ d
		/^#$/ s/.*/#, fuzzy/
		
		/^.Project-Id-Version:/ {
			s/PACKAGE/txt2tags/
			s/VERSION/$version/
		}
		/^.Content-Type:/ s/CHARSET/UTF-8/
		/^.Content-Transfer-Encoding:/ s/ENCODING/8bit/
	" > "$pot.new" 

diff -u "$pot" "$pot.new"

echo
echo "---- Move $pot.new to $pot? [Yn]"
read YN

if test "$YN" != n -a "$YN" != N
then
	mv -v "$pot.new" "$pot"
	echo
	echo "---- Saved $pot"
else
	rm "$pot.new"
	echo
	echo "---- Update cancelled."
fi



#### Obsoleted my old home-made sed method
# (
#   echo "$header" | sed "s/%DATE%/$currdate/ ; s/%VERSION%/$version/"
# 
#   # extract from python code
#   # 0. join multiline messages into one
#   # 1. grep just the message
#   # 2. remove duplicated lines (not consecutive also)
#   # 3. insert msgid and msgstr
#   # 4. make line breaks
# 
#   # XXX: needs GNU sed
#   # sed -n "s/.*_(\('\([^']*\)'\|\"\(.*\)\"\)[	 ]*).*/\2\3/p" |
#   sed "/.*_([^)]*$/{N;s/\n//;}" $src |
#   sed -n "
#   	s/.*_('\([^']*\)'[	 ]*).*/\1/p
#   	s/.*_(\"\(.*\)\"[	 ]*).*/\1/p" |
#   cat -n - | sort -k2 | uniq -f1 | sort -n | cut -f2- |
#   sed -n "s/.*/msgid \"&\"#msgstr \"\"#/p" |
#   tr '#' '\n'
# ) > $pot
