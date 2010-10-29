
Folder - Level 2.
%!include: folder/_folder-back.inc
%%%
This is WRONG! It should be:

%!include: ../_folder-back.inc

But txt2tags considers "current path" the path for the mother .t2t file
(../../include-nesting-folder-back.t2t)

Another problem is that the "include itself" check fails in this situation.

Funny thing is that %!includeconf do not suffer from this bug. See ConfigLines.include_config_file()
%%%
