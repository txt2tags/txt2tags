" Vim syntax file
" Filename: txt2tags.vim
" Language: marked text for conversion by txt2tags
" Maintainer: Aurelio Jargas
" Last change: 2010-10-22 - Added new targets for v2.6
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" INFO:
"
" - This is the txt2tags VIM syntax file.
" - It's a syntax file just like those for programming languages as C
"   or Python, so you know it's handy.
" - Here are registered all the structures for txt2tags marks.
" - When composing your text file, the marks will be highlighted,
"   helping you to quickly make error-free txt2tags files.
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" FOLD:
"
" - There are some folding rules on the syntax also
" - To use fold just uncomment the line of foldmethod below
" - Or set the fold use directly on the t2t file, adding this last line:
"
"     % vim: foldmethod=syntax
"
" - There are two kinds of fold:
"
"   Automatic fold:
"     - The fold starts at any top level title
"     - The fold ends with 3 consecutive blank lines
"
"   User defined fold:
"     - The fold starts by the "% label {{{" comment
"     - The fold ends with the "% }}}" comment
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" INSTALL: (as user)
"
" - Copy this file to the ~/.vim/syntax/ dir (create it if necessary)
"
" - Put in your .vimrc the following line:
"   au BufNewFile,BufRead *.t2t set ft=txt2tags
"
" If you use other extension for txt2tags files, change the '*.t2t'
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" INSTALL: (as superuser)
"
" If you have access to the system configuration, edit the
" /usr/share/vim/vim*/filetype.vim file, adding the following
" lines after the 'Z-Shell script' entry (near the end):
"
"   " txt2tags file
"   au BufNewFile,BufRead *.t2t                 setf txt2tags
"
" And copy this file (txt2tags.vim) to the Vim syntax dir:
"
"   /usr/share/vim/vim*/syntax/
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"FOLD: just uncomment the following line if you like to use Vim fold
"set foldmethod=syntax


" init
syn clear
syn sync minlines=500
syn case ignore

"TODO see if user already has foldmethod defined, if so, set foldmethod=syntax
"TODO2 learn vim language :/

syn cluster t2tComponents  contains=t2tNumber,t2tPercent,t2tMacro,t2tImg,t2tEmail,t2tUrl,t2tUrlMark,t2tUrlMarkImg,t2tUrlLocal
syn cluster t2tBeautifiers contains=t2tStrike,t2tUnderline,t2tItalic,t2tBold,t2tMonospace,t2tRaw

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"LIST:
syn match t2tList    '^ *[-+:]\s*$'
syn match t2tList    '^ *: '
syn match t2tList    '^ *[+-] [^ ]'me=e-1

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"TITLE:
syn match t2tTitleRef  contained '\[[a-z0-9_-]*\]\s*$'
syn match t2tTitleMark contained '^ *=\+'
syn match t2tTitleMark contained '=\+\s*$'
syn match t2tTitleMark contained '=\+\['me=e-1,he=e-1
syn match t2tTitle '^ *\(=\{1,5}\)[^=]\(\|.*[^=]\)\1\(\[[a-z0-9_-]*\]\)\=\s*$' contains=t2tTitleMark,t2tTitleRef

