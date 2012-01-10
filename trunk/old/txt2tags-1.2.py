#!/usr/bin/env python
# txt2tags - generic text conversion tool
# http://txt2tags.sf.net 
#
# Copyright 2001, 2002 Aurélio Marinho Jargas
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 2.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You have received a copy of the GNU General Public License along
#   with this program, on the COPYING file.
#

# please, don't look at this code, it's ugly!
# i'll try to make it better on the next releases


import re, string, os, sys, getopt, traceback
from time import strftime,time,localtime

my_url = 'http://txt2tags.sf.net'
my_email = 'aurelio@verde666.org'
my_version = '1.2'

DEBUG = 0   # do not edit here, please use --debug
targets = ['txt', 'sgml', 'html', 'pm6', 'mgp', 'moin', 'man', 'tex']
FLAGS = {'noheaders':0,'enumtitle':0,'maskemail':0, 'stdout':0,
         'toconly'  :0,'toc'      :0,'gui'      :0, 'fixme' :0}
regex = {}
TAGS = {}
rules = {}
CMDLINE = ''

currdate = strftime('%Y%m%d',localtime(time()))    # ISO current date
splitlevel = '' ; lang = 'english'
doctype = outfile = ''
pipefileid = '-'
has_obsolete = has_fixed = 0

#my_version = my_version + '-dev' + currdate[4:]  # devel!

# global vars for doClose*()
quotedepth = []
listindent = []
listids = []
subarea = None
tableborder = 0

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
"""%(versionstr, re.sub(r"[]'[]",'',repr(targets)))


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
  'tex': \
r"""\documentclass[11pt,a4paper]{article}
\usepackage{amsfonts,amssymb,graphicx,url}
\usepackage[latin1]{inputenc}  %% for accented chars
\pagestyle{plain}   %% do page numbering ('empty' turns off)
\frenchspacing      %% no aditional spaces after periods
%% all paragraph must be indented equaly
\setlength{\parskip}{8pt}\parindent=0pt
%% uncomment next line for fancy PDF output on Adobe Acrobat Reader
%%\usepackage[pdfstartview=FitV,colorlinks=true,bookmarks=true]{hyperref}

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

def FixFile(file, newcontent):
	Savefile(file+'.OLD', Readfile(file)) # copy to .old
	Savefile(file, newcontent)
	print "\nFile '%s' correctly updated and saved."%(infile)
	print "The old contents were saved to '%s.OLD'."%(infile)

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
		Savefile(outfile, addLineBreaks(outlist))
		if not FLAGS['gui']: print 'wrote %s'%(outfile)
	
	if splitlevel:
		print "--- html..."
		os.system('sgml2html --language=%s --split=%s %s'%(
		           lang,splitlevel,outfile))

def ParseCmdline(cmdline=sys.argv):
	"return a dic with all options:value found"
	global CMDLINE ; CMDLINE = cmdline  # save for dofooter()
	Debug("cmdline: %s"%cmdline, 1)
	options = {'infile': '', 'infiles':''}
	
	# get cmdline options
	longopt = ['help', 'version', 'type=', 'split=', 'lang=']+FLAGS.keys()
	try: (opt, args) = getopt.getopt(cmdline[1:], 'hVt:', longopt)
	except getopt.GetoptError:
		Error('Bad option or missing argument (try --help)')
	
	# get infile, if any
	if args:
		options['infile'] = args[0]
		options['infiles'] = args  # multi
	
	for name,val in opt:
		# parse information options
		if   name in ['-h','--help'   ]: Quit(usage)
		elif name in ['-V','--version']: Quit(versionstr)
		# parse short/long options
		elif name in ['-t','--type']:
			options['doctype'] = val
			continue
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
	
	if not doctype and FLAGS['toconly']: doctype = 'txt' # toconly dft type
	if not infile or not doctype: Quit(usage, 1)    # no filename/doctype
	
	# sanity check: validate target type
	if not targets.count(doctype):
		Error("Invalid document type '%s' (try --help)"%(doctype))
	
	outfile = set_outfile_name(infile, doctype)
	
	# sanity check: validate split level
	if doctype != 'html': splitlevel = '' # only valid for HTML target
	if splitlevel:
		# checkings
		if outfile == pipefileid:
			Error('You need to provide a FILE (not STDIN) '
			      'when using --split')
		if splitlevel[0] not in '012':
			Error('Option --split must be 0, 1 or 2')
		# check for sgml-tools	
		#TODO how to test (in a clever way) if an executable is in path?
		#TODO os.system() return code? sgml2html w/out --help exit 0?
		#TODO bah! implement sgml2html split natively and we're done
		# Error("Sorry, you must have 'sgml2html' to use --split")
		
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
		x,y,toc = convert(['']+toc+['',''], doctype)
		
		# TOC between bars (not for --toconly)
		if FLAGS['toc']:
			para = TAGS['paragraph']
			tocbar = [para, regex['x'].sub('-'*72,TAGS['bar1']), para]
			toc = tocbar + toc + tocbar
		
		if FLAGS['toconly']: header = doc = []
	else:
		toc = []
	
	# on tex, \tableofcontents do it all - see doHeader()
	if doctype == 'tex' and not FLAGS['toconly']:
		toc = []
	
	return header + toc + doc


def doitall(cmdlinedic):
	global outfile
	infile,outfile,doctype = ParseCmdlineOptions(cmdlinedic)
	header,toc,doc = convert(Readfile(infile), doctype)
	outlist = toc_master(doctype,header,doc,toc)
	if has_obsolete: ObsoletedInstructions(infile)
	return doctype, outfile, outlist


# set the Line Break across platforms
LB = '\n'                                   # default
if   sys.platform[:3] == 'win': LB = '\r\n'
#elif sys.platform[:3] == 'cyg': LB = '\r\n' # not sure if it's best :(
elif sys.platform[:3] == 'mac': LB = '\r'

