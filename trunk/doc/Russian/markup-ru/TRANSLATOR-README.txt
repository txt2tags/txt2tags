Hi,

First, THANK YOU for translating this document to your language.
It is *very* important to the program users.

A short road map to help your work:

- Start by renaming markup.t2t to markup-XX.t2t, where XX is the
  two-letter code of your language. Maybe your language needs a
  four-letter code, like pt_BR. If you don't know the code,
  search here:
  http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

  Do the same for the name of this folder: markup -> markup-XX
  There is no need to rename the other .t2t files.

- Edit markup-XX.t2t file and translate the very few messages
  is has. Attention to the TRANSLATOR notes inside!

- You can already convert the main file and check if you are
  going OK: txt2tags markup-XX.t2t

  Note that the HTML file is saved on the parent folder. Open
  it on the browser and check.

- Now all you have to do is to translate all the other .t2t
  files. Some notes about them:
  
  - Note that the first line is always empty. Don't change that.
  - Just translate the text, don't change the marks.
  - Try to use short words and rearrange the text, to make the
    converted document a nice not-so-wide table. Common wide
    candidates are quote.t2t and link.t2t.
  - On table.t2t, attention to not mess the cell align.
  - verb.t2t and raw.t2t are right-aligned. Try to maintain this.
  - tagged.t2t has HTML tags <div> and <p>, do not translate them.
