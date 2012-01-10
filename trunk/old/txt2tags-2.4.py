#!/usr/bin/env python
# txt2tags - generic text conversion tool
# http://txt2tags.sf.net
#
# Copyright 2001, 2002, 2003, 2004, 2005, 2006 Aurelio Marinho Jargas
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
########################################################################
#
#   BORING CODE EXPLANATION AHEAD
#
# Just read if you wish to understand how the txt2tags code works
#
########################################################################
#
# Version 2.0 was a complete rewrite for the program 'core'.
#
# Now the code that [1] parses the marked text is separated from the
# code that [2] insert the target tags.
#
#   [1] made by: def convert()
#   [2] made by: class BlockMaster
#
# The structures of the marked text are identified and its contents are
# extracted into a data holder (Python lists and dictionaries).
#
# When parsing the source file, the blocks (para, lists, quote, table)
# are opened with BlockMaster, right when found. Then its contents,
# which spans on several lines, are feeded into a special holder on the
# BlockMaster instance. Just when the block is closed, the target tags
# are inserted for the full block as a whole, in one pass. This way, we
# have a better control on blocks. Much better than the previous line by
# line approach.
#
# In other words, whenever inside a block, the parser *holds* the tag
# insertion process, waiting until the full block is read. That was
# needed primary to close paragraphs for the new XHTML target, but
# proved to be a very good adding, improving many other processing.
#
# -------------------------------------------------------------------
#
# There is also a brand new code for the Configuration schema, 100%
# rewritten. There are new classes, all self documented: CommandLine,
# SourceDocument, ConfigMaster and ConfigLines. In short, a new RAW
# Config format was created, and all kind of configuration is first
# converted to this format, and then a generic method parses it.
#
# The init processing was changed also, and now the functions which
# gets informations about the input files are: get_infiles_config(),
#  process_source_file() and convert_this_files()
#
# Other parts are untouched, and remains the same as in v1.7, as the
# marks regexes, target Headers and target Tags & Rules.
#
########################################################################

# Now I think the code is nice, easier to read and understand

#XXX Python coding warning
# Avoid common mistakes:
# - do NOT use newlist=list instead newlist=list[:]
# - do NOT use newdic=dic   instead newdic=dic.copy()
# - do NOT use dic[key]     instead dic.get(key)
# - do NOT use del dic[key] without has_key() before

#XXX Smart Image Align don't work if the image is a link
# Can't fix that because the image is expanded together with the
# link, at the linkbank filling moment. Only the image is passed
# to parse_images(), not the full line, so it is always 'middle'.

#XXX Paragraph separation not valid inside Quote
# Quote will not have <p></p> inside, instead will close and open
# again the <blockquote>. This really sux in CSS, when defining a
# different background color. Still don't know how to fix it.

#XXX TODO (maybe)
# New mark or macro which expands to an anchor full title.
# It is necessary to parse the full document in this order:
#  DONE  1st scan: HEAD: get all settings, including %!includeconf
#  DONE  2nd scan: BODY: expand includes & apply %!preproc
#        3rd scan: BODY: read titles and compose TOC info
#        4th scan: BODY: full parsing, expanding [#anchor] 1st
# Steps 2 and 3 can be made together, with no tag adding.
# Two complete body scans will be *slow*, don't know if it worths.
# One solution may be add the titles as postproc rules


##############################################################################

# User config (1=ON, 0=OFF)

USE_I18N    = 1   # use gettext for i18ned messages?        (default is 1)
COLOR_DEBUG = 1   # show debug messages in colors?          (default is 1)
BG_LIGHT    = 0   # your terminal background color is light (default is 0)
HTML_LOWER  = 0   # use lowercased HTML tags instead upper? (default is 0)

##############################################################################


# These are all the core Python modules used by txt2tags (KISS!)
import re, string, os, sys, time, getopt

# Program information
my_url = 'http://txt2tags.sf.net'
my_name = 'txt2tags'
my_email = 'verde@aurelio.net'
my_version = '2.4'

# i18n - just use if available
if USE_I18N:
	try:
		import gettext
		# If your locale dir is different, change it here
		cat = gettext.Catalog('txt2tags',localedir='/usr/share/locale/')
		_ = cat.gettext
	except:
		_ = lambda x:x
else:
	_ = lambda x:x

# FLAGS   : the conversion related flags  , may be used in %!options
# OPTIONS : the conversion related options, may be used in %!options
# ACTIONS : the other behavior modifiers, valid on command line only
# MACROS  : the valid macros with their default values for formatting
# SETTINGS: global miscellaneous settings, valid on RC file only
# NO_TARGET: actions that don't require a target specification
# NO_MULTI_INPUT: actions that don't accept more than one input file
# CONFIG_KEYWORDS: the valid %!key:val keywords
#
# FLAGS and OPTIONS are configs that affect the converted document.
# They usually have also a --no-<option> to turn them OFF.
# ACTIONS are needed because when doing multiple input files, strange
# behavior would be found, as use command line interface for the
# first file and gui for the second. There is no --no-<action>.
# --version and --help inside %!options are also odd
#
TARGETS  = ['html', 'xhtml', 'sgml', 'tex', 'lout', 'man', 'mgp',
            'moin', 'pm6'  , 'txt']
FLAGS    = {'headers'    :1 , 'enum-title' :0 , 'mask-email' :0 ,
            'toc-only'   :0 , 'toc'        :0 , 'rc'         :1 ,
            'css-sugar'  :0 , 'css-suggar' :0 , 'css-inside' :0 ,
            'quiet'      :0 }
OPTIONS  = {'target'     :'', 'toc-level'  :3 , 'style'      :'',
            'infile'     :'', 'outfile'    :'', 'encoding'   :'',
            'config-file':'', 'split'      :0 , 'lang'       :''}
ACTIONS  = {'help'       :0 , 'version'    :0 , 'gui'        :0 ,
            'verbose'    :0 , 'debug'      :0 , 'dump-config':0 ,
            'dump-source':0 }
MACROS   = {'date' : '%Y%m%d',  'infile': '%f',
            'mtime': '%Y%m%d', 'outfile': '%f'}
SETTINGS = {}         # for future use
NO_TARGET = ['help', 'version', 'gui', 'toc-only', 'dump-config', 'dump-source']
NO_MULTI_INPUT = ['gui','dump-config','dump-source']
CONFIG_KEYWORDS = [
            'target', 'encoding', 'style', 'options', 'preproc','postproc',
            'guicolors']
TARGET_NAMES = {
  'html' : _('HTML page'),
  'xhtml': _('XHTML page'),
  'sgml' : _('SGML document'),
  'tex'  : _('LaTeX document'),
  'lout' : _('Lout document'),
  'man'  : _('UNIX Manual page'),
  'mgp'  : _('MagicPoint presentation'),
  'moin' : _('MoinMoin page'),
  'pm6'  : _('PageMaker document'),
  'txt'  : _('Plain Text'),
}

DEBUG = 0     # do not edit here, please use --debug
VERBOSE = 0   # do not edit here, please use -v, -vv or -vvv
QUIET = 0     # do not edit here, please use --quiet
GUI = 0       # do not edit here, please use --gui
AUTOTOC = 1   # do not edit here, please use --no-toc or %%toc

RC_RAW = []
CMDLINE_RAW = []
CONF = {}
BLOCK = None
regex = {}
TAGS = {}
rules = {}

lang = 'english'
TARGET = ''

STDIN = STDOUT = '-'
MODULEIN = MODULEOUT = '-module-'
ESCCHAR   = '\x00'
SEPARATOR = '\x01'
LISTNAMES = {'-':'list', '+':'numlist', ':':'deflist'}
LINEBREAK = {'default':'\n', 'win':'\r\n', 'mac':'\r'}

# Platform specific settings
LB = LINEBREAK.get(sys.platform[:3]) or LINEBREAK['default']

VERSIONSTR = _("%s version %s <%s>")%(my_name,my_version,my_url)

USAGE = string.join([
'',
_("Usage: %s [OPTIONS] [infile.t2t ...]") % my_name,
'',
_("  -t, --target=TYPE   set target document type. currently supported:"),
'                      %s' % re.sub(r"[]'[]",'',repr(TARGETS)),
_("  -i, --infile=FILE   set FILE as the input file name ('-' for STDIN)"),
_("  -o, --outfile=FILE  set FILE as the output file name ('-' for STDOUT)"),
_("  -H, --no-headers    suppress header, title and footer contents"),
_("      --headers       show header, title and footer contents (default ON)"),
_("      --encoding=ENC  set target file encoding (utf-8, iso-8859-1, etc)"),
_("      --style=FILE    use FILE as the document style (like HTML CSS)"),
_("      --css-sugar     insert CSS-friendly tags for HTML and XHTML targets"),
_("      --css-inside    insert CSS file contents inside HTML/XHTML headers"),
_("      --mask-email    hide email from spam robots. x@y.z turns <x (a) y z>"),
_("      --toc           add TOC (Table of Contents) to target document"),
_("      --toc-only      print document TOC and exit"),
_("      --toc-level=N   set maximum TOC level (depth) to N"),
_("  -n, --enum-title    enumerate all titles as 1, 1.1, 1.1.1, etc"),
_("  -C, --config-file=F read config from file F"),
_("      --rc            read user config file ~/.txt2tagsrc (default ON)"),
_("      --gui           invoke Graphical Tk Interface"),
_("  -q, --quiet         quiet mode, suppress all output (except errors)"),
_("  -v, --verbose       print informative messages during conversion"),
_("  -h, --help          print this help information and exit"),
_("  -V, --version       print program version and exit"),
_("      --dump-config   print all the config found and exit"),
_("      --dump-source   print the document source, with includes expanded"),
'',
_("Turn OFF options:"),
"     --no-outfile, --no-infile, --no-style, --no-encoding, --no-headers",
"     --no-toc, --no-toc-only, --no-mask-email, --no-enum-title, --no-rc",
"     --no-css-sugar, --no-css-inside, --no-quiet, --no-dump-config",
"     --no-dump-source",
'',
_("Example:\n     %s -t html --toc myfile.t2t") % my_name,
'',
_("By default, converted output is saved to 'infile.<target>'."),
_("Use --outfile to force an output file name."),
_("If  input file is '-', reads from STDIN."),
_("If output file is '-', dumps output to STDOUT."),
'',
'http://txt2tags.sourceforge.net',
''
], '\n')


##############################################################################


# Here is all the target's templates
# You may edit them to fit your needs
#  - the %(HEADERn)s strings represent the Header lines
#  - the %(STYLE)s string is changed by --style contents
#  - the %(ENCODING)s string is changed by --encoding contents
#  - if any of the above is empty, the full line is removed
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

  'html': """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<META NAME="generator" CONTENT="http://txt2tags.sf.net">
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%(ENCODING)s">
<LINK REL="stylesheet" TYPE="text/css" HREF="%(STYLE)s">
<TITLE>%(HEADER1)s</TITLE>
</HEAD><BODY BGCOLOR="white" TEXT="black">
<P ALIGN="center"><CENTER><H1>%(HEADER1)s</H1>
<FONT SIZE="4">
<I>%(HEADER2)s</I><BR>
%(HEADER3)s
</FONT></CENTER>
""",

  'htmlcss': """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<META NAME="generator" CONTENT="http://txt2tags.sf.net">
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%(ENCODING)s">
<LINK REL="stylesheet" TYPE="text/css" HREF="%(STYLE)s">
<TITLE>%(HEADER1)s</TITLE>
</HEAD>
<BODY>

<DIV CLASS="header" ID="header">
<H1>%(HEADER1)s</H1>
<H2>%(HEADER2)s</H2>
<H3>%(HEADER3)s</H3>
</DIV>
""",

  'xhtml': """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.sf.net" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>
<body bgcolor="white" text="black">
<div align="center">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</div>
""",

  'xhtmlcss': """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.sf.net" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>
<body>

<div class="header" id="header">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</div>
""",

  'man': """\
.TH "%(HEADER1)s" 1 "%(HEADER3)s" "%(HEADER2)s"
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

  'moin': """\
'''%(HEADER1)s'''

''%(HEADER2)s''

%(HEADER3)s
""",

  'tex': \
r"""\documentclass{article}
\usepackage{graphicx}
\usepackage[urlcolor=blue,colorlinks=true]{hyperref}
\usepackage[%(ENCODING)s]{inputenc}  %% char encoding
\usepackage{%(STYLE)s}  %% user defined

\title{%(HEADER1)s}
\author{%(HEADER2)s}
\begin{document}
\date{%(HEADER3)s}
\maketitle
\clearpage
""",

  'lout': """\
@SysInclude { doc }
@Document
  @InitialFont { Times Base 12p }  # Times, Courier, Helvetica, ...
  @PageOrientation { Portrait }    # Portrait, Landscape
  @ColumnNumber { 1 }              # Number of columns (2, 3, ...)
  @PageHeaders { Simple }          # None, Simple, Titles, NoTitles
  @InitialLanguage { English }     # German, French, Portuguese, ...
  @OptimizePages { Yes }           # Yes/No smart page break feature
