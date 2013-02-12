" Vim syntax file
" Language: pm6
" Maintainer: Aurelio Jargas <verde (a) aurelio net>
" URL: http://txt2tags.org/tools/pagemaker.vim
" Last Change: 20010730

syn clear
syn case ignore

" tags
syn region pm6String   contained start=+"+ end=+"+ keepend
syn region pm6String   contained start=+'+ end=+'+ keepend
syn match  pm6HeaderName contained 'PMTags[0-9.]\+ win' 
syn match  pm6Number '\(^-\|[ \t]-\)\=\<[0-9.-]*[0-9]\>'
syn match  pm6Value    contained "=[\t ]*[^'" \t>][^ \t>]*"hs=s+1
syn match  pm6Special contained '[$()]'
syn match  pm6Bullet  '•'

syn region pm6Tag      matchgroup=pm6TagDelimiter start='<' end='>' contains=pm6String,pm6Value,pm6Number,pm6TagName,pm6HeaderName,pm6Special
syn region pm6StyleDef matchgroup=pm6Style start='<@[^=]*=' skip='<[^>]*>' end='>' contains=pm6Tag,pm6StyleIDK
syn region pm6Comment  matchgroup=pm6TagDelimiter start='<#' end='#>'

syn match  pm6StyleIDK contained '<@-[A-Z]* [^>]*>'
syn match  pm6StyleCall          '<@[^:>]*:>'

" tag names
syn keyword pm6TagName contained ccolor horizontal letterspace ctrack cleading ggrid gleft ghyphenation gspace gknext gkwindow gkorphan gtabs gwordspace cssize cbaseline cnobreak gright gfirst galignment gmethod gpairs gkwidow font gbabove gbbelow gcontents size
syn match pm6TagName contained "\<\(b\|i\|u\|p\)\>"
syn match pm6TagName contained "c[-+]\(size\|position\|colortable\)"
syn match pm6TagName contained "g[-+]\(before\|after\|page\|column\)"
syn match pm6TagName contained "g[&%]"


syn cluster pm6Top contains=pm6Tag,pm6Style

syn region pm6Bold matchgroup=pm6DestakTag start="<b\s*>" end="<[bp]>" end='<@'me=e-2 contains=@pm6Top
syn region pm6Underline matchgroup=pm6DestakTag start="<u\s*>" end="<[up]>" end='<@'me=e-2 contains=@pm6Top
syn region pm6Italic matchgroup=pm6DestakTag start="<i\s*>" end="<[ip]>" end='<@'me=e-2 contains=@pm6Top

hi      pm6TagDelimiter              ctermfg=darkcyan
hi link pm6Style                     Special
hi      pm6TagName                   ctermfg=darkcyan
hi link pm6HeaderName                Special
hi link pm6Style                     Function
hi link pm6StyleIDK                  PreProc
hi link pm6StyleCall                 PreProc
hi      pm6Number                    ctermfg=darkmagenta
hi link pm6Value                     Value
hi      pm6String                    ctermfg=darkgreen
hi link pm6Value                     String
hi link pm6Special                   Statement
hi link pm6DestakTag                 Statement
hi      pm6Bullet                    ctermfg=red

hi      pm6Destak                    ctermfg=white
hi link pm6Bold                      pm6Destak
hi link pm6Italic                    pm6Destak
hi link pm6Underline                 pm6Destak
hi link pm6Comment                   Comment
  
let b:current_syntax = "pm6"
