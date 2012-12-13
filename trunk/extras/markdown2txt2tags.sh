#!/bin/sh

# This script converts from markdown to the txt2tags format.
# It requires:
#   - Pandoc (to convert from markdown to html) see http://johnmacfarlane.net/pandoc
#   - html2wiki http://search.cpan.org/~diberri/HTML-WikiConverter-0.68/bin/html2wiki
#   - txt2tags export for html2wiki http://wiki.txt2tags.org/index.php/Main/Html2wiki

case $1 in
	"")
	echo -e "Usage: markdown2txt2tags.sh file_in_markdown_format.md"
	;;
	*)
	echo -e "\n\n\n" > $1.t2t && pandoc -f markdown -t html $1 | html2wiki --dialect Txt2tags |sed -r -e "s@^=@\n=@g" >> $1.t2t
	;;
esac


