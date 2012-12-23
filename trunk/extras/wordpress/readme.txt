


This plugin can add Txt2tags (among others) lightweight markup to WordPress. To install, just download the complete version from https://wordpress.org/extend/plugins/text-control-2 or just create a text-control folder into /wp-content/plugins, and put the txt2tags.class.php extension into /wp-content/plugins/text-control-2/text-control



=== Text Control ===
Tags: Post, Format, Formatting, Encoding
Contributors: Bueltge, eforgeot (txt2tags addition)
Donate link: http://bueltge.de/wunschliste/
Requires at least: 1.5
Tested up to: 3.4-Beta2
Stable tag: 2.3.2
Date: 2012-12-23

Take complete control of text formatting options on your blog: Formatting and encoding per post, globally on posts, and globally on comments.

Text Control will allow you to choose from a variety of formatting syntaxes and encoding options. You can choose between Markdown, Txt2tags, Textile 1, Textile 2, nl2br, WPautop, and "No Formatting" for formatting along with the choice of SmartyPants, WPTexturize or "No Encoding" for character encodings. 

= Localizations =
* Thanks to [Frank B&uuml;ltge](http://bueltge.de/ "Frank B&uuml;ltge") for german language file
* Thanks to [Brian Flores](http://www.inmotionhosting.com/) for spanish translation
* Lithuanian translation files by [Vincent G](http://www.host1plus.com)

== Installation ==
= Requirements =
* WordPress version 1.5 and later

= Installation =
1. Download
1. Unzip and upload into wp-content/plugins/
1. Activate in the Plugins section of your admin panel

= Usage =
When installed, this plugin will format text the exact same way that WordPress does by default.

You can define which text formatting engine to use by changing the values in the drop down menu on individual post pages.

Additionally, you can change the defaults on a blog-wide basis by changing the "Posts & Excerpts" options in "Your site Admin page >> `Options` >> `Text Control`".

Finally, you can set text processing for all comments as well. Set this up in the "Comments" options in "Your site Admin page >> `Options` >> `Text Control`".

== Other Notes ==
* Not really a bug so much, but an issue: Textile 2 is freaking huge (145k > 4000 lines of code) so it can be quite a burden on your server. If you can get away with *not* using it, I highly reccomend you do so.

* Additionally, in Textile 2 there is a feature that would grab an image via PHP and get it's height and width for placing in the IMG tags. This has been disabled It literally took a post from 1 second to display straight to 6 seconds -- completely unacceptable. 

= Acknowledgements =
* Romanian language files, thanks to [Alexander Ovsov](http://webhostinggeeks.com/)

= Licence =
Good news, this plugin is free for everyone! Since it's released under the GPL, you can use it free of charge on your personal or commercial blog. But if you enjoy this plugin, you can thank me and leave a [small donation](http://bueltge.de/wunschliste/ "Wishliste and Donate") for the time I've spent writing and supporting this plugin. And I really don't want to know how many hours of my life this plugin has already eaten ;)

= Translations =
The plugin comes with various translations, please refer to the [WordPress Codex](http://codex.wordpress.org/Installing_WordPress_in_Your_Language "Installing WordPress in Your Language") for more information about activating the translation. If you want to help to translate the plugin to your language, please have a look at the .pot file which contains all defintions and may be used with a [gettext](http://www.gnu.org/software/gettext/) editor like [Poedit](http://www.poedit.net/) (Windows) or plugin for WordPress [Localization](http://wordpress.org/extend/plugins/codestyling-localization/).

== Changelog ==
= 2.3.1 =
* Add also settings for pages

= 2.3.0 =
* Check on WP 3.2*, change different source, remove sql-queries and use WP-functions

= 2.2.3 =
* WordPress 2.7 ready, new functions for more comfort

= 2.2.2 =
* WP 2.5 ready, new metabox-function etc.

= 2.0b =
* Name changed from MTSpp to Text Control. Heavy updates!

= 1.0.1 =
* Changed a variable so that this would actually work in places like, oh ya know, the index.php file (places where s_single would be false.)

= 1.0 =
* Introduction 

== Screenshots ==
1. Options in WP 2.9-rare
1. Settings on post in WP 2.9-rare
1. A shot of the configuration options that show up in your admin section allowing you to detup how the blog will parse entries and comments by default.
1. The mechanism for setting per-post formatting options.
