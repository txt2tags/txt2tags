h1. TXT2TAGS SAMPLE

Author: Aurelio Jargas
Date: 10/20/2010


h1. Introduction

Welcome to the txt2tags sample file.

Here you have examples and a brief explanation of all
marks.

The first 3 lines of the this file are used as headers,
on the following format:

<pre>
line1: document title
line2: author name, email
line3: date, version
</pre>

Lines with balanced equal signs = around are titles.

h1. Fonts and Beautifiers

We have two sets of fonts:

The NORMAL type that can be improved with beautifiers.

The TYPEWRITER type that uses monospaced font for
pre-formatted text.

We will now enter on a subtitle...

h2. Beautifiers

The text marks for beautifiers are simple, just as you
type on a plain text email message.

We use double *, /, - and _ to represent *bold*,
_italic_, -strike- and +underline+.

The *_bold italic_* style is also supported as a
combination.

h2. Pre-Formatted Text

We can put a code sample or other pre-formatted text:

<pre>
  here    is     pre-formatted
//marks// are  **not**  ``interpreted``
</pre>

And also, it's easy to put a one line pre-formatted
text:

<pre>
prompt$ ls /etc
</pre>

Or use @pre-formatted@ inside sentences.

h2. More Cosmetics

Special entities like email (duh@somewhere.com) and
URL (http://www.duh.com) are detected automagically,
as long as the horizontal line:

---

^ thin or large v

---

You can also specify an "explicit link":http://duh.org
with label.

And remember,

bq. A TAB in front of the line does a quotation.
bq. More TABs, more depth (if allowed).

Nice.

h1. Lists

A list of items is natural, just putting a *dash* or
a *plus* at the beginning of the line.

h2. Plain List

The dash is the default list identifier. For sublists,
just add *spaces* at the beginning of the line. More
spaces, more sublists.

* earth
** america
*** south america
**** brazil
***** how deep can i go?
** europe
*** lots of countries
* mars
** who knows?

The list ends with *two* consecutive blank lines.

h2. Numbered List

The same rules as the plain list, just a different
identifier (plus).

# one
# two
# three
** mixed lists!
** what a mess
### counting again
### ...
# four

h2. Definition List

The definition list identifier is a colon, followed by
the term. The term contents is placed on the next line.

* orange
a yellow fruit
* apple
a green or red fruit
* other fruits
** wee!
** mixing lists
### again!
### and again!

h1. Tables

Use pipes to compose table rows and cells.
Double pipe at the line beginning starts a heading row.
Natural spaces specify each cell alignment.

|_.heading 1|_.heading 2|_.heading 3|
|. cell 1.1|. cell 1.2|. cell 1.3|
|. cell 2.1|. cell 2.2|. cell 2.3|

Without the last pipe, no border:

|_.heading 1|_.heading 2|_.heading 3|
|. cell 1.1|. cell 1.2|. cell 1.3|
|. cell 2.1|. cell 2.2|. cell 2.3|

h1. Special Entities

Because things were too simple.

h2. Images

The image mark is as simple as it can be: @[filename]@.

                      !=img/photo.jpg!  

* The filename must end in PNG, JPG, GIF, or similar.
* No spaces inside the brackets!

h2. Other

The handy @%%date@ macro expands to the current date.

So today is 20101112 on the ISO @YYYYMMDD@ format.

You can also specify the date format with the %? flags,
as @%%date(%m-%d-%Y)@ which gives: 11-12-2010.

That's all for now.

---

!img/t2tpowered.png! ("sample.t2t":sample.t2t)

