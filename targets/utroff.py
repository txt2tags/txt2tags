"""
An utroff target.
http://utroff.org
"""

from targets import _

NAME = _('Utroff document')

TYPE = 'office'

HEADER = """\
.TH "%(HEADER1)s" 1 "%(HEADER3)s" "%(HEADER2)s"
"""

# man groff_man ; man 7 groff
TAGS = {
    'paragraphOpen'         : '.PP'     ,
    'title1'                : '.H1 \a' ,
    'title2'                : '.H2 \a' ,
    'title3'                : '.H3 \a' ,
    'title4'                : '.H4 \a' ,
    'title5'                : '.H5 \a' ,
    'blockVerbOpen'         : '.nf'    ,
    'blockVerbClose'        : '.fi\n'  ,
    'blockQuoteOpen'        : '.RS'    ,
    'blockQuoteClose'       : '.RE'    ,
    'fontBoldOpen'          : '\\*B'   ,
    'fontBoldClose'         : '\\*R'   ,
    'fontItalicOpen'        : '\\*I'   ,
    'fontItalicClose'       : '\\*R'   ,
    'fontUnderlineOpen'    : '.ul'            ,
    'fontUnderlineClose'   : '\\*R'           ,
    'fontStrikeOpen'       : '.uf'            ,
    'fontStrikeClose'      : '\\*R'           ,
    'listOpen'              : '.PI'    ,
    'listItemOpen'          : '.IP \(bu 3\n',
    'listClose'             : '.RE\n.IP',
    'numlistOpen'           : '.RS'    ,
    'numlistItemOpen'       : '.IP \a. 3\n',
    'numlistClose'          : '.RE\n.IP',
    'deflistItem1Open'      : '.TP\n'  ,
    'bar1'                  : '\n\n'   ,
    'url'                   : '\a'     ,
    'urlMark'               : '\a (\a)',
    'email'                 : '\a'     ,
    'emailMark'             : '\a (\a)',
    'img'                   : '\a'     ,
    'tableOpen'             : '.TS\n~A~~B~tab(^); ~C~.',
    'tableClose'            : '.TE'     ,
    'tableRowOpen'          : ' '       ,
    'tableCellSep'          : '^'       ,
    '_tableAlignCenter'     : 'center, ',
    '_tableBorder'          : 'allbox, ',
    '_tableColAlignLeft'    : 'l'       ,
    '_tableColAlignRight'   : 'r'       ,
    '_tableColAlignCenter'  : 'c'       ,
    'comment'               : '.\\" \a'
}
 
RULES = {
    'spacedlistitem': 1,
    'tagnotindentable': 1,
    'tableable': 1,
    'tablecellaligntype': 'column',
    'tabletitlerowinbold': 1,
    'tablecellstrip': 1,
    'barinsidequote': 1,
    'parainsidelist': 0,
    'plaintexttoc': 1,

    'blanksaroundpara': 0,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    # 'blanksaroundbar': 1,
    'blanksaroundtitle': 0,
    'blanksaroundnumtitle': 1,
}

ESCAPES = [('-', 'vvvvManDashvvvv', r'\-')]