//
@Text @Begin
@Display @Heading { %(HEADER1)s }
@Display @I { %(HEADER2)s }
@Display { %(HEADER3)s }
#@NP                               # Break page after Headers
"""
# @SysInclude { tbl }                   # Tables support
# setup: @MakeContents { Yes }          # show TOC
# setup: @SectionGap                    # break page at each section
}


##############################################################################


def getTags(config):
	"Returns all the known tags for the specified target"
	
	keys = [
	'paragraphOpen','paragraphClose',
	'title1','title2','title3','title4','title5',
	'title1Open','title1Close','title2Open','title2Close',
	'blocktitle1Open','title1Close','title2Open','title2Close',
	'title3Open','title3Close','title4Open','title4Close',
	'title5Open','title5Close',
	'numtitle1','numtitle2','numtitle3','numtitle4','numtitle5',
	'blockVerbOpen','blockVerbClose',
	'blockQuoteOpen','blockQuoteClose','blockQuoteLine',
	'blockCommentOpen','blockCommentClose',
	'fontMonoOpen','fontMonoClose',
	'fontBoldOpen','fontBoldClose',
	'fontItalicOpen','fontItalicClose',
	'fontUnderlineOpen','fontUnderlineClose',
	'listOpen','listClose',
	'listItemOpen','listItemClose','listItemLine',
	'numlistOpen','numlistClose',
	'numlistItemOpen','numlistItemClose','numlistItemLine',
	'deflistOpen','deflistClose',
	'deflistItem1Open','deflistItem1Close',
	'deflistItem2Open','deflistItem2Close',
	'bar1','bar2',
	'url','urlMark','email','emailMark',
	'img','imgAlignLeft','imgAlignRight','imgAlignCenter',
	'tableOpen','tableClose',
	'tableRowOpen','tableRowClose','tableRowSep',
	'tableCellOpen','tableCellClose','tableCellSep',
	'tableTitleCellOpen','tableTitleCellClose','tableTitleCellSep',
	'tableTitleRowOpen','tableTitleRowClose',
	'tableBorder', 'tableAlignLeft', 'tableAlignCenter',
	'tableCellAlignLeft','tableCellAlignRight','tableCellAlignCenter',
	'tableColAlignLeft','tableColAlignRight','tableColAlignCenter',
	'tableColAlignSep', 'tableCellColSpan',
	'anchor','comment','pageBreak',
	'TOC','tocOpen','tocClose',
	'cssOpen', 'cssClose',
	'bodyOpen','bodyClose',
	'EOD'
	]
	
	# TIP: \a represents the current text on the mark
	# TIP: ~A~, ~B~ and ~C~ are expanded to other tags parts
	
	alltags = {
	
	'txt': {
	   'title1'              : '  \a'      ,
	   'title2'              : '\t\a'      ,
	   'title3'              : '\t\t\a'    ,
	   'title4'              : '\t\t\t\a'  ,
	   'title5'              : '\t\t\t\t\a',
	   'blockQuoteLine'      : '\t'        ,
	   'listItemOpen'        : '- '        ,
	   'numlistItemOpen'     : '\a. '      ,
	   'bar1'                : '\a'        ,
	   'url'                 : '\a'        ,
	   'urlMark'             : '\a (\a)'   ,
	   'email'               : '\a'        ,
	   'emailMark'           : '\a (\a)'   ,
	   'img'                 : '[\a]'      ,
	},
	
	'html': {
	   'paragraphOpen'       : '<P>'            ,
	   'paragraphClose'      : '</P>'           ,
	   'title1'              : '~A~<H1>\a</H1>' ,
	   'title2'              : '~A~<H2>\a</H2>' ,
	   'title3'              : '~A~<H3>\a</H3>' ,
	   'title4'              : '~A~<H4>\a</H4>' ,
	   'title5'              : '~A~<H5>\a</H5>' ,
	   'blockVerbOpen'       : '<PRE>'          ,
	   'blockVerbClose'      : '</PRE>'         ,
	   'blockQuoteOpen'      : '<BLOCKQUOTE>'   ,
	   'blockQuoteClose'     : '</BLOCKQUOTE>'  ,
	   'fontMonoOpen'        : '<CODE>'         ,
	   'fontMonoClose'       : '</CODE>'        ,
	   'fontBoldOpen'        : '<B>'            ,
	   'fontBoldClose'       : '</B>'           ,
	   'fontItalicOpen'      : '<I>'            ,
	   'fontItalicClose'     : '</I>'           ,
	   'fontUnderlineOpen'   : '<U>'            ,
	   'fontUnderlineClose'  : '</U>'           ,
	   'listOpen'            : '<UL>'           ,
	   'listClose'           : '</UL>'          ,
	   'listItemOpen'        : '<LI>'           ,
	   'numlistOpen'         : '<OL>'           ,
	   'numlistClose'        : '</OL>'          ,
	   'numlistItemOpen'     : '<LI>'           ,
	   'deflistOpen'         : '<DL>'           ,
	   'deflistClose'        : '</DL>'          ,
	   'deflistItem1Open'    : '<DT>'           ,
	   'deflistItem1Close'   : '</DT>'          ,
	   'deflistItem2Open'    : '<DD>'           ,
	   'bar1'                : '<HR NOSHADE SIZE=1>'        ,
	   'bar2'                : '<HR NOSHADE SIZE=5>'        ,
	   'url'                 : '<A HREF="\a">\a</A>'        ,
	   'urlMark'             : '<A HREF="\a">\a</A>'        ,
	   'email'               : '<A HREF="mailto:\a">\a</A>' ,
	   'emailMark'           : '<A HREF="mailto:\a">\a</A>' ,
	   'img'                 : '<IMG~A~ SRC="\a" BORDER="0" ALT="">',
	   'imgAlignLeft'        : ' ALIGN="left"'  ,
	   'imgAlignCenter'      : ' ALIGN="middle"',
	   'imgAlignRight'       : ' ALIGN="right"' ,
	   'tableOpen'           : '<TABLE~A~ CELLPADDING="4"~B~>',
	   'tableClose'          : '</TABLE>'       ,
	   'tableRowOpen'        : '<TR>'           ,
	   'tableRowClose'       : '</TR>'          ,
	   'tableCellOpen'       : '<TD~A~~S~>'      ,
	   'tableCellClose'      : '</TD>'          ,
	   'tableTitleCellOpen'  : '<TH~S~>'        ,
	   'tableTitleCellClose' : '</TH>'          ,
	   'tableBorder'         : ' BORDER="1"'    ,
	   'tableAlignCenter'    : ' ALIGN="center"',
	   'tableCellAlignRight' : ' ALIGN="right"' ,
	   'tableCellAlignCenter': ' ALIGN="center"',
	   'tableCellColSpan'    : ' COLSPAN="\a"'  ,
	   'anchor'              : '<A NAME="\a"></A>\n',
	   'cssOpen'             : '<STYLE TYPE="text/css">',
	   'cssClose'            : '</STYLE>'       ,
	   'comment'             : '<!-- \a -->'    ,
	   'EOD'                 : '</BODY></HTML>'
	},
	
	#TIP xhtml inherits all HTML definitions (lowercased)
	#TIP http://www.w3.org/TR/xhtml1/#guidelines
	#TIP http://www.htmlref.com/samples/Chapt17/17_08.htm
	'xhtml': {
	   'listItemClose'       : '</li>'          ,
	   'numlistItemClose'    : '</li>'          ,
	   'deflistItem2Close'   : '</dd>'          ,
	   'bar1'                : '<hr class="light" />',
	   'bar2'                : '<hr class="heavy" />',
	   'anchor'              : '<a id="\a" name="\a"></a>\n',
	   'img'                 : '<img~A~ src="\a" border="0" alt=""/>',
	},
	
	'sgml': {
	   'paragraphOpen'       : '<p>'                ,
	   'title1'              : '<sect>\a~A~<p>'     ,
	   'title2'              : '<sect1>\a~A~<p>'    ,
	   'title3'              : '<sect2>\a~A~<p>'    ,
	   'title4'              : '<sect3>\a~A~<p>'    ,
	   'title5'              : '<sect4>\a~A~<p>'    ,
	   'blockVerbOpen'       : '<tscreen><verb>'    ,
	   'blockVerbClose'      : '</verb></tscreen>'  ,
	   'blockQuoteOpen'      : '<quote>'            ,
	   'blockQuoteClose'     : '</quote>'           ,
	   'fontMonoOpen'        : '<tt>'               ,
	   'fontMonoClose'       : '</tt>'              ,
	   'fontBoldOpen'        : '<bf>'               ,
	   'fontBoldClose'       : '</bf>'              ,
	   'fontItalicOpen'      : '<em>'               ,
	   'fontItalicClose'     : '</em>'              ,
	   'fontUnderlineOpen'   : '<bf><em>'           ,
	   'fontUnderlineClose'  : '</em></bf>'         ,
	   'listOpen'            : '<itemize>'          ,
	   'listClose'           : '</itemize>'         ,
	   'listItemOpen'        : '<item>'             ,
	   'numlistOpen'         : '<enum>'             ,
	   'numlistClose'        : '</enum>'            ,
	   'numlistItemOpen'     : '<item>'             ,
	   'deflistOpen'         : '<descrip>'          ,
	   'deflistClose'        : '</descrip>'         ,
	   'deflistItem1Open'    : '<tag>'              ,
	   'deflistItem1Close'   : '</tag>'             ,
	   'bar1'                : '<!-- \a -->'        ,
	   'url'                 : '<htmlurl url="\a" name="\a">'        ,
	   'urlMark'             : '<htmlurl url="\a" name="\a">'        ,
	   'email'               : '<htmlurl url="mailto:\a" name="\a">' ,
	   'emailMark'           : '<htmlurl url="mailto:\a" name="\a">' ,
	   'img'                 : '<figure><ph vspace=""><img src="\a">'+\
	                           '</figure>'                           ,
	   'tableOpen'           : '<table><tabular ca="~C~">'           ,
	   'tableClose'          : '</tabular></table>' ,
	   'tableRowSep'         : '<rowsep>'           ,
	   'tableCellSep'        : '<colsep>'           ,
	   'tableColAlignLeft'   : 'l'                  ,
	   'tableColAlignRight'  : 'r'                  ,
	   'tableColAlignCenter' : 'c'                  ,
	   'comment'             : '<!-- \a -->'        ,
	   'anchor'              : '<label id="\a">'    ,
	   'TOC'                 : '<toc>'              ,
	   'EOD'                 : '</article>'
	},
	
	'tex': {
	   'title1'              : '\n\section*{\a}'     ,
	   'title2'              : '\\subsection*{\a}'   ,
	   'title3'              : '\\subsubsection*{\a}',
	   # title 4/5: DIRTY: para+BF+\\+\n
	   'title4'              : '\\paragraph{}\\textbf{\a}\\\\\n',
	   'title5'              : '\\paragraph{}\\textbf{\a}\\\\\n',
	   'numtitle1'           : '\n\section{\a}'      ,
	   'numtitle2'           : '\\subsection{\a}'    ,
	   'numtitle3'           : '\\subsubsection{\a}' ,
	   'blockVerbOpen'       : '\\begin{verbatim}'   ,
	   'blockVerbClose'      : '\\end{verbatim}'     ,
	   'blockQuoteOpen'      : '\\begin{quotation}'  ,
	   'blockQuoteClose'     : '\\end{quotation}'    ,
	   'fontMonoOpen'        : '\\texttt{'           ,
	   'fontMonoClose'       : '}'                   ,
	   'fontBoldOpen'        : '\\textbf{'           ,
	   'fontBoldClose'       : '}'                   ,
	   'fontItalicOpen'      : '\\textit{'           ,
	   'fontItalicClose'     : '}'                   ,
	   'fontUnderlineOpen'   : '\\underline{'        ,
	   'fontUnderlineClose'  : '}'                   ,
	   'listOpen'            : '\\begin{itemize}'    ,
	   'listClose'           : '\\end{itemize}'      ,
	   'listItemOpen'        : '\\item '             ,
	   'numlistOpen'         : '\\begin{enumerate}'  ,
	   'numlistClose'        : '\\end{enumerate}'    ,
	   'numlistItemOpen'     : '\\item '             ,
	   'deflistOpen'         : '\\begin{description}',
	   'deflistClose'        : '\\end{description}'  ,
	   'deflistItem1Open'    : '\\item['             ,
	   'deflistItem1Close'   : ']'                   ,
	   'bar1'                : '\n\\hrulefill{}\n'   ,
	   'bar2'                : '\n\\rule{\linewidth}{1mm}\n',
	   'url'                 : '\\htmladdnormallink{\a}{\a}',
	   'urlMark'             : '\\htmladdnormallink{\a}{\a}',
	   'email'               : '\\htmladdnormallink{\a}{mailto:\a}',
	   'emailMark'           : '\\htmladdnormallink{\a}{mailto:\a}',
	   'img'                 : '\\includegraphics{\a}',
	   'tableOpen'           : '\\begin{center}\\begin{tabular}{|~C~|}',
	   'tableClose'          : '\\end{tabular}\\end{center}',
	   'tableRowOpen'        : '\\hline ' ,
	   'tableRowClose'       : ' \\\\'    ,
	   'tableCellSep'        : ' & '      ,
	   'tableColAlignLeft'   : 'l'        ,
	   'tableColAlignRight'  : 'r'        ,
	   'tableColAlignCenter' : 'c'        ,
	   'tableColAlignSep'    : '|'        ,
	   'comment'             : '% \a'     ,
	   'TOC'                 : '\\tableofcontents',
	   'pageBreak'           : '\\clearpage',
	   'EOD'                 : '\\end{document}'
	},
	
	'lout': {
	   'paragraphOpen'       : '@LP'                     ,
	   'blockTitle1Open'     : '@BeginSections'          ,
	   'blockTitle1Close'    : '@EndSections'            ,
	   'blockTitle2Open'     : ' @BeginSubSections'      ,
	   'blockTitle2Close'    : ' @EndSubSections'        ,
	   'blockTitle3Open'     : '  @BeginSubSubSections'  ,
	   'blockTitle3Close'    : '  @EndSubSubSections'    ,
	   'title1Open'          : '\n@Section @Title { \a } @Begin',
	   'title1Close'         : '@End @Section'           ,
	   'title2Open'          : '\n @SubSection @Title { \a } @Begin',
	   'title2Close'         : ' @End @SubSection'       ,
	   'title3Open'          : '\n  @SubSubSection @Title { \a } @Begin',
	   'title3Close'         : '  @End @SubSubSection'   ,
	   'title4Open'          : '\n@LP @LeftDisplay @B { \a }',
	   'title5Open'          : '\n@LP @LeftDisplay @B { \a }',
	   'anchor'              : '@Tag { \a }'             ,
	   'blockVerbOpen'       : '@LP @ID @F @RawVerbatim @Begin',
	   'blockVerbClose'      : '@End @RawVerbatim'   ,
	   'blockQuoteOpen'      : '@QD {'               ,
	   'blockQuoteClose'     : '}'                   ,
	   # enclosed inside {} to deal with joined**words**
	   'fontMonoOpen'        : '{@F {'               ,
	   'fontMonoClose'       : '}}'                  ,
	   'fontBoldOpen'        : '{@B {'               ,
	   'fontBoldClose'       : '}}'                  ,
	   'fontItalicOpen'      : '{@II {'              ,
	   'fontItalicClose'     : '}}'                  ,
	   'fontUnderlineOpen'   : '{@Underline{'        ,
	   'fontUnderlineClose'  : '}}'                  ,
	   # the full form is more readable, but could be BL EL LI NL TL DTI
	   'listOpen'            : '@BulletList'         ,
	   'listClose'           : '@EndList'            ,
	   'listItemOpen'        : '@ListItem{'          ,
	   'listItemClose'       : '}'                   ,
	   'numlistOpen'         : '@NumberedList'       ,
	   'numlistClose'        : '@EndList'            ,
	   'numlistItemOpen'     : '@ListItem{'          ,
	   'numlistItemClose'    : '}'                   ,
	   'deflistOpen'         : '@TaggedList'         ,
	   'deflistClose'        : '@EndList'            ,
	   'deflistItem1Open'    : '@DropTagItem {'      ,
	   'deflistItem1Close'   : '}'                   ,
	   'deflistItem2Open'    : '{'                   ,
	   'deflistItem2Close'   : '}'                   ,
	   'bar1'                : '\n@DP @FullWidthRule\n'     ,
	   'url'                 : '{blue @Colour { \a }}'      ,
	   'urlMark'             : '\a ({blue @Colour { \a }})' ,
	   'email'               : '{blue @Colour { \a }}'      ,
	   'emailMark'           : '\a ({blue Colour{ \a }})'   ,
	   'img'                 : '~A~@IncludeGraphic { \a }'  ,  # eps only!
	   'imgAlignLeft'        : '@LeftDisplay '              ,
	   'imgAlignRight'       : '@RightDisplay '             ,
	   'imgAlignCenter'      : '@CentredDisplay '           ,
	   # lout tables are *way* complicated, no support for now
	   #'tableOpen'          : '~A~@Tbl~B~\naformat{ @Cell A | @Cell B } {',
	   #'tableClose'         : '}'     ,
	   #'tableRowOpen'       : '@Rowa\n'       ,
	   #'tableTitleRowOpen'  : '@HeaderRowa'       ,
	   #'tableCenterAlign'   : '@CentredDisplay '         ,
	   #'tableCellOpen'      : '\a {'                     ,  # A, B, ...
	   #'tableCellClose'     : '}'                        ,
	   #'tableBorder'        : '\nrule {yes}'             ,
	   'comment'             : '# \a'                     ,
	   # @MakeContents must be on the config file
	   'TOC'                 : '@DP @ContentsGoesHere @DP',
	   'pageBreak'           : '\n@NP\n'                  ,
	   'EOD'                 : '@End @Text'
	},
	
	'moin': {
	   'title1'              : '= \a ='        ,
	   'title2'              : '== \a =='      ,
	   'title3'              : '=== \a ==='    ,
	   'title4'              : '==== \a ===='  ,
	   'title5'              : '===== \a =====',
	   'blockVerbOpen'       : '{{{'           ,
	   'blockVerbClose'      : '}}}'           ,
	   'blockQuoteLine'      : '  '            ,
	   'fontMonoOpen'        : '{{{'           ,
	   'fontMonoClose'       : '}}}'           ,
	   'fontBoldOpen'        : "'''"           ,
	   'fontBoldClose'       : "'''"           ,
	   'fontItalicOpen'      : "''"            ,
	   'fontItalicClose'     : "''"            ,
	   'fontUnderlineOpen'   : "__"            ,
	   'fontUnderlineClose'  : "__"            ,
	   'listItemOpen'        : ' * '           ,
	   'numlistItemOpen'     : ' \a. '         ,
	   'bar1'                : '----'          ,
	   'url'                 : '[\a]'          ,
	   'urlMark'             : '[\a \a]'       ,
	   'email'               : '[\a]'          ,
	   'emailMark'           : '[\a \a]'       ,
	   'img'                 : '[\a]'          ,
	   'tableRowOpen'        : '||'            ,
	   'tableCellOpen'       : '~A~'           ,
	   'tableCellClose'      : '||'            ,
	   'tableTitleCellClose' : '||'            ,
	   'tableCellAlignRight' : '<)>'           ,
	   'tableCellAlignCenter': '<:>'           ,
	   'comment'             : '## \a'         ,
	   'TOC'                 : '[[TableOfContents]]'
	},
	
	'mgp': {
	   'paragraphOpen'       : '%font "normal", size 5'     ,
	   'title1'              : '%page\n\n\a\n'              ,
	   'title2'              : '%page\n\n\a\n'              ,
	   'title3'              : '%page\n\n\a\n'              ,
	   'title4'              : '%page\n\n\a\n'              ,
	   'title5'              : '%page\n\n\a\n'              ,
	   'blockVerbOpen'       : '%font "mono"'               ,
	   'blockVerbClose'      : '%font "normal"'             ,
	   'blockQuoteOpen'      : '%prefix "       "'          ,
	   'blockQuoteClose'     : '%prefix "  "'               ,
	   'fontMonoOpen'        : '\n%cont, font "mono"\n'     ,
	   'fontMonoClose'       : '\n%cont, font "normal"\n'   ,
	   'fontBoldOpen'        : '\n%cont, font "normal-b"\n' ,
	   'fontBoldClose'       : '\n%cont, font "normal"\n'   ,
	   'fontItalicOpen'      : '\n%cont, font "normal-i"\n' ,
	   'fontItalicClose'     : '\n%cont, font "normal"\n'   ,
	   'fontUnderlineOpen'   : '\n%cont, fore "cyan"\n'     ,
	   'fontUnderlineClose'  : '\n%cont, fore "white"\n'    ,
	   'listItemLine'        : '\t'                         ,
	   'numlistItemLine'     : '\t'                         ,
	   'deflistItem1Open'    : '\t\n%cont, font "normal-b"\n',
	   'deflistItem1Close'   : '\n%cont, font "normal"\n'   ,
	   'bar1'                : '%bar "white" 5'             ,
	   'bar2'                : '%pause'                     ,
	   'url'                 : '\n%cont, fore "cyan"\n\a'   +\
	                           '\n%cont, fore "white"\n'    ,
	   'urlMark'             : '\a \n%cont, fore "cyan"\n\a'+\
	                           '\n%cont, fore "white"\n'    ,
	   'email'               : '\n%cont, fore "cyan"\n\a'   +\
	                           '\n%cont, fore "white"\n'    ,
	   'emailMark'           : '\a \n%cont, fore "cyan"\n\a'+\
	                           '\n%cont, fore "white"\n'    ,
	   'img'                 : '~A~\n%newimage "\a"\n%left\n',
	   'imgAlignLeft'        : '\n%left'                    ,
	   'imgAlignRight'       : '\n%right'                   ,
	   'imgAlignCenter'      : '\n%center'                  ,
	   'comment'             : '%% \a'                      ,
	   'pageBreak'           : '%page\n\n\n'                ,
	   'EOD'                 : '%%EOD'
	},
	
	# man groff_man ; man 7 groff
	'man': {
	   'paragraphOpen'       : '.P'     ,
	   'title1'              : '.SH \a' ,
	   'title2'              : '.SS \a' ,
	   'title3'              : '.SS \a' ,
	   'title4'              : '.SS \a' ,
	   'title5'              : '.SS \a' ,
	   'blockVerbOpen'       : '.nf'    ,
	   'blockVerbClose'      : '.fi\n'  ,
	   'blockQuoteOpen'      : '.RS'    ,
	   'blockQuoteClose'     : '.RE'    ,
	   'fontBoldOpen'        : '\\fB'   ,
	   'fontBoldClose'       : '\\fR'   ,
	   'fontItalicOpen'      : '\\fI'   ,
	   'fontItalicClose'     : '\\fR'   ,
	   'listOpen'            : '.RS'    ,
	   'listItemOpen'        : '.IP \(bu 3\n',
	   'listClose'           : '.RE'    ,
	   'numlistOpen'         : '.RS'    ,
	   'numlistItemOpen'     : '.IP \a. 3\n',
	   'numlistClose'        : '.RE'    ,
	   'deflistItem1Open'    : '.TP\n'  ,
	   'bar1'                : '\n\n'   ,
	   'url'                 : '\a'     ,
	   'urlMark'             : '\a (\a)',
	   'email'               : '\a'     ,
	   'emailMark'           : '\a (\a)',
	   'img'                 : '\a'     ,
	   'tableOpen'           : '.TS\n~A~~B~tab(^); ~C~.',
	   'tableClose'          : '.TE'     ,
	   'tableRowOpen'        : ' '       ,
	   'tableCellSep'        : '^'       ,
	   'tableAlignCenter'    : 'center, ',
	   'tableBorder'         : 'allbox, ',
	   'tableColAlignLeft'   : 'l'       ,
	   'tableColAlignRight'  : 'r'       ,
	   'tableColAlignCenter' : 'c'       ,
	   'comment'             : '.\\" \a'
	},
	
	'pm6': {
	   'paragraphOpen'       : '<@Normal:>'    ,
	   'title1'              : '\n<@Title1:>\a',
	   'title2'              : '\n<@Title2:>\a',
	   'title3'              : '\n<@Title3:>\a',
	   'title4'              : '\n<@Title4:>\a',
	   'title5'              : '\n<@Title5:>\a',
	   'blockVerbOpen'       : '<@PreFormat:>' ,
	   'blockQuoteLine'      : '<@Quote:>'     ,
	   'fontMonoOpen'        : '<FONT "Lucida Console"><SIZE 9>' ,
	   'fontMonoClose'       : '<SIZE$><FONT$>',
	   'fontBoldOpen'        : '<B>'           ,
	   'fontBoldClose'       : '<P>'           ,
	   'fontItalicOpen'      : '<I>'           ,
	   'fontItalicClose'     : '<P>'           ,
	   'fontUnderlineOpen'   : '<U>'           ,
	   'fontUnderlineClose'  : '<P>'           ,
	   'listOpen'            : '<@Bullet:>'    ,
	   'listItemOpen'        : '\x95\t'        ,  # \x95 == ~U
	   'numlistOpen'         : '<@Bullet:>'    ,
	   'numlistItemOpen'     : '\x95\t'        ,
	   'bar1'                : '\a'            ,
	   'url'                 : '<U>\a<P>'      ,  # underline
	   'urlMark'             : '\a <U>\a<P>'   ,
	   'email'               : '\a'            ,
	   'emailMark'           : '\a \a'         ,
	   'img'                 : '\a'
	}
	}
	
	# Exceptions for --css-sugar
	if config['css-sugar'] and config['target'] in ('html','xhtml'):
		# Change just HTML because XHTML inherits it
		htmltags = alltags['html']
		# Table with no cellpadding
		htmltags['tableOpen'] = string.replace(
			htmltags['tableOpen'], ' CELLPADDING="4"', '')
		# DIVs
		htmltags['tocOpen' ] = '<DIV CLASS="toc" ID="toc">'
		htmltags['tocClose'] = '</DIV>'
		htmltags['bodyOpen'] = '<DIV CLASS="body" ID="body">'
		htmltags['bodyClose']= '</DIV>'
	
	# Make the HTML -> XHTML inheritance
	xhtml = alltags['html'].copy()
	for key in xhtml.keys(): xhtml[key] = string.lower(xhtml[key])
	# Some like HTML tags as lowercase, some don't... (headers out)
	if HTML_LOWER: alltags['html'] = xhtml.copy()
	xhtml.update(alltags['xhtml'])
	alltags['xhtml'] = xhtml.copy()
	
	# Compose the target tags dictionary
	tags = {}
	target_tags = alltags[config['target']].copy()
	
	for key in keys: tags[key] = ''     # create empty keys
	for key in target_tags.keys():
		tags[key] = maskEscapeChar(target_tags[key]) # populate
	
	# Map strong line to separator if not defined
	if not tags['bar2'] and tags['bar1']:
		tags['bar2'] = tags['bar1']
	
	return tags


##############################################################################


def getRules(config):
	"Returns all the target-specific syntax rules"
	
	ret = {}
	allrules = [
	
	 # target rules (ON/OFF)
	  'linkable',             # target supports external links
	  'tableable',            # target supports tables
	  'imglinkable',          # target supports images as links
	  'imgalignable',         # target supports image alignment
	  'imgasdefterm',         # target supports image as definition term
	  'autonumberlist',       # target supports numbered lists natively
	  'autonumbertitle',      # target supports numbered titles natively
	  'stylable',             # target supports external style files
	  'parainsidelist',       # lists items supports paragraph
	  'spacedlistitem',       # lists support blank lines between items
	  'listnotnested',        # lists cannot be nested
	  'quotenotnested',       # quotes cannot be nested
	  'verbblocknotescaped',  # don't escape specials in verb block
	  'verbblockfinalescape', # do final escapes in verb block
	  'escapeurl',            # escape special in link URL
	  'onelinepara',          # dump paragraph as a single long line
	  'tabletitlerowinbold',  # manually bold any cell on table titles
	  'tablecellstrip',       # strip extra spaces from each table cell
	  'tablecellspannable',   # the table cells can have span attribute
	  'barinsidequote',       # bars are allowed inside quote blocks
	  'finalescapetitle',     # perform final escapes on title lines
	  'autotocnewpagebefore', # break page before automatic TOC
	  'autotocnewpageafter',  # break page after automatic TOC
	  'autotocwithbars',      # automatic TOC surrounded by bars
	  'mapbar2pagebreak',     # map the strong bar to a page break
	  'titleblocks',          # titles must be on open/close section blocks
	
	# Target code beautify (ON/OFF)
	  'indentverbblock',      # add leading spaces to verb block lines
	  'breaktablecell',       # break lines after any table cell
	  'breaktablelineopen',   # break line after opening table line
	  'notbreaklistopen',     # don't break line after opening a new list
	  'notbreakparaopen',     # don't break line after opening a new para
	  'keepquoteindent',      # don't remove the leading TABs on quotes
	  'keeplistindent',       # don't remove the leading spaces on lists
	  'blankendmotherlist',   # append a blank line at the mother list end
	  'blankendtable',        # append a blank line at the table end
	  'blankendautotoc',      # append a blank line at the auto TOC end
	  'tagnotindentable',     # tags must be placed at the line begining
	
	# Value settings
	  'listmaxdepth',         # maximum depth for lists
	  'quotemaxdepth',        # maximum depth for quotes
	  'tablecellaligntype'    # type of table cell align: cell, column
	]
	
	rules_bank = {
	  'txt' : {
	    'indentverbblock':1,
	    'spacedlistitem':1,
	    'parainsidelist':1,
	    'keeplistindent':1,
	    'barinsidequote':1,
	    'autotocwithbars':1,
	    'blankendmotherlist':1
	    },
	  'html': {
	    'indentverbblock':1,
	    'linkable':1,
	    'stylable':1,
	    'escapeurl':1,
	    'imglinkable':1,
	    'imgalignable':1,
	    'imgasdefterm':1,
	    'autonumberlist':1,
	    'spacedlistitem':1,
	    'parainsidelist':1,
	    'blankendmotherlist':1,
	    'tableable':1,
	    'tablecellstrip':1,
	    'blankendtable':1,
	    'breaktablecell':1,
	    'breaktablelineopen':1,
	    'keeplistindent':1,
	    'keepquoteindent':1,
	    'barinsidequote':1,
	    'autotocwithbars':1,
	    'tablecellspannable':1,
	    'tablecellaligntype':'cell'
	    },
	  #TIP xhtml inherits all HTML rules
	  'xhtml': {
	    },
	  'sgml': {
	    'linkable':1,
	    'escapeurl':1,
	    'autonumberlist':1,
	    'spacedlistitem':1,
	    'blankendmotherlist':1,
	    'tableable':1,
	    'tablecellstrip':1,
	    'blankendtable':1,
	    'blankendautotoc':1,
	    'quotenotnested':1,
	    'keeplistindent':1,
	    'keepquoteindent':1,
	    'barinsidequote':1,
	    'finalescapetitle':1,
	    'tablecellaligntype':'column'
	    },
	  'mgp' : {
	    'blankendmotherlist':1,
	    'tagnotindentable':1,
	    'spacedlistitem':1,
	    'imgalignable':1,
	    'autotocnewpagebefore':1,
	    },
	  'tex' : {
	    'stylable':1,
	    'escapeurl':1,
	    'autonumberlist':1,
	    'autonumbertitle':1,
	    'spacedlistitem':1,
	    'blankendmotherlist':1,
	    'tableable':1,
	    'tablecellstrip':1,
	    'tabletitlerowinbold':1,
	    'blankendtable':1,
	    'verbblocknotescaped':1,
	    'keeplistindent':1,
	    'listmaxdepth':4,  # deflist is 6
	    'quotemaxdepth':6,
	    'barinsidequote':1,
	    'finalescapetitle':1,
	    'autotocnewpageafter':1,
	    'mapbar2pagebreak':1,
	    'tablecellaligntype':'column'
	    },
	  'lout': {
	    'keepquoteindent':1,
	    'escapeurl':1,
	    'verbblocknotescaped':1,
	    'imgalignable':1,
	    'mapbar2pagebreak':1,
	    'titleblocks':1,
	    'notbreakparaopen':1
	    },
	  'moin': {
	    'spacedlistitem':1,
	    'linkable':1,
	    'blankendmotherlist':1,
	    'keeplistindent':1,
	    'tableable':1,
	    'barinsidequote':1,
	    'blankendtable':1,
	    'tabletitlerowinbold':1,
	    'tablecellstrip':1,
	    'autotocwithbars':1,
	    'tablecellaligntype':'cell'
	    },
	  'man' : {
	    'spacedlistitem':1,
	    'indentverbblock':1,
	    'blankendmotherlist':1,
	    'tagnotindentable':1,
	    'tableable':1,
	    'tablecellaligntype':'column',
	    'tabletitlerowinbold':1,
	    'tablecellstrip':1,
	    'blankendtable':1,
	    'keeplistindent':0,
	    'barinsidequote':1,
	    'parainsidelist':0,
	    },
	  'pm6' : {
	    'keeplistindent':1,
	    'verbblockfinalescape':1,
	    #TODO add support for these - maybe set a JOINNEXT char and
	    #     do it on addLineBreaks()
	    'notbreaklistopen':1,
	    'notbreakparaopen':1,
	    'barinsidequote':1,
	    'autotocwithbars':1,
	    'onelinepara':1,
	    }
	}
	
	# Exceptions for --css-sugar
	if config['css-sugar'] and config['target'] in ('html','xhtml'):
		rules_bank['html']['indentverbblock'] = 0
		rules_bank['html']['autotocwithbars'] = 0
	
	# Get the target specific rules
	if config['target'] == 'xhtml':
		myrules = rules_bank['html'].copy()   # inheritance
		myrules.update(rules_bank['xhtml'])   # get XHTML specific
	else:
		myrules = rules_bank[config['target']].copy()
	
	# Populate return dictionary
	for key in allrules: ret[key] = 0        # reset all
	ret.update(myrules)                      # get rules
	
	return ret


##############################################################################


def getRegexes():
	"Returns all the regexes used to find the t2t marks"
	
	bank = {
	'blockVerbOpen':
		re.compile(r'^```\s*$'),
	'blockVerbClose':
		re.compile(r'^```\s*$'),
	'blockRawOpen':
		re.compile(r'^"""\s*$'),
	'blockRawClose':
		re.compile(r'^"""\s*$'),
	'blockCommentOpen':
		re.compile(r'^%%%\s*$'),
	'blockCommentClose':
		re.compile(r'^%%%\s*$'),
	'quote':
		re.compile(r'^\t+'),
	'1lineVerb':
		re.compile(r'^``` (?=.)'),
	'1lineRaw':
		re.compile(r'^""" (?=.)'),
	# mono, raw, bold, italic, underline:
	# - marks must be glued with the contents, no boundary spaces
	# - they are greedy, so in ****bold****, turns to <b>**bold**</b>
	'fontMono':
		re.compile(  r'``([^\s](|.*?[^\s])`*)``'),
	'raw':
		re.compile(  r'""([^\s](|.*?[^\s])"*)""'),
	'fontBold':
		re.compile(r'\*\*([^\s](|.*?[^\s])\**)\*\*'),
	'fontItalic':
		re.compile(  r'//([^\s](|.*?[^\s])/*)//'),
	'fontUnderline':
		re.compile(  r'__([^\s](|.*?[^\s])_*)__'),
	'list':
		re.compile(r'^( *)(-) (?=[^ ])'),
	'numlist':
		re.compile(r'^( *)(\+) (?=[^ ])'),
	'deflist':
		re.compile(r'^( *)(:) (.*)$'),
	'listclose':
		re.compile(r'^( *)([-+:])\s*$'),
	'bar':
		re.compile(r'^(\s*)([_=-]{20,})\s*$'),
	'table':
		re.compile(r'^ *\|\|? '),
	'blankline':
		re.compile(r'^\s*$'),
	'comment':
		re.compile(r'^%'),
	
	# Auxiliary tag regexes
	'_imgAlign'        : re.compile(r'~A~', re.I),
	'_tableAlign'      : re.compile(r'~A~', re.I),
	'_anchor'          : re.compile(r'~A~', re.I),
	'_tableBorder'     : re.compile(r'~B~', re.I),
	'_tableColAlign'   : re.compile(r'~C~', re.I),
	'_tableCellColSpan': re.compile(r'~S~', re.I),
	'_tableCellAlign'  : re.compile(r'~A~', re.I),
	}
	
	# Special char to place data on TAGs contents  (\a == bell)
	bank['x'] = re.compile('\a')
	
	# %%macroname [ (formatting) ]
	bank['macros'] = re.compile(r'%%%%(?P<name>%s)\b(\((?P<fmt>.*?)\))?'%(
	                            string.join(MACROS.keys(), '|')), re.I)
	
	# %%TOC special macro for TOC positioning
	bank['toc'] = re.compile(r'^ *%%toc\s*$', re.I)
	
	# Almost complicated title regexes ;)
	titskel = r'^ *(?P<id>%s)(?P<txt>%s)\1(\[(?P<label>[\w-]*)\])?\s*$'
	bank[   'title'] = re.compile(titskel%('[=]{1,5}','[^=](|.*[^=])'))
	bank['numtitle'] = re.compile(titskel%('[+]{1,5}','[^+](|.*[^+])'))
	
	### Complicated regexes begin here ;)
	#
	# Textual descriptions on --help's style: [...] is optional, | is OR
	
	
	### First, some auxiliary variables
	#
	
	# [image.EXT]
	patt_img = r'\[([\w_,.+%$#@!?+~/-]+\.(png|jpe?g|gif|eps|bmp))\]'
	
	# Link things
	# http://www.gbiv.com/protocols/uri/rfc/rfc3986.html
	# pchar: A-Za-z._~- / %FF / !$&'()*+,;= / :@
	# Recomended order: scheme://user:pass@domain/path?query=foo#anchor
	# Also works      : scheme://user:pass@domain/path#anchor?query=foo
	# TODO form: !'():
	urlskel = {
	  'proto' : r'(https?|ftp|news|telnet|gopher|wais)://',
	  'guess' : r'(www[23]?|ftp)\.',         # w/out proto, try to guess
	  'login' : r'A-Za-z0-9_.-',             # for ftp://login@domain.com
	  'pass'  : r'[^ @]*',                   # for ftp://login:pass@dom.com
	  'chars' : r'A-Za-z0-9%._/~:,=$@&+-',   # %20(space), :80(port), D&D
	  'anchor': r'A-Za-z0-9%._-',            # %nn(encoded)
	  'form'  : r'A-Za-z0-9/%&=+;.,$@*_-',   # .,@*_-(as is)
	  'punct' : r'.,;:!?'
	}
	
	# username [ :password ] @
	patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
	
	# [ http:// ] [ username:password@ ] domain.com [ / ]
	#     [ #anchor | ?form=data ]
	retxt_url = r'\b(%s%s|%s)[%s]+\b/*(\?[%s]+)?(#[%s]*)?'%(
	             urlskel['proto'],patt_url_login, urlskel['guess'],
	             urlskel['chars'],urlskel['form'],urlskel['anchor'])
	
	# filename | [ filename ] #anchor
	retxt_url_local = r'[%s]+|[%s]*(#[%s]*)'%(
	             urlskel['chars'],urlskel['chars'],urlskel['anchor'])
	
	# user@domain [ ?form=data ]
	patt_email = r'\b[%s]+@([A-Za-z0-9_-]+\.)+[A-Za-z]{2,4}\b(\?[%s]+)?'%(
	             urlskel['login'],urlskel['form'])
	
	# Saving for future use
	bank['_urlskel'] = urlskel
	
	### And now the real regexes
	#
	
	bank['email'] = re.compile(patt_email,re.I)
	
	# email | url
	bank['link'] = re.compile(r'%s|%s'%(retxt_url,patt_email), re.I)
	
	# \[ label | imagetag    url | email | filename \]
	bank['linkmark'] = re.compile(
		r'\[(?P<label>%s|[^]]+) (?P<link>%s|%s|%s)\]'%(
		  patt_img, retxt_url, patt_email, retxt_url_local),
		re.L+re.I)
	
	# Image
	bank['img'] = re.compile(patt_img, re.L+re.I)
	
	# Special things
	bank['special'] = re.compile(r'^%!\s*')
	return bank
