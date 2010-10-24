<?php

// TXT2TAGS syntax for pmwiki
//
// Get the lastest version from http://www.pmwiki.org/wiki/Cookbook/Txt2tags
//
// Installation :
// - Save this txt2tags.php in your /cookbook directory.
// - Add the following line into your local/config.php script:
//   require_once ("cookbook/txt2tags.php"); 
//   
// - If you wish to use the GUI icons for edition (included in pmwiki), add also:
//   $EnableGUIButtons = 1;
// - And if you want the full GUI icons
//   download t2tguiedit.zip from the txt2tags cookbook page and unzip it into your /pub directory.
// - You'll probably have to adapt the icon path to make it work. In the case the t2tguiedit folder is not found, it will fallback to the default guiedit icons (with a limited selection of icons).
// - For your users, you should edit the '''/pmwiki/index.php/Site/EditQuickReference''' file and add for example:
//    //Visit [txt2tags' website http://txt2tags.sourceforge.net/markup.html] to learn more about the syntax, or use the icons for quick formatting.//

$RecipeInfo['txt2tags']['Version'] = '2010-10-23';

// Check if the customized fonts were installed. Adapt it to your own path.
$MyGuiEditor = '/pmwiki/pub/t2tguiedit/';
//$MyGuiEditor = '/pub/t2tguiedit/';


	if (!defined('PmWiki')) {	
		exit();
	}
	

// GUIButtons



    /*
     * Expanden file_exists function
     * Searches in include_path
     */
    function file_exists_ip($filename) {
        if(function_exists("get_include_path")) {
            $include_path = get_include_path();
        } elseif(false !== ($ip = ini_get("include_path"))) {
            $include_path = $ip;
        } else {return false;}

        if(false !== strpos($include_path, PATH_SEPARATOR)) {
            if(false !== ($temp = explode(PATH_SEPARATOR, $include_path)) && count($temp) > 0) {
                for($n = 0; $n < count($temp); $n++) {
                    if(false !== @file_exists($temp[$n] . $filename)) {
                        return true;
                    }
                }
                return false;
            } else {return false;}
        } elseif(!empty($include_path)) {
            if(false !== @file_exists($include_path)) {
                return true;
            } else {return false;}
        } else {return false;}
    } 
    /* */
    
    

