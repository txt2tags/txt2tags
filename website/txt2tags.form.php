<?php
/**
  txt2tags.class.php : text to HTML convertor in PHP
  Written by (c) Petko Yotov 2012 www.pmwiki.org/Petko
  Development sponsored by Eric Forgeot.
  
  This is an example use of the txt2tags.class.php script
  with a web form.
    
  You can edit this file and adapt it for your needs.
  
*/

function stripmagic($x) # form helper function from PmWiki
  { return get_magic_quotes_gpc() ? stripslashes($x) : $x; }

require_once('txt2tags.class.php');


# OPTION 1: serve a single file:
#
# $page =  file_get_contents("sample.t2t");


# OPTION 2: serve a file called by 'txt2tags.form.php?id='
#           Use 'switch' for defined files
#           <!> change $fichier = "$id"; for default switch
#               if you don't want your visitors to be able 
#               to execute random code. 
#           See txt2tags.sample.php for an example of use.
#
# foreach ($_POST as $key => $value) $$key = addslashes($value);
# foreach ($_GET as $key => $value) $$key = addslashes($value);
#
#   $id = $_GET['id'];
#	if ($_GET['id'] != "undefined")
#    {
#        switch($id) {
#				case "file1":
#					$fichier = "file1.t2t";
#					break;
#				case "file2":
#					$fichier = "file2.t2t";
#					break;
#				case "sample":
#					$fichier = "sample.t2t";
#					break;
#				default:
#					$fichier = "$id";
#					break;
#				}
#	}
#	
# $page =  $text = file_get_contents($fichier);

# OPTION 3: serve a form which visitors can fill themselves (for testing purpose)
$page = <<<EOF
txt2tags

Free online php conversion

%!style: inc/site.css
%%%
  Note, we write in the %!postproc below \\n\\1 because it is
  inside a PHP variable. In a text file or in a web form, we
  would write just \n for newline and \1 for the first match.
%%%
%!postproc: (</head>) <style type='text/css'></style>\\n\\1
%!postproc: (</style>) div.demo, pre {width: 90%; border: 2px solid #ddd; margin: 1em; padding: 1em;}\\n\\1
%!postproc: (</style>) textarea {width: 90%; border: 2px solid #ddd; margin: 1em;}\\n\\1
%!postproc: (</style>) hr {  color: #f00; background-color: #f00; width: 90%; }\\n\\1
%!postproc: (</style>) hr.light { height: 2px; }\\n\\1
%!postproc: (</style>) hr.heavy { height: 6px; }\\n\\1
%!postproc: (</title>) ".class.php - online convertor\\1"
%!postproc: "<div style='text-align:center;'>" <div class='header' id='header'>
%!postproc: "(<h1>)(.+.)(</h1>)" \\1<a href="/">\\2</a>\\3
%!postproc: "(<h3>.*</h3>)" \\1\\nby <a href="http://notamment.fr/">Petko Yotov</a>

''' <div class="body" id="body">
= txt2tags.class.php - online convertor =

Here you can test the [txt2tags.class.php txt2tags-php.zip] script.

Write or paste some ``t2t markup`` in the text area below.

'''
<form action="txt2tags.form.php" method="post">
<textarea name="text" rows="12" cols="80">
{(TEXT)}</textarea><br/>
<input type="submit" value="Convert!"/> <a href="txt2tags.form.php">Reset</a>
</form>
'''

== Resulting HTML code ==

``` {(CODE)}

== Rendered HTML ==

''' <div class='demo'>
{(HTML)}
''' </div>

% </div class=body>
''' </div>
EOF;

# create the form page
$x = new T2T($page);

# change the %%mtime
$x->mtime = filemtime(__FILE__);

$x->go();
$html = $x->fullhtml;
# for including in an HTML page: $html = $x->bodyhtml;
# for a complete HTML page:      $html = $x->fullhtml;

$search = array('{(CODE)}', '{(HTML)}', '{(TEXT)}');

if(@$_POST['text']) {
  $text = stripmagic($_POST['text']);
  $z = new T2T($text);
  $z->go();
  
  $fullhtml = $z->fullhtml;
  $onlybody = $z->bodyhtml;
  
  $replace = array( htmlspecialchars($fullhtml), $onlybody, htmlspecialchars($text));
  
}
else
  $replace = array("The result will appear here.", "The result will appear here.", '');

$html = str_replace($search, $replace, $html);

echo $html;



