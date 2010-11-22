
TXT2TAGS=/usr/bin/python2 ../txt2tags 


html: 
	$(TXT2TAGS) -T template -t html talk.t2t

slidy: 
	$(TXT2TAGS) -C slidy.conf.t2t --css-inside -T slidy -t xhtml -o talk.html talk.t2t
	

beamer: 
	$(TXT2TAGS) -C beamer.conf.t2t -T beamer -t tex talk.t2t
	pdflatex talk.tex
