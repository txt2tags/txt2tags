local $/;
require 't/runtests.pl';
runtests( data => <DATA>, dialect => 'DokuWiki', wiki_uri => 'http://www.test.com/wiki:', camel_case => 1 );
close DATA;

__DATA__
table
__H__
<table><tr><td>thing</td></tr></table>
__W__
| thing |
__NEXT__
table (multi-row)
__H__
<table>
<tr><td>one</td></tr>
<tr><td>two</td></tr>
</table>
__W__
| one |
| two |
__NEXT__
table (full 1)
__H__
<table>
<tr><th class="centeralign" colspan="3">Table with alignment</th></tr>
<tr><td class="rightalign">right</td><td class="centeralign">center</td><td class="leftalign">left</td></tr>
<tr><td class="leftalign">left</td><td class="rightalign">right</td><td class="centeralign">center</td></tr>
<tr><td>xxxxxxxxxxxx</td><td>xxxxxxxxxxxx</td><td>xxxxxxxxxxxx</td></tr>
</table>
__W__
^  Table with alignment  ^^^
|  right |  center  | left  |
| left  |  right |  center  |
| xxxxxxxxxxxx | xxxxxxxxxxxx | xxxxxxxxxxxx |
__NEXT__
table (full 2)
__H__
<table>
<tr><th class="leftalign">Heading 1</th><th class="leftalign">Heading 2</th><th class="leftalign">Heading 3</th></tr>
<tr><td class="leftalign">Row 1 Col 1</td><td class="leftalign">Row 1 Col 2</td><td class="leftalign">Row 1 Col 3</td></tr>
<tr><td class="leftalign">Row 2 Col 1</td><td colspan="2">some colspan (note the double pipe)</td></tr>
<tr><td class="leftalign">Row 3 Col 1</td><td class="leftalign">Row 2 Col 2</td><td class="leftalign">Row 2 Col 3</td></tr>
</table>
__W__
^ Heading 1  ^ Heading 2  ^ Heading 3  ^
| Row 1 Col 1  | Row 1 Col 2  | Row 1 Col 3  |
| Row 2 Col 1  | some colspan (note the double pipe) ||
| Row 3 Col 1  | Row 2 Col 2  | Row 2 Col 3  |
__NEXT__
table (full 3)
__H__
<table>
<tr><th>name</th><td>foo</td></tr>
<tr><th>age</th><td>3.14</td></tr>
<tr><th>odd</th><td>true</td></tr>
</table>
__W__
^ name | foo |
^ age | 3.14 |
^ odd | true |
__NEXT__
h1
__H__
<h1>one</h1>
__W__
====== one ======
__NEXT__
h2
__H__
<h2>two</h2>
__W__
===== two =====
__NEXT__
h3
__H__
<h3>three</h3>
__W__
==== three ====
__NEXT__
h4
__H__
<h4>four</h4>
__W__
=== four ===
__NEXT__
h5
__H__
<h5>five</h5>
__W__
== five ==
__NEXT__
h6
__H__
<h6>six</h6>
__W__
== six ==
__NEXT__
external image
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" />
__W__
{{http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png}}
__NEXT__
external image (resize width)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" width="25" />
__W__
{{http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png?25}}
__NEXT__
external image (resize width and height)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" width="25" height="30" />
__W__
{{http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png?25x30}}
__NEXT__
external image align (left)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" class="medialeft" />
__W__
{{http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png }}
__NEXT__
external image align (right)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" class="mediaright" />
__W__
{{ http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png}}
__NEXT__
external image align (center)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" class="mediacenter" />
__W__
{{ http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png }}
__NEXT__
external image align (center w/ caption)
__H__
<img src="http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png" class="mediacenter" alt="Caption" />
__W__
{{ http://wiki.splitbrain.org/fetch.php?w=&h=&cache=cache&media=wiki:dokuwiki-128.png |Caption}}
__NEXT__
blockquote
__H__
<blockquote>one</blockquote>
__W__
> one
__NEXT__
blockquote (nested)
__H__
<blockquote><blockquote>two</blockquote></blockquote>
__W__
>> two
__NEXT__
blockquote (multi-line)
__H__
<blockquote>span
single
line</blockquote>
__W__
> span single line
__NEXT__
blockquote (nested multi-line)
__H__
<blockquote><blockquote>span
single
line</blockquote></blockquote>
__W__
>> span single line
__NEXT__
blockquote (markup)
__H__
<blockquote><b>with</b> <em>fancy
markup</em> that <u>spans
multiple
lines</u></blockquote>
__W__
> **with** //fancy markup// that __spans multiple lines__
__NEXT__
blockquote (nested continuous)
__H__
<blockquote>one<blockquote>two</blockquote></blockquote>
__W__
> one
>> two
__NEXT__
blockquote (doubly nested continuous)
__H__
<blockquote>one<blockquote>two<blockquote>three</blockquote></blockquote></blockquote>
__W__
> one
>> two
>>> three
__NEXT__
blockquote (linebreak)
__H__
<blockquote>line<br />break</blockquote>
__W__
> line\\ break
__NEXT__
blockquote (full)
__H__
<blockquote>
 No we shouldn't</blockquote>
<blockquote>
<blockquote>
 Well, I say we should</blockquote>
</blockquote>
<blockquote>
 Really?</blockquote>
<blockquote>

<blockquote>
 Yes!</blockquote>
</blockquote>
<blockquote>
<blockquote>
<blockquote>
 Then lets do it!</blockquote>
</blockquote>
</blockquote>
__W__
> No we shouldn't

>> Well, I say we should

> Really?

>> Yes!

>>> Then lets do it!
__NEXT__
internal link (lcase)
__H__
<a href="/wiki:test">test</a>
__W__
[[test]]
__NEXT__
internal link (ucase)
__H__
<a href="/wiki:test">TEST</a>
__W__
[[TEST]]
__NEXT__
internal link (camel case)
__H__
<a href="/wiki:test">tEsT</a>
__W__
tEsT
__NEXT__
external link (anonymous)
__H__
<a href="http://www.test.com">http://www.test.com</a>
__W__
http://www.test.com
__NEXT__
external link (named)
__H__
<a href="http://www.test.com">test</a>
__W__
[[http://www.test.com|test]]
__NEXT__
external link (fragment)
__H__
<a href="/wiki:syntax#internal">this Section</a>
__W__
[[syntax#internal|this Section]]
__NEXT__
linebreak
__H__
line<br />break
__W__
line\\ break
__NEXT__
bold
__H__
<b>bold text</b>
__W__
**bold text**
__NEXT__
strong
__H__
<strong>strong text</strong>
__W__
**strong text**
__NEXT__
italic
__H__
<i>italic text</i>
__W__
//italic text//
__NEXT__
emphasized
__H__
<em>em text</em>
__W__
//em text//
__NEXT__
ul
__H__
<ul>
  <li>one
  <li>two
  <li>three
</ul>
__W__
  * one
  * two
  * three
__NEXT__
ul (nested)
__H__
<ul>
  <li>1
    <ul>
      <li>1.a
      <li>1.b
    </ul>
  </li>
  <li>2
  <li>3
</ul>
__W__
  * 1
    * 1.a
    * 1.b
  * 2
  * 3
__NEXT__
ol
__H__
<ol>
  <li>one
  <li>two
  <li>three
</ol>
__W__
  - one
  - two
  - three
__NEXT__
ol (nested)
__H__
<ol>
  <li>1
    <ol>
      <li>1.a
      <li>1.b
    </ol>
  </li>
  <li>2
  <li>3
</ol>
__W__
  - 1
    - 1.a
    - 1.b
  - 2
  - 3
__NEXT__
ul/ol combo
__H__
<ol>
  <li>1
    <ul>
      <li>1.a
      <li>1.b
    </ul>
  </li>
  <li>2
  <li>3
</ol>
__W__
  - 1
    * 1.a
    * 1.b
  - 2
  - 3
__NEXT__
ol/ul combo
__H__
<ul>
  <li>1
    <ol>
      <li>1.a
      <li>1.b
    </ol>
  </li>
  <li>2
  <li>3
</ul>
__W__
  * 1
    - 1.a
    - 1.b
  * 2
  * 3
