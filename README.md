# txt2tags

Txt2tags is a document generator created by Aurelio Jargas in 2001. It reads a text file with minimal markup such as `**bold**` and `//italic//` and converts it to many formats, such as:

 * AsciiDoc
 * DocBook
 * HTML
 * LaTeX
 * MoinMoin
 * UNIX man page
 * Wikipedia/MediaWiki
 * …and many others.

Txt2tags is available in two different versions, which are branches inside this repository.


## [Branch v2](https://github.com/txt2tags/txt2tags/tree/v2), txt2tags version 2.7-dev

Full featured txt2tags version that works on Python 2.

- Runs on Python versions 2.6 and 2.7.

- Many years of development and contributions since txt2tags version 2.6 from 2010: bug fixes, new features (templates, remote files, more macros), new targets (bbcode, CSV, HTML5, Markdown, RTF, ReStructuredText, …) - [see changelog](https://github.com/txt2tags/txt2tags/blob/v2/ChangeLog.t2t)

- No official release for txt2tags version 2.7 yet, use the GitHub code.

- The maintainer is [Florent Gallaire](https://github.com/fgallaire).


## [Branch v3](https://github.com/txt2tags/txt2tags/tree/v3), txt2tags version 3.x

Simpler txt2tags version that works on Python 3, branched off from txt2tags version 2.6.

- Runs on Python versions 2.7 and 3.x.

- Removed less used features (GUI, ASCII Art/PageMaker/XHTML targets, CSV macro, i18n, translations) to achieve easier maintenance ([see changelog](https://github.com/txt2tags/txt2tags/blob/v3/CHANGELOG.md)).

- New releases are available as [PyPI packages](https://pypi.org/project/txt2tags/).

- The maintainer is [Jendrik Seipp](https://github.com/jendrikseipp).
