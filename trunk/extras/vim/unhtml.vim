" unhtml.vim - by Aurelio Jargas
" - Converts HTML tags into txt2tags marks
" - Part of the txt2tags <http://txt2tags.org> software
"
" INSTRUCTIONS
"   1. Open the HTML file on Vim and execute
"        :so /path/to/unhtml.vim
"
"   2. A new <yourfile>.html.t2t will be saved.
"
"   3. Check the new .t2t file and correct by hand what has left.
"

""" [ preparing ]
" ignore case
set ic
" join multiline tags
g/<\s*\([ap]\|img\)\s*$/join
g/<\s*a\s[^>]*>[^<]*$/join


""" [ do it! ]
" link
%s,<\s*a\s[^>]*href="\(.\{-}\)"[^>]*>\(.\{-}\)<\/a>,[\2 \1],ge
%s,<\s*a\s[^>]*href=\([^ >]\+\)[^>]*>\(.\{-}\)<\/a>,[\2 \1],ge
" images
%s,<\s*img\s[^>]*src="\(.\{-}\)"[^>]*>,[\1],ge
%s,<\s*img\s[^>]*src=\([^ >]\+\)[^>]*>,[\1],ge
" anchor
%s,^<\s*a\s\+name=.\{-}>\(.*\)<\/a>,== \1 ==,ge
" comments
%s,\s*<!--\(.*\)-->,\% \1,ge

/<!--/,/-->/s,^,\% ,e
" paragraph
%s,<\s*p\(\s[^>]*\)\=\s*>,
,ge
" bar
%s,<\s*hr[^>]*>,-------------------------------------------------,ge
" title
%s,</\=\s*h1\s*>,=,ge
%s,</\=\s*h2\s*>,==,ge
%s,</\=\s*h3\s*>,===,ge
%s,</\=\s*h4\s*>,====,ge
%s,</\=\s*h5\s*>,=====,ge
%s,</\=\s*h6\s*>,=====,ge
" beautifiers
%s,</\=\s*code\s*>,``,ge
%s,</\=\s*\(b\|strong\)\s*>,**,ge
%s,</\=\s*\(i\|em\)\s*>,//,ge
%s,</\=\s*u\s*>,__,ge
%s,</\=\s*s\s*>,--,ge
" pre
%s,</\=\s*pre\s*>,
```
,ge
" bullet/numbered list
%s,<\s*li\s*>,- ,ge
%s,</\s*li\s*>,,ge
%s,<\s*[uo]l\s*>,,ge
%s,</\s*[uo]l\s*>,

,ge
" definition list
%s,<\s*dl\s*>,,ge
%s,</\s*dl\s*>,

,ge
%s,<\s*dt\s*>,: ,ge
%s,</\s*dt\s*>,
,ge
%s,</\=\s*dd\s*>,,ge
" BR is ignored
%s,<\s*br\s*/*>,
,ge
" trash
%s,</\s*font[^>]*\s*>,,ge
%s,</\s*p\s*>,,ge
%s,</\s*a\s*>,,ge
%s,</\=\s*blink\s*>,,ge
%s,<\s*a\s\+name=[^>]*>,,ge
%s,</\=\s*\(html\|body\|head\|title\)\(\s[^>]*\)\=\s*>,,ge
" mmmmm, dangerous! it removes all remaining HTML tags
"%s,<[^>]*>,,ge
" clear just-blanks lines
%s,^\s*$,,
" special entities
%s,&quot;,",ge
%s,&amp;,\&,ge
%s,&gt;,>,ge
%s,&lt;,<,ge
%s,&nbsp;, ,ge

" save new .t2t file and turn on syntax
saveas! %.t2t | set ft=txt2tags
