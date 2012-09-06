Simple PHP File Editor script
by Dustin Minnich


%%toc

//License: "do whatever you like with this script, i care not".//

It allows you to edit text based files that are already on your server.  




== Features ==

- When looking for files it can edit it recurses into subdirectories. 
- Very small.  The entire script is one file.  
- Very easy to change. this script uses very straightforward syntax and has
lots of comments.  If you have ever messed with PHP you should be able to
adapt it to fit your needs. 
- It outputs valid CSS and XHTML by default.
- completely free.  no links back to my page.  do whatever you like with this
script, i care not.


== What this script doesn't do ==

- This is NOT a file manager script. 
- You can not move or rename files. 
- You can not chmod or chown files.
- You can not upload or download files.
- You can not create or delete files. 
- There is only basic password protection. Consider Using htaccess files. 
- There is no WYSIWYG editor.  
- Only text based files are supported. 
- You can not change out of the default directory you specify in the script.
- There is no special viewer for media (no image viewer, no audio player, etc).
- No support for languages other than english. 
- No automatic backing up of files.  
- No syntax highlighting.  


== Who this script is for ==

- Me! 
- People who want a small script that edits files and __not__ a FTP replacement
script.  
- Web developers that like to make quick and dirty changes to their pages, and
don't mind seeing the source code. 
- For people new to PHP (like me).  This is a good script to look at and learn
from and adapt to your needs.


== Installation ==

+ Create an "admin" directory on your webhost.
+ Update the $filedir variable in fileed.php.  This directory should be the
full path to the directory of files you wish to be able to edit with this
script. 
+ Upload fileed.php into the admin directory. 
+ Use your webhosts CP to password protect the admin directory.
+ Test the password protection.  Make sure you don't see the form unless you
enter the proper login and password. 
+ Try the script out!


== Updates and Credit ==

The following people have contributed code to this project:

- Dustin Minnich: original project: http://www.dminnich.com/my_work.php
- spagettilogic.org - Simple Password Auth
- anoldman.com - Regular expressions modernization and rewrite

Their contributed code will be noted inside of fileed.php.
Thanks guys!


== Notes ==

- Why is the file I want to edit is not showing up in the file drop down box?

This could be caused by two reasons.  
 + That specific file is not writable. chmod it 666 or greater.  
 + That specific file does not have a 'valid' extension. By default this script 
only lists text based files with common extensions (ie: txt,php,htm,html,css,asp,etc).
Add the extension you need tothe valid_ext array in fileed.php. Instructions to do 
this are at the top of fileed.php. Also, the following things do not show up in the edit 
drop down box by default: current directory (.), up a directory (..),
the file itself ($me), and unix hidden files.      

- Why does the file i'm editing show the tag [/textarea] instead of
< /textarea >? 
Since this script opens the file you want to edit inside of 
a textarea the file you are editing  can not contain < /textarea >. If it did
the editing box would close at that position in the file you are editing and
the rest of the file you were trying to edit would be shown 
below the fileed.php form.  <--Thats really confusing.  Think about it
though, it makes sense.  Just leave the tag alone, it gets replaced with
the proper < /textarea > tag when you save your changes.

- Don't want fileed.php to recursively list all the files you can edit?
Search for $filelist = directoryToArray($filedir, true);
and change true to false.
  
- Files you want to edit must be chmoded properly. Files need to be 666 or
higher for this script to be able write changes to them. Do not recursively
chmod all the files in a directory.  This is dangerous and will likely break
scripts that check to make sure their config files aren't world writable.
Just chmod the files you really really need to edit. 
- Want to edit files with slashes in them?  Comment out the stripslashes line
in fileed.php.  
- This script has not been thoroughly tested.  
- This is the only version of this script. I consider it a done project.
- I guarantee nothing about this script. I am not offering any support for it,
so please do not contact me regarding it.


- txt2tags adaptation specific notes:
 - all file extensions in the original php file were removed except for 'txt'. We added 't2t' as well, of course. If you need to edit files with different extensions, please add them by hand, or get the original php script on http://www.dminnich.com/my_work.php
 - password is enabled, but you should change the default one (search for the $password variable). You might also consider disabling the built-in password system, and use a .htaccess which could prove to be more secure. You can also put the fileed.php into a folder with a random name on your server so visitors can't guess it even exists. You can also rename the fileed.php file.
 
 