### END OF regex nightmares


##############################################################################

class error(Exception):
	pass
def echo(msg):   # for quick debug
	print '\033[32;1m%s\033[m'%msg
def Quit(msg=''):
	if msg: print msg
	sys.exit(0)
def Error(msg):
	msg = _("%s: Error: ")%my_name + msg
	raise error, msg
def getTraceback():
	try:
		from traceback import format_exception
		etype, value, tb = sys.exc_info()
		return string.join(format_exception(etype, value, tb), '')
	except: pass
def getUnknownErrorMessage():
	msg = '%s\n%s (%s):\n\n%s'%(
	  _('Sorry! Txt2tags aborted by an unknown error.'),
	  _('Please send the following Error Traceback to the author'),
	  my_email, getTraceback())
	return msg
def Message(msg,level):
	if level <= VERBOSE and not QUIET:
		prefix = '-'*5
		print "%s %s"%(prefix*level, msg)
def Debug(msg,id=0,linenr=None):
	"Show debug messages, categorized (colored or not)"
	if QUIET or not DEBUG: return
	if int(id) not in range(8): id = 0
	# 0:black 1:red 2:green 3:yellow 4:blue 5:pink 6:cyan 7:white ;1:light
	ids            = ['INI','CFG','SRC','BLK','HLD','GUI','OUT','DET']
	colors_bgdark  = ['7;1','1;1','3;1','6;1','4;1','5;1','2;1','7;1']
	colors_bglight = ['0'  ,'1'  ,'3'  ,'6'  ,'4'  ,'5'  ,'2'  ,'0'  ]
	if linenr is not None: msg = "LINE %04d: %s"%(linenr,msg)
	if COLOR_DEBUG:
		if BG_LIGHT: color = colors_bglight[id]
		else       : color = colors_bgdark[id]
		msg = '\033[3%sm%s\033[m'%(color,msg)
	print "++ %s: %s"%(ids[id],msg)
def Readfile(file, remove_linebreaks=0, ignore_error=0):
	data = []
	if file == '-':
		try: data = sys.stdin.readlines()
		except:
			if not ignore_error:
				Error(_('You must feed me with data on STDIN!'))
	else:
		try: f = open(file); data = f.readlines() ; f.close()
		except:
			if not ignore_error:
				Error(_("Cannot read file:")+" %s"%file)
	if remove_linebreaks:
		data = map(lambda x:re.sub('[\n\r]+$','',x), data)
	Message(_("File read (%d lines): %s")%(len(data),file),2)
	return data
def Savefile(file, contents):
	try: f = open(file, 'wb')
	except: Error(_("Cannot open file for writing:")+" %s"%file)
	if type(contents) == type([]): doit = f.writelines
	else: doit = f.write
	doit(contents) ; f.close()

def showdic(dic):
	for k in dic.keys(): print "%15s : %s" % (k,dic[k])
def dotted_spaces(txt=''):
	return string.replace(txt,' ','.')

# TIP: win env vars http://www.winnetmag.com/Article/ArticleID/23873/23873.html
def get_rc_path():
	"Return the full path for the users' RC file"
	# Try to get the path from an env var. if yes, we're done
	user_defined = os.environ.get('T2TCONFIG')
	if user_defined: return user_defined
	# Env var not found, so perform automatic path composing
	# Set default filename according system platform
	rc_names = {'default':'.txt2tagsrc', 'win':'_t2trc'}
	rc_file = rc_names.get(sys.platform[:3]) or rc_names['default']
	# The file must be on the user directory, but where is this dir?
	rc_dir_search = ['HOME', 'HOMEPATH']
	for var in rc_dir_search:
		rc_dir = os.environ.get(var)
		if rc_dir: break
	# rc dir found, now we must join dir+file to compose the full path
	if rc_dir:
		# Compose path and return it if the file exists
		rc_path = os.path.join(rc_dir, rc_file)
		# On windows, prefix with the drive (%homedrive%: 2k/XP/NT)
		if sys.platform[:3] == 'win':
			rc_drive = os.environ.get('HOMEDRIVE')
			rc_path = os.path.join(rc_drive,rc_path)
		return rc_path
	# Sorry, not found
	return ''



##############################################################################

class CommandLine:
	"""
	Command Line class - Masters command line

	This class checks and extract data from the provided command line.
	The --long options and flags are taken from the global OPTIONS,
	FLAGS and ACTIONS dictionaries. The short options are registered
	here, and also their equivalence to the long ones.

	METHODS:
	  _compose_short_opts() -> str
	  _compose_long_opts() -> list
	      Compose the valid short and long options list, on the
	      'getopt' format.
	  
	  parse() -> (opts, args)
	      Call getopt to check and parse the command line.
	      It expects to receive the command line as a list, and
	      without the program name (sys.argv[1:]).
	  
	  get_raw_config() -> [RAW config]
	      Scans command line and convert the data to the RAW config
	      format. See ConfigMaster class to the RAW format description.
	      Optional 'ignore' and 'filter' arguments are used to filter
	      in or out specified keys.
	  
	  compose_cmdline(dict) -> [Command line]
	      Compose a command line list from an already parsed config
	      dictionary, generated from RAW by ConfigMaster(). Use
	      this to compose an optimal command line for a group of
	      options.
	
	The get_raw_config() calls parse(), so the tipical use of this
	class is:
	
            raw = CommandLine().get_raw_config(sys.argv[1:])
	"""
	def __init__(self):
		self.all_options = OPTIONS.keys()
		self.all_flags   = FLAGS.keys()
		self.all_actions = ACTIONS.keys()
		
		# short:long options equivalence
		self.short_long = {
		  'h':'help'     ,   'V':'version',
		  'n':'enum-title',  'i':'infile' ,
		  'H':'no-headers',  'o':'outfile',
		  'v':'verbose'   ,  't':'target' ,
		  'q':'quiet'     ,  'C':'config-file'
		}
		
		# Compose valid short and long options data for getopt
		self.short_opts = self._compose_short_opts()
		self.long_opts  = self._compose_long_opts()
	
	def _compose_short_opts(self):
		"Returns a string like 'hVt:o' with all short options/flags"
		ret = []
		for opt in self.short_long.keys():
			long = self.short_long[opt]
			if long in self.all_options: # is flag or option?
				opt = opt+':'        # option: have param
			ret.append(opt)
		#Debug('Valid SHORT options: %s'%ret)
		return string.join(ret, '')
	
	def _compose_long_opts(self):
		"Returns a list with all the valid long options/flags"
		ret = map(lambda x:x+'=', self.all_options)          # add =
		ret.extend(self.all_flags)                           # flag ON
		ret.extend(self.all_actions)                         # acts
		ret.extend(map(lambda x:'no-'+x, self.all_flags))    # add no-*
		ret.extend(['no-style','no-encoding'])               # turn OFF
		ret.extend(['no-outfile','no-infile'])               # turn OFF
		ret.extend(['no-dump-config', 'no-dump-source'])     # turn OFF
		#Debug('Valid LONG options: %s'%ret)
		return ret
	
	def _tokenize(self, cmd_string=''):
		"Convert a command line string to a list"
		#TODO protect quotes contents
		return string.split(cmd_string)
	
	def parse(self, cmdline=[]):
		"Check/Parse a command line list     TIP: no program name!"
		# Get the valid options
		short, long = self.short_opts, self.long_opts
		# Parse it!
		try:
			opts, args = getopt.getopt(cmdline, short, long)
		except getopt.error, errmsg:
			Error(_("%s (try --help)")%errmsg)
		return (opts, args)
	
	def get_raw_config(self, cmdline=[], ignore=[], filter=[], relative=0):
		"Returns the options/arguments found as RAW config"
		if not cmdline: return []
		ret = []
		# We need lists, not strings
		if type(cmdline) == type(''): cmdline = self._tokenize(cmdline)
		opts, args = self.parse(cmdline[:])
		# Parse all options
		for name,value in opts:
			# Remove leading - and --
			name = re.sub('^--?', '', name)
			# Alias to old misspelled 'suGGar'
			if   name ==    'css-suggar': name =    'css-sugar'
			elif name == 'no-css-suggar': name = 'no-css-sugar'
			# Translate short opt to long
			if len(name) == 1: name = self.short_long.get(name)
			# Outfile exception: path relative to PWD
			if name == 'outfile' and relative \
			   and value not in [STDOUT, MODULEOUT]:
				value = os.path.abspath(value)
			# config-file inclusion, path relative to PWD
			if name == 'config-file':
				configs = ConfigLines().include_config_file(
				          value)
				# Remove the 'target' item of all configs
				configs = map(lambda c: [c[1],c[2]], configs)
				ret.extend(configs)
				continue
			# Save it
			ret.append([name, value])
		# Get infile, if any
		while args:
			infile = args.pop(0)
			ret.append(['infile', infile])
		# Apply 'ignore' and 'filter' rules (filter is stronger)
		temp = ret[:] ; ret = []
		for name,value in temp:
			if (not filter and not ignore) or \
			   (filter and name in filter) or \
			   (ignore and name not in ignore):
				ret.append( ['all', name, value] )
		# Add the original command line string as 'realcmdline'
		ret.append( ['all', 'realcmdline', cmdline] )
		return ret
	
	def compose_cmdline(self, conf={}, no_check=0):
		"compose a full (and diet) command line from CONF dict"
		if not conf: return []
		args = []
		dft_options = OPTIONS.copy()
		cfg = conf.copy()
		valid_opts = self.all_options + self.all_flags
		use_short = {'no-headers':'H', 'enum-title':'n'}
		# Remove useless options
		if not no_check and cfg.get('toc-only'):
			if cfg.has_key('no-headers'):
				del cfg['no-headers']
			if cfg.has_key('outfile'):
				del cfg['outfile']      # defaults to STDOUT
			if cfg.get('target') == 'txt':
				del cfg['target']       # already default
			args.append('--toc-only')  # must be the first
			del cfg['toc-only']
		# Add target type
		if cfg.has_key('target'):
			args.append('-t '+cfg['target'])
			del cfg['target']
		# Add other options
		for key in cfg.keys():
			if key not in valid_opts: continue  # may be a %!setting
			if key == 'outfile' or key == 'infile': continue # later
			val = cfg[key]
			if not val: continue
			# Default values are useless on cmdline
			if val == dft_options.get(key): continue
			# -short format
			if key in use_short.keys():
				args.append('-'+use_short[key])
				continue
			# --long format
			if key in self.all_flags: # add --option
				args.append('--'+key)
			else:                     # add --option=value
				args.append('--%s=%s'%(key,val))
		# The outfile using -o
		if cfg.has_key('outfile') and \
		   cfg['outfile'] != dft_options.get('outfile'):
			args.append('-o '+cfg['outfile'])
		# Place input file(s) always at the end
		if cfg.has_key('infile'):
			args.append(string.join(cfg['infile'],' '))
		# Return as a nice list
		Debug("Diet command line: %s"%string.join(args,' '), 1)
		return args