def getTags(doctype):
	keys = [
	'paragraph','title1','title2','title3','title4','title5',
	'areaPreOpen','areaPreClose',
	'areaQuoteOpen','areaQuoteClose',
	'fontMonoOpen','fontMonoClose',
	'fontBoldOpen','fontBoldClose',
	'fontItalicOpen','fontItalicClose',
	'fontBolditalicOpen','fontBolditalicClose',
	'fontUnderlineOpen','fontUnderlineClose',
	'listOpen','listClose','listItem',
	'numlistOpen','numlistClose','numlistItem',
	'deflistOpen','deflistClose','deflistItem1','deflistItem2',
	'bar1','bar2',
	'url','urlMark','email','emailMark',
	'img','imgsolo',
	'tableOpen','tableClose','tableLineOpen','tableLineClose',
	'tableCellOpen','tableCellClose',
	'tableTitleCellOpen','tableTitleCellClose',
	'anchor','comment',
	'EOD'
	]
	
	if doctype == "txt":
		tags = {
		'title1'             : '  \a'      , 
		'title2'             : '\t\a'      ,
		'title3'             : '\t\t\a'    ,
		'title4'             : '\t\t\t\a'  ,
		'title5'             : '\t\t\t\t\a',
		'areaQuoteOpen'      : '    '      ,
		'listItem'           : '- '        ,
		'numlistItem'        : '\a. '      ,
		'bar1'               : '\a'        ,
		'bar2'               : '\a'        ,
		'url'                : '\a'        ,
		'urlMark'            : '\a (\a)'   ,
		'email'              : '\a'        ,
		'emailMark'          : '\a (\a)'   ,
		'img'                : '[\a]'      ,
		}
	
	elif doctype == "html":
		tags = {
		'paragraph'          : '<P>'            ,
		'title1'             : '<H1>\a</H1>'    ,
		'title2'             : '<H2>\a</H2>'    ,
		'title3'             : '<H3>\a</H3>'    ,
		'title4'             : '<H4>\a</H4>'    ,
		'title5'             : '<H5>\a</H5>'    ,
		'areaPreOpen'        : '<PRE>'          ,
		'areaPreClose'       : '</PRE>'         ,
		'areaQuoteOpen'      : '<BLOCKQUOTE>'   ,
		'areaQuoteClose'     : '</BLOCKQUOTE>'  ,
		'fontMonoOpen'       : '<CODE>'         ,
		'fontMonoClose'      : '</CODE>'        ,
		'fontBoldOpen'       : '<B>'            ,
		'fontBoldClose'      : '</B>'           ,
		'fontItalicOpen'     : '<I>'            ,
		'fontItalicClose'    : '</I>'           ,
		'fontBolditalicOpen' : '<B><I>'         ,
		'fontBolditalicClose': '</I></B>'       ,
		'fontUnderlineOpen'  : '<U>'            ,
		'fontUnderlineClose' : '</U>'           ,
		'listOpen'           : '<UL>'           ,
		'listClose'          : '</UL>'          ,
		'listItem'           : '<LI>'           ,
		'numlistOpen'        : '<OL>'           ,
		'numlistClose'       : '</OL>'          ,
		'numlistItem'        : '<LI>'           ,
		'deflistOpen'        : '<DL>'           ,
		'deflistClose'       : '</DL>'          ,
		'deflistItem1'       : '<DT>\a</DT>'    ,
		'deflistItem2'       : '<DD>'           ,
		'bar1'               : '<HR NOSHADE SIZE=1>'        ,
		'bar2'               : '<HR NOSHADE SIZE=5>'        ,
		'url'                : '<A HREF="\a">\a</A>'        ,
		'urlMark'            : '<A HREF="\a">\a</A>'        ,
		'email'              : '<A HREF="mailto:\a">\a</A>' ,
		'emailMark'          : '<A HREF="mailto:\a">\a</A>' ,
		'img'                : '<IMG ALIGN="\a" SRC="\a" BORDER="0">',
		'imgsolo'            : '<P ALIGN="center">\a</P>'   ,
		'tableOpen'          : '<table align=center cellpadding=4 border=\a>',
		'tableClose'         : '</table>'       ,
		'tableLineOpen'      : '<tr>'           ,
		'tableLineClose'     : '</tr>'          ,
		'tableCellOpen'      : '<td>'           ,
		'tableCellClose'     : '</td>'          ,
		'tableTitleCellOpen' : '<th>'           ,
		'tableTitleCellClose': '</th>'          ,
		'anchor'             : '<a name="\a">'  ,
		'comment'            : '<!-- \a -->'    ,
		'EOD'                : '</BODY></HTML>'
		}
	
	elif doctype == "sgml":
		tags = {
		'paragraph'          : '<p>'                ,
		'title1'             : '<sect>\a<p>'        ,
		'title2'             : '<sect1>\a<p>'       ,
		'title3'             : '<sect2>\a<p>'       ,
		'title4'             : '<sect3>\a<p>'       ,
		'title5'             : '<sect4>\a<p>'       ,
		'areaPreOpen'        : '<tscreen><verb>'    ,
		'areaPreClose'       : '</verb></tscreen>'  ,
		'areaQuoteOpen'      : '<quote>'            ,
		'areaQuoteClose'     : '</quote>'           ,
		'fontMonoOpen'       : '<tt>'               ,
		'fontMonoClose'      : '</tt>'              ,
		'fontBoldOpen'       : '<bf>'               ,
		'fontBoldClose'      : '</bf>'              ,
		'fontItalicOpen'     : '<em>'               ,
		'fontItalicClose'    : '</em>'              ,
		'fontBolditalicOpen' : '<bf><em>'           ,
		'fontBolditalicClose': '</em></bf>'         ,
		'fontUnderlineOpen'  : '<bf><em>'           ,
		'fontUnderlineClose' : '</em></bf>'         ,
		'listOpen'           : '<itemize>'          ,
		'listClose'          : '</itemize>'         ,
		'listItem'           : '<item>'             ,
		'numlistOpen'        : '<enum>'             ,
		'numlistClose'       : '</enum>'            ,
		'numlistItem'        : '<item>'             ,
		'bar1'               : '<!-- \a -->'        ,
		'bar2'               : '<!-- \a -->'        ,
		'url'                : '<htmlurl url="\a" name="\a">'        ,
		'urlMark'            : '<htmlurl url="\a" name="\a">'        ,
		'email'              : '<htmlurl url="mailto:\a" name="\a">' ,
		'emailMark'          : '<htmlurl url="mailto:\a" name="\a">' ,
		'img'                : '<figure><ph vspace=""><img src="\a"></figure>',
		'tableOpen'          : '<table><tabular ca="c">'             ,
		'tableClose'         : '</tabular></table>' ,
		'tableLineClose'     : '<rowsep>'           ,
		'tableCellClose'     : '<colsep>'           ,
		'tableTitleCellClose': '<colsep>'           ,
		'comment'            : '<!-- \a -->'        ,
		'EOD'                : '</article>'
		}
	
	elif doctype == "tex":
		tags = {
		'title1'             : '\n\\newpage\section{\a}',
		'title2'             : '\\subsection{\a}'       ,
		'title3'             : '\\subsubsection{\a}'    ,
		# title 4/5: DIRTY: para+BF+\\+\n
		'title4'             : '\\paragraph{}\\textbf{\a}\\\\\\\n' ,
		'title5'             : '\\paragraph{}\\textbf{\a}\\\\\\\n' ,
		'areaPreOpen'        : '\\begin{verbatim}'    ,
		'areaPreClose'       : '\\end{verbatim}'      ,
		'areaQuoteOpen'      : '\\begin{quotation}'   ,
		'areaQuoteClose'     : '\\end{quotation}'     ,
		'fontMonoOpen'       : '\\texttt{'            ,
		'fontMonoClose'      : '}'                    ,
		'fontBoldOpen'       : '\\textbf{'            ,
		'fontBoldClose'      : '}'                    ,
		'fontItalicOpen'     : '\\textit{'            ,
		'fontItalicClose'    : '}'                    ,
		'fontBolditalicOpen' : '\\textbf{\\textit{'   ,
		'fontBolditalicClose': '}}'                   ,
		'fontUnderlineOpen'  : '\\underline{'         ,  
		'fontUnderlineClose' : '}'                    ,
		'listOpen'           : '\\begin{itemize}'     ,
		'listClose'          : '\\end{itemize}'       ,
		'listItem'           : '\\item '              ,
		'numlistOpen'        : '\\begin{enumerate}'   ,
		'numlistClose'       : '\\end{enumerate}'     ,
		'numlistItem'        : '\\item '              ,
		'deflistOpen'        : '\\begin{description}' ,
		'deflistClose'       : '\\end{description}'   ,
		'deflistItem1'       : '\\item[\a]'           ,
		'bar1'               : '\n\\hrulefill{}\n'    ,
		'bar2'               : '\n\\rule{\linewidth}{1mm}\n'    ,
		'url'                : '\\url{\a}'                      ,
		'urlMark'            : '\\textit{\a} (\\url{\a})'       ,
		'email'              : '\\email{\a}'                    ,
		'emailMark'          : '\\textit{\a} (\\email{\a})'     ,
		'img'                : '(\a)'                           ,
		'tableOpen'          : '\\begin{center}\\begin{tabular}',
		'tableClose'         : '\\end{tabular}\\end{center}'    ,
		'tableLineOpen'      : '\\hline '             ,
		'tableLineClose'     : ' \\\\'                ,
		'tableCellClose'     : ' & '                  ,
		'tableTitleCellOpen' : '\\textbf{'            ,
		'tableTitleCellClose': '} & '                 ,
		'comment'            : '% \a'                 ,
		'EOD'                : '\\end{document}'
		}
	
	elif doctype == "moin":
		tags = {
		'title1'             : '= \a ='         ,
		'title2'             : '== \a =='       ,
		'title3'             : '=== \a ==='     ,
		'title4'             : '==== \a ===='   ,
		'title5'             : '===== \a =====' ,
		'areaPreOpen'        : '{{{'            ,
		'areaPreClose'       : '}}}'            ,
		'areaQuoteOpen'      : ' '              ,
		'fontMonoOpen'       : '{{{'            ,
		'fontMonoClose'      : '}}}'            ,
		'fontBoldOpen'       : "'''"            ,
		'fontBoldClose'      : "'''"            ,
		'fontItalicOpen'     : "''"             ,
		'fontItalicClose'    : "''"             ,
		'fontBolditalicOpen' : "'''''"          ,
		'fontBolditalicClose': "'''''"          ,
		'fontUnderlineOpen'  : "'''''"          ,
		'fontUnderlineClose' : "'''''"          , 
		'listItem'           : '* '             ,
		'numlistItem'        : '\a. '           ,
		'bar1'               : '----'           ,
		'bar2'               : '----'           ,
		'url'                : '[\a]'           ,
		'urlMark'            : '[\a \a]'        ,
		'email'              : '[\a]'           ,
		'emailMark'          : '[\a \a]'        ,
		'img'                : '[\a]'           ,
		'tableLineOpen'      : '||'             ,
		'tableCellClose'     : '||'             ,
		'tableTitleCellClose': '||'             ,
		}
	
	elif doctype == "mgp":
		tags = {
		'paragraph'          : '%font "normal", size 5\n'    , 
		'title1'             : '%page\n\n\a'                 ,
		'title2'             : '%page\n\n\a'                 ,
		'title3'             : '%page\n\n\a'                 ,
		'title4'             : '%page\n\n\a'                 ,
		'title5'             : '%page\n\n\a'                 ,
		'areaPreOpen'        : '\n%font "mono"'              ,
		'areaPreClose'       : '%font "normal"'              ,
		'areaQuoteOpen'      : '%prefix "       "'           ,
		'areaQuoteClose'     : '%prefix "  "'                ,
		'fontMonoOpen'       : '\n%cont, font "mono"\n'      ,
		'fontMonoClose'      : '\n%cont, font "normal"\n'    ,
		'fontBoldOpen'       : '\n%cont, font "normal-b"\n'  ,
		'fontBoldClose'      : '\n%cont, font "normal"\n'    ,
		'fontItalicOpen'     : '\n%cont, font "normal-i"\n'  ,
		'fontItalicClose'    : '\n%cont, font "normal"\n'    ,
		'fontBolditalicOpen' : '\n%cont, font "normal-bi"\n' ,
		'fontBolditalicClose': '\n%cont, font "normal"\n'    ,
		'fontUnderlineOpen'  : '\n%cont, fore "cyan"\n'      ,
		'fontUnderlineClose' : '\n%cont, fore "white"\n'     ,
		'numlistItem'        : '\a. '                        ,
		'bar1'               : '%bar "white" 5'              ,
		'bar2'               : '%pause'                      ,
		'url'                : '\n%cont, fore "cyan"\n\a\n%cont, fore "white"\n',
		'urlMark'            : '\a \n%cont, fore "cyan"\n\a\n%cont, fore "white"\n',
		'email'              : '\n%cont, fore "cyan"\n\a\n%cont, fore "white"\n',
		'emailMark'          : '\a \n%cont, fore "cyan"\n\a\n%cont, fore "white"\n',
		'img'                : '\n%center\n%newimage "\a", left\n',
		'comment'            : '%% \a'                       ,
		'EOD'                : '%%EOD'
		}
	
	elif doctype == "man":
		tags = {
		'paragraph'          : '.P'      ,
		'title1'             : '.SH \a'  ,
		'title2'             : '.SS \a'  ,
		'title3'             : '.SS \a'  ,
		'title4'             : '.SS \a'  ,
		'title5'             : '.SS \a'  ,
		'areaPreOpen'        : '.nf'     ,
		'areaPreClose'       : '.fi\n'   ,
		'areaQuoteOpen'      : '\n'      ,
		'areaQuoteClose'     : '\n'      ,
		'fontBoldOpen'       : '\\fB'   ,
		'fontBoldClose'      : '\\fP'   ,
		'fontItalicOpen'     : '\\fI'   ,
		'fontItalicClose'    : '\\fP'   ,
		'fontBolditalicOpen' : '\n.BI '  ,
		'fontBolditalicClose': '\n\\&'   ,
		'listOpen'           : '\n.nf'   ,  # pre
		'listClose'          : '.fi\n'   ,
		'listItem'           : '* '      ,
		'numlistOpen'        : '\n.nf'   ,  # pre
		'numlistClose'       : '.fi\n'   ,
		'numlistItem'        : '\a. '    ,
		'bar1'               : '\n\n'    ,
		'bar2'               : '\n\n'    ,
		'url'                : '\a'      ,
		'urlMark'            : '\a (\a)' ,
		'email'              : '\a'      ,
		'emailMark'          : '\a (\a)' ,
		'img'                : '\a'      ,
		'comment'            : '.\\" \a'
		}
	
	elif doctype == "pm6":
		tags = {
		'paragraph'          : '<@Normal:>'     ,
		'title1'             : '\n<@Title1:>\a' ,
		'title2'             : '\n<@Title2:>\a' ,
		'title3'             : '\n<@Title3:>\a' ,
		'title4'             : '\n<@Title4:>\a' ,
		'title5'             : '\n<@Title5:>\a' ,
		'areaPreOpen'        : '<@PreFormat:>'  ,
		'areaQuoteOpen'      : '<@Quote:>'      ,
		'fontMonoOpen'       : '<FONT "Lucida Console"><SIZE 9>' ,
		'fontMonoClose'      : '<SIZE$><FONT$>' ,
		'fontBoldOpen'       : '<B>'            ,
		'fontBoldClose'      : '<P>'            ,
		'fontItalicOpen'     : '<I>'            ,
		'fontItalicClose'    : '<P>'            , 
		'fontBolditalicOpen' : '<B><I>'         ,
		'fontBolditalicClose': '<P>'            ,
		'fontUnderlineOpen'  : '<U>'            ,
		'fontUnderlineClose' : '<P>'            ,
		'listOpen'           : '<@Bullet:>'     ,
		'listItem'           : '\x95	'       ,   # \x95 == ~U
		'numlistOpen'        : '<@Bullet:>'     ,
		'numlistItem'        : '\x95    '       ,
		'bar1'               : '\a'             ,
		'bar2'               : '\a'             ,
		'url'                : '<U>\a<P>'       ,   # underline
		'urlMark'            : '\a <U>\a<P>'    ,
		'email'              : '\a'             ,
		'emailMark'          : '\a \a'          ,
		'img'                : '\a'             ,
		}
	
	# create empty tags keys
	for key in keys:
		if not tags.has_key(key):
			tags[key] = ''
		else:
			# drawback of using re.sub() - double escape some specials
			# see also: 'force_re' marks on the code
			specials = {'1':'ntsrful', '2':'ntsrf'}
			specials = specials[sys.version[0]]
			tags[key] = re.sub(r'(\\[%s])'%specials,r'\\\1',tags[key])
	
	return tags


