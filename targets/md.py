"""
A Markdown target.
http://daringfireball.net/projects/markdown
"""

from targets import _

NAME = _('Markdown document')

TYPE = 'wiki'

HEADER = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

# regular markdown: http://daringfireball.net/projects/markdown/syntax
# markdown extra:   http://michelf.com/projects/php-markdown/extra/
# sandbox:
# http://daringfireball.net/projects/markdown/dingus
# http://michelf.com/projects/php-markdown/dingus/
TAGS = {
    'title1'               : '# \a '         ,
    'title2'               : '## \a '        ,
    'title3'               : '### \a '       ,
    'title4'               : '#### \a '      ,
    'title5'               : '##### \a '     ,
    'blockVerbLine'        : '    '          ,
    'blockQuoteLine'       : '> '            ,
    'fontMonoOpen'         : "`"             ,
    'fontMonoClose'        : "`"             ,
    'fontBoldOpen'         : "**"            ,
    'fontBoldClose'        : "**"            ,
    'fontItalicOpen'       : "*"             ,
    'fontItalicClose'      : "*"             ,
    'fontUnderlineOpen'    : ""              ,
    'fontUnderlineClose'   : ""              ,
    'fontStrikeOpen'       : ""              ,
    'fontStrikeClose'      : ""              ,
    # Lists
    #'listOpenCompact'             : '*'     ,
    'listItemLine'          : ' '            ,
    'listItemOpen'          : '*'            ,
    #'numlistItemLine'       : '1.'          ,
    'numlistItemOpen'       : '1.'           ,
    'deflistItem1Open'      : ': '           ,
    #'deflistItem1Close'     : ':'           ,
    #'deflistItem2LineOpen'  : '::'          ,
    #'deflistItem2LineClose' : ':'           ,
    # Verbatim block
    #'blockVerbOpen'        : ''             ,
    #'blockVerbClose'       : ''             ,
    'bar1'                 : '---'           ,
    'bar2'                 : '---'           ,
    # URL, email and anchor
    'url'                   : '\a'           ,
    'urlMark'               : '[\a](\a)'     ,
    'email'                 : '\a'           ,
    #'emailMark'             : '[[\a -> mailto:\a]]',
    #'anchor'                : '[[#\a]]\n'   ,
    # Image markup
    'img'                   : '![](\a)'      ,
    #'imgAlignLeft'         : '{{\a }}'      ,
    #'imgAlignRight'        : '{{ \a}}'      ,
    #'imgAlignCenter'       : '{{ \a }}'     ,
    # Table attributes
    'tableTitleRowOpen'    : '| '            ,
    'tableTitleRowClose'   : '|\n|---------------|'            ,
    'tableTitleCellSep'    : ' |'            ,
    'tableRowOpen'         : '|'             ,
    'tableRowClose'        : '|'             ,
    'tableCellSep'         : ' |'            ,
}

RULES = {
    #'keeplistindent': 1,
    'linkable': 1,
    'labelbeforelink': 1,
    'tableable': 1,
    'imglinkable': 1,
    'tablecellstrip': 1,
    'autonumberlist': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'deflisttextstrip': 1,
    'blanksaroundpara': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    #'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
}
