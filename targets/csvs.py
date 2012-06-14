"""
A CSV Spreadsheet target.
"""

# inherits from the CSV table target
from csv import TYPE, TAGS, RULES

NAME = 'CSV Spreadsheet'

RULES['spread'] = 1
RULES['spreadmarkup'] = 'txt'
