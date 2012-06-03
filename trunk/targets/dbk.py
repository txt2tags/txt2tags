"""
A DocBook target.
Target specific occurrence number in txt2tags core: 1.
"""

NAME = 'DocBook document'

TYPE = 'office'

HEADER = """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN"\
 "docbook/dtd/xml/4.5/docbookx.dtd">
<article lang="en">
  <articleinfo>
    <title>%(HEADER1)s</title>
    <authorgroup>
      <author><othername>%(HEADER2)s</othername></author>
    </authorgroup>
    <date>%(HEADER3)s</date>
  </articleinfo>
"""

TAGS = {
    'paragraphOpen'        : '<para>'                            ,
    'paragraphClose'       : '</para>'                           ,
    'title1Open'           : '~A~<sect1><title>\a</title>'       ,
    'title1Close'          : '</sect1>'                          ,
    'title2Open'           : '~A~  <sect2><title>\a</title>'     ,
    'title2Close'          : '  </sect2>'                        ,
    'title3Open'           : '~A~    <sect3><title>\a</title>'   ,
    'title3Close'          : '    </sect3>'                      ,
    'title4Open'           : '~A~      <sect4><title>\a</title>' ,
    'title4Close'          : '      </sect4>'                    ,
    'title5Open'           : '~A~        <sect5><title>\a</title>',
    'title5Close'          : '        </sect5>'                  ,
    'anchor'               : '<anchor id="\a"/>\n'               ,
    'blockVerbOpen'        : '<programlisting>'                  ,
    'blockVerbClose'       : '</programlisting>'                 ,
    'blockQuoteOpen'       : '<blockquote><para>'                ,
    'blockQuoteClose'      : '</para></blockquote>'              ,
    'fontMonoOpen'         : '<code>'                            ,
    'fontMonoClose'        : '</code>'                           ,
    'fontBoldOpen'         : '<emphasis role="bold">'            ,
    'fontBoldClose'        : '</emphasis>'                       ,
    'fontItalicOpen'       : '<emphasis>'                        ,
    'fontItalicClose'      : '</emphasis>'                       ,
    'fontUnderlineOpen'    : '<emphasis role="underline">'       ,
    'fontUnderlineClose'   : '</emphasis>'                       ,
    # 'fontStrikeOpen'       : '<emphasis role="strikethrough">'   ,  # Don't know
    # 'fontStrikeClose'      : '</emphasis>'                       ,
    'listOpen'             : '<itemizedlist>'                    ,
    'listClose'            : '</itemizedlist>'                   ,
    'listItemOpen'         : '<listitem><para>'                  ,
    'listItemClose'        : '</para></listitem>'                ,
    'numlistOpen'          : '<orderedlist numeration="arabic">' ,
    'numlistClose'         : '</orderedlist>'                    ,
    'numlistItemOpen'      : '<listitem><para>'                  ,
    'numlistItemClose'     : '</para></listitem>'                ,
    'deflistOpen'          : '<variablelist>'                    ,
    'deflistClose'         : '</variablelist>'                   ,
    'deflistItem1Open'     : '<varlistentry><term>'              ,
    'deflistItem1Close'    : '</term>'                           ,
    'deflistItem2Open'     : '<listitem><para>'                  ,
    'deflistItem2Close'    : '</para></listitem></varlistentry>' ,
    # 'bar1'                 : '<>'                                ,  # Don't know
    # 'bar2'                 : '<>'                                ,  # Don't know
    'url'                  : '<ulink url="\a">\a</ulink>'        ,
    'urlMark'              : '<ulink url="\a">\a</ulink>'        ,
    'email'                : '<email>\a</email>'                 ,
    'emailMark'            : '<email>\a</email>'                 ,
    'img'                  : '<mediaobject><imageobject><imagedata fileref="\a"/></imageobject></mediaobject>',
    # '_imgAlignLeft'        : ''                                 ,  # Don't know
    # '_imgAlignCenter'      : ''                                 ,  # Don't know
    # '_imgAlignRight'       : ''                                 ,  # Don't know
    'tableOpenDbk'         : '<informaltable><tgroup cols="n_cols"><tbody>',
    'tableClose'           : '</tbody></tgroup></informaltable>' ,
    'tableRowOpen'         : '<row>'                             ,
    'tableRowClose'        : '</row>'                            ,
    'tableCellOpen'        : '<entry>'                           ,
    'tableCellClose'       : '</entry>'                          ,
    'tableTitleRowOpen'    : '<thead>'                           ,
    'tableTitleRowClose'   : '</thead>'                          ,
    '_tableBorder'         : ' frame="all"'                      ,
    '_tableAlignCenter'    : ' align="center"'                   ,
    '_tableCellAlignRight' : ' align="right"'                    ,
    '_tableCellAlignCenter': ' align="center"'                   ,
    '_tableCellColSpan'    : ' COLSPAN="\a"'                     ,
    'TOC'                  : '<index/>'                          ,
    'comment'              : '<!-- \a -->'                       ,
    'EOD'                  : '</article>'
}

RULES = {
    'escapexmlchars': 1,
    'linkable': 1,
    'tableable': 1,  # activate when table tags are ready
    'imglinkable': 1,
    'imgalignable': 1,
    'imgasdefterm': 1,
    'autonumberlist': 1,
    'autonumbertitle': 1,
    'parainsidelist': 1,
    'spacedlistitem': 1,
    'titleblocks': 1,
}