if (file_exists($_SERVER{'DOCUMENT_ROOT'} . $MyGuiEditor)) {
    $GUIButtonDirUrlFmt = $MyGuiEditor;
    
    $GUIButtons ['strong']      = array(10, "**", "**", '$[Strong Text]',
                                    '$GUIButtonDirUrlFmt/strong.png"$[Strong]"');                                 
                                    
	$GUIButtons ['underline']      = array(20, "__", "__", '$[Underline Text]',
                                    '$GUIButtonDirUrlFmt/underline.png"$[Underline]"');

	
	$GUIButtons ['em']      = array(30, "//", "//", '$[Emphasized Text]',
                                    '$GUIButtonDirUrlFmt/em.png"$[Italic]"');
                                    
    $GUIButtons ['strike']      = array(40, "--", "--", '$[Strike Text]',
                                    '$GUIButtonDirUrlFmt/strike.png"$[Strike]"');
  
    $GUIButtons ['empty1'] = array(60, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');
                                    

	$GUIButtons['h1'] = array(100, "= ", " =", '$[Heading level 1]',
                     '$GUIButtonDirUrlFmt/h1.png"$[Heading level 1]"');
 
	$GUIButtons['h2'] = array(110, "== ", " ==", '$[Heading level 2]',
                     '$GUIButtonDirUrlFmt/h2.png"$[Heading level 2]"');

	$GUIButtons['h3'] = array(120, "=== ", " ===", '$[Heading level 3]',
                     '$GUIButtonDirUrlFmt/h3.png"$[Heading level 3]"');
                    
    $GUIButtons ['empty2'] = array(200, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');

	$GUIButtons ['extlink'] = array(300, '[',']', '$[link text http://]',
                                    '$GUIButtonDirUrlFmt/extlink.png"Link to external page"');

	$GUIButtons ['innerlink'] = array(350, '[[',']]', '$[WikiPage | description text]',
                                    '$GUIButtonDirUrlFmt/link.png"Link to a page in this wiki"');

	$GUIButtons ['empty3'] = array(400, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');

	$GUIButtons['ul'] = array(530, "- ", "", '$[Unordered list]',
                     '$GUIButtonDirUrlFmt/ul.png"$[Unordered (bullet) list]"');
                     
	$GUIButtons ['ol'] = array(531, "+ ", "", '$[Ordered list]',
                                    '$GUIButtonDirUrlFmt/ol.png"$[Ordered (numbered) list]"');

	$GUIButtons ['empty4'] = array(600, "", "", '',
                                    '$GUIButtonDirUrlFmt/empty.png');
                                    
	$GUIButtons ['hr'] = array(700, "--------------------", "", '',
                                    '$GUIButtonDirUrlFmt/hr.png"$[Separator line]"');
                                    
    $GUIButtons ['comment'] = array(800, "% ", "", '',
                                    '$GUIButtonDirUrlFmt/comment.png"$[Comment]"');
    
} else {
    //echo "rem";
    //$GUIButtonDirUrlFmt = '/../../pmwiki/pub/guiedit';

    $GUIButtons ['strong']      = array($ArrayCount++, "**", "**", '$[Strong Text]',
                                    '$GUIButtonDirUrlFmt/strong.gif"$[Strong]"');                                 
                                    
	$GUIButtons ['underline']      = array($ArrayCount++, "__", "__", '$[Underline Text]',
                                    '$GUIButtonDirUrlFmt/underline.gif"$[Underline]"');

	
	$GUIButtons ['em']      = array($ArrayCount++, "//", "//", '$[Emphasized Text]',
                                    '$GUIButtonDirUrlFmt/em.gif"$[Italic]"');
      
	$GUIButtons ['strike']      = array($ArrayCount++, "--", "--", '$[Strike Text]',
                                    '$GUIButtonDirUrlFmt/hr.gif"$[Strike]"');

	$GUIButtons['h1'] = array(400, "= ", " =", '$[Heading level 1]',
                     '$GUIButtonDirUrlFmt/h1.gif"$[Heading level 1]"');
 
	$GUIButtons['h2'] = array(401, "== ", " ==", '$[Heading level 2]',
                     '$GUIButtonDirUrlFmt/h2.gif"$[Heading level 2]"');

	$GUIButtons['h3'] = array(402, "=== ", " ===", '$[Heading level 3]',
                     '$GUIButtonDirUrlFmt/h3.gif"$[Heading level 3]"');

	$GUIButtons ['extlink'] = array($ArrayCount++, '[',']', '$[link text http://]',
                                    '$GUIButtonDirUrlFmt/extlink.gif"Link to external page"');

	$GUIButtons['ul'] = array(530, "- ", "", '$[Unordered list]',
                     '$GUIButtonDirUrlFmt/ul.gif"$[Unordered (bullet) list]"');
                     
	$GUIButtons ['ol'] = array(531, "+ ", "", '$[Ordered list]',
                                    '$GUIButtonDirUrlFmt/ol.gif"$[Ordered (numbered) list]"');
}




// TODO verbatim zone

// Buttons to be hidden
	$GUIButtons['big'] = array();

	$GUIButtons['small'] = array();

	$GUIButtons['pagelink'] = array();
	/*$GUIButtons['extlink'] = array();*/

	$GUIButtons['attach'] = array();
						 
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
	
	Markup ('txt2tags_comment'    , '>_end', '/>% (.*?)$/si', '<!--**-->');	// works, but you can't have two following lines with comments, just add a blanck line in between. A character space must follow the % to work.
	
	
	
// beautifiers
	
	Markup ('txt2tags_bold'     , 'directives', '/\*\*(.*?)\*\*/'              , "'''$1'''");
	Markup ('txt2tags_undeline' , 'directives', '/__(.*?)__/'              , "{+$1+}");
	
	
	Markup ('txt2tags_italics0'  , '<directives', '/http:\/\//'              , "HTTPREP");
	Markup ('txt2tags_italics'  , 'directives', '/\/\/(.*?)\/\//'              , "''$1''");
	Markup ('txt2tags_italics1'  , 'inline', '/HTTPREP/'              , "http://");
	
	
	Markup ('txt2tags_strike'    , 'directives', '/--(.*?)--/', "{-$1-}");	
	// mono : see below


// HR Lines
	
	DisableMarkup("^----");
	Markup ('txt2tags_hr'    , '<txt2tags_strike', '/^--------------------+/', "<:block,1><hr noshade  size=1/>");		
	Markup ('txt2tags_hr5'    , '_begin', '/^====================+/', "<:block,1><hr noshade size=5/>");	


// Headings
	
	/*
	Markup ('txt2tags_h4','<txt2tags_h3'    , '/====(.*?)====/', "<h4>$1</h4>");		
	Markup ('txt2tags_h3','<txt2tags_h2'    , '/===(.*?)===/', "<h3>$1</h3>");	
	Markup ('txt2tags_h2','<txt2tags_h1'    , '/==(.*?)==/', "<h2>$1</h2>");	
	Markup ('txt2tags_h1'    , 'directives', '/= (.*?) =/', "<h1>$1</h1>");	
	*/
	
	Markup ('txt2tags_h4','<txt2tags_h3'    , '/( *)====[^=](.*?)[^=]====/', "!!!!$2");		
	Markup ('txt2tags_h3','<txt2tags_h2'    , '/( *)===[^=](.*?)[^=]===/', "!!!$2");	
	Markup ('txt2tags_h2','<txt2tags_h1'    , '/( *)==[^=](.*?)[^=]==/', "!!$2");	
	Markup ('txt2tags_h1'    , '<split', '/( *)= (.*?) =/', "!$2");	
	

	Markup ('txt2tags_nh4','<txt2tags_nh3'    ,  '/\+\+\+\+(.*?)\+\+\+\+/', "!!!!$1");		
	Markup ('txt2tags_nh3','<txt2tags_nh2'    ,  '/\+\+\+(.*?)\+\+\+/', "!!!$1");	
	Markup ('txt2tags_nh2','<txt2tags_nh1'    ,  '/\+\+(.*?)\+\+/', "!!$1");	
	//Markup ('txt2tags_nh1'    , '<txt2tags_numberedlist', '/\+ (.*?) \+/', "!$1");	
	Markup ('txt2tags_nh1'    , '<split', '/\+ (.*?) \+/', "!$1");	
	
	
// Lists (^ = occurs at the beginning of a line only)

	Markup ('txt2tags_bulletlist'    , 'directives', '/^- (.*?)/', "*$1");	
	Markup ('txt2tags_bulletlist2'    , 'directives', '/^ - (.*?)/', "**$1");	// works
	Markup ('txt2tags_bulletlist3'    , 'directives', '/^  - (.*?)/', "***$1");	// works

	Markup ('txt2tags_numberedlist'    , 'directives', '/^\+ (.*?)/', "#$1");	
	Markup ('txt2tags_numberedlist2'    , 'directives', '/^ \+ (.*?)/', "##$1");	// works
	Markup ('txt2tags_numberedlist3'    , 'directives', '/^  \+ (.*?)/', "###$1");	// works
	
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
	
	Markup ('txt2tags_table0'    , 'directives', '/\|\|/', "BARTAB");	// 
	//Markup ('txt2tags_table_2'    , '>txt2tags_table0', '/\| (.*?) \| (.*?) \|/', "|| $1 || $2 ||");	//  doesnt works well
	//Markup ('txt2tags_table_end'    , '<txt2tags_table0', '/\|$/', "||");	//  
	Markup ('txt2tags_table_1'    , '>txt2tags_table0', '/\| (.*?) \|/', "|| $1 ||");	//  almost works
	Markup ('txt2tags_table1'    , '>txt2tags_table_1', '/BARTAB/', "||");	//  
	
	
// // // /    LINKS
	
	//Markup ('txt2tags_locallink'    , 'directives', '/\[(.*?) local:\/\/(.*?)\]/s', '[[http://$2|$1]]');
	
	Markup ('txt2tags_urllink'    , 'directives', '/\[(.*?) HTTPREP(.*?)\]/s', '[[HTTPREP$2|$1]]');	
	// (beware this rule rely on the txt2tags_italics0 rule as well)

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

	Markup ('txt2tags_toc'    , '_begin', '/%%toc/', '(:*toc:)');
	
	 


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

A quoted paragraph is prefixed by a TAB. 			: not working.  Do we need this? Is it relevant for a wiki?

raw area											: similar to verbatim area

raw line											: works

verbatim area										: works

Verbatim line prefixed with 3 backquotes. 			: works


Tables												: not working


single external url links				 			: works (pmwiki behavior)
named url links									    : works
txt2tags style inner links  (without http) 			: doesn't works, use [[ ]] instead otherwise it will mess with links made with the pmwiki syntax


*/
