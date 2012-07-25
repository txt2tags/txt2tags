"""
A XHTML target.
"""

from targets import _
from html import TYPE, RULES
import html

NAME = _('XHTML page')

HEADER = """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>
<body bgcolor="white" text="black">
<div align="center">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADER3)s</h3>
</div>
"""

HEADERCSS = """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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

#TIP xhtml inherits all HTML definitions (lowercased)
#TIP http://www.w3.org/TR/xhtml1/#guidelines
#TIP http://www.htmlref.com/samples/Chapt17/17_08.htm
TAGS = html.TAGS.copy()
for tag in TAGS:
    TAGS[tag] = TAGS[tag].lower()
XHTMLTAGS = {
    'listItemClose'        : '</li>'          ,
    'numlistItemClose'     : '</li>'          ,
    'deflistItem2Close'    : '</dd>'          ,
    'bar1'                 : '<hr class="light" />',
    'bar2'                 : '<hr class="heavy" />',
    'img'                  : '<img~A~ src="\a" border="0" alt=""/>',
    'imgEmbed'             : '<img~A~ SRC="\a" border="0" alt=""/>'
}
TAGS.update(XHTMLTAGS)
