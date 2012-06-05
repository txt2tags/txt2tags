"""
A PageMaker target.
Target specific occurrence number in txt2tags core: 2.
"""

NAME = 'PageMaker document'

TYPE = 'office'

HEADER = """\
<PMTags1.0 win><C-COLORTABLE ("Preto" 1 0 0 0)
><@Normal=
  <FONT "Times New Roman"><CCOLOR "Preto"><SIZE 11>
  <HORIZONTAL 100><LETTERSPACE 0><CTRACK 127><CSSIZE 70><C+SIZE 58.3>
  <C-POSITION 33.3><C+POSITION 33.3><P><CBASELINE 0><CNOBREAK 0><CLEADING -0.05>
  <GGRID 0><GLEFT 7.2><GRIGHT 0><GFIRST 0><G+BEFORE 7.2><G+AFTER 0>
  <GALIGNMENT "justify"><GMETHOD "proportional"><G& "ENGLISH">
  <GPAIRS 12><G%% 120><GKNEXT 0><GKWIDOW 0><GKORPHAN 0><GTABS $>
  <GHYPHENATION 2 34 0><GWORDSPACE 75 100 150><GSPACE -5 0 25>
><@Bullet=<@-PARENT "Normal"><FONT "Abadi MT Condensed Light">
  <GLEFT 14.4><G+BEFORE 2.15><G%% 110><GTABS(25.2 l "")>
><@PreFormat=<@-PARENT "Normal"><FONT "Lucida Console"><SIZE 8><CTRACK 0>
  <GLEFT 0><G+BEFORE 0><GALIGNMENT "left"><GWORDSPACE 100 100 100><GSPACE 0 0 0>
><@Title1=<@-PARENT "Normal"><FONT "Arial"><SIZE 14><B>
  <GCONTENTS><GLEFT 0><G+BEFORE 0><GALIGNMENT "left">
><@Title2=<@-PARENT "Title1"><SIZE 12><G+BEFORE 3.6>
><@Title3=<@-PARENT "Title1"><SIZE 10><GLEFT 7.2><G+BEFORE 7.2>
><@Title4=<@-PARENT "Title3">
><@Title5=<@-PARENT "Title3">
><@Quote=<@-PARENT "Normal"><SIZE 10><I>>

%(HEADER1)s
%(HEADER2)s
%(HEADER3)s
"""

TAGS = {
    'paragraphOpen'         : '<@Normal:>'    ,
    'title1'                : '<@Title1:>\a',
    'title2'                : '<@Title2:>\a',
    'title3'                : '<@Title3:>\a',
    'title4'                : '<@Title4:>\a',
    'title5'                : '<@Title5:>\a',
    'blockVerbOpen'         : '<@PreFormat:>' ,
    'blockQuoteLine'        : '<@Quote:>'     ,
    'fontMonoOpen'          : '<FONT "Lucida Console"><SIZE 9>' ,
    'fontMonoClose'         : '<SIZE$><FONT$>',
    'fontBoldOpen'          : '<B>'           ,
    'fontBoldClose'         : '<P>'           ,
    'fontItalicOpen'        : '<I>'           ,
    'fontItalicClose'       : '<P>'           ,
    'fontUnderlineOpen'     : '<U>'           ,
    'fontUnderlineClose'    : '<P>'           ,
    'listOpen'              : '<@Bullet:>'    ,
    'listItemOpen'          : '\x95\t'        ,  # \x95 == ~U
    'numlistOpen'           : '<@Bullet:>'    ,
    'numlistItemOpen'       : '\x95\t'        ,
    'bar1'                  : '\a'            ,
    'url'                   : '<U>\a<P>'      ,  # underline
    'urlMark'               : '\a <U>\a<P>'   ,
    'email'                 : '\a'            ,
    'emailMark'             : '\a \a'         ,
    'img'                   : '\a'
}

RULES = {
    'keeplistindent': 1,
    'verbblockfinalescape': 1,
    #TODO add support for these
    # maybe set a JOINNEXT char and do it on addLineBreaks()
    'notbreaklistopen': 1,
    'barinsidequote': 1,
    'autotocwithbars': 1,
    'onelinepara': 1,

    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    # 'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    # 'blanksaroundtable': 1,
    # 'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
}
