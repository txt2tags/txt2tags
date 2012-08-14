import aat
import html
from targets import _

NAME = _('ASCII Art Text Web')

TYPE = 'html'

EXTENSION = 'html'

TAGS = aat.TAGS.copy()
TAGS['url'] = TAGS['urlMark'] = '<a href="\a">\a</a>'
TAGS['email'] = TAGS['emailMark'] = '<a href="mailto:\a">\a</a>'
TAGS['img'] = '<img src="\a" alt=""/>'
TAGS['anchor'] = '<a id="\a">'
TAGS['comment'] = '<!-- \a -->'
for beautifier in ['Bold', 'Italic', 'Underline', 'Strike']:
    _open, close = 'font' + beautifier + 'Open', 'font' + beautifier + 'Close'
    TAGS[_open], TAGS[close] = html.TAGS[_open].lower(), html.TAGS[close].lower()

RULES = aat.RULES.copy()
RULES['linkable'] = 1
RULES['imglinkable'] = 1
RULES['escapexmlchars'] = 1
RULES['web'] = 1
