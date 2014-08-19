<?php $T2TVersion = "20140518";
/**
  txt2tags.class.php
  Written by (c) Petko Yotov 2012 www.pmwiki.org/Petko
  Development sponsored by Eric Forgeot.
  
  txt2tags is a lightweight markup language created by 
  Aurelio Jargas and written in Python (www.txt2tags.org).
  
  This class here attempts to transpose some of the features 
  of the Python convertor to the PHP language.
  
  Most of this script was written by Petko Yotov except:
  - functions PSS(), Keep(), Restore(), RegExp $UEX based on 
    the PmWiki engine by Patrick R. Michaud www.pmichaud.com
  - the RegExp $imgrx based on txt2tags.py by Aurelio Jargas
  
  This text is Free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 3
  of the License, or (at your option) any later version.
  See http://www.gnu.org/copyleft/gpl.html for full details 
  and lack of warranty.
  
  
  == How to use this script ==
  
  This class should be included from other scripts, for example:
  
  # load the class
  require_once('txt2tags.class.php');
  
  ## initialize a new T2T object: two ways
  
  # either with an existing disk file:
  $x = new T2T("test.t2t", true);
  
  # or with a variable containing the entire T2T markup:
  $x = new T2T($page["text"]);
  
  # optional: some settings, after new/init, before go()
  $x->enabletoc = 1;
  $x->enableinclude = 1;
  $x->snippets['**'] = "<strong>%s</strong>"; # instead of <b>
  
  # run all processing
  $x->go();
  
  # get the complete HTML output including <head>
  $html = $x->fullhtml;
  
  # alternatively, get some other variables:
  $body = $x->bodyhtml;     # only the part inside the <body> tags
  $fullconfig = $x->config; # what was in the "config" area of the file?
  
  
  == Notes ==
  
  - This is an early public release, ready to be tested.
  - Including disk files is disabled out of the box, because of 
    potential vulnerabilities. Enabling it on systems where
    untrusted people could edit the t2t content is not recommended.
    A future version may allow the inclusion of files from the 
    current directory or only with *.t2t extension.
    To enable inclusions, use $x->enableinclude = 1;

*/