##############################################################################

class SourceDocument:
	"""
	SourceDocument class - scan document structure, extract data
	
	It knows about full files. It reads a file and identify all
	the areas begining (Head,Conf,Body). With this info it can
	extract each area contents.
	Note: the original line break is removed.
	
	DATA:
	  self.arearef - Save Head, Conf, Body init line number
	  self.areas   - Store the area names which are not empty
	  self.buffer  - The full file contents (with NO \\r, \\n)

	METHODS:
	  get()   - Access the contents of an Area. Example:
	            config = SourceDocument(file).get('conf')
	
	  split() - Get all the document Areas at once. Example:
	            head, conf, body = SourceDocument(file).split()
	
	RULES:
	    * The document parts are sequential: Head, Conf and Body.
	    * One ends when the next begins.
	    * The Conf Area is optional, so a document can have just
	      Head and Body Areas.
	
	    These are the Areas limits:
	      - Head Area: the first three lines
	      - Body Area: from the first valid text line to the end
	      - Conf Area: the comments between Head and Body Areas

	    Exception: If the first line is blank, this means no
	    header info, so the Head Area is just the first line.
	"""
	def __init__(self, filename='', contents=[]):
		self.areas = ['head','conf','body']
		self.arearef = []
		self.areas_fancy = ''
		self.filename = filename
		self.buffer = []
		if filename:
			self.scan_file(filename)
		elif contents:
			self.scan(contents)
	
	def split(self):
		"Returns all document parts, splitted into lists."
		return self.get('head'), self.get('conf'), self.get('body')
	
	def get(self, areaname):
		"Returns head|conf|body contents from self.buffer"
		# Sanity
		if areaname not in self.areas: return []
		if not self.buffer           : return []
		# Go get it
		bufini = 1
		bufend = len(self.buffer)
		if   areaname == 'head':
			ini = bufini
			end = self.arearef[1] or self.arearef[2] or bufend
		elif areaname == 'conf':
			ini = self.arearef[1]
			end = self.arearef[2] or bufend
		elif areaname == 'body':
			ini = self.arearef[2]
			end = bufend
		else:
			Error("Unknown Area name '%s'"%areaname)
		lines = self.buffer[ini:end]
		# Make sure head will always have 3 lines
		while areaname == 'head' and len(lines) < 3:
			lines.append('')
		return lines
	
	def scan_file(self, filename):
		Debug("source file: %s"%filename)
		Message(_("Loading source document"),1)
		buf = Readfile(filename, remove_linebreaks=1)
		self.scan(buf)
	
	def scan(self, lines):
		"Run through source file and identify head/conf/body areas"
		buf = lines
		if len(buf) == 0:
			Error(_('The input file is empty: %s')%self.filename)
		cfg_parser = ConfigLines().parse_line
		buf.insert(0, '')                         # text start at pos 1
		ref = [1,4,0]
		if not string.strip(buf[1]):              # no header
			ref[0] = 0 ; ref[1] = 2
		rgx = getRegexes()
		on_comment_block = 0
		for i in xrange(ref[1],len(buf)):         # find body init:
			# Handle comment blocks inside config area
			if not on_comment_block \
			   and rgx['blockCommentOpen'].search(buf[i]):
				on_comment_block = 1
				continue
			if on_comment_block \
			   and rgx['blockCommentOpen'].search(buf[i]):
				on_comment_block = 0
				continue
			if on_comment_block: continue
			
			if string.strip(buf[i]) and (     # ... not blank and
			   buf[i][0] != '%' or            # ... not comment or
			   rgx['macros'].match(buf[i]) or # ... %%macro
			   rgx['toc'].match(buf[i])    or # ... %%toc
			   cfg_parser(buf[i],'include')[1]): # ... %!include
				ref[2] = i ; break
		if ref[1] == ref[2]: ref[1] = 0           # no conf area
		for i in 0,1,2:                           # del !existent
			if ref[i] >= len(buf): ref[i] = 0 # title-only
			if not ref[i]: self.areas[i] = ''
		Debug('Head,Conf,Body start line: %s'%ref)
		self.arearef = ref                        # save results
		self.buffer  = buf
		# Fancyness sample: head conf body (1 4 8)
		self.areas_fancy = "%s (%s)"%(
		     string.join(self.areas),
		     string.join(map(str, map(lambda x:x or '', ref))))
		Message(_("Areas found: %s")%self.areas_fancy, 2)
	
	def get_raw_config(self):
		"Handy method to get the CONF area RAW config (if any)"
		if not self.areas.count('conf'): return []
		Message(_("Scanning source document CONF area"),1)
		raw = ConfigLines(
		      file=self.filename, lines=self.get('conf'),
		      first_line=self.arearef[1]).get_raw_config()
		Debug("document raw config: %s"%raw, 1)
		return raw

##############################################################################

class ConfigMaster:
	"""
	ConfigMaster class - the configuration wizard
	
	This class is the configuration master. It knows how to handle
	the RAW and PARSED config format. It also performs the sanity
	checking for a given configuration.
	
	DATA:
	  self.raw         - Stores the config on the RAW format
	  self.parsed      - Stores the config on the PARSED format
	  self.defaults    - Stores the default values for all keys
	  self.off         - Stores the OFF values for all keys
	  self.multi       - List of keys which can have multiple values
	  self.numeric     - List of keys which value must be a number
	  self.incremental - List of keys which are incremental
	
        RAW FORMAT:
	  The RAW format is a list of lists, being each mother list item
	  a full configuration entry. Any entry is a 3 item list, on
	  the following format: [ TARGET, KEY, VALUE ]
	  Being a list, the order is preserved, so it's easy to use
	  different kinds of configs, as CONF area and command line,
	  respecting the precedence.
	  The special target 'all' is used when no specific target was
	  defined on the original config.
	
	PARSED FORMAT:
	  The PARSED format is a dictionary, with all the 'key : value'
	  found by reading the RAW config. The self.target contents
	  matters, so this dictionary only contains the target's
	  config. The configs of other targets are ignored.
	
	The CommandLine and ConfigLines classes have the get_raw_config()
	method which convert the configuration found to the RAW format.
	Just feed it to parse() and get a brand-new ready-to-use config
	dictionary. Example:
	
	    >>> raw = CommandLine().get_raw_config(['-n', '-H'])
	    >>> print raw
	    [['all', 'enum-title', ''], ['all', 'no-headers', '']]
	    >>> parsed = ConfigMaster(raw).parse()
	    >>> print parsed
	    {'enum-title': 1, 'headers': 0}
	"""
	def __init__(self, raw=[], target=''):
		self.raw          = raw
		self.target       = target
		self.parsed       = {}
		self.dft_options  = OPTIONS.copy()
		self.dft_flags    = FLAGS.copy()
		self.dft_actions  = ACTIONS.copy()
		self.dft_settings = SETTINGS.copy()
		self.defaults     = self._get_defaults()
		self.off          = self._get_off()
		self.incremental  = ['verbose']
		self.numeric      = ['toc-level','split']
		self.multi        = ['infile', 'preproc', 'postproc',
		                     'options', 'style']
	
	def _get_defaults(self):
		"Get the default values for all config/options/flags"
		empty = {}
		for kw in CONFIG_KEYWORDS: empty[kw] = ''
		empty.update(self.dft_options)
		empty.update(self.dft_flags)
		empty.update(self.dft_actions)
		empty.update(self.dft_settings)
		empty['realcmdline'] = ''  # internal use only
		empty['sourcefile']  = ''  # internal use only
		return empty
	
	def _get_off(self):
		"Turns OFF all the config/options/flags"
		off = {}
		for key in self.defaults.keys():
			kind = type(self.defaults[key])
			if kind == type(9):
				off[key] = 0
			elif kind == type(''):
				off[key] = ''
			elif kind == type([]):
				off[key] = []
			else:
				Error('ConfigMaster: %s: Unknown type'+key)
		return off
	
	def _check_target(self):
		"Checks if the target is already defined. If not, do it"
		if not self.target:
			self.target = self.find_value('target')
	
	def get_target_raw(self):
		"Returns the raw config for self.target or 'all'"
		ret = []
		self._check_target()
		for entry in self.raw:
			if entry[0] == self.target or entry[0] == 'all':
				ret.append(entry)
		return ret
	
	def add(self, key, val):
		"Adds the key:value pair to the config dictionary (if needed)"
		# %!options
		if key == 'options':
			ignoreme = self.dft_actions.keys() + ['target']
			ignoreme.remove('dump-config')
			ignoreme.remove('dump-source')
			raw_opts = CommandLine().get_raw_config(
			             val, ignore=ignoreme)
			for target, key, val in raw_opts:
				self.add(key, val)
			return
		# The no- prefix turns OFF this key
		if key[:3] == 'no-':
			key = key[3:]              # remove prefix
			val = self.off.get(key)    # turn key OFF
		# Is this key valid?
		if key not in self.defaults.keys():
			Debug('Bogus Config %s:%s'%(key,val),1)
			return
		# Is this value the default one?
		if val == self.defaults.get(key):
			# If default value, remove previous key:val
			if self.parsed.has_key(key):
				del self.parsed[key]
			# Nothing more to do
			return
		# Flags ON comes empty. we'll add the 1 value now
		if val == '' and (
		   key in self.dft_flags.keys() or
		   key in self.dft_actions.keys()):
			val = 1
		# Multi value or single?
		if key in self.multi:
			# First one? start new list
			if not self.parsed.has_key(key):
				self.parsed[key] = []
			self.parsed[key].append(val)
		# Incremental value? so let's add it
		elif key in self.incremental:
			self.parsed[key] = (self.parsed.get(key) or 0) + val
		else:
			self.parsed[key] = val
		fancykey = dotted_spaces("%12s"%key)
		Message(_("Added config %s : %s")%(fancykey,val),3)
	
	def get_outfile_name(self, config={}):
		"Dirname is the same for {in,out}file"
		infile, outfile = config['sourcefile'], config['outfile']
		if outfile and outfile not in (STDOUT, MODULEOUT) \
		   and not os.path.isabs(outfile):
			outfile = os.path.join(os.path.dirname(infile), outfile)
		if infile == STDIN    and not outfile: outfile = STDOUT
		if infile == MODULEIN and not outfile: outfile = MODULEOUT
		if not outfile and (infile and config.get('target')):
			basename = re.sub('\.(txt|t2t)$','',infile)
			outfile = "%s.%s"%(basename, config['target'])
		Debug(" infile: '%s'"%infile , 1)
		Debug("outfile: '%s'"%outfile, 1)
		return outfile
	
	def sanity(self, config, gui=0):
		"Basic config sanity checking"
		if not config: return {}
		target = config.get('target')
		# Some actions don't require target specification
		if not target:
			for action in NO_TARGET:
				if config.get(action):
					target = 'txt'
					break
		# On GUI, some checking are skipped
		if not gui:
			# We *need* a target
			if not target:
				Error(_('No target specified (try --help)')+\
				'\n\n'+\
				_('Maybe trying to convert an old v1.x file?'))
			# And of course, an infile also
			if not config.get('infile'):
				Error(_('Missing input file (try --help)'))
			# Is the target valid?
			if not TARGETS.count(target):
				Error(_("Invalid target '%s' (try --help)")%\
				     target)
		# Ensure all keys are present
		empty = self.defaults.copy() ; empty.update(config)
		config = empty.copy()
		# Check integers options
		for key in config.keys():
			if key in self.numeric:
				try: config[key] = int(config[key])
				except: Error(_('--%s value must be a number'
				                )%key)
		# Check split level value
		if config['split'] not in (0,1,2):
			Error(_('Option --split must be 0, 1 or 2'))
		# --toc-only is stronger than others
		if config['toc-only']:
			config['headers'] = 0
			config['toc']     = 0
			config['split']   = 0
			config['gui']     = 0
			config['outfile'] = config['outfile'] or STDOUT
		# Splitting is disable for now (future: HTML only, no STDOUT)
		config['split'] = 0
		# Restore target
		config['target'] = target
		# Set output file name
		config['outfile'] = self.get_outfile_name(config)
		# Checking suicide
		if config['sourcefile'] == config['outfile'] and \
		   config['outfile'] not in [STDOUT,MODULEOUT] and not gui:
			Error(_("Input and Output files are the same: %s")%(
			config['outfile']))
		return config
	
	def parse(self):
		"Returns the parsed config for the current target"
		raw = self.get_target_raw()
		for target, key, value in raw:
			self.add(key, value)
		Message(_("Added the following keys: %s")%string.join(
		         self.parsed.keys(),', '),2)
		return self.parsed.copy()
	
	def find_value(self, key='', target=''):
		"Scans ALL raw config to find the desired key"
		ret = []
		# Scan and save all values found
		for targ, k, val in self.raw:
			if k == key and (targ == target or targ == 'all'):
				ret.append(val)
		if not ret: return ''
		# If not multi value, return only the last found
		if key in self.multi: return ret
		else                : return ret[-1]

########################################################################

class ConfigLines:
	"""
	ConfigLines class - the config file data extractor
	
	This class reads and parse the config lines on the %!key:val
	format, converting it to RAW config. It deals with user
	config file (RC file), source document CONF area and
	%!includeconf directives.

	Call it passing a file name or feed the desired config lines.
	Then just call the get_raw_config() method and wait to
	receive the full config data on the RAW format. This method
	also follows the possible %!includeconf directives found on
	the config lines. Example:

	    raw = ConfigLines(file=".txt2tagsrc").get_raw_config()

	The parse_line() method is also useful to be used alone,
	to identify and tokenize a single config line. For example,
	to get the %!include command components, on the source
	document BODY:
	
	    target, key, value = ConfigLines().parse_line(body_line)
	"""
	def __init__(self, file='', lines=[], first_line=1):
		self.file = file or 'NOFILE'
		self.lines = lines
		self.first_line = first_line
	
	def load_lines(self):
		"Make sure we've loaded the file contents into buffer"
		if not self.lines and not self.file:
			Error("ConfigLines: No file or lines provided")
		if not self.lines:
			self.lines = self.read_config_file(self.file)
	
	def read_config_file(self, filename=''):
		"Read a Config File contents, aborting on invalid line"
		if not filename: return []
		errormsg = _("Invalid CONFIG line on %s")+"\n%03d:%s"
		lines = Readfile(filename, remove_linebreaks=1)
		# Sanity: try to find invalid config lines
		for i in xrange(len(lines)):
			line = string.rstrip(lines[i])
			if not line: continue  # empty
			if line[0] != '%': Error(errormsg%(filename,i+1,line))
		return lines
	
	def include_config_file(self, file=''):
		"Perform the %!includeconf action, returning RAW config"
		if not file: return []
		# Current dir relative to the current file (self.file)
		current_dir = os.path.dirname(self.file)
		file = os.path.join(current_dir, file)
		# Read and parse included config file contents
		lines = self.read_config_file(file)
		return ConfigLines(file=file, lines=lines).get_raw_config()
	
	def get_raw_config(self):
		"Scan buffer and extract all config as RAW (including includes)"
		ret = []
		self.load_lines()
		first = self.first_line
		for i in xrange(len(self.lines)):
			line = self.lines[i]
			Message(_("Processing line %03d: %s")%(first+i,line),2)
			target, key, val = self.parse_line(line)
			if not key: continue    # no config on this line
			if key == 'includeconf':
				err = _('A file cannot include itself (loop!)')
				if val == self.file:
					Error("%s: %%!includeconf: %s"%(
						err, self.file))
				more_raw = self.include_config_file(val)
				ret.extend(more_raw)
				Message(_("Finished Config file inclusion: %s"
				          )%(val),2)
			else:
				ret.append([target, key, val])
				Message(_("Added %s")%key,3)
		return ret
	
	def parse_line(self, line='', keyname='', target=''):
		"Detects %!key:val config lines and extract data from it"
		empty = ['', '', '']
		if not line: return empty
		no_target = ['target', 'includeconf']
		re_name   = keyname or '[a-z]+'
		re_target = target  or '[a-z]*'
		# XXX TODO <value>\S.+?  requires TWO chars, breaks %!include:a
		cfgregex  = re.compile("""
		  ^%%!\s*               # leading id with opt spaces
		  (?P<name>%s)\s*       # config name
		  (\((?P<target>%s)\))? # optional target spec inside ()
		  \s*:\s*               # key:value delimiter with opt spaces
		  (?P<value>\S.+?)      # config value
		  \s*$                  # rstrip() spaces and hit EOL
		  """%(re_name,re_target), re.I+re.VERBOSE)
		prepostregex = re.compile("""
		                        # ---[ PATTERN ]---
		  ^( "([^"]*)"          # "double quoted" or
		   | '([^']*)'          # 'single quoted' or
		   | ([^\s]+)           # single_word
		   )
		    \s+                 # separated by spaces
		
		                        # ---[ REPLACE ]---
		       ( "([^"]*)"      # "double quoted" or
		       | '([^']*)'      # 'single quoted' or
		       | (.*)           # anything
		           )
		            \s*$
		  """, re.VERBOSE)
		guicolors = re.compile("^([^\s]+\s+){3}[^\s]+") # 4 tokens
		match = cfgregex.match(line)
		if not match: return empty
		
		name   = string.lower(match.group('name') or '')
		target = string.lower(match.group('target') or 'all')
		value  = match.group('value')
		
		# NO target keywords: force all targets
		if name in no_target: target = 'all'
		
		# Special config for GUI colors
		if name == 'guicolors':
			valmatch = guicolors.search(value)
			if not valmatch: return empty
			value = re.split('\s+', value)
		
		# Special config with two quoted values (%!preproc: "foo" 'bar')
		if name == 'preproc' or name == 'postproc':
			valmatch = prepostregex.search(value)
			if not valmatch: return empty
			getval = valmatch.group
			patt   = getval(2) or getval(3) or getval(4) or ''
			repl   = getval(6) or getval(7) or getval(8) or ''
			value  = (patt, repl)
		return [target, name, value]

##############################################################################

class MaskMaster:
	"(Un)Protect important structures from escaping and formatting"
	def __init__(self):
		self.linkmask  = 'vvvLINKvvv'
		self.monomask  = 'vvvMONOvvv'
		self.macromask = 'vvvMACROvvv'
		self.rawmask   = 'vvvRAWvvv'
		self.tocmask   = 'vvvTOCvvv'
		self.macroman  = MacroMaster()
		self.reset()
	
	def reset(self):
		self.linkbank = []
		self.monobank = []
		self.macrobank = []
		self.rawbank = []
	
	def mask(self, line=''):
		global AUTOTOC
		
		# Protect raw text
		while regex['raw'].search(line):
			txt = regex['raw'].search(line).group(1)
			txt = doEscape(TARGET,txt)
			self.rawbank.append(txt)
			line = regex['raw'].sub(self.rawmask,line,1)
		
		# Protect pre-formatted font text
		while regex['fontMono'].search(line):
			txt = regex['fontMono'].search(line).group(1)
			txt = doEscape(TARGET,txt)
			self.monobank.append(txt)
			line = regex['fontMono'].sub(self.monomask,line,1)
		
		# Protect macros
		while regex['macros'].search(line):
			txt = regex['macros'].search(line).group()
			self.macrobank.append(txt)
			line = regex['macros'].sub(self.macromask,line,1)
		
		# Protect TOC location
		while regex['toc'].search(line):
			line = regex['toc'].sub(self.tocmask,line)
			AUTOTOC = 0
		
		# Protect URLs and emails
		while regex['linkmark'].search(line) or \
		      regex['link'    ].search(line):
			
			# Try to match plain or named links
			match_link  = regex['link'].search(line)
			match_named = regex['linkmark'].search(line)
			
			# Define the current match
			if match_link and match_named:
				# Both types found, which is the first?
				m = match_link
				if match_named.start() < match_link.start():
					m = match_named
			else:
				# Just one type found, we're fine
				m = match_link or match_named
			
			# Extract link data and apply mask
			if m == match_link:              # plain link
				link = m.group()
				label = ''
				link_re = regex['link']
			else:                            # named link
				link = m.group('link')
				label = string.rstrip(m.group('label'))
				link_re = regex['linkmark']
			line = link_re.sub(self.linkmask,line,1)
			
			# Save link data to the link bank
			self.linkbank.append((label, link))
		return line
	
	def undo(self, line):
		
		# url & email
		for label,url in self.linkbank:
			link = get_tagged_link(label, url)
			line = string.replace(line, self.linkmask, link, 1)
		
		# Expand macros
		for macro in self.macrobank:
			macro = self.macroman.expand(macro)
			line = string.replace(line, self.macromask, macro, 1)
		
		# Expand verb
		for mono in self.monobank:
			open,close = TAGS['fontMonoOpen'],TAGS['fontMonoClose']
			tagged = open+mono+close
			line = string.replace(line, self.monomask, tagged, 1)
		
		# Expand raw
		for raw in self.rawbank:
			line = string.replace(line, self.rawmask, raw, 1)
		
		return line


