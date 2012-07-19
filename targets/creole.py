"""
A Creole 1.0 target.
http://www.wikicreole.org
"""

from targets import _

NAME = _('Creole 1.0 document')

TYPE = 'wiki'

HEADER = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

# http://www.wikicreole.org/wiki/AllMarkup
TAGS = {
    'title1'               : '= \a ='        ,
    'title2'               : '== \a =='      ,
    'title3'               : '=== \a ==='    ,
    'title4'               : '==== \a ===='  ,
    'title5'               : '===== \a =====',
    'blockVerbOpen'        : '{{{'           ,
    'blockVerbClose'       : '}}}'           ,
    'blockQuoteLine'       : '  '            ,
#   'fontMonoOpen'         : '##'            ,  # planned for 2.0,
#   'fontMonoClose'        : '##'            ,  # meanwhile we disable it
    'fontBoldOpen'         : '**'            ,
    'fontBoldClose'        : '**'            ,
    'fontItalicOpen'       : '//'            ,
    'fontItalicClose'      : '//'            ,
    'fontUnderlineOpen'    : '//'            ,  # no underline in 1.0, planned for 2.0,
    'fontUnderlineClose'   : '//'            ,  # meanwhile we can use italic (emphasized)
#   'fontStrikeOpen'       : '--'            ,  # planned for 2.0,
#   'fontStrikeClose'      : '--'            ,  # meanwhile we disable it
    'listItemLine'          : '*'            ,
    'numlistItemLine'       : '#'            ,
    'deflistItem2LinePrefix': ':'            ,
    'bar1'                  : '----'         ,
    'url'                  : '[[\a]]'        ,
    'urlMark'              : '[[\a|\a]]'     ,
    'img'                  : '{{\a}}'        ,
    'tableTitleRowOpen'    : '|= '           ,
    'tableTitleRowClose'   : '|'             ,
    'tableTitleCellSep'    : ' |= '          ,
    'tableRowOpen'         : '| '            ,
    'tableRowClose'        : ' |'            ,
    'tableCellSep'         : ' | '           ,
    # TODO: placeholder (mark for unknown syntax)
    # if possible: http://www.wikicreole.org/wiki/Placeholder
}

RULES = {
    'linkable': 1,
    'tableable': 1,
    'imglinkable': 1,
    'tablecellstrip': 1,
    'autotocwithbars': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'deflisttextstrip': 1,
    'verbblocknotescaped': 1,
    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
}
