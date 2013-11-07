"""
A MOM target.
http://www.schaffter.ca/mom/mom-01.html
"""

from targets import _

NAME = _('MOM groff macro')

TYPE = 'office'

## MOM ##
#
# "mom" is a sort of "LaTeX" for groff and has a lot of macro
# commands and variables to customize for specific needs.
# These few lines of commands are sufficient anyway for a good
# postscript typesetted document (and so also pdf): the author
# of "mom" is a professional typographer so the typesetting
# defaults are pleasant and sane.  See mom's author site:
# http://www.schaffter.ca/mom/mom-01.html that's a good
# example of documentation too!
# NB: \# are commented lines in groff.
# I put here a lot of options, commented or not, to let you
# see the possibilities but there many more...
# NB: use "-k" option for groff if input/output is UTF-8
#
# usage: groff -k -m mom sample.mom > sample.ps
#
HEADER = """\
\# Cover and title
.TITLE "%(HEADER1)s"
.AUTHOR "%(HEADER2)s"
\#.DOCTITLE \" ONLY to collate different files (sections, chapters etc.)
.SUBTITLE "%(HEADER3)s"
\#
\# printstyle: typeset or typewrite it's MANDATORY!
.PRINTSTYLE TYPESET
\#.PRINTSTYLE TYPEWRITE
\#
\# doctype: default, chapter, user-defined, letter (commented is "default")
\#.DOCTYPE DEFAULT
\#
\# copystyle: draft or final
.COPYSTYLE FINAL
\#.COPYSTYLE DRAFT
\#
\# Default values for some strings
\# They're valid in every printstyle or copystyle
\# Here are MY defaults (italian)
\# For a more general use I think they should be groff commented
\#
\#.CHAPTER_STRING "Capitolo"
\#.ATTRIBUTE_STRING "di"
\#.TOC_HEADER_STRING "Indice"
\#.ENDNOTE_TITLE "Note"
\#
\# section break char "#" for 1 time (LINEBREAK)
\#.LINEBREAK_CHAR # 1
\# a null end string
.FINIS_STRING ""
\#
\# Typesetting values
\# These are all MY preferences! Comment out for default.
\#
.PAPER A4
\# Left margin (c=centimeters)
\#.L_MARGIN 2.8c
\# Length of line (it's for 62 chars a line for point size 12 in typewrite style)
\#.LL 15.75c
\# Palatino groff font, better than Times for reading. IMHO
.FAMILY P
.PT_SIZE 12
\# line spacing
.LS 18
\# left aligned (mom macro defaults to "both aligned")
.QUAD L
\# No hyphenation
.HY OFF
\# Header and footer sizes
.HEADER_SIZE -1
.FOOTER_SIZE -1
.PAGENUM_SIZE -2
\#
\# Other options
\#
\# Indent space for "quote" and "blockquote" (defaults are good too!)
\#.QUOTE_INDENT 2
\#.BLOCKQUOTE_INDENT 2
\#
\# Footnotes
\#
\# Next gives you superscript numbers (use STAR for symbols, it's default)
\# use additional argument NO_SUPERSCRIPT for typewrite printstyle
\#.FOOTNOTE_MARKER_STYLE NUMBER
\# Cover title at about 1/3 from top
\#.DOCHEADER_ADVANCE 7.5c
\#
\# Double quotes italian style! aka << and >> It works only for "typeset" printstyle
\#.SMARTQUOTES IT
\# Next cmd is MANDATORY.
.START
"""

