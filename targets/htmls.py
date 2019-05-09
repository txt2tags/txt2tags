"""
A HTML Spreadsheet target.
"""

from targets import _
from . import html5
from .html5 import TYPE, TAGS

NAME =  _('HTML Spreadsheet')

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
table,img.center{border:0;margin:0 auto;}
table th,table td{padding:4px;}
.center,header{text-align:center;}
.right{text-align:right;}
.tableborder,.tableborder td,.tableborder th{border:1px solid #000;}
.underline{text-decoration:underline;}
</style>
</head>
<body>
<article>
"""

RULES = html5.RULES.copy()
HTMLSRULES = {
    'tableonly': 1,
    'spread': 1,
    'spreadgrid': 1,
    'spreadmarkup': 'html',
}
RULES.update(HTMLSRULES)
