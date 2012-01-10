#!/usr/bin/env python
# txt2tags - generic text conversion tool
# http://txt2tags.sf.net - aurelio

# please, don't look at this code, it's ugly!
# i'll try to make it better on the next releases


import re, string, os, sys, getopt, traceback
from time import strftime,time,localtime

my_url = 'http://txt2tags.sf.net'
my_email = 'aurelio@verde666.org'
my_version = '1.1'

DEBUG = 0   # do not edit here, please use --debug
tags = ['txt', 'sgml', 'html', 'pm6', 'mgp', 'moin', 'man']
#tex will be 100% on v1.2
#tags = ['txt', 'sgml', 'html', 'pm6', 'mgp', 'moin', 'man', 'tex']
FLAGS = {'noheaders':0,'enumtitle':0,'maskemail':0, 'stdout':0,
         'toconly'  :0,'toc'      :0,'gui'      :0, 'fixme' :0}
T = CMDLINE = ''

currdate = strftime('%Y%m%d',localtime(time()))    # ISO current date
splitlevel = '' ; lang = 'english'
doctype = outfile = ''
pipefileid = '-'
has_obsolete = has_fixed = 0

# global vars for doClose*()
quotedepth = []
listindent = []
listids = []
istable = istableaware = tableborder = pendingtableopen = 0

versionstr = "txt2tags version %s <%s>"%(my_version,my_url)
usage = """
%s

usage: txt2tags -t <type> [OPTIONS] file.t2t
       txt2tags -t html -s <split level> -l <lang> file.t2t

  -t, --type       target document type. actually supported:
                   %s

      --stdout     by default, the output is written to file.<type>
                   with this option, STDOUT is used (no files written)
      --noheaders  suppress header, title and footer information
      --enumtitle  enumerate all title lines as 1, 1.1, 1.1.1, etc
      --maskemail  hide email from spam robots. x@y.z turns to <x (a) y z>

      --toc        add TOC (Table of Contents) to target document
      --toconly    print document TOC and exit
      --gui        invoke Graphical Tk Interface

      --fixme      temporary option to fix obsoleted structures

  -h, --help       print this help information and exit
  -V, --version    print program version and exit

extra options for HTML target (needs sgml-tools):
      --split      split documents. values: 0, 1, 2 (default 0)
      --lang       document language (default english)
"""%(versionstr, re.sub(r"[]'[]",'',repr(tags)))


# here is all the target's templates
# you may edit them to fit your needs
#  - the %(HEADERn)s strings represent the Header lines
#  - use %% to represent a literal %
#
HEADER_TEMPLATE = {
  'txt': """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
""",

  'sgml': """\
<!doctype linuxdoc system>
<article>
<title>%(HEADER1)s
<author>%(HEADER2)s
<date>%(HEADER3)s
""",

#TODO (peter valach) <meta http-equiv="Content-Type"
#  content="text/html; charset=iso-8859-2">
  'html': """\
<HTML>
<HEAD><TITLE>%(HEADER1)s</TITLE></HEAD>
<BODY BGCOLOR="white" TEXT="black">
<P ALIGN="center"><CENTER><H1>%(HEADER1)s</H1>
<FONT SIZE=4>
<I>%(HEADER2)s</I><BR>
%(HEADER3)s
</FONT></CENTER>
""",


# TODO man section 1 is hardcoded...
  'man': """\
.TH "%(HEADER1)s" 1 %(HEADER3)s "%(HEADER2)s"
""",

# TODO style to <HR>
  'pm6': """\
<PMTags1.0 win><C-COLORTABLE ("Preto" 1 0 0 0)
><@Normal=
  <FONT "Times New Roman"><CCOLOR "Preto"><SIZE 11>
  <HORIZONTAL 100><LETTERSPACE 0><CTRACK 127><CSSIZE 70><C+SIZE 58.3>
  <C-POSITION 33.3><C+POSITION 33.3><P><CBASELINE 0><CNOBREAK 0><CLEADING -0.05>
  <GGRID 0><GLEFT 7.2><GRIGHT 0><GFIRST 0><G+BEFORE 7.2><G+AFTER 0>
  <GALIGNMENT "justify"><GMETHOD "proportional"><G& "ENGLISH">
  <GPAIRS 12><G%% 120><GKNEXT 0><GKWIDOW 0><GKORPHAN 0><GTABS $>
  <GHYPHENATION 2 34 0><GWORDSPACE 75 100 150><GSPACE -5 0 25>
><@Bullet=<@-PARENT "Normal"><FONT "Abadi MT Condensed Light">
  <GLEFT 14.4><G+BEFORE 2.15><G%% 110><GTABS(25.2 l "")>
><@PreFormat=<@-PARENT "Normal"><FONT "Lucida Console"><SIZE 8><CTRACK 0>
  <GLEFT 0><G+BEFORE 0><GALIGNMENT "left"><GWORDSPACE 100 100 100><GSPACE 0 0 0>
><@Title1=<@-PARENT "Normal"><FONT "Arial"><SIZE 14><B>
  <GCONTENTS><GLEFT 0><G+BEFORE 0><GALIGNMENT "left">
><@Title2=<@-PARENT "Title1"><SIZE 12><G+BEFORE 3.6>
><@Title3=<@-PARENT "Title1"><SIZE 10><GLEFT 7.2><G+BEFORE 7.2>
><@Title4=<@-PARENT "Title3">
><@Title5=<@-PARENT "Title3">
><@Quote=<@-PARENT "Normal"><SIZE 10><I>>

%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
""",

#TODO escape lines beginning with %% after all formatting
  'mgp': """\
#!/usr/X11R6/bin/mgp -t 90
%%deffont "normal"    xfont  "utopia-medium-r", charset "iso8859-1"
%%deffont "normal-i"  xfont  "utopia-medium-i", charset "iso8859-1"
%%deffont "normal-b"  xfont  "utopia-bold-r"  , charset "iso8859-1"
%%deffont "normal-bi" xfont  "utopia-bold-i"  , charset "iso8859-1"
%%deffont "mono"      xfont "courier-medium-r", charset "iso8859-1"
%%default 1 size 5
%%default 2 size 8, fore "yellow", font "normal-b", center
%%default 3 size 5, fore "white",  font "normal", left, prefix "  "
%%tab 1 size 4, vgap 30, prefix "     ", icon arc "red" 40, leftfill
%%tab 2 prefix "            ", icon arc "orange" 40, leftfill
%%tab 3 prefix "                   ", icon arc "brown" 40, leftfill
%%tab 4 prefix "                          ", icon arc "darkmagenta" 40, leftfill
%%tab 5 prefix "                                ", icon arc "magenta" 40, leftfill
%%%%------------------------- end of headers -----------------------------
%%page





%%size 10, center, fore "yellow"
%(HEADER1)s

%%font "normal-i", size 6, fore "white", center
%(HEADER2)s

%%font "mono", size 7, center
%(HEADER3)s
""",

# TODO please, improve me!
  'moin': """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
""",

#TODO how to make acrobat left-side pages count?
# \includepackage{graphics}
# --lang matters! \usepackage[brazil]{babel}
# local links seems to be \label, \ref, \pageref
  'tex': r"""
\documentclass[11pt,a4paper]{article}
\usepackage{amsfonts,amssymb,graphicx,url}
\usepackage[latin1]{inputenc}  %% for accented chars
\pagestyle{empty}   %% no page numbering and header/footer
\frenchspacing      %% no aditional spaces after periods

\newcommand\email{\begingroup \urlstyle{tt}\Url}  %% for email

\title{%(HEADER1)s}
\author{%(HEADER2)s}
\begin{document}
\date{%(HEADER3)s}
\maketitle
"""
}

#-----------------------------------------------------------------------

def Quit(msg, exitcode=0): print msg ; sys.exit(exitcode)
def Error(msg): print "ERROR: %s"%msg ; sys.exit()
def Debug(msg,i=0,linenr=None):
	if i > DEBUG: return
	if linenr is not None:
		print "(%d) %04d:%s"%(i,linenr,msg)
	else:
		print "(%d) %s"%(i,msg)
def Readfile(file):
	if file == '-':
		try: data = sys.stdin.readlines()
		except: Error('You must feed me with data on STDIN!')
	else:
		try: f = open(file); data = f.readlines() ; f.close()
		except: Error("Cannot read file:\n    %s"%file)
	return data