#
## MOM ##
#
# for mom macros documentation see: http://www.schaffter.ca/mom/mom-01.html
# I commented the difficult parts...
TAGS = {
    'paragraphOpen'        : '.PP'            ,
    'title1'               : '.HEAD "\a"'     ,
    'title2'               : '.SUBHEAD "\a"' ,
    'title3'               : '.SUBSUBHEAD "\a"' ,
    'title4'               : '.PP\n.PARAHEAD "\a"' ,
    'title5'               : '.PP\n.PARAHEAD "\\*[UL]\a\\f[R]\\"' , # my choice
# NB for mom ALL heads of a level after the first numbered are numbered!
# The "NUMBER_*" macros are toggle ones
    'numtitle1'            : '.NUMBER_HEADS\n.HEAD "\a"' ,
    'numtitle2'            : '.NUMBER_SUBHEADS\n.SUBHEAD "\a"' ,
    'numtitle3'            : '.NUMBER_SUBSUBHEADS\n.SUBSUBHEAD "\a"' ,
    'numtitle4'            : '.NUMBER_PARAHEADS\n.PP\nPARAHEAD "\a"' ,
    'numtitle5'            : '.NUMBER_PARAHEADS\n.PP\n.PARAHEAD "\\*[UL]\a\\f[R]\\"' , # my choice
    #'anchor'               : '"\a"', # not supported
    'blockVerbOpen'        : '.QUOTE\n.CODE' , # better for quoting code
    'blockVerbClose'       : '.CODE OFF\n.QUOTE OFF'         ,
    'blockVerbLine '       : '.QUOTE\n.CODE\n\a\n.CODE OFF\n.QUOTE OFF' ,
    'blockQuoteOpen'       : '.BLOCKQUOTE'   ,
    'blockQuoteClose'      : '.BLOCKQUOTE OFF'  ,
    #'blockQuoteLine'       : '.BLOCKQUOTE\n\a\.BLOCKQUOTE OFF' , 
    'fontMonoOpen'         : '\\f[CR]' ,
    'fontMonoClose'        : '\\f[]'  ,
    'fontBoldOpen'         : '\\f[B]'  ,
    'fontBoldClose'        : '\\f[]'  ,
    'fontItalicOpen'       : '\\f[I]'  ,
    'fontItalicClose'      : '\\f[]'  ,
    'fontUnderlineOpen'    : '\\*[FWD 8p]\\*[UL]' , # dirty trick for a bug(?) in mom!
    'fontUnderlineClose'   : '\\*[ULX]'           ,
# Strike. Not directly supported. A groff geek could do a macro for that, not me! :-(
# Use this tricks to emulate "a sort of" strike through word.
# It strikes start and end of a word.
# Not good for less than 3 chars word
# For 4 or 5 chars word is not bad!
# Beware of escapes trying to change it!
# No! It's too ugly!
#        'fontStrikeOpen'       : '\\v\'-0.25m\'\\l\'1P\'\\h\'-1P\'\\v\'0.25m\'' ,
#        'fontStrikeClose'      : '\\v\'-0.25m\'\\l\'-1P\'\\v\'0.25m\'' ,
# Prefer a sort of tag to point out situation
    'fontStrikeOpen'       : '[\(mi' ,
    'fontStrikeClose'      : '\(mi]' ,
    'listOpen'             : '.LIST BULLET' , # other kinds of lists are possible, see mom documentation at site
    'listClose'            : '.LIST OFF'  ,
    'listItemOpen'         : '.ITEM\n'    ,
    'numlistOpen'          : '.LIST DIGIT',
    'numlistClose'         : '.LIST OFF'  ,
    'numlistItemOpen'      : '.ITEM\n'    ,
    'deflistOpen'          : '\\# DEF LIST ON'        , # deflist non supported but "permitted" using PARAHEAD macro or some other hack
    'deflistClose'         : '\\# DEF LIST OFF'        ,
#'deflistItem1Open'     : '.BR\n.PT_SIZE +1\n\\f[B]' , # trick 1
#'deflistItem1Close'    : '\\f[P]\n.PT_SIZE -1'      , # trick 2 for deflist
    'deflistItem1Open'     : '.PP\n.PARAHEAD "'        , # using PARAHEAD is better, it needs PP before.
    'deflistItem1Close'    : ': "'      , # "colon" is a personal choice...
    'bar1'                 : '.LINEBREAK' , # section break
    'bar2'                 : '.NEWPAGE' , # new page
    'url'                  : '\a' ,
# urlMark outputs like this: "label (http://ser.erfg.gov)". Needs a
# preproc rule to transform #anchor links, not used by mom, in
# labels only. Like this one: '\[(.+) #.+\]' '\1'   without that
# one obtains: label (#anchor)
    'urlMark'              : '\a (\a)' ,
    'email'                : '\a' ,
    'emailMark'            : '\a (\a)' , # like urlMark
    'urlImg'               : '.PSPIC "\a"\n.(\a)\n.SHIM\n', # Mmmh...
# NB images: works only with .ps and .eps images (postscript and
# encapsulated postscript) easily obtained with "convert" (in
# ImageMagick suite) from *jpg, *png ecc. It's groff!
    'img'                 : '.PSPIC "\a"\n.SHIM\n',
    'imgAlignLeft'        : '.PSPIC -L "\a"\n.SHIM\n'  ,
    'imgAlignCenter'      : '.PSPIC "\a"\n.SHIM\n',
    'imgAlignRight'       : '.PSPIC -R "\a"\n.SHIM\n' ,
# All table stuff copied from man target! Tables need
# preprocessing with "tbl" using option "-t" with groff
    'tableOpen'             : '.TS\n~A~~B~tab(^); ~C~.', 
    'tableClose'            : '.TE'     ,
    'tableRowOpen'          : ' '       ,
    'tableCellSep'          : '^'       ,
    '_tableAlignCenter'     : 'center, ',
    '_tableBorder'          : 'allbox, ',
    '_tableColAlignLeft'    : 'l'       ,
    '_tableColAlignRight'   : 'r'       ,
    '_tableColAlignCenter'  : 'c'       ,
    #'cssOpen'              : '<STYLE TYPE="text/css">',
    #'cssClose'             : '</STYLE>',
    'comment'              : '\\# \a'    ,
    'blockCommentOpen'     : '.COMMENT' ,
    'blockCommentClose'    : '.COMMENT OFF' ,
    'TOC'                  : '.TOC', # NB: it must be the last macro in file!
    'EOD'                  : '.FINIS'
}

RULES = {
    'autonumberlist': 1,         # target supports numbered lists natively
    'autonumbertitle': 1,        # target supports numbered titles natively
    'imgalignable': 1,           # target supports image alignment
    #'stylable': 1,               # target supports external style files
    'parainsidelist': 1,         # lists items supports paragraph
    'spacedlistitem': 1,         # lists support blank lines between items
    'labelbeforelink': 1,        # label comes before the link on the tag
    'barinsidequote': 1,         # bars are allowed inside quote blocks
    'quotenotnested': 1,         # quotes cannot be nested
    'autotocnewpagebefore': 1,   # break page before automatic TOC
    'autotocnewpageafter': 1,    # break page after automatic TOC
    'mapbar2pagebreak': 1,       # map the strong bar to a page break
    'tableable': 1,              # target supports tables
    'tablecellaligntype': 'column',
    'tabletitlerowinbold': 1,
    'tablecellstrip': 1,
    'blanksaroundlist': 1,       # put a blank line before and after lists
    #'blanksaroundnumlist': 1,    # put a blank line before and after numlists
    #'blanksarounddeflist': 1,    # put a blank line before and after deflists
    #'blanksaroundnestedlist': 1, # put a blank line before and after all type of nested lists
    #'blanksaroundquote',      # put a blank line before and after quotes
    'blanksaroundtable': 1,      # put a blank line before and after tables
    'blankendautotoc': 1,        # append a blank line at the auto TOC end
    'tagnotindentable': 1,       # tags must be placed at the line beginning
}
