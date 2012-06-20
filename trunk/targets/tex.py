"""
A LaTeX target.
http://www.latex-project.org
Target specific occurrence number in txt2tags core: 8.
"""

NAME = 'LaTeX document'

TYPE = 'office'

HEADER = \
r"""\documentclass{article}
\usepackage{graphicx}
\usepackage{paralist} %% needed for compact lists
\usepackage[normalem]{ulem} %% needed by strike
\usepackage[urlcolor=blue,colorlinks=true]{hyperref}
\usepackage[%(ENCODING)s]{inputenc}  %% char encoding
\usepackage{%(STYLE)s}  %% user defined

\title{%(HEADER1)s}
\author{%(HEADER2)s}
\begin{document}
\date{%(HEADER3)s}
\maketitle
\clearpage
"""

TAGS = {
    'title1'               : '~A~\section*{\a}'     ,
    'title2'               : '~A~\\subsection*{\a}'   ,
    'title3'               : '~A~\\subsubsection*{\a}',
    # title 4/5: DIRTY: para+BF+\\+\n
    'title4'               : '~A~\\paragraph{}\\textbf{\a}\\\\\n',
    'title5'               : '~A~\\paragraph{}\\textbf{\a}\\\\\n',
    'numtitle1'            : '\n~A~\section{\a}'      ,
    'numtitle2'            : '~A~\\subsection{\a}'    ,
    'numtitle3'            : '~A~\\subsubsection{\a}' ,
    'anchor'               : '\\hypertarget{\a}{}\n'  ,
    'blockVerbOpen'        : '\\begin{verbatim}'   ,
    'blockVerbClose'       : '\\end{verbatim}'     ,
    'blockQuoteOpen'       : '\\begin{quotation}'  ,
    'blockQuoteClose'      : '\\end{quotation}'    ,
    'fontMonoOpen'         : '\\texttt{'           ,
    'fontMonoClose'        : '}'                   ,
    'fontBoldOpen'         : '\\textbf{'           ,
    'fontBoldClose'        : '}'                   ,
    'fontItalicOpen'       : '\\textit{'           ,
    'fontItalicClose'      : '}'                   ,
    'fontUnderlineOpen'    : '\\underline{'        ,
    'fontUnderlineClose'   : '}'                   ,
    'fontStrikeOpen'       : '\\sout{'             ,
    'fontStrikeClose'      : '}'                   ,
    'listOpen'             : '\\begin{itemize}'    ,
    'listClose'            : '\\end{itemize}'      ,
    'listOpenCompact'      : '\\begin{compactitem}',
    'listCloseCompact'     : '\\end{compactitem}'  ,
    'listItemOpen'         : '\\item '             ,
    'numlistOpen'          : '\\begin{enumerate}'  ,
    'numlistClose'         : '\\end{enumerate}'    ,
    'numlistOpenCompact'   : '\\begin{compactenum}',
    'numlistCloseCompact'  : '\\end{compactenum}'  ,
    'numlistItemOpen'      : '\\item '             ,
    'deflistOpen'          : '\\begin{description}',
    'deflistClose'         : '\\end{description}'  ,
    'deflistOpenCompact'   : '\\begin{compactdesc}',
    'deflistCloseCompact'  : '\\end{compactdesc}'  ,
    'deflistItem1Open'     : '\\item['             ,
    'deflistItem1Close'    : ']'                   ,
    'bar1'                 : '\\hrulefill{}'       ,
    'bar2'                 : '\\rule{\linewidth}{1mm}',
    'url'                  : '\\htmladdnormallink{\a}{\a}',
    'urlMark'              : '\\htmladdnormallink{\a}{\a}',
    'email'                : '\\htmladdnormallink{\a}{mailto:\a}',
    'emailMark'            : '\\htmladdnormallink{\a}{mailto:\a}',
    'img'                  : '\\includegraphics{\a}',
    'tableOpen'            : '\\begin{center}\\begin{tabular}{|~C~|}',
    'tableClose'           : '\\end{tabular}\\end{center}',
    'tableRowOpen'         : '\\hline ' ,
    'tableRowClose'        : ' \\\\'    ,
    'tableCellSep'         : ' & '      ,
    '_tableColAlignLeft'   : 'l'        ,
    '_tableColAlignRight'  : 'r'        ,
    '_tableColAlignCenter' : 'c'        ,
    '_tableCellAlignLeft'  : 'l'        ,
    '_tableCellAlignRight' : 'r'        ,
    '_tableCellAlignCenter': 'c'        ,
    '_tableCellColSpan'    : '\a'       ,
    '_tableCellMulticolOpen'  : '\\multicolumn{\a}{|~C~|}{',
    '_tableCellMulticolClose' : '}',
    'tableColAlignSep'     : '|'        ,
    'comment'              : '% \a'     ,
    'TOC'                  : '\\tableofcontents',
    'pageBreak'            : '\\clearpage',
    'EOD'                  : '\\end{document}'
}

RULES = {
    'stylable': 1,
    'escapeurl': 1,
    'autonumberlist': 1,
    'autonumbertitle': 1,
    'spacedlistitem': 1,
    'compactlist': 1,
    'parainsidelist': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'tabletitlerowinbold': 1,
    'verbblocknotescaped': 1,
    'keeplistindent': 1,
    'listmaxdepth': 4,  # deflist is 6
    'quotemaxdepth': 6,
    'barinsidequote': 1,
    'finalescapetitle': 1,
    'autotocnewpageafter': 1,
    'mapbar2pagebreak': 1,
    'tablecellaligntype': 'column',
    'tablecellmulticol': 1,

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
