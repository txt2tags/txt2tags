"""
A mark target in a file named mark.py
"""

NAME = 'A not real Markup'

TYPE = 'wiki'

HEADER = """\
Mark is not a real Markup syntax, it's just a test.
"""

TAGS = {
    'title1'               : 'I \a'                   ,
    'title2'               : 'II \a'                  ,
    'title3'               : 'III \a'                 ,
    'title4'               : 'IIII \a'                ,
    'title5'               : 'IIIII \a'               ,
    'fontBoldOpen'         : '#'                      ,
    'fontBoldClose'        : '#'                      ,
    'fontItalicOpen'       : '$'                      ,
    'fontItalicClose'      : '$'                      ,
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
