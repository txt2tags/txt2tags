"""
A Txt2tags target.
http://www.txt2tags.org
"""

NAME = 'Txt2tags document'

TYPE = 'wiki'

HEADER = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
%%! style    : %(STYLE)s
%%! encoding : %(ENCODING)s
"""

TAGS = {
    'title1' : '         = \a =~A~' ,
    'title2' : '        == \a ==~A~' ,
    'title3' : '       === \a ===~A~' ,
    'title4' : '      ==== \a ====~A~' ,
    'title5' : '     ===== \a =====~A~' ,
    'numtitle1' : '         + \a +~A~' ,
    'numtitle2' : '        ++ \a ++~A~' ,
    'numtitle3' : '       +++ \a +++~A~' ,
    'numtitle4' : '      ++++ \a ++++~A~' ,
    'numtitle5' : '     +++++ \a +++++~A~' ,
    'anchor' : '[\a]',
    'blockVerbOpen' : '```' ,
    'blockVerbClose' : '```' ,
    'blockQuoteLine' : '\t' ,
    'blockCommentOpen' : '%%%' ,
    'blockCommentClose' : '%%%' ,
    'fontMonoOpen' : '``' ,
    'fontMonoClose' : '``' ,
    'fontBoldOpen' : '**' ,
    'fontBoldClose' : '**' ,
    'fontItalicOpen' : '//' ,
    'fontItalicClose' : '//' ,
    'fontUnderlineOpen' : '__' ,
    'fontUnderlineClose' : '__' ,
    'fontStrikeOpen' : '--' ,
    'fontStrikeClose' : '--' ,
    'listItemOpen' : '- ' ,
    'numlistItemOpen' : '+ ' ,
    'deflistItem1Open' : ': ' ,
    'listClose': '-',
    'numlistClose': '+',
    'deflistClose': ':',
    'bar1' : '-------------------------' ,
    'bar2' : '=========================' ,
    'url' : '\a' ,
    'urlMark' : '[\a \a]' ,
    #'urlMarkAnchor' : '' ,
    'email' : '\a' ,
    'emailMark' : '[\a \a]' ,
    'img' : '[\a]' ,
    '_tableBorder' : '|' ,
    '_tableAlignLeft' : '' ,
    '_tableAlignCenter' : '   ' ,
    'tableRowOpen' : '~A~' ,
    'tableRowClose' : '~B~' ,
    #'tableRowSep' : '' ,
    'tableTitleRowOpen' : '~A~|' ,
    'tableCellOpen' : '| ' ,
    'tableCellClose' : ' ~S~' ,
    #'tableCellSep' : '' ,
    'tableCellAlignLeft' : '\a  ' ,
    'tableCellAlignRight' : '  \a' ,
    'tableCellAlignCenter' : '  \a  ' ,
    #'_tableCellColSpan' : '' ,
    '_tableCellColSpanChar' : '|' ,
    'comment' : '% \a' ,
}

RULES = {
    'linkable': 1,
    'tableable': 1,
    'imglinkable': 1,
    # 'imgalignable',
    'imgasdefterm': 1,
    'autonumberlist': 1,
    'autonumbertitle': 1,
    'stylable': 1,
    'spacedlistitem': 1,
    'labelbeforelink': 1,
    'tablecellstrip': 1,
    'tablecellspannable': 1,
    'keepblankheaderline': 1,
    'barinsidequote': 1,
    'keeplistindent': 1,
    'blankendautotoc': 1,
    'blanksaroundpara': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
    'tablecellaligntype': 'cell',
}
