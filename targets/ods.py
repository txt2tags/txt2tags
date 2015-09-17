"""
An Open Document Spreadsheet target.
"""

from targets import _

NAME = _('Open Document Spreadsheet')

TYPE = 'office'

HEADER = """\
<?xml version='1.0' encoding='%(ENCODING)s'?>
<office:document xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.1" office:mimetype="application/vnd.oasis.opendocument.spreadsheet"><office:meta><meta:generator>Txt2tags www.txt2tags.org</meta:generator></office:meta><office:automatic-styles><style:style style:name="T1" style:family="text"><style:text-properties fo:font-weight="bold"/></style:style><style:style style:name="ce1" style:family="table-cell"><style:paragraph-properties fo:text-align="center"/></style:style><style:style style:name="ce2" style:family="table-cell"><style:paragraph-properties fo:text-align="end"/></style:style><style:style style:name="ce3" style:family="table-cell"><style:table-cell-properties fo:border="0.06pt solid #000000"/></style:style><style:style style:name="ce4" style:family="table-cell"><style:paragraph-properties fo:text-align="center"/><style:table-cell-properties fo:border="0.06pt solid #000000"/></style:style><style:style style:name="ce5" style:family="table-cell"><style:paragraph-properties fo:text-align="end"/><style:table-cell-properties fo:border="0.06pt solid #000000"/></style:style></office:automatic-styles><office:body><office:spreadsheet>
"""

TAGS = {
    'tableOpen'            : '<table:table table:name="' + 'table_name' + 'n_table">',
    'tableClose'           : '</table:table>'                  ,
    'tableRowOpen'         : '<table:table-row>'               ,
    'tableRowClose'        : '</table:table-row>'              ,
    'tableCellOpen'        : '<table:table-cell~A~><text:p>'   ,
    'tableCellClose'       : '</text:p></table:table-cell>'    ,
    'tableTitleCellOpen'   : '<table:table-cell~A~><text:p><text:span text:style-name="T1">',
    'tableTitleCellClose'  : '</text:span></text:p></table:table-cell>',
    '_tableCellAlignCenter': ' table:style-name="ce1"',
    '_tableCellAlignRight' : ' table:style-name="ce2"',
    '_tableCellAlignLeftBorder'  : ' table:style-name="ce3"',
    '_tableCellAlignCenterBorder': ' table:style-name="ce4"',
    '_tableCellAlignRightBorder' : ' table:style-name="ce5"',
    'EOD'                  : '</office:spreadsheet></office:body></office:document>',
}

RULES = {
    'escapexmlchars': 1,
    'tableable': 1,
    'tableonly': 1,
    'tablecellstrip': 1,
    'tablecellaligntype': 'cell',
}
