"""
A LaTeX Spreadsheet target.
Target specific occurrence number in txt2tags core: 7.
"""

# inherits from the LaTeX target
from tex import TYPE, TAGS, ESCAPES
import tex
from targets import _

NAME = _('LaTeX Spreadsheet')

HEADER = \
r"""\documentclass{article}
\usepackage{graphicx}
\usepackage[urlcolor=black,colorlinks=true]{hyperref}
\usepackage[%(ENCODING)s]{inputenc}  %% char encoding
\usepackage{%(STYLE)s}  %% user defined

\begin{document}
"""

RULES = tex.RULES.copy()
RULES['tableonly'] = 1
RULES['spread'] = 1
RULES['spreadgrid'] = 1
RULES['spreadmarkup'] = 'tex'
