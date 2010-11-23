#!/usr/bin/env python
# 2010-11-12 Aurelio Jargas
#
# Tool to compare the tags and rules of two or more targets.
#
# Show all tags/rules by default.
#   -d    Show only the tags/rules that are different
#   -t    Show tags only
#   -r    Show rules only
#   -l    Lowercase all tags (useful with -d when comparing)
#
# Examples:
#
# $ ./compare-targets.py -dl html xhtml
# listItemClose       ''                                        '</li>'
# numlistItemClose    ''                                        '</li>'
# deflistItem2Close   ''                                        '</dd>'
# bar1                '<hr noshade size=1>'                     '<hr class="light" />'
# bar2                '<hr noshade size=5>'                     '<hr class="heavy" />'
# img                 '<img~a~ src="\x07" border="0" alt="">'   '<img~a~ src="\x07" border="0" alt=""/>'
# anchor              '<a name="\x07"></a>\n'                   '<a id="\x07" name="\x07"></a>\n'
#
# $ ./compare-targets.py -dr gwiki doku moin wiki
# imgalignable          0       1       0       1
# autonumberlist        1       1       0       1
# spacedlistitem        1       1       1       0
# tabletitlerowinbold   1       0       1       0
# barinsidequote        0       1       1       0
# autotocwithbars       0       1       1       1
# indentverbblock       0       1       0       0
# keeplistindent        1       1       1       0
# spacedlistitemopen    0       0       0       1
# spacednumlistitemopen 0       0       0       1
# deflisttextstrip      0       0       1       1
# blanksaroundbar       0       1       0       1
# tablecellaligntype    0       'cell'  'cell'  0


# Remember to place the 'txt2tags.py' file on the same dir
import txt2tags

import sys
mode = ''
try:
    if sys.argv[1][0] == '-':
        mode = sys.argv[1]
        del sys.argv[1]
    targets = sys.argv[1:]
except:
    print "Usage: compare-targets.py [-drt] target1 target2 ... targetN"
    sys.exit(1)

