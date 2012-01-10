#!/bin/bash
# txt2tags - a generic tagged language text generator
#
# 20010726 <aurelio@verde666.org> ** debut
# TODO allow lists inside quotes? (mgp TAB problems)
# TODO =title=[label] for "local" links (HTML)
# TODO mgp: subquote (increase prefix) ----mmmm, maybe not (big letters, few hspace)
# TODO pm6 : check quote
# TODO moin: list should have leading spaces
#
# BUG: sgml: title after quote left a blank line before </quote>
#
#i pm6: paragraph == 1 line
#
# 20010727 ++mgp: prefix "  " for all lines
#          ++mgp: ^% scape with prefix
# 20010730 ++comments MUST be at ^
# 20010928 ++man target, ++shell wrapper & py together
# 20011109 ++["label" url] tag, ++%%date(fmt)
# 20020104 ++simple table support (with \t TAB \t separated \t fields)
# 20020311 ++lots of fixes on man target: bold, ita, title, pre, lists
#          ++ smarter URL matcher, preformatted lines indented
#          ++--help --version
# 20020322 <>adapted to python v1.5, ++read from STDIN, ++--noheaders
# 20020410 ++--enumtitle ++ordered lists
# 20020703 ++--maskemail


# defaults
stdout=0
noheaders=0
enumtitle=0
maskemail=0
split=0
lang=english
tmpdir=${TMPDIR:-/tmp}

# if you've got a "python: can't open file '--type'" message, uncomment this:
python_v1=1

Usage(){
  local ver types name=${0##*/}
    ver=`sed "/^#my_version = '/!d;s///" $0`
  types=`sed "/^#tags = /!d;s///;s/[][']//g" $0`
  echo "\
$name version ${ver%?} <http://txt2tags.sf.net>

usage: $name -t <type> [--stdout|--noheaders|--enumtitle] file.txt
       $name -t html -s <split level> -l <lang> file.txt

  -t, --type       target document type. actually supported:
                   $types
      --stdout     by default, the output is written to file.<type>
                   with this option, STDOUT is used (no files written)
      --noheaders  suppress header, title and footer information
      --enumtitle  enumerate all title lines as 1, 1.1, 1.1.1, etc
      --maskemail  hide email from spam robots. x@y.z turns to <x (a) y z>

  -h, --help       prints this help information and exits 
  -V, --version    prints program version and exits

extra options for HTML target (needs sgml-tools):
  -s, --split      split documents. values: 0, 1, 2 (default 0)
  -l, --lang       document language (default english)

"
  exit 1
}

case "$1" in
  -h|--help) Usage;;
  -V|--version) Usage | sed q; exit ;;
esac

while [ "$2" ]; do
  case "$1" in
    -t|--type)  [ "$2" ] || Usage; shift; doctype=$1;;
    -s|--split) [ "$2" ] || Usage; shift; split=$1;;
    -l|--lang)  [ "$2" ] || Usage; shift; lang=$1;;
    --noheaders) noheaders=1 ;;
    --enumtitle) enumtitle=1 ;;
    --maskemail) maskemail=1 ;;
    --stdout) stdout=1 ;;
    *) Usage;;
  esac
  shift
done

[ "$1" ] || Usage
TXT="$1"

# data from STDIN
if [ "$TXT" == '-' ]; then
  stdout=1                   # no filename, force STDOUT
  TXT="$tmpdir/txt2tags.txt"; cat - > $TXT ; removetmp=1
  # sux. the python script already takes over STDIN
fi

# sanity
[ -f "$TXT" ] || { echo "file $TXT not found! aborting..."; exit 1; }


name=`basename $TXT .txt`
D=$PWD

fecho(){ echo -e "\033[1m--- $*...\033[m" ; }               # fancyness
checkdoc(){ [ ! -f "$D/$name.$1" -o "$D/$name.$1" -ot "$TXT" ] && doAll $1; }
letsdoit(){
  if [ "$python_v1" ]  # python 1.5 is buggy when using - as filename
  then sed "1,/^##@##/d;s/^#//" $0 > $tmpdir/txt2tags.py
       python $tmpdir/txt2tags.py "$@"
       rm $tmpdir/txt2tags.py
  else sed "1,/^##@##/d;s/^#//" $0 | python - "$@" # nice
  fi
}

dodoc(){ 
  local extra type=$1
  [ $noheaders -eq 1 ] && extra='--noheaders'  
  [ $enumtitle -eq 1 ] && extra="$extra --enumtitle"  
  [ $maskemail -eq 1 ] && extra="$extra --maskemail"  
  if [ $stdout -eq 1 ]; then
    letsdoit $extra --type $type $TXT
  elif [ "$type" == "txt" ]; then
    echo 'hey, --type txt requires --stdout!'
    echo '"shoot on the foot" does mean something to you? &:)'
    # yes, i've got my sample.txt file deleted, then i did this safety test...
  else
    fecho $type; letsdoit $extra --type $type $TXT > $D/$name.$type
    echo "wrote $D/$name.$type"
  fi
}