def Savefile(file, contents):
	try: f = open(file, 'w')
	except: Error("Cannot open file for writing:\n    %s"%file)
	if type(contents) == type([]): doit = f.writelines
	else: doit = f.write
	doit(contents) ; f.close()

def NewArea(new, linenr):
	if new not in ['head', 'conf', 'body']:
		Error("Invalid new AREA '%s' on line '%s'"%(new,linenr))
	Debug('NEW AREA: %s'%new, 1, linenr)
	return new

def Obsoleted(n, old, new, ver):
	global has_obsolete
	has_obsolete = 1
	print 'OBSOLETE WARNING: line %04d'%n
	print '  The %s is now obsoleted and will be removed'%old
	print '  on txt2tags version %s. Please use %s instead.'%(ver,new)

def Fixed(n, old, new):
	global has_fixed
	has_fixed = 1
	print 'FIXED: line %04d: %15s ---> %s'%(n,old,new)

def FixTable(tabline):
	new = string.replace(tabline,'\t',' ',1)  # del 1st TAB
	new = string.replace(new,'\t',' | ')      # change TABs by spaced pipes
	new = re.sub('(.*[^\n\r])', '\\1 |', new) # add last pipe (for border)
	return new

def ObsoletedInstructions(infile):
	print """\n
ATTENTION:
  Some obsoleted txt2tags structures were found on your source document.
  Please correct them by hand, or just run:

     txt2tags --fixme %s

  To update (rewrite) this file automatically.

  Please don't ignore this message.
  On next releases of txt2tags, these old structures will not be valid.
\n"""%infile 

def reset_flags():
	global FLAGS
	for flag in FLAGS.keys(): FLAGS[flag] = 0

def set_outfile_name(infile, doctype):
	"dirname is the same for {in,out}file"
	if not infile: return
	if infile == pipefileid or FLAGS['toconly'] or FLAGS['stdout']:
		outfile = pipefileid
	else:
		outfile = "%s.%s"%(re.sub('\.(txt|t2t)$','',infile), doctype)
	Debug(" infile: '%s'"% infile, 1)
	Debug("outfile: '%s'"%outfile, 1)
	return outfile

def finish_him(outlist, outfile):
	"writing output to screen or file"
	if outfile == pipefileid:
		for line in outlist: print line
	else:
		f = open(outfile, 'w'); f.writelines(addLineBreaks(outlist)); f.close()
		if not FLAGS['gui']: print 'wrote %s'%(outfile)
	
	if splitlevel:
		print "--- html..."
		os.system('sgml2html --language=%s --split=%s %s'%(
		           lang,splitlevel,outfile))

def ParseCmdline(cmdline=sys.argv):
	"return a dic with all options:value found"
	global CMDLINE ; CMDLINE = cmdline  # save for dofooter()
	Debug("cmdline: %s"%cmdline, 1)
	options = {'infile': ''}
	
	# get cmdline options
	longopt = ['help', 'version', 'type=', 'split=', 'lang=']+FLAGS.keys()
	try: (opt, args) = getopt.getopt(cmdline[1:], 'hVt:', longopt)
	except getopt.GetoptError:
		Error('Bad option or missing argument (try --help)')
	
	# get infile, if any
	if args: options['infile'] = args[0]
	
	for name,val in opt:
		# parse information options
		if   name in ['-h','--help'   ]: Quit(usage)
		elif name in ['-V','--version']: Quit(versionstr)
		# parse short/long options
		elif name in ['-t','--type']: options['doctype'] = val ; continue
		# just long options
		options[name[2:]] = val  # del --
	
	Debug("cmdline options: %s"%options, 1)
	return options


def ParseCmdlineOptions(optdic):
	"set vars and flags according to options dic"
	global FLAGS, splitlevel, lang
	
	# store flags and vars 
	myflags = [] # for debug msg
	for flag in FLAGS.keys():
		if optdic.has_key(flag):
			FLAGS[flag] = 1
			myflags.append(flag)
	doctype    = optdic.get('doctype')
	infile     = optdic.get('infile')
	splitlevel = optdic.get('split')
	lang       = optdic.get('lang')
	Debug("cmdline flags: %s"%string.join(myflags,', '), 1)
	
	if FLAGS['fixme']:
		if not infile: Quit(usage, 1)
		doctype = 'moin'  # bogus, not used at all
	
	if not doctype and FLAGS['toconly']: doctype = 'txt' # toconly default type
	if not infile or not doctype: Quit(usage, 1)    # no filename/doctype
	
	# sanity check: validate target type
	if not tags.count(doctype):
		Error("Invalid document type '%s' (try --help)"%(doctype))
	
	outfile = set_outfile_name(infile, doctype)
	
	# sanity check: validate split level
	if doctype != 'html': splitlevel = '' # only valid for HTML target
	if splitlevel:
		# checkings
		if outfile == pipefileid:
			Error('You need to provide a FILE (not STDIN) when using --split')
		if splitlevel[0] not in '012':
			Error('Option --split must be 0, 1 or 2')
		# check for sgml-tools	
		#TODO how to test (in a clever way) if an executable is in path?
		#TODO  os.system() return code? sgml2html without --help exit 0 also?
		#TODO bah! implement sgml2html split natively and we're done
		# Error("Sorry, you must have 'sgml2html' program to use --split")
		
		# set things
		FLAGS['stdout'] = 0  # no --stdout
		doctype = 'sgml'     # 1st do a sgml, then sgml2html
		outfile = set_outfile_name(infile, doctype)
	
	# sanity check: source loss!
	if infile != pipefileid and infile == outfile:
		Error("SUICIDE WARNING!!!   (try --stdout)\n  source"+\
		      " and target files has the same name: %s"%outfile)
	### yes, i've got my sample.t2t file deleted before add this test... :/
	
	return infile,outfile,doctype
	#TODO splitlevel, lang

#---End of ParseCmdlineOptions

def toc_master(doctype, header, doc, toc):
	"decide to include TOC or not on the outlist"
	
	# deal with the TOC options
	if FLAGS['toc'] or FLAGS['toconly']:
		# format TOC lines
		### here we do toc as a valid t2t marked text (list type)
		FLAGS['noheaders'] = 1
		x,y,toc = doitall(['']+toc+['',''], doctype)
		
		# TOC between bars (not for --toconly)
		if FLAGS['toc']:
			para = TAGparagraph[T]
			tocbar = [para, re_x.sub('-'*72,TAGbar1[T]), para]
			toc = tocbar + toc + tocbar
		
		if FLAGS['toconly']: header = doc = []
	else:
		toc = []
	
	# on tex, \tableofcontents do it all - see doHeader()
	if doctype == 'tex' and not FLAGS['toconly']:
		toc = []
	
	return header + toc + doc

# check if we will enter on GUI mode
if len(sys.argv) == 2 and sys.argv[1] == '--gui':
	FLAGS['gui'] = 1
if len(sys.argv) == 1 and sys.platform[:3] in ['mac','cyg','win']:
	FLAGS['gui'] = 1

# check for GUI mode ressorces
if FLAGS['gui'] == 1:
	try:
		from tkFileDialog import askopenfilename
		from tkMessageBox import showinfo, showwarning, showerror
		import Tkinter
	except:
		# if GUI was forced, show the error message
		if len(sys.argv) > 1 and sys.argv[1] == '--gui':
			traceback.print_exc()
			sys.exit()
		# or just abandon GUI mode, and continue
		else:
			FLAGS['gui'] = 0

# set the Line Break across platforms
LB = '\n'                                   # default
if   sys.platform[:3] == 'win': LB = '\r\n'
#elif sys.platform[:3] == 'cyg': LB = '\r\n' # not sure if it's best :(
elif sys.platform[:3] == 'mac': LB = '\r'

