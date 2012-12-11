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

class action_plugin_t2t extends DokuWiki_Action_Plugin {

   function register(&$controller) {
      $controller->register_hook('PARSER_WIKITEXT_PREPROCESS',
'BEFORE', $this, 'handle_parser_wikitext_preprocess');
   }

   function handle_parser_wikitext_preprocess(&$event, $param) {
       global $ID;
       if(substr($ID,-4) != '.t2t') return true;

       $event->data = "<t2t>\n".$event->data."\n</t2t>";
   }

}