def getRules(doctype):
	ret = {}
	allrules = [
	
	 # target rules (ON/OFF)
	  'linkable',           # target supports external links
	  'tableable',          # target supports tables
	  'imgalignable',       # target supports image alignment
	  'listcountable',      # target supports numbered lists natively
	  'tablecellsplit',     # place delimiters only *between* cells
	  'listnotnested',      # lists cannot be nested
	  'quotenotnested',     # quotes cannot be nested 
	  'preareanotescaped',  # don't escape specials in PRE area
	  
	# target code beautify (ON/OFF)
	  'indentprearea',      # add leading spaces to PRE area lines
	  'breaktablecell',     # break lines after any table cell
	  'breaktablelineopen', # break line after opening table line
	  'keepquoteindent',    # don't remove the leading TABs on quotes
	
	# value settings
	  'listmaxdepth',       # maximum depth for lists
	]
	
	rules = {
	  'txt' : {
	    'indentprearea':1
	    },
	  'html': {
	    'indentprearea':1,
	    'linkable':1,
	    'imgalignable':1,
	    'listcountable':1,
	    'tableable':1,
	    'breaktablecell':1,
	    'breaktablelineopen':1,
	    'keepquoteindent':1
	    },
	  'sgml': {
	    'linkable':1,
	    'listcountable':1,
	    'tableable':1,
	    'tablecellsplit':1,
	    'quotenotnested':1,
	    'keepquoteindent':1
	    },
	  'mgp' : {
	    },
	  'tex' : {
	    'listcountable':1,
	    'tableable':1,
	    'tablecellsplit':1,
	    'preareanotescaped':1,
	    'listmaxdepth':4
	    },
	  'moin': {
	    'linkable':1,
	    'tableable':1
	    },
	  'man' : {
	    'indentprearea':1,
	    'listnotnested':1
	    },
	  'pm6' : {
	    }
	}
	
	
	# populate return dictionary
	myrules = rules[doctype]
	for key in allrules      : ret[key] = 0            # reset all
	for key in myrules.keys(): ret[key] = myrules[key] # turn ON
	return ret


