"""
A Foswiki/TWiki target.
http://foswiki.org
http://twiki.org
"""

NAME = 'Foswiki or TWiki page'

TYPE = 'wiki'

HEADER = """\
---+!! %(HEADER1)s
*%(HEADER2)s* %%BR%% __%(HEADER3)s__
"""

# http://foswiki.org/System/TextFormattingRules
# http://twiki.org/cgi-bin/view/TWiki/TextFormattingRules
TAGS = {
    'title1'            : '---++ \a',
    'title2'            : '---+++ \a',
    'title3'            : '---++++ \a',
    'title4'            : '---+++++ \a',
    'title5'            : '---++++++ \a',
    'blockVerbOpen'     : '<verbatim>',
    'blockVerbClose'        : '</verbatim>',
    'blockQuoteOpen'        : '<blockquote>',
    'blockQuoteClose'       : '</blockquote>',
    'fontMonoOpen'          : '=',
    'fontMonoClose'         : '=',
    'fontBoldOpen'          : "*",
    'fontBoldClose'         : "*",
    'fontItalicOpen'        : "_",
    'fontItalicClose'       : "_",
    'fontUnderlineOpen'     : '<u>',
    'fontUnderlineClose'    : '</u>',
    'fontStrikeOpen'        : '<del>',
    'fontStrikeClose'       : '</del>',
    'listItemLine'          : '   ',
    'listItemOpen'          : '* ',
    'numlistItemLine'       : '   ',
    'numlistItemOpen'       : '1. ',
    'deflistItemLine'       : '   ',
    'listItemLine'          : '   ',
    'listItemOpen'          : '* ',
    'numlistItemLine'       : '   ',
    'numlistItemOpen'       : '1. ',
    'deflistItemLine'       : '   ',
    'deflistItem1Open'      : '$ ',
    'deflistItem2Open'      : ': ',
    'bar1'                  : '---',
    'bar2'                  : '---',
    'img'                   : '<img~A~ src="%ATTACHURL%/\a" border="0" alt="">',
    'urlImg'                : '[[\a][<img~A~ src="%ATTACHURL%/\a" border="0" alt="">]]',
    'imgEmbed'              : '<img~A~ src="%ATTACHURL%/\a" border="0" alt="">',
    '_imgAlignLeft'         : ' align="left"',
    '_imgAlignCenter'       : ' align="middle"',
    '_imgAlignRight'        : ' align="right"',
    'url'                   : '[[\a]]',
    'urlMark'               : '[[\a][\a]]',
    'anchor'                : '[[#\a]]\n',
    'urlMarkAnchor'         : '[[\a][\a]]',
    'email'                 : '\a',
    'emailMark'             : '[[mailto:\a][\a]]',
    'tableRowOpen'          : '|',
    'tableRowClose'         : '|',
    'tableTitleCellOpen'    : ' *',
    'tableTitleCellClose'   : '* ',
    'tableTitleCellSep'     : '|',
    'tableCellOpen'         : ' ',
    'tableCellClose'        : ' ~S~',
    'tableCellSep'  : '|',
    '_tableCellColSpan'     : '|',
    'comment'               : '<!-- \a -->',
    'TOC'                   : '%TOC%',
}

RULES = {
    'escapexmlchars': 1,
    'linkable': 1,
    'tableable': 1,
    'tablecellstrip': 1,
    'tablecellspannable': 1,
    'spacedlistitem': 1,
    'autonumberlist': 1,
    'notbreaklistopen': 1,
    'imgalignable': 1,
    'imglinkable': 1,
    'tablecellaligntype': 'cell',
    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
}
