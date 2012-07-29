import aatw
from aatw import TYPE, TAGS
from targets import _

NAME = _('ASCII Art Spreadsheet Web')

RULES = aatw.RULES.copy()
RULES['tableonly'] = 1
RULES['spread'] = 1
RULES['spreadgrid'] = 1
RULES['spreadmarkup'] = 'html'