##############################################################################


class TitleMaster:
	"Title things"
	def __init__(self):
		self.count = ['',0,0,0,0,0]
		self.toc   = []
		self.level = 0
		self.kind  = ''
		self.txt   = ''
		self.label = ''
		self.tag   = ''
		self.tag_hold = []
		self.last_level = 0
		self.count_id = ''
		self.user_labels = {}
		self.anchor_count = 0
		self.anchor_prefix = 'toc'
	
	def _open_close_blocks(self):
		"Open new title blocks, closing the previous (if any)"
		if not rules['titleblocks']: return
		tag = ''
		last = self.last_level
		curr = self.level
		
		# Same level, just close the previous
		if curr == last:
			tag = TAGS.get('title%dClose'%last)
			if tag: self.tag_hold.append(tag)
		
		# Section -> subsection, more depth
		while curr > last:
			last = last + 1
			
			# Open the new block of subsections
			tag = TAGS.get('blockTitle%dOpen'%last)
			if tag: self.tag_hold.append(tag)
			
			# Jump from title1 to title3 or more
			# Fill the gap with an empty section
			if curr - last > 0:
				tag = TAGS.get('title%dOpen'%last)
				tag = regex['x'].sub('', tag)      # del \a
				if tag: self.tag_hold.append(tag)
		
		# Section <- subsection, less depth
		while curr < last:
			# Close the current opened subsection
			tag = TAGS.get('title%dClose'%last)
			if tag: self.tag_hold.append(tag)
			
			# Close the current opened block of subsections
			tag = TAGS.get('blockTitle%dClose'%last)
			if tag: self.tag_hold.append(tag)
			
			last = last - 1
			
			# Close the previous section of the same level
			# The subsections were under it
			if curr == last:
				tag = TAGS.get('title%dClose'%last)
				if tag: self.tag_hold.append(tag)
	
	def add(self, line):
		"Parses a new title line."
		if not line: return
		self._set_prop(line)
		self._open_close_blocks()
		self._set_count_id()
		self._set_label()
		self._save_toc_info()
	
	def close_all(self):
		"Closes all opened title blocks"
		ret = []
		ret.extend(self.tag_hold)
		while self.level:
			tag = TAGS.get('title%dClose'%self.level)
			if tag: ret.append(tag)
			tag = TAGS.get('blockTitle%dClose'%self.level)
			if tag: ret.append(tag)
			self.level = self.level - 1
		return ret
	
	def _save_toc_info(self):
		"Save TOC info, used by self.dump_marked_toc()"
		self.toc.append((self.level, self.count_id,
		                 self.txt  , self.label   ))
	
	def _set_prop(self, line=''):
		"Extract info from original line and set data holders."
		# Detect title type (numbered or not)
		id = string.lstrip(line)[0]
		if   id == '=': kind = 'title'
		elif id == '+': kind = 'numtitle'
		else: Error("Unknown Title ID '%s'"%id)
		# Extract line info
		match = regex[kind].search(line)
		level = len(match.group('id'))
		txt   = string.strip(match.group('txt'))
		label = match.group('label')
		# Parse info & save
		if CONF['enum-title']: kind = 'numtitle'  # force
		if rules['titleblocks']:
			self.tag = TAGS.get('%s%dOpen'%(kind,level)) or \
			           TAGS.get('title%dOpen'%level)
		else:
			self.tag = TAGS.get(kind+`level`) or \
			           TAGS.get('title'+`level`)
		self.last_level = self.level
		self.kind  = kind
		self.level = level
		self.txt   = txt
		self.label = label
	
	def _set_count_id(self):
		"Compose and save the title count identifier (if needed)."
		count_id = ''
		if self.kind == 'numtitle' and not rules['autonumbertitle']:
			# Manually increase title count
			self.count[self.level] = self.count[self.level] +1
			# Reset sublevels count (if any)
			max_levels = len(self.count)
			if self.level < max_levels-1:
				for i in xrange(self.level+1, max_levels):
					self.count[i] = 0
			# Compose count id from hierarchy
			for i in xrange(self.level):
				count_id= "%s%d."%(count_id, self.count[i+1])
		self.count_id = count_id
	
	def _set_label(self):
		"Compose and save title label, used by anchors."
		# Remove invalid chars from label set by user
		self.label = re.sub('[^A-Za-z0-9_-]', '', self.label or '')
		# Generate name as 15 first :alnum: chars
		#TODO how to translate safely accented chars to plain?
		#self.label = re.sub('[^A-Za-z0-9]', '', self.txt)[:15]
		# 'tocN' label - sequential count, ignoring 'toc-level'
		#self.label = self.anchor_prefix + str(len(self.toc)+1)
	
	def _get_tagged_anchor(self):
		"Return anchor if user defined a label, or TOC is on."
		ret = ''
		label = self.label
		if CONF['toc'] and self.level <= CONF['toc-level']:
			# This count is needed bcos self.toc stores all
			# titles, regardless of the 'toc-level' setting,
			# so we can't use self.toc length to number anchors
			self.anchor_count = self.anchor_count + 1
			# Autonumber label (if needed)
			label = label or '%s%s'%(
			        self.anchor_prefix, self.anchor_count)
		if label and TAGS['anchor']:
			ret = regex['x'].sub(label,TAGS['anchor'])
		return ret
	
	def _get_full_title_text(self):
		"Returns the full title contents, already escaped."
		ret = self.txt
		# Insert count_id (if any) before text
		if self.count_id:
			ret = '%s %s'%(self.count_id, ret)
		# Escape specials
		ret = doEscape(TARGET, ret)
		# Same targets needs final escapes on title lines
		# It's here because there is a 'continue' after title
		if rules['finalescapetitle']:
			ret = doFinalEscape(TARGET, ret)
		return ret
	
	def get(self):
		"Returns the tagged title as a list."
		ret = []
		
		# Maybe some anchoring before?
		anchor = self._get_tagged_anchor()
		self.tag = regex['_anchor'].sub(anchor, self.tag)
		
		### Compose & escape title text (TOC uses unescaped)
		full_title = self._get_full_title_text()
		
		# Close previous section area
		ret.extend(self.tag_hold)
		self.tag_hold = []
		 
		# Finish title, adding "underline" on TXT target
		tagged = regex['x'].sub(full_title, self.tag)
		if TARGET == 'txt':
			ret.append('') # blank line before
			ret.append(tagged)
			ret.append(regex['x'].sub('='*len(full_title),self.tag))
			ret.append('') # blank line after
		else:
			ret.append(tagged)
		return ret
	
	def dump_marked_toc(self, max_level=99):
		"Dumps all toc itens as a valid t2t markup list"
		#TODO maybe use quote+linebreaks instead lists
		ret = []
		toc_count = 1
		for level, count_id, txt, label in self.toc:
			if level > max_level: continue   # ignore
			indent = '  '*level
			id_txt = string.lstrip('%s %s'%(count_id, txt))
			label = label or self.anchor_prefix+`toc_count`
			toc_count = toc_count + 1
			# TOC will have links
			if TAGS['anchor']:
				# TOC is more readable with master topics
				# not linked at number. This is a stoled
				# idea from Windows .CHM help files
				if CONF['enum-title'] and level == 1:
					tocitem = '%s+ [""%s"" #%s]'%(
					          indent, txt, label)
				else:
					tocitem = '%s- [""%s"" #%s]'%(
					          indent, id_txt, label)
			# No links on TOC, just text
			else:
				# man don't reformat TOC lines, cool!
				if TARGET == 'txt' or TARGET == 'man':
					tocitem = '%s""%s""' %(
					          indent, id_txt)
				else:
					tocitem = '%s- ""%s""'%(
					          indent, id_txt)
			ret.append(tocitem)
		return ret


##############################################################################

#TODO check all this table mess
# Trata linhas TABLE, com as prop do parse_row
# O metodo table() do BLOCK xunxa e troca as celulas pelas parseadas
class TableMaster:
	def __init__(self, line=''):
		self.rows      = []
		self.border    = 0
		self.align     = 'Left'
		self.cellalign = []
		self.cellspan  = []
		if line:
			prop = self.parse_row(line)
			self.border    = prop['border']
			self.align     = prop['align']
			self.cellalign = prop['cellalign']
			self.cellspan  = prop['cellspan']
	
	def _get_open_tag(self):
		topen     = TAGS['tableOpen']
		tborder   = TAGS['tableBorder']
		talign    = TAGS['tableAlign'+self.align]
		calignsep = TAGS['tableColAlignSep']
		calign    = ''
		
		# The first line defines if table has border or not
		if not self.border: tborder = ''
		# Set the columns alignment
		if rules['tablecellaligntype'] == 'column':
			calign = map(lambda x: TAGS['tableColAlign%s'%x],
			             self.cellalign)
			calign = string.join(calign, calignsep)
		# Align full table, set border and Column align (if any)
		topen = regex['_tableAlign'   ].sub(talign , topen)
		topen = regex['_tableBorder'  ].sub(tborder, topen)
		topen = regex['_tableColAlign'].sub(calign , topen)
		# Tex table spec, border or not: {|l|c|r|} , {lcr}
		if calignsep and not self.border:
			# Remove cell align separator
			topen = string.replace(topen, calignsep, '')
		return topen
	
	def _get_cell_align(self, cells):
		ret = []
		for cell in cells:
			align = 'Left'
			if string.strip(cell):
				if cell[0] == ' ' and cell[-1] == ' ':
					align = 'Center'
				elif cell[0] == ' ':
					align = 'Right'
			ret.append(align)
		return ret
	
	def _get_cell_span(self, cells):
		ret = []
		for cell in cells:
			span = 0
			m = re.search('\a(\|+)$', cell)
			if m: span = len(m.group(1))+1
			ret.append(span)
		return ret
	
	def _tag_cells(self, rowdata):
		row = []
		cells  = rowdata['cells']
		open   = TAGS['tableCellOpen']
		close  = TAGS['tableCellClose']
		sep    = TAGS['tableCellSep']
		calign = map(lambda x: TAGS['tableCellAlign'+x],
		             rowdata['cellalign'])
		# Populate the span tag
		cspan = []
		for i in rowdata['cellspan']:
			if i > 0:
				cspan.append(regex['x'].sub(
				str(i), TAGS['tableCellColSpan']))
			else:
				cspan.append('')
		
		# Maybe is it a title row?
		if rowdata['title']:
			open  = TAGS['tableTitleCellOpen']  or open
			close = TAGS['tableTitleCellClose'] or close
			sep   = TAGS['tableTitleCellSep']   or sep
		
		# Should we break the line on *each* table cell?
		if rules['breaktablecell']: close = close+'\n'
		
		# Cells pre processing
		if rules['tablecellstrip']:
			cells = map(lambda x: string.strip(x), cells)
		if rowdata['title'] and rules['tabletitlerowinbold']:
			cells = map(lambda x: enclose_me('fontBold',x), cells)
		
		# Add cell BEGIN/END tags
		for cell in cells:
			copen = open
			# Make sure we will pop from some filled lists
			# Fixes empty line bug '| |'
			this_align = this_span = ''
			if calign: this_align = calign.pop(0)
			if cspan : this_span = cspan.pop(0)
			# Insert cell align into open tag (if cell is alignable)
			if rules['tablecellaligntype'] == 'cell':
				copen = regex['_tableCellAlign'].sub(
					this_align, copen)
			if rules['tablecellspannable']:
				copen = regex['_tableCellColSpan'].sub(
					this_span, copen)
			row.append(copen + cell + close)
		
		# Maybe there are cell separators?
		return string.join(row, sep)
	
	def add_row(self, cells):
		self.rows.append(cells)
	
	def parse_row(self, line):
		# Default table properties
		ret = {'border':0,'title':0,'align':'Left',
		       'cells':[],'cellalign':[], 'cellspan':[]}
		# Detect table align (and remove spaces mark)
		if line[0] == ' ': ret['align'] = 'Center'
		line = string.lstrip(line)
		# Detect title mark
		if line[1] == '|': ret['title'] = 1
		# Detect border mark and normalize the EOL
		m = re.search(' (\|+) *$', line)
		if m: line = line+' ' ; ret['border'] = 1
		else: line = line+' | '
		# Delete table mark
		line = regex['table'].sub('', line)
		# Detect colspan  | foo | bar baz |||
		line = re.sub(' (\|+)\| ', '\a\\1 | ', line)
		# Split cells (the last is fake)
		ret['cells'] = string.split(line, ' | ')[:-1]
		# Find cells span
		ret['cellspan'] = self._get_cell_span(ret['cells'])
		# Remove span ID
		ret['cells'] = map(lambda x:re.sub('\a\|+$','',x),ret['cells'])
		# Find cells align
		ret['cellalign'] = self._get_cell_align(ret['cells'])
		# Hooray!
		Debug('Table Prop: %s' % ret, 7)
		return ret
	
	def dump(self):
		open  = self._get_open_tag()
		rows  = self.rows
		close = TAGS['tableClose']
		
		rowopen     = TAGS['tableRowOpen']
		rowclose    = TAGS['tableRowClose']
		rowsep      = TAGS['tableRowSep']
		titrowopen  = TAGS['tableTitleRowOpen']  or rowopen
		titrowclose = TAGS['tableTitleRowClose'] or rowclose
		
		if rules['breaktablelineopen']:
			rowopen = rowopen + '\n'
			titrowopen = titrowopen + '\n'
		
		# Tex gotchas
		if TARGET == 'tex':
			if not self.border:
				rowopen = titrowopen = ''
			else:
				close = rowopen + close
		
		# Now we tag all the table cells on each row
		#tagged_cells = map(lambda x: self._tag_cells(x), rows) #!py15
		tagged_cells = []
		for cell in rows: tagged_cells.append(self._tag_cells(cell))
		
		# Add row separator tags between lines
		tagged_rows = []
		if rowsep:
			#!py15
			#tagged_rows = map(lambda x:x+rowsep, tagged_cells)
			for cell in tagged_cells:
				tagged_rows.append(cell+rowsep)
			# Remove last rowsep, because the table is over
			tagged_rows[-1] = string.replace(
			                  tagged_rows[-1], rowsep, '')
		# Add row BEGIN/END tags for each line
		else:
			for rowdata in rows:
				if rowdata['title']:
					o,c = titrowopen, titrowclose
				else:
					o,c = rowopen, rowclose
				row = tagged_cells.pop(0)
				tagged_rows.append(o + row + c)
		
		fulltable = [open] + tagged_rows + [close]
		
		if rules['blankendtable']: fulltable.append('')
		return fulltable


##############################################################################


class BlockMaster:
	"TIP: use blockin/out to add/del holders"
	def __init__(self):
		self.BLK = []
		self.HLD = []
		self.PRP = []
		self.depth = 0
		self.last = ''
		self.tableparser = None
		self.contains = {
		  'para'    :['comment','raw'],
		  'verb'    :[],
		  'table'   :['comment'],
		  'raw'     :[],
		  'tagged'  :[],
		  'comment' :[],
		  'quote'   :['quote','comment','raw'],
		  'list'    :['list' ,'numlist' ,'deflist','para','verb',
		              'comment', 'raw'],
		  'numlist' :['list' ,'numlist' ,'deflist','para','verb',
		              'comment', 'raw'],
		  'deflist' :['list' ,'numlist' ,'deflist','para','verb',
		              'comment', 'raw']
		}
		self.allblocks = self.contains.keys()
		# If one found inside another, ignore the marks
		self.exclusive = ['comment','verb','raw']
	
	def block(self):
		if not self.BLK: return ''
		return self.BLK[-1]
	
	def isblock(self, name=''):
		return self.block() == name
	
	def prop(self, key):
		if not self.PRP: return ''
		return self.PRP[-1].get(key) or ''
	
	def propset(self, key, val):
		self.PRP[-1][key] = val
		#Debug('BLOCK prop ++: %s->%s'%(key,repr(val)), 1)
		#Debug('BLOCK props: %s'%(repr(self.PRP)), 1)
	
	def hold(self):
		if not self.HLD: return []
		return self.HLD[-1]
	
	def holdadd(self, line):
		if self.block()[-4:] == 'list': line = [line]
		self.HLD[-1].append(line)
		Debug('HOLD add: %s'%repr(line), 4)
		Debug('FULL HOLD: %s'%self.HLD, 4)
	
	def holdaddsub(self, line):
		self.HLD[-1][-1].append(line)
		Debug('HOLD addsub: %s'%repr(line), 4)
		Debug('FULL HOLD: %s'%self.HLD, 4)
	
	def holdextend(self, lines):
		if self.block()[-4:] == 'list': lines = [lines]
		self.HLD[-1].extend(lines)
		Debug('HOLD extend: %s'%repr(lines), 4)
		Debug('FULL HOLD: %s'%self.HLD, 4)
	
	def blockin(self, block):
		ret = []
		if block not in self.allblocks:
			Error("Invalid block '%s'"%block)
		# First, let's close other possible open blocks
		while self.block() and block not in self.contains[self.block()]:
			ret.extend(self.blockout())
		# Now we can gladly add this new one
		self.BLK.append(block)
		self.HLD.append([])
		self.PRP.append({})
		if block == 'table': self.tableparser = TableMaster()
		# Deeper and deeper
		self.depth = len(self.BLK)
		Debug('block ++ (%s): %s' % (block,self.BLK), 3)
		return ret
	
	def blockout(self):
		if not self.BLK: Error('No block to pop')
		self.last = self.BLK.pop()
		result = getattr(self, self.last)()
		parsed = self.HLD.pop()
		self.PRP.pop()
		self.depth = len(self.BLK)
		if self.last == 'table': del self.tableparser
		# Inserting a nested block into mother
		if self.block():
			if self.last != 'comment': # ignore comment blocks
				if self.block()[-4:] == 'list':
					self.HLD[-1][-1].append(result)
				else:
					self.HLD[-1].append(result)
			# Reset now. Mother block will have it all
			result = []
		Debug('block -- (%s): %s' % (self.last,self.BLK), 3)
		Debug('RELEASED (%s): %s' % (self.last,parsed), 3)
		if result: Debug('BLOCK: %s'%result, 6)
		return result
	
	def _last_escapes(self, line):
		return doFinalEscape(TARGET, line)
	
	def _get_escaped_hold(self):
		ret = []
		for line in self.hold():
			linetype = type(line)
			if linetype == type(''):
				ret.append(self._last_escapes(line))
			elif linetype == type([]):
				ret.extend(line)
			else:
				Error("BlockMaster: Unknown HOLD item type:"
				      " %s"%linetype)
		return ret
	
	def _remove_twoblanks(self, lastitem):
		if len(lastitem) > 1 and lastitem[-2:] == ['','']:
			return lastitem[:-2]
		return lastitem
	
	def tagged(self):
		return self.hold()
	
	def comment(self):
		return ''
	
	def raw(self):
		lines = self.hold()
		return map(lambda x: doEscape(TARGET, x), lines)
	
	def para(self):
		result = []
		open  = TAGS['paragraphOpen']
		close = TAGS['paragraphClose']
		lines = self._get_escaped_hold()
		# Open (or not) paragraph
		if not open+close and self.last == 'para':
			pass # avoids multiple blank lines
		else:
			result.append(open)
		# Pagemaker likes a paragraph as a single long line
		if rules['onelinepara']:
			result.append(string.join(lines,' '))
		# Others are normal :)
		else:
			result.extend(lines)
		result.append(close)
		
		# Very very very very very very very very very UGLY fix
		# Needed because <center> can't appear inside <p>
		try:
			if len(lines) == 1 and \
			   TARGET in ('html', 'xhtml') and \
			   re.match('^\s*<center>.*</center>\s*$', lines[0]):
				result = [lines[0]]
		except: pass
		
		return result
	
	def verb(self):
		"Verbatim lines are not masked, so there's no need to unmask"
		result = []
		result.append(TAGS['blockVerbOpen'])
		for line in self.hold():
			if self.prop('mapped') == 'table':
				line = MacroMaster().expand(line)
			if not rules['verbblocknotescaped']:
				line = doEscape(TARGET,line)
			if rules['indentverbblock']:
				line = '  '+line
			if rules['verbblockfinalescape']:
				line = doFinalEscape(TARGET, line)
			result.append(line)
		#TODO maybe use if not TAGS['blockVerbClose']
		if TARGET != 'pm6':
			result.append(TAGS['blockVerbClose'])
		return result
	
	def table(self):
		# Rewrite all table cells by the unmasked and escaped data
		lines = self._get_escaped_hold()
		for i in xrange(len(lines)):
			cells = string.split(lines[i], SEPARATOR)
			self.tableparser.rows[i]['cells'] = cells
		
		return self.tableparser.dump()
	
	def quote(self):
		result = []
		myre   = regex['quote']
		open   = TAGS['blockQuoteOpen']            # block based
		close  = TAGS['blockQuoteClose']
		qline  = TAGS['blockQuoteLine']            # line based
		indent = tagindent = '\t'*self.depth
		if rules['tagnotindentable']: tagindent = ''
		if not rules['keepquoteindent']: indent = ''
		
		if open: result.append(tagindent+open)     # open block
		for item in self.hold():
			if type(item) == type([]):
				result.extend(item)        # subquotes
			else:
				item = myre.sub('', item)  # del TABs
				if rules['barinsidequote']:
					item = get_tagged_bar(item)
				item = self._last_escapes(item)
				item = qline*self.depth + item
				result.append(indent+item) # quote line
		if close: result.append(tagindent+close)   # close block
		return result
	
	def deflist(self): return self.list('deflist')
	def numlist(self): return self.list('numlist')
	def list(self, name='list'):
		result    = []
		items     = self.hold()
		indent    = self.prop('indent')
		tagindent = indent
		listopen  = TAGS.get(name+'Open')
		listclose = TAGS.get(name+'Close')
		listline  = TAGS.get(name+'ItemLine')
		itemcount = 0
		if rules['tagnotindentable']: tagindent = ''
		if not rules['keeplistindent']: indent = ''
		
		if name == 'deflist':
			itemopen  = TAGS[name+'Item1Open']
			itemclose = TAGS[name+'Item2Close']
			itemsep   = TAGS[name+'Item1Close']+\
			            TAGS[name+'Item2Open']
		else:
			itemopen  = TAGS[name+'ItemOpen']
			itemclose = TAGS[name+'ItemClose']
			itemsep   = ''
		
		# ItemLine: number of leading chars identifies list depth
		if listline:
			itemopen  = listline*self.depth
			# Dirty fix for mgp
			if name == 'numlist': itemopen = itemopen + '\a. '
		
		# Remove two-blanks from list ending mark, to avoid <p>
		items[-1] = self._remove_twoblanks(items[-1])
		
		# Open list (not nestable lists are only opened at mother)
		if listopen and not \
		   (rules['listnotnested'] and BLOCK.depth != 1):
			result.append(tagindent+listopen)
		
		# Tag each list item (multiline items)
		itemopenorig = itemopen
		for item in items:
			
			# Add "manual" item count for noautonum targets
			itemcount = itemcount + 1
			if name == 'numlist' and not rules['autonumberlist']:
				n = str(itemcount)
				itemopen = regex['x'].sub(n, itemopenorig)
				del n
			
			item[0] = self._last_escapes(item[0])
			if name == 'deflist':
				z,term,rest = string.split(item[0],SEPARATOR,2)
				item[0] = rest
				if not item[0]: del item[0]      # to avoid <p>
				result.append(tagindent+itemopen+term+itemsep)
			else:
				fullitem = tagindent+itemopen
				result.append(string.replace(
				              item[0], SEPARATOR, fullitem))
				del item[0]
			
			# Process next lines for this item (if any)
			for line in item:
				if type(line) == type([]): # sublist inside
					result.extend(line)
				else:
					line = self._last_escapes(line)
					# Blank lines turns to <p>
					if not line and rules['parainsidelist']:
						line = string.rstrip(indent   +\
						         TAGS['paragraphOpen']+\
						         TAGS['paragraphClose'])
					if not rules['keeplistindent']:
						line = string.lstrip(line)
					result.append(line)
			
			# Close item (if needed)
			if itemclose: result.append(tagindent+itemclose)
		
		# Close list (not nestable lists are only closed at mother)
		if listclose and not \
		   (rules['listnotnested'] and BLOCK.depth != 1):
			result.append(tagindent+listclose)
		
		if rules['blankendmotherlist'] and BLOCK.depth == 1:
			result.append('')
		
		return result


