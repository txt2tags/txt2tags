"""
A MediaWiki (Wikipedia) target.
http://www.mediawiki.org
"""

from targets import _

NAME = _('Wikipedia page')

TYPE = 'wiki'

HEADER = """\
'''%(HEADER1)s'''

%(HEADER2)s

''%(HEADER3)s''
"""

# http://en.wikipedia.org/wiki/Help:Editing
# http://www.mediawiki.org/wiki/Sandbox
TAGS = {
    'title1'                : '== \a =='        ,
    'title2'                : '=== \a ==='      ,
    'title3'                : '==== \a ===='    ,
    'title4'                : '===== \a ====='  ,
    'title5'                : '====== \a ======',
    'blockVerbOpen'         : '<pre>'           ,
    'blockVerbClose'        : '</pre>'          ,
    'blockQuoteOpen'        : '<blockquote>'    ,
    'blockQuoteClose'       : '</blockquote>'   ,
    'fontMonoOpen'          : '<tt>'            ,
    'fontMonoClose'         : '</tt>'           ,
    'fontBoldOpen'          : "'''"             ,
    'fontBoldClose'         : "'''"             ,
    'fontItalicOpen'        : "''"              ,
    'fontItalicClose'       : "''"              ,
    'fontUnderlineOpen'     : '<u>'             ,
    'fontUnderlineClose'    : '</u>'            ,
    'fontStrikeOpen'        : '<s>'             ,
    'fontStrikeClose'       : '</s>'            ,
    #XXX Mixed lists not working: *#* list inside numlist inside list
    'listItemLine'          : '*'               ,
    'numlistItemLine'       : '#'               ,
    'deflistItem1Open'      : '; '              ,
    'deflistItem2LinePrefix': ': '              ,
    'bar1'                  : '----'            ,
    'url'                   : '[\a]'            ,
    'urlMark'               : '[\a \a]'         ,
    'urlMarkAnchor'         : '[[\a|\a]]'       ,
    'email'                 : 'mailto:\a'       ,
    'emailMark'             : '[mailto:\a \a]'  ,
    # [[Image:foo.png|right|Optional alt/caption text]] (right, left, center, none)
    'img'                   : '[[Image:\a~A~]]' ,
    '_imgAlignLeft'         : '|left'           ,
    '_imgAlignCenter'       : '|center'         ,
    '_imgAlignRight'        : '|right'          ,
    # {| border="1" cellspacing="0" cellpadding="4" align="center"
    'tableOpen'             : '{|~A~~B~'        ,
    'tableClose'            : '|}'              ,
    'tableRowOpen'          : '|-'              ,
    'tableTitleRowOpen'     : '|-'              ,
    # Note: using one cell per line syntax
    'tableCellOpen'         : '\n|~A~~S~~Z~ '   ,
    'tableTitleCellOpen'    : '\n!~A~~S~~Z~ '   ,
    '_tableBorder'          : ' border="1"'     ,
    '_tableAlignCenter'     : ' align="center"' ,
    '_tableCellAlignRight'  : ' align="right"'  ,
    '_tableCellAlignCenter' : ' align="center"' ,
    '_tableCellColSpan'     : ' colspan="\a"'   ,
    '_tableAttrDelimiter'   : ' |'              ,
    'comment'               : '<!-- \a -->'     ,
    'TOC'                   : '__TOC__'         ,
}

RULES = {
    'escapexmlchars': 1,
    'linkable': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'autotocwithbars': 1,
    'spacedlistitemopen': 1,
    'spacednumlistitemopen': 1,
    'deflisttextstrip': 1,
    'autonumberlist': 1,
    'imgalignable': 1,
    'tablecellspannable': 1,
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
