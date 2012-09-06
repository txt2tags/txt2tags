<?

// Simple PHP File Editor 
// original by Dustin Minnich

// License: "do whatever you like with this script, i care not".

// Found on http://www.dminnich.com/my_work.php

//By default this script will allow you to edit all the files in $filedir that
//have extensions in the valid_ext array and are writable.  It also allows you
//to edit all the files that are writable and have valid extensions in the sub
//folders of $filedir.  In other words, it recursively searches for files you
//can edit in $filedir.  If you wish to change this behavior, so that it only
//stays in $filedir and doesn't drill down to any of its subdirs,--search for
//$filelist = directoryToArray($filedir, true); and change true to false.

//YOU MUST CHANGE THIS VARIABLE!! Specify the full path to the directory of
//files you wish to be able to edit. NO TRAILING SLASH.
$filedir = $_SERVER['DOCUMENT_ROOT'].'/txt2tags-php';
// $filedir = "/home/yourlogin/public_html";

//Valid Extension array.  
//The array below lists the extensions files must have in order to 
//show up in the selection drop down box of fileed.php.  NOTE: In order for you
//to be able to edit a file it must have an extension in the array below and
//must be writable (chmoded 666). It must also be in the $filedir folder or 
//in a subfolder in the $filedir folder.  All folders that the script must
//transverse in order to reach your file must be chmoded at least 555. To
//add a new extenstion to this array do the following:
//1. Copy the bottom valid_ext line. Insert a new line below it
//   (hit enter).  Paste the line you copied.
//2. Increase [x] by one.
//3. Change the text inside the quotes to the extension you want to allow.
//   Case must match exactly.
//4. Save your changes.
$valid_ext[0] = "TXT";
$valid_ext[1] = "txt";
$valid_ext[2] = "t2t";
$valid_ext[3] = "T2T";
$valid_ext[4] = "txt2tags";
$valid_ext[5] = "TXT2TAGS";
/*$valid_ext[6] = "php";
$valid_ext[7] = "PHP";
$valid_ext[8] = "htm";
$valid_ext[9] = "HTM";
$valid_ext[10] = "html";
$valid_ext[11] = "HTML";
*/

//That should cover what most people use!  I hope anyhow :)


//The following password auth code was contributed by spaghettilogic.org.
//Note: It is rather simple and really shouldn't be used on sites  
//that have highly sensitive information or by people that have lots of 
//enimies; as it doesn't do hashing, brute force prevention, log outs, etc.
//None the less, it is a great addition for small sites! They can use it instead
//of or in addition to an htaccess file.  Thanks for the code James!

$password_enabled = 'true'; //Change to 'true' to enable passwords and to 'false' to disable it.
$password = 'password'; //If you enable passwords, change this!

if($password_enabled == 'true'){
session_start(); //Enable cookies

//If neither password nor cookie is present
if($_POST['password']!= $password && $_SESSION['password'] != $password){
print '
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style type="text/css">
h2 {text-align: center}
</style>
<title>Simple File Editor</title>
</head>
<body>
<h2>Simple File Editor</h2>
<form action="'.$_SERVER['PHP_SELF'].'" method="post">
<input name=password type=password>
<input type=submit name=login value="Log In">
</form>
</body>
</html>
';
return;
}elseif($_POST['password'] == $password && $_SESSION['password'] != $password){

//If password is present but cookie has not been set
$_SESSION['password'] = $password; 

}
}


//You should not have to change anything below this line. 


