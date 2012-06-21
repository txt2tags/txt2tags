"""
A RTF target.
Target specific occurrence number in txt2tags core: 6.
"""

NAME = 'RTF document'

TYPE = 'office'

HEADER = \
r"""{\rtf1\ansi\ansicpg1252\deff0
{\fonttbl
{\f0\froman Times;}
{\f1\fswiss Arial;}
{\f2\fmodern Courier;}
}
{\colortbl;\red0\green0\blue255;}
{\stylesheet
{\s1\sbasedon222\snext1\f0\fs24\cf0 Normal;}
{\s2\sbasedon1\snext2{\*\txttags paragraph}\f0\fs24\qj\sb0\sa0\sl480\slmult1\li0\ri0\fi360 Body Text;}
{\s3\sbasedon2\snext3{\*\txttags verbatim}\f2\fs20\ql\sb0\sa240\sl240\slmult1\li720\ri720\fi0 Verbatim;}
{\s4\sbasedon2\snext4{\*\txttags quote}\f0\fs24\qj\sb0\sa0\sl480\slmult1\li720\ri720\fi0 Block Quote;}
{\s10\sbasedon1\snext10\keepn{\*\txttags maintitle}\f1\fs24\qc\sb0\sa0\sl480\slmult1\li0\ri0\fi0 Title;}
{\s11\sbasedon1\snext2\keepn{\*\txttags title1}\f1\fs24\qc\sb240\sa240\sl480\slmult1\li0\ri0\fi0\b Heading 1;}
{\s12\sbasedon11\snext2\keepn{\*\txttags title2}\f1\fs24\ql\sb240\sa240\sl480\slmult1\li0\ri0\fi0\b Heading 2;}
{\s13\sbasedon11\snext2\keepn{\*\txttags title3}\f1\fs24\ql\sb240\sa240\sl480\slmult1\li360\ri0\fi0\b Heading 3;}
{\s14\sbasedon11\snext2\keepn{\*\txttags title4}\f1\fs24\ql\sb240\sa240\sl480\slmult1\li360\ri0\fi0\b\i Heading 4;}
{\s15\sbasedon11\snext2\keepn{\*\txttags title5}\f1\fs24\ql\sb240\sa240\sl480\slmult1\li360\ri0\fi0\i Heading 5;}
{\s21\sbasedon2\snext21{\*\txttags list}\f0\fs24\qj\sb0\sa0\sl480\slmult1{\*\txttags list indent}\li720\ri0\fi-360 List;}
}
{\*\listtable
{\list\listtemplateid1
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li720\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li1080\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li1440\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li1800\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li2160\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li2520\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li2880\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li3240\ri0\fi-360}
{\listlevel\levelnfc23\leveljc0\levelstartat1\levelfollow0{\leveltext \'01\'95;}{\levelnumbers;}{\*\txttags list indent}\li3600\ri0\fi-360}
\listid1}
{\list\listtemplateid2
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'00.;}{\levelnumbers\'01;}{\*\txttags list indent}\li720\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'01.;}{\levelnumbers\'01;}{\*\txttags list indent}\li1080\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'02.;}{\levelnumbers\'01;}{\*\txttags list indent}\li1440\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'03.;}{\levelnumbers\'01;}{\*\txttags list indent}\li1800\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'04.;}{\levelnumbers\'01;}{\*\txttags list indent}\li2160\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'05.;}{\levelnumbers\'01;}{\*\txttags list indent}\li2520\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'06.;}{\levelnumbers\'01;}{\*\txttags list indent}\li2880\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'07.;}{\levelnumbers\'01;}{\*\txttags list indent}\li3240\ri0\fi-360}
{\listlevel\levelnfc0\leveljc0\levelstartat1\levelfollow0{\leveltext \'02\'08.;}{\levelnumbers\'01;}{\*\txttags list indent}\li3600\ri0\fi-360}
\listid2}
{\list\listtemplateid3
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'02\'00.;}{\levelnumbers\'01;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'04\'00.\'01.;}{\levelnumbers\'01\'03;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'06\'00.\'01.\'02.;}{\levelnumbers\'01\'03\'05;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'08\'00.\'01.\'02.\'03.;}{\levelnumbers\'01\'03\'05\'07;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'10\'00.\'01.\'02.\'03.\'04.;}{\levelnumbers\'01\'03\'05\'07\'09;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'02\'05.;}{\levelnumbers\'01;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'02\'06.;}{\levelnumbers\'01;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow1{\leveltext \'02\'07.;}{\levelnumbers\'01;}}
{\listlevel\levelnfc0\leveljc1\levelstartat1\levelfollow0{\leveltext \'02\'08.;}{\levelnumbers\'01;}}
\listid3}
}
{\listoverridetable
{\listoverride\listid1\listoverridecount0\ls1}
{\listoverride\listid2\listoverridecount0\ls2}
{\listoverride\listid3\listoverridecount0\ls3}
}
{\info
{\title %(HEADER1)s }
{\author %(HEADER2)s }
}
\deflang1033\widowctrl\hyphauto\uc1\fromtext
\paperw12240\paperh15840
\margl1440\margr1440\margt1440\margb1440
\sectd
{\header\pard\qr\plain\f0 Page \chpgn\par}
{\pard\plain\s10\keepn{\*\txttags maintitle}\f1\fs24\qc\sb2880\sa0\sl480\slmult1\li0\ri0\fi0 %(HEADER1)s\par}
{\pard\plain\s10\keepn{\*\txttags maintitle}\f1\fs24\qc\sb0\sa0\sl480\slmult1\li0\ri0\fi0 %(HEADER2)s\par}
{\pard\plain\s10\keepn{\*\txttags maintitle}\f1\fs24\qc\sb0\sa0\sl480\slmult1\li0\ri0\fi0 %(HEADER3)s\par}
"""

