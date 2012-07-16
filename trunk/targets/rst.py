from lib import aa
import targets

NAME = 'ReStructuredText document'

TYPE = 'wiki'

TAGS = {
    'title1'               : '\a'                     ,
    'title2'               : '\a'                     ,
    'title3'               : '\a'                     ,
    'title4'               : '\a'                     ,
    'title5'               : '\a'                     ,
    'blockVerbOpen'        : '::\n'                   ,
    'blockQuoteLine'       : '    '                   ,
    'listItemOpen'         : targets.RST['bullet'] + ' ',
    'numlistItemOpen'      : '\a. '                   ,
    'bar1'                 : aa.line(targets.RST['bar1'], 10) ,
    'url'                  : '\a'                     ,
    'urlMark'              : '`\a <\a>`_'             ,
    'email'                : '\a'                     ,
    'emailMark'            : '`\a <\a>`_'             ,
    'img'                  : '\n\n.. image:: \a\n   :align: ~A~\n\nENDIMG',
    'urlImg'               : '\n   :target: '         ,
    '_imgAlignLeft'        : 'left'                   ,
    '_imgAlignCenter'      : 'center'                 ,
    '_imgAlignRight'       : 'right'                  ,
    'fontMonoOpen'         : '``'                     ,
    'fontMonoClose'        : '``'                     ,
    'fontBoldOpen'         : '**'                     ,
    'fontBoldClose'        : '**'                     ,
    'fontItalicOpen'       : '*'                      ,
    'fontItalicClose'      : '*'                      ,
    'comment'              : '.. \a'                  ,
    'TOC'                  : '\n.. contents::'        ,
}

RULES = {
    'indentverbblock': 1,
    'spacedlistitem': 1,
    'parainsidelist': 1,
    'keeplistindent': 1,
    'barinsidequote': 1,
    'imgalignable': 1,
    'imglinkable': 1,
    'tableable': 1,

    'blanksaroundpara': 1,
    'blanksaroundverb': 1,
    'blanksaroundquote': 1,
    'blanksaroundlist': 1,
    'blanksaroundnumlist': 1,
    'blanksarounddeflist': 1,
    'blanksaroundtable': 1,
    'blanksaroundbar': 1,
    'blanksaroundtitle': 1,
    'blanksaroundnumtitle': 1,
    'blanksaroundnestedlist': 1,
    'confdependenttags': 1,
}
