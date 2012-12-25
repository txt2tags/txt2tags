<?php
/*
Plugin Name: Text Control t2t
Plugin URI: http://dev.wp-plugins.org/wiki/TextControl
Description: Take total control of how your blog formats text: Textile 1+2, Markdown, Txt2tags, AutoP, nl2br, SmartyPant, and Texturize. Blog wide, individual posts, and defaults for comments.
Author: Jeff Minard, Frank B&uuml;ltge, Eric Forgeot
Author URI: http://bueltge.de
Version: 2.3.2
Date: 2012-12-23
*/ 

// Hey!
// Get outta here! All configuration is done in WordPress
// Check the "options > Text Control Config" in your admin section


// Pre-2.6 compatibility
if ( !defined( 'WP_CONTENT_URL' ) )
	define( 'WP_CONTENT_URL', get_option( 'siteurl' ) . '/wp-content' );
if ( !defined( 'WP_CONTENT_DIR' ) )
	define( 'WP_CONTENT_DIR', ABSPATH . 'wp-content' );
if ( !defined( 'WP_PLUGIN_URL' ) )
	define( 'WP_PLUGIN_URL', WP_CONTENT_URL. '/plugins' );
if ( !defined( 'WP_PLUGIN_DIR' ) )
	define( 'WP_PLUGIN_DIR', WP_CONTENT_DIR . '/plugins' );


function tc_textdomain() {

	load_plugin_textdomain('textcontrol', FALSE, dirname( plugin_basename(__FILE__) ) . '/languages');
}


/**
 * Add action link(s) to plugins page
 * Thanks Dion Hulse -- http://dd32.id.au/wordpress-plugins/?configure-link
 */
function tc_filter_plugin_actions($links, $file) {
	static $this_plugin;

	if ( ! $this_plugin )
		$this_plugin = plugin_basename(__FILE__);

	if ( $file == $this_plugin )
		$links = array_merge( array('<a href="options-general.php?page=text-control-t2t/text-control.php">' . __('Settings') . '</a>'), $links); // before other links
	
	return $links;
}


/**
 * settings in plugin-admin-page
 */
function tc_add_settings_page() {
	
	if ( is_admin() && function_exists('add_options_page') && current_user_can('switch_themes') ) {
		$menutitle = '';
		if ( version_compare( $GLOBALS['wp_version'], '2.6.999', '>' ) ) {
			$menutitle = '<img src="data:image/gif;base64,R0lGODlhCwALAPcAAAAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpaWltbW1xcXF1dXV5eXl9fX2BgYGFhYWJiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFxcXJycnNzc3R0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYmJmZmZqampubm5ycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2tra6urq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///ywAAAAACwALAAAIhQD//UN3y5GhQ63ICfxHrtCZLl+8iLnz7J+6RF/csPFiho4YOOBmlfljTloaYe4cednUaMutf+UK0fvHqcqbQllm/TKD5tsfLVrGHNoiqFSWLq/gbBmTJtUZLoICcVnzyMwXSeTsiOmyNUwYL2C2/YsWZ0wYMWK+kPm1MFwoOGTUZPImMCAAOw==" alt="" />' . ' ';
		}
		
		add_options_page(
			__('Text Control Formatting Options', 'textcontrol'), 
			$menutitle . __('Text Control', 'textcontrol'), 
			'manage_options', 
			__FILE__, 
			'tc_post_option_page'
		);
		add_filter( 'plugin_action_links', 'tc_filter_plugin_actions', 10, 2 );
	}
}


function tc_post($text) {
	global $id;
	
	if ( ! $id )
		$id = get_the_ID();
	
	/* Start with the default values */
	$do_text = get_option('tc_post_format');
	$do_char = get_option('tc_post_encoding');
	
	/* Now for the updated format that will take precedence */
	if ( get_post_meta( $id, '_tc_post_format', TRUE ) )
		$do_text = get_post_meta( $id, '_tc_post_format', TRUE );
	if ( get_post_meta( $id, '_tc_post_encoding', TRUE ) )
		$do_char =  get_post_meta( $id, '_tc_post_encoding', TRUE );
	
	$text = tc_post_process( $text, $do_text, $do_char );
	
	return $text;
}


function tc_comment($text) {
	
	return tc_post_process( $text, get_option('tc_comment_format'), get_option('tc_comment_encoding') );
}


