"""
A Vimwiki target.
https://code.google.com/p/vimwiki/
"""

from targets import _

NAME = _('Vimwiki document')

TYPE = 'wiki'

HEADER = """\
%%title %(HEADER1)s
## by %(HEADER2)s in %(HEADER3)s
%%toc %(HEADER1)s
"""

TAGS = {
        'title1'                : '= \a ='        ,
        'title2'                : '== \a =='        ,
        'title3'                : '=== \a ==='      ,
        'title4'                : '==== \a ===='    ,
        'title5'                : '===== \a ====='  ,
        'blockVerbOpen'         : '{{{'           ,
        'blockVerbClose'        : '}}}'          ,
        'blockQuoteOpen'        : '{{{'    ,
        'blockQuoteClose'       : '}}}'   ,
        'fontMonoOpen'          : '`'            ,
        'fontMonoClose'         : '`'           ,
        'fontBoldOpen'          : ' *'             ,
        'fontBoldClose'         : '* '           ,
        'fontItalicOpen'        : ' _'              ,
        'fontItalicClose'       : '_ '              ,
        #'fontUnderlineOpen'     : '<u>'             ,
        #'fontUnderlineClose'    : '</u>'            ,
        'fontStrikeOpen'        : ' ~~'             ,
        'fontStrikeClose'       : '~~ '            ,
        'listItemOpen'         : '- '            ,
        'listItemLine'         : '\t'            ,
        'numlistItemOpen'      : '# '            ,
        'numlistItemLine'       : '\t'               ,
        'bar1'                  : '----'            ,
        'url'                   : '[\a]'            ,
        'urlMark'               : '[\a \a]'         ,
        'email'                 : 'mailto:\a'       ,
        'emailMark'             : '[mailto:\a \a]'  ,
        'img'                  : '[\a]'          ,
        #'_imgAlignLeft'         : '|left'           ,
        #'_imgAlignCenter'       : '|center'         ,
        #'_imgAlignRight'        : '|right'          ,
        'tableRowOpen'          : '| '          ,
        'tableRowClose'          : ' |'          ,
        #'tableTitleRowOpen'     : '|-\n! '          ,
        'tableCellSep'          : ' | '            ,
        #'tableTitleCellSep'     : ' | '            ,
        #'_tableBorder'          : ' border="1"'     ,
        #'_tableAlignCenter'     : ' align="center"' ,
        'comment'               : '%% \a'     ,
        'TOC'                   : '%toc'         ,
}

RULES = {
            'linkable':1,
            'tableable':1,
            #'spacedlistitem':1,
            #'tablecellstrip':1,
            #'autotocwithbars':1,
            #'spacedlistitemopen':1,
            #'spacednumlistitemopen':1,
            #'deflisttextstrip':1,
            'autonumberlist':1,
            'autonumbertitle':1,
            'imgalignable':1,
            'keeplistindent':1,

            'blanksaroundpara':1,
            'blanksaroundverb':1,
            # 'blanksaroundquote':1,
            #'blanksaroundlist':1,
            #'blanksaroundnumlist':1,
            #'blanksarounddeflist':1,
            'blanksaroundtable':1,
            'blanksaroundbar':1,
            'blanksaroundtitle':1,
            'blanksaroundnumtitle':1,
}
