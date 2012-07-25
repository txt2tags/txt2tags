"""
A HTML 4.0 target.
"""

from targets import _
import targets
from config import HTML_LOWER

NAME = _('HTML page')

TYPE = 'html'

HEADER = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<META NAME="generator" CONTENT="http://txt2tags.org">
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%(ENCODING)s">
<LINK REL="stylesheet" TYPE="text/css" HREF="%(STYLE)s">
<TITLE>%(HEADER1)s</TITLE>
</HEAD><BODY BGCOLOR="white" TEXT="black">
<CENTER>
<H1>%(HEADER1)s</H1>
<FONT SIZE="4"><I>%(HEADER2)s</I></FONT><BR>
<FONT SIZE="4">%(HEADER3)s</FONT>
</CENTER>
"""

HEADERCSS = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<META NAME="generator" CONTENT="http://txt2tags.org">
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%(ENCODING)s">
<LINK REL="stylesheet" TYPE="text/css" HREF="%(STYLE)s">
<TITLE>%(HEADER1)s</TITLE>
</HEAD>
<BODY>

<DIV CLASS="header" ID="header">
<H1>%(HEADER1)s</H1>
<H2>%(HEADER2)s</H2>
<H3>%(HEADER3)s</H3>
</DIV>
"""

TAGS = {
    'paragraphOpen'        : '<P>'            ,
    'paragraphClose'       : '</P>'           ,
    'title1'               : '<H1~A~>\a</H1>' ,
    'title2'               : '<H2~A~>\a</H2>' ,
    'title3'               : '<H3~A~>\a</H3>' ,
    'title4'               : '<H4~A~>\a</H4>' ,
    'title5'               : '<H5~A~>\a</H5>' ,
    'anchor'               : ' ID="\a"',
    'blockVerbOpen'        : '<PRE>'          ,
    'blockVerbClose'       : '</PRE>'         ,
    'blockQuoteOpen'       : '<BLOCKQUOTE>'   ,
    'blockQuoteClose'      : '</BLOCKQUOTE>'  ,
    'fontMonoOpen'         : '<CODE>'         ,
    'fontMonoClose'        : '</CODE>'        ,
    'fontBoldOpen'         : '<B>'            ,
    'fontBoldClose'        : '</B>'           ,
    'fontItalicOpen'       : '<I>'            ,
    'fontItalicClose'      : '</I>'           ,
    'fontUnderlineOpen'    : '<U>'            ,
    'fontUnderlineClose'   : '</U>'           ,
    'fontStrikeOpen'       : '<S>'            ,
    'fontStrikeClose'      : '</S>'           ,
    'listOpen'             : '<UL>'           ,
    'listClose'            : '</UL>'          ,
    'listItemOpen'         : '<LI>'           ,
    'numlistOpen'          : '<OL>'           ,
    'numlistClose'         : '</OL>'          ,
    'numlistItemOpen'      : '<LI>'           ,
    'deflistOpen'          : '<DL>'           ,
    'deflistClose'         : '</DL>'          ,
    'deflistItem1Open'     : '<DT>'           ,
    'deflistItem1Close'    : '</DT>'          ,
    'deflistItem2Open'     : '<DD>'           ,
    'bar1'                 : '<HR NOSHADE SIZE=1>'        ,
    'bar2'                 : '<HR NOSHADE SIZE=5>'        ,
    'url'                  : '<A HREF="\a">\a</A>'        ,
    'urlMark'              : '<A HREF="\a">\a</A>'        ,
    'email'                : '<A HREF="mailto:\a">\a</A>' ,
    'emailMark'            : '<A HREF="mailto:\a">\a</A>' ,
    'img'                  : '<IMG~A~ SRC="\a" BORDER="0" ALT="">',
    'imgEmbed'             : '<IMG~A~ SRC="\a" BORDER="0" ALT="">',
    '_imgAlignLeft'        : ' ALIGN="left"'  ,
    '_imgAlignCenter'      : ' ALIGN="middle"',
    '_imgAlignRight'       : ' ALIGN="right"' ,
    'tableOpen'            : '<TABLE~A~~B~ CELLPADDING="4">',
    'tableClose'           : '</TABLE>'       ,
    'tableRowOpen'         : '<TR>'           ,
    'tableRowClose'        : '</TR>'          ,
    'tableCellOpen'        : '<TD~A~~S~>'     ,
    'tableCellClose'       : '</TD>'          ,
    'tableTitleCellOpen'   : '<TH~S~>'        ,
    'tableTitleCellClose'  : '</TH>'          ,
    '_tableBorder'         : ' BORDER="1"'    ,
    '_tableAlignCenter'    : ' ALIGN="center"',
    '_tableCellAlignRight' : ' ALIGN="right"' ,
    '_tableCellAlignCenter': ' ALIGN="center"',
    '_tableCellColSpan'    : ' COLSPAN="\a"'  ,
    'cssOpen'              : '<STYLE TYPE="text/css">',
    'cssClose'             : '</STYLE>'       ,
    'comment'              : '<!-- \a -->'    ,
    'EOD'                  : '</BODY></HTML>'
}

if targets.CSS_SUGAR:
        # Table with no cellpadding
        TAGS['tableOpen'] = TAGS['tableOpen'].replace(' CELLPADDING="4"', '')
        # DIVs
        TAGS['tocOpen'] = '<DIV CLASS="toc">'
        TAGS['tocClose'] = '</DIV>'
        TAGS['bodyOpen'] = '<DIV CLASS="body" ID="body">'
        TAGS['bodyClose'] = '</DIV>'

# Some like HTML tags as lowercase, some don't... (headers out)
if HTML_LOWER:
    for tag in TAGS:
        TAGS[tag] = TAGS[tag].lower()

RULES = {
    'escapexmlchars': 1,
    'indentverbblock': 1,
    'linkable': 1,
    'stylable': 1,
    'escapeurl': 1,
    'imglinkable': 1,
    'imgalignable': 1,
    'imgasdefterm': 1,
    'autonumberlist': 1,
    'spacedlistitem': 1,
    'parainsidelist': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'breaktablecell': 1,
    'breaktablelineopen': 1,
    'keeplistindent': 1,
    'keepquoteindent': 1,
    'barinsidequote': 1,
    'autotocwithbars': 1,
    'tablecellspannable': 1,
    'tablecellaligntype': 'cell',

    # 'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
    'confdependenttags':1,
}
