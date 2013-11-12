"""
An utmac target.
http://utroff.org/tmac.html
http://utroff.org/man/utmac.html
man utmac
"""

from targets import _

NAME = _('Utmac document')

TYPE = 'office'

HEADER = """\
.DT "%(HEADER1)s"
.DA "%(HEADER2)s"
.DI "%(HEADER3)s"
.H1 "%(HEADER1)s"
.H* "%(HEADER2)s"
.
.\\" txt2tags shortcuts
.ds url \\W'\\\\$2'\\\\$1\\W
.ds mail \\W'mailto:\\\\$2'\\\\$1\\W
.ds underl \\Z'\\\\$*'\\v'.25m'\\l"\\w'\\\\$*'u"\\v'-.25m'
.ds strike \\Z'\\\\$*'\\v'-.25m'\\l"\w'\\\\$*'u"\\v'.25m'
.\\"ds underl \\X'SetColor blue'\\\\$1\\X'SetColor black'
.\\"ds strike \\X'SetColor red'\\\\$1\\X'SetColor black'
.\
"""

TAGS = {
# Use H1 for the title of the document
    'title1'                : '.\n.H2 \a',
    'title2'                : '.\n.H3 \a',
    'title3'                : '.\n.H4 \a',
    'title4'                : '.PP\n\\*B\a\\*R\n.br\n',
    'title5'                : '.PP\n\\*B\a\\*R',

    'paragraphOpen'         : '.PP',
    'blockQuoteOpen'        : '.PQ',
    'blockVerbOpen'         : '.PX',

# We could also use the following to highlight
# source code, where \a is the language (sh, xml...)
    #'blockVerbOpen'         : '.vS \a',
    #'blockVerbClose'        : '.vE',

# Utmac does not handle nested font, and txt2tag
# only understand nested bold italic. So, text2tag
# can't produce the utmac \*(BI.
    'fontBoldOpen'          : '\\*B',
    'fontBoldClose'         : '\\*R',
    'fontItalicOpen'        : '\\*I',
    'fontItalicClose'       : '\\*R',
    'fontUnderlineOpen'    : '\\*[underl ',
    'fontUnderlineClose'   : ']',
    'fontStrikeOpen'       : '\\*[strike ',
    'fontStrikeClose'      : ']',

# There's no nested lists in utmac.
    'listItemOpen'          : '.PI \n',
    'numlistItemOpen'       : '.PI \a\n',
    'deflistItem1Open'      : '.PI ',

# Drawing a bar does not make sense in utmac.
# We prefer space and break page.
    'bar1'                  : '.sp 2v',
    'bar2'                  : '.bp',


# txt2tag should give access to the non space characters
# arround mails and urls to handle correctly the utmac syntax.
# With ~A~ = chars after and ~B~ = chars before,
# the utmac syntax should be:
#    'url' : '\n.LP "\a" ~A~ ~B~\n.LU \a\n',
# We use shortcuts to raw (heirloom) troff instead:
    'anchor'                : '\a\\A"\a"',
    'url'                   : '\\*[url "\a" "\a"]',
    'urlMark'               : '\\*[url "\a" "\a"]',
    'email'                 : '\\*[mail "\a" "\a"]',
    'emailMark'             : '\\*[mail "\a" "\a"]',

# The utmac macro for images is not documented since
# the syntax is not fixed yet. But it just works if
# the image is eps. Expect an update soon...
    #'imgAlignLeft'        : '\n.img:left \a\n',
    #'imgAlignCenter'      : '\n.img:center \a\n',
    #'imgAlignRight'       : '\n.img:left \a\n',

# For the moment, images are ignored
    'img'                   : '\n.\\" \a',

# tables follow the same rules as man (raw tbl syntax)
    'tableOpen'             : '.TS\n~A~~B~tab(^); ~C~.',
    'tableClose'            : '.TE',
    'tableRowOpen'          : ' ',
    'tableCellSep'          : '^',
    '_tableAlignCenter'     : 'center, ',
    '_tableBorder'          : 'allbox, ',
    '_tableColAlignLeft'    : 'l',
    '_tableColAlignRight'   : 'r',
    '_tableColAlignCenter'  : 'c',

# This is raw troff
    'comment'               : '.\\" \a',
    'blockCommentOpen'      : '.ig',
    'blockCommentClose'     : '..',
    'pageBreak'             : '.bp',

# Utmac has a toc macro
    'TOC'                   : '.XT',
}
 
RULES = {
    'tagnotindentable': 1,
    'autonumbertitle': 1,
    'quotenotnested' : 1,
    'barinsidequote': 1,
    'parainsidelist': 0,
    'spacedlistitem': 0,
    'labelbeforelink' : 0, # is that work ?
    'imgalignable': 1,
    'plaintexttoc': 0,

    'tableable': 1,
    'tablecellaligntype': 'column',
    'tabletitlerowinbold': 1,
    'tablecellstrip': 1,

    'blanksaroundpara': 0,
    'blanksaroundverb': 0,
    'blanksaroundquote': 0,
    'blanksaroundlist': 0,
    'blanksaroundnumlist': 0,
    'blanksarounddeflist': 0,
    'blanksaroundtable': 0,
    'blanksaroundbar': 0,
    'blanksaroundtitle': 0,
    'blanksaroundnumtitle': 0,
}

ESCAPES = [('^ *', 'vvvvTroffBreakvvvv', r'')]
# a post-processor should clean the output of txt2tag,
# to remove space(s) and tab(s) at the begining of
# lines, blank lines, and lines containing only spaces
# or tabs.
