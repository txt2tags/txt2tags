<?php
/**
  txt2tags.class.php : text to HTML convertor in PHP
  Written by (c) Petko Yotov 2012 www.pmwiki.org/Petko
  Development sponsored by Eric Forgeot.
  
  This is an example use of the txt2tags.class.php script
  with some php inclusion.
    
  You can edit this file and adapt it for your needs.
  
*/

function stripmagic($x) # form helper function from PmWiki
  { return get_magic_quotes_gpc() ? stripslashes($x) : $x; }

require_once('txt2tags.class.php');


# note, we write in the %!postproc below \\n\\1 because it is in a
# PHP variable; in a text file or in a web form, we would write just
# \n for newline and \1 for the first match

# OPTION 1: serve a single file:
#
# $page =  file_get_contents("file1.t2t");


# OPTION 2: serve a file called by 'txt2tags.sample.php?id='
#           Use 'switch' for predefined files
#
foreach ($_POST as $key => $value) $$key = addslashes($value);
foreach ($_GET as $key => $value) $$key = addslashes($value);

$id = $_GET['id'];
if ($_GET['id'] != "undefined")
    {
        switch($id) {
				case "file01":
					$fichier = "file1.t2t";
					break;
				case "readme":
					$fichier = "readme.t2t";
					break;
 			    case "sample":
					$fichier = "sample.t2t";
					break;
				default:
					$fichier = "readme.t2t";
					break;
				}
	}
	
$page =  $text = file_get_contents($fichier);

# OPTION 3: serve a form which visitors can fill themselves (for testing purpose)
#           See txt2tags.form.php for an example.

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