def getRegexes():
	regex = {
	# extra at end: (\[(?P<label>\w+)\])? 
	'title':
		re.compile(r'^\s*(?P<tag>={1,5})(?P<txt>[^=].*[^=])\1$'), 
	'areaPreOpen':
		re.compile(r'^---$'), 
	'areaPreClose':
		re.compile(r'^---$'), 
	'quote':
		re.compile(r'^\t+'), 
	'1linePreOld':
		re.compile(r'^ {4}([^\s-])'), 
	'1linePre':
		re.compile(r'^--- '), 
	'fontMono':
		re.compile(r'`([^`]+)`'), 
	'fontBold':
		re.compile(r'\*\*([^\s*].*?)\*\*'), 
	'fontItalic':
		re.compile(r'(^|[^:])//([^ /].*?)//'), 
	'fontUnderline':
		re.compile(r'__([^_].*?)__'), # underline lead/trailing blank
	'fontBolditalic':
		re.compile(r'\*/([^/].*?)/\*'), 
	'list':
		re.compile(r'^( *)([+-]) ([^ ])'), 
	'deflist':
		re.compile(r'^( *)(=) ([^:]+):'), 
	'bar':
		re.compile(r'^\s*([_=-]{20,})\s*$'), 
	'table':
		re.compile(r'^ *\|\|?[<:>]*\s'), 
	'blankline':
		re.compile(r'^\s*$'), 
	'comment':
		re.compile(r'^(//|%)')
	}
	
	# special char to place data on TAGs contents  (\a == bell)
	regex['x'] = re.compile('\a')
	
	# %%date [ (formatting) ]
	regex['date'] = re.compile(r'%%date\b(\((?P<fmt>.*?)\))?', re.I)
	
	
	### complicated regexes begin here ;)
	#
	# textual descriptions on --help's style: [...] is optional, | is OR
	
	
	### first, some auxiliar variables
	#
	
	# [image.EXT]
	patt_img = r'\[([\w_,.+%$#@!?+~/-]+\.(png|jpe?g|gif|eps|bmp))\]'
	
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
	
	# username [ :password ] @
	patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
	
	# [ http:// ] [ username:password@ ] domain.com [ / ] [ #anchor | ?form=data ]
	retxt_url = r'\b(%s%s|%s)[%s]+\b/*(\?[%s]+)?(#[%s]+)?'%(
	             urlskel['proto'],patt_url_login, urlskel['guess'],
	             urlskel['chars'],urlskel['form'],urlskel['anchor'])
	
	# filename | [ filename ] #anchor
	retxt_url_local = r'[%s]+|[%s]*(#[%s]+)'%(
	             urlskel['chars'],urlskel['chars'],urlskel['anchor'])
	
	# user@domain [ ?form=data ]
	patt_email = r'\b[%s]+@([A-Za-z0-9_-]+\.)+[A-Za-z]{2,4}\b(\?[%s]+)?'%(
	             urlskel['login'],urlskel['form'])
	
	
	# saving for future use
	regex['_urlskel'] = urlskel
	
	### and now the real regexes
	#
	
	regex['email'] = re.compile(patt_email,re.I)
	
	# email | url
	regex['link'] = \
		re.compile(r'%s|%s'%(retxt_url,patt_email), re.I)
	
	# \[ label | imagetag    url | email | filename \]
	regex['linkmark'] = \
		re.compile(r'\[(?P<label>%s|[^]]+) (?P<link>%s|%s|%s)\]'%(
		   patt_img, retxt_url, patt_email, retxt_url_local),
		   re.L+re.I)
	
	# image
	regex['img'] = re.compile(patt_img, re.L+re.I)
	
	# all macros
	regex['macro'] = regex['date']
	
	# Settings are still in development stage - DON'T USE THIS
	#regex['setting'] = re.compile(r'^%\s*Document \s*(Encoding|Toc)\s*:\s*(.*)$',re.I)
	
	return regex
