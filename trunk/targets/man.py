"""
A Man target.
Target specific occurrence number in txt2tags core: 1.
"""

from targets import _

NAME = _('UNIX Manual page')

TYPE = 'text'

HEADER = """\
.TH "%(HEADER1)s" 1 "%(HEADER3)s" "%(HEADER2)s"
"""

# man groff_man ; man 7 groff
TAGS = {
    'paragraphOpen'         : '.P'     ,
    'title1'                : '.SH \a' ,
    'title2'                : '.SS \a' ,
    'title3'                : '.SS \a' ,
    'title4'                : '.SS \a' ,
    'title5'                : '.SS \a' ,
    'blockVerbOpen'         : '.nf'    ,
    'blockVerbClose'        : '.fi\n'  ,
    'blockQuoteOpen'        : '.RS'    ,
    'blockQuoteClose'       : '.RE'    ,
    'fontBoldOpen'          : '\\fB'   ,
    'fontBoldClose'         : '\\fR'   ,
    'fontItalicOpen'        : '\\fI'   ,
    'fontItalicClose'       : '\\fR'   ,
    'listOpen'              : '.RS'    ,
    'listItemOpen'          : '.IP \(bu 3\n',
    'listClose'             : '.RE'    ,
    'numlistOpen'           : '.RS'    ,
    'numlistItemOpen'       : '.IP \a. 3\n',
    'numlistClose'          : '.RE'    ,
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