function tc_post_process($text, $do_text = '', $do_char = '') {
	
	if ( 'textile2' == $do_text ) {
		require_once('text-control/textile2.php');
		$t = new Textile();
		$text = $t -> process($text);
		
	} else if ( 'textile1' == $do_text ) {
		require_once('text-control/textile1.php');
		$text = textile($text);
		
	} else if ( 'markdown' == $do_text ) {
		require_once('text-control/markdown.php');
		//$text = Markdown_Parser($text);
		$o = new Markdown_Parser;
		return $o->transform($text);

	} else if ( 'txt2tags' == $do_text ) {
		require_once('text-control/txt2tags.class.php');
		$x = new T2T($text);
		$x->go();
		return $text = $x->bodyhtml;
		
	} else if ( 'wpautop' == $do_text ) {
		$text = wpautop($text);
		
	} else if ( 'nl2br' == $do_text ) {
		$text = nl2br($text);
		
	} else if ( 'none' == $do_text ) {
		$text = $text;
		
	} else {
		$text = wpautop($text);
	}
	
	if ( 'smartypants' == $do_char ) {
		require_once('text-control/smartypants.php');
		$text = SmartyPants($text);
		
	} else if ( 'wptexturize' == $do_char ) {
		$text = wptexturize($text);
		
	} else if ( 'none' == $do_char ) {
		$text = $text;
		
	} else {
		$text = wptexturize($text);
	}
	
	return $text;
}


