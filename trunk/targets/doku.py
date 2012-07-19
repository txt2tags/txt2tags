"""
A DokuWiki target.
http://www.dokuwiki.org
"""

from targets import _

NAME = _('DokuWiki page')

TYPE = 'wiki'

HEADER = """\
===== %(HEADER1)s =====

**//%(HEADER2)s//**

//%(HEADER3)s//
"""

# http://www.dokuwiki.org/syntax
# http://www.dokuwiki.org/playground:playground
# Hint: <br> is \\ $
# Hint: You can add footnotes ((This is a footnote))
TAGS = {
    'title1'               : '===== \a =====',
    'title2'               : '==== \a ===='  ,
    'title3'               : '=== \a ==='    ,
    'title4'               : '== \a =='      ,
    'title5'               : '= \a ='        ,
    # DokuWiki uses '  ' identation to mark verb blocks (see indentverbblock)
    'blockQuoteLine'       : '>'             ,
    'fontMonoOpen'         : "''"            ,
    'fontMonoClose'        : "''"            ,
    'fontBoldOpen'         : "**"            ,
    'fontBoldClose'        : "**"            ,
    'fontItalicOpen'       : "//"            ,
    'fontItalicClose'      : "//"            ,
    'fontUnderlineOpen'    : "__"            ,
    'fontUnderlineClose'   : "__"            ,
    'fontStrikeOpen'       : '<del>'         ,
    'fontStrikeClose'      : '</del>'        ,
    'listItemOpen'         : '  * '          ,
    'numlistItemOpen'      : '  - '          ,
    'bar1'                 : '----'          ,
    'url'                  : '[[\a]]'        ,
    'urlMark'              : '[[\a|\a]]'     ,
    'email'                : '[[\a]]'        ,
    'emailMark'            : '[[\a|\a]]'     ,
    'img'                  : '{{\a}}'        ,
    'imgAlignLeft'         : '{{\a }}'       ,
    'imgAlignRight'        : '{{ \a}}'       ,
    'imgAlignCenter'       : '{{ \a }}'      ,
    'tableTitleRowOpen'    : '^ '            ,
    'tableTitleRowClose'   : ' ^'            ,
    'tableTitleCellSep'    : ' ^ '           ,
    'tableRowOpen'         : '| '            ,
    'tableRowClose'        : ' |'            ,
    'tableCellSep'         : ' | '           ,
    # DokuWiki has no attributes. The content must be aligned!
    # '_tableCellAlignRight' : '<)>'           ,  # ??
    # '_tableCellAlignCenter': '<:>'           ,  # ??
    # DokuWiki colspan is the same as txt2tags' with multiple |||
    # 'comment'             : '## \a'         ,  # ??
    # TOC is automatic
}

RULES = {
    'indentverbblock': 1,  # DokuWiki uses '  ' to mark verb blocks
    'spacedlistitem': 1,
    'linkable': 1,
    'keeplistindent': 1,
    'tableable': 1,
    'barinsidequote': 1,
    'tablecellstrip': 1,
    'autotocwithbars': 1,
    'autonumberlist': 1,
    'imgalignable': 1,
    'tablecellaligntype': 'cell',

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
