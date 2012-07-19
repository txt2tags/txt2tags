"""
An AsciiDoc target.
http://www.methods.co.nz/asciidoc
"""

from targets import _

NAME = _('AsciiDoc document')

TYPE = 'wiki'

HEADER = """\
= %(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

# http://powerman.name/doc/asciidoc
TAGS = {
    'title1'               : '== \a'         ,
    'title2'               : '=== \a'        ,
    'title3'               : '==== \a'       ,
    'title4'               : '===== \a'      ,
    'title5'               : '===== \a'      ,
    'blockVerbOpen'        : '----'          ,
    'blockVerbClose'       : '----'          ,
    'fontMonoOpen'         : '+'             ,
    'fontMonoClose'        : '+'             ,
    'fontBoldOpen'         : '*'             ,
    'fontBoldClose'        : '*'             ,
    'fontItalicOpen'       : '_'             ,
    'fontItalicClose'      : '_'             ,
    'listItemOpen'         : '- '            ,
    'listItemLine'         : '\t'            ,
    'numlistItemOpen'      : '. '            ,
    'url'                  : '\a'            ,
    'urlMark'              : '\a[\a]'        ,
    'email'                : 'mailto:\a'     ,
    'emailMark'            : 'mailto:\a[\a]' ,
    'img'                  : 'image::\a[]'   ,
}

RULES = {
    'spacedlistitem': 1,
    'linkable': 1,
    'keeplistindent': 1,
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
