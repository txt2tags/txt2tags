<?php

// TXT2TAGS syntax for pmwiki
//
// Get the lastest version from http://www.pmwiki.org/wiki/Cookbook/txt2tags
// or from the svn: http://txt2tags.googlecode.com/svn/trunk/extras/pmwiki/txt2tags.php
//
// Installation :
// - Save this txt2tags.php in your /cookbook directory.
// - Add the following line into your local/config.php script:
//   require_once ("cookbook/txt2tags.php"); 
//   
// - If you wish to use the GUI icons for edition (included in pmwiki), add also:
//   $EnableGUIButtons = 1; in your local/config.php file
//   and download t2tguiedit.zip from the txt2tags cookbook page and unzip it into your /pub directory.
// - You'll probably have to adapt the icon path to make it work. In the case the t2tguiedit folder is not found, it will fallback to the default guiedit icons (with a limited selection of icons).
// - For your users, you should edit the '''/pmwiki/index.php/Site/EditQuickReference''' file and add for example:
//    //Visit [txt2tags' website http://txt2tags.sourceforge.net/markup.html] to learn more about the syntax, or use the icons for quick formatting.//

$RecipeInfo['txt2tags']['Version'] = '2013-03-10';

$MyGuiEditor = '$FarmPubDirUrl/t2tguiedit/';

	if (!defined('PmWiki')) {	
		exit();
	}
	