doAll(){
  case "$1" in
  txt|sgml|pm6|mgp|moin|man)
        dodoc $1
        ;;
  html)
        [ $split -eq 0 ] && { dodoc $1; return; }
        
        ### for splitted html, sgml2html does the job

        # html target dir
        [ -d "$D/$name" ] || mkdir "$D/$name"
        # we have to have an updated .sgml
        checkdoc sgml
        # let's go!
        fecho splitted html
        cd $D/$name ; rm -f $name{,-[0-9]*}.html
        sgml2html --language=$lang --split=$split $D/$name.sgml
        ln -sf $name.html index.html
        ;;
  ps)
        fecho $1
        checkdoc sgml
        sgml2latex -o $1 --language=$lang $D/$name.sgml
        ;;
  pdf)
        fecho $1
        checkdoc ps
        ps2pdf $D/$name.ps
        ;;
  *)
        Usage
  esac
}

doAll $doctype
[ "$removetmp" ] && rm $TXT

  

##@##
#import re, string, os, sys, getopt
#from time import strftime,time,localtime
#
#
#my_url = 'http://txt2tags.sourceforge.net'
#my_email = 'aurelio@verde666.org'
#my_version = '0.8'
#
#f_noheaders = f_enumtitle = f_maskemail = 0
#doctype = ''
#usage = 'usage: %s [--noheaders|--enumtitle|--maskemail] --type <type> file.txt|-\n'%(sys.argv[0])
#
## get cmdline options
#errormsg = 'bad option or missing argument. try --help.'
#try: (opt, args) = getopt.getopt(sys.argv[1:], '',
#     ['noheaders', 'enumtitle', 'maskemail', 'type='])
#except getopt.GetoptError: print errormsg+'\n'+usage; sys.exit(1)
#for o in opt:
#	if   o[0] == '--noheaders': f_noheaders = 1
#	elif o[0] == '--enumtitle': f_enumtitle = 1
#	elif o[0] == '--maskemail': f_maskemail = 1
#	elif o[0] == '--type'     : doctype = o[1]
#if not args or not doctype: print usage; sys.exit(1)
#file = args[0]
#
#tags = ['txt', 'sgml', 'html', 'pm6', 'mgp', 'moin', 'man']
#try: T = tags.index(doctype)
#except ValueError:
#	print "invalid document type '%s'"%(doctype)
#	print usage
#	sys.exit(1)
#
#if file != '-' and not os.path.isfile(file):
#	print 'file not found:',file
#	sys.exit(1)
#
#
#### all the registered tags
#TAGparagraph = ['', '<p>', '<P>', '<@Normal:>', '%font "normal", size 5\n', '', '.P']
#TAGtitle1 = ['  \a'      , '<sect>\a<p>' , '<H1>\a</H1>', '\n<@Title1:>\a', '%page\n\n\a', '= \a =', '.SH \a']
#TAGtitle2 = ['\t\a'      , '<sect1>\a<p>', '<H2>\a</H2>', '\n<@Title2:>\a', '%page\n\n\a', '== \a ==', '.SS \a']
#TAGtitle3 = ['\t\t\a'    , '<sect2>\a<p>', '<H3>\a</H3>', '\n<@Title3:>\a', '%page\n\n\a', '=== \a ===', '.SS \a']
#TAGtitle4 = ['\t\t\t\a'  , '<sect3>\a<p>', '<H4>\a</H4>', '\n<@Title4:>\a', '%page\n\n\a', '==== \a ====', '.SS \a']
#TAGtitle5 = ['\t\t\t\t\a', '<sect4>\a<p>', '<H5>\a</H5>', '\n<@Title5:>\a', '%page\n\n\a', '===== \a =====', '.SS \a']
#TAGareaPreOpen = ['',  '<tscreen><verb>',   '<PRE>', '<@PreFormat:>', '\n%font "mono"', '{{{', '.nf']
#TAGareaPreClose = ['', '</verb></tscreen>', '</PRE>', '', '%font "normal"', '}}}', '.fi\n']
#TAGareaQuoteOpen = ['    ',   '<quote>', '<BLOCKQUOTE>', '<@Quote:>', '%prefix "       "', ' ', '\n']
#TAGareaQuoteClose = ['', '</quote>', '</BLOCKQUOTE>', '', '%prefix "  "', '', '\n']
#TAGfontMonoOpen  = ['',  '<tt>',  '<CODE>', '<FONT "Lucida Console"><SIZE 9>', '\n%cont, font "mono"\n', '{{{', '']
#TAGfontMonoClose = ['', '</tt>', '</CODE>', '<SIZE$><FONT$>', '\n%cont, font "normal"\n', '}}}', '']
#TAGfontBoldOpen  = ['',  '<bf>',  '<B>', '<B>', '\n%cont, font "normal-b"\n', "'''", r'\\fB']
#TAGfontBoldClose = ['', '</bf>', '</B>', '<P>', '\n%cont, font "normal"\n', "'''", r'\\fP']
#TAGfontItalicOpen  = ['',  '<em>',  '<I>', '<I>', '\n%cont, font "normal-i"\n', "''", r'\\fI']
#TAGfontItalicClose = ['', '</em>', '</I>', '<P>', '\n%cont, font "normal"\n', "''", r'\\fP']
#TAGfontBoldItalicOpen  = ['',  '<bf><em>',   '<B><I>', '<B><I>', '\n%cont, font "normal-bi"\n', "'''''", '\n.BI ']
#TAGfontBoldItalicClose = ['', '</em></bf>', '</I></B>', '<P>',   '\n%cont, font "normal"\n', "'''''", '\n\\&']
#TAGfontUnderlineOpen = ['', TAGfontBoldItalicOpen[1], '<U>', '<U>', '\n%cont, fore "cyan"\n', TAGfontBoldItalicOpen[5], '']
#TAGfontUnderlineClose = ['', TAGfontBoldItalicClose[1], '</U>', '<P>', '\n%cont, fore "white"\n', TAGfontBoldItalicClose[5], '']
#TAGlistOpen     = ['', '<itemize>', '<UL>', '<@Bullet:>', '', '', '\n'+TAGareaPreOpen[6]]
#TAGlistClose    = ['', '</itemize>', '</UL>', '', '', '', TAGareaPreClose[6]]
#TAGlistItem     = ['- ', '<item>', '<LI>', '•	', '', '* ', '* ']
#TAGnumlistOpen  = ['', '<enum>', '<OL>', '<@Bullet:>', '', '', '\n'+TAGareaPreOpen[6]]
#TAGnumlistClose = ['', '</enum>', '</OL>', '', '', '', TAGareaPreClose[6]]
#TAGnumlistItem  = ['\a. ', '<item>', '<LI>', '~U    ', '\a. ', '\a. ', '\a. ']
#TAGdeflistOpen  = ['', '', '<DL>'       , '', '', '', '']
#TAGdeflistItem1 = ['', '', '<DT>\a</DT>', '', '', '', '']
#TAGdeflistItem2 = ['', '', '<DD>'       , '', '', '', ''] #TODO must close?
#TAGdeflistClose = ['', '', '</DL>'      , '', '', '', '']
#TAGbar1 = ['\a', '<!-- \a -->', '<HR NOSHADE SIZE=1>', '\a', '%bar "white" 5', '----', '\n\n']
#TAGbar2 = ['\a', '<!-- \a -->', '<HR NOSHADE SIZE=5>', '\a', '%pause', '----', '\n\n']
#TAGurl = ['\a', '<htmlurl url="\a" name="\a">', '<A HREF="\a">\a</A>', TAGfontUnderlineOpen[3]+'\a'+TAGfontUnderlineClose[3], '\n%cont, fore "cyan"\n\a\n%cont, fore "white"\n', '[\a]', '\a']
#TAGurlMark = ['\a (\a)', TAGurl[1], TAGurl[2], '\a '+TAGurl[3], '\a '+TAGurl[4], '[\a \a]', '\a (\a)']
#TAGemail = ['\a', '<htmlurl url="mailto:\a" name="\a">', '<A HREF="mailto:\a">\a</A>', '\a', TAGurl[4], '[\a]', '\a']
#TAGemailMark = ['\a (\a)', TAGemail[1], TAGemail[2], '\a '+TAGemail[3], '\a '+TAGemail[4], '[\a \a]', '\a (\a)']
#TAGemail = ['\a', '<htmlurl url="mailto:\a" name="\a">', '<A HREF="mailto:\a">\a</A>', '\a', TAGurl[4], '[\a]', '\a']
#TAGimg = ['[\a]', '<figure><ph vspace=""><img src="\a"></figure>', '<IMG ALIGN="\a" SRC="\a">', '\a', '\n%center\n%newimage "\a", left\n', '[\a]', '\a']
#TAGtableOpen     = [ '', '<table><tabular ca="c">', '<table align=center cellpadding=4 border=\a>', '', '', '', '']
#TAGtableLineOpen = [ '', '', '<tr>', '', '', '||', '']
#TAGtableLineClose = [ '', '<rowsep>', '</tr>', '', '', '', '']
#TAGtableCellOpen = [ '', '', '<td>', '', '', '', '']
#TAGtableCellClose = [ '', '<colsep>', '</td>', '', '', '||', '']
#TAGtableTitleCellOpen = [ '', '', '<th>', '', '', '', '']
#TAGtableTitleCellClose = [ '', '<colsep>', '</th>', '', '', '||', '']
#TAGtableClose = [ '', '</tabular></table>', '</table>', '', '', '', '']
#TAGEOD = ['', '</article>', '</BODY></HTML>', '', '%%EOD', '', '']
#
#
#### the cool regexes
#re_title = re.compile(r'^\s*(?P<tag>={1,5})(?P<txt>[^=].*[^=])\1(\[(?P<label>\w+)\])?$')
#re_areaPreOpen = re_areaPreClose = re.compile(r'^---$')
#re_quote = re.compile(r'^\t+')
#re_1linePreOld = re.compile(r'^ {4}([^\s-])')
#re_1linePre = re.compile(r'^--- ')
#re_mono = re.compile(r'`([^`]+)`')
#re_bold = re.compile(r'\*\*([^\s*].*?)\*\*')
#re_italic = re.compile(r'(^|[^:])//([^ /].*?)//')
#re_underline = re.compile(r'__([^_].*?)__') # underline lead/trailing blank
#re_bolditalic = re.compile(r'\*/([^/].*?)/\*')
#re_list    = re.compile(r'^( *)([+-]) ([^ ])')
#re_deflist = re.compile(r'^( *)(=) ([^:]+):')
#re_bar =re.compile(r'^\s*([_=-]{20,})\s*$')
#re_table = re.compile(r'^ *\|\|?[<:>]*\s')
#
## link things
#urlskel = {
#  'proto' : r'(https?|ftp|news|telnet|gopher|wais)://',
#  'guess' : r'(www[23]?|ftp)\.',   # w/out proto, try to guess
#  'login' : r'A-Za-z0-9_.-',       # for ftp://login@domain.com
#  'pass'  : r'[^ @]*',             # for ftp://login:password@domain.com
#  'chars' : r'A-Za-z0-9%._/~:,=-', # %20(space), :80(port)
#  'anchor': r'A-Za-z0-9%.-',       # %nn(encoded)
#  'form'  : r'A-Za-z0-9/%&=+.@*_-',# .@*_-(as is)
#  'punct' : r'.,;:!?'
#}
#patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
#retxt_url = r'\b(%s%s|%s)[%s]+(#[%s]+|\?[%s]+)?(?=[%s]|[^%s]|$)\b'%(
#             urlskel['proto'],patt_url_login, urlskel['guess'],
#             urlskel['chars'],urlskel['anchor'],
#             urlskel['form'] ,urlskel['punct'],urlskel['form'])
#retxt_url_local = r'[%s]+|[%s]*(#[%s]+)'%(
#             urlskel['chars'],urlskel['chars'],urlskel['anchor'])
#retxt_email = r'\b[%s]+@([A-Za-z0-9_-]+\.)+[A-Za-z]{2,4}(\?[%s]+)?\b'%(
#             urlskel['login'],urlskel['form'])
#re_link = re.compile(r'%s|%s'%(retxt_url,retxt_email), re.I)
#re_linkmark = re.compile(r'\[([^]]*) (%s|%s|%s)\]'%(
#             retxt_url, retxt_email, retxt_url_local))
#
#re_x = re.compile('\a')
#re_blankline = re.compile(r'^\s*$')
#re_comment = re.compile(r'^//')
#re_date = re.compile(r'%%date\b(\((?P<fmt>.*?)\))?', re.I)
#re_img = re.compile(r'\[([\w_,.+%$#@!?+~/-][\w_,.+%$#@!?+~/ -]+\.(png|jpe?g|gif|eps|bmp))\]', re.L+re.I)
#
## the defaults
#title = 'document title'
#author = 'author name'
#currdate = strftime('%Y%m%d',localtime(time()))    # ISO current date
#date = currdate
#f_tt = 0
#listident = []
#listids = []
#listcount = []
#titlecount = ['',0,0,0,0,0]
#f_header = 0
#f_lastblank = 0
#holdspace = ''
#listholdspace = ''
#quotedepth = 0
#istable = 0
#tableborder = 0
#tablealign = []
#linkmask = '@@_@_@@'
#monomask = '@@_m_@@'
#
#
#def printHeader(title, author, date):
#	title = string.strip(title)
#	author = string.strip(author)
#	date = string.strip(date)
#	if doctype == 'txt':
#		print "%s\n%s\n%s"%(title,author,date)
#	elif doctype == 'sgml':
#		print "<!doctype linuxdoc system>\n<article>"
#		print "<title>%s\n<author>%s\n<date>%s\n" %(title,author,date)
#	elif doctype == 'html':
#		print '<HTML>\n<HEAD><TITLE>%s</TITLE></HEAD>'%title
#		print '<BODY BGCOLOR="white" TEXT="black">'
#		print '<P ALIGN="center"><CENTER><H1>%s</H1>'%title
#		print '<FONT SIZE=4><I>%s</I><BR>\n%s</FONT></CENTER>\n'%(author,date)
#	elif doctype == 'man':
#		# TODO man section 1 is hardcoded...
#		print '.TH "%s" 1 %s "%s"'%(title,date,author)
#	elif doctype == 'pm6':
#		# TODO style to <HR>
#		# TODO unix2dos before apply
#		print """\
#<PMTags1.0 win><C-COLORTABLE ("Preto" 1 0 0 0)
#><@Normal=
#  <FONT "Times New Roman"><CCOLOR "Preto"><SIZE 11>
#  <HORIZONTAL 100><LETTERSPACE 0><CTRACK 127><CSSIZE 70><C+SIZE 58.3>
#  <C-POSITION 33.3><C+POSITION 33.3><P><CBASELINE 0><CNOBREAK 0><CLEADING -0.05>
#  <GGRID 0><GLEFT 7.2><GRIGHT 0><GFIRST 0><G+BEFORE 7.2><G+AFTER 0>
#  <GALIGNMENT "justify"><GMETHOD "proportional"><G& "ENGLISH">
#  <GPAIRS 12><G% 120><GKNEXT 0><GKWIDOW 0><GKORPHAN 0><GTABS $>
#  <GHYPHENATION 2 34 0><GWORDSPACE 75 100 150><GSPACE -5 0 25>
#><@Bullet=<@-PARENT "Normal"><FONT "Abadi MT Condensed Light">
#  <GLEFT 14.4><G+BEFORE 2.15><G% 110><GTABS(25.2 l "")>
#><@PreFormat=<@-PARENT "Normal"><FONT "Lucida Console"><SIZE 8><CTRACK 0>
#  <GLEFT 0><G+BEFORE 0><GALIGNMENT "left"><GWORDSPACE 100 100 100><GSPACE 0 0 0>
#><@Title1=<@-PARENT "Normal"><FONT "Arial"><SIZE 14><B>
#  <GCONTENTS><GLEFT 0><G+BEFORE 0><GALIGNMENT "left">
#><@Title2=<@-PARENT "Title1"><SIZE 12><G+BEFORE 3.6>
#><@Title3=<@-PARENT "Title1"><SIZE 10><GLEFT 7.2><G+BEFORE 7.2>
#><@Title4=<@-PARENT "Title3">
#><@Title5=<@-PARENT "Title3">
#><@Quote=<@-PARENT "Normal"><SIZE 10><I>>
#"""
#	elif doctype == 'mgp':
#		print """\
##!/usr/X11R6/bin/mgp -t 90
#%deffont "normal"    xfont "utopia-medium-r", charset "iso8859-1"
#%deffont "normal-i"  xfont "utopia-medium-i", charset "iso8859-1"
#%deffont "normal-b"  xfont "utopia-bold-r",   charset "iso8859-1"
#%deffont "normal-bi" xfont "utopia-bold-i",   charset "iso8859-1"
#%deffont "mono"     xfont "courier-medium-r", charset "iso8859-1"
#%default 1 size 5
#%default 2 size 8, fore "yellow", font "normal-b", center
#%default 3 size 5, fore "white",  font "normal", left, prefix "  "
#%tab 1 size 4, vgap 30, prefix "     ", icon arc "red" 40, leftfill
#%tab 2 prefix "            ", icon arc "orange" 40, leftfill
#%tab 3 prefix "                   ", icon arc "brown" 40, leftfill
#%tab 4 prefix "                          ", icon arc "darkmagenta" 40, leftfill
#%tab 5 prefix "                                ", icon arc "magenta" 40, leftfill
#%%%%%%%%%%%%%%%%%%%%%%%%%% end of headers %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%page
#"""
#		# 1st title page
#		print '\n\n\n\n%%size 10, center, fore "yellow"\n%s'%title
#		print '\n%%font "normal-i", size 6, fore "white", center\n%s'%author
#		print '\n%%font "mono", size 7, center\n%s'%date
#
#def printFooter():
#	txt = '%s code generated by txt2tags %s (%s)'%(doctype,my_version,my_url)
#	if doctype == 'sgml' or doctype == 'html': print "<!-- %s -->"%txt
#	elif doctype == 'mgp': print "%%%% %s"%txt
#	elif doctype == 'man': print '.\\" %s'%txt
#	print TAGEOD[T]
#
#def doEscape(txt):
#	if doctype == 'html' or doctype == 'sgml':
#		txt = re.sub('&','&amp;',txt)
#		txt = re.sub('<','&lt;',txt)
#		txt = re.sub('>','&gt;',txt)
#		if doctype == 'sgml': txt = re.sub('ÿ','&yuml;',txt)
#	elif doctype == 'pm6' : txt = re.sub('<','<\#60>',txt)
#	elif doctype == 'mgp' : txt = re.sub('^%([^%])','%prefix ""\n  %\n%cont, prefix "  "\n\\1',txt)
#	elif doctype == 'man' : txt = re.sub('^\.', ' .',txt) # command ID
#	return txt
#
#def doEscapeEscape(txt):
#	while re.search(r'\\<', txt):
#		txt = re.sub(r'\\<','<\#92><',txt)
#	return txt
#
#
#################################################################################
####MerryChristmas,IdontwanttofighttonightwithyouImissyourbodyandIneedyourlove###
#################################################################################
#
## reading our source file
#if file == '-':
#	lines = sys.stdin.readlines()
#else:
#	f = open(file, 'r')
#	lines = f.readlines()
#	f.close
#
## let's mark it up!
#linenr = 0
#for lineref in range(len(lines)):
#	skip_continue = 0
#	urlbank = [] ; emailbank = []
#	linkbank = []
#	monobank = []
#	linenr = lineref +1
#	line = string.rstrip(lines[lineref])
#	
#	# we need (not really) to mark each paragraph
#	if doctype == 'pm6' and f_lastblank:
#		if f_tt or f_header or listident: holdspace = ''
#		else: holdspace = TAGparagraph[T]+'\n'
#
## PRE-formatted area
#	# we'll never support beautifiers inside pre-formatted
#	if f_tt:
#		f_lastblank = 0
#		line = doEscape(line)
#		
#		# closing PRE
#		if re_areaPreClose.search(line):
#			if doctype != 'pm6': print TAGareaPreClose[T]
#			f_tt = 0
#			continue
#		
#		# normal PRE-inside line
#		if doctype == 'pm6': line = doEscapeEscape(line)
#		elif doctype in ('txt', 'man', 'html'): line = '  '+line # align
#		print line
#		continue
#	
#	# detecting PRE
#	if re_areaPreOpen.search(line):
#		line = doEscape(line)
#		
#		if f_tt:
#			print "%d:opening PRE-formatted tag without closing previous one" %linenr
#			print line
#			continue
#		
#		print TAGareaPreOpen[T]
#		f_tt = 1
#		continue
#
## one line PRE-formatted text
#	if re_1linePre.search(line):
#		f_lastblank = 0
#		line = doEscape(line)
#		line = re_1linePre.sub('',line)
#		if   doctype == 'pm6': line = doEscapeEscape(line)
#		if doctype in ('txt', 'man', 'html'): line = '  '+line  # align
#		print '%s\n%s\n%s'%(TAGareaPreOpen[T],line,TAGareaPreClose[T])
#		continue
#
## blank lines
#	#TODO "holdspace" to save <p> to not show in closelist
#	if re_blankline.search(line):
#	
#		if istable:
#			if istableaware: print TAGtableClose[T]
#			else: print TAGareaPreClose[T]
#			istable = tableborder = 0
#			continue
#		
#		#TODO generic class or function to close quotes/lists/tables
#		#     when entering pre,list,table,etc
#		# closing quotes
#		while quotedepth:
#			quotedepth = quotedepth-1
#			print TAGareaQuoteClose[T]
#		
#		if f_lastblank:      # 2nd consecutive blank line
#			if listident:    # closes list (if any)
#				while len(listident):
#					if   listids[-1] == '-': tag = TAGlistClose[T]
#					elif listids[-1] == '+': tag = TAGnumlistClose[T]
#					elif listids[-1] == '=': tag = TAGdeflistClose[T]
#					if not tag: tag = TAGlistClose[T] # default
#					if tag: # man tags just for mother-list and at ^
#						if doctype == 'man':
#							if len(listident) == 1: print tag
#						else: print listident[-1]+tag
#					del listident[-1]
#					del listids[-1]
#				holdspace = ''
#			continue         # consecutive blanks are trash
#		
#		if f_header or linenr == 1:  # 1st blank after header (if any)
#			if not f_noheaders: printHeader(title,author,date)
#			if doctype != 'pm6': print TAGparagraph[T]
#			f_header = 0     # we're done with header
#			continue
#		
#		# normal blank line
#		if doctype != 'pm6':
#			# paragraph (if any) is wanted inside lists also
#			if listident:
#				holdspace = holdspace+TAGparagraph[T]+'\n'
#			elif doctype == 'html': print TAGparagraph[T]
#			# sgml: the quote close tag must not be \n\n</quote>
#			elif doctype == 'sgml' and quotedepth:
#				skip_continue = 1
#			# otherwise we just print a blank line
#			else: print
#		
#		f_lastblank = 1
#		if not skip_continue: continue
#	else:
#		f_lastblank = 0      # reset blank status
#
## first line with no header
#	if f_noheaders and linenr == 1 and doctype != 'pm6': print TAGparagraph[T]
#
## comments
#	# just skip them
#	if re_comment.search(line):
#		f_lastblank = 1
#		continue
#
#
## protect pre-formatted font text from escaping and formatting
#	if not f_tt:
#		while re_mono.search(line):
#			txt = re_mono.search(line).group(1)
#			monobank.append(doEscape(txt))
#			line = re_mono.sub(monomask,line,1)
#
## protect URLs and emails from escaping and formatting
## changing them by a mask
#	if not f_tt:
#		while re_linkmark.search(line):    # search for named link
#			m = re_linkmark.search(line)
#			# remove quotes from old ["" link] tag
#			label = re.sub('^"|"$','',m.group(1))
#			link = m.group(2)
#			linkbank.append([label, link])
#			line = re_linkmark.sub(linkmask,line,1)
#		
#		while re_link.search(line):        # simple url or email
#			link = re_link.search(line).group()
#			linkbank.append(['', link])
#			line = re_link.sub(linkmask,line,1)
#
## the target-specific special char escapes 
#	line = doEscape(line)
#
#
## HR line
#	if re_bar.search(line):
#		txt = re_bar.search(line).group(1)
#		if txt[0] == '=': bar = TAGbar2[T]
#		else            : bar = TAGbar1[T]
#		line = re_bar.sub(bar,line)
#		print re_x.sub(txt,line)
#		continue
#
#
## quote
#	if re_quote.search(line):
#		currquotedepth = len(re_quote.search(line).group(0)) # number of TABs
#		if doctype == 'sgml' and quotedepth and currquotedepth > quotedepth:
#			currquotedepth = quotedepth
#		if not TAGareaQuoteClose[T]:
#			line = re_quote.sub(TAGareaQuoteOpen[T]*currquotedepth, line)
#		else:
#			# new (sub)quote
#			if not quotedepth or currquotedepth > quotedepth:
#				quotedepth = currquotedepth
#				print TAGareaQuoteOpen[T]
#			
#			if doctype != 'html'and doctype != 'sgml':
#				line = re_quote.sub('', line)
#			
#			# closing quotes
#			while currquotedepth < quotedepth:
#				quotedepth = quotedepth-1
#				print TAGareaQuoteClose[T]
#	else:
#		# closing quotes
#		while quotedepth:
#			quotedepth = quotedepth-1
#			print TAGareaQuoteClose[T]
#
#
## title
#	#TODO set next blank and set f_lastblank or f_lasttitle
#	if re_title.search(line) and not listident:
#		m = re_title.search(line)
#		tag = m.group('tag')
#		level = len(tag)
#		tag = eval('TAGtitle%s[T]'%level)
#		
#		txt = string.strip(m.group('txt'))
#		if doctype == 'sgml':
#			txt = re.sub(r'\[', r'&lsqb;', txt)
#			txt = re.sub(r'\\', r'&bsol;', txt)
#		
#		if f_enumtitle:                       ### numbered title
#			id = '' ; n = level               #
#			titlecount[n] = titlecount[n] +1  # add count
#			if n < len(titlecount)-1:         # reset sublevels count
#				for i in range(n+1, len(titlecount)): titlecount[i] = 0
#			for i in range(n):                # compose id from hierarchy
#				id = "%s%d."%(id,titlecount[i+1])
#			txt = "%s %s"%(id, txt)           # add id to title
#		
#		line = re_title.sub(tag,line)
#		print re_x.sub(txt,line)
#		continue
#		
##		labeltxt = ''
##		label = m.group('label')
##		if label: labeltxt = '<label id="%s">' %label
#
#
## list
#	if re_list.search(line) or re_deflist.search(line):
#		if re_list.search(line): rgx = re_list
#		else                   : rgx = re_deflist
#		
#		m = rgx.search(line)
#		listitemident = m.group(1)
#		listtype = m.group(2)
#		extra = m.group(3)        # regex anchor char
#		
#		if listtype == '=':
#			listdefterm = m.group(3)
#			extra = ''
#		
#		# new sublist
#		if not listident or len(listitemident) > len(listident[-1]):
#			listident.append(listitemident)
#			listids.append(listtype)
#			if   listids[-1] == '-': tag = TAGlistOpen[T]
#			elif listids[-1] == '+': tag = TAGnumlistOpen[T]
#			elif listids[-1] == '=': tag = TAGdeflistOpen[T]
#			if not tag: tag = TAGlistOpen[T] # default
#			# no need to reopen <pre> tag on man sublists
#			if doctype == 'man' and len(listident) != 1: tag = ''
#			openlist = listident[-1]+tag
#			if doctype == 'pm6': listholdspace = openlist
#			else:
#				if string.strip(openlist): print openlist
#			# reset item manual count
#			listcount.append(0)
#		
#		# closing sublists
#		while len(listitemident) < len(listident[-1]):
#			if   listids[-1] == '-': tag = TAGlistClose[T]
#			elif listids[-1] == '+': tag = TAGnumlistClose[T]
#			elif listids[-1] == '=': tag = TAGdeflistClose[T]
#			if not tag: tag = TAGlistClose[T] # default
#			if tag: # man list is just a <pre> text, closed at mother-list
#				if doctype != 'man': print listident[-1]+tag
#			del listident[-1]
#			del listids[-1]
#			if listcount: del listcount[-1]
#		
#		# normal item
#		listid = listident[-1]
#		if listids[-1] == '-':
#			tag = TAGlistItem[T]
#		elif listids[-1] == '+':
#			tag = TAGnumlistItem[T]
#			listcount[-1] = listcount[-1] +1
#			if doctype in ['txt', 'man', 'moin', 'mgp']:
#				tag = re_x.sub(str(listcount[-1]), tag)
#		elif listids[-1] == '=':
#			if not TAGdeflistItem1[T]:
#				# emulate def list, with <li><b>def</b>:
#				tag = TAGlistItem[T] +TAGfontBoldOpen[T] +listdefterm
#				tag = tag +TAGfontBoldClose[T] +':'
#			else:
#				tag = re_x.sub(listdefterm, TAGdeflistItem1[T])
#			tag = tag + TAGdeflistItem2[T]  # open <DD>
#		if doctype == 'mgp': listid = len(listident)*'\t'
#		
#		line = rgx.sub(listid+tag+extra,line)
#		if listholdspace:
#			line = listholdspace+line
#			listholdspace = ''
#		if doctype == 'sgml': line = re.sub(r'\[', r'&lsqb;', line)
#
#
#
## table
##TODO escape undesired format inside table
##TODO not rstrip if table line (above)
##TODO add man, pm6 targets
#	if re_table.search(line): # only HTML for now
#		
#		closingbar = re.compile(r'\| *$')
#		tableid = line[re_table.search(line).end()-1]
#		
#		if not istable:  # table header
#			if doctype in ['sgml', 'html', 'moin']:
#				istableaware = 1
#				if tableid == '\t': tableborder = 1
#				if closingbar.search(line): tableborder = 1
#				print re_x.sub(`tableborder`, TAGtableOpen[T]) # add border=1
#			else:
#				istableaware = 0 ; print TAGareaPreOpen[T]
#		
#		istable = 1
#		
#		if istableaware:
#			line = re.sub(r'^ *'  , '', line)    # del leading spaces
#			line = closingbar.sub('', line)      # del last bar |
#			
#			tablefmt, tablecel = re.split(r'\s', line, 1)
#			tablefmt = tablefmt[1:]  # cut mark off
#			tablecel = re.split(r'\t\|?| \|', tablecel)
#			line = ''
#			
#			# setting cell and line tags
#			tl1, tl2 = TAGtableLineOpen[T], TAGtableLineClose[T]
#			tc1, tc2 = TAGtableCellOpen[T], TAGtableCellClose[T]
#			if tablefmt and tablefmt[0] == '|': # title cell
#				tc1, tc2 = TAGtableTitleCellOpen[T], TAGtableTitleCellClose[T]
#			if doctype == 'html': tc2 = tc2+'\n' ; tl1 = tl1+'\n'
#			
#			if tablecel:
#				while tablecel:
#					cel = tablecel.pop(0)
#					if not cel and doctype == 'html':
#						cel = '&nbsp;'
#					else:
#						# user escaped (not delim!)
#						cel = string.replace(cel,'\|', '|')
#					if not tablecel and doctype == 'sgml':
#						tc2 = '' # last cell
#					line = '%s%s%s%s'%(line,tc1,string.strip(cel),tc2)
#			line = '%s%s%s'%(tl1,line,tl2)
#
#
#
#### BEGIN of at-any-part-of-the-line/various-per-line TAGs.
#
## date
#	while re_date.search(line):
#		m = re_date.search(line)
#		fmt = m.group('fmt') or ''
#		dateme = currdate
#		if fmt: dateme = strftime(fmt,localtime(time()))
#		line = re_date.sub(dateme,line,1)
#
## bold
#	if re_bold.search(line):
#		txt = r'%s\1%s'%(TAGfontBoldOpen[T],TAGfontBoldClose[T])
#		line = re_bold.sub(txt,line)
#
## italic
#	if re_italic.search(line):
#		txt = r'\1%s\2%s'%(TAGfontItalicOpen[T],TAGfontItalicClose[T])
#		line = re_italic.sub(txt,line)
#
## bolditalic
#	if re_bolditalic.search(line):
#		txt = r'%s\1%s'%(TAGfontBoldItalicOpen[T],TAGfontBoldItalicClose[T])
#		line = re_bolditalic.sub(txt,line)
#
## underline
#	if re_underline.search(line):
#		txt = r'%s\1%s'%(TAGfontUnderlineOpen[T],TAGfontUnderlineClose[T])
#		line = re_underline.sub(txt,line)
#
## image
#	# first store blanks to detect image at ^
#	try: leadingblanks = re.match(' +',line).end()
#	except: leadingblanks = 0
#	while re_img.search(line) and doctype != 'moin':  # moin tag is the same
#		m = re_img.search(line)
#		txt = m.group(1)
#		ini = m.start() ; head = leadingblanks 
#		end = m.end()   ; tail = len(line)
#		tag = TAGimg[T]
#		
#		if doctype == 'html': # do img align
#			
#			align = 'center'  # default align         # text + img + text
#			if   ini == head and end == tail:
#				tag = '<P ALIGN="center">%s</P>'%tag  # ^img$
#			elif ini == head: align = 'left'          # ^img + text$
#			elif end == tail: align = 'right'         # ^text + img$
#			tag = re_x.sub(align, tag, 1)             # add align on tag
#		
#		line = re_img.sub(tag,line,1)
#		line = re_x.sub(txt,line,1)
#		
#		if doctype == 'sgml': line = re.sub(r'\[', r'&lsqb;', line)
#	line = '%s%s'%(' '*leadingblanks,line) # put blanks back
#
## font PRE
#	for mono in monobank:
#		line = string.replace(line, monomask, "%s%s%s"%(
#		       TAGfontMonoOpen[T],mono,TAGfontMonoClose[T]),1)
#
## URL & email
#	for link in linkbank:
#		linktype = 'url'; label = link[0]; url = link[1]
#		if re.match(retxt_email, url): linktype = 'email'
#		
#		guessurl = ''                    # adding protocol to guessed link
#		if linktype == 'url' and re.match(urlskel['guess'], url):
#			if url[0] == 'w': guessurl = 'http://' +url
#			else: guessurl = 'ftp://' +url
#		
#		if not label and not guessurl:   # simple link
#			if f_maskemail and linktype == 'email':
#				url = string.replace(url,'@',' (a) ')
#				url = string.replace(url,'.',' ')
#				url = doEscape("<%s>"%url)
#				line = string.replace(line, linkmask, url, 1)
#			else:
#				line = eval('string.replace(line,linkmask,TAG%s[T],1)'%linktype)
#				line = re_x.sub(url,line)
#		else:                            # named link!
#			if not label: label = url
#			if guessurl: url = guessurl
#			# putting data on the right appearance order
#			urlorder = [label, url]                 # label before link
#			if doctype in ('html', 'sgml', 'moin'): # link before label
#				urlorder = [url, label]
#			
#			# replace mask with tag
#			line = eval('string.replace(line,linkmask,TAG%sMark[T],1)'%linktype)
#			for data in urlorder:        # fill \a from tag with data
#				line = re_x.sub(data,line,1)
#
## header
#	if not f_noheaders:
#		if linenr == 1:
#			title = line
#			f_header = 1
#			continue
#		if f_header:
#			if   linenr == 2: author = line ; continue
#			elif linenr == 3: date   = line ; continue
#			else:
#				printHeader(title,author,date)
#				f_header = 0
#
#	# FINAL scapes. TODO function for it
#	# convert all \ before <...> to tag
#	if doctype == 'pm6': line = doEscapeEscape(line)
#	elif doctype == 'man' : line = re.sub('-',r'\-',line)
#	
#	print holdspace+line
#	holdspace = ''
#
#if not f_noheaders: printFooter()
#
#
#
####  RESOURCES
## html: http://www.w3.org/TR/WD-html-lex
## man: man 7 man
## sgml: www.linuxdoc.org
## moin: http://twistedmatrix.com/users/jh.twistd/moin/moin.cgi/WikiSandBox
## moin: http://moin.sf.net
## pm6: <font$> volta ao normal do estilo
## pm6: <#comentários#> <font #comment# $>
##  pagemaker table
##  1 = 0,55
##  2 = 1,10
##  3 = 1,65
##  4 = 2,20
##
##        |__1_|    |    |    |    |    |
##        |_______2_|    |    |    |    |
##        |____________3_|    |    |    |
