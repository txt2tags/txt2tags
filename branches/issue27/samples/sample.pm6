<PMTags1.0 win><C-COLORTABLE ("Preto" 1 0 0 0)
><@Normal=
  <FONT "Times New Roman"><CCOLOR "Preto"><SIZE 11>
  <HORIZONTAL 100><LETTERSPACE 0><CTRACK 127><CSSIZE 70><C+SIZE 58.3>
  <C-POSITION 33.3><C+POSITION 33.3><P><CBASELINE 0><CNOBREAK 0><CLEADING -0.05>
  <GGRID 0><GLEFT 7.2><GRIGHT 0><GFIRST 0><G+BEFORE 7.2><G+AFTER 0>
  <GALIGNMENT "justify"><GMETHOD "proportional"><G& "ENGLISH">
  <GPAIRS 12><G% 120><GKNEXT 0><GKWIDOW 0><GKORPHAN 0><GTABS $>
  <GHYPHENATION 2 34 0><GWORDSPACE 75 100 150><GSPACE -5 0 25>
><@Bullet=<@-PARENT "Normal"><FONT "Abadi MT Condensed Light">
  <GLEFT 14.4><G+BEFORE 2.15><G% 110><GTABS(25.2 l "")>
><@PreFormat=<@-PARENT "Normal"><FONT "Lucida Console"><SIZE 8><CTRACK 0>
  <GLEFT 0><G+BEFORE 0><GALIGNMENT "left"><GWORDSPACE 100 100 100><GSPACE 0 0 0>
><@Title1=<@-PARENT "Normal"><FONT "Arial"><SIZE 14><B>
  <GCONTENTS><GLEFT 0><G+BEFORE 0><GALIGNMENT "left">
><@Title2=<@-PARENT "Title1"><SIZE 12><G+BEFORE 3.6>
><@Title3=<@-PARENT "Title1"><SIZE 10><GLEFT 7.2><G+BEFORE 7.2>
><@Title4=<@-PARENT "Title3">
><@Title5=<@-PARENT "Title3">
><@Quote=<@-PARENT "Normal"><SIZE 10><I>>

TXT2TAGS SAMPLE
Aurelio Jargas
07/26/2008


<@Title1:>Introduction

<@Normal:>
Welcome to the txt2tags sample file.

<@Normal:>
Here you have examples and a brief explanation of all marks.

<@Normal:>
The first 3 lines of the this file are used as headers, on the following format:

<@PreFormat:>
line1: document title
line2: author name, email
line3: date, version

<@Normal:>
Lines with balanced equal signs = around are titles.

<@Title1:>Fonts and Beautifiers

<@Normal:>
We have two sets of fonts:

<@Normal:>
The NORMAL type that can be improved with beautifiers.

<@Normal:>
The TYPEWRITER type that uses monospaced font for pre-formatted text.

<@Normal:>
We will now enter on a subtitle...

<@Title2:>Beautifiers

<@Normal:>
The text marks for beautifiers are simple, just as you type on a plain text email message.

<@Normal:>
We use double *, /, - and _ to represent <B>bold<P>, <I>italic<P>, strike and <U>underline<P>.

<@Normal:>
The <B><I>bold italic<P><P> style is also supported as a combination.

<@Title2:>Pre-Formatted Text

<@Normal:>
We can put a code sample or other pre-formatted text:

<@PreFormat:>
  here    is     pre-formatted
//marks// are  **not**  ``interpreted``

<@Normal:>
And also, it's easy to put a one line pre-formatted text:

<@PreFormat:>
prompt$ ls /etc

<@Normal:>
Or use <FONT "Lucida Console"><SIZE 9>pre-formatted<SIZE$><FONT$> inside sentences.

<@Title2:>More Cosmetics

<@Normal:>
Special entities like email (duh@somewhere.com) and URL (<U>http://www.duh.com<P>) are detected automagically, as long as the horizontal line:

--------------------------------------------------------

<@Normal:>
^ thin or large v

========================================================

<@Normal:>
You can also specify an explicit link <U>http://duh.org<P> with label.

<@Normal:>
And remember,

<@Quote:>A TAB in front of the line does a quotation.
<@Quote:><@Quote:>More TABs, more depth (if allowed).

<@Normal:>
Nice.

<@Title1:>Lists

<@Normal:>
A list of items is natural, just putting a <B>dash<P> or a <B>plus<P> at the beginning of the line.

<@Title2:>Plain List

<@Normal:>
The dash is the default list identifier. For sublists, just add <B>spaces<P> at the beginning of the line. More spaces, more sublists.

<@Bullet:>
•	earth
  <@Bullet:>
  •	america
    <@Bullet:>
    •	south america
      <@Bullet:>
      •	brazil
        <@Bullet:>
        •	how deep can i go?
  •	europe
    <@Bullet:>
    •	lots of countries
•	mars
  <@Bullet:>
  •	who knows?

<@Normal:>
The list ends with <B>two<P> consecutive blank lines.

<@Title2:>Numbered List

<@Normal:>
The same rules as the plain list, just a different identifier (plus).

<@Bullet:>
•	one
•	two
•	three
  <@Bullet:>
  •	mixed lists!
  •	what a mess
    <@Bullet:>
    •	counting again
    •	...
•	four

<@Title2:>Definition List

<@Normal:>
The definition list identifier is a colon, followed by the term. The term contents is placed on the next line.

orange
  a yellow fruit
apple
  a green or red fruit
other fruits
  <@Bullet:>
  •	wee!
  •	mixing lists
    <@Bullet:>
    •	again!
    •	and again!

<@Title1:>Tables

<@Normal:>
Use pipes to compose table rows and cells. Double pipe at the line beginning starts a heading row. Natural spaces specify each cell alignment.

<@PreFormat:>
 || heading 1 |  heading 2  |  heading 3 |
  | cell 1.1  |  cell 1.2   |   cell 1.3 |
  | cell 2.1  |  cell 2.2   |   cell 2.3 |

<@Normal:>
Without the last pipe, no border:

<@PreFormat:>
 || heading 1 |  heading 2  |  heading 3
  | cell 1.1  |  cell 1.2   |   cell 1.3
  | cell 2.1  |  cell 2.2   |   cell 2.3

<@Title1:>Special Entities

<@Normal:>
Because things were too simple.

<@Title2:>Images

<@Normal:>
The image mark is as simple as it can be: <FONT "Lucida Console"><SIZE 9>[filename]<SIZE$><FONT$>.

<@Normal:>
                      img/photo.jpg  

<@Bullet:>
•	The filename must end in PNG, JPG, GIF, or similar.
•	No spaces inside the brackets!

<@Title2:>Other

<@Normal:>
The handy <FONT "Lucida Console"><SIZE 9>%%date<SIZE$><FONT$> macro expands to the current date.

<@Normal:>
So today is 20100806 on the ISO <FONT "Lucida Console"><SIZE 9>YYYYMMDD<SIZE$><FONT$> format.

<@Normal:>
You can also specify the date format with the %? flags, as <FONT "Lucida Console"><SIZE 9>%%date(%m-%d-%Y)<SIZE$><FONT$> which gives: 08-06-2010.

<@Normal:>
That's all for now.

-------------------------------------------------------

<@Normal:>
img/t2tpowered.png (sample.t2t <U>sample.t2t<P>)