### all the registered tags
TAGparagraph = ['', '<p>', '<P>', '<@Normal:>', '%font "normal", size 5\n', '', '.P', '']
TAGtitle1 = ['  \a'      , '<sect>\a<p>' , '<H1>\a</H1>', '\n<@Title1:>\a', '%page\n\n\a', '= \a =', '.SH \a', r'\n\\newpage\section{\a}']
# TODO tex: '\section*' is unumbered, but not added to TOC also
TAGtitle2 = ['\t\a'      , '<sect1>\a<p>', '<H2>\a</H2>', '\n<@Title2:>\a', '%page\n\n\a', '== \a ==', '.SS \a', r'\subsection{\a}']
TAGtitle3 = ['\t\t\a'    , '<sect2>\a<p>', '<H3>\a</H3>', '\n<@Title3:>\a', '%page\n\n\a', '=== \a ===', '.SS \a', r'\subsubsection{\a}']
TAGtitle4 = ['\t\t\t\a'  , '<sect3>\a<p>', '<H4>\a</H4>', '\n<@Title4:>\a', '%page\n\n\a', '==== \a ====', '.SS \a', r'\paragraph{\a}\\textbf{}\\\\\n'] #tex: DIRTY: para+emptyBF+\\+\n
TAGtitle5 = ['\t\t\t\t\a', '<sect4>\a<p>', '<H5>\a</H5>', '\n<@Title5:>\a', '%page\n\n\a', '===== \a =====', '.SS \a', TAGtitle4[7]]
TAGareaPreOpen = ['',  '<tscreen><verb>',   '<PRE>', '<@PreFormat:>', '\n%font "mono"', '{{{', '.nf', r'\begin{verbatim}']
TAGareaPreClose = ['', '</verb></tscreen>', '</PRE>', '', '%font "normal"', '}}}', '.fi\n', r'\end{verbatim}']
TAGareaQuoteOpen = ['    ',   '<quote>', '<BLOCKQUOTE>', '<@Quote:>', '%prefix "       "', ' ', '\n', r'\begin{quotation}']
TAGareaQuoteClose = ['', '</quote>', '</BLOCKQUOTE>', '', '%prefix "  "', '', '\n', r'\end{quotation}']
TAGfontMonoOpen  = ['',  '<tt>',  '<CODE>', '<FONT "Lucida Console"><SIZE 9>', '\n%cont, font "mono"\n', '{{{', '', r'\texttt{']
TAGfontMonoClose = ['', '</tt>', '</CODE>', '<SIZE$><FONT$>', '\n%cont, font "normal"\n', '}}}', '', '}']
TAGfontBoldOpen  = ['',  '<bf>',  '<B>', '<B>', '\n%cont, font "normal-b"\n', "'''", r'\\fB', r'\textbf{']
TAGfontBoldClose = ['', '</bf>', '</B>', '<P>', '\n%cont, font "normal"\n', "'''", r'\\fP', '}']
TAGfontItalicOpen  = ['',  '<em>',  '<I>', '<I>', '\n%cont, font "normal-i"\n', "''", r'\\fI', r'\textit{']
TAGfontItalicClose = ['', '</em>', '</I>', '<P>', '\n%cont, font "normal"\n', "''", r'\\fP', '}']
TAGfontBoldItalicOpen  = ['',  '<bf><em>',   '<B><I>', '<B><I>', '\n%cont, font "normal-bi"\n', "'''''", '\n.BI ', r'\textbf{\textit{']
TAGfontBoldItalicClose = ['', '</em></bf>', '</I></B>', '<P>',   '\n%cont, font "normal"\n', "'''''", '\n\\&', '}}']
TAGfontUnderlineOpen = ['', TAGfontBoldItalicOpen[1], '<U>', '<U>', '\n%cont, fore "cyan"\n', TAGfontBoldItalicOpen[5], '', r'\underline{']
TAGfontUnderlineClose = ['', TAGfontBoldItalicClose[1], '</U>', '<P>', '\n%cont, fore "white"\n', TAGfontBoldItalicClose[5], '', '}']
TAGlistOpen     = ['', '<itemize>', '<UL>', '<@Bullet:>', '', '', '\n'+TAGareaPreOpen[6], r'\begin{itemize}']
TAGlistClose    = ['', '</itemize>', '</UL>', '', '', '', TAGareaPreClose[6], r'\end{itemize}']
TAGlistItem     = ['- ', '<item>', '<LI>', '\x95	', '', '* ', '* ', r'\item ']  # \x95 == ~U
TAGnumlistOpen  = ['', '<enum>', '<OL>', '<@Bullet:>', '', '', '\n'+TAGareaPreOpen[6], r'\begin{enumerate}']
TAGnumlistClose = ['', '</enum>', '</OL>', '', '', '', TAGareaPreClose[6], r'\end{enumerate}']
TAGnumlistItem  = ['\a. ', '<item>', '<LI>', '~U    ', '\a. ', '\a. ', '\a. ', r'\item ']
TAGdeflistOpen  = ['', '', '<DL>'       , '', '', '', '', r'\begin{description}']
TAGdeflistItem1 = ['', '', '<DT>\a</DT>', '', '', '', '', '\\item[\a]']
TAGdeflistItem2 = ['', '', '<DD>'       , '', '', '', '', '']
TAGdeflistClose = ['', '', '</DL>'      , '', '', '', '', r'\end{description}']
TAGbar1 = ['\a', '<!-- \a -->', '<HR NOSHADE SIZE=1>', '\a', '%bar "white" 5', '----', '\n\n', '\n\\hrulefill{}\n']
TAGbar2 = ['\a', '<!-- \a -->', '<HR NOSHADE SIZE=5>', '\a', '%pause', '----', '\n\n', '\n\\hrulefill{}\n']
TAGurl = ['\a', '<htmlurl url="\a" name="\a">', '<A HREF="\a">\a</A>', TAGfontUnderlineOpen[3]+'\a'+TAGfontUnderlineClose[3], '\n%cont, fore "cyan"\n\a\n%cont, fore "white"\n', '[\a]', '\a', '\\url{\a}']
TAGurlMark = ['\a (\a)', TAGurl[1], TAGurl[2], '\a '+TAGurl[3], '\a '+TAGurl[4], '[\a \a]', '\a (\a)', '\\textit{\a} (\\url{\a})']
TAGemail = ['\a', '<htmlurl url="mailto:\a" name="\a">', '<A HREF="mailto:\a">\a</A>', '\a', TAGurl[4], '[\a]', '\a', '\\email{\a}']
TAGemailMark = ['\a (\a)', TAGemail[1], TAGemail[2], '\a '+TAGemail[3], '\a '+TAGemail[4], '[\a \a]', '\a (\a)', '\\textit{\a} (\\email{\a})']
TAGimg = ['[\a]', '<figure><ph vspace=""><img src="\a"></figure>', '<IMG ALIGN="\a" SRC="\a" BORDER="0">', '\a', '\n%center\n%newimage "\a", left\n', '[\a]', '\a', '\a']
TAGtableOpen     = [ '', '<table><tabular ca="c">', '<table align=center cellpadding=4 border=\a>', '', '', '', '', r'\begin{center}\begin{tabular}']
TAGtableLineOpen = [ '', '', '<tr>', '', '', '||', '', r'\hline ']
TAGtableLineClose = [ '', '<rowsep>', '</tr>', '', '', '', '', r' \\']
TAGtableCellOpen = [ '', '', '<td>', '', '', '', '', '']
TAGtableCellClose = [ '', '<colsep>', '</td>', '', '', '||', '', ' & ']
TAGtableTitleCellOpen = [ '', '', '<th>', '', '', '', '', r'\textbf{']
TAGtableTitleCellClose = [ '', '<colsep>', '</th>', '', '', '||', '', '} & ']
TAGtableClose = [ '', '</tabular></table>', '</table>', '', '', '', '', r'\end{tabular}\end{center}']
TAGanchor = ['', '', '<a name="\a">', '', '', '', '', '']
TAGEOD = ['', '</article>', '</BODY></HTML>', '', '%%EOD', '', '', r'\end{document}']


### the cool regexes
re_title = re.compile(r'^\s*(?P<tag>={1,5})(?P<txt>[^=].*[^=])\1(\[(?P<label>\w+)\])?$')
re_areaPreOpen = re_areaPreClose = re.compile(r'^---$')
re_quote = re.compile(r'^\t+')
re_1linePreOld = re.compile(r'^ {4}([^\s-])')
re_1linePre = re.compile(r'^--- ')
re_mono = re.compile(r'`([^`]+)`')
re_bold = re.compile(r'\*\*([^\s*].*?)\*\*')
re_italic = re.compile(r'(^|[^:])//([^ /].*?)//')
re_underline = re.compile(r'__([^_].*?)__') # underline lead/trailing blank
re_bolditalic = re.compile(r'\*/([^/].*?)/\*')
re_list    = re.compile(r'^( *)([+-]) ([^ ])')
re_deflist = re.compile(r'^( *)(=) ([^:]+):')
re_bar =re.compile(r'^\s*([_=-]{20,})\s*$')
re_table = re.compile(r'^ *\|\|?[<:>]*\s')

