<?php # txt2tags.php (http://txt2tags.org)
   # A handy web interface for the txt2tags conversion tool
   # License: GPL
   #
   # 2002-03-22 Aurelio Jargas <verde@aurelio.net>
   # 2004-06-26 Aurelio: v2.0: %%date, photo, s/orange/blue/, XHTML target,
   #            CSS, work in new PHP, --enum-title, show parsed x?html
   # 2004-10-20 Aurelio: v2.1: Text capitalized, using button instead photo
   # 2004-12-28 Aurelio: v2.2: Lout target
   # 2005-05-28 Aurelio: v2.3: link: s/sample.t2t/markup.html/, gray table
   # 2006-07-24 Aurelio: v2.4: rewrote. Now configurable, clean and modular
   #            Form using labels and fieldset, --toc, hints simplified
   # 2008-07-08 Aurelio: v2.5: is_standalone flag to turn headers on/off
   # 2010-10-22 Aurelio: v2.6: new targets, $dfttarget, targets alpha order


#-----------------------------[ CONFIG ]-----------------------------
#
# The txt2tags program location (PATH)
#
$prog = "./txt2tags-2.6.py";

# Set to 1 to use this file alone (will print page headers)
# Set to 0 to use this file inserted on another .php (embedded)
$is_standalone = 0;

# The default target
$dtftarget = "html";

# The default text encoding
$dtfencoding = "UTF-8";

# The default marked text
#
$dfttxt = "= My Title =";
$dfttxt.= "\nA __paragraph__ with **bold** and //italic//.\n";
$dfttxt.= "\nToday is %%date(%c).";
$dfttxt.= "\nHere is a nice pic: [img/t2tpowered.png].\n";
$dfttxt.= "\n  | John |  33  |    Male |";
$dfttxt.= "\n  | Mary |  19  |  Female |";

# The options labels for the form
#
$labels = array(
	'target'    => 'Target',
	'noheaders' => 'Hide headers',
	'enumtitle' => 'Numbered titles',
	'toc'       => 'Table Of Contents',
	'csssugar'  => 'CSS Sugar (HTML and XHTML)'
);

# The available targets
#
$targets = array(
	'art'    => 'ASCII Art text',
	'adoc'   => 'AsciiDoc document',
	'creole' => 'Creole 1.0 document',
	'dbk'    => 'DocBook document',
	'doku'   => 'DokuWiki page',
	'gwiki'  => 'Google Wiki page',
	'html'   => 'HTML page',
	'tex'    => 'LaTeX document',
	'lout'   => 'Lout document',
	'mgp'    => 'MagicPoint slides',
	'moin'   => 'MoinMoin page',
	'pm6'    => 'PageMaker document',
	'txt'    => 'Plain Text (no marks)',
	'pmw'    => 'PmWiki page',
	'sgml'   => 'SGML document',
	'man'    => 'UNIX Manual page',
	'wiki'   => 'Wikipedia page',
	'xhtml'  => 'XHTML page'
);


#----------------------------[ FUNCTIONS ]---------------------------

function FormSelect($name, $arr, $selected='', $size=0) {
	if ($size == 0) $size = count($arr);
	$r = "\n<select id=\"$name\" name=\"$name\" size=\"$size\">\n";
	while (list($id, $txt) = each($arr)) {
		$sel = ($id == $selected) ? ' selected' : '';
		$r .= "<option value=\"$id\"$sel>$txt</option>\n";
	}
	$r .= "</select>\n";
	return $r;
}

function FormCheck($name, $value, $on=0){
	$on = ($on) ? 'checked' : '';
	return "<input type=\"checkbox\" id=\"$name\" name=\"$name\" value=\"$value\" $on>";
}

function FormLabel($name) {
	global $labels;
	return "<label for=\"$name\">{$labels[$name]}</label>";
	}

function getvar($name){
	eval('global $'.$name.';');         # first try the global one
	eval('$val = $'.$name.';');
	if (!$val) $val = $_SERVER[$name];  # if not found, try others
	if (!$val) $val = $_POST[$name];
	# echo "<p>key: <b>$name</b>, value: <b>$val</b>---</p>"; 
	return $val;
}


#-----------------------------[ INIT ]----------------------------

$myself    = getvar('PHP_SELF');
$txt       = getvar('txt');
$target    = getvar('target');
$noheaders = getvar('noheaders');
$enumtitle = getvar('enumtitle');
$toc       = getvar('toc');
$csssugar  = getvar('csssugar');

