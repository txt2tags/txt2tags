"""
A MagicPoint target.
http://member.wide.ad.jp/wg/mgp
Target specific occurrence number in txt2tags core: 5.
"""

from targets import _

NAME = _('MagicPoint presentation')

TYPE = 'office'

HEADER = """\
#!/usr/X11R6/bin/mgp -t 90
%%deffont "normal"    xfont  "utopia-medium-r", charset "iso8859-1"
%%deffont "normal-i"  xfont  "utopia-medium-i", charset "iso8859-1"
%%deffont "normal-b"  xfont  "utopia-bold-r"  , charset "iso8859-1"
%%deffont "normal-bi" xfont  "utopia-bold-i"  , charset "iso8859-1"
%%deffont "mono"      xfont "courier-medium-r", charset "iso8859-1"
%%default 1 size 5
%%default 2 size 8, fore "yellow", font "normal-b", center
%%default 3 size 5, fore "white",  font "normal", left, prefix "  "
%%tab 1 size 4, vgap 30, prefix "     ", icon arc "red" 40, leftfill
%%tab 2 prefix "            ", icon arc "orange" 40, leftfill
%%tab 3 prefix "                   ", icon arc "brown" 40, leftfill
%%tab 4 prefix "                          ", icon arc "darkmagenta" 40, leftfill
%%tab 5 prefix "                                ", icon arc "magenta" 40, leftfill
%%%%------------------------- end of headers -----------------------------
%%page





%%size 10, center, fore "yellow"
%(HEADER1)s

%%font "normal-i", size 6, fore "white", center
%(HEADER2)s

%%font "mono", size 7, center
%(HEADER3)s
"""

# http://www.inference.phy.cam.ac.uk/mackay/mgp/SYNTAX
# http://en.wikipedia.org/wiki/MagicPoint
TAGS = {
    'paragraphOpen'         : '%font "normal", size 5'     ,
    'title1'                : '%page\n\n\a\n'              ,
    'title2'                : '%page\n\n\a\n'              ,
    'title3'                : '%page\n\n\a\n'              ,
    'title4'                : '%page\n\n\a\n'              ,
    'title5'                : '%page\n\n\a\n'              ,
    'blockVerbOpen'         : '%font "mono"'               ,
    'blockVerbClose'        : '%font "normal"'             ,
    'blockQuoteOpen'        : '%prefix "       "'          ,
    'blockQuoteClose'       : '%prefix "  "'               ,
    'fontMonoOpen'          : '\n%cont, font "mono"\n'     ,
    'fontMonoClose'         : '\n%cont, font "normal"\n'   ,
    'fontBoldOpen'          : '\n%cont, font "normal-b"\n' ,
    'fontBoldClose'         : '\n%cont, font "normal"\n'   ,
    'fontItalicOpen'        : '\n%cont, font "normal-i"\n' ,
    'fontItalicClose'       : '\n%cont, font "normal"\n'   ,
    'fontUnderlineOpen'     : '\n%cont, fore "cyan"\n'     ,
    'fontUnderlineClose'    : '\n%cont, fore "white"\n'    ,
    'listItemLine'          : '\t'                         ,
    'numlistItemLine'       : '\t'                         ,
    'numlistItemOpen'       : '\a. '                       ,
    'deflistItem1Open'      : '\t\n%cont, font "normal-b"\n',
    'deflistItem1Close'     : '\n%cont, font "normal"\n'   ,
    'bar1'                  : '%bar "white" 5'             ,
    'bar2'                  : '%pause'                     ,
    'url'                   : '\n%cont, fore "cyan"\n\a'    +\
                              '\n%cont, fore "white"\n'    ,
    'urlMark'               : '\a \n%cont, fore "cyan"\n\a' +\
                              '\n%cont, fore "white"\n'    ,
    'email'                 : '\n%cont, fore "cyan"\n\a'    +\
                              '\n%cont, fore "white"\n'    ,
    'emailMark'             : '\a \n%cont, fore "cyan"\n\a' +\
                              '\n%cont, fore "white"\n'    ,
    'img'                   : '~A~\n%newimage "\a"\n%left\n',
    '_imgAlignLeft'         : '\n%left'                    ,
    '_imgAlignRight'        : '\n%right'                   ,
    '_imgAlignCenter'       : '\n%center'                  ,
    'comment'               : '%% \a'                      ,
    'pageBreak'             : '%page\n\n\n'                ,
    'EOD'                   : '%%EOD'
}

RULES = {
    'tagnotindentable': 1,
    'spacedlistitem': 1,
    'imgalignable': 1,
    'autotocnewpagebefore': 1,

    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'tableable': 1,
    # 'blanksaroundtitle': 1,
    # 'blanksaroundnumtitle': 1,
}