# link things
urlskel = {
  'proto' : r'(https?|ftp|news|telnet|gopher|wais)://',
  'guess' : r'(www[23]?|ftp)\.',   # w/out proto, try to guess
  'login' : r'A-Za-z0-9_.-',       # for ftp://login@domain.com
  'pass'  : r'[^ @]*',             # for ftp://login:password@domain.com
  'chars' : r'A-Za-z0-9%._/~:,=-', # %20(space), :80(port)
  'anchor': r'A-Za-z0-9%._-',      # %nn(encoded)
  'form'  : r'A-Za-z0-9/%&=+.@*_-',# .@*_-(as is)
  'punct' : r'.,;:!?'
}


### WARNING: regex nightmares ahead :)
# textual descriptions are on --help's style: [...] is optional, | is OR
#
# username [ :password ] @
patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
#
# [ http:// ] [ username:password@ ] domain.com [ / ] [ #anchor | ?form=data ]
retxt_url = r'\b(%s%s|%s)[%s]+\b/?(#[%s]+|\?[%s]+)?'%(
             urlskel['proto'],patt_url_login, urlskel['guess'],
             urlskel['chars'],urlskel['anchor'],urlskel['form'])
#
# filename | [ filename ] #anchor
retxt_url_local = r'[%s]+|[%s]*(#[%s]+)'%(
             urlskel['chars'],urlskel['chars'],urlskel['anchor'])
#
# user@domain [ ?form=data ]
retxt_email = r'\b[%s]+@([A-Za-z0-9_-]+\.)+[A-Za-z]{2,4}\b(\?[%s]+)?'%(
             urlskel['login'],urlskel['form'])
#
# email | url
re_link = re.compile(r'%s|%s'%(retxt_url,retxt_email), re.I)
#
# [image.EXT]
retxt_img = r'\[([\w_,.+%$#@!?+~/-]+\.(png|jpe?g|gif|eps|bmp))\]'
#
# \[ label | imagetag    url | email | filename \]
re_linkmark = re.compile(r'\[(?P<label>%s|[^]]+) (?P<link>%s|%s|%s)\]'%(
              retxt_img, retxt_url, retxt_email, retxt_url_local),
              re.L+re.I)
#
# special char to place data on TAGs contents  (\a == bell)
re_x = re.compile('\a')
#
# special lines: blank lines and comment lines
re_blankline = re.compile(r'^\s*$')
re_comment = re.compile(r'^(//|%)')
#
# %%date [ (formatting) ]
re_date = re.compile(r'%%date\b(\((?P<fmt>.*?)\))?', re.I)
#
re_img = re.compile(retxt_img, re.L+re.I)
re_macro = re_date
# Settings are still in development stage - DON'T USE THIS
#re_setting = re.compile(r'^%\s*Document \s*(Encoding|Toc)\s*:\s*(.*)$',re.I)
#
### END OF regex nightmares


def doHeader(doctype, headdic):
	if not HEADER_TEMPLATE.has_key(doctype):
		Error("doheader: Unknow doctype '%s'"%doctype)
	Debug('HEADER data: %s'%headdic, 1)
	template = string.split(HEADER_TEMPLATE[doctype], '\n')
	
	# scan for empty dictionary keys
	# if found, scan template lines for that key reference
	# if found, remove the reference
	# if there aren't any other key reference on the same line, remove it
	for key in headdic.keys():
		if not headdic[key]:
			for line in template:
				if string.count(line, key):
					sline = string.replace(line, '%%(%s)s'%key, '')
					if not string.count(sline, '%(HEADER'):
						template.remove(line)
	# populate template with data
	template = string.join(template, '\n') % headdic
	
	# post processing
	if doctype == 'tex':
		if FLAGS['toc']:
			template = template + '\n' + r'\newpage\tableofcontents'
		if headdic['HEADER3'] == currdate:
			# let tex format today
			template = re.sub(r'\\date\{.*?}', r'\date', template)
	
	return string.split(template, '\n')

def doCommentLine(doctype,txt):
	if doctype == 'sgml' or doctype == 'html': ret = "<!-- %s -->"%txt
	elif doctype == 'mgp': ret = "%%%% %s"%txt
	elif doctype == 'man': ret = '.\\" %s'%txt
	elif doctype == 'tex': ret = "%% %s"%txt
	else: ret = ''
	return ret

def doFooter(doctype):
	ret = []
	typename = doctype
	if doctype == 'tex': typename = 'LaTeX2e'
	ppgd = '%s code generated by txt2tags %s (%s)'%(typename,my_version,my_url)
	cmdline = 'cmdline: txt2tags %s'%string.join(CMDLINE[1:], ' ')
	ret.append('\n'+doCommentLine(doctype,ppgd))
	ret.append(doCommentLine(doctype,cmdline))
	ret.append(TAGEOD[T])
	return ret

def doEscape(doctype,txt):
	if doctype == 'html' or doctype == 'sgml':
		txt = re.sub('&','&amp;',txt)
		txt = re.sub('<','&lt;',txt)
		txt = re.sub('>','&gt;',txt)
		if doctype == 'sgml': txt = re.sub('\xff','&yuml;',txt)  # "+y
	elif doctype == 'pm6':
		txt = re.sub('<','<\#60>',txt)
	elif doctype == 'mgp':
		txt = re.sub('^%',' %',txt)  # add leading blank to avoid confusion
		#txt = re.sub('^%([^%])','%prefix ""\n  %\n%cont, prefix "  "\n\\1',txt)
	elif doctype == 'man':
		txt = re.sub('^\.', ' .',txt) # command ID
	elif doctype == 'tex':
		txt = string.replace(txt, '\\', r'\verb!\!')
		txt = string.replace(txt, '~', r'\verb!~!')
		txt = string.replace(txt, '^', r'\verb!^!')
		txt = re.sub('([#$&%{}])', r'\\\1', txt)
		# TIP the _ is escaped at end
	return txt

def doFinalEscape(txt):
	if   doctype == 'pm6': txt = string.replace(txt, r'\<',r'<\#92><')
	elif doctype == 'man': txt = string.replace(txt, '-', r'\-')
	elif doctype == 'tex': txt = string.replace(txt, '_', r'\_')
	return txt

def doEscapeEscapechar(txt):
	return string.replace(txt, '\\', '\\\\')

def addLineBreaks(list):
	"use LB to respect sys.platform"
	ret = []
	for line in list:
		line = string.replace(line,'\n',LB)  # embedded \n's
		ret.append(line+LB)                  # add final line break
	return ret

def doPreLine(doctype,line):
	"Parsing procedures for preformatted (verbatim) lines"
	# tex doesn't need escapes inside verbatim
	if doctype != 'tex': line = doEscape(doctype,line)
	if doctype == 'pm6': line = doFinalEscape(line)
	elif doctype in ['txt','man','html']: line = '  '+line # align
	return line

def doCloseTable(doctype):
	global istable, istableaware, tableborder, pendingtableopen
	ret = ''
	if istableaware:
		if doctype == 'tex' and tableborder:
			ret = TAGtableLineOpen[T]+TAGtableClose[T]+'\n'
		else:
			ret = TAGtableClose[T]+'\n'
	else:
		ret = TAGareaPreClose[T]
	istable = tableborder = pendingtableopen = 0
	return ret

def doCloseQuote(howmany=1):
	global quotedepth
	ret = []
	for i in range(howmany):
		quotedepth.pop()
		#TODO align open/close tag -> FREE_ALING_TAG = 1 (man not)
		ret.append(TAGareaQuoteClose[T])
	return string.join(ret,'\n')