/* confiug page in  options */
function tc_post_option_page() {
?>
	<div class="wrap">
		<h2><?php _e('Text Control', 'textcontrol');?></h2>
		<?php
		if ( isset($_POST['tc_post_format']) && isset($_POST['tc_post_encoding']) ) {
			// set the post formatting options
			update_option( 'tc_post_format',   $_POST['tc_post_format'] );
			update_option( 'tc_post_encoding', $_POST['tc_post_encoding'] );
	
			echo '<div class="updated"><p>' . __('Post/Excerpt formatting updated.', 'textcontrol') . '</p></div>';
		}
	
		if ( isset($_POST['tc_comment_format']) && isset($_POST['tc_comment_encoding']) ) {
			// set the comment formatting options
			update_option( 'tc_comment_format',   $_POST['tc_comment_format'] );
			update_option( 'tc_comment_encoding', $_POST['tc_comment_encoding'] );
	
			echo '<div class="updated"><p>' . __('Comment formatting updated.', 'textcontrol') . '</p></div>';
		}
		?>
	
		<br class="clear" />
		<div id="poststuff" class="ui-sortable">
			<div class="postbox" >
				<h3><?php _e('Text Control Settings', 'textcontrol');?></h3>
				<div class="inside">
					<p>
						<?php _e('Set up the default settings for your blog text formatting.', 'textcontrol');?>
					</p>
					<br class="clear" />
					<form method="post" action="">
						<fieldset class="options">
							<legend>
								<strong><?php _e('Posts &amp; Excerpts', 'textcontrol');?></strong>
							</legend>
							<p>
								<?php _e('These will set up what the blog parses posts with by default unless over ridden on a per-post basis.', 'textcontrol');?>
							</p>
							<?php
							$do_text = get_option('tc_post_format');
							$do_char = get_option('tc_post_encoding');
							?>
							<select name="tc_post_format">
								<option value="wpautop"<?php if ( $do_text == 'wpautop' OR $do_text == ''){ echo(' selected="selected"');}?>>Default (wpautop)</option>
								<option value="textile1"<?php
									if ( $do_text == 'textile1') { echo(' selected="selected"');
									}
								?>>Textile 1</option>
								<option value="textile2"<?php
									if ( $do_text == 'textile2') { echo(' selected="selected"');
									}
								?>>Textile 2</option>
								<option value="markdown"<?php
									if ( $do_text == 'markdown') { echo(' selected="selected"');
									}
								?>>Markdown</option>
								<option value="txt2tags"<?php
									if ( $do_text == 'txt2tags') { echo(' selected="selected"');
									}
								?>>Txt2tags</option>
								<option value="nl2br"<?php
									if ( $do_text == 'nl2br') { echo(' selected="selected"');
									}
								?>>nl2br</option>
								<option value="none"<?php
									if ( $do_text == 'none') { echo(' selected="selected"');
									}
								?>><?php _e('No Formatting', 'textcontrol');?></option>
							</select>
							<select name="tc_post_encoding">
								<option value="wptexturize"<?php
								if ( $do_char == 'wptexturize') { echo(' selected="selected"');
								}
							?>>Default (wptexturize)</option>
								<option value="smartypants"<?php
									if ( $do_char == 'smartypants') { echo(' selected="selected"');
									}
								?>>Smarty Pants</option>
								<option value="none"<?php
									if ( $do_char == 'none') { echo(' selected="selected"');
									}
								?>><?php _e('No Character Encoding', 'textcontrol');?></option>
							</select>
							<input class="button" type="submit" value="<?php _e('Change Default Post/Excerpt Formatting', 'textcontrol');?>" /
						</fieldset>
					</form>
					<br />
					<form method="post" action="">
						<fieldset class="options">
							<legend>
								<strong><?php _e('Comments', 'textcontrol');?></strong>
							</legend>
							<p>
								<?php _e('All comments will be processed with these:', 'textcontrol');?>
							</p>
							<?php
							$do_text = get_option('tc_comment_format');
							$do_char = get_option('tc_comment_encoding');
							?>
							<select name="tc_comment_format">
								<option value="wpautop"<?php if ( $do_text == 'wpautop' OR $do_text == ''){ echo(' selected="selected"');}?>>Default (wpautop)</option>
								<option value="textile1"<?php
									if ( $do_text == 'textile1') { echo(' selected="selected"');
									}
								?>>Textile 1</option>
								<option value="textile2"<?php
									if ( $do_text == 'textile2') { echo(' selected="selected"');
									}
								?>>Textile 2</option>
								<option value="markdown"<?php
									if ( $do_text == 'markdown') { echo(' selected="selected"');
									}
								?>>Markdown</option>
								<option value="txt2tags"<?php
									if ( $do_text == 'txt2tags') { echo(' selected="selected"');
									}
								?>>Txt2tags</option>
								<option value="nl2br"<?php
									if ( $do_text == 'nl2br') { echo(' selected="selected"');
									}
								?>>nl2br</option>
								<option value="none"<?php
									if ( $do_text == 'none') { echo(' selected="selected"');
									}
								?>><?php _e('No Formatting', 'textcontrol');?></option>
							</select>
							<select name="tc_comment_encoding">
								<option value="wptexturize"<?php
								if ( $do_char == 'wptexturize') { echo(' selected="selected"');
								}
							?>>Default (wptexturize)</option>
								<option value="smartypants"<?php
									if ( $do_char == 'smartypants') { echo(' selected="selected"');
									}
								?>>Smarty Pants</option>
								<option value="none"<?php
									if ( $do_char == 'none') { echo(' selected="selected"');
									}
								?>><?php _e('No Character Formatting', 'textcontrol');?></option>
							</select>
							<input class="button" type="submit" value="<?php _e('Change Default Comment Formatting', 'textcontrol');?>" />
						</fieldset>
					</form>
				</div>
			</div>
		</div>
		<div id="poststuff" class="ui-sortable">
			<div class="postbox" >
				<h3><?php _e('Information on the plugin', 'feedstats')
				?></h3>
				<div class="inside">
					<p>
						<?php _e('For further information or to grab the latest version of this plugin, visit the <a href=\'http://dev.wp-plugins.org/wiki/TextControl\' title=\'to the plugin-website\' >plugin\'s homepage</a>.', 'textcontrol');?><br />
						&copy; Copyright 2006 - <?php echo date("Y");?> <a href="http://thecodepro.com/" title="<?php _e('to the Website', 'textcontrol');?>" >Jeff Minard</a><?php _e('and', 'textcontrol');?> <a href="http://bueltge.de" title="<?php _e('to the Website', 'textcontrol');?>" >Frank B&uuml;ltge</a> |<?php _e('Want to say thank you? Visit my <a href=\'http://bueltge.de/wunschliste/\' title=\'to the wishlist\' >wishlist</a>.', 'textcontrol');?>
					</p>
					<!-- <?php echo get_num_queries(); ?> queries. <?php timer_stop(1); ?> seconds. -->
				</div>
			</div>
		</div>
		<script type="text/javascript"><!--<?php if ( version_compare( substr($GLOBALS['wp_version'], 0, 3), '2.7', '<' ) ) { ?>
		jQuery('.postbox h3').prepend('<a class="togbox">+</a> ');
	
	<?php }?>
		jQuery('.postbox h3').click(function() { jQuery(jQuery(this).parent().get(0)).toggleClass('closed');
		});
		jQuery('.postbox.close-me').each(function() {
			jQuery(this).addClass("closed");
		});
		//-->
		</script>
	</div>
<?php
}

