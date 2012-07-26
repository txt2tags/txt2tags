"""
A HTML5 target.
"""

from targets import _
from html import TYPE, RULES
import html

NAME = _('HTML5 page')

HEADER = """\
<!doctype html>
<html>
<head>
<meta charset=%(ENCODING)s>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org"/>
<link rel="stylesheet" href="%(STYLE)s"/>
<style>
body{background-color:#fff;color:#000;}
hr{background-color:#000;border:0;color:#000;}
hr.heavy{height:5px;}
hr.light{height:1px;}
img{border:0;display:block;}
img.right{margin:0 0 0 auto;}
img.center{border:0;margin:0 auto;}
table th,table td{padding:4px;}
.center,header{text-align:center;}
table.center {margin-left:auto; margin-right:auto;}
.right{text-align:right;}
.left{text-align:left;}
.tableborder,.tableborder td,.tableborder th{border:1px solid #000;}
.underline{text-decoration:underline;}
</style>
</head>
<body>
<header>
<hgroup>
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</hgroup>
</header>
<article>
"""

HEADERCSS = """\
<!doctype html>
<html>
<head>
<meta charset=%(ENCODING)s>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org"/>
<link rel="stylesheet" href="%(STYLE)s"/>
</head>
<body>
<header>
<hgroup>
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</hgroup>
</header>
<article>
"""

TAGS = html.TAGS.copy()
for tag in TAGS:
    TAGS[tag] = TAGS[tag].lower()
HTML5TAGS = {
    'fontBoldOpen'         : '<strong>'       ,
    'fontBoldClose'        : '</strong>'      ,
    'fontItalicOpen'       : '<em>'           ,
    'fontItalicClose'      : '</em>'          ,
    'fontUnderlineOpen'    : '<span class="underline">',
    'fontUnderlineClose'   : '</span>'        ,
    'fontStrikeOpen'       : '<del>'          ,
    'fontStrikeClose'      : '</del>'         ,
    'listItemClose'        : '</li>'          ,
    'numlistItemClose'     : '</li>'          ,
    'deflistItem2Close'    : '</dd>'          ,
    'bar1'                 : '<hr class="light"/>'        ,
    'bar2'                 : '<hr class="heavy"/>'        ,
    'img'                  : '<img~a~ src="\a" alt=""/>'  ,
    'imgEmbed'             : '<img~a~ src="\a" alt=""/>'  ,
    '_imgAlignLeft'        : ' class="left"'  ,
    '_imgAlignCenter'      : ' class="center"',
    '_imgAlignRight'       : ' class="right"' ,
    'tableOpen'            : '<table~a~~b~>'  ,
    '_tableBorder'         : ' class="tableborder"'      ,
    '_tableAlignCenter'    : ' style="margin-left: auto; margin-right: auto;"',
    '_tableCellAlignRight' : ' class="right"' ,
    '_tableCellAlignCenter': ' class="center"',
    'cssOpen'              : '<style>'        ,
    'tocOpen'              : '<nav>'          ,
    'tocClose'             : '</nav>'         ,
    'EOD'                  : '</article></body></html>'
}
TAGS.update(HTML5TAGS)
