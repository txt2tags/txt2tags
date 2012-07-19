"""
A SPIP target.
http://www.spip.net
"""

from targets import _

NAME = _('SPIP article')

TYPE = 'wiki'

HEADER = """\
{{{%(HEADER1)s}}}

{{%(HEADER2)s}}

{%(HEADER3)s}

"""

# http://www.spip-contrib.net/Les-raccourcis-typographiques-en
# http://www.spip-contrib.net/Carnet-Bac-a-Sable
# some tags are not implemented by spip tags, but spip accept html tags.
TAGS = {
    'title1'                : '{{{ \a }}}' ,
    'title2'                : '<h4>\a</h4>',
    'title3'                : '<h5>\a</h5>',
    'blockVerbOpen'         : '<cadre>'    ,
    'blockVerbClose'        : '</cadre>'   ,
    'blockQuoteOpen'        : '<quote>'    ,
    'blockQuoteClose'       : '</quote>'   ,
    'fontMonoOpen'          : '<code>'     ,
    'fontMonoClose'         : '</code>'    ,
    'fontBoldOpen'          : '{{'         ,
    'fontBoldClose'         : '}}'         ,
    'fontItalicOpen'        : '{'          ,
    'fontItalicClose'       : '}'          ,
    'fontUnderlineOpen'     : '<u>'        ,
    'fontUnderlineClose'    : '</u>'       ,
    'fontStrikeOpen'        : '<del>'      ,
    'fontStrikeClose'       : '</del>'     ,
    'listItemOpen'          : '-'          ,  # -* list, -** sublist, -*** subsublist
    'listItemLine'          : '*'          ,
    'numlistItemOpen'       : '-'          ,  # -# list, -## sublist, -### subsublist
    'numlistItemLine'       : '#'          ,
    'bar1'                  : '----'       ,
    'url'                   : '[->\a]'     ,
    'urlMark'               : '[\a->\a]'   ,
    'email'                 : '[->\a]'     ,
    'emailMark'             : '[\a->\a]'   ,
    'img'                   : '<img src="\a" />',
    'imgAlignLeft'          : '<img src="\a" align="left" />',
    'imgAlignRight'         : '<img src="\a" align="right" />',
    'imgAlignCenter'        : '<img src="\a" align="center" />',
    'tableTitleRowOpen'     : '| {{'       ,
    'tableTitleRowClose'    : '}} |'       ,
    'tableTitleCellSep'     : '}} | {{'    ,
    'tableRowOpen'          : '| '         ,
    'tableRowClose'         : ' |'         ,
    'tableCellSep'          : ' | '        ,
    # TOC is automatic whith title1 when plugin "couteau suisse" is activate and the option "table des matieres" activate.
}

RULES = {
    'spacedlistitem': 1,
    'spacedlistitemopen': 1,
    'linkable': 1,
    'blankendmotherlist': 1,
    'tableable': 1,
    'barinsidequote': 1,
    'keepquoteindent': 1,
    'blankendtable': 1,
    'tablecellstrip': 1,
    'imgalignable': 1,
    'tablecellaligntype': 'cell',
    'listlineafteropen': 1,
    'labelbeforelink': 1,
    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
}
