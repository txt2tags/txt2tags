"""
A MoinMoin target.
http://moinmo.in
"""

NAME = 'MoinMoin page'

TYPE = 'wiki'

HEADER = """\
'''%(HEADER1)s'''

''%(HEADER2)s''

%(HEADER3)s
"""

# http://moinmo.in/HelpOnMoinWikiSyntax
TAGS = {
    'title1'                : '= \a ='        ,
    'title2'                : '== \a =='      ,
    'title3'                : '=== \a ==='    ,
    'title4'                : '==== \a ===='  ,
    'title5'                : '===== \a =====',
    'blockVerbOpen'         : '{{{'           ,
    'blockVerbClose'        : '}}}'           ,
    'blockQuoteLine'        : '  '            ,
    'fontMonoOpen'          : '{{{'           ,
    'fontMonoClose'         : '}}}'           ,
    'fontBoldOpen'          : "'''"           ,
    'fontBoldClose'         : "'''"           ,
    'fontItalicOpen'        : "''"            ,
    'fontItalicClose'       : "''"            ,
    'fontUnderlineOpen'     : '__'            ,
    'fontUnderlineClose'    : '__'            ,
    'fontStrikeOpen'        : '--('           ,
    'fontStrikeClose'       : ')--'           ,
    'listItemOpen'          : ' * '           ,
    'numlistItemOpen'       : ' \a. '         ,
    'deflistItem1Open'      : ' '             ,
    'deflistItem1Close'     : '::'            ,
    'deflistItem2LinePrefix': ' :: '          ,
    'bar1'                  : '----'          ,
    'bar2'                  : '--------'      ,
    'url'                   : '[[\a]]'          ,
    'urlMark'               : '[[\a|\a]]'       ,
    'email'                 : '\a'          ,
    'emailMark'             : '[[mailto:\a|\a]]'       ,
    'img'                   : '{{\a}}'          ,
    'tableRowOpen'          : '||'            ,  # || one || two ||
    'tableCellOpen'         : '~S~~A~ '       ,
    'tableCellClose'        : ' ||'           ,
    '_tableCellAlignRight'  : '<)>'           ,  # ||<)> right ||
    '_tableCellAlignCenter' : '<:>'           ,  # ||<:> center ||
    '_tableCellColSpanChar' : '||'            ,  # || cell |||| 2 cells spanned ||
    # Another option for span is ||<-2> two cells spanned ||
    # But mixing span+align is harder with the current code:
    # ||<-2:> two cells spanned and centered ||
    # ||<-2)> two cells spanned and right aligned ||
    # Just appending attributes doesn't work:
    # ||<-2><:> no no no ||
    'comment'               : '/* \a */'      ,
    'TOC'                   : '<<TableOfContents>>'
}

RULES = {
    'spacedlistitem': 1,
    'linkable': 1,
    'keeplistindent': 1,
    'tableable': 1,
    'barinsidequote': 1,
    'tabletitlerowinbold': 1,
    'tablecellstrip': 1,
    'autotocwithbars': 1,
    'tablecellspannable': 1,
    'tablecellaligntype': 'cell',
    'deflisttextstrip': 1,

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
