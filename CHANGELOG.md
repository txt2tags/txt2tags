# Version 3.3 (unreleased)

* Remove ASCII art target (Jendrik Seipp).
* Remove %!csv macro (Jendrik Seipp).
* Remove i18n (Jendrik Seipp).
* Remove plugins and tools that now live in their own repositories (Jendrik Seipp).
* Remove code for unused split feature (Jendrik Seipp).
* Use \n for linebreaks on all platforms as recommended by Python docs (Jendrik Seipp).
* Fix errors detected by flake8 (Jendrik Seipp).
* Explain how to install txt2tags with pipx in README file (Jendrik Seipp).

# Version 3.2 (2019-10-30)

 * Remove GUI (Jendrik Seipp).
 * Rename txt2tags to txt2tags.py (Jendrik Seipp).
 * Add setup.py file (Jendrik Seipp).
 * Upload txt2tags to PyPI (Jendrik Seipp).

# Version 3.1 (2019-10-29)

 * Check code format with black (Jendrik Seipp).
 * Correctly compute title length under Python 3 for txt target (Jendrik Seipp).
 * Update and continuously check Python sample scripts under samples/module (Jendrik Seipp).
 * Check that sample file is converted to all targets correctly in CI (Jendrik Seipp).
 * lout: fix email markup (Martin Michel, backported by Jendrik Seipp).
 * man: fix closing lists (Matteo Cypriani, backported by Jendrik Seipp).
 * Improve table regex (Aurelio Jargas, backported by Jendrik Seipp).
 * man: fix extra line (Nicolas Delvaux, backported by Jendrik Seipp).
 * Improve comments inside doHeader() (Aurelio Jargas, backported by Jendrik Seipp).
 * Don't list targets manually (Aurelio Jargas, backported by Jendrik Seipp).
 * Canonicalize paths before checking whether input and output files match (Jason Seeley, backported by Jendrik Seipp).

# Version 3.0 (2019-10-21)

 * Convert changelog file to Markdown (Jendrik Seipp).
 * Add travis-ci config file (Jendrik Seipp).
 * Add tox.ini file for testing multiple Python versions (Jendrik Seipp).
 * Reformat test suite with black (Jendrik Seipp).
 * Support running test suite under Python 3 (Jendrik Seipp).
 * Fix and refactor tests (Jendrik Seipp).
 * Add support for SVG images (Jendrik Seipp).
 * Don't escape underscores in tagged and raw LaTeX text (Jendrik Seipp).
 * Support Python 3 (Jendrik Seipp).
 * Use spaces instead of tabs (Jendrik Seipp).

