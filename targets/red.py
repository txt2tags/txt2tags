"""
A Redmine target.
http://www.redmine.org
"""

NAME = 'Redmine Wiki page'

TYPE = 'wiki'

HEADER = """\
h1. %(HEADER1)s

Author: %(HEADER2)s
Date: %(HEADER3)s
"""

TAGS = {
    'title1'                : 'h1. \a'   ,
    'title2'                : 'h2. \a'   ,
    'title3'                : 'h3. \a'   ,
    'title4'                : 'h4. \a'   ,
    'title5'                : 'h5. \a'   ,
    'fontBoldOpen'          : '*'        ,
    'fontBoldClose'         : '*'        ,
    'fontItalicOpen'        : '_'        ,
    'fontItalicClose'       : '_'        ,
    'fontStrikeOpen'        : '-'        ,
    'fontStrikeClose'       : '-'        ,
    'fontUnderlineOpen'     : "+"        ,
    'fontUnderlineClose'    : "+"        ,
    'blockVerbOpen'         : '<pre>'    ,
    'blockVerbClose'        : '</pre>'   ,
    'blockQuoteLine'        : 'bq. '     ,  # XXX It's a *paragraph* prefix. (issues 64, 65)
    'fontMonoOpen'          : '@'        ,
    'fontMonoClose'         : '@'        ,
    'listItemLine'          : '*'        ,
    'numlistItemLine'       : '#'        ,
    'deflistItem1Open'      : '* '       ,
    'url'                   : '\a'       ,
    'urlMark'               : '"\a":\a'  ,  # "Google":http://www.google.com
    'email'                 : '\a'       ,
    'emailMark'             : '"\a":\a'  ,
    'img'                   : '!~A~\a!'  ,
    '_imgAlignLeft'         : ''         ,  # !image.png! (no align == left)
    '_imgAlignCenter'       : '='        ,  # !=image.png!
    '_imgAlignRight'        : '>'        ,  # !>image.png!
    'tableTitleCellOpen'    : '_.'       ,  # Table header is |_.header|
    'tableTitleCellSep'     : '|'        ,
    'tableCellOpen'         : '~S~~A~. ' ,
    'tableCellSep'          : '|'        ,
    'tableRowOpen'          : '|'        ,
    'tableRowClose'         : '|'        ,
    '_tableCellColSpan'     : '\\\a'     ,
    'bar1'                  : '---'      ,
    'bar2'                  : '---'      ,
    'TOC'                   : '{{toc}}'  ,
}

RULES = {
    'linkable': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'tablecellspannable': 1,
    'tablecellaligntype': 'cell',
    'autotocwithbars': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'deflisttextstrip': 1,
    'autonumberlist': 1,
    'imgalignable': 1,
    'labelbeforelink': 1,
    'quotemaxdepth': 1,
    'autonumbertitle': 1,
    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
}
