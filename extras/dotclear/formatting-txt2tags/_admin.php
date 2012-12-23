<?php
# -- BEGIN LICENSE BLOCK ----------------------------------
#
# This file is part of Dotclear 2.
#
# Copyright (c) 2003-2008 Olivier Meunier and contributors
# Licensed under the GPL version 2.0 license.
# See LICENSE file or
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#
# -- END LICENSE BLOCK ------------------------------------

require_once('txt2tags.class.php');

//$GLOBALS['__autoload']['Txt2tags_Parser'] = dirname(__FILE__).'/txt2tags.class.php';
$core->addFormater('txt2tags', array('dcTxt2tags','convert'));

class dcTxt2tags
{
	public static function convert($str)
	{
		$x = new T2T($str);
		$x->go();
		return $html = $x->bodyhtml;
	}
}
?>