### END OF regex nightmares


class SubareaMaster:
	def __init__(self) : self.x = []
	def __call__(self) :
		if not self.x: return ''
		return self.x[-1]
	def add(self, area):
		if not self.x or (self.x and self.x[-1] != area):
			self.x.append(area)
		Debug('subarea ++ (%s): %s' % (area,self.x), 1)
	def pop(self, area=None):
		if area and self.x[-1] == area: self.x.pop()
		Debug('subarea -- (%s): %s' % (area,self.x), 1)

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
					sline = string.replace(
					          line, '%%(%s)s'%key, '')
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
	# the -- string ends a sgml comment :(
	if doctype == 'sgml':
		txt = string.replace(txt, '--', '\\-\\-')
	
	if TAGS['comment']:
		return regex['x'].sub(txt, TAGS['comment'])
	return ''

def doFooter(doctype):
	ret = []
	typename = doctype
	if doctype == 'tex': typename = 'LaTeX2e'
	ppgd = '%s code generated by txt2tags %s (%s)'%(
	        typename,my_version,my_url)
	cmdline = 'cmdline: txt2tags %s'%string.join(CMDLINE[1:], ' ')
	ret.append('\n'+doCommentLine(doctype,ppgd))
	ret.append(doCommentLine(doctype,cmdline))
	ret.append(TAGS['EOD'])
	return ret

def doEscape(doctype,txt):
	if doctype == 'html' or doctype == 'sgml':
		txt = re.sub('&','&amp;',txt)
		txt = re.sub('<','&lt;',txt)
		txt = re.sub('>','&gt;',txt)
		if doctype == 'sgml':
			txt = re.sub('\xff','&yuml;',txt)  # "+y
	elif doctype == 'pm6':
		txt = re.sub('<','<\#60>',txt)
	elif doctype == 'mgp':
		txt = re.sub('^%',' %',txt)  # add leading blank to avoid parse
		#txt = re.sub('^%([^%])','%prefix ""\n  %\n%cont, prefix "  "\n\\1',txt)
	elif doctype == 'man':
		txt = re.sub('^\.', ' .',txt) # command ID
		txt = doEscapeEscapechar(txt)
	elif doctype == 'tex':
		txt = string.replace(txt, '\\', r'\verb!\!')
		txt = string.replace(txt, '~', r'\verb!~!')
		txt = string.replace(txt, '^', r'\verb!^!')
		txt = re.sub('([#$&%{}])', r'\\\1', txt)
		# TIP the _ is escaped at end
	return txt

def doFinalEscape(doctype, txt):
	if   doctype == 'pm6' : txt = string.replace(txt, r'\<',r'<\#92><')
	elif doctype == 'man' : txt = string.replace(txt, '-', r'\-')
	elif doctype == 'tex' : txt = string.replace(txt, '_', r'\_')
	elif doctype == 'sgml': txt = string.replace(txt, '[', '&lsqb;')
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
	if not rules['preareanotescaped']: line = doEscape(doctype,line)
	if rules['indentprearea']: line = '  '+line
	if doctype == 'pm6': line = doFinalEscape(doctype, line)
	return line

def doCloseTable(doctype):
	global subarea, tableborder
	ret = ''
	if rules['tableable']:
		if doctype == 'tex' and tableborder:
			ret = TAGS['tableLineOpen']+TAGS['tableClose']+'\n'
		else:
			ret = TAGS['tableClose']+'\n'
	else:
		ret = TAGS['areaPreClose']
	tableborder = 0
	subarea.pop('table')
	return ret

def doCloseQuote(howmany=None):
	global quotedepth
	ret = []
	if not howmany: howmany = len(quotedepth)
	for i in range(howmany):
		quotedepth.pop()
		#TODO align open/close tag -> FREE_ALING_TAG = 1 (man not)
		ret.append(TAGS['areaQuoteClose'])
	
	if not quotedepth: subarea.pop('quote')
	return string.join(ret,'\n')

def doCloseList(howmany=None):
	global listindent, listids
	ret = []
	if not howmany: howmany = len(listindent)
	for i in range(howmany):
		if   listids[-1] == '-': tag = TAGS['listClose']
		elif listids[-1] == '+': tag = TAGS['numlistClose']
		elif listids[-1] == '=': tag = TAGS['deflistClose']
		if not tag: tag = TAGS['listClose'] # default
		if tag:
			# unnested lists are only closed at mother-list
			if rules['listnotnested']:
				if len(listindent) == 1:
					ret.append(tag)
			else:
				ret.append(listindent[-1]+tag)
		del listindent[-1]
		del listids[-1]
	
	if not listindent: subarea.pop('list')
	return string.join(ret,'\n')


def beautify_me(name, doctype, line):
	"where name is: bold, italic, underline or bolditalic"
	name  = 'font%s' % string.capitalize(name)
	open  = TAGS['%sOpen'%name]
	close = TAGS['%sClose'%name]
	txt = r'%s\1%s'%(open, close)
	if name == 'fontItalic':
		txt = r'\1%s\2%s'%(open, close)
	line = regex[name].sub(txt,line)
	return line


