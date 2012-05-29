"""
A target which inherits from the mark target.
"""

# import of the base target
import mark

# NAME inherits from mark.NAME
NAME = 'Inherits from ' + mark.NAME 

# TYPE inherits from mark.TYPE
TYPE = mark.TYPE

# HEADER inherits from mark.HEADER
HEADER = """\
Header inherits from: """ + mark.HEADER

# TAGS inherits from  mark.TAGS
TAGS = mark.TAGS.copy()
# Adds new tags to TAGS
NEW_TAGS = {
    'title1'        : 'HERIT \a',
    'fontBoldOpen'  : '%%'      ,
    'fontBoldClose' : '%%'      ,
}
TAGS.update(NEW_TAGS)

# RULES defaults to {}
RULES = mark.RULES.copy()
# Adds new rules to RULES
RULES['autotocwithbars'] = 0
RULES['iswrapped']       = 0
