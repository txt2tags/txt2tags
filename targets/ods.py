"""
An Open Document Spreadsheet target.
"""

from targets import _

NAME = _('Open Document Spreadsheet')

TYPE = 'office'

HEADER = """\
<?xml version='1.0' encoding='%(ENCODING)s'?>
<office:document xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.1" office:mimetype="application/vnd.oasis.opendocument.spreadsheet"><office:meta><meta:generator>Txt2tags www.txt2tags.org</meta:generator></office:meta><office:automatic-styles/><office:body><office:spreadsheet>
"""

TAGS = {
    'tableOpen'            : '<table:table table:name="' + _('Sheet') + 'n_table">',
    'tableClose'           : '</table:table>'                  ,
    'tableRowOpen'         : '<table:table-row>'               ,
    'tableRowClose'        : '</table:table-row>'              ,
    'tableCellOpen'        : '<table:table-cell><text:p>'      ,
    'tableCellClose'       : '</text:p></table:table-cell>'    ,
    'EOD'                  : '</office:spreadsheet></office:body></office:document>',
}

RULES = {
    'escapexmlchars': 1,
    'tableable': 1,
    'tableonly': 1,
    'tablecellstrip': 1,
    'tablenumber': 1,
}