syn match t2tNumTitleMark contained '^ *+\+'
syn match t2tNumTitleMark contained '+\+\s*$'
syn match t2tNumTitleMark contained '+\+\['me=e-1,he=e-1
syn match t2tNumTitle '^ *\(+\{1,5}\)[^+]\(\|.*[^+]\)\1\(\[[a-z0-9_-]*\]\)\=\s*$' contains=t2tNumTitleMark,t2tTitleRef

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"URL EMAIL:
"syn case match
syn match t2tEmail '\<[A-Za-z0-9_.-]\+@\([A-Za-z0-9_-]\+\.\)\+[A-Za-z]\{2,4}\>\(?[A-Za-z0-9%&=+.,@*_-]\+\)\='
syn match t2tUrl   '\<\(\(https\=\|ftp\|news\|telnet\|gopher\|wais\)://\([A-Za-z0-9._-]\+\(:[^ @]*\)\=@\)\=\|\(www[23]\=\.\|ftp\.\)\)[A-Za-z0-9%._/~:,=$@&-]\+\>/*\(?[A-Za-z0-9/%&=+;.,@*_-]\+\)\=\(#[A-Za-z0-9%._-]\+\)\='
syn match t2tUrlLocal contained ' \([A-Za-z0-9%._/~,-]\+\|[A-Za-z0-9%._/~,-]*#[A-Za-z0-9%._-]\+\)\]'ms=s+1,me=e-1
syn match t2tUrlMark '\[[^]]\+ [^] ]\+\]' contains=t2tUrlLabel,t2tUrl,t2tEmail,t2tUrlLocal
syn match t2tUrlMarkImg '\[\[[[:alnum:]_,.+%$#@!?+~/-]\+\.\(png\|jpe\=g\|gif\|eps\|bmp\)\( \+"[^"]*"\)\{0,1\}\] [^] ]\+\]' contains=t2tUrl,t2tEmail,t2tUrlLocal,t2tImg
syn match t2tUrlLabel contained '\[[^]]\+ 'ms=s+1,me=e-1

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"FONT BEAUTIFIERS:
syn match   t2tBold       '\*\*\S\(\|.\{-}\S\)\*\*\+'hs=s+2,he=e-2
syn match   t2tItalic       '//\S\(\|.\{-}\S\)//\+'hs=s+2,he=e-2
syn match   t2tUnderline    '__\S\(\|.\{-}\S\)__\+'hs=s+2,he=e-2
syn match   t2tStrike       '--\S\(\|.\{-}\S\)--\+'hs=s+2,he=e-2
syn match   t2tMonospace    '``\S\(\|.\{-}\S\)``\+'hs=s+2,he=e-2
syn match   t2tRaw          '""\S\(\|.\{-}\S\)""\+'hs=s+2,he=e-2
syn match   t2tTagged       "''\S\(\|.\{-}\S\)''\+"hs=s+2,he=e-2
syn match   t2tVerb1Line     '^``` .*$'hs=s+3
syn match   t2tRaw1Line      '^""" .*$'hs=s+3
syn match   t2tTagged1Line   "^''' .*$"hs=s+3
syn region  t2tVerbArea     start='^```\s*$'hs=s+3 end='^```\s*$'he=e-3
syn region  t2tRawArea      start='^"""\s*$'hs=s+3 end='^"""\s*$'he=e-3
syn region  t2tTaggedArea   start="^'''\s*$"hs=s+3 end="^'''\s*$"he=e-3
syn match   t2tComment '^%.*$' contains=t2tTodo,t2tFoldMark,t2tIncluded
syn region  t2tCommentArea  start="^%%%\s*$" end="^%%%\s*$"