##############################################################################


class MacroMaster:
	def __init__(self, config={}):
		self.name     = ''
		self.config   = config or CONF
		self.infile   = self.config['sourcefile']
		self.outfile  = self.config['outfile']
		self.currdate = time.localtime(time.time())
		self.rgx      = regex.get('macros') or getRegexes()['macros']
		self.fileinfo = { 'infile': None, 'outfile': None }
		self.dft_fmt  = MACROS
	
	def walk_file_format(self, fmt):
		"Walks the %%{in/out}file format string, expanding the % flags"
		i = 0; ret = ''                                 # counter/hold
		while i < len(fmt):                             # char by char
			c = fmt[i]; i = i + 1
			if c == '%':                            # hot char!
				if i == len(fmt):               # % at the end
					ret = ret + c
					break
				c = fmt[i]; i = i + 1           # read next
				ret = ret + self.expand_file_flag(c)
			else:
				ret = ret +c                    # common char
		return ret
	
	def expand_file_flag(self, flag):
		"%f: filename          %F: filename (w/o extension)"
		"%d: dirname           %D: dirname (only parent dir)"
		"%p: file path         %e: extension"
		info = self.fileinfo[self.name]           # get dict
		if   flag == '%': x = '%'                 # %% -> %
		elif flag == 'f': x = info['name']
		elif flag == 'F': x = re.sub('\.[^.]*$','',info['name'])
		elif flag == 'd': x = info['dir']
		elif flag == 'D': x = os.path.split(info['dir'])[-1]
		elif flag == 'p': x = info['path']
		elif flag == 'e': x = re.search('.(\.([^.]+))?$',info['name']
		                                ).group(2) or ''
		#TODO simpler way for %e ?
		else            : x = '%'+flag            # false alarm
		return x
	
	def set_file_info(self, macroname):
		if self.fileinfo.get(macroname): return   # already done
		file = getattr(self, self.name)           # self.infile
		if file == STDOUT or file == MODULEOUT:
			dir = ''; path = name = file
		else:
			path = os.path.abspath(file)
			dir  = os.path.dirname(path)
			name = os.path.basename(path)
		self.fileinfo[macroname] = {'path':path,'dir':dir,'name':name}
	
	def expand(self, line=''):
		"Expand all macros found on the line"
		while self.rgx.search(line):
			m = self.rgx.search(line)
			name = self.name = string.lower(m.group('name'))
			fmt = m.group('fmt') or self.dft_fmt.get(name)
			if name == 'date':
				txt = time.strftime(fmt,self.currdate)
			elif name == 'mtime':
				if self.infile in (STDIN, MODULEIN):
					fdate = self.currdate
				else:
					mtime = os.path.getmtime(self.infile)
					fdate = time.localtime(mtime)
				txt = time.strftime(fmt,fdate)
			elif name == 'infile' or name == 'outfile':
				self.set_file_info(name)
				txt = self.walk_file_format(fmt)
			else:
				Error("Unknown macro name '%s'"%name)
			line = self.rgx.sub(txt,line,1)
		return line


##############################################################################


def dumpConfig(source_raw, parsed_config):
	onoff = {1:_('ON'), 0:_('OFF')}
	data = [
	  (_('RC file')        , RC_RAW     ),
	  (_('source document'), source_raw ),
	  (_('command line')   , CMDLINE_RAW)
	]
	# First show all RAW data found
	for label, cfg in data:
		print _('RAW config for %s')%label
		for target,key,val in cfg:
			target = '(%s)'%target
			key    = dotted_spaces("%-14s"%key)
			val    = val or _('ON')
			print '  %-8s %s: %s'%(target,key,val)
		print
	# Then the parsed results of all of them
	print _('Full PARSED config')
	keys = parsed_config.keys() ; keys.sort()  # sorted
	for key in keys:
		val = parsed_config[key]
		# Filters are the last
		if key == 'preproc' or key == 'postproc':
			continue
		# Flag beautifier
		if key in FLAGS.keys() or key in ACTIONS.keys():
			val = onoff.get(val) or val
		# List beautifier
		if type(val) == type([]):
			if key == 'options': sep = ' '
			else               : sep = ', '
			val = string.join(val, sep)
		print "%25s: %s"%(dotted_spaces("%-14s"%key),val)
	print
	print _('Active filters')
	for filter in ['preproc','postproc']:
		for rule in parsed_config.get(filter) or []:
			print "%25s: %s  ->  %s"%(
			   dotted_spaces("%-14s"%filter),rule[0],rule[1])


def get_file_body(file):
	"Returns all the document BODY lines"
	return process_source_file(file, noconf=1)[1][2]


def finish_him(outlist, config):
	"Writing output to screen or file"
	outfile = config['outfile']
	outlist = unmaskEscapeChar(outlist)
	outlist = expandLineBreaks(outlist)
	
	# Apply PostProc filters
	if config['postproc']:
		filters = compile_filters(config['postproc'],
		                        _('Invalid PostProc filter regex'))
		postoutlist = []
		errmsg = _('Invalid PostProc filter replacement')
		for line in outlist:
			for rgx,repl in filters:
				try: line = rgx.sub(repl, line)
				except: Error("%s: '%s'"%(errmsg, repl))
			postoutlist.append(line)
		outlist = postoutlist[:]
	
	if outfile == MODULEOUT:
		return outlist
	elif outfile == STDOUT:
		if GUI:
			return outlist, config
		else:
			for line in outlist: print line
	else:
		Savefile(outfile, addLineBreaks(outlist))
		if not GUI and not QUIET:
			print _('%s wrote %s')%(my_name,outfile)
	
	if config['split']:
		if not QUIET: print "--- html..."
		sgml2html = 'sgml2html -s %s -l %s %s'%(
		            config['split'],config['lang'] or lang,outfile)
		if not QUIET: print "Running system command:", sgml2html
		os.system(sgml2html)


def toc_inside_body(body, toc, config):
	ret = []
	if AUTOTOC: return body                     # nothing to expand
	toc_mark = MaskMaster().tocmask
	# Expand toc mark with TOC contents
	for line in body:
		if string.count(line, toc_mark):    # toc mark found
			if config['toc']:
				ret.extend(toc)     # include if --toc
			else:
				pass                # or remove %%toc line
		else:
			ret.append(line)            # common line
	return ret

def toc_tagger(toc, config):
	"Convert t2t-marked TOC (it is a list) to target-tagged TOC"
	ret = []
	# Tag if TOC-only TOC "by hand" (target don't have a TOC tag)
	if config['toc-only'] or (config['toc'] and not TAGS['TOC']):
		fakeconf = config.copy()
		fakeconf['headers']    = 0
		fakeconf['toc-only']   = 0
		fakeconf['mask-email'] = 0
		fakeconf['preproc']    = []
		fakeconf['postproc']   = []
		fakeconf['css-sugar']  = 0
		ret,foo = convert(toc, fakeconf)
		set_global_config(config)   # restore config
	# Target TOC is a tag
	elif config['toc'] and TAGS['TOC']:
		ret = [TAGS['TOC']]
	return ret

def toc_formatter(toc, config):
	"Formats TOC for automatic placement between headers and body"
	if config['toc-only']: return toc              # no formatting needed
	if not config['toc'] : return []               # TOC disabled
	ret = toc
	# TOC open/close tags (if any)
	if TAGS['tocOpen' ]: ret.insert(0, TAGS['tocOpen'])
	if TAGS['tocClose']: ret.append(TAGS['tocClose'])
	# Autotoc specific formatting
	if AUTOTOC:
		if rules['autotocwithbars']:           # TOC between bars
			para = TAGS['paragraphOpen']+TAGS['paragraphClose']
			bar  = regex['x'].sub('-'*72,TAGS['bar1'])
			tocbar = [para, bar, para]
			ret = tocbar + ret + tocbar
		if rules['blankendautotoc']:           # blank line after TOC
			ret.append('')
		if rules['autotocnewpagebefore']:      # page break before TOC
			ret.insert(0,TAGS['pageBreak'])
		if rules['autotocnewpageafter']:       # page break after TOC
			ret.append(TAGS['pageBreak'])
	return ret


def doHeader(headers, config):
	if not config['headers']: return []
	if not headers: headers = ['','','']
	target = config['target']
	if not HEADER_TEMPLATE.has_key(target):
		Error("doheader: Unknow target '%s'"%target)
	
	if target in ('html','xhtml') and config.get('css-sugar'):
		template = string.split(HEADER_TEMPLATE[target+'css'], '\n')
	else:
		template = string.split(HEADER_TEMPLATE[target], '\n')
	
	head_data = {'STYLE':[], 'ENCODING':''}
	for key in head_data.keys():
		val = config.get(string.lower(key))
		# Remove .sty extension from each style filename (freaking tex)
		# XXX Can't handle --style foo.sty,bar.sty
		if target == 'tex' and key == 'STYLE':
			val = map(lambda x:re.sub('(?i)\.sty$','',x), val)
		if key == 'ENCODING':
			val = get_encoding_string(val, target)
		head_data[key] = val
	# Parse header contents
	for i in 0,1,2:
		# Expand macros
		contents = MacroMaster(config=config).expand(headers[i])
		# Escapes - on tex, just do it if any \tag{} present
		if target != 'tex' or \
		  (target == 'tex' and re.search(r'\\\w+{', contents)):
			contents = doEscape(target, contents)
		if target == 'lout':
			contents = doFinalEscape(target, contents)
		
		head_data['HEADER%d'%(i+1)] = contents
	# css-inside removes STYLE line
	#XXX In tex, this also removes the modules call (%!style:amsfonts)
	if target in ('html','xhtml') and config.get('css-inside') and \
	   config.get('style'):
		head_data['STYLE'] = []
	Debug("Header Data: %s"%head_data, 1)
	# Scan for empty dictionary keys
	# If found, scan template lines for that key reference
	# If found, remove the reference
	# If there isn't any other key reference on the same line, remove it
	#TODO loop by template line > key
	for key in head_data.keys():
		if head_data.get(key): continue
		for line in template:
			if string.count(line, '%%(%s)s'%key):
				sline = string.replace(line, '%%(%s)s'%key, '')
				if not re.search(r'%\([A-Z0-9]+\)s', sline):
					template.remove(line)
	# Style is a multiple tag.
	# - If none or just one, use default template
	# - If two or more, insert extra lines in a loop (and remove original)
	styles = head_data['STYLE']
	if len(styles) == 1:
		head_data['STYLE'] = styles[0]
	elif len(styles) > 1:
		style_mark = '%(STYLE)s'
		for i in xrange(len(template)):
			if string.count(template[i], style_mark):
				while styles:
					template.insert(i+1,
						string.replace(
							template[i],
							style_mark,
							styles.pop()))
				del template[i]
				break
	# Populate template with data (dict expansion)
	template = string.join(template, '\n') % head_data
	
	# Adding CSS contents into template (for --css-inside)
	# This code sux. Dirty++
	if target in ('html','xhtml') and config.get('css-inside') and \
	   config.get('style'):
		set_global_config(config) # usually on convert(), needed here
		for i in xrange(len(config['style'])):
			cssfile = config['style'][i]
			if not os.path.isabs(cssfile):
				infile = config.get('sourcefile')
				cssfile = os.path.join(
					os.path.dirname(infile), cssfile)
			try:
				contents = Readfile(cssfile, 1)
				css = "\n%s\n%s\n%s\n%s\n" % (
					doCommentLine("Included %s" % cssfile),
					TAGS['cssOpen'],
					string.join(contents, '\n'),
					TAGS['cssClose'])
				# Style now is content, needs escaping (tex)
				#css = maskEscapeChar(css)
			except:
				errmsg = "CSS include failed for %s" % cssfile
				css = "\n%s\n" % (doCommentLine(errmsg))
			# Insert this CSS file contents on the template
			template = re.sub('(?i)(</HEAD>)', css+r'\1', template)
			# template = re.sub(r'(?i)(\\begin{document})',
			#		css+'\n'+r'\1', template) # tex
		
		# The last blank line to keep everything separated
		template = re.sub('(?i)(</HEAD>)', '\n'+r'\1', template)
	
	return string.split(template, '\n')

def doCommentLine(txt):
	# The -- string ends a (h|sg|xht)ml comment :(
	txt = maskEscapeChar(txt)
	if string.count(TAGS['comment'], '--') and \
	   string.count(txt, '--'):
		txt = re.sub('-(?=-)', r'-\\', txt)
	
	if TAGS['comment']:
		return regex['x'].sub(txt, TAGS['comment'])
	return ''

def doFooter(config):
	if not config['headers']: return []
	ret = []
	target = config['target']
	cmdline = config['realcmdline']
	typename = target
	if target == 'tex': typename = 'LaTeX2e'
	ppgd = '%s code generated by %s %s (%s)'%(
	        typename,my_name,my_version,my_url)
	cmdline = 'cmdline: %s %s'%(my_name, string.join(cmdline, ' '))
	ret.append('')
	ret.append(doCommentLine(ppgd))
	ret.append(doCommentLine(cmdline))
	ret.append(TAGS['EOD'])
	return ret

def doEscape(target,txt):
	"Target-specific special escapes. Apply *before* insert any tag."
	tmpmask = 'vvvvThisEscapingSuxvvvv'
	if target in ('html','sgml','xhtml'):
		txt = re.sub('&','&amp;',txt)
		txt = re.sub('<','&lt;',txt)
		txt = re.sub('>','&gt;',txt)
		if target == 'sgml':
			txt = re.sub('\xff','&yuml;',txt)  # "+y
	elif target == 'pm6':
		txt = re.sub('<','<\#60>',txt)
	elif target == 'mgp':
		txt = re.sub('^%',' %',txt)  # add leading blank to avoid parse
	elif target == 'man':
		txt = re.sub("^([.'])", '\\&\\1',txt)           # command ID
		txt = string.replace(txt,ESCCHAR, ESCCHAR+'e')  # \e
	elif target == 'lout':
		# TIP: / moved to FinalEscape to avoid //italic//
		# TIP: these are also converted by lout:  ...  ---  --
		txt = string.replace(txt, ESCCHAR, tmpmask)             # \
		txt = string.replace(txt, '"', '"%s""'%ESCCHAR)         # "\""
		txt = re.sub('([|&{}@#^~])', '"\\1"',txt)               # "@"
		txt = string.replace(txt, tmpmask, '"%s"'%(ESCCHAR*2))  # "\\"
	elif target == 'tex':
		# Mark literal \ to be changed to $\backslash$ later
		txt = string.replace( txt, ESCCHAR, tmpmask)
		txt = re.sub('([#$&%{}])', ESCCHAR+r'\1'  , txt)  # \%
		txt = re.sub('([~^])'    , ESCCHAR+r'\1{}', txt)  # \~{}
		txt = re.sub('([<|>])'   ,         r'$\1$', txt)  # $>$
		txt = string.replace(txt, tmpmask,
		                     maskEscapeChar(r'$\backslash$'))
		# TIP the _ is escaped at the end
	return txt

# TODO man: where - really needs to be escaped?
def doFinalEscape(target, txt):
	"Last escapes of each line"
	if   target == 'pm6' : txt = string.replace(txt,ESCCHAR+'<',r'<\#92><')
	elif target == 'man' : txt = string.replace(txt, '-', r'\-')
	elif target == 'sgml': txt = string.replace(txt, '[', '&lsqb;')
	elif target == 'lout': txt = string.replace(txt, '/', '"/"')
	elif target == 'tex' :
		txt = string.replace(txt, '_', r'\_')
		txt = string.replace(txt, 'vvvvTexUndervvvv', '_')  # shame!
	return txt

def EscapeCharHandler(action, data):
	"Mask/Unmask the Escape Char on the given string"
	if not string.strip(data): return data
	if action not in ('mask','unmask'):
		Error("EscapeCharHandler: Invalid action '%s'"%action)
	if action == 'mask': return string.replace(data,'\\',ESCCHAR)
	else:                return string.replace(data,ESCCHAR,'\\')

def maskEscapeChar(data):
	"Replace any Escape Char \ with a text mask (Input: str or list)"
	if type(data) == type([]):
		return map(lambda x: EscapeCharHandler('mask', x), data)
	return EscapeCharHandler('mask',data)

def unmaskEscapeChar(data):
	"Undo the Escape char \ masking (Input: str or list)"
	if type(data) == type([]):
		return map(lambda x: EscapeCharHandler('unmask', x), data)
	return EscapeCharHandler('unmask',data)

def addLineBreaks(mylist):
	"use LB to respect sys.platform"
	ret = []
	for line in mylist:
		line = string.replace(line,'\n',LB)  # embedded \n's
		ret.append(line+LB)                  # add final line break
	return ret

# Convert ['foo\nbar'] to ['foo', 'bar']
def expandLineBreaks(mylist):
	ret = []
	for line in mylist:
		ret.extend(string.split(line, '\n'))
	return ret

def compile_filters(filters, errmsg='Filter'):
	if filters:
		for i in xrange(len(filters)):
			patt,repl = filters[i]
			try: rgx = re.compile(patt)
			except: Error("%s: '%s'"%(errmsg, patt))
			filters[i] = (rgx,repl)
	return filters

def enclose_me(tagname, txt):
	return TAGS.get(tagname+'Open') + txt + TAGS.get(tagname+'Close')

def beautify_me(name, line):
	"where name is: bold, italic or underline"
	name  = 'font%s' % string.capitalize(name)
	open  = TAGS['%sOpen'%name]
	close = TAGS['%sClose'%name]
	txt = r'%s\1%s'%(open, close)
	line = regex[name].sub(txt,line)
	return line

