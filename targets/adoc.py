"""
An AsciiDoc target.
http://www.methods.co.nz/asciidoc
"""

from targets import _

NAME = _('AsciiDoc document')

ALIASES = ['asc', 'asciidoc']

TYPE = 'wiki'

HEADER = """\
= %(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

# http://asciidoc.org/asciidoc.css-embedded.html
TAGS = {
        'title1'               : '== \a'         ,
        'title2'               : '=== \a'        ,
        'title3'               : '==== \a'       ,
        'title4'               : '===== \a'      ,
        'title5'               : '===== \a'      ,
        'blockVerbOpen'        : '----'          ,
        'blockVerbClose'       : '----'          ,
        'deflistItem1Close'    : '::'            ,
        'deflistClose'         : ''              ,
        'deflistItem2Open'     : '	'            ,
        'deflistItem2LinePrefix': '	'            ,
        'fontMonoOpen'         : '+'             ,
        'fontMonoClose'        : '+'             ,
        'fontBoldOpen'         : '*'             ,
        'fontBoldClose'        : '*'             ,
        'fontItalicOpen'       : '_'             ,
        'fontItalicClose'      : '_'             ,
        'listItemOpen'         : ' '             ,
        'listItemLine'         : '*'             ,
        'numlistItemOpen'      : '1. '           ,
        'url'                  : '\a'            ,
        'urlMark'              : '\a[\a]'        ,
        'email'                : 'mailto:\a'     ,
        'emailMark'            : 'mailto:\a[\a]' ,
        'img'                  : 'image::\a[]'   ,
}

RULES = {
            'spacedlistitem': 1,
            'linkable': 1,
            'keeplistindent': 0,
            'autonumberlist': 1,
            'autonumbertitle': 1,
            'listnotnested': 1,
            'blanksaroundpara': 1,
            'blanksaroundverb': 1,
            'blanksaroundlist': 1,
            'blanksaroundnumlist': 1,
            'blanksarounddeflist': 1,
            'blanksaroundtable': 1,
            'blanksaroundtitle': 1,
            'blanksaroundnumtitle': 1,
}