"Experimental
syn region  t2tTableArea  start="^|||\s*$" end="^|||\s*$" contains=t2tTableTab,t2tComment
syn match   t2tTableTab '\t' contained
"hi t2tTableTab    term=reverse     cterm=reverse     gui=reverse
"hi link t2tTableArea  Statement
set list listchars=tab:··


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"TABLE:
syn match   t2tTableAlign contained ' \+$'
syn match   t2tTableMark  contained '^ *[^ ]\+'
syn match   t2tTableBar   contained ' |\+ '     contains=t2tBlank
syn match   t2tTableBar   contained '|\+\s*$'   contains=t2tBlank
syn match   t2tTableTit   contained '^ *||.*' contains=t2tTableMark,t2tTableBar,t2tTableAlign
syn match   t2tTable             '^ *||\= .*' contains=t2tTableMark,t2tTableBar,t2tTableTit,@t2tBeautifiers,@t2tComponents,t2tTableAlign

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"MISC:
syn keyword t2tTodo    TODO FIXME XXX contained
syn match   t2tNumber  '\<\d\+\([,.]\d\+\)\{,1}\>'
syn match   t2tPercent '\<\d\+\([,.]\d\+\)\{,1}%'
syn match   t2tBlank   '\s\+$'
syn match   t2tQuote   '^\t\+'
syn match   t2tBar     '^\s*[_=-]\{20,}\s*$' contains=t2tQuote
syn match   t2tImg     '\[[[:alnum:]_,.+%$#@!?+~/-]\+\.\(png\|jpe\=g\|gif\|eps\|bmp\)\( \+"[^"]*"\)\{0,1\}\]'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"MACROS AND COMMANDS:
"syn match   t2tMacro    '%%[a-z]\+'
syn match   t2tMacro    '%%\(date\|mtime\|infile\|outfile\)\>\(([^)]*)\)\='
syn match   t2tMacro    '^ *%%toc\s*$'
syn match   t2tIncluded '^%INCLUDED([a-z2]\+)'ms=s+1 contained 
syn match   t2tIncluded '^%--\{10,} Area Delimiter:'ms=s+1 contained 
syn match   t2tCommand  "^%!\s*include\s*\((\(\|txt\|html\|xhtml\|sgml\|lout\|tex\|mgp\|man\|moin\|pm6\|wiki\|gwiki\|doku\))\)\=\s*:\s*\S"me=e-1 contains=t2tTargets

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"FOLD:
syn match  t2tFoldMark '\({{{\|}}}\)$'
syn region t2tUserFold keepend transparent fold start='^%.\+{{{$' end='^%.*}}}$'
syn region t2tTitleFold    transparent fold start='^ *=[^=].*[^=]=\(\[[a-z0-9_-]*\]\)\=\s*$' end='\n\n\n\n'
syn region t2tNumtitleFold transparent fold start='^ *+[^+].*[^+]+\(\[[a-z0-9_-]*\]\)\=\s*$' end='\n\n\n\n'
"heavy-folding-users: uncomment the following to fold *every* subtitle area
"syn region t2tTitleFoldDeep transparent fold start='^ *\(=\{2,5}\)[^=].*[^=]\1$' end='\n\n\n\n'
"syn region t2tNumtitleFoldDeep transparent fold start='^ *\(+\{2,5}\)[^+].*[^+]\1$' end='\n\n\n\n'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"HEADERS AND CONFIG:
"Headers are the first 3 lines
"Config are special comments right after the headers
"Config Area ends on a no-comment and no-blank line
syn keyword t2tTargets    contained txt xhtml html sgml tex lout mgp man
syn keyword t2tTargets    contained moin pm6 wiki gwiki doku dbk creole
syn keyword t2tTargets    contained pmw adoc art
syn match t2tConfigString contained +"[^"]*"\|'[^']*'+
syn match t2tConfigValue  contained ':.*'ms=s+1 contains=t2tConfigString
syn match t2tConfigKey    contained '^%![^:]\+:' contains=t2tTargets
syn match t2tConfigLine   contained "^%!\s*\(encoding\|style\|preproc\|postproc\|includeconf\|options\)\s*\((\s*\(\|txt\|html\|xhtml\|sgml\|tex\|lout\|mgp\|man\|moin\|pm6\|wiki\|gwiki\|doku\|dbk\|creole\|pmw\|adoc\|art\)\s*)\)\=\s*:\s*\S.*" contains=t2tConfigKey,t2tConfigValue,t2tConfigString
syn match t2tConfigLine   contained "^%!\s*target\s*:\s*\S.*" contains=t2tConfigKey,t2tTargets
syn match t2tConfigLine   contained "^%!\s*guicolors\s*:\s*\(\S\+\s\+\)\{3}\S\+\s*$" contains=t2tConfigKey,t2tTargets

