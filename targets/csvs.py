"""
A CSV Spreadsheet target.
"""

# inherits from the CSV table target
from csv import TYPE, TAGS
import csv
from targets import _

NAME = _('CSV Spreadsheet')

RULES = csv.RULES.copy()
RULES['spread'] = 1
RULES['spreadmarkup'] = 'txt'
