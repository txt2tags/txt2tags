* Run test/sample/run.sh in CI
* Upload txt2tags to PyPI
* Support running txt2tags with pipx
* Rename txt2tags file to txt2tags.py
* Clean up the code
* Make the code faster
* Remove seldom-used features
* Inspect the following commits from https://github.com/txt2tags/txt2tags and backport useful changes:

  * Escaping:

    73f5aecb90cfd4d3c5b778ab3e46755625fe46b8: New MaskMaster

    20405d82494cd5789540ea86d72a182c2fde7110: do not escape text in tagged blocks (closes issue 11)

  * HTML:

    c2945d57a1e743758c62225aeafb67c4b25b42ba: HTML, XHTML and XHTMLS: moved anchors as title ids

    457e2308a0012a55cbc844ecdc6d13dfc18a3188: [html] updated tests and fixed some issues with centering tables and images in xhtml

  * Path adjustment:

    1b6d27f169293475f1901507117d0448b9e12aa4 and
    5eaaa90d53fbb31cb3e3213928da6237bd89ce17 and
    124054b6d968a31eb33cee1cd5d775ec577d635d and
    d7ee71e8018d19c3cf66a947a22f86d5620acc47:
        The path adjustment for images now is not done when source or output files are STDIN/STDOUT. See issue 62.

    0b9eb9bca5a95d35ea089e7c23dde3988b553d1b: Fixed the problem with CSS files path when using %!includeconf from a different folder. Closes issue 71.

    b2200665eac4ad39aac7c1af8f8d99095830c2f0: New fix_css_out_path() to fix inconsistent behavior with relative CSS paths. Now these paths are handled the same way as image paths. Added new tests in test/path for %!style. See issue 71.

    bb5ccc0d77b07ad40e994175f37505938ae2719a: New class PathMaster to help solving the path issues.
        New tests in test/path to check %!option: --style and config nesting.
        New ghost option --dirname (for internal use only) to help tracking the original folder for %!options settings.
        Closes issue 85.

    39327217a1bdb9c1eb7f7d85443d48b5478b02b1:  New option --fix-path to enable the path adjustment for images, local links and CSS files when saving output file to a different folder with --outfile. Use --no-fix-path to turn it off. Tests updated.
        This reverts txt2tags to v2.6 state, when resources path in output is not touched at all. This way we don't break existing setups. See discussion in issue 62 for details. See also: issue 63, issue 71.

    63ae4342500702510e296cd132c9ab103ea57e5c: Outfile path fix. With the recently added path routines, it's not necessary to join paths inside get_outfile_name() anymore.

    6ae08f85e84599d012a568f3211f0d19aaa4eed6: Bugfix in --fix-path option: now it behaves the same regardless if the input file was informed as a relative or absolute path. New tests added to trunk/test/path to check for this specific case.


  * Wikipedia:

    f0a4c5d265b85d3edb9c49253216a249e19ab164:
        Wikipedia: Changed table syntax for cells. Now using "one cell per line" syntax, to make it easier to add alignment and colspan. Also, this syntax seems to be the preferred in MediaWiki docs. Sample file updated. See issue 93.

    25a0f867e5bed98ce29577a455cd92970f1026e4:
        Wikipedia: Added cell span and cell alignment to tables. Sample file updated. See issue 93.
        New regex/key called _tableAttrDelimiter, to place a delimiter into the table cell opening tag only when attributes (as align and span) were used.

    cfac162d394d6733622714f9588890919f075be6:
        Wikipedia: Added support for internal links to anchors. See issue 93.
        Added new tag key urlMarkAnchor, for those cases were the link to anchor tag is different from the normal link tag.
