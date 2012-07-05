"""
A target which inherits from the mark target.
"""

# direct import of strings
from mark import  NAME, TYPE, HEADER
# direct import of dictionnary if you don't modify it
from mark import TAGS
# no direct import of dictionnary if you modify it
import mark

# NAME inherits from mark.NAME
NAME = 'Inherits from ' + NAME 

# TYPE inherits from mark.TYPE

# HEADER inherits from mark.HEADER
HEADER = """\
Header inherits from: """ + HEADER

# TAGS inherits from  mark.TAGS

# RULES inherits from mark.RULES
RULES = mark.RULES.copy()
# Adds new rules to RULES
RULES['autotocwithbars'] = 0
RULES['iswrapped']       = 0
