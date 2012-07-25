"""
A XHTML Strict target.
"""

from targets import _
from html import TYPE, RULES
import html

NAME = _('XHTML Strict page')

HEADER = """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
<style type="text/css">body {background-color:#FFFFFF ; color:#000000}</style>
</head>
<body>
<div style="text-align:center">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</div>
"""

HEADERCSS = """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>
<body>

<div class="header" id="header">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</div>
"""

TAGS = html.TAGS.copy()
for tag in TAGS:
    TAGS[tag] = TAGS[tag].lower()
XHTMLSTAGS = {
    'fontBoldOpen'         : '<strong>'       ,
    'fontBoldClose'        : '</strong>'      ,
    'fontItalicOpen'       : '<em>'           ,
    'fontItalicClose'      : '</em>'          ,
    'fontUnderlineOpen'    : '<span style="text-decoration:underline">',
    'fontUnderlineClose'   : '</span>'        ,
    'fontStrikeOpen'       : '<span style="text-decoration:line-through">',  # use <del> instead ?
    'fontStrikeClose'      : '</span>'        ,
    'listItemClose'        : '</li>'          ,
    'numlistItemClose'     : '</li>'          ,
    'deflistItem2Close'    : '</dd>'          ,
    'bar1'                 : '<hr class="light" />',
    'bar2'                 : '<hr class="heavy" />',
    'img'                  : '<img style="display: block;~a~" src="\a" alt=""/>',
    'imgEmbed'             : '<img~a~ src="\a" alt=""/>',
    '_imgAlignLeft'        : 'margin: 0 auto 0 0;'  ,
    '_imgAlignCenter'      : 'margin: 0 auto 0 auto;',
    '_imgAlignRight'       : 'margin: 0 0 0 auto;' ,
    '_tableAlignCenter'    : ' style="margin-left: auto; margin-right: auto;"',
    '_tableCellAlignRight' : ' style="text-align:right"' ,
    '_tableCellAlignCenter': ' style="text-align:center"',
}
TAGS.update(XHTMLSTAGS)
