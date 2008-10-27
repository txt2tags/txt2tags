#!/usr/bin/env python
#
# Sample of txt2tags being used as a module (http://txt2tags.sf.net) 
#
# Details:
#   The document body is a string.
#   Headers and config are set with Python code.
#

# Remember to place the 'txt2tags.py' file on the same dir
import txt2tags

# Here is the marked body text, it must be a list.
txt = "Hi!\n\nHave a **nice** day.\n\nBye."
txt = txt.split('\n')

# Set the three header fields
headers = ['Header 1', 'Header 2', 'Header 3'] 

# Set the configuration on the 'config' dict.
config = txt2tags.ConfigMaster()._get_defaults()
config['outfile'] = txt2tags.MODULEOUT  # results as list
config['target'] = 'html'               # target type: HTML
config['encoding'] = 'iso-8859-1'       # document encoding
config['css-sugar'] = 1                 # CSS flag

# The Pre (and Post) processing config is a list of lists:
# [ [this, that], [foo, bar], [patt, replace] ]
config['preproc'] = []
config['preproc'].append(['nice','VERY NICE'])
config['preproc'].append(['day','life'])

# Let's do the conversion
try:
	headers   = txt2tags.doHeader(headers, config)
	body, toc = txt2tags.convert(txt, config)
	footer    = txt2tags.doFooter(config)
	full_doc  = headers + toc + body + footer
	finished  = txt2tags.finish_him(full_doc, config)
	print '\n'.join(finished)

# Txt2tags error, show the messsage to the user
except txt2tags.error, msg:
	print msg

# Unknown error, show the traceback to the user
except:
	print txt2tags.getUnknownErrorMessage()