def doCloseList(doctype, howmany=1):
	global listindent, listids
	ret = []
	for i in range(howmany):
		if   listids[-1] == '-': tag = TAGlistClose[T]
		elif listids[-1] == '+': tag = TAGnumlistClose[T]
		elif listids[-1] == '=': tag = TAGdeflistClose[T]
		if not tag: tag = TAGlistClose[T] # default
		if tag:
			# man tags just for mother-list and at ^
			if doctype == 'man':
				if len(listindent) == 1:
					ret.append(tag)
			else:
				ret.append(listindent[-1]+tag)
		del listindent[-1]
		del listids[-1]
	return string.join(ret,'\n')


################################################################################
###MerryChristmas,IdontwanttofighttonightwithyouImissyourbodyandIneedyourlove###
################################################################################


def doitall(inlines, doctype):
	# global vars for doClose*()
	global T, quotedepth, listindent, listids
	global istable, istableaware, tableborder, pendingtableopen
	
	# the defaults
	linkmask  = '@@_link_@@'
	monomask  = '@@_mono_@@'
	macromask = '@@_macro_@@' 
	T = tags.index(doctype)
	
	AREA = NewArea('head',0)   # then conf, then body
	HEADERS = { 'HEADER1': '-NO TITLE-', 'HEADER2':'', 'HEADER3':'' }
#	SETTINGS = {}
	ret = []
	fixedinfile = []
	toclist = []
	header = []
	f_tt = 0
	listindent = []
	listids = []
	listcount = []
	titlecount = ['',0,0,0,0,0]
	f_lastblank = 0
	holdspace = ''
	listholdspace = ''
	quotedepth = []
	istable = 0
	tableborder = 0
	pendingtableopen = 0
	tablealign = []
	
	if outfile != pipefileid:
		if not FLAGS['gui'] and not FLAGS['fixme']:
			print "--- %s..."%doctype
	
	# let's mark it up!
	linenr = 0
	for lineref in range(len(inlines)):
		skip_continue = 0
		linkbank = []
		monobank = []
		macrobank = []
		linenr = lineref +1
		untouchedline = inlines[lineref]
		line = string.rstrip(untouchedline)
		# save line to the 'fixed' buffer
		fixedinfile.append(untouchedline)
		
		#print 'LINE: %s'%repr(line)  # for heavy debug
		
		# detect if head section is over
		#TIP 'not line' depends on previous line.rstrip()
		if (linenr == 4 and AREA == 'head') or \
		   (linenr == 1 and not line):
			AREA = NewArea('conf',linenr)
			if not FLAGS['noheaders']:
				header = doHeader(doctype,HEADERS)
		
		# we need (not really) to mark each paragraph
		#TODO check if this is really needed
		if doctype == 'pm6' and f_lastblank:
			if f_tt or AREA == 'head' or listindent:
				holdspace = ''
			else:
				holdspace = TAGparagraph[T]+'\n'
		
		# any NOT table line, closes an open table 
		if istable and not re_table.search(line):
			ret.append(doCloseTable(doctype))
		
		
		#---------------------[ PRE formatted ]----------------------
		
		#TIP we'll never support beautifiers inside pre-formatted
		
		# we're already on a PRE area
		if f_tt:
			# closing PRE
			if re_areaPreClose.search(line):
				if doctype != 'pm6': ret.append(TAGareaPreClose[T])
				f_tt = 0
				continue
			
			# normal PRE-inside line
			line = doPreLine(doctype, line)
			ret.append(line)
			continue
		
		# detecting PRE area init
		if re_areaPreOpen.search(line):
			ret.append(TAGareaPreOpen[T])
			f_lastblank = 0
			f_tt = 1
			continue
		
		# one line PRE-formatted text
		if re_1linePre.search(line):
			f_lastblank = 0
			line = re_1linePre.sub('',line)
			line = doPreLine(doctype, line)
			ret.append('%s\n%s\n%s'%(TAGareaPreOpen[T],line,TAGareaPreClose[T]))
			continue
		
		#---------------------[ blank lines ]-----------------------
		
		#TODO "holdspace" to save <p> to not show in closelist
		if re_blankline.search(line):
			
			# closing all open quotes
			if quotedepth: ret.append(doCloseQuote(len(quotedepth)))
			
			# closing all open lists
			if f_lastblank:      # 2nd consecutive blank line
				if listindent:   # closes list (if any)
					ret.append(doCloseList(doctype,len(listindent)))
					holdspace = ''
				continue         # consecutive blanks are trash
			
			# normal blank line
			if doctype != 'pm6' and AREA == 'body':
				# paragraph (if any) is wanted inside lists also
				if listindent:
					holdspace = holdspace+TAGparagraph[T]+'\n'
				elif doctype == 'html': ret.append(TAGparagraph[T])
				# sgml: the quote close tag must not be \n\n</quote>
				elif doctype == 'sgml' and quotedepth:
					skip_continue = 1
				# otherwise we just print a blank line
				else: ret.append('')
			
			f_lastblank = 1
			if not skip_continue: continue
		else:
			f_lastblank = 0      # reset blank status
		
		
		#---------------------[ comments ]-----------------------
		
		# just skip them (if not macro or setting)
		if re_comment.search(line) and not re_date.match(line):
			