syn match  t2tHeaderArea  contained '\%^.*\n.*\n.*$' contains=t2tMacro
syn region t2tConfigArea         contained start='\%4l' end='^\%>3l[^%]'me=e-1 end='^\%>3l%!include[^c]'me=e-10 end='%%\(date\|mtim\|infi\|outf\)'me=e-6 contains=t2tComment,t2tConfigLine,t2tConfig1
syn region t2tConfigAreaNoHeader contained start='\%2l' end='^\%>1l[^%]'me=e-1 end='^\%>1l%!include[^c]'me=e-10 end='%%\(date\|mtim\|infi\|outf\)'me=e-6 contains=t2tComment,t2tConfigLine,t2tConfig1


syn region t2tTopArea       start='\%^\s*\S' end='^[^%]'me=e-1 end='^%!include[^c]'me=e-10 end='%%\(date\|mtim\|infi\|outf\)'me=e-6 contains=t2tHeaderArea,t2tConfigArea
syn region t2tTopAreaNoHead start='\%^\s*$'  end='^[^%]'me=e-1 end='^%!include[^c]'me=e-10 end='%%\(date\|mtim\|infi\|outf\)'me=e-6 contains=t2tConfigAreaNoHeader

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"
" color groups
hi default link t2t_Link       PreProc
hi default link t2t_Component  Statement
hi default link t2t_Delim      Identifier
hi default link t2t_Verb       Type
hi default link t2t_Raw        String
hi default link t2t_Tagged     Special
"
" color definitions (specific)
hi default t2tBar         term=bold        cterm=bold        gui=bold
hi default t2tBold        term=bold        cterm=bold        gui=bold
hi default t2tItalic      term=italic      cterm=italic      gui=italic
hi default t2tStrike      term=italic      cterm=italic      gui=italic
hi default t2tUnderline   term=underline   cterm=underline   gui=underline
hi default t2tQuote       term=reverse     cterm=reverse     gui=reverse
hi default t2tTableAlign  term=reverse     cterm=reverse     gui=reverse
if &background == "light"
    hi default t2tComment     ctermfg=brown    guifg=brown
else
    hi default t2tComment     ctermfg=brown    guifg=bisque
endif
hi default link t2tCommentArea t2tComment 
"
" color definitions (using Vim defaults)
hi default link t2tTitle         Error
hi default link t2tNumTitle      Error
" comment the following line to avoid having trailing whitespaces in red
hi default link t2tBlank         Error
hi default link t2tNumber        Number
hi default link t2tPercent       Number
hi default link t2tFoldMark      Special
hi default link t2tTodo          Todo
hi default link t2tCommand       Special
hi default      t2tIncluded      cterm=bold
hi default link t2tTargets       Type
hi default link t2tConfigKey     Special
hi default link t2tConfigValue   NONE
hi default link t2tConfigString  String
hi default link t2tHeaderArea    t2t_Raw
hi default link t2tUrlMark       t2t_Delim
hi default link t2tUrlMarkImg    t2t_Delim
hi default link t2tUrlLabel      t2t_Delim
hi default link t2tTableTit      t2t_Delim
hi default link t2tTableMark     t2t_Delim
hi default link t2tTableBar      t2t_Delim
hi default link t2tEmail         t2t_Link
hi default link t2tUrl           t2t_Link
hi default link t2tUrlLocal      t2t_Link
hi default link t2tTitleRef      t2t_Link
hi default link t2tMacro         t2t_Component
hi default link t2tImg           t2t_Component
hi default link t2tList          t2t_Component
hi default link t2tMacro         t2t_Component
hi default link t2tTitleMark     NONE
hi default link t2tVerbArea      t2t_Verb
hi default link t2tVerb1Line     t2t_Verb
hi default link t2tMonospace     t2t_Verb
hi default link t2tRaw           t2t_Raw
hi default link t2tRaw1Line      t2t_Raw
hi default link t2tRawArea       t2t_Raw
hi default link t2tTagged        t2t_Tagged
hi default link t2tTagged1Line   t2t_Tagged
hi default link t2tTaggedArea    t2t_Tagged

"
let b:current_syntax = 'txt2tags'
" vim:tw=0:et
