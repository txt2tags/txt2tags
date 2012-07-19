"""
A Google Wiki target.
"""

from targets import _

NAME = _('Google Wiki page')

TYPE = 'wiki'

HEADER = """\
*%(HEADER1)s*

%(HEADER2)s

_%(HEADER3)s_
"""

# http://code.google.com/p/support/wiki/WikiSyntax
TAGS = {
    'title1'               : '= \a ='        ,
    'title2'               : '== \a =='      ,
    'title3'               : '=== \a ==='    ,
    'title4'               : '==== \a ===='  ,
    'title5'               : '===== \a =====',
    'blockVerbOpen'        : '{{{'           ,
    'blockVerbClose'       : '}}}'           ,
    'blockQuoteLine'       : '  '            ,
    'fontMonoOpen'         : '{{{'           ,
    'fontMonoClose'        : '}}}'           ,
    'fontBoldOpen'         : '*'             ,
    'fontBoldClose'        : '*'             ,
    'fontItalicOpen'       : '_'             ,  # underline == italic
    'fontItalicClose'      : '_'             ,
    'fontStrikeOpen'       : '~~'            ,
    'fontStrikeClose'      : '~~'            ,
    'listItemOpen'         : ' * '           ,
    'numlistItemOpen'      : ' # '           ,
    'url'                  : '\a'            ,
    'urlMark'              : '[\a \a]'       ,
    'email'                : 'mailto:\a'     ,
    'emailMark'            : '[mailto:\a \a]',
    'img'                  : '[\a]'          ,
    'tableRowOpen'         : '|| '           ,
    'tableRowClose'        : ' ||'           ,
    'tableCellSep'         : ' || '          ,
}

RULES = {
    'spacedlistitem': 1,
    'linkable': 1,
    'keeplistindent': 1,
    'tableable': 1,
    'tabletitlerowinbold': 1,
    'tablecellstrip': 1,
    'autonumberlist': 1,

    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    # 'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
}