### Still in development stage
#			# detect settings
#			if re_setting.search(line):
#				if AREA == 'conf':
#					m = re_setting.search(line)
#					name, val = m.group(1), m.group(2)
#					SETTINGS[string.lower(name)] = string.strip(val)
#					Debug("Found Setting '%s', value '%s'"%(name,val),1,linenr)
#				continue
			
			# obsoleted comment format
			if line[0] == '/':
				# fixes it
				if FLAGS['fixme']:
					fixedinfile.pop()  # discard original line, save new
					fixedinfile.append(re.sub('^//','%',untouchedline))
					Fixed(linenr, '// comment line', '% comment line')
				# just show a warning message
				else:
					old = '// as the comment line string'
					new = '% as the new comment line char'
					Obsoleted(linenr, old, new, '1.3')
			
			f_lastblank = 1
			continue
		
		#---------------------[ BODY detect ]-----------------------
		
		### if got here, its a header or a valid line
		if AREA == 'conf':
			# oops, not header, so we're now on document BODY
			AREA = NewArea('body', linenr)
			# so, let's print the opening paragraph
			if doctype != 'pm6':
				ret.append(TAGparagraph[T])
		
		
		#---------------------[ Title ]-----------------------
		
		#TODO set next blank and set f_lastblank or f_lasttitle
		if re_title.search(line) and not listindent and AREA == 'body':
			line = doEscape(doctype,line)
			
			m = re_title.search(line)
			tag = m.group('tag')
			level = len(tag)
			tag = eval('TAGtitle%s[T]'%level)
			
			txt = string.strip(m.group('txt'))
			if doctype == 'sgml':
				txt = re.sub(r'\[', r'&lsqb;', txt)
				txt = re.sub(r'\\', r'&bsol;', txt)
			
			if FLAGS['enumtitle']:                ### numbered title
				id = '' ; n = level               #
				titlecount[n] = titlecount[n] +1  # add count
				if n < len(titlecount)-1:         # reset sublevels count
					for i in range(n+1, len(titlecount)): titlecount[i] = 0
				for i in range(n):                # compose id from hierarchy
					id = "%s%d."%(id,titlecount[i+1])
				idtxt = "%s %s"%(id, txt)         # add id to title
			else:
				idtxt = txt
			
			anchorid = 'toc%d'%(len(toclist)+1)
			if TAGanchor[T] and FLAGS['toc']:
				ret.append(re_x.sub(anchorid,TAGanchor[T]))
			
			# escape to handle \ on title
			idtxt = string.replace(idtxt, '\\', '\\\\')
			
			line = re_title.sub(tag,line)
			ret.append(re_x.sub(idtxt,line))
			
			# let's do some TOC!
			if TAGanchor[T]:
				# tocitemid = '#toc%d'%(len(toclist)+1)
				# TOC more readable with master topics not linked at number
				# stoled idea from windows .CHM files (help system)
				if FLAGS['enumtitle'] and level == 1:
					tocitem = '%s+ [%s #%s]'%(' '*level,txt,anchorid)
				else:
					tocitem = '%s- [%s #%s]'%(' '*level,idtxt,anchorid)
			else:
				tocitem = '%s- %s'%(' '*level,idtxt)
				if doctype in ['txt', 'man']:
					tocitem = '%s%s' %('  '*level,idtxt)
			if level <= 3: toclist.append(tocitem) # max toc level: 3
			
			# add "underline" to text titles
			if doctype == 'txt': ret.append(re_x.sub('='*len(idtxt),tag))
			
			continue
		
		#TODO!	labeltxt = ''
		#		label = m.group('label')
		#		if label: labeltxt = '<label id="%s">' %label
		
		
		#---------------------[ apply masks ]-----------------------
		
		### protect important structures from escaping and formatting
		# protect pre-formatted font text 
		while re_mono.search(line):
			txt = re_mono.search(line).group(1)
			if doctype == 'tex':
				monobank.append(txt)
			else:
				monobank.append(doEscape(doctype,txt))
			line = re_mono.sub(monomask,line,1)
		
		# protect macros
		while re_macro.search(line):
			txt = re_macro.search(line).group()
			macrobank.append(txt)
			line = re_macro.sub(macromask,line,1)
		
		# protect URLs and emails
		while re_linkmark.search(line) or re_link.search(line):
			
			# try to match plain or named links
			match_link  = re_link.search(line)
			match_named = re_linkmark.search(line)
			
			# define the current match
			if match_link and match_named:
				# both types found, which is the first?
				m = match_link
				if match_named.start() < match_link.start():
					m = match_named
			else:
				# just one type found, we're fine
				m = match_link or match_named
			
			# extract link data and apply mask
			if m == match_link:              # plain link
				label = ''
				link  = m.group()
				line  = re_link.sub(linkmask,line,1)
			else:                            # named link
				label = string.rstrip(m.group('label'))
				link  = m.group('link')
				line = re_linkmark.sub(linkmask,line,1)
			
			# save link data to the link bank
			linkbank.append((label, link))
		
		#---------------------[ do Escapes ]-----------------------
		
		# the target-specific special char escapes for body lines
		line = doEscape(doctype,line)
		
		#---------------------[ Horizontal Bar ]--------------------
		
		if re_bar.search(line):
			txt = re_bar.search(line).group(1)
			if txt[0] == '=': bar = TAGbar2[T]
			else            : bar = TAGbar1[T]
			line = re_bar.sub(bar,line)
			ret.append(re_x.sub(txt,line))
			continue
		
		#---------------------[ Quote ]-----------------------
		
		if re_quote.search(line) and AREA == 'body':
			# store number of leading TABS
			currquotedepth = len(re_quote.search(line).group(0))
			
			# SGML doesn't support nested quotes
			if doctype == 'sgml':
				if quotedepth and currquotedepth > quotedepth[-1]:
					currquotedepth = quotedepth[-1]
			
			# for don't-close-me quote tags
			if not TAGareaQuoteClose[T]:
				line = re_quote.sub(TAGareaQuoteOpen[T]*currquotedepth, line)
			else:
				# new (sub)quote
				if not quotedepth or currquotedepth > quotedepth[-1]:
					quotedepth.append(currquotedepth)
					ret.append(TAGareaQuoteOpen[T])
				
				if doctype != 'html'and doctype != 'sgml':
					line = re_quote.sub('', line)
				
				# closing quotes
				while currquotedepth < quotedepth[-1]:
					ret.append(doCloseQuote(1))
		else:
			# closing all quotes (not quote line)
			if quotedepth: ret.append(doCloseQuote(len(quotedepth)))
		
		
		#---------------------[ Lists ]-----------------------
		
		if (re_list.search(line) or re_deflist.search(line)) and AREA == 'body':
			if re_list.search(line): rgx = re_list
			else                   : rgx = re_deflist
			
			m = rgx.search(line)
			listitemindent = m.group(1)
			listtype = m.group(2)
			extra = m.group(3)        # regex anchor char
			
			if listtype == '=':
				listdefterm = m.group(3)
				extra = ''
				if doctype == 'tex':
					# on tex, brackets are term delimiters
					# TODO escape ] at list definition
					# \], \rbrack{} and \verb!]!  don't work :(
					#listdefterm = string.replace(listdefterm, ']', '???')
					pass
			
			# tex maximum list depth is 4, so let's force it
			if doctype == 'tex' and len(listindent) == 4:
				if len(listitemindent) > len(listindent[-1]):
					listitemindent = listindent[-1]
			
			# new sublist
			if not listindent or len(listitemindent) > len(listindent[-1]):
				listindent.append(listitemindent)
				listids.append(listtype)
				if   listids[-1] == '-': tag = TAGlistOpen[T]
				elif listids[-1] == '+': tag = TAGnumlistOpen[T]
				elif listids[-1] == '=': tag = TAGdeflistOpen[T]
				if not tag: tag = TAGlistOpen[T] # default
				# no need to reopen <pre> tag on man sublists
				if doctype == 'man' and len(listindent) != 1: tag = ''
				openlist = listindent[-1]+tag
				if doctype == 'pm6': listholdspace = openlist
				else:
					if string.strip(openlist): ret.append(openlist)
				# reset item manual count
				listcount.append(0)
			
			# closing sublists
			while len(listitemindent) < len(listindent[-1]):
				close = doCloseList(doctype)
				if close: ret.append(close)
				if listcount: del listcount[-1]
			
			# normal item
			listid = listindent[-1]
			if listids[-1] == '-':
				tag = TAGlistItem[T]
			elif listids[-1] == '+':
				tag = TAGnumlistItem[T]
				listcount[-1] = listcount[-1] +1
				if doctype in ['txt', 'man', 'moin', 'mgp']:
					tag = re_x.sub(str(listcount[-1]), tag)
			elif listids[-1] == '=':
				if not TAGdeflistItem1[T]:
					# emulate def list, with <li><b>def</b>:
					tag = TAGlistItem[T] +TAGfontBoldOpen[T] +listdefterm
					tag = tag +TAGfontBoldClose[T] +':'
				else:
					tag = re_x.sub(listdefterm, TAGdeflistItem1[T])
				tag = tag + TAGdeflistItem2[T]  # open <DD>
			if doctype == 'mgp': listid = len(listindent)*'\t'
			line = rgx.sub(listid+tag+extra,line)
			if listholdspace:
				line = listholdspace+line
				listholdspace = ''
			if doctype == 'sgml': line = re.sub(r'\[', r'&lsqb;', line)
		
		
		#---------------------[ Table ]-----------------------
		
		#TODO rework all this table spaghetti code
		#TODO escape undesired format inside table
		#TODO not rstrip if table line (above)
		#TODO add man, pm6 targets
		if re_table.search(line) and AREA == 'body':
			
			closingbar = re.compile(r'\| *$')
			tableid = line[re_table.search(line).end()-1]
			
			if not istable:  # table header
				if doctype in ['sgml', 'html', 'moin', 'tex']:
					istableaware = 1
					
					# obsoleted TAB-made table
					if tableid == '\t': tableborder = 1
					if closingbar.search(line): tableborder = 1
					# add border=1 and open table
					if doctype == 'tex':
						pendingtableopen = 1
					else:
						ret.append(re_x.sub(`tableborder`, TAGtableOpen[T]))
				else:
					istableaware = 0 ; ret.append(TAGareaPreOpen[T])
			
			istable = 1
			
			if istableaware:
				line = re.sub(r'^ *'  , '', line)    # del leading spaces
				line = closingbar.sub('', line)      # del last bar |
				
				# obsoleted TAB-made table
				if line[1] == '\t' or line[1:3] == '|\t':
					# fix it
					if FLAGS['fixme']:
						fixedinfile.pop()  # discard original line, save new
						fixedinfile.append(FixTable(untouchedline))
						Fixed(linenr, 'TAB-made table', 'PIPE-made table')
					# just show a warning message
					else:
						Obsoleted(linenr,'TAB-made table',
						  'PIPE-made table','1.3')
				  
				tablefmt, tablecel = re.split(r'\s', line, 1)
				tablefmt = tablefmt[1:]  # cut mark off
				# TODO v1.3: take \t\|?| out
				# TODO use ' | ' as field separator
				
				  
				tablecel = re.split(r'\t\|?| \|', tablecel)
				line = ''
				if doctype == 'tex' and pendingtableopen:
					vlinechar = '|'
					if not tableborder: vlinechar = ''
					cellspec = vlinechar+'l' # lcr = left, center, right align
					tablespec = (cellspec)*len(tablecel)
					tablespec = '{%s%s}'%(tablespec,vlinechar)
					ret.append(TAGtableOpen[T]+tablespec)
					pendingtableopen = 0
				
				# setting cell and line tags
				tl1, tl2 = TAGtableLineOpen[T], TAGtableLineClose[T]
				tc1, tc2 = TAGtableCellOpen[T], TAGtableCellClose[T]
				#TODO if ' |   ' table cell is center align
				if tablefmt and tablefmt[0] == '|': # title cell
					tc1,tc2 = TAGtableTitleCellOpen[T],TAGtableTitleCellClose[T]
				if doctype == 'html': tc2 = tc2+'\n' ; tl1 = tl1+'\n'
				if doctype == 'tex' and not tableborder: tl1 = ''
				
				if tablecel:
					while tablecel:
						cel = tablecel.pop(0)
						if not cel and doctype == 'html':
							cel = '&nbsp;'
						else:
							# user escaped (not delim!)
							cel = string.replace(cel,'\|', '|')
						if not tablecel and doctype in ['sgml','tex']:
							tc2 = '' # last cell don't need separator
						# close beautifier for last title cell
						if not tablecel and doctype == 'tex':
							if tablefmt and tablefmt[0] == '|': tc2 = '}'
						line = '%s%s%s%s'%(line,tc1,string.strip(cel),tc2)
				line = '%s%s%s'%(tl1,line,tl2)
		
		
		### BEGIN of at-any-part-of-the-line/various-per-line TAGs.
		
		# bold
		if re_bold.search(line):
			txt = r'%s\1%s'%(TAGfontBoldOpen[T],TAGfontBoldClose[T])
			if doctype == 'tex': txt = '\\'+txt # escape escape
			line = re_bold.sub(txt,line)
		
		# italic
		if re_italic.search(line):
			open, close = TAGfontItalicOpen[T], TAGfontItalicClose[T]
			if doctype == 'tex': open = '\\'+open  # must escape escape (sux)
			txt = r'\1%s\2%s'%(open, close)
			line = re_italic.sub(txt,line)
		
		# bolditalic
		if re_bolditalic.search(line):
			open, close = TAGfontBoldItalicOpen[T], TAGfontBoldItalicClose[T]
			if doctype == 'tex': open = doEscapeEscapechar(open)
			txt = r'%s\1%s'%(open, close)
			line = re_bolditalic.sub(txt,line)
		
		# underline
		if re_underline.search(line):
			txt = r'%s\1%s'%(TAGfontUnderlineOpen[T],TAGfontUnderlineClose[T])
			line = re_underline.sub(txt,line)
		
		#---------------------[ URL & E-mail ]-----------------------
		
		for linkdata in linkbank:
			# set link type and data
			label, url = linkdata
			linktype = 'url';
			if re.match(retxt_email, url): linktype = 'email'
			
			# adding protocol to guessed link
			guessurl = ''
			if linktype == 'url' and re.match(urlskel['guess'], url):
				if url[0] == 'w': guessurl = 'http://' +url
				else            : guessurl =  'ftp://' +url
				
				# not link aware targets -> protocol is useless 
				if doctype in ['txt','man','pm6','mgp','tex']: guessurl = ''
			
			# simple link (not guessed)
			if not label and not guessurl:
				if FLAGS['maskemail'] and linktype == 'email':
					# do the email mask feature (no TAGs, just text)
					url = string.replace(url,'@',' (a) ')
					url = string.replace(url,'.',' ')
					url = doEscape(doctype,"<%s>"%url)
					line = string.replace(line, linkmask, url, 1)
				else:
					# replace mask with tag, add link data to tag
					cmd = 'string.replace(line,linkmask,TAG%s[T],1)'%linktype
					line = eval(cmd)
					line = re_x.sub(url,line)
			
			# named link or guessed simple link
			else:
				# adjusts for guessed link
				if not label: label = url      # no   protocol
				if guessurl : url   = guessurl # with protocol
				
				# putting data on the right appearance order
				urlorder = [label, url]                 # label before link
				if doctype in ('html', 'sgml', 'moin'): # link before label
					urlorder = [url, label]
				
				# replace mask with tag
				cmd = 'string.replace(line,linkmask,TAG%sMark[T],1)'%linktype
				line = eval(cmd)
				
				# add link data to tag (replace \a)
				for data in urlorder:
					# escape to handle \ on link
					data = string.replace(data, '\\', '\\\\')
					line = re_x.sub(data,line,1)
		
		#---------------------[ Image ]-----------------------
		
		#TODO fix smart align when image is a link label
		# moin and txt tags are the same as the mark, so just skip
		if re_img.search(line) and doctype not in ['moin','txt']:
			# first store blanks final position to detect image at ^
			try: leadingblanks = re.match(' +',line).end()
			except: leadingblanks = 0
			while re_img.search(line):
				m = re_img.search(line)
				txt = m.group(1)
				ini = m.start() ; head = leadingblanks 
				end = m.end()   ; tail = len(line)
				tag = TAGimg[T]
				
				if doctype == 'html': # do img align
					
					align = 'center'  # default align         # text +img +text
					if ini == head and end == tail:
						tag = '<P ALIGN="center">%s</P>'%tag  # ^img$
					elif ini == head: align = 'left'          # ^img + text$
					elif end == tail: align = 'right'         # ^text + img$
					tag = re_x.sub(align, tag, 1)             # add align on tag
				
				line = re_img.sub(tag,line,1)
				line = re_x.sub(txt,line,1)
				
				if doctype == 'sgml': line = re.sub(r'\[', r'&lsqb;', line)
			line = '%s%s'%(' '*leadingblanks,line) # put blanks back
		
		#---------------------[ Rethink this ]-----------------------
		
		# mgp/tex: restore orig line for headers (no formatting at all!)
		# only %%date must be converted
		if not FLAGS['noheaders'] and AREA == 'head':
			uline = string.rstrip(untouchedline)
			# is there any tex on the line?
			# TODO protect %%date from escaping
			if doctype == 'tex' and re.search(r'\\\w+{', line):
				line = doEscape(doctype, uline)
			# mgp, escape anyway
			elif doctype == 'mgp':
				line = doEscape(doctype, uline)
		
		#---------------------[ Expand Macros ]-----------------------
		
		if macrobank:
			for macro in macrobank:
				line = string.replace(line, macromask, macro,1)
			# now the line is full of macros again
			
			# date
			while re_date.search(line):
				m = re_date.search(line)
				fmt = m.group('fmt') or ''
				dateme = currdate
				if fmt: dateme = strftime(fmt,localtime(time()))
				line = re_date.sub(dateme,line,1)
		
		#---------------------[ Expand PREs ]-----------------------
		
		for mono in monobank:
			line = string.replace(line, monomask, "%s%s%s"%(
			       TAGfontMonoOpen[T],mono,TAGfontMonoClose[T]),1)
		
		#---------------------[ Headers ]-----------------------
		
		if AREA == 'head' and linenr < 4:
			HEADERS['HEADER%d'%linenr] = line
			continue
		
		#---------------------[ Final Escapes ]-----------------------
		
		line = doFinalEscape(line)
		ret.append(holdspace+line)
		holdspace = ''
	
	# EOF: close any open lists/tables/quotes
	if listindent: ret.append(doCloseList(doctype,len(listindent)))
	if istable   : ret.append(doCloseTable(doctype))
	if quotedepth: ret.append(doCloseQuote(len(quotedepth)))
	
	if not FLAGS['noheaders']: ret.extend(doFooter(doctype))
	if FLAGS['fixme']: ret = fixedinfile[:]
	return header,toclist,ret

