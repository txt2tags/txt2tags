"""
A target which inherits from the mark target.
"""

# import of the base target
from mark import *

# NAME inherits from mark.NAME
NAME = 'Inherits from ' + NAME 

# TYPE inherits from mark.TYPE

# HEADER inherits from mark.HEADER
HEADER = """\
Header inherits from: """ + HEADER

# TAGS inherits from  mark.TAGS
# Adds new tags to TAGS
NEW_TAGS = {
    'title1'        : 'HERIT \a',
    'fontBoldOpen'  : '%%'      ,
    'fontBoldClose' : '%%'      ,
}
TAGS.update(NEW_TAGS)

# RULES inherits from mark.RULES
# Adds new rules to RULES
RULES['autotocwithbars'] = 0
RULES['iswrapped']       = 0
