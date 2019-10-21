[![Build Status](https://travis-ci.org/jendrikseipp/txt2tags.svg?branch=master)](https://travis-ci.org/jendrikseipp/txt2tags)

# Txt2tags

Txt2tags is a document generator. It reads a text file with
minimal markup such as `**bold**` and `//italic//` and converts it
to the following formats:

 * ASCII Art
 * AsciiDoc
 * Creole 1.0
 * DocBook
 * DokuWiki
 * Google Wiki
 * HTML
 * LaTeX
 * Lout
 * MagicPoint
 * MoinMoin
 * PageMaker
 * PmWiki
 * Plain Text
 * SGML
 * UNIX Manpage
 * Wikipedia / MediaWiki
 * XHTML

You can use it as a Web component (PHP), as a GUI application
(windows and buttons), as a command line program or in a Python application.

# Usage

Simple example for command line usage:

1. Write a text file like this (leave 1st line blank):

   ```
   = Hello =
   I'm a robot. You're my **master**!
   [smile.jpg]
   ```

2. Run this command:

   `txt2tags --target html --no-headers file.t2t`

3. The result is:
   
   ```
   <H1>Hello</H1>
   <P>
   I'm a robot. You're my <B>master</B>!
   <IMG ALIGN="middle" SRC="smile.jpg" BORDER="0" ALT="">
   </P>
   ```

# History

Aurelio Jargas started the development of Txt2tags in 2001. The program saw several releases from 2001 to 2010, the last of which was version 2.6. Afterwards, Aurelio became less involved in the development. Still, many new features were added in the main repository (https://github.com/txt2tags/txt2tags), but they were never officially released. In my opinion, many of the new features are only useful for a very small set of users. The extra code adds bloat to the program and makes it hard to maintain the code. Unfortunately, these concerns are not shared by the whole Txt2tags development team. Therefore, I decided to branch off version 2.6 with the following goals

 * Support Python 3 (done)
 * Clean up the code code (in progress)
 * Make the code faster (not started)
 * Remove seldom-used features (not started)
 * Fix test suite (done)
 * Reintegrate bugfixes and useful features from main Txt2tags repo (not started)

 If you'd like to help out with any of these tasks, please get in touch. Pull requests are very welcome!