def get_tagged_link(doctype, label, url):
	ret = ''
	
	# set link type
	if regex['email'].match(url):
		linktype = 'email'
	else:
		linktype = 'url';
	
	# adding protocol to guessed link
	guessurl = ''
	if linktype == 'url' and \
	   re.match(regex['_urlskel']['guess'], url):
		if url[0] == 'w': guessurl = 'http://' +url
		else            : guessurl =  'ftp://' +url
		
		# not link aware targets -> protocol is useless 
		if not rules['linkable']: guessurl = ''
	
	# escape specials from TEXT parts
	label = doEscape(doctype,label)
	if not rules['linkable']:
		if doctype == 'tex':
			url = re.sub('^#', '\#', url) # ugly, but compile
		else:
			url = doEscape(doctype,url)
	
	# simple link (not guessed)
	if not label and not guessurl:
		if FLAGS['maskemail'] and linktype == 'email':
			# do the email mask feature (no TAGs, just text)
			url = string.replace(url,'@',' (a) ')
			url = string.replace(url,'.',' ')
			url = "<%s>" % url
			if rules['linkable']: url = doEscape(url)
			ret = url
		else:
			# just add link data to tag
			tag = re.sub('.*', TAGS[linktype], '')  #force_re
			ret = regex['x'].sub(url,tag)
	
	# named link or guessed simple link
	else:
		# adjusts for guessed link
		if not label: label = url       # no   protocol
		if guessurl : url   = guessurl  # with protocol
		
		# handle \ on link label
		label = doEscapeEscapechar(label)
		
		# putting data on the right appearance order
		if rules['linkable']:
			urlorder = [url, label]   # link before label
		else:
			urlorder = [label, url]   # label before link
		
		# get tag
		ret = re.sub('.*', TAGS["%sMark"%linktype], '')  #force_re
		
		# add link data to tag (replace \a's)
		for data in urlorder:
			ret = regex['x'].sub(data,ret,1)
	return ret


def get_image_align(line):
	align = ''
	line = string.strip(line)
	m = regex['img'].search(line)
	ini = m.start() ; head = 0
	end = m.end()   ; tail = len(line)
	
	align = 'center'  # default align              # ^text +img +text$
	if ini == head and end == tail: align = 'para' # ^img$
	elif ini == head: align = 'left'               # ^img + text$
	elif end == tail: align = 'right'              # ^text + img$
	
	return align


def get_table_prop(line):
	# default table proprierties
	ret = {'border': 0, 'type': '|', 'header':0, 'cells':[]}
	# strip and del leading table mark |
	line = string.strip(line)
	line = line[1:]
	# detect (and delete) header mark
	if line[0] == '|':
		ret['header'] = 1
		line = line[1:]
	# detect (and delete) table ID (pipe-made is default)
	if line[0] == '\t':
		ret['type'] = '\t'
		ret['border'] = 1
	line = line[1:]
	# detect (and delete) border mark
	if line[-1] == '|':
		ret['border'] = 1
		line = line[:-1]
	# split cells
	# TODO v1.3: take \t\|?| out
	ret['cells'] = re.split(r'\t\|?| \| ', line)
	
	Debug('Table Prop: %s' % ret, 1)
	return ret


#TODO if ' |   ' table cell is center align
def tag_table_cells(table, doctype):
	ret = ''
	# plain cell
	open, close = TAGS['tableCellOpen'], TAGS['tableCellClose']
	# title cell
	if table['header']:
		open = TAGS['tableTitleCellOpen']
		close = TAGS['tableTitleCellClose']
	# should we break the line?
	if rules['breaktablecell']: close = close+'\n'
	# here we go
	while table['cells']:
		cel = table['cells'].pop(0)
		if not cel and doctype == 'html':
			cel = '&nbsp;'
		# last cell gotchas
		if not table['cells']:
			# don't need cell separator
			if rules['tablecellsplit']: close = ''
			# close beautifier for last title cell
			if doctype == 'tex' and table['header']: close = '}'
		newcell = open + string.strip(cel) + close
		newcell = re.sub('.*', newcell, '') #force_re
		ret = ret + newcell
	return ret


################################################################################
###MerryChristmas,IdontwanttofighttonightwithyouImissyourbodyandIneedyourlove###
################################################################################


def convert(inlines, doctype):
	# global vars for doClose*()
	global TAGS, regex, rules, quotedepth, listindent, listids
	global subarea, tableborder
	global has_obsolete, has_fixed
	
	TAGS = getTags(doctype)
	rules = getRules(doctype)
	regex = getRegexes()
	
	# the defaults
	linkmask  = '@@_link_@@'
	monomask  = '@@_mono_@@'
	macromask = '@@_macro_@@' 
	
	AREA = NewArea('head',0)   # then conf, then body
	subarea = SubareaMaster()
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
	tableborder = 0
	tablealign = []
	has_obsolete = has_fixed = 0
	
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
		
		Debug('LINE %04d: %s' % (linenr,repr(line)), 1)  # for heavy debug
		
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
				holdspace = TAGS['paragraph']+'\n'
		
		# any NOT table line, closes an open table 
		if subarea() == 'table' and not regex['table'].search(line):
			ret.append(doCloseTable(doctype))
		
		
		#---------------------[ PRE formatted ]----------------------
		
		#TIP we'll never support beautifiers inside pre-formatted
		
		# we're already on a PRE area
		if f_tt:
			# closing PRE
			if regex['areaPreClose'].search(line):
				if doctype != 'pm6':
					ret.append(TAGS['areaPreClose'])
				f_tt = 0
				continue
			
			# normal PRE-inside line
			line = doPreLine(doctype, line)
			ret.append(line)
			continue
		
		# detecting PRE area init
		if regex['areaPreOpen'].search(line):
			ret.append(TAGS['areaPreOpen'])
			f_lastblank = 0
			f_tt = 1
			continue
		
		# one line PRE-formatted text
		if regex['1linePre'].search(line):
			f_lastblank = 0
			line = regex['1linePre'].sub('',line)
			line = doPreLine(doctype, line)
			t1, t2 = TAGS['areaPreOpen'],TAGS['areaPreClose']
			ret.append('%s\n%s\n%s'%(t1,line,t2))
			continue
		
		#---------------------[ blank lines ]-----------------------
		
		#TODO "holdspace" to save <p> to not show in closelist
		if regex['blankline'].search(line):
			
			# closing all open quotes
			if quotedepth:
				ret.append(doCloseQuote())
			
			# closing all open lists
			if f_lastblank:      # 2nd consecutive blank line
				if listindent:   # closes list (if any)
					ret.append(doCloseList())
					holdspace = ''
				continue         # consecutive blanks are trash
			
			# normal blank line
			if doctype != 'pm6' and AREA == 'body':
				# paragraph (if any) is wanted inside lists also
				if listindent:
					para = TAGS['paragraph'] + '\n'
					holdspace = holdspace + para
				elif doctype == 'html':
					ret.append(TAGS['paragraph'])
				# sgml: quote close tag must not be \n\n</quote>
				elif doctype == 'sgml' and quotedepth:
					skip_continue = 1
				# otherwise we just print a blank line
				else:
					ret.append('')
			
			f_lastblank = 1
			if not skip_continue: continue
		else:
			f_lastblank = 0      # reset blank status
		
		
		#---------------------[ comments ]-----------------------
		
		# just skip them (if not macro or setting)
		if regex['comment'].search(line) and not regex['date'].match(line):
			