# Version 2.6 (2010-11-05)

 * New target: art (ASCII Art). (Florent Gallaire)
 * New target: adoc (AsciiDoc). (Neil Voss)
 * New target: creole (Creole 1.0). (Eric Forgeot)
 * New target: dbk (DocBook). (David Hajage)
 * New target: pmw (PmWiki). (Ritesh Sood)

 * New mark: `''tagged''` for inline tagged text.
 * New mark: `'''` for blocks of tagged text.

 * New option: `--targets` to list all the available targets.
 * New option: `--slides` to format output as presentation slides (-t art). (Florent Gallaire)
 * New option: `--width` to set the document's width (used by -t art). (Florent Gallaire)
 * New option: `--height` to set the document's height (used by -t art). (Florent Gallaire)
 * New option: `--art-chars` to set the ASCII Art decorations. (Florent Gallaire)
 * New options (turn off): `--no-slides`, `--no-targets`.

 * New command: `%!csv` to include an external CSV file as a table. (Florent Gallaire)

 * HTML/XHTML: Removed those random `<P></P>` that used to appear on the output.
 * HTML: Headers changed to avoid orphan tags when not using `--css-sugar`. (Thomas Hafner)
 * HTML: Removed `id="toc"` from the toc DIV, but `class="toc"` still remains.
 * LaTeX: New compact lists with no paragraph breaks between items. (Mark White)
 * LaTeX: Added column span and cell alignment to tables. (Mark White)
 * LaTeX: UTF-8 encoding is now correctly set as `utf8` instead `utf-8`. (Aad Mathijssen)
 * Lout: Removed list indent to avoid gaps in text. (Barrie Stott)
 * Lout: Now paragraphs are allowed inside lists. (Barrie Stott)
 * Man: Removed indentation in verbatim blocks.

 * i18n: Sample files converted to UTF-8.
 * i18n: Manual Pages converted to UTF-8.
 * i18n: All .po files converted to UTF-8.
 * i18n: Added po/tools folder and po/stats.txt file.
 * i18n: Added Basque translations. (Ales Zabala Alava)
 * i18n: Added Ukrainian translations. (Bunyk Taras)
 * Docs: the Manual Page was rewritten: now a reference not a guide.
 * Docs: Markup Demo, Sample File, Manual Page translated to Basque. (Ales Zabala Alava)
 * Docs: User Guide translated to Chinese (simplified). (Chris Leng)
 * Docs: Sample File translated to Ukrainian. (Bunyk Taras)

 * extras: Added syntax files for JOE, "ne", "le" text editors. (Stefano D'Archino)
 * extras: Added a txt2tags markup set for markItUp! (Florent Gallaire)
 * extras: Added "dynartslides", a script to generate art slides dynamically. (Florent Gallaire)
 * extras: Added the Cookbook to use txt2tags markup in a PmWiki website. (Eric Forgeot)
 * extras: t2tmake.rb: Now compatible with ruby 1.9. (Lucas Buchala)
 * extras: Improved txt2tags.vim, unhtml.vim and txt2tagsrc files.
 * extras: Removed TextMate Bundle, it's already available at TextMate's SVN.

 * PHP Web interface improved: targets in alphabetical order, new $dfttarget.
 * Blank lines were added/removed to improve the generated code of all targets.
 * No more several blank lines at the end of the document.
 * Raw and tagged blocks are allowed inside paragraphs, they don't close it. (Kruzslicz Ferenc)
 * If called with no arguments, don't load the Gui. Must use `--gui` to load it.
 * The ":" char is now allowed in the query component of a URI (link). (sphaira, Chris lavabit)
 * Added TOC formatting example in samples/module/module-body.py file. (Jendrik Seipp)
 * Test-suite: 256 tests. New modules: art, csv, include, includeconf, sample.
 * Improved some error messages. (Leo Rosa)
 * Raise error when using `(target)` in `%!target` and `%!includeconf`.
 * The program code is now cleaner/safer with the help of `pychecker`.
 * Removed string module import: using `foo.upper()` instead `string.upper(foo)`.
 * Bugfix: Now `-C`,`--config-file` respects `(target)` in the config file settings. (Emmanuel Godard)
 * Bugfix: Now inline verbatim, raw and tagged marks are really mutually
exclusive. No marks are interpreted inside them.

 * **IMPORTANT:** This release requires Python 2.2 or newer. The only exception
is the new %!csv command that requires Python 2.3 or newer.

 * New website: http://txt2tags.org - Thanks Florent Gallaire for the domain!

 * This release was sponsored by Rubens Queiroz de Almeida.

# Version 2.5 (2008-07-26)

 * New target: wiki (Wikipedia) (Eric Forgeot @ .fr for the idea)
 * New target: gwiki (Google Code Wiki)
 * New target: doku (DokuWiki) (Joerg Desch)
 * New mark `--` for ~~strikeout~~ text, currently implemented for:
html, xhtml, tex, wiki, gwiki, doku, moin
 * New document: How to add a new target to txt2tags
 * New tools: TextMate bundle, Gedit language file, gensite program
(see 'extras' folder)

 * Improved Unicode (UTF-8) support
 * PHP Web interface rewrote: now configurable, clean and modular
 * Moin target improved: added support for definition list and strong line
 * LaTeX target improved: Added support for anchors and local links
 * Lout target improved: Added support for anchors in titles
 * Added PreProc sample on the samples/module/module-body.py file

 * i18n: Added Finnish translations (Mikko J Piippo)
 * Docs: Sample file translated to Finnish (Mikko J Piippo)
 * Docs: Man Page translated to Chinese (Abby Pan)
 * Docs: Portuguese Man Page updated

 * Bugfix: Fixed title underline length on txt target for UTF-8 files (Jan Rejlek)
 * Bugfix: Fixed fatal error on sources files with UTF-8 encoding (Miguel Filho)

 * **IMPORTANT:** Txt2tags is not compatible with old Python 1.5.2 anymore,
because Unicode strings were added in Python 2.0. If your Python is
older than 2.0, please use txt2tags version 2.4.

 * This release was sponsored by Dmitri Popov.

# Version 2.4 (2006-12-24)

 * New mark `%%%` for commented blocks (Leo Rosa)
 * The Style config now may be used multiple times
 * Different list types on the same indent now forces previous to close
 * Empty anchor is now part of a link (i.e. foo.html#) (Fabiano Engler)
 * tex: Default headers cleanup, now it's minimalist
 * tex: Now limiting the maximum quote depth to six
 * tex: User-defined styles now overwrite default formatting on headers
 * (x)html: New header comment showing the CSS file path, when using
`--css-inside`

 * i18n: Added Chinese translations (wfifi)

 * Bugfix: xhtml: Fixed encoding declaration when using `--css-sugar`
 * Bugfix: (x)html: No empty `<STYLE>` tag on `--css-inside` when CSS file is missing
 * Bugfix: (x)html: Removed useless `<P></P>` after table followed by blank line
 * Bugfix: tex: Now removing `.sty` extension of user style files
 * Bugfix: Macro at line beginning now closes Quote
 * Bugfix: Verbatim and Raw areas are now mutually exclusive
 * Bugfix: Fixed protocol adding to uppercased URLs like WWW.FOO.COM
 * Bugfix: Fixed fatal error on macro after table (i.e. "| x |\n%%date")
 * Bugfix: Fixed fatal error on table inside deflist (i.e. ": | foo")
 * Bugfix: Fixed fatal error on empty table (i.e. "| |")
 * Bugfix: Fixed fatal error on malformed lists (i.e. ": foo\n- bar")

 * Raw doesn't close Quote anymore
 * Optimization changes made the program execution slightly faster (Campbell Barton)
 * Unknown errors now sent to STDERR and exiting 1
 * Gui: Now using a green theme, following the new website colors
 * Test-suite with new modules and a total of 152 tests
 * Tarball clean up (less files, easier to generate and package)
 * Spell check and Capitalization on the code comments :)

# Version 2.3 (2005-06-17)

 * New rule to allow COLSPAN in table cells
 * New option `--dump-source` to show source file with t2t includes expanded
 * New options `--config-file` and `-C` to include an external config file
 * New options (turn off): `--no-infile`, `--no-dump-config`, `--no-dump-source`
 * New 'test' folder with the program test-suite
 * tex: FitV changed to FitH in hyperref package PDF settings

 * Docs: New "Markup Rules" document, obsoleting old RULES and Abuse Me docs
 * Docs: All documentation translated to French (Claude Hiebel @ .fr for making them)
 * Docs: Sample file translated to Hungarian (Adam Schmideg)
 * Docs: Sample file and Markup Demo translated to Chinese (Zoom Quiet)
 * Docs: Little fixes at the program man page and pt_BR.po potfile

 * Bugfix: Option `--css-inside` now working for xhtml target also
 * Bugfix: Macros names are case insensitive again (it was broken on v2.1)
 * Bugfix: Not dumping traceback when input file is empty
 * Bugfix: Now identifying invalid filter replacement (as \1 with no group)
 * Bugfix: Outfile buffer \n's expanded *before* postproc filters
 * Bugfix: Detection when `%!includeconf` is including itself (loop)
 * Bugfix: Module: Improved support, samples/module/* updated
 * Bugfix: Module: finish_him() has not module-aware
 * Bugfix: Module: Using `%%mtime` was dumping error (Ulysses Almeida)

# Version 2.2 (2004-12-30)

 * New target: lout
 * New option `--css-inside` to include the CSS file contents inside
HTML/XHTML headers
 * New T2TCONFIG environment variable to specify RC file location
 * The strong bar
 * tex: Now links are blue and clickable on PDF, using 'hyperref' package (Rahul Bhargava)

 * Debug messages revamped: categorized with IDs, background color setting
 * The `--help` message was improved with metavars (i.e. `--target=TYPE`)
 * The "wrote file" message now shows the full path if -o was used on
the command line
 * Module: New samples/module dir with sample Python scripts
 * Module: Better interface to use a string as a full marked file
 * Gui: Now all errors are printed *and* placed inside windows

 * i18n: Added French translations (Claude Hiebel)
 * i18n: Added German translations (Manfred Schreiweis)
 * i18n: Added Spanish translations (Ielton Ferreira)
 * Docs: "Markup Demo" translated to portuguese

 * Bugfix: outfile location inside %!options now respects infile path
 * Bugfix: xhtml: now the enconding is defined on <?xml> tag, not <meta>
 * Bugfix: tex: not escaping the underscore char '_' on image paths anymore
 * Bugfix: Module: now raising exceptions on errors instead print/sys.exit

# Version 2.1 (2004-11-13)

 * New `%%toc` macro to specify the TOC position
 * New `%%infile` and `%%outfile` macros, to get file information
 * New `%%mtime` macro, for source file modification time (Tamas Ivan)
 * New options `-q` and `--quiet` for quiet operation
 * New extras/gvim-menu.vim file for the gVim text editor (Otavio Correa)

 * Pre/Postproc regexes now compiled once (faster conversion!)
 * Now an empty item closes the current list
 * Option `--toc-only` now respecting `--outfile` (if any)
 * Tables with no "cellpadding" declaration when using `--css-sugar`
 * URL matcher: char "+" added on address and ";$" added for form data
 * The hyphen char "-" now can be used in anchors (Stefano Spinucci)
 * Misspelled option`--css-suggar` changed to `--css-sugar` (both works now)

 * i18n: Added Italian translations (Stefano Spinucci)
 * i18n: Added Hungarian translations (Tamas Ivan)
 * Docs: New "Markup Demo" document, which obsoleted old RULES file
 * Docs: New "Writing Books with Txt2tags" document
 * Docs: New "Reference Card" document in portuguese (Jose Inacio Coelho and Leslie Watter)
 * Docs: New "FAQ" document in portuguese (Wilson Freitas)
 * Docs: User Guide revamped: new chapters and now is a PDF
 * Docs: Abuseme and sample files translated to Spanish (Luis Cortazar)
 * Docs: Fixed typo on the program manpage

 * Bugfix: Detecting when input file is empty (zero sized)
 * Bugfix: Now deals with user malformed list: sublist before list
 * Bugfix: Windows RC file directory now pointing to %homepath%
 * Bugfix: Maximize result window on Gui now working (Marcus Aurelius Farias)
 * Bugfix: A macro right after the headers begins Body

# Version 2.0 (2004-07-25)

 * Program internationalized (i18n) and translated to Portuguese
 * New user configuration file `~/.txt2tagsrc`
 * New mark `"""` for Raw Text Area
 * New `%!includeconf` command to insert external file config
 * New `%!include: ""file""` command to include raw text
 * New pre-checking on Pre/Post Proc filters for regex errors
 * Graphical interface color configurable via `%!guicolors`
 * The program is now an importable Python module
 * Code changes to make pychecker happy (from 123 warnings to 10)
 * HTML and XHTML codes approved by w3c validator
 * New options: --dump-config, --debug, -v, --verbose, --encoding,
-i, --infile, --rc, --css-suggar
 * New options (turn off): --no-style, --no-toc, --no-toc-only,
--no-enum-title, --no-mask-email, --no-rc, --no-css-suggar,
--no-encoding, --no-infile, --no-outfile

 * Bugfix: fixed the program description on the documentation
 * Bugfix: sgml: removed useless <rowsep> from table last row
 * Bugfix: tex: now escaping correctly <, > and | chars
 * Bugfix: TOC and list errors when inverting order
 * New optional anchor specification for title: `=title=[anchor]`
 * New CSS sample files to help CSS beginners (Osvaldo Santana)
 * New target: xhtml (XHTML page) (Peter Valach and Christian Zuckschwerdt)
 * Tex: now using `--style` to load `\usepackage` modules
 * User Guide images on the tarball

 * Man target improved: added support for lists, quote and tables
 * Mgp target improved: image is now alignable
 * Moin target improved: added support for underline, quote, table
cell align, comment and TOC
 * Tex target improved: removed amssymb from headers, not breaking
pages anymore, mapping `--style` do \usepackage, using \clearpage,
image tag not using {figure} anymore (Leo Rosa, Leslie Watter and Sandor Markon)

 * Graphical and web interfaces improved (blue theme)
 * Error messages improved and prefixed by txt2tags string
 * New rules for beautifiers: glued and greedy
 * Solo centered images now requires spaces on both sides
 * Added & to URL filename valid chars (~michaelreaves/D&Dpreface.html)
 * User config on source code for i18n, debug and HTML lowered tags

 * Old `--type` option changed to `--target`
 * Old `--noheaders` option changed to `--no-headers`
 * Old `--enumtitle` option changed to `--enum-title`
 * Old `--maskemail` option changed to `--mask-email`
 * Old `--toclevel` option changed to `--toc-level`
 * Old `--toconly` option changed to `--toc-only`

 * Old ``pre`` mark changed to ```pre```
 * Old ```raw``` mark changed to `""""raw""""`
 * Old `---` mark changed to ````` for Verbatim Area
 * Old `= term:` mark changed to `: term` for definition list term
 * Old bolditalic mark removed, use `**//bold+italic//**` instead

 * Old `%!cmdline` config changed to `%!target` and `%!options`
 * Old `%!include: `file.txt`` changed to `%!include: ``file.txt```
when including a text file
 * Old `%!include: 'file.html'` changed to `%!include: ''file.html''`
when including a tagged file

# Version 1.7 (2003-11-30)

 * New `%!include` command to insert external files
 * Command line options errors now more descriptive
 * Regex errors now detected on Pre/Post proc filters
 * Program man page added to the tarball (Jose Inacio Coelho)
 * Rewritten the Emacs syntax highlight file (Leslie Watter)

 * Bugfix: moin: first level lists must have a leading space
 * Bugfix: man: headers using quotes
 * Bugfix: Footer composer on Windows was dumping error
 * Bugfix: Gui + STDOUT not showing `%!postproc` edits

# Version 1.6 (2003-07-23)

 * New mark `+` for explicit numbered titles, +like this+
 * New `%!preproc:` and `%!postproc:` user defined filters
 * New `%!key(target):` optional format to apply a config to a target,
as in `%!encoding(html): iso-8859-1`
 * Removed accented letter from Author's name
 * Added separator blank line before and after titles for txt target

 * Bugfix: `--toconly` now respects `--toclevel` setting
 * Bugfix: no more double spaced lines on Windows (Guaracy Monteiro @ .br for fixing)
 * Bugfix: man: escaping \ with \e
 * Bugfix: man: escaping lines that begin with . and '
 * Bugfix: tex: solved lots of LaTeX special chars issues: ~ ^ \
 * Bugfix: tex: the _ char is now escaped on titles
 * Bugfix: html: escaping '--' on comment lines
 * Bugfix: html: `<IMG ALIGN="middle">` (not "center")
 * Bugfix: html: closing `<A NAME>` tag with `</A>`
 * Bugfix: tex: now using \section* as the
 * Bugfix: tex: now respecting `--enumtitle`

 * Gui: now showing
 * Gui: refresh checkboxes when a new file is loaded
 * Gui: accepts extra options when called via command line, example:
`txt2tags --gui -n file.t2t`

# Version 1.5.1 (2003-05-14)

 * Just a patch for v1.5, in which the GUI was broken

# Version 1.5 (2003-05-09)

 * New `%!cmdline:` setting to specify a default command line
 * Target LaTeX now supporting images (Leslie Watter)
 * New option `-n`, short for `--enumtitle`
 * New option `-H`, short for `--noheaders`
 * New options `-o` and `--outfile` to set the output filename

 * New `<!DOCTYPE>` declaration on HTML target headers
 * Now the TODO file is public, included on the tarball
 * Some improvements on extras/unhtml.vim file

 * Syntax: Headers are parsed as plain text, except `%%date`
 * Syntax: Comma added as valid URL form data char

 * Bugfix: Masking of encoding name on tex was not working
 * Bugfix: \1, \2, \N special chars was not correctly escaped
 * Bugfix: '1linePre' regex was matching empty line as '--- '
 * Bugfix: Some targets don't support images as links
 * Bugfix: URL special chars was not escaped on Sgml target
 * Bugfix: Marks was being parsed on TOC items on man,pm6,moin,mgp,txt
 * Bugfix: Most targets don't support images as definition list term
 * Bugfix: Fixed escape char \ issues (now it is masked)

# Version 1.4 (2003-02-18)

 * New table smart align for the full table (left,center)
 * New table smart align for each table cell
 * New option `--style` and `%!style:` setting for doc style
 * New option `--toclevel` to set the maximum TOC deepness
 * Syntax: now comment lines doesn't close tables
 * If no headers, now the title is left empty (no more "`-NO TITLE-`")

 * Bugfix: `--maskemail` was not working since v1.2  :/
 * Bugfix: \t,\n,\r & friends was parsed as specials inside tables
 * Bugfix: Paragraph+comment+blankline+paragraph was parsed as one
paragraph

# Version 1.3 (2002-12-20)

 * New "Txt2tags User Guide" document
 * New mark `""` for RAW strings (pass-thru txt2tags parsing)
 * New `%!encoding:` command to specify the document charset
 * New 'contrib' dir for user contributed stuff
 * Improvements on SGML target: now using `<toc>` and `<descrip>`
 * Added '$' and '@' chars to the URL matcher, so http://this.is/valid@$99

 * Sanity: Removed from code structures marked as obsoleted on v1.1
 * Sanity: Removed `\email{}` tag from LaTeX headers. Using `\url{}`.
 * Sanity: `\usepackage[latin1]{inputenc}` is not default anymore on
LaTeX headers. If needed, use new *encoding* command.

 * Bugfix: LaTeX target added on the Web Interface menu
 * Bugfix: \n, \t and other special pairs escaped under `inline mono`
 * Bugfix: TOC anchor respecting maximum TOC level
 * Bugfix: Beautifiers not parsed on TOC items
 * Bugfix: Special chars not double escaped on TOC items

# Version 1.2 (2002-12-03)

 * New target: tex (LaTeX document) (Leslie Watter)
 * Now multiple source files can be specified on the command line
as `txt2tags -t html *.t2t` (Maksim Ischenko @ .ua for the idea)
 * URL matcher was improved and now gets valid insane paths as
http://this.com/// and http://this.com?var=abc#anchor
 * Added a COPYING file on the tarball, with the GPL license
 * Added a handy unhtml.vim script to the extras directory, to
convert by brute force an HTML file to a txt2tags file on Vim.
 * Bugfix: Special chars escaped on link label

# Version 1.1 (2002-11-06)

 * Images can now point to links, as: `[[img.gif] www.abc.com]`
 * New foldmethod=syntax rules on the Vim syntax file
 * Now any non-table line closes a table (blank line or not)
 * Begin of the major code-cleanup (aka complete rewrite)

 * Sanity: New RULE for headers: if the very first line of the file
is blank, this means 'this file has no header information'
 * Sanity: New comment char: % at the line beginning (no leading spaces!)
 * Sanity: Marks are not parsed on title lines
 * Sanity: // as comment mark is obsoleted, due conflicts with
italic mark. will be removed on version 1.3
 * Sanity: TAB-made tables are marked as obsoleted, will be removed on
version 1.3. Use the PIPE-made tables instead.
 * Sanity: Removed support for filename with spaces on the image mark,
due conflicts with named URL mark, `[like this.gif]`
 * New option `--fixme` (temporary) to update obsoleted structures and
automatically fix all this Sanity changes

 * Bugfix: `--noheaders` now act just as 'suppress headers from output',
and not 'treat headers as plain text'
 * Bugfix: Trailing . is now part of the URL when it contains anchor
location or form data (as #abc. and ?var=abc.)
 * Bugfix: Trailing / added to the URL matcher (as [www.abc.com/](http://www.abc.com/))
 * Bugfix: Title with \ char now is correctly handled

# Version 1.0 (2002-09-25)

 * New Graphical Tk Interface
 * Fixed target file format on Windows and Mac platforms
 * TOC deepness now is limited to level 3
 * RULES file sync'ed with actual rules (sorry!)
 * ChangeLog (this file) is now a txt2tags file
 * Added underscore char _ to anchor on URL regex

 * Bugfix: Closing any open list or table at EOF
 * Bugfix: HTML anchor name have no #

# Version 0.9 (2002-08-23)

 * Now txt2tags is a 100% pure Python script. The bash part has gone
so now it runs nicely on MS Windows and other Python aware platforms
 * New options `--toc` and `--toconly` to generate Table Of Contents
 * Defined `.t2t` as the official txt2tags file extension
 * Txt.vim file renamed to txt2tags.vim, and added instructions
 * Now titles are underlined on target txt
 * Cmdline used to generate the document is inserted as a comment on it
 * Tarball reorganized, adding 'extras' and 'samples' directories

 * Bugfix: When all ok, force system exit status to 0

# Version 0.8 (2002-07-03)

 * New abuseme.txt complex sample file (test-suite)
 * New smart image align feature for HTML (see abuseme.t2t)
 * New option `--maskemail` to hide email from SPAM robots
 * Table now can have border or no on HTML
 * Improvements on txt.vim syntax file, now colors works on gui also
 * Image mark can't accept filename with spaces (conflicts named link)

 * Bugfix: Parse more than one `%%date` on the same line
 * Bugfix: Special chars now escaped inside `preformatted`
 * Bugfix: Closing quote mark was kinda broken

# Version 0.7 (2002-06-20)

 * New Emacs syntax highlight file for txt2tags rules (Leslie Watter)
 * New mark `:` for definition lists (<DL> on HTML)
 * Now adding protocol to guessed link like [www.abc.com](http://www.abc.com)
 * Explicit link mark changed from `["label" url]` to `[label url]`
in other words, quotes are not necessary anymore
 * Image mark now correctly handles filenames with space for html
 * Corrected typos on sample.txt file
 * Named links now can point to local links as file.html, #anchor
and file.html#anchor

# Version 0.6 (2002-04-10)

 * Tables are now supported for sgml and moin targets
 * New option `--enumtitle` to enumerate all titles as 1, 1.1, 1.1.1, etc
 * New mark `+` for numbered list type for all targets
 * Better pre-formatted font escaping (won't parse marks)
 * URL matcher now supports ftp://user:passwd@domain.com login URLs
and user@domain.com?subject=test&cc=me@domain.com filled emails

# Version 0.5 (2002-03-22)

 * New handy Web interface to use it online (Internet or Intranet)
 * New option `--noheaders` to suppress headers information
 * Now it can read the marked text from STDIN (specify - as file)
 * Adapted to work on python old v1.5 also

# Version 0.4 (2002-03-11)

 * New simple table support (just for HTML by now)
 * Fixed lots of bugs on the man target, now it's kinda usable
 * The preformatted line mark must have a space after the dashes: '--- '
 * The preformatted line now has leading spaces
 * New options `-h`, `--help`, `-V` and `--version`
 * URL matcher is smarter, supporting `#local_anchors` and `?form=data`

# Version 0.3 (2001-11-09)

 * New mark `["my label" http://duh.com]` for explicit URL/email with label
 * Date macro now supports format string like `%%date(%m/%d/%Y)`

# Version 0.2 (2001-10-01)

 * New target: man (UNIX man page)
 * Nice shell wrapper to deal with files/directories/options.
in fact, the python code is now "embedded" on the sh script.
 * New options `--lang` and `--split` (for sgml2html)

# Version 0.1 (2001-07-26)

 * Initial release
