"""
A do-nothing target, uses the default values.
"""

# NAME defaults to 'Null target'
#NAME = ''

# TYPE defaults to 'others', possible values are 'wiki', 'html', 'office' and 'text'
#TYPE = ''

# HEADER defaults to ''
#HEADER = """\
#"""

# TAGS defaults to {}
#TAGS = {
#}

# RULES defaults to {}
#RULES = {
#        # target rules (ON/OFF)
#        'linkable': 1,               # target supports external links
#        'tableable': 1,              # target supports tables
#        'tableonly': 1,              # target computes only the tables
#        'imglinkable': 1,            # target supports images as links
#        'imgalignable': 1,           # target supports image alignment
#        'imgasdefterm': 1,           # target supports image as definition term
#        'autonumberlist': 1,         # target supports numbered lists natively
#        'autonumbertitle': 1,        # target supports numbered titles natively
#        'stylable': 1,               # target supports external style files
#        'parainsidelist': 1,         # lists items supports paragraph
#        'compactlist': 1,            # separate enclosing tags for compact lists
#        'spacedlistitem': 1,         # lists support blank lines between items
#        'listnotnested': 1,          # lists cannot be nested
#        'listitemnotnested': 1,      # list items must be closed before nesting lists
#        'quotenotnested': 1,         # quotes cannot be nested
#        'verbblocknotescaped': 1,    # don't escape specials in verb block
#        'verbblockfinalescape': 1,   # do final escapes in verb block
#        'escapeurl': 1,              # escape special in link URL
#        'labelbeforelink': 1,        # label comes before the link on the tag
#        'onelinepara': 1,            # dump paragraph as a single long line
#        'onelinequote': 1,           # dump quote as a single long line (EXPERIMENTAL)
#        'notbreaklistitemclose': 1,  # do not break line before the list item close tag (EXPERIMENTAL)
#        'tabletitlerowinbold': 1,    # manually bold any cell on table titles
#        'tablecellstrip': 1,         # strip extra spaces from each table cell
#        'tablecellspannable': 1,     # the table cells can have span attribute
#        'tablecellmulticol': 1,      # separate open+close tags for multicol cells
#        'barinsidequote': 1,         # bars are allowed inside quote blocks
#        'finalescapetitle': 1,       # perform final escapes on title lines
#        'autotocnewpagebefore': 1,   # break page before automatic TOC
#        'autotocnewpageafter': 1,    # break page after automatic TOC
#        'autotocwithbars': 1,        # automatic TOC surrounded by bars
#        'mapbar2pagebreak': 1,       # map the strong bar to a page break
#        'titleblocks': 1,            # titles must be on open/close section blocks
#        'listlineafteropen': 1,      # put listItemLine after listItemOpen
#        'escapexmlchars': 1,         # escape the XML special chars: < > &
#        'listlevelzerobased': 1,     # list levels start at 0 when encoding into tags
#        'zerodepthparagraph': 1,     # non-nested paras have block depth of 0 instead of 1
#        'cellspancumulative': 1,     # cell span value adds up for each cell of a row
#        'keepblankheaderline': 1,    # template lines are not removed if headers are blank
#
#        # Target code beautify (ON/OFF)
#        'indentverbblock': 1,        # add leading spaces to verb block lines
#        'breaktablecell': 1,         # break lines after any table cell
#        'breaktablelineopen': 1,     # break line after opening table line
#        'notbreaklistopen': 1,       # don't break line after opening a new list
#        'keepquoteindent': 1,        # don't remove the leading TABs on quotes
#        'keeplistindent': 1,         # don't remove the leading spaces on lists
#        'blankendautotoc': 1,        # append a blank line at the auto TOC end
#        'tagnotindentable': 1,       # tags must be placed at the line beginning
#        'spacedlistitemopen': 1,     # append a space after the list item open tag
#        'spacednumlistitemopen': 1,  # append a space after the numlist item open tag
#        'deflisttextstrip': 1,       # strip the contents of the deflist text
#        'blanksaroundpara': 1,       # put a blank line before and after paragraphs
#        'blanksaroundverb': 1,       # put a blank line before and after verb blocks
#        'blanksaroundquote': 1,      # put a blank line before and after quotes
#        'blanksaroundlist': 1,       # put a blank line before and after lists
#        'blanksaroundnumlist': 1,    # put a blank line before and after numlists
#        'blanksarounddeflist': 1,    # put a blank line before and after deflists
#        'blanksaroundnestedlist': 1, # put a blank line before and after all type of nested lists
#        'blanksaroundtable': 1,      # put a blank line before and after tables
#        'blanksaroundbar': 1,        # put a blank line before and after bars
#        'blanksaroundtitle': 1,      # put a blank line before and after titles
#        'blanksaroundnumtitle': 1,   # put a blank line before and after numtitles
#        'iswrapped': 1,              # wrap with the --width value
#
#        # Value settings
#        'listmaxdepth': 1,           # maximum depth for lists
#        'quotemaxdepth': 1,          # maximum depth for quotes
#        'tablecellaligntype': 'cell',     # type of table cell align: cell, column
#        'blockdepthmultiply': 1,     # block depth multiple for encoding
#        'depthmultiplyplus': 1,      # add to block depth before multiplying
#        'cellspanmultiplier': 1,     # cell span is multiplied by this value
#}