### Still in development stage
#			# detect settings
#			if regex['setting'].search(line):
#				if AREA == 'conf':
#					m = regex['setting'].search(line)
#					name, val = m.group(1), m.group(2)
#					SETTINGS[string.lower(name)] = string.strip(val)
#					Debug("Found Setting '%s', value '%s'"%(name,val),1,linenr)
#				continue
			
			# obsoleted comment format
			if line[0] == '/':
				# fixes it
				if FLAGS['fixme']:
					# discard original line, save new
					fixedinfile.pop()
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
				ret.append(TAGS['paragraph'])
		
		
		#---------------------[ Title ]-----------------------
		
		# man: - should not be escaped, \ turns to \\\\
		
		#TODO set next blank and set f_lastblank or f_lasttitle
		if regex['title'].search(line) and not listindent and AREA == 'body':
			line = doEscape(doctype,line)
			
			# double escape escape char
			if doctype ==  'man':
				line = doEscapeEscapechar(line)
			
			m = regex['title'].search(line)
			tag = m.group('tag')
			level = len(tag)
			tag = TAGS['title%s'%level]
			
			txt = string.strip(m.group('txt'))
			if doctype == 'sgml':
				txt = re.sub(r'\[', r'&lsqb;', txt)
			
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
			if TAGS['anchor'] and FLAGS['toc']:
				ret.append(regex['x'].sub(anchorid,TAGS['anchor']))
			
			# escape to handle \ on title
			idtxt = doEscapeEscapechar(idtxt)
			
			line = regex['title'].sub(tag,line)
			ret.append(regex['x'].sub(idtxt,line))
			
			# let's do some TOC!
			if TAGS['anchor']:
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
			if doctype == 'txt':
				ret.append(regex['x'].sub('='*len(idtxt),tag))
			
			continue
		
		#TODO!	labeltxt = ''
		#		label = m.group('label')
		#		if label: labeltxt = '<label id="%s">' %label
		
		
		#---------------------[ apply masks ]-----------------------
		
		### protect important structures from escaping and formatting
		# protect pre-formatted font text 
		while regex['fontMono'].search(line):
			txt = regex['fontMono'].search(line).group(1)
			monobank.append(doEscape(doctype,txt))
			line = regex['fontMono'].sub(monomask,line,1)
		
		# protect macros
		while regex['macro'].search(line):
			txt = regex['macro'].search(line).group()
			macrobank.append(txt)
			line = regex['macro'].sub(macromask,line,1)
		
		# protect URLs and emails
		while regex['linkmark'].search(line) or regex['link'].search(line):
			
			# try to match plain or named links
			match_link  = regex['link'].search(line)
			match_named = regex['linkmark'].search(line)
			
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
				line  = regex['link'].sub(linkmask,line,1)
			else:                            # named link
				label = string.rstrip(m.group('label'))
				link  = m.group('link')
				line = regex['linkmark'].sub(linkmask,line,1)
			
			# save link data to the link bank
			linkbank.append((label, link))
		
		#---------------------[ do Escapes ]-----------------------
		
		# the target-specific special char escapes for body lines
		line = doEscape(doctype,line)
		
		#---------------------[ Horizontal Bar ]--------------------
		
		if regex['bar'].search(line):
			txt = regex['bar'].search(line).group(1)
			if txt[0] == '=': bar = TAGS['bar2']
			else            : bar = TAGS['bar1']
			
			# to avoid comment tag confusion
			if doctype == 'sgml':
				txt = string.replace(txt,'--','__')
			
			line = regex['bar'].sub(bar,line)
			ret.append(regex['x'].sub(txt,line))
			continue
		
		#---------------------[ Quote ]-----------------------
		
		if regex['quote'].search(line) and AREA == 'body':
			subarea.add('quote')
			
			# store number of leading TABS
			currquotedepth = len(regex['quote'].search(line).group(0))
			
			# SGML doesn't support nested quotes
			if rules['quotenotnested']:
				if quotedepth and currquotedepth > quotedepth[-1]:
					currquotedepth = quotedepth[-1]
			
			# for don't-close-me quote tags
			if not TAGS['areaQuoteClose']:
				line = regex['quote'].sub(TAGS['areaQuoteOpen']*currquotedepth, line)
			else:
				# new (sub)quote
				if not quotedepth or currquotedepth > quotedepth[-1]:
					quotedepth.append(currquotedepth)
					ret.append(TAGS['areaQuoteOpen'])
				
				# remove leading TABs
				if not rules['keepquoteindent']:
					line = regex['quote'].sub('', line)
				
				# closing quotes
				while currquotedepth < quotedepth[-1]:
					ret.append(doCloseQuote(1))
		else:
			# closing all quotes (not quote line)
			if quotedepth: ret.append(doCloseQuote())
		
		
		#---------------------[ Lists ]-----------------------
		
		if (regex['list'].search(line) or
		    regex['deflist'].search(line)) and AREA == 'body':
			subarea.add('list')
			
			if regex['list'].search(line): rgx = regex['list']
			else: rgx = regex['deflist']
			
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
			
			# don't cross depth limit
			maxdepth =  rules['listmaxdepth']
			if maxdepth and len(listindent) == maxdepth:
				if len(listitemindent) > len(listindent[-1]):
					listitemindent = listindent[-1]
			
			# new sublist
			if not listindent or len(listitemindent) > len(listindent[-1]):
				listindent.append(listitemindent)
				listids.append(listtype)
				if   listids[-1] == '-': tag = TAGS['listOpen']
				elif listids[-1] == '+': tag = TAGS['numlistOpen']
				elif listids[-1] == '=': tag = TAGS['deflistOpen']
				if not tag: tag = TAGS['listOpen'] # default
				# no need to reopen <pre> tag on man sublists
				if rules['listnotnested'] and len(listindent) != 1:
					tag = ''
				openlist = listindent[-1]+tag
				if doctype == 'pm6':
					listholdspace = openlist
				else:
					if string.strip(openlist): ret.append(openlist)
				# reset item manual count
				listcount.append(0)
			
			# closing sublists
			while len(listitemindent) < len(listindent[-1]):
				close = doCloseList(1)
				if close: ret.append(close)
				if listcount: del listcount[-1]
			
			# normal item
			listid = listindent[-1]
			if listids[-1] == '-':
				tag = TAGS['listItem']
			elif listids[-1] == '+':
				tag = TAGS['numlistItem']
				listcount[-1] = listcount[-1] +1
				if not rules['listcountable']:
					tag = regex['x'].sub(str(listcount[-1]), tag)
			elif listids[-1] == '=':
				if not TAGS['deflistItem1']:
					# emulate def list, with <li><b>def</b>:
					tag = TAGS['listItem'] +TAGS['fontBoldOpen'] +listdefterm
					tag = tag +TAGS['fontBoldClose'] +':'
				else:
					tag = regex['x'].sub(listdefterm, TAGS['deflistItem1'])
				tag = tag + TAGS['deflistItem2']  # open <DD>
			if doctype == 'mgp': listid = len(listindent)*'\t'
			line = rgx.sub(listid+tag+extra,line)
			if listholdspace:
				line = listholdspace+line
				listholdspace = ''
		
		
		#---------------------[ Table ]-----------------------
		
		#TODO escape undesired format inside table
		#TODO add man, pm6 targets
		if regex['table'].search(line) and AREA == 'body':
			
			table = get_table_prop(line)
			
			if subarea() != 'table':
				# first table line!
				subarea.add('table')
				if rules['tableable']:
					# the first line defines if border or not
					tableborder = table['border']
					
					# tex need some complicated table spec
					if doctype == 'tex':
						cols = len(table['cells'])
						align = 'l'   # l,c,r = left,center,right
						# table spec example: {|l|l|l|}
						spec = '{%s|}' % (('|'+align)*cols)
						# remove border setting (the | char)
						if not tableborder:
							spec = string.replace(spec,'|','')
						ret.append(TAGS['tableOpen']+spec)
					
					# other targets are easier
					else:
						tag = regex['x'].sub(`tableborder`, TAGS['tableOpen'])
						ret.append(tag)
				
				# targets not 'tableable', treat them as preformatted
				else:
					ret.append(TAGS['areaPreOpen'])
			
			if rules['tableable']:
				
				# obsoleted TAB-made table
				if table['type'] == '\t':
					# fix it
					if FLAGS['fixme']:
						# discard original line, save new
						fixedinfile.pop()
						fixedinfile.append(FixTable(untouchedline))
						Fixed(linenr, 'TAB-made table', 'PIPE-made table')
					# just show a warning message
					else:
						Obsoleted(linenr,'TAB-made table',
						  'PIPE-made table','1.3')
				  
				# setting line tags
				tl1 = TAGS['tableLineOpen']
				tl2 = TAGS['tableLineClose']
				
				if rules['breaktablelineopen']:
					tl1 = tl1+'\n'
				if doctype == 'tex' and not tableborder:
					tl1 = ''
				
				# do cells and finish
				cells = tag_table_cells(table, doctype)
				line = tl1 + cells + tl2
		
		
		### BEGIN of at-any-part-of-the-line/various-per-line TAGs.
		
		for beauti in ['Bold', 'Italic', 'Bolditalic', 'Underline']:
			if regex['font%s'%beauti].search(line):
				line = beautify_me(beauti, doctype, line)
		
		#---------------------[ URL & E-mail ]-----------------------
		
		for label,url in linkbank:
			link = get_tagged_link(doctype, label, url)
			line = string.replace(line, linkmask, link, 1)
		
		#---------------------[ Image ]-----------------------
		
		#TODO fix smart align when image is a link label
		while regex['img'].search(line) and TAGS['img'] != '[\a]':
			txt = regex['img'].search(line).group(1)
			tag = TAGS['img']
			
			# HTML is the only align-aware target for now
			if rules['imgalignable']:
				align = get_image_align(line)
				if align == 'para':
					align = 'center'
					tag = regex['x'].sub(tag, TAGS['imgsolo'])
				# add align on tag
				tag = regex['x'].sub(align, tag, 1)
			
			line = regex['img'].sub(tag,line,1)
			line = regex['x'].sub(txt,line,1)
		
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
			while regex['date'].search(line):
				m = regex['date'].search(line)
				fmt = m.group('fmt') or ''
				dateme = currdate
				if fmt: dateme = strftime(fmt,localtime(time()))
				line = regex['date'].sub(dateme,line,1)
		
		#---------------------[ Expand PREs ]-----------------------
		
		for mono in monobank:
			open,close = TAGS['fontMonoOpen'],TAGS['fontMonoClose']
			line = re.sub(monomask,open+mono+close,line,1) #force_re
		
		#---------------------[ Headers ]-----------------------
		
		if AREA == 'head' and linenr < 4:
			HEADERS['HEADER%d'%linenr] = line
			continue
		
		#---------------------[ Final Escapes ]-----------------------
		
		line = doFinalEscape(doctype, line)
		ret.append(holdspace+line)
		holdspace = ''
	
	# EOF: close any open lists/tables/quotes
	#TODO take table exception out when self.doctype 
	while subarea():
		func = eval("doClose%s" % string.capitalize(subarea()))
		parm = None
		if subarea() == 'table': parm = doctype
		txt = func(parm)
		if txt: ret.append(txt)
	
	# add footer
	if not FLAGS['noheaders']:
		ret.extend(doFooter(doctype))
	
	# return only the fixed source document
	if FLAGS['fixme']:
		ret = fixedinfile[:]
		header = [] ; toclist = []
	
	return header,toclist,ret



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
			cmdlinedic = ParseCmdline(cmdline)
			doctype, outfile, outlist = doitall(cmdlinedic)
			infile = cmdlinedic['infile']
			
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
			errmsg = 'Unknown error occurred.\n\n'+\
			         'Please send the Error Traceback '+\
			         'dumped to the author:\n    %s'%my_email
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
		self.menu(self.doctype, targets).pack() 
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


