"""
A SQLite target.
http://www.sqlite.org
Target VERY specific occurrence number in txt2tags core: 4.
"""

from targets import _

NAME = _('SQLite database')

TYPE = 'office'

RULES = {
    'tableable': 1,
    'tableonly': 1,
}
