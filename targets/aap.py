from lib import aa
import aat
from aat import TYPE, EXTENSION
import targets
from targets import _

NAME = _('ASCII Art Presentation')

TAGS = aat.TAGS.copy()
TAGS['urlMark'] = TAGS['emailMark'] = '\a (\a)'
TAGS['bar1'] = aa.line(targets.AA['bar1'], targets.CONF['width'] - 2)
TAGS['bar2'] = aa.line(targets.AA['bar2'], targets.CONF['width'] - 2)
if not targets.CONF['chars']:
    TAGS['listItemOpen'] = '* '

RULES = aat.RULES.copy()
RULES['blanksaroundtitle'] = 0
RULES['blanksaroundnumtitle'] = 0
RULES['blanksaroundlist'] = 0
RULES['blanksaroundnumlist'] = 0
RULES['blanksarounddeflist'] = 0
RULES['slides'] = 1
