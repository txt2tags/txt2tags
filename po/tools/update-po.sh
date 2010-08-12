#!/bin/bash
# update-po.sh
# 2004-05-30 Aurelio Marinho Jargas
# 2010-06-18 renamed to update-po.sh, pot extraction moved to update-pot.sh
#
# You get the msgmerge/msgfmt commands from gettext package.
# On the Mac, download gettext at http://rudix.org
#
# Tips:
#
#   1. To generate the .mo file:
#      msgfmt -o de.mo de.po
#
#   2. To install the mo file:
#      su -c "cp -v de.mo /usr/share/locale/de/LC_MESSAGES/"
#

cd ..  # Operate on the 'po' folder

pot=txt2tags.pot

becho(){ echo -e "\033[36;1m$*\033[m"; }

for po in *.po; do
	clear
	becho "=============================================="
	becho "$po"
	becho "=============================================="
	becho
	becho "--------- Merging pot changes into $po"
	msgmerge --no-fuzzy-matching $po $pot > $po.new
	rm -f messages.mo

	becho "--------- Any difference?"
	diff -u $po $po.new

	becho "--------- Update $po? [Yn]"
	read YN
	
	if test "$YN" != n -a "$YN" != N
	then
		mv -v $po $po.old
		mv -v $po.new $po
	fi

	becho "--------- Stats for $po"
	msgfmt -c --statistics $po
	
	becho
	becho "$po done    (Press Enter to continue)"
	read foo
done
