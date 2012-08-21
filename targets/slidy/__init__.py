"""
A Slidy target.
http://www.w3.org/Talks/Tools/Slidy2
"""

from targets import _
from targets.xhtml import RULES, EXTENSION
import targets.xhtml

NAME = _('Slidy slides')

TYPE = 'office'

TAGS = targets.xhtml.TAGS.copy()
TAGS['numlistOpen'] = '<ul class="incremental">'
TAGS['numlistClose'] = '</ul>'
TAGS['blocktitle1Open'] = '<div class="slide">'
TAGS['blocktitle1Close'] = '</div>'

HEADER = """\
<?xml version="1.0" encoding="%(ENCODING)s"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
  <title>%(HEADER1)s</title> 
  <meta name="copyright" 
   content="Copyright &#169; %(HEADER2)s %(HEADER2)s" /> 
  <meta name="generator" content="http://txt2tags.org" />
  <link rel="stylesheet" type="text/css" media="screen, projection, print" href="slidy_t2t.css" /> 
  <link rel="stylesheet" type="text/css" href="%(STYLE)s" />
  <script src="http://www.w3.org/Talks/Tools/Slidy2/scripts/slidy.js.gz" charset="utf-8" type="text/javascript"></script> 
  <script src="slidy.js" charset="utf-8" type="text/javascript"></script> 
  <link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>

<div class="background"><a href="http://www.txt2tags.org/"><img
alt="txt2tags logo" id="head-logo-fallback"
src="t2tgems.png" align="right"/></a>
</div>
"""
