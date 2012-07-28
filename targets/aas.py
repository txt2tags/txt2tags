import aat
from aat import TYPE, TAGS
from targets import _

NAME = _('ASCII Art Spreadsheet')

RULES = aat.RULES.copy()
RULES['tableonly'] = 1
RULES['spread'] = 1
RULES['spreadgrid'] = 1
RULES['spreadmarkup'] = 'txt'