# TODO each formatting function should set flags
#      like: readnetxline: 1 , continue: 1, etc.
#        for func in [do_bold, do_under, ...]:
#           func(); if readnextline: read(); etc



################################################################################
##################################### GUI ######################################
################################################################################

# tk help: http://python.org/topics/tkinter/
class Gui:
	"Graphical Tk Interface"
	def __init__(self):
		self.bg = 'orange'
		self.root = Tkinter.Tk()
		self.root.config(bd=15,bg=self.bg)
		self.root.title("txt2tags")
		self.frame1 = Tkinter.Frame(self.root,bg=self.bg)
		self.frame1.pack(fill='x')
		self.frame2 = Tkinter.Frame(self.root,bg=self.bg)
		self.frame2.pack()
		self.frame3 = Tkinter.Frame(self.root,bg=self.bg)
		self.frame3.pack(fill='x')
		self.frame = self.root
		
		self.infile  = self.setvar('')
		#self.infile  = self.setvar('C:/cygwin/home/Milene/abc.txt')
		#self.infile  = self.setvar('C:/aurelio/a.txt')
		self.doctype = self.setvar('html')
		self.f_noheaders = self.setvar('')
		self.f_enumtitle = self.setvar('')
		self.f_toc       = self.setvar('')
		self.f_toconly   = self.setvar('')
		self.f_stdout    = self.setvar('')
	
	### config as dic for python 1.5 compat (**opts don't work :( )
	def entry(self, **opts): return Tkinter.Entry(self.frame, opts)
	def label(self, txt='', **opts):
		opts.update({'text':txt,'bg':self.bg})
		return Tkinter.Label(self.frame, opts)
	def button(self,name,cmd,**opts):
		opts.update({'text':name,'command':cmd})
		return Tkinter.Button(self.frame, opts)
	def check(self,name,val,**opts):
		opts.update( {'text':name, 'onvalue':val, 'offvalue':'',
		  'anchor':'w', 'bg':self.bg, 'activebackground':self.bg} )
		Tkinter.Checkbutton(self.frame, opts).pack(fill='x',padx=10)
	### config as positional parameters for python 2.*
	#	def entry(self, **opts): return Tkinter.Entry(self.frame, **opts)
	#	def label(self, txt='', **opts):
	#		return Tkinter.Label(self.frame, text=txt, bg=self.bg, **opts)
	#	def button(self,name,cmd,**opts):
	#		return Tkinter.Button(self.frame, text=name, command=cmd, **opts)
	#	def check(self,name,val,**opts):
	#		Tkinter.Checkbutton(self.frame,text=name, onvalue=val, offvalue='',
	#		   anchor='w', bg=self.bg, activebackground=self.bg, **opts).pack(
	#		   fill='x',padx=10)
	
	def exit(self): self.root.destroy(); sys.exit()
	def setvar(self, val): z = Tkinter.StringVar() ; z.set(val) ; return z
	def menu(self,sel,items):
		return apply(Tkinter.OptionMenu,(self.frame,sel)+tuple(items))
	def askfile(self):
		ftypes = [("txt2tags files",("*.t2t","*.txt")),("All files","*")]
		self.infile.set(askopenfilename(filetypes=ftypes))
	def scrollwindow(self,txt='no text!',title=''):
		win = Tkinter.Toplevel() ; win.title(title)
		scroll = Tkinter.Scrollbar(win)
		text = Tkinter.Text(win,yscrollcommand=scroll.set)
		scroll.config(command=text.yview)
		text.insert(Tkinter.END, string.join(txt,'\n'))
		text.pack(side='left',fill='both')
		scroll.pack(side='right',fill='y')
	
	def runprogram(self):
		# prepare
		infile, doctype = self.infile.get(), self.doctype.get()
		if not infile:
			showwarning('txt2tags',"You must provide the source file location!")
			return
		# compose cmdline
		reset_flags(); FLAGS['gui'] = 1
		myflags = []
		for flag in FLAGS.keys():
			if flag in ['maskemail','gui','fixme']:
				continue # not supported
			flag = getattr(self, 'f_%s'%flag)
			if flag.get(): myflags.append(flag.get())
		cmdline = ['txt2tags', '-t', doctype] +myflags +[infile]
		Debug('Gui/tk cmdline: %s'%cmdline,1) 
		# run!
		try:
			infile,outfile,doctype = ParseCmdlineOptions(ParseCmdline(cmdline))
			header,toc,doc = doitall(Readfile(infile), doctype)
			outlist = toc_master(doctype,header,doc,toc)
			if outfile == pipefileid:
				title = 'txt2tags: %s converted to %s'%(
				        os.path.basename(infile),string.upper(doctype))
				self.scrollwindow(outlist, title)
			else:
				finish_him(outlist,outfile)
				msg = "FROM:\n\t%s\nTO:\n\t%s"%(infile,outfile)
				showinfo('txt2tags', "Conversion done!\n\n%s"%msg)
		except ZeroDivisionError:   # common error, not quit
			pass  
		except:                     # fatal error
			traceback.print_exc()
			print '\nSorry! txt2tags-Tk Fatal Error.'
			errmsg = 'Unknown error occurred.\n\nPlease send the Error '+\
			         'Traceback dumped to the author:\n    %s'%my_email
			showerror('txt2tags FATAL ERROR!',errmsg)
			self.exit()
	
	def mainwindow(self):
		action1 = "  \nChoose the target document type:"
		action2 = "\n\nEnter the tagged source file location:"
		action3 = "\n\nSome options you may check:"
		nohead_txt = "Suppress headers from output"
		enum_txt   = "Number titles (1, 1.1, 1.1.1, etc)" 
		toc_txt    = "Do TOC also (Table of Contents)"
		toconly_txt= "Just do TOC, nothing more"
		stdout_txt = "Dump to screen (Don't save target file)"
		
		self.frame = self.frame1
		self.label("TXT2TAGS\n%s\nv%s"%(my_url,my_version)).pack()
		self.label(action1, anchor='w').pack(fill='x')
		self.menu(self.doctype, tags).pack() 
		self.label(action2, anchor='w').pack(fill='x')
		
		self.frame = self.frame2
		self.entry(textvariable=self.infile).pack(side='left',padx=10)
		self.button("Browse", self.askfile).pack(side='right')
		
		self.frame = self.frame3
		self.label(action3, anchor='w').pack(fill='x')
		self.check(nohead_txt ,'--noheaders',variable=self.f_noheaders)
		self.check(enum_txt   ,'--enumtitle',variable=self.f_enumtitle)
		self.check(toc_txt    ,'--toc'      ,variable=self.f_toc)
		self.check(toconly_txt,'--toconly'  ,variable=self.f_toconly)
		self.check(stdout_txt ,'--stdout'   ,variable=self.f_stdout)
		self.label('\n').pack() 
		self.button("Quit", self.exit).pack(side='left',padx=40)
		self.button("Convert!", self.runprogram).pack(side='right',padx=40)
		
		# as documentation told me
		if sys.platform[:3] == 'win':
			self.root.iconify()
			self.root.update()
			self.root.deiconify()
		
		self.root.mainloop()


