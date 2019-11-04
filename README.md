[![Build Status](https://travis-ci.org/jendrikseipp/txt2tags.svg?branch=master)](https://travis-ci.org/jendrikseipp/txt2tags)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Txt2tags

Txt2tags is a document generator. It reads a text file with
minimal markup such as `**bold**` and `//italic//` and converts it
to the following formats:

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
 * PmWiki
 * Plain Text
 * SGML
 * UNIX Manpage
 * Wikipedia/MediaWiki

You can use it as a command line program or in a Python application.

# Installation

We recommend using [pipx](https://pipxproject.github.io/pipx/) to install and run txt2tags in an isolated environment without affecting any system packages:

    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    pipx install txt2tags
    txt2tags --help

Of course you can also use pip to install txt2tags globally or in a virtual environment:

    pip install -U txt2tags

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

Aurelio Jargas started the development of Txt2tags in 2001. The program
saw several releases from 2001 to 2010, the last of which was version
2.6. Afterwards, Aurelio became less involved in the development. Still,
many new features were added in the main repository
(https://github.com/txt2tags/txt2tags), but they were never officially
released. In my opinion, many of the new features are only useful for a
very small set of users. The extra code adds bloat to the program and
makes it hard to maintain the code. Unfortunately, these concerns are
not shared by the whole Txt2tags development team. Therefore, I decided
to branch off version 2.6 and maintain a simpler txt2tags version that
works on Python 3. The file [TODO.md](TODO.md) lists the goals for the
project.

If you'd like to help out with any of the tasks, please get in touch.
Pull requests are very welcome!
