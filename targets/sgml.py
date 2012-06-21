"""
A SGML target.
Target specific occurrence number in txt2tags core: 1.
"""

NAME = 'SGML document'

TYPE = 'office'

HEADER = """\
<!doctype linuxdoc system>
<article>
<title>%(HEADER1)s
<author>%(HEADER2)s
<date>%(HEADER3)s
"""

TAGS = {
    'paragraphOpen'        : '<p>'                ,
    'title1'               : '<sect>\a~A~<p>'     ,
    'title2'               : '<sect1>\a~A~<p>'    ,
    'title3'               : '<sect2>\a~A~<p>'    ,
    'title4'               : '<sect3>\a~A~<p>'    ,
    'title5'               : '<sect4>\a~A~<p>'    ,
    'anchor'               : '<label id="\a">'    ,
    'blockVerbOpen'        : '<tscreen><verb>'    ,
    'blockVerbClose'       : '</verb></tscreen>'  ,
    'blockQuoteOpen'       : '<quote>'            ,
    'blockQuoteClose'      : '</quote>'           ,
    'fontMonoOpen'         : '<tt>'               ,
    'fontMonoClose'        : '</tt>'              ,
    'fontBoldOpen'         : '<bf>'               ,
    'fontBoldClose'        : '</bf>'              ,
    'fontItalicOpen'       : '<em>'               ,
    'fontItalicClose'      : '</em>'              ,
    'fontUnderlineOpen'    : '<bf><em>'           ,
    'fontUnderlineClose'   : '</em></bf>'         ,
    'listOpen'             : '<itemize>'          ,
    'listClose'            : '</itemize>'         ,
    'listItemOpen'         : '<item>'             ,
    'numlistOpen'          : '<enum>'             ,
    'numlistClose'         : '</enum>'            ,
    'numlistItemOpen'      : '<item>'             ,
    'deflistOpen'          : '<descrip>'          ,
    'deflistClose'         : '</descrip>'         ,
    'deflistItem1Open'     : '<tag>'              ,
    'deflistItem1Close'    : '</tag>'             ,
    'bar1'                 : '<!-- \a -->'        ,
    'url'                  : '<htmlurl url="\a" name="\a">'        ,
    'urlMark'              : '<htmlurl url="\a" name="\a">'        ,
    'email'                : '<htmlurl url="mailto:\a" name="\a">' ,
    'emailMark'            : '<htmlurl url="mailto:\a" name="\a">' ,
    'img'                  : '<figure><ph vspace=""><img src="\a"></figure>',
    'tableOpen'            : '<table><tabular ca="~C~">'           ,
    'tableClose'           : '</tabular></table>' ,
    'tableRowSep'          : '<rowsep>'           ,
    'tableCellSep'         : '<colsep>'           ,
    '_tableColAlignLeft'   : 'l'                  ,
    '_tableColAlignRight'  : 'r'                  ,
    '_tableColAlignCenter' : 'c'                  ,
    'comment'              : '<!-- \a -->'        ,
    'TOC'                  : '<toc>'              ,
    'EOD'                  : '</article>'
}

RULES = {
    'escapexmlchars': 1,
    'linkable': 1,
    'escapeurl': 1,
    'autonumberlist': 1,
    'spacedlistitem': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'blankendautotoc': 1,
    'keeplistindent': 1,
    'keepquoteindent': 1,
    'barinsidequote': 1,
    'finalescapetitle': 1,
    'tablecellaligntype': 'column',

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
    'quotemaxdepth': 1,
}
             
ESCAPES = [('[', 'vvvvSgmlBracketvvvv', '&lsqb;')]