# copy/paste from txt2tags code
keys = """
title1              numtitle1
title2              numtitle2
title3              numtitle3
title4              numtitle4
title5              numtitle5
title1Open          title1Close
title2Open          title2Close
title3Open          title3Close
title4Open          title4Close
title5Open          title5Close
blocktitle1Open     blocktitle1Close
blocktitle2Open     blocktitle2Close
blocktitle3Open     blocktitle3Close

paragraphOpen       paragraphClose
blockVerbOpen       blockVerbClose  blockVerbLine
blockQuoteOpen      blockQuoteClose blockQuoteLine
blockCommentOpen    blockCommentClose

fontMonoOpen        fontMonoClose
fontBoldOpen        fontBoldClose
fontItalicOpen      fontItalicClose
fontUnderlineOpen   fontUnderlineClose
fontStrikeOpen      fontStrikeClose

listOpen            listClose
listOpenCompact     listCloseCompact
listItemOpen        listItemClose     listItemLine
numlistOpen         numlistClose
numlistOpenCompact  numlistCloseCompact
numlistItemOpen     numlistItemClose  numlistItemLine
deflistOpen         deflistClose
deflistOpenCompact  deflistCloseCompact
deflistItem1Open    deflistItem1Close
deflistItem2Open    deflistItem2Close deflistItem2LinePrefix

bar1                bar2
url                 urlMark
email               emailMark
img                 imgAlignLeft  imgAlignRight  imgAlignCenter
                   _imgAlignLeft _imgAlignRight _imgAlignCenter

tableOpen           tableClose
_tableBorder        _tableAlignLeft      _tableAlignCenter
tableRowOpen        tableRowClose        tableRowSep
tableTitleRowOpen   tableTitleRowClose
tableCellOpen       tableCellClose       tableCellSep
tableTitleCellOpen  tableTitleCellClose  tableTitleCellSep
_tableColAlignLeft  _tableColAlignRight  _tableColAlignCenter
_tableCellAlignLeft _tableCellAlignRight _tableCellAlignCenter
_tableCellColSpan   tableColAlignSep
_tableCellMulticolOpen
_tableCellMulticolClose

bodyOpen            bodyClose
cssOpen             cssClose
tocOpen             tocClose             TOC
anchor
comment
pageBreak
EOD
""".split()
allrules = [

    # target rules (ON/OFF)
    'linkable',             # target supports external links
    'tableable',            # target supports tables
    'imglinkable',          # target supports images as links
    'imgalignable',         # target supports image alignment
    'imgasdefterm',         # target supports image as definition term
    'autonumberlist',       # target supports numbered lists natively
    'autonumbertitle',      # target supports numbered titles natively
    'stylable',             # target supports external style files
    'parainsidelist',       # lists items supports paragraph
    'compactlist',          # separate enclosing tags for compact lists
    'spacedlistitem',       # lists support blank lines between items
    'listnotnested',        # lists cannot be nested
    'quotenotnested',       # quotes cannot be nested
    'verbblocknotescaped',  # don't escape specials in verb block
    'verbblockfinalescape', # do final escapes in verb block
    'escapeurl',            # escape special in link URL
    'labelbeforelink',      # label comes before the link on the tag
    'onelinepara',          # dump paragraph as a single long line
    'tabletitlerowinbold',  # manually bold any cell on table titles
    'tablecellstrip',       # strip extra spaces from each table cell
    'tablecellspannable',   # the table cells can have span attribute
    'tablecellmulticol',    # separate open+close tags for multicol cells
    'barinsidequote',       # bars are allowed inside quote blocks
    'finalescapetitle',     # perform final escapes on title lines
    'autotocnewpagebefore', # break page before automatic TOC
    'autotocnewpageafter',  # break page after automatic TOC
    'autotocwithbars',      # automatic TOC surrounded by bars
    'mapbar2pagebreak',     # map the strong bar to a page break
    'titleblocks',          # titles must be on open/close section blocks

    # Target code beautify (ON/OFF)
    'indentverbblock',      # add leading spaces to verb block lines
    'breaktablecell',       # break lines after any table cell
    'breaktablelineopen',   # break line after opening table line
    'notbreaklistopen',     # don't break line after opening a new list
    'keepquoteindent',      # don't remove the leading TABs on quotes
    'keeplistindent',       # don't remove the leading spaces on lists
    'blankendautotoc',      # append a blank line at the auto TOC end
    'tagnotindentable',     # tags must be placed at the line beginning
    'spacedlistitemopen',   # append a space after the list item open tag
    'spacednumlistitemopen',# append a space after the numlist item open tag
    'deflisttextstrip',     # strip the contents of the deflist text
    'blanksaroundpara',     # put a blank line before and after paragraphs
    'blanksaroundverb',     # put a blank line before and after verb blocks
    'blanksaroundquote',    # put a blank line before and after quotes
    'blanksaroundlist',     # put a blank line before and after lists
    'blanksaroundnumlist',  # put a blank line before and after numlists
    'blanksarounddeflist',  # put a blank line before and after deflists
    'blanksaroundtable',    # put a blank line before and after tables
    'blanksaroundbar',      # put a blank line before and after bars
    'blanksaroundtitle',    # put a blank line before and after titles
    'blanksaroundnumtitle', # put a blank line before and after numtitles

    # Value settings
    'listmaxdepth',         # maximum depth for lists
    'quotemaxdepth',        # maximum depth for quotes
    'tablecellaligntype',   # type of table cell align: cell, column
]

# Load the default configuration
config = txt2tags.ConfigMaster()._get_defaults()

# Load tags/rules of the informed targets
rules = []
tags = []
for target in targets:
    config['target'] = target
    txt2tags.rules = txt2tags.getRules(config)
    rules.append(txt2tags.rules.copy())
    this_tags = txt2tags.getTags(config)
    if 'l' in mode:
        for key in this_tags:
            this_tags[key] = this_tags[key].lower()
    tags.append(this_tags)

# get the largest item width for each column
widths = []
if 'r' in mode:
    widths.append(max([len(x) for x in allrules]))
    for r in rules:
        widths.append(max([len(repr(x)) for x in r.values()]))
else:
    widths.append(max([len(x) for x in keys]))
    for t in tags:
        widths.append(max([len(repr(x)) for x in t.values()]))

# compose print formatting for each column: %-NNs\t
line_fmt = '\t'.join(['%-' + str(x) + 's' for x in widths])

# print tags
if not 'r' in mode:
    for key in keys:
        values = [repr(x[key]) for x in tags]
        if 'd' not in mode or len(list(set(values))) > 1:
            print line_fmt % tuple([key] + values)

# print rules
if not 't' in mode:
    for key in allrules:
        values = [repr(x[key]) for x in rules]
        if 'd' not in mode or len(list(set(values))) > 1:
            print line_fmt % tuple([key] + [repr(x[key]) for x in rules])

# note: the list(set(my_list)) is a trick to remove duplicates from my_list