if __name__ == '__main__':

	# check if we will enter on GUI mode
	if len(sys.argv) == 2 and sys.argv[1] == '--gui':
		FLAGS['gui'] = 1
	if len(sys.argv) == 1 and sys.platform[:3] in ['mac','cyg','win']:
		FLAGS['gui'] = 1
	
	# check for GUI mode ressorces
	if FLAGS['gui'] == 1:
		try:
			from tkFileDialog import askopenfilename
			from tkMessageBox import showinfo,showwarning,showerror
			import Tkinter
		except:
			# if GUI was forced, show the error message
			if len(sys.argv) > 1 and sys.argv[1] == '--gui':
				traceback.print_exc()
				sys.exit()
			# or just abandon GUI mode, and continue
			else:
				FLAGS['gui'] = 0
	
	# set debug are remove option from cmdline
	if sys.argv.count('--debug'):
		DEBUG = 1
		sys.argv.remove('--debug')
	
	Debug("system platform: %s"%sys.platform,1)
	Debug("line break char: %s"%repr(LB),1)
	
	if FLAGS['gui'] == 1:
		# redefine Error function to raise exception instead sys.exit()
		def Error(msg):
			showerror('txt2tags ERROR!', msg)
			raise ZeroDivisionError
		Gui().mainwindow()
	else:
		# console mode rocks forever!
		cmdlinedic = ParseCmdline()
		if not cmdlinedic['infiles']: Quit(usage, 1)
		for infile in cmdlinedic['infiles'] or '':
			cmdlinedic['infile'] = infile
			doctype, outfile, outlist = doitall(cmdlinedic)
			
			if FLAGS['fixme']:
				if has_fixed:
					FixFile(infile, outlist)
				else:
					print "%s is OK! Nothing to fix."%infile
			else:
				# writing output to screen or file
				finish_him(outlist, outfile)
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
