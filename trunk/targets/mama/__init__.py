"""
A mama target in a directory named mama
"""

NAME = 'The mama office'

TYPE = 'office'

HEADER = """\
Mama is not a real office suite, it's just a test.
"""

TAGS = {
    'title1'               : 'M \a'                   ,
    'title2'               : 'MM \a'                  ,
    'title3'               : 'MMM \a'                 ,
    'title4'               : 'MMMM \a'                ,
    'title5'               : 'MMMMM \a'               ,
    'fontBoldOpen'         : '@@'                     ,
    'fontBoldClose'        : '@@'                     ,
    'fontItalicOpen'       : '%%'                     ,
    'fontItalicClose'      : '%%'                     ,
}

RULES = {
            'indentverbblock': 1,
            'spacedlistitem': 1,
            'parainsidelist': 1,
            'keeplistindent': 1,
            'barinsidequote': 1,
            'autotocwithbars': 1,

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