def get_tagged_link(label, url):
	ret = ''
	target = CONF['target']
	image_re = regex['img']
	
	# Set link type
	if regex['email'].match(url):
		linktype = 'email'
	else:
		linktype = 'url';
	
	# Escape specials from TEXT parts
	label = doEscape(target,label)
	
	# Escape specials from link URL
	if not rules['linkable'] or rules['escapeurl']:
		url = doEscape(target, url)
	
	# Adding protocol to guessed link
	guessurl = ''
	if linktype == 'url' and \
	   re.match('(?i)'+regex['_urlskel']['guess'], url):
		if url[0] in 'Ww': guessurl = 'http://' +url
		else             : guessurl =  'ftp://' +url
		
		# Not link aware targets -> protocol is useless
		if not rules['linkable']: guessurl = ''
	
	# Simple link (not guessed)
	if not label and not guessurl:
		if CONF['mask-email'] and linktype == 'email':
			# Do the email mask feature (no TAGs, just text)
			url = string.replace(url,'@',' (a) ')
			url = string.replace(url,'.',' ')
			url = "<%s>" % url
			if rules['linkable']: url = doEscape(target, url)
			ret = url
		else:
			# Just add link data to tag
			tag = TAGS[linktype]
			ret = regex['x'].sub(url,tag)
	
	# Named link or guessed simple link
	else:
		# Adjusts for guessed link
		if not label: label = url         # no   protocol
		if guessurl : url   = guessurl    # with protocol
		
		# Image inside link!
		if image_re.match(label):
			if rules['imglinkable']:  # get image tag
				label = parse_images(label)
			else:                     #  img@link !supported
				label = "(%s)"%image_re.match(label).group(1)
		
		# Putting data on the right appearance order
		if rules['linkable']:
			urlorder = [url, label]   # link before label
		else:
			urlorder = [label, url]   # label before link
		
		# Add link data to tag (replace \a's)
		ret = TAGS["%sMark"%linktype]
		for data in urlorder:
			ret = regex['x'].sub(data,ret,1)
	
	return ret


def parse_deflist_term(line):
	"Extract and parse definition list term contents"
	img_re = regex['img']
	term   = regex['deflist'].search(line).group(3)
	
	# Mask image inside term as (image.jpg), where not supported
	if not rules['imgasdefterm'] and img_re.search(term):
		while img_re.search(term):
			imgfile = img_re.search(term).group(1)
			term = img_re.sub('(%s)'%imgfile, term, 1)
	
	#TODO tex: escape ] on term. \], \rbrack{} and \verb!]! don't work :(
	return term


def get_tagged_bar(line):
	m = regex['bar'].search(line)
	if not m: return line
	txt = m.group(2)
	
	# Map strong bar to pagebreak
	if rules['mapbar2pagebreak'] and TAGS['pageBreak']:
		TAGS['bar2'] = TAGS['pageBreak']
	
	# Set bar type
	if txt[0] == '=': bar = TAGS['bar2']
	else            : bar = TAGS['bar1']
	
	# To avoid comment tag confusion like <!-- ------ -->
	if string.count(TAGS['comment'], '--'):
		txt = string.replace(txt,'--','__')
	
	# Tag line
	return regex['x'].sub(txt, bar)


def get_image_align(line):
	"Return the image (first found) align for the given line"
	
	# First clear marks that can mess align detection
	line = re.sub(SEPARATOR+'$', '', line)  # remove deflist sep
	line = re.sub('^'+SEPARATOR, '', line)  # remove list sep
	line = re.sub('^[\t]+'     , '', line)  # remove quote mark
	
	# Get image position on the line
	m = regex['img'].search(line)
	ini = m.start() ; head = 0
	end = m.end()   ; tail = len(line)
	
	# The align detection algorithm
	if   ini == head and end != tail: align = 'left'   # ^img + text$
	elif ini != head and end == tail: align = 'right'  # ^text + img$
	else                            : align = 'center' # default align
	
	# Some special cases
	if BLOCK.isblock('table'): align = 'center'    # ignore when table
#	if TARGET == 'mgp' and align == 'center': align = 'center'
	
	return align


# Reference: http://www.iana.org/assignments/character-sets
# http://www.drclue.net/F1.cgi/HTML/META/META.html
def get_encoding_string(enc, target):
	if not enc: return ''
	# Target specific translation table
	translate = {
	'tex': {
	  # missing: ansinew , applemac , cp437 , cp437de , cp865
	  'us-ascii'    : 'ascii',
	  'windows-1250': 'cp1250',
	  'windows-1252': 'cp1252',
	  'ibm850'      : 'cp850',
	  'ibm852'      : 'cp852',
	  'iso-8859-1'  : 'latin1',
	  'iso-8859-2'  : 'latin2',
	  'iso-8859-3'  : 'latin3',
	  'iso-8859-4'  : 'latin4',
	  'iso-8859-5'  : 'latin5',
	  'iso-8859-9'  : 'latin9',
	  'koi8-r'      : 'koi8-r'
	  }
	}
	# Normalization
	enc = re.sub('(?i)(us[-_]?)?ascii|us|ibm367','us-ascii'  , enc)
	enc = re.sub('(?i)(ibm|cp)?85([02])'        ,'ibm85\\2'  , enc)
	enc = re.sub('(?i)(iso[_-]?)?8859[_-]?'     ,'iso-8859-' , enc)
	enc = re.sub('iso-8859-($|[^1-9]).*'        ,'iso-8859-1', enc)
	# Apply translation table
	try: enc = translate[target][string.lower(enc)]
	except: pass
	return enc


##############################################################################
##MerryChristmas,IdontwanttofighttonightwithyouImissyourbodyandIneedyourlove##
##############################################################################


def process_source_file(file='', noconf=0, contents=[]):
	"""
	Find and Join all the configuration available for a source file.
	No sanity checking is done on this step.
	It also extracts the source document parts into separate holders.
	
	The config scan order is:
	   1. The user configuration file (i.e. $HOME/.txt2tagsrc)
	   2. The source document's CONF area
	   3. The command line options

	The return data is a tuple of two items:
	   1. The parsed config dictionary
	   2. The document's parts, as a (head, conf, body) tuple
	
	All the conversion process will be based on the data and
	configuration returned by this function.
	The source files is read on this step only.
	"""
	if contents:
		source = SourceDocument(contents=contents)
	else:
		source = SourceDocument(file)
	head, conf, body = source.split()
	Message(_("Source document contents stored"),2)
	if not noconf:
		# Read document config
		source_raw = source.get_raw_config()
		# Join all the config directives found, then parse it
		full_raw = RC_RAW + source_raw + CMDLINE_RAW
		Message(_("Parsing and saving all config found (%03d items)")%(
		        len(full_raw)),1)
		full_parsed = ConfigMaster(full_raw).parse()
		# Add manually the filename to the conf dic
		if contents:
			full_parsed['sourcefile'] = MODULEIN
			full_parsed['infile'] = MODULEIN
			full_parsed['outfile'] = MODULEOUT
		else:
			full_parsed['sourcefile'] = file
		# Maybe should we dump the config found?
		if full_parsed.get('dump-config'):
			dumpConfig(source_raw, full_parsed)
			Quit()
		# Okay, all done
		Debug("FULL config for this file: %s"%full_parsed, 1)
	else:
		full_parsed = {}
	return full_parsed, (head,conf,body)

def get_infiles_config(infiles):
	"""
	Find and Join into a single list, all configuration available
	for each input file. This function is supposed to be the very
	first one to be called, before any processing.
	"""
	return map(process_source_file, infiles)

def convert_this_files(configs):
	global CONF
	for myconf,doc in configs:                 # multifile support
		target_head = []
		target_toc  = []
		target_body = []
		target_foot = []
		source_head, source_conf, source_body = doc
		myconf = ConfigMaster().sanity(myconf)
		# Compose the target file Headers
		#TODO escape line before?
		#TODO see exceptions by tex and mgp
		Message(_("Composing target Headers"),1)
		target_head = doHeader(source_head, myconf)
		# Parse the full marked body into tagged target
		first_body_line = (len(source_head) or 1)+ len(source_conf) + 1
		Message(_("Composing target Body"),1)
		target_body, marked_toc = convert(source_body, myconf,
		                          firstlinenr=first_body_line)
		# If dump-source, we're done
		if myconf['dump-source']:
			for line in source_head+source_conf+target_body:
				print line
			return
		# Make TOC (if needed)
		Message(_("Composing target TOC"),1)
		tagged_toc  = toc_tagger(marked_toc, myconf)
		target_toc  = toc_formatter(tagged_toc, myconf)
		target_body = toc_inside_body(target_body, target_toc, myconf)
		if not AUTOTOC and not myconf['toc-only']: target_toc = []
		# Compose the target file Footer
		Message(_("Composing target Footer"),1)
		target_foot = doFooter(myconf)
		# Finally, we have our document
		outlist = target_head + target_toc + target_body + target_foot
		# If on GUI, abort before finish_him
		# If module, return finish_him as list
		# Else, write results to file or STDOUT
		if GUI:
			return outlist, myconf
		elif myconf.get('outfile') == MODULEOUT:
			return finish_him(outlist, myconf), myconf
		else:
			Message(_("Saving results to the output file"),1)
			finish_him(outlist, myconf)


def parse_images(line):
	"Tag all images found"
	while regex['img'].search(line) and TAGS['img'] != '[\a]':
		txt = regex['img'].search(line).group(1)
		tag = TAGS['img']
		
		# HTML, XHTML and mgp!
		if rules['imgalignable']:
			align = get_image_align(line)
			# Add align on tag
			align_name = string.capitalize(align)
			align_tag = TAGS['imgAlign'+align_name]
			tag = regex['_imgAlign'].sub(align_tag, tag, 1)
			# Dirty fix to allow centered solo images
			if align == 'center' and TARGET in ('html','xhtml'):
				rest = regex['img'].sub('',line,1)
				if re.match('^\s+$', rest):
					tag = "<center>%s</center>" %tag
		
		if TARGET == 'tex':
			tag = re.sub(r'\\b',r'\\\\b',tag)
			txt = string.replace(txt, '_', 'vvvvTexUndervvvv')
		
		line = regex['img'].sub(tag,line,1)
		line = regex['x'].sub(txt,line,1)
	return line


def add_inline_tags(line):
	# Beautifiers
	for beauti in ('Bold', 'Italic', 'Underline'):
		if regex['font%s'%beauti].search(line):
			line = beautify_me(beauti, line)
	
	line = parse_images(line)
	return line


def get_include_contents(file, path=''):
	"Parses %!include: value and extract file contents"
	ids = {'`':'verb', '"':'raw', "'":'tagged' }
	id = 't2t'
	# Set include type and remove identifier marks
	mark = file[0]
	if mark in ids.keys():
		if file[:2] == file[-2:] == mark*2:
			id = ids[mark]     # set type
			file = file[2:-2]  # remove marks
	# Handle remote dir execution
	filepath = os.path.join(path, file)
	# Read included file contents
	lines = Readfile(filepath, remove_linebreaks=1)
	# Default txt2tags marked text, just BODY matters
	if id == 't2t':
		lines = get_file_body(filepath)
		lines.insert(0, '%%INCLUDED(%s) starts here: %s'%(id,file))
		# This appears when included hit EOF with verbatim area open
		#lines.append('%%INCLUDED(%s) ends here: %s'%(id,file))
	return id, lines


def set_global_config(config):
	global CONF, TAGS, regex, rules, TARGET
	CONF   = config
	TAGS   = getTags(CONF)
	rules  = getRules(CONF)
	regex  = getRegexes()
	TARGET = config['target']  # save for buggy functions that need global


def convert(bodylines, config, firstlinenr=1):
	global BLOCK
	
	set_global_config(config)
	
	target = config['target']
	BLOCK = BlockMaster()
	MASK  =  MaskMaster()
	TITLE = TitleMaster()
	
	ret = []
	dump_source = []
	f_lastwasblank = 0
	
	# Compiling all PreProc regexes
	pre_filter = compile_filters(
		CONF['preproc'], _('Invalid PreProc filter regex'))
	
	# Let's mark it up!
	linenr = firstlinenr-1
	lineref = 0
	while lineref < len(bodylines):
		# Defaults
		MASK.reset()
		results_box = ''
		
		untouchedline = bodylines[lineref]
		dump_source.append(untouchedline)
		
		line = re.sub('[\n\r]+$','',untouchedline)   # del line break
		
		# Apply PreProc filters
		if pre_filter:
			errmsg = _('Invalid PreProc filter replacement')
			for rgx,repl in pre_filter:
				try: line = rgx.sub(repl, line)
				except: Error("%s: '%s'"%(errmsg, repl))
		
		line = maskEscapeChar(line)                  # protect \ char
		linenr  = linenr  +1
		lineref = lineref +1
		
		Debug(repr(line), 2, linenr)  # heavy debug: show each line
		
		#------------------[ Comment Block ]------------------------
		
		# We're already on a comment block
		if BLOCK.block() == 'comment':
		
			# Closing comment
			if regex['blockCommentClose'].search(line):
				ret.extend(BLOCK.blockout() or [])
				continue
			
			# Normal comment-inside line. Ignore it.
			continue
		
		# Detecting comment block init
		if regex['blockCommentOpen'].search(line) \
		   and BLOCK.block() not in BLOCK.exclusive:
			ret.extend(BLOCK.blockin('comment'))
			continue
		
		#-------------------------[ Raw Text ]----------------------
		
		# We're already on a raw block
		if BLOCK.block() == 'raw':
		
			# Closing raw
			if regex['blockRawClose'].search(line):
				ret.extend(BLOCK.blockout())
				continue
			
			# Normal raw-inside line
			BLOCK.holdadd(line)
			continue
		
		# Detecting raw block init
		if regex['blockRawOpen'].search(line) \
		   and BLOCK.block() not in BLOCK.exclusive:
			ret.extend(BLOCK.blockin('raw'))
			continue
		
		# One line raw text
		if regex['1lineRaw'].search(line) \
		   and BLOCK.block() not in BLOCK.exclusive:
			ret.extend(BLOCK.blockin('raw'))
			line = regex['1lineRaw'].sub('',line)
			BLOCK.holdadd(line)
			ret.extend(BLOCK.blockout())
			continue
		
		#------------------------[ Verbatim  ]----------------------
		
		#TIP We'll never support beautifiers inside verbatim
		
		# Closing table mapped to verb
		if BLOCK.block() == 'verb' \
		   and BLOCK.prop('mapped') == 'table' \
		   and not regex['table'].search(line):
			ret.extend(BLOCK.blockout())
		
		# We're already on a verb block
		if BLOCK.block() == 'verb':
			
			# Closing verb
			if regex['blockVerbClose'].search(line):
				ret.extend(BLOCK.blockout())
				continue
			
			# Normal verb-inside line
			BLOCK.holdadd(line)
			continue
		
		# Detecting verb block init
		if regex['blockVerbOpen'].search(line) \
		   and BLOCK.block() not in BLOCK.exclusive:
			ret.extend(BLOCK.blockin('verb'))
			f_lastwasblank = 0
			continue
		
		# One line verb-formatted text
		if regex['1lineVerb'].search(line) \
		   and BLOCK.block() not in BLOCK.exclusive:
			ret.extend(BLOCK.blockin('verb'))
			line = regex['1lineVerb'].sub('',line)
			BLOCK.holdadd(line)
			ret.extend(BLOCK.blockout())
			f_lastwasblank = 0
			continue
		
		# Tables are mapped to verb when target is not table-aware
		if not rules['tableable'] and regex['table'].search(line):
			if not BLOCK.isblock('verb'):
				ret.extend(BLOCK.blockin('verb'))
				BLOCK.propset('mapped', 'table')
				BLOCK.holdadd(line)
				continue
		
		#---------------------[ blank lines ]-----------------------
		
		if regex['blankline'].search(line):
			
			# Close open paragraph
			if BLOCK.isblock('para'):
				ret.extend(BLOCK.blockout())
				f_lastwasblank = 1
				continue
			
			# Close all open tables
			if BLOCK.isblock('table'):
				ret.extend(BLOCK.blockout())
				f_lastwasblank = 1
				continue
			
			# Close all open quotes
			while BLOCK.isblock('quote'):
				ret.extend(BLOCK.blockout())
			
			# Closing all open lists
			if f_lastwasblank:          # 2nd consecutive blank
				if BLOCK.block()[-4:] == 'list':
					BLOCK.holdaddsub('')   # helps parser
				while BLOCK.depth:  # closes list (if any)
					ret.extend(BLOCK.blockout())
				continue            # ignore consecutive blanks
			
			# Paragraph (if any) is wanted inside lists also
			if BLOCK.block()[-4:] == 'list':
				BLOCK.holdaddsub('')
			else:
				# html: show blank line (needs tag)
				if target in ('html','xhtml'):
					ret.append(TAGS['paragraphOpen']+\
					           TAGS['paragraphClose'])
				# Otherwise we just show a blank line
				else:
					ret.append('')
			
			f_lastwasblank = 1
			continue
		
		
		#---------------------[ special ]---------------------------
		
		if regex['special'].search(line):
			# Include command
			targ, key, val = ConfigLines().parse_line(
			                   line, 'include', target)
			if key:
				Debug("Found config '%s', value '%s'"%(
				       key,val),1,linenr)
				
				incpath = os.path.dirname(CONF['sourcefile'])
				incfile = val
				err = _('A file cannot include itself (loop!)')
				if CONF['sourcefile'] == incfile:
					Error("%s: %s"%(err,incfile))
				inctype, inclines = get_include_contents(
				                      incfile, incpath)
				# Verb, raw and tagged are easy
				if inctype != 't2t':
					ret.extend(BLOCK.blockin(inctype))
					BLOCK.holdextend(inclines)
					ret.extend(BLOCK.blockout())
				else:
					# Insert include lines into body
					#TODO include maxdepth limit
					bodylines = bodylines[:lineref] \
					           +inclines \
					           +bodylines[lineref:]
					#TODO fix path if include@include
					# Remove %!include call
					if CONF['dump-source']:
						dump_source.pop()
				continue
			else:
				Debug('Bogus Special Line',1,linenr)
		
		#---------------------[ dump-source ]-----------------------
		
		# We don't need to go any further
		if CONF['dump-source']:
			continue
		
		#---------------------[ Comments ]--------------------------
		
		# Just skip them (if not macro)
		if regex['comment'].search(line) and not \
		   regex['macros'].match(line) and not \
		   regex['toc'].match(line):
			continue
		
		#---------------------[ Triggers ]--------------------------
		
		# Valid line, reset blank status
		f_lastwasblank = 0
		
		# Any NOT quote line closes all open quotes
		if BLOCK.isblock('quote') and not regex['quote'].search(line):
			while BLOCK.isblock('quote'):
				ret.extend(BLOCK.blockout())
		
		# Any NOT table line closes an open table
		if BLOCK.isblock('table') and not regex['table'].search(line):
			ret.extend(BLOCK.blockout())
		
		
		#---------------------[ Horizontal Bar ]--------------------
		
		if regex['bar'].search(line):
			
			# A bar closes a paragraph
			if BLOCK.isblock('para'):
				ret.extend(BLOCK.blockout())
			
			# We need to close all opened quote blocks
			# if bar isn't allowed inside or if not a quote line
			if BLOCK.isblock('quote'):
				if not rules['barinsidequote'] or \
				   not regex['quote'].search(line):
					while BLOCK.isblock('quote'):
						ret.extend(BLOCK.blockout())
			
			# Quote + bar: continue processing for quoting
			if rules['barinsidequote'] and \
			   regex['quote'].search(line):
				pass
			
			# Just bar: save tagged line and we're done
			else:
				line = get_tagged_bar(line)
				if BLOCK.block()[-4:] == 'list':
					BLOCK.holdaddsub(line)
				elif BLOCK.block():
					BLOCK.holdadd(line)
				else:
					ret.append(line)
					Debug("BAR: %s"%line, 6)
				continue
		
		#---------------------[ Title ]-----------------------------
		
		#TODO set next blank and set f_lastwasblank or f_lasttitle
		if (regex['title'].search(line) or
		    regex['numtitle'].search(line)) and \
		    BLOCK.block()[-4:] != 'list':
			
			# A title closes a paragraph
			if BLOCK.isblock('para'):
				ret.extend(BLOCK.blockout())
			
			TITLE.add(line)
			tagged_title = TITLE.get()
			ret.extend(tagged_title)
			Debug("TITLE: %s"%tagged_title, 6)
			
			f_lastwasblank = 1
			continue
		
		#---------------------[ %%toc ]-----------------------
		
		# %%toc line closes paragraph
		if BLOCK.block() == 'para' and regex['toc'].search(line):
			ret.extend(BLOCK.blockout())
		
		#---------------------[ apply masks ]-----------------------
		
		line = MASK.mask(line)
		
		#XXX from here, only block-inside lines will pass
		
		#---------------------[ Quote ]-----------------------------
		
		if regex['quote'].search(line):
			
			# Store number of leading TABS
			quotedepth = len(regex['quote'].search(line).group(0))
			
			# SGML doesn't support nested quotes
			if rules['quotenotnested']: quotedepth = 1
			
			# Don't cross depth limit
			maxdepth = rules['quotemaxdepth']
			if maxdepth and quotedepth > maxdepth:
				quotedepth = maxdepth
			
			# New quote
			if not BLOCK.isblock('quote'):
				ret.extend(BLOCK.blockin('quote'))
			
			# New subquotes
			while BLOCK.depth < quotedepth:
				BLOCK.blockin('quote')
			
			# Closing quotes
			while quotedepth < BLOCK.depth:
				ret.extend(BLOCK.blockout())
		
		#---------------------[ Lists ]-----------------------------
		
		# An empty item also closes the current list
		if BLOCK.block()[-4:] == 'list':
			m = regex['listclose'].match(line)
			if m:
				listindent = m.group(1)
				listtype = m.group(2)
				currlisttype = BLOCK.prop('type')
				currlistindent = BLOCK.prop('indent')
				if listindent == currlistindent and \
				   listtype == currlisttype:
					ret.extend(BLOCK.blockout())
					continue
		
		if   regex['list'].search(line) or \
		  regex['numlist'].search(line) or \
		  regex['deflist'].search(line):
			
			listindent = BLOCK.prop('indent')
			listids = string.join(LISTNAMES.keys(), '')
			m = re.match('^( *)([%s]) '%listids, line)
			listitemindent = m.group(1)
			listtype = m.group(2)
			listname = LISTNAMES[listtype]
			results_box = BLOCK.holdadd
			
			# Del list ID (and separate term from definition)
			if listname == 'deflist':
				term = parse_deflist_term(line)
				line = regex['deflist'].sub(
					SEPARATOR+term+SEPARATOR,line)
			else:
				line = regex[listname].sub(SEPARATOR,line)
			
			# Don't cross depth limit
			maxdepth = rules['listmaxdepth']
			if maxdepth and BLOCK.depth == maxdepth:
				if len(listitemindent) > len(listindent):
					listitemindent = listindent
			
			# List bumping (same indent, diff mark)
			# Close the currently open list to clear the mess
			if BLOCK.block()[-4:] == 'list' \
			   and listname != BLOCK.block() \
			   and len(listitemindent) == len(listindent):
				ret.extend(BLOCK.blockout())
				listindent = BLOCK.prop('indent')
			
			# Open mother list or sublist
			if BLOCK.block()[-4:] != 'list' or \
			   len(listitemindent) > len(listindent):
				ret.extend(BLOCK.blockin(listname))
				BLOCK.propset('indent',listitemindent)
				BLOCK.propset('type',listtype)
			
			# Closing sublists
			while len(listitemindent) < len(BLOCK.prop('indent')):
				ret.extend(BLOCK.blockout())
			
			# O-oh, sublist before list ("\n\n  - foo\n- foo")
			# Fix: close sublist (as mother), open another list
			if BLOCK.block()[-4:] != 'list':
				ret.extend(BLOCK.blockin(listname))
				BLOCK.propset('indent',listitemindent)
				BLOCK.propset('type',listtype)
		
		#---------------------[ Table ]-----------------------------
		
		#TODO escape undesired format inside table
		#TODO add pm6 target
		if regex['table'].search(line):
			
			if not BLOCK.isblock('table'):   # first table line!
				ret.extend(BLOCK.blockin('table'))
				BLOCK.tableparser.__init__(line)
			
			tablerow = TableMaster().parse_row(line)
			BLOCK.tableparser.add_row(tablerow)     # save config
			
			# Maintain line to unmask and inlines
			line = string.join(tablerow['cells'], SEPARATOR)
		
		#---------------------[ Paragraph ]-------------------------
		
		if not BLOCK.block() and \
		   not string.count(line, MASK.tocmask): # new para!
			ret.extend(BLOCK.blockin('para'))
		
		
		############################################################
		############################################################
		############################################################
		
		
		#---------------------[ Final Parses ]----------------------
		
		# The target-specific special char escapes for body lines
		line = doEscape(target,line)
		
		line = add_inline_tags(line)
		line = MASK.undo(line)
		
		
		#---------------------[ Hold or Return? ]-------------------
		
		### Now we must choose where to put the parsed line
		#
		if not results_box:
			# List item extra lines
			if BLOCK.block()[-4:] == 'list':
				results_box = BLOCK.holdaddsub
			# Other blocks
			elif BLOCK.block():
				results_box = BLOCK.holdadd
			# No blocks
			else:
				line = doFinalEscape(target, line)
				results_box = ret.append
		
		results_box(line)
	
	# EOF: close any open para/verb/lists/table/quotes
	Debug('EOF',7)
	while BLOCK.block():
		ret.extend(BLOCK.blockout())
	
	# Maybe close some opened title area?
	if rules['titleblocks']:
		ret.extend(TITLE.close_all())
	
	# Maybe a major tag to enclose body? (like DIV for CSS)
	if TAGS['bodyOpen' ]: ret.insert(0, TAGS['bodyOpen'])
	if TAGS['bodyClose']: ret.append(TAGS['bodyClose'])
	
	if CONF['toc-only']: ret = []
	marked_toc = TITLE.dump_marked_toc(CONF['toc-level'])
	
	# If dump-source, all parsing is ignored
	if CONF['dump-source']: ret = dump_source[:]
	
	return ret, marked_toc



