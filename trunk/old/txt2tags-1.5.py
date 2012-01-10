#!/usr/bin/env python
# txt2tags - generic text conversion tool
# http://txt2tags.sf.net
#
# Copyright 2001, 2002, 2003 Aurélio Marinho Jargas
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

# the code is better, even readable now, but needs more improvements

# TODO what if %!cmdline with syn error or wrong opts? and if on include?
# TODO headers. what is valid: date, !image, !link, !beautifiers, !structs
# TODO mgp: any line (header or not) can't begin with % (add a space before)

import re, string, os, sys, getopt, traceback
from time import strftime,time,localtime

my_url = 'http://txt2tags.sf.net'
my_email = 'verde@aurelio.net'
my_version = '1.5'

DEBUG = 0   # do not edit here, please use --debug
targets = ['txt', 'sgml', 'html', 'pm6', 'mgp', 'moin', 'man', 'tex']
FLAGS   = {'noheaders':0,'enumtitle':0 ,'maskemail':0 ,'stdout'  :0,
           'toconly'  :0,'toc'      :0 ,'gui'      :0 ,'included':0}
OPTIONS = {'toclevel' :3,'style'    :'','type'     :'','outfile' :'',
           'split':0, 'lang':''}
CONFIG_KEYWORDS = ['encoding', 'style', 'cmdline']
CONF = {}
regex = {}
TAGS = {}
rules = {}

currdate = strftime('%Y%m%d',localtime(time()))    # ISO current date
lang = 'english'
doctype = outfile = ''
STDIN = STDOUT = '-'

ESCCHAR = '\x00'

#my_version = my_version + '-beta0505'            # beta!
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

Usage: txt2tags -t <type> [OPTIONS] file.t2t

  -t, --type         set target document type. actually supported:
                     %s

  -o, --outfile=FILE set FILE as the output filename ('-' for STDOUT)   	  
      --stdout       same as '-o -' or '--outfile -' (deprecated option)
  -H, --noheaders    suppress header, title and footer information
  -n, --enumtitle    enumerate all title lines as 1, 1.1, 1.1.1, etc
      --maskemail    hide email from spam robots. x@y.z turns <x (a) y z>

      --toc          add TOC (Table of Contents) to target document
      --toconly      print document TOC and exit
      --toclevel=N   set maximum TOC level (deepness) to N

      --gui          invoke Graphical Tk Interface
      --style=FILE   use FILE as the document style (like Html CSS)

  -h, --help         print this help information and exit
  -V, --version      print program version and exit

Extra options for HTML target (needs sgml-tools):
      --split        split documents. values: 0, 1, 2 (default 0)
      --lang         document language (default english)

By default, converted output is saved to 'file.<type>'.
Use --outfile to force an output filename.
If input file is '-', reads from STDIN.
If outfile is '-', dumps output to STDOUT.\
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

  'tex': \