function tc_add_custom_box() {

	if ( function_exists('add_meta_box') ) { // for WordPress >=2.5
		add_meta_box(
			'textcontroldiv',
			__('Text Control', 'textcontrol'),
			'tc_inside_the_textcontrol_box',
			'post',
			'advanced'
		);
		
		add_meta_box(
			'textcontroldiv',
			__('Text Control', 'textcontrol'),
			'tc_inside_the_textcontrol_box',
			'page',
			'advanced'
		);
	
	} else {
		add_filter( 'dbx_post_advanced', 'tc_post_admin_footer' );
	}
}

function tc_post_edit_post($id) {
	global $id;
	
	if ( ! isset($id) )
		$id = $_REQUEST['post_ID'];
	
	if ( $id && isset($_POST['tc_post_i_format']) && isset($_POST['tc_post_i_encoding']) ) {
		update_post_meta($id, '_tc_post_format', esc_attr($_POST['tc_post_i_format']) );
		update_post_meta($id, '_tc_post_encoding', esc_attr($_POST['tc_post_i_encoding']) );
	}

}

function tc_inside_the_textcontrol_box($post) {
	global $id;
	
	if ( ! isset($id) && isset($_REQUEST['post']) )
		$id = $_REQUEST['post'];
	
	$do_text = get_option('tc_post_format');
	$do_char = get_option('tc_post_encoding');
	
	if ( get_post_meta( $id, '_tc_post_format', TRUE ) )
		$do_text = get_post_meta( $id, '_tc_post_format', TRUE );
	
	if( get_post_meta( $id, '_tc_post_encoding', TRUE ) )
		$do_char =  get_post_meta( $id, '_tc_post_encoding', TRUE );
	?>
	<p>
		<?php _e('Format this post with:', 'textcontrol');?>
		<select name="tc_post_i_format">
			<option value="wpautop"<?php if ( 'wpautop' == $do_text || '' == $do_text ) echo(' selected="selected"'); ?>>Default (wpautop)</option>
			<option value="textile1"<?php if ( 'textile1' == $do_text ) echo (' selected="selected"'); ?>>Textile 1</option>
			<option value="textile2"<?php if ( 'textile2' == $do_text ) echo (' selected="selected"'); ?>>Textile 2</option>
			<option value="markdown"<?php if ( 'markdown' == $do_text ) echo (' selected="selected"'); ?>>Markdown</option>
			<option value="txt2tags"<?php if ( 'txt2tags' == $do_text ) echo (' selected="selected"'); ?>>Txt2tags</option>
			<option value="nl2br"<?php if ( 'nl2br' == $do_text ) echo (' selected="selected"'); ?>>nl2br</option>
			<option value="none"<?php if ( 'none' == $do_text ) echo (' selected="selected"'); ?>><?php _e('No Formatting', 'textcontrol');?></option>
		</select>
		<select name="tc_post_i_encoding">
			<option value="wptexturize"<?php if ( 'wptexturize' == $do_char ) echo (' selected="selected"'); ?>>Default (wptexturize)</option>
			<option value="smartypants"<?php if ( 'smartypants' == $do_char ) echo (' selected="selected"'); ?>>Smarty Pants</option>
			<option value="none"<?php if ( 'none' == $do_char ) echo (' selected="selected"'); ?>><?php _e('No Character Formatting', 'textcontrol');?></option>
		</select>
	</p>
	<script language="JavaScript" type="text/javascript">
		<!--
		var placement = document.getElementById("titlediv");
		var substitution = document.getElementById("mtspp");
		var mozilla = document.getElementById && !document.all;
		if(mozilla)
			placement.parentNode.appendChild(substitution);
		else
			placement.parentElement.appendChild(substitution);
		//-->
	</script>
<?php
}

