" Vim Compiler File
" Compiler:	txt2tags
" Maintainer:	Wilson Freitas <wilson.freitas at econofisica dot com dot br>
" Last Change:	05.07.2004
" URL:		http://econofisica.com.br/people/wilson/

if exists("current_compiler")
  finish
endif
let current_compiler = "txt2tags"

if !exists('g:txt2tags_executable')
	let g:txt2tags_executable = "txt2tags"
endif

if !exists('g:txt2tags_options')
	let g:txt2tags_options = " "
endif

map  <F5> :mak<CR><ESC>
map! <F5> <ESC>:mak<CR><ESC>
map  <F4> :copen<CR>
map! <F4> <ESC>:copen<CR>
map  <F3> :ccl<CR>
map! <F3> <ESC>:ccl<CR>

" txt2tags default compiler
let &makeprg = g:txt2tags_executable . " " . g:txt2tags_options . " %"
"setlocal errorformat=%+EERROR:%m,%-E---\ %m,%-Ewrote\ %m
setlocal errorformat=
