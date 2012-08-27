<?php
/**
  txt2tags.php : text to HTML convertor in PHP
  Written by (c) Petko Yotov 2012 www.pmwiki.org/Petko
  Development sponsored by Eric Forgeot.
  
  This is an example use of the txt2tags.class.php script
  on the command line.
  
  In a terminal, call 
    php command_line.php file1.t2t
    php command_line.php *.t2t
    
  You can edit this file and adapt it for your needs.
  
*/


require_once('txt2tags.class.php');

for($i=1; $i<$argc; $i++) {
  $f = $argv[$i];
  
  if(file_exists($f)) {
    
    # create the T2T object with a file
    $x = new T2T($f, true);
    $x->enableinclude = 1;
    
    # run all processing
    $x->go();
    
    # get the complete HTML output
    $html = $x->fullhtml;
    
    # do whatever you have to with it
    file_put_contents("$f.html", $html);
    echo "$f.html written.\n";
    
  }

}

