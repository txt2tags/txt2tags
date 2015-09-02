import aap
from aap import TYPE, EXTENSION, TAGS
from targets import _

NAME = _('ASCII Art Presentation Print')

RULES = aap.RULES.copy()
RULES['print'] = 1
