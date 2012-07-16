"""
A Plain Text target.
"""

NAME = 'Plain Text'

TYPE = 'text'

HEADER = """\
%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

TAGS = {
    'title1'               : '  \a'      ,
    'title2'               : '\t\a'      ,
    'title3'               : '\t\t\a'    ,
    'title4'               : '\t\t\t\a'  ,
    'title5'               : '\t\t\t\t\a',
    'blockQuoteLine'       : '\t'        ,
    'listItemOpen'         : '- '        ,
    'numlistItemOpen'      : '\a. '      ,
    'bar1'                 : '\a'        ,
    'url'                  : '\a'        ,
    'urlMark'              : '\a (\a)'   ,
    'email'                : '\a'        ,
    'emailMark'            : '\a (\a)'   ,
    'img'                  : '[\a]'      ,
}

RULES = {
    'indentverbblock': 1,
    'spacedlistitem': 1,
    'parainsidelist': 1,
    'keeplistindent': 1,
    'barinsidequote': 1,
    'autotocwithbars': 1,
    'plaintexttoc': 1,

    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
    'iswrapped': 1,
}