# http://en.wikipedia.org/wiki/Rich_Text_Format
# Based on RTF Version 1.5 specification
# Should be compatible with MS Word 97 and newer
# ~D~ and ~L~ are used to encode depth and nesting level formatting
TAGS = {
    'title1'                : '~A~{\\pard\\plain\\s11\\keepn{\\*\\txttags title1}\\f1\\fs24\\qc\\sb240\\sa240\\sl480\\slmult1\\li0\\ri0\\fi0{\\b{\a}}\\par}',
    'title2'                : '~A~{\\pard\\plain\\s12\\keepn{\\*\\txttags title2}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li0\\ri0\\fi0{\\b{\a}}\\par}',
    'title3'                : '~A~{\\pard\\plain\\s13\\keepn{\\*\\txttags title3}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0{\\b{\a}}\\par}',
    'title4'                : '~A~{\\pard\\plain\\s14\\keepn{\\*\\txttags title4}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0{\\b\\i{\a}}\\par}',
    'title5'                : '~A~{\\pard\\plain\\s15\\keepn{\\*\\txttags title5}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0{\\i{\a}}\\par}',
    'numtitle1'             : '~A~{\\pard\\plain\\s11\\keepn{\\*\\txttags title1}\\f1\\fs24\\qc\\sb240\\sa240\\sl480\\slmult1\\li0\\ri0\\fi0\\ls3\\ilvl0{\\b{\a}}\\par}',
    'numtitle2'             : '~A~{\\pard\\plain\\s12\\keepn{\\*\\txttags title2}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li0\\ri0\\fi0\\ls3\\ilvl1{\\b{\a}}\\par}',
    'numtitle3'             : '~A~{\\pard\\plain\\s13\\keepn{\\*\\txttags title3}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0\\ls3\\ilvl2{\\b{\a}}\\par}',
    'numtitle4'             : '~A~{\\pard\\plain\\s14\\keepn{\\*\\txttags title4}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0\\ls3\\ilvl3{\\b\\i{\a}}\\par}',
    'numtitle5'             : '~A~{\\pard\\plain\\s15\\keepn{\\*\\txttags title5}\\f1\\fs24\\ql\\sb240\\sa240\\sl480\\slmult1\\li360\\ri0\\fi0\\ls3\\ilvl4{\\i{\a}}\\par}',
    'paragraphOpen'         : '{\\pard\\plain\\s2{\\*\\txttags paragraph}\\f0\\fs24\\qj\\sb0\\sa0\\sl480\\slmult1\\li~D~\\ri0\\fi360',
    'paragraphClose'        : '\\par}',
    'blockVerbOpen'         : '{\\pard\\plain\\s3{\\*\\txttags verbatim}\\f2\\fs20\\ql\\sb0\\sa240\\sl240\\slmult1\\li720\\ri720\\fi0',
    'blockVerbSep'          : '\\line',
    'blockVerbClose'        : '\\par}',
    'blockQuoteOpen'        : '{\\pard\\plain\\s4{\\*\\txttags quote}\\f0\\fs24\\qj\\sb0\\sa0\\sl480\\slmult1\\li~D~\\ri720\\fi0',
    'blockQuoteClose'       : '\\par}',
    'fontMonoOpen'          : '{\\f2\\fs20{',
    'fontMonoClose'         : '}}',
    'fontBoldOpen'          : '{\\b{',
    'fontBoldClose'         : '}}',
    'fontItalicOpen'        : '{\\i{',
    'fontItalicClose'       : '}}',
    'fontUnderlineOpen'     : '{\\ul{',
    'fontUnderlineClose'    : '}}',
    'fontStrikeOpen'        : '{\\strike{',
    'fontStrikeClose'       : '}}',
    'anchor'                : '{\\*\\bkmkstart \a}{\\*\\bkmkend \a}',
    # 'comment'               : '{\\v \a }',  # doesn't hide text in all readers
    'pageBreak'             : '\\page\n',
    'EOD'                   : '}',
    'url'                   : '{\\field{\\*\\fldinst{HYPERLINK "\a"}}{\\fldrslt{\\ul\\cf1 \a}}}',
    'urlMark'               : '{\\field{\\*\\fldinst{HYPERLINK "\a"}}{\\fldrslt{\\ul\\cf1 \a}}}',
    'email'                 : '{\\field{\\*\\fldinst{HYPERLINK "mailto:\a"}}{\\fldrslt{\\ul\\cf1 \a}}}',
    'emailMark'             : '{\\field{\\*\\fldinst{HYPERLINK "mailto:\a"}}{\\fldrslt{\\ul\\cf1 \a}}}',
    'img'                   : '{\\field{\\*\\fldinst{INCLUDEPICTURE "\a" \\\\* MERGEFORMAT \\\\d}}{\\fldrslt{(\a)}}}',
    'imgEmbed'              : '{\*\shppict{\pict\a}}',
    'listOpen'              : '{\\pard\\plain\\s21{\\*\\txttags list}\\f0\\fs24\\qj\\sb0\\sa0\\sl480\\slmult1',
    'listClose'             : '}',
    'listItemOpen'          : '{\\*\\listtext{\\*\\txttags list indent}\\li~D~\\ri0\\fi-360\\\'95\\tab}\\ls1\\ilvl~L~{\\*\\txttags list indent}\\li~D~\\ri0\\fi-360\n',
    'listItemClose'         : '\\par',
    'numlistOpen'           : '{\\pard\\plain\\s21{\\*\\txttags list}\\f0\\fs24\\qj\\sb0\\sa0\\sl480\\slmult1',
    'numlistClose'          : '}',
    'numlistItemOpen'       : '{\\*\\listtext{\\*\\txttags list indent}\\li~D~\\ri0\\fi-360 \a.\\tab}\\ls2\\ilvl~L~{\\*\\txttags list indent}\\li~D~\\ri0\\fi-360\n',
    'numlistItemClose'      : '\\par',
    'deflistOpen'           : '{\\pard\\plain\\s21{\\*\\txttags list}\\f0\\fs24\\qj\\sb0\\sa0\\sl480\\slmult1',
    'deflistClose'          : '}',
    'deflistItem1Open'      : '{\\*\\txttags list indent}\\li~D~\\ri0\\fi-360{\\b\n',
    'deflistItem1Close'     : ':}\\tab',
    'deflistItem2Open'      : '',
    'deflistItem2Close'     : '\\par',
    'tableOpen'             : '{\\pard\\plain',
    'tableClose'            : '\\par}',
    'tableRowOpen'          : '{\\trowd\\trgaph60~A~~B~',
    'tableRowClose'         : '\\row}',
    'tableRowSep'           : '',
    'tableTitleRowOpen'     : '{\\trowd\\trgaph60\\trhdr~A~~B~\\trbrdrt\\brdrs\\brdrw20\\trbrdrb\\brdrs\\brdrw20',
    'tableTitleRowClose'    : '',
    'tableCellOpen'         : '{\\intbl\\itap1\\f0\\fs20~A~ ',
    'tableCellClose'        : '\\cell}',
    'tableCellHead'         : '~B~~S~',
    'tableTitleCellOpen'    : '{\\intbl\\itap1\\f0\\fs20~A~\\b ',
    'tableTitleCellClose'   : '\\cell}',
    'tableTitleCellHead'    : '~B~\\clbrdrt\\brdrs\\brdrw20\\clbrdrb\\brdrs\\brdrw20~S~',
    '_tableCellColSpan'     : '\\cellx\a',
    '_tableAlignLeft'       : '\\trql',
    '_tableAlignCenter'     : '\\trqc',
    '_tableBorder'          : '\\trbrdrt\\brdrs\\brdrw10\\trbrdrb\\brdrs\\brdrw10\\trbrdrl\\brdrs\\brdrw10\\trbrdrr\\brdrs\\brdrw10',
    '_tableCellAlignLeft'   : '\\ql',
    '_tableCellAlignRight'  : '\\qr',
    '_tableCellAlignCenter' : '\\qc',
    '_tableCellBorder'      : '\\clbrdrt\\brdrs\\brdrw10\\clbrdrb\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10',
    'bar1'                  : '{\\pard\\plain\\s1\\brdrt\\brdrs\\brdrw10\\li1400\\sb120\\sa120\\ri1400\\fs12\\par}',
    'bar2'                  : '{\\pard\\plain\\s1\\brdrt\\brdrs\\brdrdb\\brdrw10\\sb120\\sa120\\li1400\\ri1400\\fs12\\par}'
}

RULES = {
    'linkable': 1,
    'tableable': 1,
    'autonumbertitle': 1,
    'parainsidelist': 1,
    'listnotnested': 1,
    'listitemnotnested': 1,
    'quotenotnested': 1,
    'onelinepara': 1,
    'tablecellstrip': 1,
    'tablecellspannable': 1,
    'tagnotindentable': 1,
    'deflisttextstrip': 1,
    'encodeblockdepth': 1,
    'zerodepthparagraph': 1,
    'cellspancumulative': 1,
    'blockdepthmultiply': 360,
    'depthmultiplyplus': 1,
    'cellspanmultiplier': 1080,
    'listmaxdepth': 9,
    'tablecellaligntype': 'cell',
}

ESCAPES = [('\t', 'vvvvRtfTabvvvv', '\x00' + 'tab')]
