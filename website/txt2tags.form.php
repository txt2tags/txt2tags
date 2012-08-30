<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<TITLE>txt2tags.class.php - online convertor</TITLE>
<LINK REL="stylesheet" TYPE="text/css" HREF="inc/site.css">
<style type='text/css'><!--
div.demo, pre {width: 90%; border: 2px solid #ddd; margin: 1em; padding: 1em;}
textarea {width: 90%; border: 2px solid #ddd; margin: 1em;}
hr.light { height: 2px; }
hr.heavy { height: 6px; }
--></style>
</HEAD>
<BODY id="online">

<DIV CLASS="header" ID="header">
<h1><a href="/">txt2tags</a></h1>
<H3>Free online php conversion</H3>
by <a href="http://notamment.fr/">Petko Yotov</a>
</DIV>


<DIV CLASS="body" ID="body">
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


# note, we write in the %!postproc below \\n\\1 because it is in a
# PHP variable; in a text file or in a web form, we would write just
# \n for newline and \1 for the first match
#
# $page =  file_get_contents("sample.t2t");
#
$page = <<<EOF
txt2tags.class.php - online convertor




Here you can test the [txt2tags.class.php txt2tags-php.zip] script.

Write or paste some ``t2t markup`` in the text area below.

'''
<form action="txt2tags.form.php" method="post">
<textarea name="text" rows="12" cols="50">
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

EOF;

# create the form page
$x = new T2T($page);

# change the %%mtime
$x->mtime = filemtime(__FILE__);

$x->go();
$html = $x->bodyhtml;
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


?>

</DIV>
</HTML>