// GUIButtons


	$GUIButtonDirUrlFmt = $MyGuiEditor;
                                       
    $GUIButtons['h1']         = array(100, "= ", " =", '$[Heading level 1]',
                                     '$GUIButtonDirUrlFmt/h1.png"$[Heading level 1]"');
                      
	$GUIButtons['h2']         = array(110, "== ", " ==", '$[Heading level 2]',
                                     '$GUIButtonDirUrlFmt/h2.png"$[Heading level 2]"');

	$GUIButtons['h3']         = array(120, "=== ", " ===", '$[Heading level 3]',
                                     '$GUIButtonDirUrlFmt/h3.png"$[Heading level 3]"');

	$GUIButtons['h4']         = array(130, "==== ", " ====", '$[Heading level 4]',
                                     '$GUIButtonDirUrlFmt/h4.png"$[Heading level 4]"');

	$GUIButtons ['empty1']    = array(199, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');
                                    

	$GUIButtons ['strong']    = array(210, "**", "**", '$[Strong Text]',
                                    '$GUIButtonDirUrlFmt/strong.png"$[Strong Text]"');                                 
                                    
	$GUIButtons ['underline'] = array(230, "__", "__", '$[Underlined Text]',
                                    '$GUIButtonDirUrlFmt/underline.png"$[Underlined Text]"');

	$GUIButtons ['em']        = array(220, "//", "//", '$[Italic Text]',
                                    '$GUIButtonDirUrlFmt/em.png"$[Italic Text]"');
                                    
	$GUIButtons ['strike']    = array(240, "--", "--", '$[Striked Text]',
                                    '$GUIButtonDirUrlFmt/strike.png"$[Striked Text]"');         

	$GUIButtons ['empty3']    = array(299, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');


	$GUIButtons ['ul']        = array(310, "\\n- ", "", '$[Unordered list]',
                                    '$GUIButtonDirUrlFmt/ul.png"$[:: Unordered (bullet) list]"');
                     
	$GUIButtons ['ol']        = array(320, "\\n+ ", "", '$[Ordered list]',
                                    '$GUIButtonDirUrlFmt/ol.png"$[:: Ordered (numbered) list]"');

	$GUIButtons ['empty2']    = array(399, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');


	$GUIButtons ['extlink']   = array(410, '[',']', '$[link description text http://]',
                                    '$GUIButtonDirUrlFmt/extlink.png"$[:: Link to external page http://]"');

	$GUIButtons ['innerlink'] = array(420, '[[',']]', '$[WikiPage | link description text]',
                                    '$GUIButtonDirUrlFmt/link.png"$[:: Link to a page in this wiki]"');

	$GUIButtons ['empty4']    = array(499, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');
                                    

                                   
	$GUIButtons ['comment']   = array(510, "\\n% ", "\\n", 'commented text\\n\\n',
                                    '$GUIButtonDirUrlFmt/comment.png"$[:: Comment (wont be interpreted)]"');
                                    
    $GUIButtons ['code']      = array(520, '``', '``', '$[Preformated Code]',
                                    '$GUIButtonDirUrlFmt/code.png"$[:: Preformated Code]"');
                                    
    $GUIButtons ['rawtxt']    = array(530, '&quot&quot', '&quot&quot', '$[Raw text]',
                                    '$GUIButtonDirUrlFmt/raw.png"$[:: Raw text]"');
                                    
	$GUIButtons ['empty5']    = array(599, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');


	$GUIButtons ['hr']        = array(610, "\\n--------------------\\n", "", '',
                                    '$GUIButtonDirUrlFmt/hr.png"$[:: Separator line]"');
 
    $GUIButtons ['table']     = array(620, '\\n| table | table ||\\n| cell | cell ||\\n', '', '',
                                    '$GUIButtonDirUrlFmt/table.png"$[:: Add sample table]"');
                    
	$GUIButtons ['sig']       = array(630, ' $CurrentTime', ' ', ' ',
                                    '$GUIButtonDirUrlFmt/sig.png"$[:: Insert <CurrentTime>]"');


	$GUIButtons ['empty6']    = array(699, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');


	$GUIButtons ['attach']    = array(710, 'Attach:', '', '$[file.ext]',
                                    '$GUIButtonDirUrlFmt/attach.png"$[:: Attach File]"');
                    
	$GUIButtons ['empty7']    = array(249, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');
                                    
    $GUIButtons ['centering'] = array(250, "{ ~~ }", "{/~~ }", '$[Center Text]',
                                    '$GUIButtonDirUrlFmt/text_align_center.png"$[Center Text]"');
                             
    
# specific translation expression
# French
XLSDV('fr', array('Strong Text'=>'Texte en gras'));
XLSDV('fr', array('Underlined Text'=>'Texte souligné'));
XLSDV('fr', array('Italic Text'=>'Texte italique'));
XLSDV('fr', array('Striked Text'=>'Texte barré'));
XLSDV('fr', array('Heading level 1'=>'Entête niveau 1'));
XLSDV('fr', array('Heading level 2'=>'Entête niveau 2'));
XLSDV('fr', array('Heading level 3'=>'Entête niveau 3'));
XLSDV('fr', array('Heading level 4'=>'Entête niveau 4'));
XLSDV('fr', array('WikiPage | link description text'=>'PageWiki | description du lien'));
XLSDV('fr', array('link description text http://'=>'description du lien http://'));
XLSDV('fr', array(':: Link to external page'=>':: Lien vers une page extérieure'));
XLSDV('fr', array(':: Link to a page in this wiki'=>':: Lien vers une page dans ce wiki'));
XLSDV('fr', array(':: Unordered (bullet) list'=>':: Liste non ordonnée (puces)'));
XLSDV('fr', array(':: Ordered (numbered) list'=>':: Liste ordonnée (numérotée)'));
XLSDV('fr', array(':: Separator line'=>':: Ligne séparatrice'));
XLSDV('fr', array(':: Comment (wont be interpreted)'=>':: Commentaire (ne sera pas interprété)'));
XLSDV('fr', array(':: Preformated Code'=>':: Code préformatté'));
XLSDV('fr', array(':: Insert <CurrentTime>'=>':: Insérer date et heure'));
XLSDV('fr', array(':: Attach File'=>':: Attacher un fichier'));



// TODO verbatim zone

// Buttons to be hidden
	$GUIButtons['big'] = array();

	$GUIButtons['small'] = array();

	$GUIButtons['pagelink'] = array();
	/*$GUIButtons['extlink'] = array();*/

	/*$GUIButtons['attach'] = array();*/
						 
	$GUIButtons['sup'] = array();

	$GUIButtons['sub'] = array();

	$GUIButtons['center'] = array();

//                                
 
                                       
	
// Basic formatting

	// RAW (markup, won't be interpreted. It should be double ' but it will interfere with the reste of the pmwiki syntax, so we use double " instead)

	Markup ('txt2tags_markup_raw'    , '<_begin', '/""(.*?)""/', '[= $1 =]');

// Comments

	//	Markup('a2z', '_end', '/a/', 'z'); 

	// Markup ('txt2tags_comment_prepare'    , '_begin', '/%(.*?)$/si', '<span></span>% $1');  // DON'T USE THIS OTHERWISE IT WILL BREAK PageActions
	
	Markup ('txt2tags_comment'    , '>_end', '/>% (.*?)$/si', '><!--**-->');
		// works, but you can't have two following lines with comments, just add a blanck line in between. A character space must follow the % to work.
	
	
// beautifiers
	
	Markup ('txt2tags_bold'     , 'directives', '/\*\*([^\s](.*?[^\s])?)\*\*/'       , "'''$1'''");
	Markup ('txt2tags_undeline' , 'directives', '/__([^\s](.*?[^\s])?)__/'           , "{+$1+}");	
	Markup ('txt2tags_strike'   , 'directives', '/--([^\s](.*?[^\s])?)--/'           , "{-$1-}");
	
	Markup ('txt2tags_http'     , '<directives', '/http:\/\//'          , "HTTPREP");
	Markup ('txt2tags_https'    , '<directives', '/https:\/\//'         , "HTTPSREP");
	Markup ('txt2tags_ftp'      , '<directives', '/ftp:\/\//'           , "FTPREP");
	Markup ('txt2tags_ftps'     , '<directives', '/sftp:\/\//'          , "SFTPREP");
	Markup ('txt2tags_italics'  , 'directives', '/\/\/([^\s](.*?[^\s])?)\/\//'       , "''$1''");

	Markup ('txt2tags_https2'   , 'inline', '/HTTPSREP/'                , "https://");	
	Markup ('txt2tags_http2'    , 'inline', '/HTTPREP/'                 , "http://");

	Markup ('txt2tags_ftp2'     , 'inline', '/FTPREP/'                  , "ftp://");
	Markup ('txt2tags_sftp2'    , 'inline', '/SFTPREP/'                 , "sftp://");
	
		
	// mono : see below


// HR Lines
	
	DisableMarkup("^----");
	Markup ('txt2tags_hr'       , '<txt2tags_strike', '/^--------------------+/', '<:block,1><hr style="height: 1px; border: none; color: gray; background: gray;"/>');		
	Markup ('txt2tags_hr5'      , '_begin', '/^====================+/', '<:block,1><hr style="height: 4px; border: none; color: gray; background: gray;"/>');	

// Headings
	
	/*
	Markup ('txt2tags_h4','<txt2tags_h3'    , '/====(.*?)====/', "<h4>$1</h4>");		
	Markup ('txt2tags_h3','<txt2tags_h2'    , '/===(.*?)===/', "<h3>$1</h3>");	
	Markup ('txt2tags_h2','<txt2tags_h1'    , '/==(.*?)==/', "<h2>$1</h2>");	
	Markup ('txt2tags_h1'    , 'directives', '/= (.*?) =/', "<h1>$1</h1>");	
	*/
	
	Markup ('txt2tags_h4','<txt2tags_h3'    , '/( *)====[^=](.*?)[^=]====/', "!!!!$2");		
	Markup ('txt2tags_h3','<txt2tags_h2'    , '/( *)===[^=](.*?)[^=]===/', "!!!$2");	
	Markup ('txt2tags_h2','<txt2tags_h1'    , '/( *)==[^=](.*?)[^=]==/' , "!!$2");	
	Markup ('txt2tags_h1', '<split'         , '/( *)= (.*?) =/'         , "!$2");	
	

	Markup ('txt2tags_nh4','<txt2tags_nh3'    ,  '/\+\+\+\+(.*?)\+\+\+\+/', "!!!!$1");		
	Markup ('txt2tags_nh3','<txt2tags_nh2'    ,  '/\+\+\+(.*?)\+\+\+/', "!!!$1");	
	Markup ('txt2tags_nh2','<txt2tags_nh1'    ,  '/\+\+(.*?)\+\+/', "!!$1");	
	//Markup ('txt2tags_nh1'    , '<txt2tags_numberedlist', '/\+ (.*?) \+/', "!$1");	
	Markup ('txt2tags_nh1'    , '<split', '/^\+ (.*?) \+/', "!$1");	  // please use the + header + at the beginning of a line

// <!> if adding a leading ^ for ex. /^( *)===[^=] it will break pagetoc.php...
	
// Lists (^ = occurs at the beginning of a line only)

	// correct lists beginning by a bold markup, like "- **bold**"
	Markup ('txt2tags_correctbulletlist'     , '<directives', '/^- \*\*/', "-  **");
	Markup ('txt2tags_correctbulletlist2'    , '>directives', '/^ - \*\*(.*?)\*\*/', "** **$1**");
	//Markup ('txt2tags_correctbulletlist2'    , '<directives', '/^ - \*\*/', " -  **");
	Markup ('txt2tags_correctbulletlist3'    , '<directives', '/^  - \*\*/', "  -  **");
	//Markup ('txt2tags_correctbulletlist4'    , '<directives', '/^   - \*\*/', "   -  **");
	Markup ('txt2tags_correctbulletlist4'    , '<directives', '/^   - \*\*(.*?)\*\*/', "*### '''$1'''");
	Markup ('txt2tags_correctbulletlist4b'    , '<directives', '/^\*\#\#\#/', "####");
	// TODO: not working as expected at the moment
	
	// transformation to the pmwiki syntax
	Markup ('txt2tags_bulletlist'     , 'directives', '/^- (.*?)/', "*$1");	
	Markup ('txt2tags_bulletlist2'    , 'directives', '/^ - (.*?)/', "**$1");	
	Markup ('txt2tags_bulletlist3'    , 'directives', '/^  - (.*?)/', "***$1");	
	Markup ('txt2tags_bulletlist4'    , 'directives', '/^   - (.*?)/', "****$1");	
	

	Markup ('txt2tags_numberedlist'   , 'directives', '/^\+ (.*?)/', "#$1");	
	Markup ('txt2tags_numberedlist2'  , 'directives', '/^ \+ (.*?)/', "##$1");	
	Markup ('txt2tags_numberedlist3'  , 'directives', '/^  \+ (.*?)/', "###$1");	
	Markup ('txt2tags_numberedlist4'  , 'directives', '/^   \+ (.*?)/', "####$1");	
	
// Definition list

	Markup ('txt2tags_deflist'    , 'directives', '/^: (.*?)$/', ":'''$1''':");	
	
	
// Verbatim and PRE
	
	Markup ('txt2tags_blockquote'    , 'inline', '/^\t(.*?)/s', "<:blockquote,1>$1");	// works
	
	DisableMarkup("^ "); //disable <pre> with space
		
	Markup('txt2tags_verbatim', '[=',  "/^```\n(.*?\n)```[^\\S\n]*\n/sme",  "Keep(PSS('<pre class=\"escaped\">$1</pre>'))"); // works
	
	
	Markup ('txt2tags_verbatimline'    , 'directives', '/``` (.*?)/', "<:pre,1>$1");	// works
	
	Markup ('txt2tags_mono'    , 'directives', '/``(.*?)``/', "@@$1@@");	


	Markup('txt2tags_raw_area', '[=',  '/^"""\n(.*?\n)"""[^\\S\n]*\n/sme',  "Keep(PSS('<pre class=\"escaped\">$1</pre>'))"); // works

	
// TABLES : use the pmwiki tables but with double || instead (not working yet)

	//Markup ('txt2tags_tablehead'    , '<^||||', '/\|\|/', "||!");		// doesnt work
	//Markup ('txt2tags_table'    , '>txt2tags_tablehead', '/\|(.*?)\|/', "|| $1 ||");	// doesnt work
	
	Markup ('txt2tags_table0'     , 'directives', '/\|\|/', "BARTAB");	// 
	//Markup ('txt2tags_table_2'    , '>txt2tags_table0', '/\| (.*?) \| (.*?) \|/', "|| $1 || $2 ||");	//  doesnt works well
	//Markup ('txt2tags_table_end'    , '<txt2tags_table0', '/\|$/', "||");	//  
	Markup ('txt2tags_table_1'    , '>txt2tags_table0', '/\| (.*?) \|/', "|| $1 ||");	//  almost works
	Markup ('txt2tags_table1'     , '>txt2tags_table_1', '/BARTAB/', "||");	//  
	
	
// // // /    LINKS
	
	// (see below) Markup ('txt2tags_locallink3'    , 'directives', '/\[(.*?) local:\/\/(.*?)\]/s', '[[http://$2|$1]]');
	
	//Markup('txt2tags_locallink',  '>fulltext',  '/\[(.*?) \| (.*?)\]/s',  '<a href="$2">$1</a>');

	// contrary to the normal txt2tags, we have to precise if the file is local with local://
	// In the case $EnablePathInfo = 1; in local/config.php use ../../ after local:
	//    [description local://../../subfolder/file.ext]
	Markup('txt2tags_locallink2',  '>fulltext',  '/\[(.*?) local:\/\/(.*?)\]/',  '<a href="$2">$1</a>');
	
	//TODO
	Markup('txt2tags_attachlink',  '<directives',  '/\[(.*?) Attach:(.*?)\]/',  '<a href="$UploadUrlFmt/$2">$1</a>');

# with simple "directive", pb link with images
	Markup ('txt2tags_urllink_var'    , '<directives', '/\[(.*?) \|[ ]HTTPREP(.*?)\]/s', '[[HTTPREP$2|$1]]');	
	Markup ('txt2tags_urllink_var2'    , '<directives', '/\[(.*?)\| HTTPREP(.*?)\]/s', '[[HTTPREP$2|$1]]');	
	Markup ('txt2tags_urllink_var3'    , '<directives', '/\[(.*?)\|HTTPREP(.*?)\]/s', '[[HTTPREP$2|$1]]');	
	
	Markup ('txt2tags_urllink'    , 'directives', '/\[(.*?) HTTPREP(.*?)\]/s', '[[HTTPREP$2|$1]]');	
	

	
	//Markup ('txt2tags_urllink'    , '<inline', '/\[(.*?) http:\/\/(.*?)\]/s', '<a href="$2>$1</a>');	
	
	Markup ('txt2tags_urllink2'    , '<txt2tags_urllink', '/\[(.*?) HTTPSREP(.*?)\]/s', '[[HTTPSREP$2|$1]]');
		
	Markup ('txt2tags_urllink3'    , 'directives', '/\[(.*?) FTPREP(.*?)\]/s', '[[FTPREP$2|$1]]');	
	// not working (empty line) Markup ('txt2tags_urllink4'    , 'directives', '/\[(.*?) SFTPREP(.*?)\]/s', '[[SFTPREP$2|$1]]');	

	// fix for using both https and http URL. Works only for maximum 2 mixed links.
	Markup ('txt2tags_urllink-fix'    , '<txt2tags_urllink2', '/\[(.*?) HTTPREP(.*?)\](.*?)\[(.*?) HTTPSREP(.*?)\]/s', '[[HTTPREP$2|$1]] $3 [[HTTPSREP$5|$4]]');	
	Markup ('txt2tags_urllink2-fix'    , '<txt2tags_urllink2', '/\[(.*?) HTTPSREP(.*?)\](.*?)\[(.*?) HTTPREP(.*?)\]/s', '[[HTTPSREP$2|$1]] $3 [[HTTPREP$5|$4]]');	

	

	// (beware this rule rely on the txt2tags_http/https/ftp/ftps (italics) rules as well)

	//Markup ('txt2tags_urllink'    , '>_end', '/\[(.*?) <a class=\'urllink\' href=\'http:\/\/(.*?)\' title=\'\' rel=\'nofollow\'>(.*?)<\/a>\]/s', '<a href="http://$2">$1</a>');	// works but not that good	

	# Markup ('bbcode_link_text', '<links' , '/\[url=(.*?)\](.*?)\[\/url\]/'     , "[[$1|$2]]");
	# Markup ('bbcode_link'     , '<links' , '/\[url\](.*?)\[\/url\]/'           , "[[$1]]");
	
	
	#Markup ('txt2tags_innerlink'    , '>_end', '/\[(.*\s?)( +)(.*?)\]/s', '<a href="$2">$1</a>');	//  works almost	



	#those 2 lines are for protecting text between brackets [like_this]
	//Markup ('txt2tags_protectlink'    , '<txt2tags_innerlink', '/\[(\w*?)\]/s', 'µµµ$1µµµ');	// 
	//Markup ('txt2tags_protectlink2'    , '>txt2tags_innerlink', '/µµµ(.*?)µµµ/s', '[$1]');	// 

// images
	
	Markup ('txt2tags_imgjpg'    , '>_end', '/\[<img src=\'(.*?).jpg\' alt=\'\' title=\'\' \/>\]/si', '<img src=\'$1.jpg\' alt=\'\' title=\'\' \/>');
	
	Markup ('txt2tags_imgpng'    , '>_end', '/\[<img src=\'(.*?).png\' alt=\'\' title=\'\' \/>\]/si', '<img src=\'$1.png\' alt=\'\' title=\'\' \/>');
	
	Markup ('txt2tags_imggif'    , '>_end', '/\[<img src=\'(.*?).gif\' alt=\'\' title=\'\' \/>\]/si', '<img src=\'$1.gif\' alt=\'\' title=\'\' \/>');

// Macros

	Markup ('txt2tags_toc'       , '_begin', '/%%toc/', '(:*toc:)');
	
	 


/*


Title level											: works
Numbered Title level								: replaced by Title level


Table of content based on titles					: works (you must use http://www.pmwiki.org/wiki/Cookbook/PageTableOfContents to get it work)
 

A paragraph is made by one or more lines.
A blank line separates them. 						: seems to work. Default in pm wiki?



a percent sign for comments							: works, with a trailing space after the %


For beautifiers we have bold and italic.			: works

There is also underline, strike and monospaced. 	: works


a list of items										: works		
More indent opens a sublist 						: works

Two blank lines close all the lists. 				: one line break is enough to close the list.

Change the hyphen by a plus
And you have a numbered list 						: works

Definition list										: not working

A quoted paragraph is prefixed by a TAB. 			: not working.  Do we need this? Is it relevant for a web form?

raw area											: similar to verbatim area

raw line											: works

verbatim area										: works

Verbatim line prefixed with 3 backquotes. 			: works


Tables												: not working


single external url links				 			: works (pmwiki behavior)
named url links									    : works
txt2tags style inner links  (without http) 			: doesn't works, use [[ ]] instead otherwise it will mess with links made with the pmwiki syntax


*/