function tc_post_admin_footer($content) {
	
	// Are we on the right page?
	if ( 
		( preg_match('|post.php|i', $_SERVER['SCRIPT_NAME']) && $_REQUEST['action'] == 'edit' ) || 
		( preg_match('|post-new.php|i', $_SERVER['SCRIPT_NAME']) ) || 
		( preg_match('|page.php|i', $_SERVER['SCRIPT_NAME']) && $_REQUEST['action'] == 'edit' ) || 
		( preg_match('|page-new.php|i', $_SERVER['SCRIPT_NAME']) )
	) {
	
	global $id;
	
	if ( ! isset($id) )
		$id = $_REQUEST['post'];
	
	$do_text = get_option('tc_post_format');
	$do_char = get_option('tc_post_encoding');
	
	if ( get_post_meta( $id, '_tc_post_format', TRUE ) )
		$do_text = get_post_meta( $id, '_tc_post_format', TRUE );
	
	if ( get_post_meta( $id, '_tc_post_encoding', TRUE ) )
		$do_char =  get_post_meta( $id, '_tc_post_encoding', TRUE );
	?>
	
	<div class="dbx-b-ox-wrapper">
		<fieldset id="textcontrol" class="dbx-box">
			<div class="dbx-h-andle-wrapper">
				<h3 class="dbx-handle"><?php _e('Text Control', 'textcontrol')
				?></h3>
			</div>
			<div class="dbx-c-ontent-wrapper">
				<div id="postcustomstuff" class="dbx-content">
					<p>
						<?php _e('Format this post with:', 'textcontrol');?>
						<select name="tc_post_i_format">
							<option value="wpautop"<?php if ( 'wpautop' == $do_text || '' == $do_text ) echo(' selected="selected"'); ?>>Default (wpautop)</option>
							<option value="textile1"<?php if ( 'textile1' == $do_text ) echo (' selected="selected"'); ?>>Textile 1</option>
							<option value="textile2"<?php if ( 'textile2' == $do_text ) echo (' selected="selected"'); ?>>Textile 2</option>
							<option value="markdown"<?php if ( 'markdown' == $do_text ) echo (' selected="selected"'); ?>>Markdown</option>
							<option value="txt2tags"<?php if ( 'txt2tags' == $do_text ) echo (' selected="selected"'); ?>>Txt2tags</option>
							<option value="nl2br"<?php if ( 'nl2br' == $do_text ) echo (' selected="selected"'); ?>>nl2br</option>
							<option value="none"<?php if ( 'none' == $do_text ) echo (' selected="selected"'); ?>><?php _e('No Formatting', 'textcontrol');?></option>
						</select>
						<select name="tc_post_i_encoding">
							<option value="wptexturize"<?php
							if ( 'wptexturize' == $do_char ) echo (' selected="selected"'); ?>>Default (wptexturize)</option>
							<option value="smartypants"<?php
								if ( 'smartypants' == $do_char ) echo (' selected="selected"'); ?>>Smarty Pants</option>
							<option value="none"<?php if ( 'none' == $do_char ) echo (' selected="selected"'); ?>><?php _e('No Character Formatting', 'textcontrol');?></option>
						</select>
					</p>
					<script language="JavaScript" type="text/javascript">
						<!--
						var placement = document.getElementById("titlediv");
						var substitution = document.getElementById("mtspp");
						var mozilla = document.getElementById && !document.all;
						if(mozilla)
							placement.parentNode.appendChild(substitution);
						else
							placement.parentElement.appendChild(substitution);
						//-->
					</script>
				</div>
			</div>
		</fieldset>
	</div>
	<?php
	}
}

/* remove and add filter in wp */
if ( function_exists( 'add_action') ) {
	
	if ( is_admin() ) {
		add_action( 'init', 'tc_textdomain' );
		add_action( 'admin_menu',   'tc_add_settings_page' );
		add_action( 'admin_menu',   'tc_add_custom_box' );
		add_filter( 'edit_post',    'tc_post_edit_post' );
		add_filter( 'publish_post', 'tc_post_edit_post' );
	} else {
		remove_filter( 'the_content', 'wpautop' );
		remove_filter( 'the_content', 'wptexturize' );
		add_filter(    'the_content', 'tc_post' );
		
		remove_filter( 'the_excerpt', 'wpautop' );
		remove_filter( 'the_excerpt', 'wptexturize' );
		add_filter(    'the_excerpt', 'tc_post' );
		
		remove_filter( 'comment_text', 'wpautop', 30 );
		remove_filter( 'comment_text', 'wptexturize' );
		add_filter(    'comment_text', 'tc_comment' );
	}
}
