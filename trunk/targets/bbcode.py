"""
A BBCode target.
http://www.bbcode.org
"""

from targets import _

NAME = _('BBCode document')

TYPE = 'wiki'

HEADER = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

# http://www.phpbb.com/community/faq.php?mode=bbcode
# http://www.bbcode.org/reference.php (but seldom implemented)
TAGS = {
    'title1'               : '[size=200]\a[/size]'             ,
    'title2'               : '[size=170]\a[/size]'             ,
    'title3'               : '[size=150]\a[/size]'             ,
    'title4'               : '[size=130]\a[/size]'             ,
    'title5'               : '[size=120]\a[/size]'             ,
    'blockQuoteOpen'       : '[quote]'         ,
    'blockQuoteClose'      : '[/quote]'        ,
    'fontMonoOpen'         : '[code]'          ,
    'fontMonoClose'        : '[/code]'         ,
    'fontBoldOpen'         : '[b]'             ,
    'fontBoldClose'        : '[/b]'            ,
    'fontItalicOpen'       : '[i]'             ,
    'fontItalicClose'      : '[/i]'            ,
    'fontUnderlineOpen'    : '[u]'             ,
    'fontUnderlineClose'   : '[/u]'            ,
    #'fontStrikeOpen'       : '[s]'            , (not supported by phpBB)
    #'fontStrikeClose'      : '[/s]'           ,
    'listOpen'             : '[list]'          ,
    'listClose'            : '[/list]'         ,
    'listItemOpen'         : '[*]'             ,
    #'listItemClose'        : '[/li]'          ,
    'numlistOpen'          : '[list=1]'        ,
    'numlistClose'         : '[/list]'         ,
    'numlistItemOpen'      : '[*]'             ,
    'url'                  : '[url]\a[/url]'   ,
    'urlMark'              : '[url=\a]\a[/url]',
    #'urlMark'              : '[url]\a[/url]',
    'img'                  : '[img]\a[/img]'   ,
    #'tableOpen'            : '[table]',
    #'tableClose'           : '[/table]'       ,
    #'tableRowOpen'         : '[tr]'           ,
    #'tableRowClose'        : '[/tr]'          ,
    #'tableCellOpen'        : '[td]'           ,
    #'tableCellClose'       : '[/td]'          ,
    #'tableTitleCellOpen'   : '[th]'           ,
    #'tableTitleCellClose'  : '[/th]'          ,
}

RULES = {
    #'keeplistindent': 1,
    'keepquoteindent': 1,
    #'indentverbblock': 1,
    'linkable': 1,
    #'labelbeforelink': 1,
    #'tableable': 1,
    'imglinkable': 1,
    'tablecellstrip': 1,
    #'autotocwithbars': 1,
    'autonumberlist': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'deflisttextstrip': 1,
    #'verbblocknotescaped': 1,
    'blanksaroundpara': 1,
    #'blanksaroundverb': 1,
    #'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    #'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
}
