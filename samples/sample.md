TXT2TAGS SAMPLE
Aurelio Jargas
11/18/2010


# Introduction 

Welcome to the txt2tags sample file.

Here you have examples and a brief explanation of all
marks.

The first 3 lines of the this file are used as headers,
on the following format:

    line1: document title
    line2: author name, email
    line3: date, version

Lines with balanced equal signs = around are titles.

# Fonts and Beautifiers 

We have two sets of fonts:

The NORMAL type that can be improved with beautifiers.

The TYPEWRITER type that uses monospaced font for
pre-formatted text.

We will now enter on a subtitle...

## Beautifiers 

The text marks for beautifiers are simple, just as you
type on a plain text email message.

We use double *, /, - and _ to represent **bold**,
*italic*, strike and underline.

The ***bold italic*** style is also supported as a
combination.

## Pre-Formatted Text 

We can put a code sample or other pre-formatted text:

      here    is     pre-formatted
    //marks// are  **not**  ``interpreted``

And also, it's easy to put a one line pre-formatted
text:

    prompt$ ls /etc

Or use `pre-formatted` inside sentences.

## More Cosmetics 

Special entities like email (duh@somewhere.com) and
URL (http://www.duh.com) are detected automagically,
as long as the horizontal line:

---

^ thin or large v

---

You can also specify an [explicit link](http://duh.org)
with label.

And remember,

> A TAB in front of the line does a quotation.
> > More TABs, more depth (if allowed).

Nice.

# Lists 

A list of items is natural, just putting a **dash** or
a **plus** at the beginning of the line.

## Plain List 

The dash is the default list identifier. For sublists,
just add **spaces** at the beginning of the line. More
spaces, more sublists.

 * Earth
  * America
   * South America
    * Brazil
     * How deep can I go?
  * Europe
   * Lots of countries
 * Mars
  * Who knows?

The list ends with **two** consecutive blank lines.

## Numbered List 

The same rules as the plain list, just a different
identifier (plus).

1. one
1. two
1. three
  * mixed lists!
  * what a mess
1. counting again
1. ...
1. four

## Definition List 

The definition list identifier is a colon, followed by
the term. The term contents is placed on the next line.

: orange
a yellow fruit
: apple
a green or red fruit
: other fruits
  * wee!
  * mixing lists
1. again!
1. and again!

# Tables 

Use pipes to compose table rows and cells.
Double pipe at the line beginning starts a heading row.
Natural spaces specify each cell alignment.

| heading 1 |heading 2 |heading 3|
|---------------|
|cell 1.1 |cell 1.2 |cell 1.3|
|cell 2.1 |cell 2.2 |cell 2.3|

Without the last pipe, no border:

| heading 1 |heading 2 |heading 3|
|---------------|
|cell 1.1 |cell 1.2 |cell 1.3|
|cell 2.1 |cell 2.2 |cell 2.3|

# Special Entities 

Because things were too simple.

## Images 

The image mark is as simple as it can be: `[filename]`.

                      ![](img/photo.jpg)  

 * The filename must end in PNG, JPG, GIF, or similar.
 * No spaces inside the brackets!

## Other 

The handy `%%date` macro expands to the current date.

So today is 20101118 on the ISO `YYYYMMDD` format.

You can also specify the date format with the %? flags,
as `%%date(%m-%d-%Y)` which gives: 11-18-2010.

That's all for now.

---

![](img/t2tpowered.png) ([sample.t2t](sample.t2t))