//IF browser does not send a POST request (ie: if open/save has not been
//pressed) then display the form and the list of files.
if(!$_POST['open'] && !$_POST['save']){
//if ($_SERVER['REQUEST_METHOD'] != 'POST'){
//If filedir is readable do...
if (is_readable($filedir)) {
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style type="text/css">
h2 {text-align: center}
</style>
<title>Simple File Editor</title>
</head>
<body>
<h2>Simple File Editor</h2>
<form action="<?=$PHP_SELF?>" method="post">
<table>
<tbody>
<tr>
<td>
<?

//Change into filedir
chdir($filedir);
//Print the directory we are in. Should match filedir.
echo "<p> We are in:  ";
echo "<br />";
echo getcwd();
echo "</p>";

//Continue page below.
//INFO for below: Select "name" is variable name.  Option value is variable
//"value".  
?>
<p> Please choose a file to open:</p>
<select name="the_file">
<?
//The below function will read directory contents into an array.
//Taken from http://www.bigbold.com/snippets/posts/show/155.
//Modified some. This will allow us to read all the contents of
//this directory and all sub-directories into an array.
//Once we have the array we will sort it alphabetically
//and print the filenames in the select box.
//The comments below the code snippets in the function
//are how I follow the code.  Since I did
//not write the original code they may not be entirely
//accurate. 

function directoryToArray($directory, $recursive) {
//Start function.  Parse var1 as directory.  Parse var2
//as true or false indicating whether to use recursive
//routine or not.

//Create a variable that referees to this file itself.  That way it can be
//excluded from the editable file list, just in case its in the directory 
//of files you want to edit.
$me = basename($_SERVER['PHP_SELF']);

$array_items = array();
//Define array for later use.
        if ($handle = opendir($directory)) {
                while (false !== ($file = readdir($handle))) {
//Don't add: this file itself ($me), unix hidden files (.files),
//the up directory link (..) and the current directory link (.) 
//to the array.  This will stop the accidental editing of
//important files, and confusing listings.
             

if ($file != "." && $file != ".." && $file != $me && substr($file,0,1) != '.') {
//Open the directory specified in the function.
//For every file that meets the above terms do...
                                if (is_dir($directory. "/" . $file)) {
//If the 'file' in the directory opened is a directory do...
                                        if($recursive) {
//If recursive is set, rerun the function on that directory.
                                                $array_items = array_merge($array_items, directoryToArray($directory. "/" . $file, $recursive));
                                        }
//Add the contents of recursed directory to the array.

//Comment the below two lines out to prevent directories from showing up 
//in the file editing list. 
                                //        $file = $directory . "/" . $file;
                                  //      $array_items[] = preg_replace("/\/\//si", "/", $file);
					 
					} else {
                                        $file = $directory . "/" . $file;
                                        $array_items[] = preg_replace("/\/\//si", "/", $file);
//Else if the "file" in the opened directory is a file (not a dir),
//replace // with / and add it to the array.
                                }
                        }
                }
                closedir($handle);
//Close the directory.
        asort($array_items);
//Sort the array alphabetically.
   }
        return $array_items;
//Return the array.
}

//End borrowed code.

//Create the array filelist by running the function
//on the filedir with recursing enabled.
//The true in this function enables recursion.  
//If you don't want the script to recursively 
//search for files you can edit change the true to false.
$filelist = directoryToArray($filedir, true);

//Loop through the array. The value in each row should be called $file and
//the following code should be executed against it.
foreach ($filelist as $file)
{
//Get the extensions of the files.  
//Look at each filename at and use
//strrchr to find the last occurrence
//of "." in the filename.  This returns .jpg
//for example.  Then use substr to return
//+1 of .jpg.  Meaning everything after ".". 
$ext = substr(strrchr($file, '.'), 1);
//If a file has an extension that
//is in the valid_ext array and that 
//file is writable list it in
// the drop down box. 
if (in_array($ext,$valid_ext) && is_writable($file)) {
//Add files to a select box.
echo "<option value=\"$file\">$file</option>";
}
}
//Continue page below.
?>
</select>
<br />
<input type="submit" name="open" value="Open" />
</td><td>
<textarea rows="30" cols="80" style="border: 1px solid #666666;" name="updatedfile"></textarea>
<br />
<!-- <div style="text-align: center;"><input type="submit" name="save" value="Save Changes" /></div> -->
</td></tr>
</tbody>
</table>
</form>
</body>
</html>
<?
}
else
{
//If directory can't be opened complain 
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
<style type=\"text/css\">
h2 {text-align: center}
</style>
<title>Simple File Editor: ERROR!</title>
</head>
<body>
<h2>Simple File Editor: ERROR!</h2>
<p>Could not open directory!! <br /> Permissions Problem??</p>
</body>
</html>";
}
}
///////////////////////////////////////////////////////////////////
//If the open button has been pressed
////////////////////////////////////////////////////////////////////
else if (isset($_POST['open'])){

//If the file can be opened and is writable do....
//This should not be needed because files that aren't writable should
//have never been shown in the selection box.
if (is_writable($_POST["the_file"])) {

//Start page 
//INFO for below: Since variable data is not saved across multiple
//form posts-- we must create a hidden input box with the same value as the
//select box on the previous form. That way the 3rd and final form (ie: the
//saving process) can use the same variable as the first form  (read: write to
//the file you choose in the select box.)      
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style type="text/css">
h2 {text-align: center}
</style>
<title>Simple File Editor: File Opened</title>
</head>
<body>
<h2>Simple File Editor: File Opened</h2>
<form action="<?=$PHP_SELF?>" method="post">

<div style="text-align: center;">
<input type="hidden" name="the_file2" value="<? echo $_POST["the_file"]; ?>" />

<textarea rows="30" cols="80" style="border: 1px solid #666666;" name="updatedfile">
<?

//Open the file chosen in the select box in the previous form into the text
//area
$file2open = fopen($_POST["the_file"], "r");


//Read all the data that is currently in the selected file into the variable
//current_data.
$current_data = @fread($file2open, filesize($_POST["the_file"]));

/*Dirty hack to allow you to edit files that contain "</textarea>" in them.  If
this was not was not here and you tried to edit a file with </textarea> in it
all of your code up to </textarea> would be in this editing forms textarea and
everything after </textarea> would be executed/displayed.  This is very
confusing, but if you look at the code in this file and then think about it a
bit, you will understand what it does.*/

//Do a case insensitive search for </textarea> in the $current_data string.
//replace it with [/textarea].
//This means when you are editing files that contain </textarea> the editing
//box will show [/textarea] instead of the </textarea> tag.  Do not be
//alarmed by this.  Do NOT change or remove this tag, it will be converted back
//to </textarea> in the saving process.  If for some reason this does not work
//for you, or if you know a better way to go about doing this please contact
//me. 

//The following code was contributed by anoldman.com.  Thanks for modernizing 
//and dealing with this issue in a more logical fashion Ken!
//$current_data = eregi_replace("</textarea>", "<END-TA-DO-NOT-EDIT>", $current_data);
$current_data = preg_replace( "!<textarea([^>]+)>(.*?)</textarea>!is", "[textarea\\1]\\2[/textarea]", $current_data );
$current_data = preg_replace( "/&([a-z\d]{2,7}|#\d{2,5});/i", "&amp;$1;", $current_data );
//Echo the data from the file 
echo $current_data;
//Close the file 
fclose($file2open);
//Continue page below.
?>
</textarea>
<br />


	<?
echo "<p>We are working on:  ";
echo "<br />";
//Get previously posted select box data
echo $_POST["the_file"];
echo "</p>";
//Continue page below.
?>
	<input type="submit" name="save" value="Save Changes" /></div>

</form>
</body>
</html>
<?
}
else
{
//If file can't be opened complain 
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
<style type=\"text/css\">
h2 {text-align: center}
</style>
<title>Simple File Editor: ERROR!</title>
</head>
<body>
<h2>Simple File Editor: ERROR!</h2>
<p>Could not open file!! <br /> Permissions Problem??</p>
</body>
</html>";
}
}
///////////////////////////////////////////////////////
//If save button has been pushed....
//////////////////////////////////////////////////////
else if (isset($_POST['save'])){

//If the file can be opened and is writable do....
//This should not be needed because files that aren't writable should
//have never been shown in the selection box. And should not have been opened
//on the previous page.  
if (is_writable($_POST["the_file2"])) {

//Get variable data for the file we are working with from the hidden input box
//in the previous form.  Then open it.
$file2ed = fopen($_POST["the_file2"], "w+");
//Dirty </textarea> hack part 2.  Copy all of the data in the previous forms
//editing textarea to the variable $data_to_save.  
$data_to_save = $_POST["updatedfile"];
//Do the opposite of above.  This time convert the [/textarea] tag you
//see in the editing form back to its proper </textarea> tag so when your files
//are saved the forms on them will still look/work right.  
#$data_to_save = eregi_replace("<END-TA-DO-NOT-EDIT>", "</textarea>", $data_to_save);

//The following code was contributed by anoldman.com.  Thanks for modernizing 
//and dealing with this issue in a more logical fashion Ken!
$data_to_save = preg_replace( "!\[textarea([^\]]+)\](.*?)\[/textarea\]!is", "<textarea\\1>\\2</textarea>", $data_to_save );

//Remove any slashes that may be added do to " ' " s.  Thats a single tick, btw.
//NOTE: If you want to work on files that have slashes in them, comment out the
//line below.
$data_to_save = stripslashes($data_to_save);
//Get the data to write from the previously posted text area, plus all the
//processing we did on it above. Write the changes to the file.
if (fwrite($file2ed,$data_to_save)) {
//If write is successful show success page.  
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
<style type=\"text/css\">
h2 {text-align: center}
</style>
<title>Simple File Editor: File Saved</title>
</head>
<body>
<h2>Simple File Editor: File Saved</h2>
<p>File saved. <br /> Click <a href=\"\">here</a> to go back to the editor.</p>
</body>
</html>";
//Close file
fclose($file2ed);
}
else {
//If write fails show failure page
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
<style type=\"text/css\">
h2 {text-align: center}
</style>
<title>Simple File Editor: ERROR!</title>
</head>
<body>
<h2>Simple File Editor: ERROR!</h2>
<p>File NOT saved!! <br /> Permissions Problem?? <br />  Click <a href=\"\">here</a> to go back to the editor.</p>
</body>
</html>";
//Close file
fclose($file2ed);
}
}
else 
{
//If file can't be opened complain
echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
<head>
<style type=\"text/css\">
h2 {text-align: center}
</style>
<title>Simple File Editor: ERROR!</title>
</head>
<body>
<h2>Simple File Editor: ERROR!</h2>
<p>File NOT saved!! <br /> Permissions Problem??</p>
</body>
</html>";
}
}
?>