##############################################################################
################################### GUI ######################################
##############################################################################
#
# Tk help: http://python.org/topics/tkinter/
#    Tuto: http://ibiblio.org/obp/py4fun/gui/tkPhone.html
#          /usr/lib/python*/lib-tk/Tkinter.py
#
# grid table : row=0, column=0, columnspan=2, rowspan=2
# grid align : sticky='n,s,e,w' (North, South, East, West)
# pack place : side='top,bottom,right,left'
# pack fill  : fill='x,y,both,none', expand=1
# pack align : anchor='n,s,e,w' (North, South, East, West)
# padding    : padx=10, pady=10, ipadx=10, ipady=10 (internal)
# checkbox   : offvalue is return if the _user_ deselected the box
# label align: justify=left,right,center

def load_GUI_resources():
	"Load all extra modules and methods used by GUI"
	global askopenfilename, showinfo, showwarning, showerror, Tkinter
	from tkFileDialog import askopenfilename
	from tkMessageBox import showinfo,showwarning,showerror
	import Tkinter

class Gui:
	"Graphical Tk Interface"
	def __init__(self, conf={}):
		self.root = Tkinter.Tk()    # mother window, come to butthead
		self.root.title(my_name)    # window title bar text
		self.window = self.root     # variable "focus" for inclusion
		self.row = 0                # row count for grid()
		
		self.action_length = 150    # left column length (pixel)
		self.frame_margin  = 10     # frame margin size  (pixel)
		self.frame_border  = 6      # frame border size  (pixel)
		
		# The default Gui colors, can be changed by %!guicolors
		self.dft_gui_colors = ['#6c6','white','#cf9','#030']
		self.gui_colors = []
		self.bg1 = self.fg1 = self.bg2 = self.fg2 = ''
		
		# On Tk, vars need to be set/get using setvar()/get()
		self.infile  = self.setvar('')
		self.target  = self.setvar('')
		self.target_name = self.setvar('')
		
		# The checks appearance order
		self.checks  = [
		  'headers','enum-title','toc','mask-email',
		  'toc-only','stdout']
		
		# Creating variables for all checks
		for check in self.checks:
			setattr(self, 'f_'+check, self.setvar(''))
		
		# Load RC config
		self.conf = {}
		if conf: self.load_config(conf)
	
	def load_config(self, conf):
		self.conf = conf
		self.gui_colors = conf.get('guicolors') or self.dft_gui_colors
		self.bg1, self.fg1, self.bg2, self.fg2 = self.gui_colors
		self.root.config(bd=15,bg=self.bg1)
	
	### Config as dic for python 1.5 compat (**opts don't work :( )
	def entry(self, **opts): return Tkinter.Entry(self.window, opts)
	def label(self, txt='', bg=None, **opts):
		opts.update({'text':txt,'bg':bg or self.bg1})
		return Tkinter.Label(self.window, opts)
	def button(self,name,cmd,**opts):
		opts.update({'text':name,'command':cmd})
		return Tkinter.Button(self.window, opts)
	def check(self,name,checked=0,**opts):
		bg, fg = self.bg2, self.fg2
		opts.update({
		  'text':name, 'onvalue':1, 'offvalue':0,
		  'activeforeground':fg, 'fg':fg,
		  'activebackground':bg, 'bg':bg,
		  'highlightbackground':bg, 'anchor':'w'
		})
		chk = Tkinter.Checkbutton(self.window, opts)
		if checked: chk.select()
		chk.grid(columnspan=2, sticky='w', padx=0)
	def menu(self,sel,items):
		return apply(Tkinter.OptionMenu,(self.window,sel)+tuple(items))
	
	# Handy auxiliary functions
	def action(self, txt):
		self.label(txt, fg=self.fg1, bg=self.bg1,
		     wraplength=self.action_length).grid(column=0,row=self.row)
	def frame_open(self):
		self.window = Tkinter.Frame(self.root,bg=self.bg2,
		     borderwidth=self.frame_border)
	def frame_close(self):
		self.window.grid(column=1, row=self.row, sticky='w',
		     padx=self.frame_margin)
		self.window = self.root
		self.label('').grid()
		self.row = self.row + 2   # update row count
	def target_name2key(self):
		name = self.target_name.get()
		target = filter(lambda x: TARGET_NAMES[x] == name, TARGETS)
		try   : key = target[0]
		except: key = ''
		self.target = self.setvar(key)
	def target_key2name(self):
		key = self.target.get()
		name = TARGET_NAMES.get(key) or key
		self.target_name = self.setvar(name)
	
	def exit(self): self.root.destroy()
	def setvar(self, val): z = Tkinter.StringVar() ; z.set(val) ; return z
	
	def askfile(self):
		ftypes= [(_('txt2tags files'),('*.t2t','*.txt')),
		         (_('All files'),'*')]
		newfile = askopenfilename(filetypes=ftypes)
		if newfile:
			self.infile.set(newfile)
			newconf = process_source_file(newfile)[0]
			newconf = ConfigMaster().sanity(newconf, gui=1)
			# Restate all checkboxes after file selection
			#TODO how to make a refresh without killing it?
			self.root.destroy()
			self.__init__(newconf)
			self.mainwindow()
	
	def scrollwindow(self, txt='no text!', title=''):
		# Create components
		win    = Tkinter.Toplevel() ; win.title(title)
		frame  = Tkinter.Frame(win)
		scroll = Tkinter.Scrollbar(frame)
		text   = Tkinter.Text(frame,yscrollcommand=scroll.set)
		button = Tkinter.Button(win)
		# Config
		text.insert(Tkinter.END, string.join(txt,'\n'))
		scroll.config(command=text.yview)
		button.config(text=_('Close'), command=win.destroy)
		button.focus_set()
		# Packing
		text.pack(side='left', fill='both', expand=1)
		scroll.pack(side='right', fill='y')
		frame.pack(fill='both', expand=1)
		button.pack(ipadx=30)
	
	def runprogram(self):
		global CMDLINE_RAW
		# Prepare
		self.target_name2key()
		infile, target = self.infile.get(), self.target.get()
		# Sanity
		if not target:
			showwarning(my_name,_("You must select a target type!"))
			return
		if not infile:
			showwarning(my_name,
			   _("You must provide the source file location!"))
			return
		# Compose cmdline
		guiflags = []
		real_cmdline_conf = ConfigMaster(CMDLINE_RAW).parse()
		if real_cmdline_conf.has_key('infile'):
			del real_cmdline_conf['infile']
		if real_cmdline_conf.has_key('target'):
			del real_cmdline_conf['target']
		real_cmdline = CommandLine().compose_cmdline(real_cmdline_conf)
		default_outfile = ConfigMaster().get_outfile_name(
		     {'sourcefile':infile, 'outfile':'', 'target':target})
		for opt in self.checks:
			val = int(getattr(self, 'f_%s'%opt).get() or "0")
			if opt == 'stdout': opt = 'outfile'
			on_config  = self.conf.get(opt) or 0
			on_cmdline = real_cmdline_conf.get(opt) or 0
			if opt == 'outfile':
				if on_config  == STDOUT: on_config = 1
				else: on_config = 0
				if on_cmdline == STDOUT: on_cmdline = 1
				else: on_cmdline = 0
			if val != on_config or (
			  val == on_config == on_cmdline and
			  real_cmdline_conf.has_key(opt)):
				if val:
					# Was not set, but user selected on GUI
					Debug("user turned  ON: %s"%opt)
					if opt == 'outfile': opt = '-o-'
					else: opt = '--%s'%opt
				else:
					# Was set, but user deselected on GUI
					Debug("user turned OFF: %s"%opt)
					if opt == 'outfile':
						opt = "-o%s"%default_outfile
					else: opt = '--no-%s'%opt
				guiflags.append(opt)
		cmdline = [my_name, '-t', target] +real_cmdline \
		          +guiflags +[infile]
		Debug('Gui/Tk cmdline: %s'%cmdline,5)
		# Run!
		cmdline_raw_orig = CMDLINE_RAW
		try:
			# Fake the GUI cmdline as the real one, and parse file
			CMDLINE_RAW = CommandLine().get_raw_config(cmdline[1:])
			data = process_source_file(infile)
			# On GUI, convert_* returns the data, not finish_him()
			outlist, config = convert_this_files([data])
			# On GUI and STDOUT, finish_him() returns the data
			result = finish_him(outlist, config)
			# Show outlist in s a nice new window
			if result:
				outlist, config = result
				title = _('%s: %s converted to %s')%(
				  my_name, os.path.basename(infile),
				  string.upper(config['target']))
				self.scrollwindow(outlist, title)
			# Show the "file saved" message
			else:
				msg = "%s\n\n  %s\n%s\n\n  %s\n%s"%(
				      _('Conversion done!'),
				      _('FROM:'), infile,
				      _('TO:'), config['outfile'])
				showinfo(my_name, msg)
		except error:         # common error (windowed), not quit
			pass
		except:               # fatal error (windowed and printed)
			errormsg = getUnknownErrorMessage()
			print errormsg
			showerror(_('%s FATAL ERROR!')%my_name,errormsg)
			self.exit()
		CMDLINE_RAW = cmdline_raw_orig
	
	def mainwindow(self):
		self.infile.set(self.conf.get('sourcefile') or '')
		self.target.set(self.conf.get('target') or \
		              _('-- select one --'))
		outfile = self.conf.get('outfile')
		if outfile == STDOUT:                  # map -o-
			self.conf['stdout'] = 1
		if self.conf.get('headers') == None:
			self.conf['headers'] = 1       # map default
		
		action1 = _("Enter the source file location:")
		action2 = _("Choose the target document type:")
		action3 = _("Some options you may check:")
		action4 = _("Some extra options:")
		checks_txt = {
		  'headers'   : _("Include headers on output"),
		  'enum-title': _("Number titles (1, 1.1, 1.1.1, etc)"),
		  'toc'       : _("Do TOC also (Table of Contents)"),
		  'mask-email': _("Hide e-mails from SPAM robots"),
		
		  'toc-only'  : _("Just do TOC, nothing more"),
		  'stdout'    : _("Dump to screen (Don't save target file)")
		}
		targets_menu = map(lambda x: TARGET_NAMES[x], TARGETS)
		
		# Header
		self.label("%s %s"%(string.upper(my_name), my_version),
		     bg=self.bg2, fg=self.fg2).grid(columnspan=2, ipadx=10)
		self.label(_("ONE source, MULTI targets")+'\n%s\n'%my_url,
		     bg=self.bg1, fg=self.fg1).grid(columnspan=2)
		self.row = 2
		# Choose input file
		self.action(action1) ; self.frame_open()
		e_infile = self.entry(textvariable=self.infile,width=25)
		e_infile.grid(row=self.row, column=0, sticky='e')
		if not self.infile.get(): e_infile.focus_set()
		self.button(_("Browse"), self.askfile).grid(
		    row=self.row, column=1, sticky='w', padx=10)
		# Show outfile name, style and encoding (if any)
		txt = ''
		if outfile:
			txt = outfile
			if outfile == STDOUT: txt = _('<screen>')
			l_output = self.label(_('Output: ')+txt,
			                fg=self.fg2,bg=self.bg2)
			l_output.grid(columnspan=2, sticky='w')
		for setting in ['style','encoding']:
			if self.conf.get(setting):
				name = string.capitalize(setting)
				val  = self.conf[setting]
				self.label('%s: %s'%(name, val),
				     fg=self.fg2, bg=self.bg2).grid(
				     columnspan=2, sticky='w')
		# Choose target
		self.frame_close() ; self.action(action2)
		self.frame_open()
		self.target_key2name()
		self.menu(self.target_name, targets_menu).grid(
		     columnspan=2, sticky='w')
		# Options checkboxes label
		self.frame_close() ; self.action(action3)
		self.frame_open()
		# Compose options check boxes, example:
		# self.check(checks_txt['toc'],1,variable=self.f_toc)
		for check in self.checks:
			# Extra options label
			if check == 'toc-only':
				self.frame_close() ; self.action(action4)
				self.frame_open()
			txt = checks_txt[check]
			var = getattr(self, 'f_'+check)
			checked = self.conf.get(check)
			self.check(txt,checked,variable=var)
		self.frame_close()
		# Spacer and buttons
		self.label('').grid() ; self.row = self.row + 1
		b_quit = self.button(_("Quit"), self.exit)
		b_quit.grid(row=self.row, column=0, sticky='w', padx=30)
		b_conv = self.button(_("Convert!"), self.runprogram)
		b_conv.grid(row=self.row, column=1, sticky='e', padx=30)
		if self.target.get() and self.infile.get():
			b_conv.focus_set()
		
		# As documentation told me
		if sys.platform[:3] == 'win':
			self.root.iconify()
			self.root.update()
			self.root.deiconify()
		
		self.root.mainloop()


##############################################################################
##############################################################################

def exec_command_line(user_cmdline=[]):
	global CMDLINE_RAW, RC_RAW, DEBUG, VERBOSE, QUIET, GUI, Error
	
	# Extract command line data
	cmdline_data = user_cmdline or sys.argv[1:]
	CMDLINE_RAW = CommandLine().get_raw_config(cmdline_data, relative=1)
	cmdline_parsed = ConfigMaster(CMDLINE_RAW).parse()
	DEBUG   = cmdline_parsed.get('debug'  ) or 0
	VERBOSE = cmdline_parsed.get('verbose') or 0
	QUIET   = cmdline_parsed.get('quiet'  ) or 0
	GUI     = cmdline_parsed.get('gui'    ) or 0
	infiles = cmdline_parsed.get('infile' ) or []
	
	Message(_("Txt2tags %s processing begins")%my_version,1)
	
	# The easy ones
	if cmdline_parsed.get('help'   ): Quit(USAGE)
	if cmdline_parsed.get('version'): Quit(VERSIONSTR)
	
	# Multifile haters
	if len(infiles) > 1:
		errmsg=_("Option --%s can't be used with multiple input files")
		for option in NO_MULTI_INPUT:
			if cmdline_parsed.get(option):
				Error(errmsg%option)
	
	Debug("system platform: %s"%sys.platform)
	Debug("python version: %s"%(string.split(sys.version,'(')[0]))
	Debug("line break char: %s"%repr(LB))
	Debug("command line: %s"%sys.argv)
	Debug("command line raw config: %s"%CMDLINE_RAW,1)
	
	# Extract RC file config
	if cmdline_parsed.get('rc') == 0:
		Message(_("Ignoring user configuration file"),1)
	else:
		rc_file = get_rc_path()
		if os.path.isfile(rc_file):
			Message(_("Loading user configuration file"),1)
			RC_RAW = ConfigLines(file=rc_file).get_raw_config()
		
		Debug("rc file: %s"%rc_file)
		Debug("rc file raw config: %s"%RC_RAW,1)
	
	# Get all infiles config (if any)
	infiles_config = get_infiles_config(infiles)
	
	# Is GUI available?
	# Try to load and start GUI interface for --gui
	# If program was called with no arguments, try GUI also
	if GUI or not infiles:
		try:
			load_GUI_resources()
			Debug("GUI resources OK (Tk module is installed)")
			winbox = Gui()
			Debug("GUI display OK")
			GUI = 1
		except:
			Debug("GUI Error: no Tk module or no DISPLAY")
			GUI = 0
	
	# User forced --gui, but it's not available
	if cmdline_parsed.get('gui') and not GUI:
		print getTraceback(); print
		Error("Sorry, I can't run my Graphical Interface - GUI\n"
		      "- Check if Python Tcl/Tk module is installed (Tkinter)\n"
		      "- Make sure you are in a graphical environment (like X)")
	
	# Okay, we will use GUI
	if GUI:
		Message(_("We are on GUI interface"),1)
		
		# Redefine Error function to raise exception instead sys.exit()
		def Error(msg):
			showerror(_('txt2tags ERROR!'), msg)
			raise error
		
		# If no input file, get RC+cmdline config, else full config
		if not infiles:
			gui_conf = ConfigMaster(RC_RAW+CMDLINE_RAW).parse()
		else:
			try   : gui_conf = infiles_config[0][0]
			except: gui_conf = {}
		
		# Sanity is needed to set outfile and other things
		gui_conf = ConfigMaster().sanity(gui_conf, gui=1)
		Debug("GUI config: %s"%gui_conf,5)
		
		# Insert config and populate the nice window!
		winbox.load_config(gui_conf)
		winbox.mainwindow()
	
	# Console mode rocks forever!
	else:
		Message(_("We are on Command Line interface"),1)
		
		# Called with no arguments, show error
		if not infiles: Error(_('Missing input file (try --help)'))
		
		convert_this_files(infiles_config)
	
	Message(_("Txt2tags finished sucessfuly"),1)

if __name__ == '__main__':
	try:
		exec_command_line()
	except error, msg:
		sys.stderr.write("%s\n"%msg)
		sys.stderr.flush()
		sys.exit(1)
	except SystemExit:
		pass
	except:
		sys.stderr.write(getUnknownErrorMessage())
		sys.stderr.flush()
		sys.exit(1)
	Quit()


# vim: ts=8
