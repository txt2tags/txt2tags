"""
A CSV table target.
"""

from targets import _

NAME = _('CSV table')

TYPE = 'office'

TAGS = {
    'tableCellSep' : ',' ,
}

RULES = {
    'tableable': 1,
    'tableonly': 1,
    'tablecellstrip': 1,
    'blanksaroundtable': 1,
}