if (!$txt) $txt = $dfttxt;
if (!$target) $noheaders = '-H';    # Default ON


#---------------------------[ HEADERS ]----------------------------

if ($is_standalone) {

?>

<html>
<head><title>txt2tags // ONE source, MULTI targets</title>

<style type="text/css">
	body { margin:20px; padding:0; }
	h1 { border-bottom:1px solid black; }
	form { margin-top:3em; font-size:85%; }
	fieldset { background:#ffc; margin:0 0 1em 0; border:1px solid #ddd; width:40em; }
	textarea { font-size:90%; }
	table#markuphint { float:right; background:#ffa; border:1px solid #ccc; font-size:90%; }
	table#markuphint tr { line-height:100%; }
	table#markuphint td { padding:0 7px; }
	pre#output { margin-left:3em; overflow:auto; }
	#parsed { border:1px solid #999; margin:0 2em 2em 3em; padding:1em; }
	#parsed td { border-style:solid; }
	#footer { border-top:1px solid black; }
</style>

</head>
<body>

<h1>txt2tags WEB Interface</h1>

<?php
}

#------------------------------[ FORM ]------------------------------
?>
<form id="userinput" method="post" action="<?php echo $myself; ?>">

<fieldset>
	<legend>Text Source</legend>
	<textarea name="txt" rows="8" cols="53" id="markItUp"><?php echo $txt; ?></textarea>
</fieldset>
<br>
<fieldset>
	<legend>Options</legend>

	<table id="markuphint">
	<caption>Markup Hints</caption>
	<tr>
		<td>**bold**</td>
		<td>= title =</td>
		<td>%%date</td>
	</tr><tr>
		<td>//italic//</td>
		<td>- list</td>
		<td>[image.jpg]</td>
	</tr><tr>
		<td>__under__</td>
		<td>+ numlist</td>
		<td colspan="2">[link www.com]</td>
	</tr><tr>
		<td>--strike--</td>
		<td>``code``</td>
		<td>| table |</td>
	</tr>
	</table>

	<?php
	echo FormLabel('target').FormSelect('target', $targets, $target ? $target : $dtftarget, 1);
	echo '<br><br>';
	echo FormCheck('noheaders', '--no-headers', $noheaders);
	echo FormLabel('noheaders').'<br>';
	echo FormCheck('enumtitle', '-n', $enumtitle);
	echo FormLabel('enumtitle').'<br>';
	echo FormCheck('toc', '--toc', $toc);
	echo FormLabel('toc').'<br>';
# Mmmmm, no.
#	echo FormCheck('csssugar', '--css-sugar', $csssugar);
#	echo FormLabel('csssugar').'<br>';
	?>
</fieldset>
<br>
<input type="submit" value="Convert!">
</form>

<?php
#----------------------------[ PROCESSING ]--------------------------

if ($target){

	# Always empty headers on input
	$txt = escapeshellarg("\n$txt");
	
	# Compose command line
	$cmd = array();
	if ($noheaders) $cmd[] = $noheaders;
	if ($enumtitle) $cmd[] = $enumtitle;
	if ($toc      ) $cmd[] = $toc;
	if ($csssugar ) $cmd[] = $csssugar;
	$cmd[] = "--encoding $dtfencoding";
	$cmd[] = "-t $target";
	$cmd[] = "-i -";
	$cmd[] = "-o -";
	
	# Security: Remove symbols from command line
	$cmd = ereg_replace('[^A-Za-z0-9 -]', '', implode(' ', $cmd));

	# Show results
	?>	
	<h3>Text converted to <?php echo strtoupper($target); ?></h3>

	<pre id="output"><?php echo htmlspecialchars(`echo $txt | $prog $cmd`); ?>
	</pre>

	<?php
	if ($target == 'html' || $target == 'xhtml') {
	?>
		<h3><?php echo strtoupper($target); ?> parsed</h3>

		<div id="parsed">
		<?php echo `echo $txt | $prog -H $cmd`; ?>
		</div>
	<?php
	}
}

#----------------------------[ FOOTER ]--------------------------

if ($is_standalone) {
?>

<p id="footer">
Txt2tags site: <a href="http://txt2tags.org">http://txt2tags.org</a><br>
Author: <a href="http://aurelio.net/en/">Aurelio Jargas</a>
</p>

</body>
</html>
<?php
}
?>
