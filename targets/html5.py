"""
A HTML5 target.
"""

from targets import _
from . import html
from .html import TYPE

NAME = _('HTML5 page')

EXTENSION = 'html'

HEADER = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="%(ENCODING)s">
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org">
<link rel="stylesheet" href="%(STYLE)s">
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
<!DOCTYPE html>
<html>
<head>
<meta charset="%(ENCODING)s">
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org">
<link rel="stylesheet" href="%(STYLE)s">
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
    'title1Open'           : '<section~A~>\n<h1>\a</h1>' ,
    'title1Close'          : '</section>'                ,
    'title2Open'           : '<section~A~>\n<h2>\a</h2>' ,
    'title2Close'          : '</section>'                ,
    'title3Open'           : '<section~A~>\n<h3>\a</h3>' ,
    'title3Close'          : '</section>'                ,
    'title4Open'           : '<section~A~>\n<h4>\a</h4>' ,
    'title4Close'          : '</section>'                ,
    'title5Open'           : '<section~A~>\n<h5>\a</h5>' ,
    'title5Close'          : '</section>'                ,
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
    'bar1'                 : '<hr class="light">'        ,
    'bar2'                 : '<hr class="heavy">'        ,
    'img'                  : '<img~a~ src="\a" alt="">'  ,
    'imgEmbed'             : '<img~a~ src="\a" alt="">'  ,
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

RULES = html.RULES.copy()
#Update the rules to use explicit <section> </section> tags
HTML5RULES = {
              'titleblocks' : 1,
             }
RULES.update(HTML5RULES)
