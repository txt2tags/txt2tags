"""
A WordPress target.
http://wordpress.org
"""

from . import html
from targets import _

NAME = _('WordPress post')

TYPE = 'html'

HEADER = HEADERCSS = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

TAGS = html.TAGS.copy()
for tag in TAGS:
    TAGS[tag] = TAGS[tag].lower()
WPTAGS = {
    # Exclusions to let the WordPress code cleaner
    'bodyOpen'             : '',
    'bodyClose'            : '',
    'paragraphOpen'        : '',
    'paragraphClose'       : '',
    'comment'              : '',
    'EOD'                  : '',
    # All list items must be closed
    'listItemClose'        : '</li>'          ,
    'numlistItemClose'     : '</li>'          ,
    'deflistItem2Close'    : '</dd>'          ,
    # WP likes tags this way
    'bar1'                 : '<hr>',
    'bar2'                 : '<hr>',
    'fontBoldOpen'         : '<strong>'       ,
    'fontBoldClose'        : '</strong>'      ,
    'fontItalicOpen'       : '<em>'           ,
    'fontItalicClose'      : '</em>'          ,
    # DIVs
    'tocOpen'              : '<div class="toc">',
    'tocClose'             : '</div>'         ,
    # Table with no cellpadding
    'tableOpen'            : '<table~A~~B~>',
}
TAGS.update(WPTAGS)

RULES = html.RULES.copy()
WPRULES = {
    'onelinepara': 1,
    'onelinequote': 1,
    'tagnotindentable': 1,
    'blanksaroundpara': 1,
    'quotemaxdepth': 1,
    'keepquoteindent': 0,
    'keeplistindent': 0,
    'notbreaklistitemclose': 1,
    'indentverbblock': 0,
    'autotocwithbars': 0,
}
RULES.update(WPRULES)
