#!/usr/bin/env python
#
# Sample of txt2tags being used as a module (http://txt2tags.org)
#
# Details:
#   The full marked text is a string with headers, config and body.
#   No post config or setting is made.
#

import sys

import setup

setup.setup_paths()

import txt2tags

# The markup must be a list.
lines = """\
Header1
Header2
Header3
%!target: html
Body line 1.""".splitlines()

# Let's do the conversion
try:
    # First we parse the text, splitting parts and getting config.
    data = txt2tags.process_source_file(contents=lines)
    # Then we convert it, dumping results to the 'tagged' list.
    tagged_files, config = txt2tags.convert_this_files([data])
    assert len(tagged_files) == 1, tagged_files
    print '\n'.join(tagged_files[0])
except txt2tags.error as err:
    # Txt2tags error, show the message to the user
    print err
    sys.exit(1)
