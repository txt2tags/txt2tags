from lib import aa
import txt
import targets
from targets import _

NAME = _('ASCII Art Text')

TYPE = 'text'

TAGS = {
    'title1'               : '\a'                     ,
    'title2'               : '\a'                     ,
    'title3'               : '\a'                     ,
    'title4'               : '\a'                     ,
    'title5'               : '\a'                     ,
    'blockQuoteLine'       : '        '               ,
    'listItemOpen'         : targets.AA['bullet'] + ' ',
    'numlistItemOpen'      : '\a. '                   ,
    'bar1'                 : aa.line(targets.AA['bar1'], targets.CONF['width']),
    'bar2'                 : aa.line(targets.AA['bar2'], targets.CONF['width']),
    'url'                  : '\a'                     ,
    'urlMark'              : '\a[\a]'                 ,
    'email'                : '\a'                     ,
    'emailMark'            : '\a[\a]'                 ,
    'img'                  : '[\a]'                   ,
    'imgEmbed'             : '\a'                     ,
    'fontBoldOpen'         : '*'                      ,
    'fontBoldClose'        : '*'                      ,
    'fontItalicOpen'       : '/'                      ,
    'fontItalicClose'      : '/'                      ,
    'fontUnderlineOpen'    : '_'                      ,
    'fontUnderlineClose'   : '_'                      ,
    'fontStrikeOpen'       : '-'                      ,
    'fontStrikeClose'      : '-'                      ,
}

RULES = txt.RULES.copy()
RULES['tableable'] = 1
RULES['confdependenttags'] = 1
