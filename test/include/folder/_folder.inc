
Folder - Level 1.
%!include: folder/subfolder/_folder.inc
%%%
This is WRONG! It should be:

%!include: subfolder/_folder.inc

But txt2tags considers "current path" the path for the mother .t2t file
(../include-nesting-folder.t2t)

Funny thing is that %!includeconf do not suffer from this bug. See ConfigLines.include_config_file()
%%%