################################################################################
################################################################################

# set debug are remove option from cmdline
if sys.argv.count('--debug'):
	DEBUG = 1
	sys.argv.remove('--debug')

Debug("system platform: %s"%sys.platform,1)
Debug("line break char: %s"%repr(LB),1)

if FLAGS['gui'] == 1:
	# redefine Error function to raise exception instead sys.exit()
	def Error(msg): showerror('txt2tags ERROR!', msg); raise ZeroDivisionError
	Gui().mainwindow()
else:
	# console mode rocks forever!
	infile, outfile, doctype = ParseCmdlineOptions(ParseCmdline())
	header,toc,doc = doitall(Readfile(infile), doctype)
	if has_obsolete: ObsoletedInstructions(infile)
	if FLAGS['fixme']:
		if has_fixed:
			Savefile(infile+'.OLD', Readfile(infile)) # copy to .old
			Savefile(infile, doc)
			print "\nFile '%s' correctly updated and saved."%(infile)
			print "The old contents were saved to '%s.OLD'."%(infile)
		else:
			print "This file is OK! Nothing to fix."
	else:
		outlist = toc_master(doctype, header, doc, toc)  # TOC!
		finish_him(outlist, outfile)   # writing output to screen or file

sys.exit(0)

#TODO pm6: check all the things @home

###  RESOURCES
# html: http://www.w3.org/TR/WD-html-lex
# man: man 7 man
# sgml: www.linuxdoc.org
# moin: http://twistedmatrix.com/users/jh.twistd/moin/moin.cgi/WikiSandBox
# moin: http://moin.sf.net
# pm6: <font$> turn all formatting to the style's default
# pm6: <#comments#> <font #comment# $>
#  pagemaker table
#  1 = 0,55
#  2 = 1,10
#  3 = 1,65
#  4 = 2,20
#
#        |__1_|    |    |    |    |    |
#        |_______2_|    |    |    |    |
#        |____________3_|    |    |    |
# vim: set ts=4