class T2T {
  # these variables could be read or forced
  var $title = '';         # the document title
  var $content = '';       # the content of the t2t file
  var $headers = '';       # the first 3 lines of the t2t file
  var $enableheaders = 1;  # enables the first 3 lines headers    (default=1)
  var $enableproc = 1;     # enables the pre and post processor   (default=1)
  var $enabletagged = 1;   # enables the tagged mark (''tagged'') (default=1)
  var $enableraw = 1;      # enables the raw mark (""raw"")       (default=1)
  var $enableverbatim = 1; # enables the verbatim mark (``raw``)  (default=1)
  var $enablehotlinks = 1; # enables hotlinks [http://www.externalserver.com/images.jpg]  (default=1) (note: it's not enabled in the python implementation of txt2tags)
  var $config = '';       # the full config area, including ext.ref.
  var $bodytext = '';     # the full body text after inclusions
  var $bodyhtml = '';     # the innerHTML of the body of the output, no <html>...<head>
  var $fullhtml = '';     # the full <html>...</html> output
  var $enabletoc = 0;     # automatically enabled if %%toc or %!options: --toc
  var $enableinclude = 1; # allow file inclusions 
  var $maxtoclevels = 5;  # h1-h? titles go into toc, same as %!options: --toc-level 1
  var $mtime;             # last modified timestamp of the input file
  var $date;              # timestamp of the current date
  var $cssfile = '';      # the css file to be included in the HTML header
  var $maskemail = 0;     # rewrite plaintext e-mail links
  var $encoding = "UTF-8";             # assume default encoding if none in file
  var $parsetargets = "html|xhtml";    # accept %!command(html) and %!command(xhtml)
  var $snippets = array(
  'header1'         => "<h1>%s</h1>\n", # text (first line of file)
  'header2'         => "<h2>%s</h2>\n", # text
  'header3'         => "<h3>%s</h3>\n", # text
  'headerwrap'      => "<div style='text-align:center;'>\n%s</div>\n", # headers
  'title'           => '<h%d id="%s">%s</h%1$d>', # level, id, text
  'hrule'           => '<hr class="%s"/>', # light|heavy
  'verbatim'        => "<pre>\n%s</pre>",  # content
  'mono'            => '<code>%s</code>',  # content
  'center'          => "<center>%s</center>", # content
  'img'             => '<img align="%s" src="%s" border="0" alt=""/>', # align, url
  'link'            => '<a href="%s">%s</a>', # url, text
  'cssfile'         => '<link rel="stylesheet" href="%s" type="text/css"/>',
  
  '**'              => '<b>%s</b>', # bold content
  '//'              => '<i>%s</i>', # italics content
  '__'              => '<u>%s</u>', # underlined content
  '--'              => '<s>%s</s>', # striked content
  
  'tableopen'       => "<table %s cellpadding=\"4\">\n", # align, border
  'tableclose'      => "</table>\n",
  'tablerow'        => " <tr>\n%s </tr>\n", # tagged cells
  'tablehead'       => "  <th%s>%s</th>\n", # align, content
  'tablecell'       => "  <td%s>%s</td>\n", # align, content
  
  # special
  'blockquoteopen'  => '<blockquote>',
  'blockquoteclose' => '</blockquote>',
  'paraopen'        => '<p>',
  'paraclose'       => '</p>',
  
  '+listopen'       => "<ol>\n", 
  '+listclose'      => "</ol>\n", 
  '+itemopen'       => "<li>", 
  '+itemmiddle'     => "", 
  '+itemclose'      => "</li>\n",
  
  '-listopen'       => "<ul>\n", 
  '-listclose'      => "</ul>\n", 
  '-itemopen'       => "<li>", 
  '-itemmiddle'     => "", 
  '-itemclose'      => "</li>\n",
  
  ':listopen'       => "<dl>\n", 
  ':listclose'      => "</dl>\n", 
  ':itemopen'       => "<dt>", 
  ':itemmiddle'     => "</dt><dd>\n", 
  ':itemclose'      => "</dd>\n",
  'listindent'      => '   ', # nicer HTML output
  
  # title, encoding, version, styles, body
  'html'            => '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=%s"/>
<meta name="generator" content="txt2tags.class.php version %s"/>
%s
</head>
<body bgcolor="white" text="black">
%s
</body></html>');
  # used internally
  var $infile = array();
  var $outfile = array();
  var $preproc = array();
  var $postproc = array();
  var $KPV = array();
  var $KPCount = 0;
  var $csslink = '';
  function T2T($input, $isfile = 0) {    
    
    $this->set_macros($input, $isfile);     # macros
    # get content
    $this->content = $isfile 
      ? $this->read($input, true) 
      : str_replace("\r", '', $input);
    
    # get header, config, body
    $this->R = $this->head_conf_body($this->content);
    
    # public variables 
    $this->headers  = implode("\n", $this->R['header']);
    $this->config   = implode("\n", $this->R['config']);
    $this->bodytext = implode("\n", $this->R['body']);
  }
  
  function go($output = '') { # run the full processing
    
    $this->parse_config($this->R['config']); # read config settings
    $lines = $this->run_preproc($this->R['body']); # run %!preproc replacements
    
    # strip comments, identify areas and titles, tables and horizontal rules (bars)
    $lines = $this->firstpass($lines); 
    
    # second pass 
    $lines = $this->secondpass($this->R['header'], $lines);
    
    # restore
    $body = implode("\n", $lines);
    $body = $this->Restore($body);
    $body = str_replace(array("\032\032", "\033\033"), '', $body);
    
    # public variables 
    $this->title = $this->esc($this->run_macros($this->R['header'][0]));
    $this->bodyhtml = $this->run_postproc($body); # %!postproc replacements
    $html = sprintf($this->snippets['html'], $this->title, $this->encoding, 
      $GLOBALS['T2TVersion'], $this->csslink, $body);
    $this->fullhtml = $this->run_postproc($html); # %!postproc replacements
    
    if($output=='body') return $this->bodyhtml;
    if($output=='html') return $this->fullhtml;
    return;
  }
  
  function parse_config($lines) { # try to read the supported configuration options
    $opts = "encoding|style|postproc|preproc|options";
    $tgts = $this->parsetargets;
    foreach($lines as $c){
      if(preg_match("/^%!\\s*({$opts})(?:\\((?:{$tgts})\\))?\\s*:\\s*(.*)$/i", $c, $m)) {
        # options, preproc and postproc are cumulative
        list(, $setting, $val) = $m;
        switch(strtolower($setting)) {
          case "encoding" : $this->encoding = trim($val); break;
          case "style" : $this->csslink = sprintf($this->snippets['cssfile'], trim($val)); 
          case "preproc"  : 
			if ($this->enableproc == 1) {
				$this->preproc[]  = $this->add_proc($setting, trim($val)); 
				break;
			}
          case "postproc" : 
			if ($this->enableproc == 1) {
				$this->postproc[] = $this->add_proc($setting, trim($val)); 
				break;
			}
          case "options": 
            if(strpos(" $val", '--mask-email')) $this->maskemail = 1;
            if(preg_match('/--toc(?!-)/', $val)) $this->enabletoc = 1;
            if(preg_match('/--toc-level[= ]+([1-5])/', $val, $n)) $this->maxtoclevels = $n[1];
            if(preg_match('/--encoding[= ]+(\\S+)/', $val, $n)) $this->encoding = $n[1];
            if(preg_match('/--style[= ]+(\\S+)/', $val, $n)) 
              $this->csslink = sprintf($this->snippets['cssfile'], trim($val)); 
            break; 
        }
      }
    }
  }
  
  function add_proc($when, $x) { # add a pre-processor or a postprocessor
    if(! preg_match("/^ *(\"[^\"]+\"|'[^']+'|\\S+)\\s*(.*)$/", $x, $m)) return;
    
    $s = preg_replace('/^("|\')(.*?)\\1$/', '$2', trim($m[1]));
    $r = preg_replace('/^("|\')(.*?)\\1$/', '$2', trim(@$m[2]));
    $r = preg_replace('/\\\\(?=[0-9])/', '$', $r);
    $r = str_replace(array('\\n', '\\t'), array("\n", "\t"), $r);
    return array("\032$s\032m", $r);
  
  }
  function run_preproc($lines) { # make the replacements
    $body = implode("\n", $lines);
    foreach($this->preproc as $a) {
      $body = preg_replace($a[0], $a[1], $body);
    }
    return explode("\n", $body);
  }
  function run_postproc($body) { # make the replacements
    foreach($this->postproc as $a) {
      $body = preg_replace($a[0], $a[1], $body);
    }
    return $body; # end of processing
  }

  function firstpass($lines) { # strip comments, identify areas, titles, toc
    $snippets = $this->snippets;
    $toc = array();
    $postoc = 0;
    
    $lines2 = array();
    $openarea = '';
    $areacontent = '';
    $toccnt = 0;
    $tocnbs = array(0, 0, 0, 0, 0, 0);
    $table = '';
    foreach($lines as $line) {
    
      # special areas raw, tagged, verbatim, comments
      if($openarea) {
        if($line == $openarea) { # close area
          if(rtrim($line) != "%%%") # comment areas
            $lines2[] = $this->closeRTV($openarea, $areacontent);
        }
        else { # fill area
          $areacontent .= "$line\n";
        }
        continue;
      }
      if(preg_match('/^("""|```|\'\'\'|%%%) *$/', $line)) { # open area
        $openarea = trim($line);
        continue;
      }
      
      if($line!='' && $line{0}=='%' && ! preg_match('/^%%(infile|outfile|date|mtime|rand|toc\\s*$)/i', $line) )
        continue; # remove comment lines
        
      # special lines raw, tagged, verbatim
      if(preg_match('/^("""|```|\'\'\') /', $line, $m)) { 
        $lines2[] = $this->closeRTV($m[1], substr($line, 4));
        continue;
      }
    
      # Title, Numbered Title 
      if(preg_match('/^ *((=){1,5})(?!=)\\s*(\\S.*[^=]|[^\\s=])\\1(?:\\[([\\w-]+)\\])?\\s*$/', $line, $m) ||
        preg_match('/^ *((\\+){1,5})(?!\\+)\\s*(\\S.*[^+]|[^\\s=])\\1(?:\\[([\\w-]+)\\])?\\s*$/', $line, $m)  ) {
        $toccnt++;
        $anchor = @$m[4] ? $m[4] : "toc$toccnt";
        $txt = $this->esc(trim($m[3]));
        $level = strlen($m[1]);
        
        if($m[2]=='+') {
          if($level>$tocnbs[0])$tocnbs[$level] = 1;
          else $tocnbs[$level]++;
          if($level<$tocnbs[0])for($i=$level+1; $i<6; $i++) $tocnbs[$i] = 0;
        
          $prefix = implode(".", array_slice($tocnbs, 1, $level));
          $prefix = preg_replace('/^(0\\.)+/', '', $prefix);
          $txt = "$prefix. $txt";
          $tocnbs[0] = $level;
        }
        
        $txt = $this->Keep($txt);
        $lines2[] = "\032\032".sprintf($snippets['title'], $level, $anchor, $txt); # \032: block that cannot be nested in lists
        
        # collect toc entries
        if($this->maxtoclevels>=$level)
          $toc[] = $this->sp($level) . "- [$txt #$anchor]";
        
        continue;
      }
      # tables
      if(preg_match('/^ *(\\|\\|?) /', $line, $m)) {
        if(!$table) { # open table
          $attr = ($line{0}==' ')? ' align="center"' : "";
          if(preg_match('/\\|\\s*$/', $line)) {
            $attr .=  ' border="1"';
          }
          
          $table = sprintf($snippets['tableopen'], $attr);
        }
        # fill table
        if($m[1]=='||') $fmt = $snippets['tablehead'];
        else $fmt = $snippets['tablecell'];
        
        $line = $this->run_inline($line);
        
        $row = substr($line, strlen($m[0]));
        
        if(! preg_match('/\\|\\s*$/', $row)) $row .= ' | ';
        $m = preg_split('/( \\|+(?: |$))/', $row, -1, PREG_SPLIT_DELIM_CAPTURE);

        $cells = '';
        for($i=1; $i<count($m); $i+=2){
          $c = $m[$i-1];
          $attr = '';
          if($c && $c{0}==' ') {
            $attr = (substr($c, -1)==' ') ? ' align="center"' : ' align="right"';
          }
          $span = strlen(trim($m[$i]));
          if($span>1) $attr .= " colspan=\"$span\"";
          $cells .= sprintf($fmt, $attr, $c);
        }
        $table .= sprintf($snippets['tablerow'], $cells);
        continue;
      }
      elseif($table) { # close table
        $lines2[] = "\033\033". $this->Keep($table . $snippets['tableclose']); # \033: block that can be nested in lists
        $table = '';
      }
      # horizontal rule (bar1, bar2)
      if(preg_match('/^ *(=|-|_){20,}\\s*$/', $line, $m)) {
        $class = $m[1] == "=" ? 'heavy':'light';
        $lines2[] = "\032\032".$this->Keep(sprintf($snippets['hrule'], $class));
        continue;
      }
      if(preg_match("/^ +\\[([\034\\w_,.+%$#@!?+~\\/-]+\\.(?:png|jpe?g|gif|bmp|svg))\\] +$/i", $line)) {
        $lines2[] = "\033\033". $this->Keep(sprintf($snippets['center'], $this->run_inline($line)));
        continue;
      }
      
      if(trim(strtolower($line))=='%%toc') {
        $this->enabletoc = $postoc = 1;
        $line = '%%toc';
      }
      $lines2[] = $line;
    } # end foreach line
    
    # close ALL
    if($openarea && $openarea != '%%%') # close all areas
      $lines2[] = $this->closeRTV($openarea, $areacontent);
    
    if($table) 
      $lines2[] = "\033\033". $this->Keep($table . $snippets['tableclose']."\n");
      
    if($this->enabletoc && count($toc)) {
      if($postoc) { # there is %%toc in the page
        array_unshift($toc, "\032\032");
        $toc[] = "\032\032";
        foreach($lines2 as $k=>$v) {
          if($v=='%%toc') array_splice($lines2, $k, 1, $toc);
        }
      }
      else { # before the body: bar, toc-list, bar
        $bar = "\032\032".$this->Keep(sprintf($snippets['hrule'], 'light'));
        array_unshift($toc, $bar);
        $toc[] = $bar;
        
        $lines2 = array_merge($toc, $lines2);
      }
    }
    return $lines2;
  }
  
  function secondpass($headers, $lines) { # all other marks
    $snippets = $this->snippets;
    
    $lines2 = array();
    $html = '';
    for($i=0; $i<3; $i++) {
      $j = $i+1;
      $h = $this->esc($headers[$i]);
      if($h) $html .= sprintf($snippets["header$j"], $this->run_macros($h));
    }
    if($html) $lines2[] = $this->Keep(sprintf($snippets["headerwrap"], $html));
      
    $blockquote = 0;
    $blockquotecontent = '';
    $para = false;
    $openlist = 0;
    $listcontent = '';
    $ListLevels = array(array(-1, '', '')); # $level, $spaces, $type

    foreach($lines as $line) {
    
      # blockquote
      if(preg_match('/^(\\t+)([^\\t].*)$/', $line, $m)) {
        if($para) { 
          $para = false;
          $lines2[] = $snippets['paraclose'];
        }
        $level = strlen($m[1]);
        $blockquotecontent .= $this->fixblockquote($blockquote, $level) 
          . $m[1]. $this->run_inline($m[2])."\n";
        continue;
      }
      elseif($blockquote) { # close bq
        $lines2[] = "\032\032".$blockquotecontent . $this->fixblockquote($blockquote, 0);
        $blockquotecontent = '';
      }
      
      # List, Numbered List, Definition List
      if(preg_match('/^( *)([+-]) (\\S.*)$/', $line, $m) || 
        preg_match( '/^( *)(:) ( *\\S.*)$/', $line, $m)) {
        $openlist = 2;
        if($para) { 
          $para = false;
          $lines2[] = $snippets['paraclose'];
        }
        
        list(, $spaces, $type, $text) = $m;
        $text = $this->run_inline($text);
        $upped = 0;
                
        while(count($ListLevels)>0) {
          list($plevel, $pspaces, $ptype) = array_pop($ListLevels);
          
          ## close previous list
          if($plevel>=0 && strcmp($spaces, $pspaces)<0) {
            $listcontent .= "\n".$this->sp($plevel).$snippets["{$ptype}itemclose"] . $this->sp($plevel).$snippets["{$ptype}listclose"];
            $upped ++;
            continue;
          }
          if($upped) $pspaces = $spaces;
          $ListLevels[] = array($plevel, $pspaces, $ptype); # restore
          
          ## open list
          if($plevel<0 || strcmp($spaces, $pspaces)>0) { # new list/sublist
            $level = $plevel+1;
            $listcontent .= "\n" . $this->sp($level). $snippets["{$type}listopen"];
            $ListLevels[] = array($level, $spaces, $type);
          }
          else { ## close prev item
            $listcontent .= "\n".$this->sp($plevel).$snippets["{$ptype}itemclose"];
            $level = $plevel;
            if($ptype!=$type) {
              $listcontent .= "\n".$this->sp($level).$snippets["{$ptype}listclose"]
                             ."\n".$this->sp($level).$snippets["{$type}listopen"];
              $ListLevels[count($ListLevels)-1][2] = $type; # restore
            }
          }
          ## open item
          $listcontent .= $this->sp($level).$snippets["{$type}itemopen"];
          
          ## fill content
          $listcontent .= $text . $snippets["{$type}itemmiddle"];
          
          break;
        }
        continue;
      }
      elseif($openlist) {
        if(trim($line)=='' || strpos($line, "\032\032")===0 ) {
          $openlist --;
          if(!$openlist || strpos($line, "\032\032")===0) { # second empty line, close ALL
            while(count($ListLevels)>1) {
              list($plevel, $pspaces, $ptype) = array_pop($ListLevels);
              $listcontent .= "\n".$this->sp($plevel).$snippets["{$ptype}itemclose"]
                                  .$this->sp($plevel).$snippets["{$ptype}listclose"];
            }
            $lines2[] = $this->Keep($listcontent);
            $lines2[] = $line;
            $listcontent = "";$openlist=0;
            continue;
          }
          else {
            list($plevel, ,) = $ListLevels[count($ListLevels)-1];
            $listcontent .= $this->sp($plevel+1)."{$snippets["paraopen"]}{$snippets["paraclose"]}\n";
          }
        }
        else {
          list($plevel, $pspaces, $ptype) = array_pop($ListLevels);
          if(preg_match('/^(( *)([+-:])) *$/', $line, $m) && $m[1]== "$pspaces$ptype") { # close 
            $listcontent .= "\n".$this->sp($plevel).$snippets["{$ptype}itemclose"] 
                              .  $this->sp($plevel).$snippets["{$ptype}listclose"];
            if($plevel) $openlist = 2;
            else {
              $lines2[] = $this->Keep($listcontent);
              $listcontent = "";$openlist=0;
              continue;
            }
          }
          else {
            if($openlist==1) 
              $listcontent .= $this->sp($plevel+1)."{$snippets["paraopen"]}{$snippets["paraclose"]}\n";
            $openlist = 2;
            $ListLevels[] = array($plevel, $pspaces, $ptype);
            $listcontent .= $this->sp($plevel+1).$this->run_inline($line)."\n";
          }
        }
        continue;
      }
      
      if(preg_match("/^[\032\033]{2}/", $line)) { 
        if($para) { 
          $para = false;
          $lines2[] = $snippets['paraclose'];
        }
        $lines2[] = $line;
        continue;
      }
      
      if($para) {
        if(trim($line)=='') {
          $para = false;
          $lines2[] = $snippets['paraclose'];
        }
        else {
          $lines2[] = $this->run_inline($line);
        }
        continue;
      }
      # $para = false;
      if(trim($line)!='') {
        $lines2[] = $snippets['paraopen'];
        $lines2[] = $this->run_inline($line);
        $para = true;
        continue;
      }
      
      $lines2[] = $line;
    }
    # close ALL
    if($blockquote) 
      $lines2[] = $this->Keep($blockquotecontent . $this->fixblockquote($blockquote, 0));
    if($openlist) {
      while(count($ListLevels)>1) {
        list($plevel, $pspaces, $ptype) = array_pop($ListLevels);
        $listcontent .= "\n".$this->sp($plevel).$snippets["{$ptype}itemclose"]
                            .$this->sp($plevel).$snippets["{$ptype}listclose"];
      }
      $lines2[] = $this->Keep($listcontent);
    }
    if($para) { 
      $para = false;
      $lines2[] = $snippets['paraclose'];
    }
    
    return $lines2;
  }
  
  function run_inline($line) { # inline transformations (links, images, bold, mono...)
    $snippets = $this->snippets;
    # inline Raw, Mono, Tagged
    if(preg_match_all('/(\'|"|`){2}([^\\s](.*?[^\\s])?\\1*)\\1\\1/', $line, $m, PREG_SET_ORDER)) {
      foreach($m as $a) {
        $type = $a[1].$a[1];
        $c = $this->PSS($a[2]);
        $tmp = $this->closeRTV($type, $c);
        $line = preg_replace('/(\'|"|`){2}([^\\s](.*?[^\\s])?\\1*)\\1\\1/', $tmp, $line, 1);
      }
    }
    # macros
    $line = $this->run_macros($line);
    
    # <[img]>
    $imgrx = "\\[([\034\\w_,.+%$#@!?+~\\/-]+\\.(?:png|jpe?g|gif|bmp))\\]";
    
    $line = preg_replace("/^$imgrx(?=.)/ei",
      "\$this->Keep(sprintf(\$snippets['img'], 'left', '$1'))", $line);
    $line = preg_replace("/(?<=.)$imgrx$/ei",
      "\$this->Keep(sprintf(\$snippets['img'], 'right', '$1'))", $line);
      
      
    $line = preg_replace("/$imgrx/ei",
      "\$this->Keep(sprintf(\$snippets['img'], 'middle', '$1', 'middle'))", $line);
    
    $UEX = '<>"{}|\\\\^`()\\[\\]\''; # UrlExcludeChars
    $PRT = '(?:https?|ftp|news|telnet|gopher|wais|mailto):';
    
    if ($this->enablehotlinks == 0) {
		$Links = array(
		  "{$PRT}[^\\s$UEX]+" =>'',
		  "www\\d?\\.[^\\s$UEX]+" =>'http://', # lazy links
		  "ftp\\d?\\.[^\\s$UEX]+" =>'ftp://',  # lazy links
		  "\\w[\\w.-]+@[\\w-.]+[^\\s$UEX]+" =>'mailto:',  # lazy links
			); #     
    }
    else {
		$Links = array(
		  //"{$PRT}[^\\s$UEX]+" =>'',  # allows hotlinks by disabling this part
		  //"www\\d?\\.[^\\s$UEX]+" =>'http://', # lazy links won't work here
		  "ftp\\d?\\.[^\\s$UEX]+" =>'ftp://',  # lazy links
		  "\\w[\\w.-]+@[\\w-.]+[^\\s$UEX]+" =>'mailto:',  # lazy links
			); #  
	}
    
    # [txt link], [txt #anchor]
    foreach($Links as $k=>$v) {
      $line = preg_replace("/\\[([^\\]]+?) +($k)\\]/ei", 
        "\$this->Keep(sprintf(\$snippets['link'], \$this->esc('$v$2'), \$this->esc('$1', 1)))", $line);
    }
    # local links
    $line = preg_replace("/\\[([^\\]]+?) +([^\\s$UEX]+)\\]/ei", 
      "\$this->Keep(sprintf(\$snippets['link'], \$this->esc('$2'), \$this->esc('$1', 1)))", $line);
    
    # free links www.link, e@mail, http://link
    foreach($Links as $k=>$v) {
      if($v=='mailto:' && $this->maskemail) {
        $line = preg_replace("/\\b({$k}[^\\s.,?!$UEX])/ei",
          "\$this->Keep('&lt;' . str_replace(array('@', '.'), array(' (a) ', ' '), '$1') . '&gt;$2')", $line);
      }
      else {
        $line = preg_replace("/\\b({$k}[^\\s.,?!$UEX])/ei", 
          "\$this->Keep(sprintf(\$snippets['link'], \$this->esc('$v$1'), \$this->esc('$1')))", $line);
	  }
    }
    
    $line = $this->esc($line);
    
    # Bold, Italic, Underline, Strike
    $b = array('*', '/', '_', '-');
    foreach($b as $c) {
      $q = preg_quote($c, '/');
      $line = preg_replace("/($q){2}([^\s](?:.*?\\S)?\\1*)\\1\\1/e", 
        "sprintf(\$snippets['$c$c'], \$this->PSS('$2'))", $line);
    }
    return $line;
  }
  
  function set_macros($input, $isfile = 0) {
    $this->date=time();
    if($isfile && file_exists($input)) {
      $this->mtime = filemtime($input);
      $this->infile = $this->fileattr($input);
    }
    else {
      $this->mtime = time();
      $this->infile = $this->fileattr('-');
    }
    $this->outfile = $this->fileattr('-');
  }
  function run_macros($line) {
    $line = preg_replace('/%%(date|mtime)(\\((.+?)\\))?/ie',  
      'strftime("$2"? $this->PSS("$3"):"%Y%m%d", $this->$1)', $line);
    $line = preg_replace('/%%infile(?:\\((.*?)\\))?/ie', 
      '"$1" ? str_replace(array_keys($this->infile), array_values($this->infile), "$1")
      : $this->infile["%f"]', $line);
    $line = preg_replace('/%%outfile(?:\\((.*?)\\))?/ie', 
      '"$1" ? str_replace(array_keys($this->outfile), array_values($this->outfile), "$1")
      : $this->outfile["%f"]', $line);
    /*$line = preg_replace_callback('/%%rand\([0-9]+,[0-9]+\)/',  'create_function(return(rand($1,$2);))', $line);
     $line = preg_replace('/%%rand\([0-9]+,[0-9]+\)/i', '<? rand($1,$2); ?>', $line);
    $line = preg_replace_callback('/%%rand\\(([0-9]+),([0-9]+)\\)/',  'return(rand($1,$2);)', $line);
*/
    return $line;
  }
  
  function fixblockquote(&$prev, $curr) { # close open blocks, open sub-blocks
    $s = $this->snippets;
    $x = '';
    while ($prev<$curr) $x .= str_repeat("\t", ++$prev) . $s['blockquoteopen'] . "\n";
    while ($prev>$curr) $x .= str_repeat("\t", $prev--) . $s['blockquoteclose'] . "\n";
    return $x;
  }
  
  function closeRTV(&$type, &$x) { # Raw, Tagged or Verbadim lines/areas
    switch($type{0}) {
      case '%': $type = $x = ''; return '';
      case "'": 
		if ($this->enabletagged == 1) {
			$y = $x; 
			break;
		}
			
      case '"': # raw
		if ($this->enableraw == 1) {
			$y = $this->esc($x);
			break;
		}
      case '`': # verbatim, mono
		if ($this->enableverbatim == 1) {
			$s = $this->snippets;
			$fmt = (strlen($type)==2) ? $s['mono'] : $s['verbatim'];
			$y = sprintf($fmt, $this->esc($x));
			break;
		}
		else {
			$y = $this->esc($x);
		}
    }
    $block = (strlen($type)==3) ? "\033\033" : '';
    $type = $x = '';
    return $block. $this->Keep($y);
  }
  function PSS($x) { return str_replace('\\"','"',$x); } # Strip RegExp slashes
  function Keep($x) { # preserves a string from being processed by wiki markups
    $x = $this->Restore($x);
    $this->KPCount++; $this->KPV[$this->KPCount]=$x;
    return "\034\034{$this->KPCount}\034\034";
  }
  function Restore($x) { # recovers all hidden strings
    return preg_replace("/\034\034(\\d.*?)\034\034/e", "\$this->KPV['\$1']", $x);
  }
  function sp($n){ # add spaces for nicer indented HTML source code
    return str_repeat($this->snippets['listindent'], $n);
  }
  
  function esc($x, $pss=0) { # htmlspecialchars
    if($pss) $x = $this->PSS($x);
    return str_replace(
      array('&', '<', '>', '$'),
      array('&amp;', '&lt;', '&gt;', '&#036;'),
      $x);
  }
  
  function fileattr($fname) { # variables that can be in %%infile()
    if($fname == '-') return array(
      '' => '-', '%f'=> '-', '%F'=> '-', '%e'=> '', 
      '%p'=> '-', '%d'=> '.', '%D'=> '.', '%%'=>'%');
    preg_match('/\\.([^.\\/]+)$/',$fname, $m); $ext=@$m[1];
    return array(
      ''  => basename($fname),
      '%f'=> basename($fname),
      '%F'=> preg_replace('/\\.[^.]+$/', '', basename($fname)),
      '%e'=> $m[1],
      '%p'=>realpath($fname),
      '%d'=>dirname(realpath($fname)),
      '%D'=>basename(dirname(realpath($fname))),
      '%%'=>'%');
  }
  
  function read($filename, $allowed = false) { # get a file content
    if(!$allowed) return '';
    if(!file_exists($filename)) return '';
    return str_replace("\r", '', implode('', @file($filename)));
  }
  
  # get the Header, Config area and Body of a t2t file
  # the function will include the content of any included files
  function head_conf_body($content) {
    $lines = explode("\n", $content);
    $R = array();
    $R['header'] = $R['config'] = $R['body'] = array();
    # headers 
	if ($this->enableheaders == 0) {
		$R['header'][0] = $R['header'][1] = $R['header'][2] = '';
	}
    else if($lines[0]=='') {
      $R['header'][0] = $R['header'][1] = $R['header'][2] = '';
      array_shift($lines);
    }
    else {
      for ($i=0; $i<3 && isset($lines[0]); $i++) {
        $R["header"][$i] = array_shift($lines);
      }
    }
    # config
    $mlcomment = false;
    while(isset($lines[0])) {
      $line = array_shift($lines);
      if(rtrim($line) == '%%%') { # comment areas in Config
        $mlcomment = ! $mlcomment;
        continue;
      }
      if($mlcomment || trim($line)=='') continue;
      
      if(preg_match('/^%!\\s*includeconf\\s*:\\s*(.+)$/', $line, $m)) {
        $f = trim($m[1]);
        if($f{0}!='/') $f =  $this->infile['%d'] . DIRECTORY_SEPARATOR . $f;
        $r = $this->head_conf_body($this->read($f, $this->enableinclude));
        for($i=count($r['config'])-1; $i>=0; $i--)
          array_unshift($lines, $r['config'][$i]); 
        continue;
      }
      
      if($line{0} != '%' || preg_match('/^%(%(date|mtime|toc|infile|outfile|rand)|! *include)/i', $line)) {
        array_unshift($lines, $line); 
        break;
      }
      $R["config"][] = $line;
    }
    
    # body
    $mlcomment = false;
    while(isset($lines[0])) {
      $line = array_shift($lines);
      
      if(rtrim($line) == '%%%') { # comment areas
        $mlcomment = ! $mlcomment;
        continue;
      }
      if($mlcomment) continue;
      
      if(preg_match('/^%!\\s*include(?:\\(x?html\\))?\\s*:\\s*(``|\'\'|""|)(.+)\\1\\s*$/', $line, $m)) {
      
        $f = trim($m[2]);
        if($f{0}!='/') $f =  $this->infile['%d'] . DIRECTORY_SEPARATOR . $f;
        $r = $this->head_conf_body($this->read($f, $this->enableinclude));
      
        if($m[1]) {
          $q = implode("\n", $r['body'])."\n";
          $type = str_repeat($m[1]{1}, 3);
          $line = $this->closeRTV($type, $q);
        }
        else {
          for($i=count($r['body'])-1; $i>=0; $i--)
            array_unshift($lines, $r['body'][$i]);
          continue;
        }
      }
      $R['body'][] = $line;
    }
    return $R;
  }
}

