<?php
/**
 * DokuWiki Plugin t2t (Action Component)
 *
 * @license GPL 2 http://www.gnu.org/licenses/gpl-2.0.html
 * @author  Eric Forgeot, derivative from Andreas Gohr work
 */

// must be run within Dokuwiki
if (!defined('DOKU_INC')) die();
if (!defined('DOKU_PLUGIN')) define('DOKU_PLUGIN',DOKU_INC.'lib/plugins/');
require_once DOKU_PLUGIN.'action.php';

class action_plugin_txt2tags extends DokuWiki_Action_Plugin {

   function register(&$controller) {
      $controller->register_hook('PARSER_WIKITEXT_PREPROCESS',
'BEFORE', $this, 'handle_parser_wikitext_preprocess');
   }

   function handle_parser_wikitext_preprocess(&$event, $param) {
		global $ID;
      // The next line enables txt2tags markup ONLY on pages which have the .t2t extension. 
       // If you want it for the whole website, just delete or comment out the line below:
		if(substr($ID,-4) != '.t2t') return true;
	  // The next line will only be useful when the previous line is commented and txt2tags syntax
	   // is enabled for the whole website: it will allow you to disable txt2tags on pages
	   // which have the .dok extension, so the dokuwiki syntax will be used instead.
		if(substr($ID,-4) == '.dok')
		{
			return true;
		}
		else
		{
			   $event->data = "<t2t>\n".$event->data."\n</t2t>";
		}
	   }

}
