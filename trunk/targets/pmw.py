"""
A PmWiki target.
http://www.pmwiki.org
"""

NAME = 'PmWiki page'

TYPE = 'wiki'

HEADER = """\
(:Title %(HEADER1)s:)

(:Description %(HEADER2)s:)

(:Summary %(HEADER3)s:)
"""

# http://www.pmwiki.org/wiki/PmWiki/TextFormattingRules
# http://www.pmwiki.org/wiki/Main/WikiSandbox
TAGS = {
    'title1'               : '~A~! \a '      ,
    'title2'               : '~A~!! \a '     ,
    'title3'               : '~A~!!! \a '    ,
    'title4'               : '~A~!!!! \a '   ,
    'title5'               : '~A~!!!!! \a '  ,
    'blockQuoteOpen'       : '->'            ,
    'blockQuoteClose'      : '\n'            ,
    # In-text font
    'fontLargeOpen'        : "[+"            ,
    'fontLargeClose'       : "+]"            ,
    'fontLargerOpen'       : "[++"           ,
    'fontLargerClose'      : "++]"           ,
    'fontSmallOpen'        : "[-"            ,
    'fontSmallClose'       : "-]"            ,
    'fontLargerOpen'       : "[--"           ,
    'fontLargerClose'      : "--]"           ,
    'fontMonoOpen'         : "@@"            ,
    'fontMonoClose'        : "@@"            ,
    'fontBoldOpen'         : "'''"           ,
    'fontBoldClose'        : "'''"           ,
    'fontItalicOpen'       : "''"            ,
    'fontItalicClose'      : "''"            ,
    'fontUnderlineOpen'    : "{+"            ,
    'fontUnderlineClose'   : "+}"            ,
    'fontStrikeOpen'       : '{-'            ,
    'fontStrikeClose'      : '-}'            ,
    # Lists
    'listItemLine'          : '*'            ,
    'numlistItemLine'       : '#'            ,
    'deflistItem1Open'      : ': '           ,
    'deflistItem1Close'     : ':'            ,
    'deflistItem2LineOpen'  : '::'           ,
    'deflistItem2LineClose' : ':'            ,
    # Verbatim block
    'blockVerbOpen'        : '[@'            ,
    'blockVerbClose'       : '@]'            ,
    'bar1'                 : '----'          ,
    # URL, email and anchor
    'url'                   : '\a'           ,
    'urlMark'               : '[[\a -> \a]]' ,
    'email'                 : '\a'           ,
    'emailMark'             : '[[\a -> mailto:\a]]',
    'anchor'                : '[[#\a]]\n'    ,
    # Image markup
    'img'                   : '\a'           ,
    #'imgAlignLeft'         : '{{\a }}'       ,
    #'imgAlignRight'        : '{{ \a}}'       ,
    #'imgAlignCenter'       : '{{ \a }}'      ,
    # Table attributes
    'tableTitleRowOpen'    : '||! '          ,
    'tableTitleRowClose'   : '||'            ,
    'tableTitleCellSep'    : ' ||!'          ,
    'tableRowOpen'         : '||'            ,
    'tableRowClose'        : '||'            ,
    'tableCellSep'         : ' ||'           ,
}

RULES = {
    'indentverbblock': 1,
    'spacedlistitem': 1,
    'linkable': 1,
    'labelbeforelink': 1,
    # 'keeplistindent': 1,
    'tableable': 1,
    'barinsidequote': 1,
    'tablecellstrip': 1,
    'autotocwithbars': 1,
    'autonumberlist': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'imgalignable': 1,
    'tabletitlerowinbold': 1,
    'tablecellaligntype': 'cell',

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