r"""\documentclass[11pt,a4paper]{article}
\usepackage{amsfonts,amssymb,graphicx,url}
\usepackage[%(ENCODING)s]{inputenc}  %% char encoding
\pagestyle{plain}   %% do page numbering ('empty' turns off)
\frenchspacing      %% no aditional spaces after periods
\setlength{\parskip}{8pt}\parindent=0pt  %% no paragraph indentation
%% uncomment next line for fancy PDF output on Adobe Acrobat Reader
%%\usepackage[pdfstartview=FitV,colorlinks=true,bookmarks=true]{hyperref}

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

def ParseConfig(text='',name='',kind=''):
	ret = {}
	if not text: return ret
	re_name = name or '[a-z]+'
	re_kind = kind or '[a-z]*'
	regex = re.compile("""
	  ^%%!\s*               # leading id with opt spaces
	  (?P<name>%s)          # config name 
	  (\((?P<kind>%s)\))?   # optional config kind inside ()
	  \s*:\s*               # key:value delimiter with opt spaces
	  (?P<value>.+?)        # config value
	  \s*$                  # rstrip() spaces and hit EOL
	  """%(re_name,re_kind), re.I+re.VERBOSE)
	match = regex.match(text)
	if match: ret = {
	  'name' :string.lower(match.group('name') or ''),
	  'kind' :string.lower(match.group('kind') or ''),
	  'value':match.group('value') }
	return ret


class Cmdline:
	def __init__(self, cmdline=[]):
		self.conf = {}
		self.cmdline = cmdline
		self.cmdline_conf = {}
		self.dft_options = OPTIONS
		self.dft_flags   = FLAGS
		self.all_options = self.dft_options.keys()
		self.all_flags   = self.dft_flags.keys()
		self.defaults = self._get_empty_conf()
		if cmdline: self.parse()
	
	#TODO protect quotes contents
	def _tokenize(self, cmd_string):
		return string.split(cmd_string)
	
	def parse(self):
		"return a dic with all options:value found"
		if not self.cmdline: return {}
		Debug("cmdline: %s"%self.cmdline, 1)
		options = {'infile': '', 'infiles':''}
		# compose valid options list
		longopts = ['help','version'] + self.all_flags + \
		           map(lambda x:x+'=', self.all_options) # add =
		cmdline = self.cmdline[1:]           # del prog name  
		# get cmdline options
		try: (opt, args) = getopt.getopt(cmdline, 'hVnHt:o:', longopts)
		except getopt.GetoptError:
			Error('Bad option or missing argument (try --help)')
		# get infile, if any
		if args:
			options['infile'] = args[0]
			options['infiles'] = args  # multi
		# parse all options
		for name,val in opt:
			if   name in ['-h','--help'   ]: Quit(usage)
			elif name in ['-V','--version']: Quit(versionstr)
			elif name in ['-t','--type'     ]: options['type'] = val
			elif name in ['-o','--outfile'  ]: options['outfile'] = val
			elif name in ['-n','--enumtitle']: options['enumtitle'] = 1
			elif name in ['-H','--noheaders']: options['noheaders'] = 1
			else: options[name[2:]] = val  # del --
		# save results
		Debug("cmdline arguments: %s"%options, 1)
		self.cmdline_conf = options
	
	def compose(self, conf):
		"compose cmdline from CONF dict"
		#TODO if toconly, del noheaders, del toc, del toclevel
		args = []
		if conf.has_key('type'):     # the first
			args.extend(['-t', conf['type']]) ; 
			del conf[type]
		for key in conf.keys():
			if key in ['infile','infiles']: continue
			args.extend(['--'+key, conf[key]])
		if conf.has_key('infiles'):  # the last
			args.extend(conf['infiles'])
		return string.join(args, ' ')
	
	def merge(self, extraopts=''):
		"insert cmdline portion BEFORE current cmdline"
		if not extraopts: return
		if type(extraopts) == type(''):
			extraopts = self._tokenize(extraopts)
		if not self.cmdline: self.cmdline = extraopts
		else: self.cmdline = ['t2t-merged'] +extraopts +self.cmdline[1:]
		self.parse()
	
	def _get_outfile_name(self, conf):
		"dirname is the same for {in,out}file"
		infile = conf['infile']
		if not infile: return ''
		if infile == STDIN or conf['stdout']:
			outfile = STDOUT
		else:
			basename = re.sub('\.(txt|t2t)$','',infile)
			outfile = "%s.%s"%(basename, conf['type'])
		Debug(" infile: '%s'"%infile , 1)
		Debug("outfile: '%s'"%outfile, 1)
		return outfile
	
	def _sanity(self, dic):
		"basic cmdline syntax checkings"
		if not dic: return {}
		if not dic['infile'] or not dic['type']:
			Quit(usage, 1)                  # no filename/doctype
		if not targets.count(dic['type']):      # check target
			Error("Invalid document type '%s' (try --help)"%(
			       dic['type']))
		if len(dic['infiles']) > 1 and dic['outfile']: # -o FILE *.t2t
			Error("--outfile can't be used with multiple files")
		for opt in self.all_options:            # check numeric options
			opttype = type(self.dft_options[opt])
			if dic.get(opt) and opttype == type(9):
				try: dic[opt] = int(dic.get(opt)) # save
				except: Error('--%s value must be a number'%opt)
		if dic['split'] not in [0,1,2]:         # check split level
			Error('Option --split must be 0, 1 or 2')
		return dic
	
	def merge_conf(self, newconfs={}):
		"include Config Area settings into self.conf"
		if not self.conf: self.get_conf()
		if not newconfs: return self.conf
		for key in newconfs.keys():
			if key == 'cmdline': continue   # already done
			# just update if still 'virgin'
			if self.conf.has_key(key) and \
			   self.conf[key] == self.defaults[key]:
				self.conf[key] = newconfs[key]
			# add new
			if not self.conf.has_key(key):
				self.conf[key] = newconfs[key]
		
		Debug("Merged CONF: %s"%self.conf, 1)
		return self.conf
	
	def _get_empty_conf(self):
		econf = self.dft_options.copy()
		for k in self.dft_flags.keys(): econf[k] = self.dft_flags[k]
		return econf
	
	def get_conf(self):
		"set vars and flags according to options dic"
		if not self.cmdline_conf:
			if not self.cmdline: return {}
			self.parse()
		dic = self.cmdline_conf
		conf = self.defaults.copy()
		
		## store flags & options
		for flag in self.all_flags:
			if dic.has_key(flag): conf[flag] = 1
		for opt in self.all_options + ['infile', 'infiles']:
			if dic.has_key(opt): conf[opt] = dic.get(opt)
		
		if not conf['type'] and conf['toconly']: conf['type'] = 'txt'
		conf = self._sanity(conf)
		
		## some gotchas for specific issues
		doctype = conf['type']
		infile = conf['infile']
		
		# toconly is stronger than others
		if conf['toconly']:
			conf['noheaders'] = 1
			conf['stdout'] = 1
			conf['toc'] = 0
			conf['split'] = 0
			conf['toclevel'] = self.dft_options['toclevel']
		
		# split: just HTML, no stdout, 1st do a sgml, then sgml2html
		if conf['split']:
			if doctype != 'html': conf['split'] = 0
			else: conf['stdout'] = 0 ; conf['type'] = 'sgml' 
		
		outfile = conf['outfile'] or self._get_outfile_name(conf)
		
		# final checkings
		if conf['split'] and outfile == STDOUT:
			Error('--split: You must provide a FILE (not STDIN)')
		if infile == outfile and outfile != STDOUT:
			Error("SUICIDE WARNING!!!  (see --outfile)\n  source"+\
			      " and target files has the same name: "+outfile)
		### author's note: "yes, i've got my sample.t2t file deleted
		### before add this test... :/"
		
		conf['outfile'] = outfile
		conf['cmdline'] = self.cmdline
		Debug("CONF data: %s\n"%conf, 1)
		self.conf = conf
		return self.conf
#		
### End of Cmdline class




class Proprierties:
	def __init__(self, filename=''):
		self.buffer = ['']   # text start at pos 1
		self.areas = ['head','conf','body']
		self.arearef = []
		self.headers = ['','','']
		self.config = self.get_empty_config()
		self.lastline = 0
		self.filename = filename
		self.conflines = []
		self.bodylines = []
		if filename:
			self.read_file(filename)
			self.find_areas()
			self.set_headers()
			self.set_config()
	
	def read_file(self, file):
		lines = Readfile(file)
		if not lines: Error('Empty file! %s'%file)
		self.buffer.extend(lines)
	
	def get_empty_config(self):
		empty = {}
		for key in CONFIG_KEYWORDS: empty[key] = ''
		return empty
	
	def find_areas(self):
		"Run through buffer and identify head/conf/body areas"
		buf = self.buffer ; ref = [1,4,0]       # defaults
		if not string.strip(buf[1]):            # no header
			ref[0] = 0 ; ref[1] = 2
		for i in range(ref[1],len(buf)):        # find body init
			if string.strip(buf[i]) and buf[i][0] != '%':
				ref[2] = i ; break      # !blank, !comment
			if ParseConfig(buf[i], 'include', 'verb|body|'):
				ref[2] = i ; break      # %!include
		if ref[1] == ref[2]: ref[1] = 0         # no conf area
		for i in 0,1,2:                         # del !existent
			if not ref[i]: self.areas[i] = ''
		self.arearef = ref                      # save results
		self.lastline = len(self.buffer)-1
		Debug('Head,Conf,Body start line: %s'%ref, 1)
		# store CONF and BODY lines found
		cfgend = ref[2] or len(buf)
		self.conflines = buf[ref[1]:cfgend]
		if ref[2]: self.bodylines = buf[ref[2]:]
	
	
	def set_headers(self):
		"Extract and save headers contents"
		if not self.arearef: self.find_areas()
		if not self.areas.count('head'): return
		if self.lastline < 3:
			#TODO on gui this checking is !working
			Error(
			"Premature end of Headers on '%s'."%self.filename +\
			'\n\nFile has %s line(s), but '%self.lastline     +\
			'Headers should be composed by 3 lines. '         +\
			'\nMaybe you should left the first line blank? '  +\
			'(for no headers)')
		for i in 0,1,2:
			self.headers[i] = string.strip(self.buffer[i+1])
		Debug("Headers found: %s"%self.headers, 1, i+1)
	
	def set_config(self):
		"Extract and save config contents (including includes)"
		if not self.arearef: self.find_areas()
		if not self.areas.count('conf'): return
		keywords = string.join(CONFIG_KEYWORDS, '|')
		linenr = self.arearef[1]  # for debug messages
		for line in self.conflines:
			linenr = linenr + 1
			if len(line) < 3: continue
			if line[:2] != '%!': continue
			cfg = ParseConfig(line, name=keywords)
			if not cfg:
				Debug('Bogus Config Line',1,linenr)
				continue
			key, val = cfg['name'], cfg['value']
			self.config[key] = val
			Debug("Found config '%s', value '%s'"%(
			       key,val),1,linenr)


def get_file_body(file):
	"Returns all the document BODY lines (including includes)"
	prop = Proprierties()
	prop.read_file(file)
	prop.find_areas()
	return prop.bodylines


def finish_him(outlist, CONF):
	"Writing output to screen or file"
	outfile = CONF['outfile']
	outlist = unmaskEscapeChar(outlist)
	if outfile == STDOUT:
		for line in outlist: print line
	else:
		Savefile(outfile, addLineBreaks(outlist))
		if not CONF['gui']: print 'wrote %s'%(outfile)
	
	if CONF['split']:
		print "--- html..."
		sgml2html = 'sgml2html -s %s -l %s %s'%(
		            CONF['split'],CONF['lang'] or lang,outfile)
		print "Running system command:", sgml2html
		os.system(sgml2html)


def toc_maker(toc, conf):
	"Compose TOC list 'by hand'"
	# TOC is a tag, so there's nothing to do here
	if TAGS['TOC']: return []
	# toc is a valid t2t marked text (list type), that is converted
	if conf['toc'] or conf['toconly']:
		fakeconf = conf.copy()
		fakeconf['noheaders'] = 1
		fakeconf['toconly']   = 0
		fakeconf['maskemail'] = 0
		toc,foo = convert(toc, fakeconf)
	# TOC between bars (not for --toconly)
	if conf['toc']:
		para = TAGS['paragraph']
		tocbar = [para, regex['x'].sub('-'*72,TAGS['bar1']), para]
		toc = tocbar + toc + tocbar
	return toc


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
	'anchor','comment','TOC',
	'EOD'
	]
	
	alltags = {
	
	'txt': {
	   'title1'              : '  \a'      ,
	   'title2'              : '\t\a'      ,
	   'title3'              : '\t\t\a'    ,
	   'title4'              : '\t\t\t\a'  ,
	   'title5'              : '\t\t\t\t\a',
	   'areaQuoteOpen'       : '    '      ,
	   'listItem'            : '- '        ,
	   'numlistItem'         : '\a. '      ,
	   'bar1'                : '\a'        ,
	   'bar2'                : '\a'        ,
	   'url'                 : '\a'        ,
	   'urlMark'             : '\a (\a)'   ,
	   'email'               : '\a'        ,
	   'emailMark'           : '\a (\a)'   ,
	   'img'                 : '[\a]'      ,
	},
	
	'html': {
	   'paragraph'           : '<P>'            ,
	   'title1'              : '<H1>\a</H1>'    ,
	   'title2'              : '<H2>\a</H2>'    ,
	   'title3'              : '<H3>\a</H3>'    ,
	   'title4'              : '<H4>\a</H4>'    ,
	   'title5'              : '<H5>\a</H5>'    ,
	   'areaPreOpen'         : '<PRE>'          ,
	   'areaPreClose'        : '</PRE>'         ,
	   'areaQuoteOpen'       : '<BLOCKQUOTE>'   ,
	   'areaQuoteClose'      : '</BLOCKQUOTE>'  ,
	   'fontMonoOpen'        : '<CODE>'         ,
	   'fontMonoClose'       : '</CODE>'        ,
	   'fontBoldOpen'        : '<B>'            ,
	   'fontBoldClose'       : '</B>'           ,
	   'fontItalicOpen'      : '<I>'            ,
	   'fontItalicClose'     : '</I>'           ,
	   'fontBolditalicOpen'  : '<B><I>'         ,
	   'fontBolditalicClose' : '</I></B>'       ,
	   'fontUnderlineOpen'   : '<U>'            ,
	   'fontUnderlineClose'  : '</U>'           ,
	   'listOpen'            : '<UL>'           ,
	   'listClose'           : '</UL>'          ,
	   'listItem'            : '<LI>'           ,
	   'numlistOpen'         : '<OL>'           ,
	   'numlistClose'        : '</OL>'          ,
	   'numlistItem'         : '<LI>'           ,
	   'deflistOpen'         : '<DL>'           ,
	   'deflistClose'        : '</DL>'          ,
	   'deflistItem1'        : '<DT>\a</DT>'    ,
	   'deflistItem2'        : '<DD>'           ,
	   'bar1'                : '<HR NOSHADE SIZE=1>'        ,
	   'bar2'                : '<HR NOSHADE SIZE=5>'        ,
	   'url'                 : '<A HREF="\a">\a</A>'        ,
	   'urlMark'             : '<A HREF="\a">\a</A>'        ,
	   'email'               : '<A HREF="mailto:\a">\a</A>' ,
	   'emailMark'           : '<A HREF="mailto:\a">\a</A>' ,
	   'img'                 : '<IMG ALIGN="\a" SRC="\a" BORDER="0">',
	   'imgsolo'             : '<P ALIGN="center">\a</P>'   ,
	   'tableOpen'           : '<table\a cellpadding=4 border=\a>',
	   'tableClose'          : '</table>'       ,
	   'tableLineOpen'       : '<tr>'           ,
	   'tableLineClose'      : '</tr>'          ,
	   'tableCellOpen'       : '<td\a>'         ,
	   'tableCellClose'      : '</td>'          ,
	   'tableTitleCellOpen'  : '<th>'           ,
	   'tableTitleCellClose' : '</th>'          ,
	   'tableAlignLeft'      : ''               ,
	   'tableAlignCenter'    : ' align="center"',
	   'tableCellAlignLeft'  : ''               ,
	   'tableCellAlignRight' : ' align="right"' ,
	   'tableCellAlignCenter': ' align="center"',
	   'anchor'              : '<a name="\a">'  ,
	   'comment'             : '<!-- \a -->'    ,
	   'EOD'                 : '</BODY></HTML>'
	},
	
	'sgml': {
	   'paragraph'           : '<p>'                ,
	   'title1'              : '<sect>\a<p>'        ,
	   'title2'              : '<sect1>\a<p>'       ,
	   'title3'              : '<sect2>\a<p>'       ,
	   'title4'              : '<sect3>\a<p>'       ,
	   'title5'              : '<sect4>\a<p>'       ,
	   'areaPreOpen'         : '<tscreen><verb>'    ,
	   'areaPreClose'        : '</verb></tscreen>'  ,
	   'areaQuoteOpen'       : '<quote>'            ,
	   'areaQuoteClose'      : '</quote>'           ,
	   'fontMonoOpen'        : '<tt>'               ,
	   'fontMonoClose'       : '</tt>'              ,
	   'fontBoldOpen'        : '<bf>'               ,
	   'fontBoldClose'       : '</bf>'              ,
	   'fontItalicOpen'      : '<em>'               ,
	   'fontItalicClose'     : '</em>'              ,
	   'fontBolditalicOpen'  : '<bf><em>'           ,
	   'fontBolditalicClose' : '</em></bf>'         ,
	   'fontUnderlineOpen'   : '<bf><em>'           ,
	   'fontUnderlineClose'  : '</em></bf>'         ,
	   'listOpen'            : '<itemize>'          ,
	   'listClose'           : '</itemize>'         ,
	   'listItem'            : '<item>'             ,
	   'numlistOpen'         : '<enum>'             ,
	   'numlistClose'        : '</enum>'            ,
	   'numlistItem'         : '<item>'             ,
	   'deflistOpen'         : '<descrip>'          ,
	   'deflistClose'        : '</descrip>'         ,
	   'deflistItem1'        : '<tag>\a</tag>'      ,
	   'bar1'                : '<!-- \a -->'        ,
	   'bar2'                : '<!-- \a -->'        ,
	   'url'                 : '<htmlurl url="\a" name="\a">'        ,
	   'urlMark'             : '<htmlurl url="\a" name="\a">'        ,
	   'email'               : '<htmlurl url="mailto:\a" name="\a">' ,
	   'emailMark'           : '<htmlurl url="mailto:\a" name="\a">' ,
	   'img'                 : '<figure><ph vspace=""><img src="\a">'+\
	                           '</figure>'                           ,
	   'tableOpen'           : '<table><tabular ca="\a">'            ,
	   'tableClose'          : '</tabular></table>' ,
	   'tableLineClose'      : '<rowsep>'           ,
	   'tableCellClose'      : '<colsep>'           ,
	   'tableTitleCellClose' : '<colsep>'           ,
	   'tableColAlignLeft'   : 'l'                  ,
	   'tableColAlignRight'  : 'r'                  ,
	   'tableColAlignCenter' : 'c'                  ,
	   'comment'             : '<!-- \a -->'        ,
	   'TOC'                 : '<toc>'              ,
	   'EOD'                 : '</article>'
	},
	   
	'tex': {
	   'title1'              : '\n\\newpage\section{\a}',
	   'title2'              : '\\subsection{\a}'       ,
	   'title3'              : '\\subsubsection{\a}'    ,
	   # title 4/5: DIRTY: para+BF+\\+\n
	   'title4'              : '\\paragraph{}\\textbf{\a}\\\\\n',
	   'title5'              : '\\paragraph{}\\textbf{\a}\\\\\n',
	   'areaPreOpen'         : '\\begin{verbatim}'   ,
	   'areaPreClose'        : '\\end{verbatim}'     ,
	   'areaQuoteOpen'       : '\\begin{quotation}'  ,
	   'areaQuoteClose'      : '\\end{quotation}'    ,
	   'fontMonoOpen'        : '\\texttt{'           ,
	   'fontMonoClose'       : '}'                   ,
	   'fontBoldOpen'        : '\\textbf{'           ,
	   'fontBoldClose'       : '}'                   ,
	   'fontItalicOpen'      : '\\textit{'           ,
	   'fontItalicClose'     : '}'                   ,
	   'fontBolditalicOpen'  : '\\textbf{\\textit{'  ,
	   'fontBolditalicClose' : '}}'                  ,
	   'fontUnderlineOpen'   : '\\underline{'        ,
	   'fontUnderlineClose'  : '}'                   ,
	   'listOpen'            : '\\begin{itemize}'    ,
	   'listClose'           : '\\end{itemize}'      ,
	   'listItem'            : '\\item '             ,
	   'numlistOpen'         : '\\begin{enumerate}'  ,
	   'numlistClose'        : '\\end{enumerate}'    ,
	   'numlistItem'         : '\\item '             ,
	   'deflistOpen'         : '\\begin{description}',
	   'deflistClose'        : '\\end{description}'  ,
	   'deflistItem1'        : '\\item[\a]'          ,
	   'bar1'                : '\n\\hrulefill{}\n'   ,
	   'bar2'                : '\n\\rule{\linewidth}{1mm}\n',
	   'url'                 : '\\url{\a}'                  ,
	   'urlMark'             : '\\textit{\a} (\\url{\a})'   ,
	   'email'               : '\\url{\a}'                  ,
	   'emailMark'           : '\\textit{\a} (\\url{\a})'   ,
	   'img'                 : '\\begin{figure}\\includegraphics{\a}'+\
	                           '\\end{figure}',
	   'tableOpen'           : '\\begin{center}\\begin{tabular}{\a|}',
	   'tableClose'          : '\\end{tabular}\\end{center}',
	   'tableLineOpen'       : '\\hline ' ,
	   'tableLineClose'      : ' \\\\'    ,
	   'tableCellClose'      : ' & '      ,
	   'tableTitleCellOpen'  : '\\textbf{',
	   'tableTitleCellClose' : '} & '     ,
	   'tableColAlignLeft'   : '|l'       ,
	   'tableColAlignRight'  : '|r'       ,
	   'tableColAlignCenter' : '|c'       ,
	   'comment'             : '% \a'     ,
	   'TOC'                 : '\\newpage\\tableofcontents',
	   'EOD'                 : '\\end{document}'
	},
	
	'moin': {
	   'title1'              : '= \a ='        ,
	   'title2'              : '== \a =='      ,
	   'title3'              : '=== \a ==='    ,
	   'title4'              : '==== \a ===='  ,
	   'title5'              : '===== \a =====',
	   'areaPreOpen'         : '{{{'           ,
	   'areaPreClose'        : '}}}'           ,
	   'areaQuoteOpen'       : ' '             ,
	   'fontMonoOpen'        : '{{{'           ,
	   'fontMonoClose'       : '}}}'           ,
	   'fontBoldOpen'        : "'''"           ,
	   'fontBoldClose'       : "'''"           ,
	   'fontItalicOpen'      : "''"            ,
	   'fontItalicClose'     : "''"            ,
	   'fontBolditalicOpen'  : "'''''"         ,
	   'fontBolditalicClose' : "'''''"         ,
	   'fontUnderlineOpen'   : "'''''"         ,
	   'fontUnderlineClose'  : "'''''"         ,
	   'listItem'            : '* '            ,
	   'numlistItem'         : '\a. '          ,
	   'bar1'                : '----'          ,
	   'bar2'                : '----'          ,
	   'url'                 : '[\a]'          ,
	   'urlMark'             : '[\a \a]'       ,
	   'email'               : '[\a]'          ,
	   'emailMark'           : '[\a \a]'       ,
	   'img'                 : '[\a]'          ,
	   'tableLineOpen'       : '||'            ,
	   'tableCellClose'      : '||'            ,
	   'tableTitleCellClose' : '||'
	},
	
	'mgp': {
	   'paragraph'           : '%font "normal", size 5\n'   ,
	   'title1'              : '%page\n\n\a'                ,
	   'title2'              : '%page\n\n\a'                ,
	   'title3'              : '%page\n\n\a'                ,
	   'title4'              : '%page\n\n\a'                ,
	   'title5'              : '%page\n\n\a'                ,
	   'areaPreOpen'         : '\n%font "mono"'             ,
	   'areaPreClose'        : '%font "normal"'             ,
	   'areaQuoteOpen'       : '%prefix "       "'          ,
	   'areaQuoteClose'      : '%prefix "  "'               ,
	   'fontMonoOpen'        : '\n%cont, font "mono"\n'     ,
	   'fontMonoClose'       : '\n%cont, font "normal"\n'   ,
	   'fontBoldOpen'        : '\n%cont, font "normal-b"\n' ,
	   'fontBoldClose'       : '\n%cont, font "normal"\n'   ,
	   'fontItalicOpen'      : '\n%cont, font "normal-i"\n' ,
	   'fontItalicClose'     : '\n%cont, font "normal"\n'   ,
	   'fontBolditalicOpen'  : '\n%cont, font "normal-bi"\n',
	   'fontBolditalicClose' : '\n%cont, font "normal"\n'   ,
	   'fontUnderlineOpen'   : '\n%cont, fore "cyan"\n'     ,
	   'fontUnderlineClose'  : '\n%cont, fore "white"\n'    ,
	   'numlistItem'         : '\a. '                       ,
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
	   'img'                 : '\n%center\n%newimage "\a", left\n',
	   'comment'             : '%% \a'                      ,
	   'EOD'                 : '%%EOD'
	},
	
	'man': {
	   'paragraph'           : '.P'     ,
	   'title1'              : '.SH \a' ,
	   'title2'              : '.SS \a' ,
	   'title3'              : '.SS \a' ,
	   'title4'              : '.SS \a' ,
	   'title5'              : '.SS \a' ,
	   'areaPreOpen'         : '.nf'    ,
	   'areaPreClose'        : '.fi\n'  ,
	   'areaQuoteOpen'       : '\n'     ,
	   'areaQuoteClose'      : '\n'     ,
	   'fontBoldOpen'        : '\\fB'   ,
	   'fontBoldClose'       : '\\fP'   ,
	   'fontItalicOpen'      : '\\fI'   ,
	   'fontItalicClose'     : '\\fP'   ,
	   'fontBolditalicOpen'  : '\n.BI ' ,
	   'fontBolditalicClose' : '\n\\&'  ,
	   'listOpen'            : '\n.nf'  ,  # pre
	   'listClose'           : '.fi\n'  ,
	   'listItem'            : '* '     ,
	   'numlistOpen'         : '\n.nf'  ,  # pre
	   'numlistClose'        : '.fi\n'  ,
	   'numlistItem'         : '\a. '   ,
	   'bar1'                : '\n\n'   ,
	   'bar2'                : '\n\n'   ,
	   'url'                 : '\a'     ,
	   'urlMark'             : '\a (\a)',
	   'email'               : '\a'     ,
	   'emailMark'           : '\a (\a)',
	   'img'                 : '\a'     ,
	   'comment'             : '.\\" \a'
	},
	
	'pm6': {
	   'paragraph'           : '<@Normal:>'    ,
	   'title1'              : '\n<@Title1:>\a',
	   'title2'              : '\n<@Title2:>\a',
	   'title3'              : '\n<@Title3:>\a',
	   'title4'              : '\n<@Title4:>\a',
	   'title5'              : '\n<@Title5:>\a',
	   'areaPreOpen'         : '<@PreFormat:>' ,
	   'areaQuoteOpen'       : '<@Quote:>'     ,
	   'fontMonoOpen'        : '<FONT "Lucida Console"><SIZE 9>' ,
	   'fontMonoClose'       : '<SIZE$><FONT$>',
	   'fontBoldOpen'        : '<B>'           ,
	   'fontBoldClose'       : '<P>'           ,
	   'fontItalicOpen'      : '<I>'           ,
	   'fontItalicClose'     : '<P>'           ,
	   'fontBolditalicOpen'  : '<B><I>'        ,
	   'fontBolditalicClose' : '<P>'           ,
	   'fontUnderlineOpen'   : '<U>'           ,
	   'fontUnderlineClose'  : '<P>'           ,
	   'listOpen'            : '<@Bullet:>'    ,
	   'listItem'            : '\x95	'       ,  # \x95 == ~U
	   'numlistOpen'         : '<@Bullet:>'    ,
	   'numlistItem'         : '\x95    '      ,
	   'bar1'                : '\a'            ,
	   'bar2'                : '\a'            ,
	   'url'                 : '<U>\a<P>'      ,  # underline
	   'urlMark'             : '\a <U>\a<P>'   ,
	   'email'               : '\a'            ,
	   'emailMark'           : '\a \a'         ,
	   'img'                 : '\a'
	}
	}
	
	# compose the target tags dictionary
	tags = {}
	target_tags = alltags[doctype]
	for key in keys: tags[key] = ''     # create empty keys
	for key in target_tags.keys():
		tags[key] = maskEscapeChar(target_tags[key]) # populate
	
	return tags


def getRules(doctype):
	ret = {}
	allrules = [
	
	 # target rules (ON/OFF)
	  'linkable',           # target supports external links
	  'tableable',          # target supports tables
	  'imglinkable',        # target supports images as links
	  'imgalignable',       # target supports image alignment
	  'imgasdefterm',       # target supports image as definition term
	  'tablealignable',     # target supports table alignment
	  'listcountable',      # target supports numbered lists natively
	  'tablecellsplit',     # place delimiters only *between* cells
	  'listnotnested',      # lists cannot be nested
	  'quotenotnested',     # quotes cannot be nested
	  'preareanotescaped',  # don't escape specials in PRE area
	  'escapeurl',          # escape special in link URL
	  
	# target code beautify (ON/OFF)
	  'indentprearea',      # add leading spaces to PRE area lines
	  'breaktablecell',     # break lines after any table cell
	  'breaktablelineopen', # break line after opening table line
	  'keepquoteindent',    # don't remove the leading TABs on quotes
	
	# value settings
	  'listmaxdepth',       # maximum depth for lists
	  'tablecellaligntype'  # type of table cell align: cell, column
	]
	
	rules = {
	  'txt' : {
	    'indentprearea':1
	    },
	  'html': {
	    'indentprearea':1,
	    'linkable':1,
	    'imglinkable':1,
	    'imgalignable':1,
	    'imgasdefterm':1,
	    'listcountable':1,
	    'tableable':1,
	    'breaktablecell':1,
	    'breaktablelineopen':1,
	    'keepquoteindent':1,
	    'tablealignable':1,
	    'tablecellaligntype':'cell'
	    },
	  'sgml': {
	    'linkable':1,
	    'escapeurl':1,
	    'listcountable':1,
	    'tableable':1,
	    'tablecellsplit':1,
	    'quotenotnested':1,
	    'keepquoteindent':1,
	    'tablecellaligntype':'column'
	    },
	  'mgp' : {
	    },
	  'tex' : {
	    'listcountable':1,
	    'tableable':1,
	    'tablecellsplit':1,
	    'preareanotescaped':1,
	    'listmaxdepth':4,
	    'tablecellaligntype':'column'
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
		re.compile(r'^\s*(?P<tag>={1,5})(?P<txt>[^=].*[^=])\1\s*$'),
	'areaPreOpen':
		re.compile(r'^---$'),
	'areaPreClose':
		re.compile(r'^---$'),
	'quote':
		re.compile(r'^\t+'),
	'1linePre':
#		re.compile(r'^--- '),
		re.compile(r'^--- (?=.)'),
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
		re.compile(r'^ *\|\|? '),
	'blankline':
		re.compile(r'^\s*$'),
	'comment':
		re.compile(r'^%'),
	'raw':
		re.compile(r'``(.+?)``')
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
	  'guess' : r'(www[23]?|ftp)\.',    # w/out proto, try to guess
	  'login' : r'A-Za-z0-9_.-',        # for ftp://login@domain.com
	  'pass'  : r'[^ @]*',              # for ftp://login:password@dom.com
	  'chars' : r'A-Za-z0-9%._/~:,=$@-',# %20(space), :80(port)
	  'anchor': r'A-Za-z0-9%._-',       # %nn(encoded)
	  'form'  : r'A-Za-z0-9/%&=+.,@*_-',# .,@*_-(as is)
	  'punct' : r'.,;:!?'
	}
	
	# username [ :password ] @
	patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
	
	# [ http:// ] [ username:password@ ] domain.com [ / ]
	#     [ #anchor | ?form=data ]
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
	
	# special things
	regex['special'] = re.compile(r'^%!\s*')
	regex['command'] = re.compile(r'(Include)\s*:\s*(.+)\s*$',re.I)
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

def doHeader(headers, CONF):
	if CONF['noheaders']: return []
	doctype = CONF['type']
	if not HEADER_TEMPLATE.has_key(doctype):
		Error("doheader: Unknow doctype '%s'"%doctype)
	
	template = string.split(HEADER_TEMPLATE[doctype], '\n')
	
	head_data = {'STYLE':'', 'ENCODING':''}
	for key in head_data.keys():
		val = CONF.get(string.lower(key))
		if key == 'ENCODING': val = get_encoding_string(val, doctype)
		head_data[key] = val
	# parse header contents
	for i in 0,1,2:
		contents = doDateMacro(headers[i])  # expand %%date
		# Escapes - on tex, just do it if any \tag{} present
		if doctype != 'tex' or \
		  (doctype == 'tex' and re.search(r'\\\w+{', contents)):
			contents = doEscape(doctype, contents)
		
		head_data['HEADER%d'%(i+1)] = contents
	Debug("Header Data: %s"%head_data, 1)
	# scan for empty dictionary keys
	# if found, scan template lines for that key reference
	# if found, remove the reference
	# if there isn't any other key reference on the same line, remove it
	for key in head_data.keys():
		if head_data.get(key): continue
		for line in template:
			if string.count(line, '%%(%s)s'%key):
				sline = string.replace(line, '%%(%s)s'%key, '')
				if not re.search(r'%\([A-Z0-9]+\)s', sline):
					template.remove(line)
	# populate template with data
	template = string.join(template, '\n') % head_data
	### post processing
	#
	# let tex format today
	if doctype == 'tex' and head_data['HEADER3'] == currdate:
		template = re.sub(r'\\date\{.*?}', r'\date', template)
	
	return string.split(template, '\n')

def doDateMacro(line):
	re_date = getRegexes()['date']
	while re_date.search(line):
		m = re_date.search(line)
		fmt = m.group('fmt') or ''
		dateme = currdate
		if fmt: dateme = strftime(fmt,localtime(time()))
		line = re_date.sub(dateme,line,1)
	return line

def doCommentLine(doctype,txt):
	# the -- string ends a sgml comment :(
	if doctype == 'sgml':
		txt = string.replace(txt, '--', '\\-\\-')
	
	if TAGS['comment']:
		return regex['x'].sub(txt, TAGS['comment'])
	return ''

def doFooter(CONF):
	ret = []
	doctype = CONF['type']
	cmdline = CONF['cmdline']
	typename = doctype
	if doctype == 'tex': typename = 'LaTeX2e'
	ppgd = '%s code generated by txt2tags %s (%s)'%(
	        typename,my_version,my_url)
	cmdline = 'cmdline: txt2tags %s'%string.join(cmdline[1:], ' ')
	ret.append('\n'+doCommentLine(doctype,ppgd))
	ret.append(doCommentLine(doctype,cmdline))
	ret.append(TAGS['EOD'])
	return ret

def doEscape(doctype,txt):
	if doctype in ['html','sgml']:
		txt = re.sub('&','&amp;',txt)
		txt = re.sub('<','&lt;',txt)
		txt = re.sub('>','&gt;',txt)
		if doctype == 'sgml':
			txt = re.sub('\xff','&yuml;',txt)  # "+y
	elif doctype == 'pm6':
		txt = re.sub('<','<\#60>',txt)
	elif doctype == 'mgp':
		txt = re.sub('^%',' %',txt)  # add leading blank to avoid parse
	elif doctype == 'man':
		txt = re.sub('^\.', ' .',txt) # command ID
		txt = doEscapeEscapechar(txt)
	elif doctype == 'tex':
		txt = string.replace(txt, ESCCHAR, maskEscapeChar(r'\verb!\!'))
		txt = string.replace(txt, '~', maskEscapeChar(r'\verb!~!'))
		txt = string.replace(txt, '^', maskEscapeChar(r'\verb!^!'))
		txt = re.sub('([#$&%{}])', r'\\\1', txt)
		# TIP the _ is escaped at the end
	return txt

def doFinalEscape(doctype, txt):
	"Last escapes of each line"
	if   doctype == 'pm6' : txt = string.replace(txt,ESCCHAR+'<',r'<\#92><')
	elif doctype == 'man' : txt = string.replace(txt, '-', r'\-')
	elif doctype == 'tex' : txt = string.replace(txt, '_', r'\_')
	elif doctype == 'sgml': txt = string.replace(txt, '[', '&lsqb;')
	return txt

def doEscapeEscapechar(txt):
	"Double all Escape Chars"
	return string.replace(txt, ESCCHAR, ESCCHAR*2)

def EscapeCharHandler(action, data):
	"Mask/Unmask the Escape Char on the given string"
	if not string.strip(data): return data
	if action not in ['mask','unmask']:
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


def get_tagged_link(label, url, CONF):
	ret = ''
	doctype = CONF['type']
	
	# set link type
	if regex['email'].match(url):
		linktype = 'email'
	else:
		linktype = 'url';
	
	# escape specials from TEXT parts
	label = doEscape(doctype,label)
	
	# escape specials from link URL
	if rules['linkable'] and rules['escapeurl']:
		url = doEscape(doctype, url)
	
	# if not linkable, the URL is plain text, that needs escape
	if not rules['linkable']:
		if doctype == 'tex':
			url = re.sub('^#', '\#', url) # ugly, but compile
		else:
			url = doEscape(doctype,url)
	
	# adding protocol to guessed link
	guessurl = ''
	if linktype == 'url' and \
	   re.match(regex['_urlskel']['guess'], url):
		if url[0] == 'w': guessurl = 'http://' +url
		else            : guessurl =  'ftp://' +url
		
		# not link aware targets -> protocol is useless
		if not rules['linkable']: guessurl = ''
	
	# simple link (not guessed)
	if not label and not guessurl:
		if CONF['maskemail'] and linktype == 'email':
			# do the email mask feature (no TAGs, just text)
			url = string.replace(url,'@',' (a) ')
			url = string.replace(url,'.',' ')
			url = "<%s>" % url
			if rules['linkable']: url = doEscape(doctype, url)
			ret = url
		else:
			# just add link data to tag
			tag = TAGS[linktype]
			ret = regex['x'].sub(url,tag)
	
	# named link or guessed simple link
	else:
		# adjusts for guessed link
		if not label: label = url       # no   protocol
		if guessurl : url   = guessurl  # with protocol
		
		# change image tag for !supported img+link targets
		if regex['img'].match(label) and not rules['imglinkable']:
			label = "(%s)"%regex['img'].match(label).group(1)
		
		# putting data on the right appearance order
		if rules['linkable']:
			urlorder = [url, label]   # link before label
		else:
			urlorder = [label, url]   # label before link
		
		# add link data to tag (replace \a's)
		ret = TAGS["%sMark"%linktype]
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


def get_tablecell_align(cells):
	ret = []
	for cell in cells:
		align = 'Left'
		if string.strip(cell): 
			if cell[0] == ' ' and cell[-1] == ' ': align = 'Center'
			elif cell[0] == ' ': align = 'Right'
		ret.append(align)
	return ret


def get_table_prop(line):
	# default table proprierties
	ret = {'border':0,'header':0,'align':'Left','cells':[],'cellalign':[]}
	# detect table align (and remove spaces mark)
	if line[0] == ' ': ret['align'] = 'Center'
	line = string.lstrip(line)
	# detect header (title) mark
	if line[1] == '|':
		ret['header'] = 1
	# delete trailing spaces after last cell border
	line = re.sub('\|\s*$','|', line)
	# detect (and delete) border mark (and leading space)
	if line[-1] == '|':
		ret['border'] = 1 ; line = line[:-2]
	# delete table mark
	line = regex['table'].sub('', line)
	# split cells
	ret['cells'] = string.split(line, ' | ')
	# find cells align
	ret['cellalign'] = get_tablecell_align(ret['cells'])
	
	Debug('Table Prop: %s' % ret, 1)
	return ret


def tag_table_cells(table, doctype):
	ret = ''
	open, close = TAGS['tableCellOpen'], TAGS['tableCellClose']
	# title cell
	if table['header']:
		open = TAGS['tableTitleCellOpen']
		close = TAGS['tableTitleCellClose']
	# should we break the line?
	if rules['breaktablecell']: close = close+'\n'
	# here we go
	while table['cells']:
		openalign = open
		cel = table['cells'].pop(0)
		# set each cell align
		if rules['tablecellaligntype'] == 'cell':
			align = table['cellalign'].pop(0)
			align = TAGS['tableCellAlign%s'%align]
			openalign = string.replace(open,'\a',align)
		# show empty cell on HTML
		if not cel and doctype == 'html': cel = '&nbsp;'
		# last cell gotchas
		if not table['cells']:
			# don't need cell separator
			if rules['tablecellsplit']: close = ''
			# close beautifier for last title cell
			if doctype == 'tex' and table['header']: close = '}'
		# join it all
		newcell = openalign + string.strip(cel) + close
		ret = ret + newcell
	return ret


def get_tableopen_tag(table_prop, doctype):
	global tableborder
	open = TAGS['tableOpen'] # the default one
	# the first line defines if table has border or not
	tableborder = table_prop['border']
	# align full table
	if rules['tablealignable']:
		talign = TAGS['tableAlign'+table_prop['align']]
		open = regex['x'].sub(talign, open, 1)
	# set the columns alignment
	if rules['tablecellaligntype'] == 'column':
		calign = map(lambda x: TAGS['tableColAlign%s'%x],
		             table_prop['cellalign'])
		calign = string.join(calign,'')
		open = regex['x'].sub(calign, open, 1)
	# tex table spec, border or not: {|l|c|r|} , {lcr}
	if doctype == 'tex' and not tableborder:
		open = string.replace(open,'|','')
	# we're almost done, just border left
	tag = regex['x'].sub(`tableborder`, open)
	return tag


# reference: http://www.iana.org/assignments/character-sets
# http://www.drclue.net/F1.cgi/HTML/META/META.html
def get_encoding_string(enc, doctype):
	if not enc: return ''
	# target specific translation table
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
	# normalization
	enc = re.sub('(?i)(us[-_]?)?ascii|us|ibm367','us-ascii'  , enc)
	enc = re.sub('(?i)(ibm|cp)?85([02])'        ,'ibm85\\2'  , enc)
	enc = re.sub('(?i)(iso[_-]?)?8859[_-]?'     ,'iso-8859-' , enc)
	enc = re.sub('iso-8859-($|[^1-9]).*'        ,'iso-8859-1', enc)
	# apply translation table
	try: enc = translate[doctype][string.lower(enc)]
	except: pass
	return enc


################################################################################
###MerryChristmas,IdontwanttofighttonightwithyouImissyourbodyandIneedyourlove###
################################################################################


def reallydoitall(cmdlinelist, gui=0):
	header = []
	# parse command line to get input files list
	cmdline = Cmdline(cmdlinelist)
	#TODO how to make an INDEPENDENT copy?
	# cmdline_orig = Cmdline(cmdlinelist)
	# cmdline = cmdline_orig
	infiles = cmdline.cmdline_conf['infiles']
	if not infiles: Quit(usage, 1)
	for infile in infiles:                 # multifile support
		cmdline = Cmdline(cmdlinelist) # one instance for each
		# extract file Headers and Config
		prop = Proprierties(infile)
		# merge %!cmdline contents (if any) into original cmdline
		cmdline.merge(prop.config['cmdline'])
		# force infile
		cmdline.cmdline_conf['infile'] = infile
		# get all the configuration (flags/options) for this file
		myconf = cmdline.merge_conf(prop.config)
		# compose the target file Headers
		#TODO escape line before?
		#TODO see exceptions by tex and mgp
		header = doHeader(prop.headers, myconf)
		# get the marked file BODY that has left
		body = prop.bodylines
		# parse the full marked body into tagged target
		doc,toc = convert(body, myconf, firstlinenr=prop.arearef[-1])
		# make TOC (if needed)
		toc = toc_maker(toc,myconf)
		# finally, we have our document
		outlist = header + toc + doc
		# break here if Gui - it has some more processing to do
		if gui: return outlist, myconf
		# write results to file or STDOUT
		finish_him(outlist, myconf)


def convert(bodylines, CONF, firstlinenr=1):
	# global vars for doClose*()
	global TAGS, regex, rules, quotedepth, listindent, listids
	global subarea, tableborder
	
	doctype = CONF['type']
	outfile = CONF['outfile']
	TAGS = getTags(doctype)
	rules = getRules(doctype)
	regex = getRegexes()
	
	# the defaults
	linkmask  = '@@_link_@@'
	monomask  = '@@_mono_@@'
	macromask = '@@_macro_@@'
	rawmask   = '@@_raw_@@'
	
	subarea = SubareaMaster()
	ret = []
	toclist = []
	f_tt = 0
	listindent = []
	listids = []
	listcount = []
	titlecount = ['',0,0,0,0,0]
	f_lastwasblank = 0
	holdspace = ''
	listholdspace = ''
	quotedepth = []
	tableborder = 0
	
	if outfile != STDOUT:
		if not CONF['gui']:
			print "--- %s..."%doctype
	
	# if TOC is a header tag
	if CONF['toc'] and TAGS['TOC']:
		ret.append(TAGS['TOC']+'\n')
	
	# let's put the opening paragraph
	if doctype != 'pm6':
		ret.append(TAGS['paragraph'])
	
	
	# let's mark it up!
	linenr = firstlinenr-1
	for lineref in range(len(bodylines)):
		skip_continue = 0
		linkbank = []
		monobank = []
		macrobank = []
		rawbank = []
		untouchedline = bodylines[lineref]
		line = re.sub('[\n\r]+$','',untouchedline)   # del line break
		line = maskEscapeChar(line)                  # protect \ char
		linenr = linenr +1
		
		Debug('LINE %04d: %s'%(linenr,repr(line)), 1)  # heavy debug
		
		# we need (not really) to mark each paragraph
		#TODO check if this is really needed
		if doctype == 'pm6' and f_lastwasblank:
			if f_tt or listindent:
				holdspace = ''
			else:
				holdspace = TAGS['paragraph']+'\n'
		
		# any NOT table line (or comment), closes an open table
		#if subarea() == 'table' and not regex['table'].search(line):
		if subarea() == 'table' \
		  and not regex['table'].search(line) \
		  and not regex['comment'].search(line):
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
			f_lastwasblank = 0
			f_tt = 1
			continue
		
		# one line PRE-formatted text
		if regex['1linePre'].search(line):
			f_lastwasblank = 0
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
			if f_lastwasblank:   # 2nd consecutive blank line
				if listindent:   # closes list (if any)
					ret.append(doCloseList())
					holdspace = ''
				continue         # consecutive blanks are trash
			
			# normal blank line
			if doctype != 'pm6':
				# paragraph (if any) is wanted inside lists also
				if listindent:
					para = TAGS['paragraph'] + '\n'
					holdspace = holdspace + para
				elif doctype == 'html':
					ret.append(TAGS['paragraph'])
				# sgml: quote close tag must not be \n\n</quote>
				elif doctype == 'sgml' and quotedepth:
					skip_continue = 1
				# otherwise we just show a blank line
				else:
					ret.append('')
			
			f_lastwasblank = 1
			if not skip_continue: continue
		
		
		#---------------------[ special ]------------------------
		# duh! nothing has left!
		
#		if regex['special'].search(line):
#			special = line[2:]
#			m = regex['command'].match(special)
#			if m:
#				name = string.lower(m.group(1))
#				val  = m.group(2)
#				Debug("Found config '%s', value '%s'"%(
#				       name,val),1,linenr)
#			else:
#				Debug('Bogus Special Line',1,linenr)
		
		#---------------------[ comments ]-----------------------
		
		# just skip them (if not macro or config)
		if regex['comment'].search(line) and not \
		   regex['date'].match(line):
			continue
		f_lastwasblank = 0       # reset blank status
		
		#---------------------[ Title ]-----------------------
		
		# man: - should not be escaped, \ turns to \\\\
		
		#TODO set next blank and set f_lastwasblank or f_lasttitle
		if regex['title'].search(line) and not listindent:
			m = regex['title'].search(line)
			tag = m.group('tag')
			level = len(tag)
			tag = TAGS['title%s'%level]
			
			txt = string.strip(m.group('txt'))
			
			if CONF['enumtitle']:                ### numbered title
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
			if TAGS['anchor'] and CONF['toc'] \
			  and level <= CONF['toclevel']:
				ret.append(regex['x'].sub(anchorid,TAGS['anchor']))
			
			# place title tag overriding line
			line = regex['title'].sub(tag,line)
			
			### escape title text (unescaped text is used for TOC)
			#
			esctxt = doEscape(doctype,idtxt)
			# sgml: [ is special on title (and lists) - here bcos 'continue'
			if doctype == 'sgml': esctxt = re.sub(r'\[', r'&lsqb;', esctxt)
			# man: \ on title becomes \\\\
			if doctype == 'man': esctxt = doEscapeEscapechar(esctxt)
			# finish title line
			ret.append(regex['x'].sub(esctxt,line))
			
			# add "underline" to text titles
			if doctype == 'txt':
				ret.append(regex['x'].sub('='*len(idtxt),tag))
			
			# let's do some TOC!
			if not CONF['toc'] and not CONF['toconly']: continue
			if level > CONF['toclevel']: continue    # max level
			if TAGS['TOC']: continue                 # TOC is a tag
			if TAGS['anchor']:
				# tocitemid = '#toc%d'%(len(toclist)+1)
				# TOC more readable with master topics not
				# linked at number stoled idea from windows .CHM
				# files (help system)
				if CONF['enumtitle'] and level == 1:
					tocitem = '%s+ [``%s`` #%s]'%(' '*level,txt,anchorid)
				else:
					tocitem = '%s- [``%s`` #%s]'%(' '*level,idtxt,anchorid)
			else:
				tocitem = '%s- ``%s``'%(' '*level,idtxt)
				if doctype in ['txt', 'man']:
					tocitem = '%s``%s``' %('  '*level,idtxt)
			toclist.append(tocitem)
			
			continue
		
		#TODO!	labeltxt = ''
		#		label = m.group('label')
		#		if label: labeltxt = '<label id="%s">' %label
		
		
		#---------------------[ apply masks ]-----------------------
		
		### protect important structures from escaping and formatting
		while regex['raw'].search(line):
			txt = regex['raw'].search(line).group(1)
			txt = doEscape(doctype,txt)
			rawbank.append(txt)
			line = regex['raw'].sub(rawmask,line,1)
		
		# protect pre-formatted font text
		while regex['fontMono'].search(line):
			txt = regex['fontMono'].search(line).group(1)
			txt = doEscape(doctype,txt)
			monobank.append(txt)
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
		
		if regex['quote'].search(line):
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
		
		if (regex['list'].search(line) or regex['deflist'].search(line)):
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
				if not rules['imgasdefterm'] and \
				   regex['img'].search(listdefterm):
					while regex['img'].search(listdefterm):
						img = regex['img'].search(listdefterm).group(1)
						masked = '(%s)'%img
						listdefterm = regex['img'].sub(masked,listdefterm,1)
			
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
		if regex['table'].search(line):
			
			table = get_table_prop(line)
			
			if subarea() != 'table':
				subarea.add('table')        # first table line!
				if rules['tableable']:      # table-aware target
					ret.append(get_tableopen_tag(table,doctype))
				else:                       # if not, use verb
					ret.append(TAGS['areaPreOpen'])
			
			if rules['tableable']:
				# setting line tags
				tl1 = TAGS['tableLineOpen']
				tl2 = TAGS['tableLineClose']
				# little table gotchas
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
			link = get_tagged_link(label, url, CONF)
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
					tag= regex['x'].sub(tag,TAGS['imgsolo'])
				# add align on tag
				tag = regex['x'].sub(align, tag, 1)
			
			if doctype == 'tex': tag = re.sub(r'\\b',r'\\\\b',tag)
			line = regex['img'].sub(tag,line,1)
			line = regex['x'].sub(txt,line,1)
		
		#---------------------[ Expand Macros ]-----------------------
		
		if macrobank:
			for macro in macrobank:
				line = string.replace(line, macromask, macro,1)
			# now the line is full of macros again
			line = doDateMacro(line)
		
		#---------------------[ Expand PREs ]-----------------------
		
		for mono in monobank:
			open,close = TAGS['fontMonoOpen'],TAGS['fontMonoClose']
			tagged = open+mono+close
			line = string.replace(line,monomask,tagged,1)
		
		#---------------------[ Expand raw ]-----------------------
		
		for raw in rawbank:
			line = string.replace(line,rawmask,raw,1)
		
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
	if not CONF['noheaders']:
		ret.extend(doFooter(CONF))
	
	if CONF['toconly']: ret = []
	return ret, toclist



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
	
	def exit(self): self.root.destroy(); sys.exit()
	def setvar(self, val): z = Tkinter.StringVar() ; z.set(val) ; return z
	def menu(self,sel,items):
		return apply(Tkinter.OptionMenu,(self.frame,sel)+tuple(items))
	def askfile(self):
		ftypes= [("txt2tags files",("*.t2t","*.txt")),("All files","*")]
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
			showwarning('txt2tags',\
			   "You must provide the source file location!")
			return
		# compose cmdline
		myflags = []
		for flag in FLAGS.keys():
			if flag in ['maskemail','gui']: continue # !supported
			flag = getattr(self, 'f_%s'%flag)
			#TODO this if is really needed?
			if flag.get(): myflags.append(flag.get())
		cmdline = ['txt2tags', '-t', doctype] +myflags +[infile]
		Debug('Gui/Tk cmdline: %s'%cmdline,1)
		# run!
		try:
			outlist, CONF = reallydoitall(cmdline, gui=1)
			outfile = CONF['outfile']
			infile  = CONF['infile']
			
			if outfile == STDOUT:
				title = 'txt2tags: %s converted to %s'%(
				  os.path.basename(infile),
				  string.upper(CONF['type']))
				self.scrollwindow(outlist, title)
			else:
				finish_him(outlist,CONF)
				msg = "Conversion done!\n\n" +\
				      "FROM:\n\t%s\n"%infile +\
				      "TO:\n\t%s"%outfile
				showinfo('txt2tags', msg)
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

	# set debug and remove option from cmdline
	if sys.argv.count('--debug'):
		DEBUG = 1
		sys.argv.remove('--debug')
	
	# check if we will enter on GUI mode
	CONF['gui'] = 0
	if len(sys.argv) == 2 and sys.argv[1] == '--gui':
		CONF['gui'] = 1
	if len(sys.argv) == 1 and sys.platform[:3] in ['mac','cyg','win']:
		CONF['gui'] = 1
	
	# check for GUI mode ressorces
	if CONF['gui'] == 1:
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
				CONF['gui'] = 0
	
	Debug("system platform: %s"%sys.platform,1)
	Debug("line break char: %s"%repr(LB),1)
	
	if CONF['gui'] == 1:
		# redefine Error function to raise exception instead sys.exit()
		def Error(msg):
			showerror('txt2tags ERROR!', msg)
			raise ZeroDivisionError
		Gui().mainwindow()
	else:
		# console mode rocks forever!
		reallydoitall(sys.argv)
	
	sys.exit(0)

# vim: ts=4
