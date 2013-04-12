"""
A CSV table target.
"""

import targets
from targets import _

NAME = _('CSV table')

TYPE = 'office'

TAGS = {
    'tableCellSep' : targets.CSV['separator'] ,
    'tableCellOpen' : targets.CSV.get('quotechar') or '' ,
    'tableCellClose' : targets.CSV.get('quotechar') or '' ,
}

RULES = {
    'tableable': 1,
    'tableonly': 1,
    'tablecellstrip': 1,
    'blanksaroundtable': 1,
    'confdependenttags': 1,
}
