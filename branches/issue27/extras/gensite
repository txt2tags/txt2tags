#!/usr/bin/env python
# http://www.davefancella.com/software/gensite.html

# This script generates a site with txt2tags
# Basically it copies all files over except those with txt2tags extension, those are
# run through txt2tags.

import os, sys
from optparse import OptionParser
from ConfigParser import ConfigParser

knownTools = {}
gensiteBase = None
defaultExtension = ".html"

def main():
    parser = OptionParser()
    
    parser.add_option("-i", "--input", default="./", help="input directory to generate from", dest="inputdir")
    parser.add_option("-o", "--output", default="./", help="directory to put all output in.  gensite will not create it if it doesn't exist, you must create it before running gensite", dest="outputdir")
    parser.add_option("-g", "--generate-config", action="store_true", default=False, dest="genConf", help="Generate a default config file.")
    (options, args) = parser.parse_args()

    if options.genConf is True:
        print "Generating default config file...",
        GenerateDefaultConfig()
        print "done!"
        sys.exit(0)

    config = None
    buildstatus = False
    
    if os.path.exists(options.inputdir):
        if os.path.exists(options.outputdir):
            if os.path.exists(os.path.join(options.inputdir, 'gensiterc') ):
                config = ConfigParser()
                config.read(os.path.join(options.inputdir, 'gensiterc') )
                Configure(config)
                
            targetDir = os.path.abspath(options.outputdir)
            os.chdir(options.inputdir)
            
            buildstatus, generatedFiles = gensite(targetDir, config)
            
            pruneDestination(targetDir, generatedFiles, config)
        else:
            print "Destination directory doesn't exist!"
            buildstatus = False
    else:
        print "Input directory doesn't exist!"
        buildstatus = False
        
    if buildstatus is True:
        sys.exit(0)
    else:
        sys.exit(10)
            
def copyFile(source, dest):
    theCommand = "cp -f " + source + " " + dest
    
    res1 = os.system(theCommand)
    res2 = os.system("chmod 664 " + dest)
    
    if res1 != 0 or res2 != 0:
        return False
        
    return True
            
def generate(theCommand, dest):
    print theCommand
    res1 = os.system(theCommand)
    res2 = os.system("chmod 664 " + dest)
    
    if res1 != 0 or res2 != 0:
        return False
    return True

def pruneDestination(targetdir, allowedFiles, config):
    os.chdir(targetdir)
    
    for (dirpath, dirnames, filenames) in os.walk('./', False):
        if dirpath.startswith('./'):
            dirpath = dirpath[2:]
            
        for aFile in filenames:
            testFile = os.path.join(dirpath, aFile)
            if testFile.startswith('./'):
                testFile = testFile[2:]
            
            if testFile in allowedFiles:
                pass
            else:
                # Delete the file
                print "Deleting '" + testFile + "', as it is not in the source directory and is not a generated file"
                os.remove(testFile)
        
        if dirpath == '':
            dirpath = "./"
        if len(os.listdir(dirpath)) == 0:
            print "Deleting '" + dirpath + "', as the directory is now empty."
            os.rmdir(dirpath)

# Returns a list of files that exist in svn, relative to the root of the checkout
def gensite(targetdir, config=None):
    global knownTools, defaultExtension
    
    allGeneratedFiles = []
    
    buildstatus = True
    
    globalIgnoreDirs = ['.svn', 'CVS', 'templates']
    globalIgnoreFiles = ['gensiterc']
    
    if config is not None:
        if config.has_section('main'):
            if config.has_option('main', 'ignoredirs'):
                globalIgnoreDirs += config.get('main', 'ignoredirs').split()
        if config.has_section('main'):
            if config.has_option('main', 'ignorefiles'):
                globalIgnoreFiles += config.get('main', 'ignorefiles').split()
    
    for (dirpath, dirnames, filenames) in os.walk('.'):
        if dirpath.startswith("./"):
            dirpath = dirpath[2:]
        # find and remove any files that are to be ignored
        for a in dirnames:
            if a.startswith("./"):
                a = a[2:]
            if a in globalIgnoreDirs:
                print "Directory " + a + " on ignore list, not entering."
                del dirnames[dirnames.index(a)]
        for a in filenames:
            if a.startswith("./"):
                a = a[2:]
            if a in globalIgnoreFiles:
                print "File " + a + " on ignore list, ignoring."
                del filenames[filenames.index(a)]
        
        # Create any directories that don't exist
        for a in dirnames:
            if a.startswith("./"):
                a = a[2:]
            if os.path.exists(os.path.join(targetdir, dirpath, a) ) is False:
                os.mkdir(os.path.join(targetdir, dirpath, a) )
                os.system('chmod 775 ' + os.path.join(targetdir, dirpath, a) )
                print "Making directory " + a
        
        # Iterate through filenames and do something with them, either copy or generate
        for aFile in filenames:
            if aFile.startswith("./"):
                aFile = aFile[2:]
            root, ext = os.path.splitext(aFile)
            ext = ext.lower()[1:]
            sourcefile = os.path.join(dirpath, aFile)
            destfile = ''
            generator = 'cp'

            if ext in knownTools.keys():
                theCommandLine = knownTools[ext]
                # Do the simple substitutions first
                theCommand = theCommandLine.replace("$SAME", gensiteBase)
                theCommand = theCommand.replace("$SOURCE", sourcefile)

                # Dig out the $DEST variable and determine if we need to provide
                # an extension, or if an extension is already provided.
                theNewExt = ".html"
                while theCommand.find("$DEST") > -1:
                    theLoc = theCommand.find("$DEST")
                    if len(theCommand[theLoc:]) > 5:
                        if theCommand[theLoc+5] == ".":
                            theNewExt = ""
                        else:
                            theNewExt = defaultExtension
                    else:
                        theNewExt = defaultExtension
                    destfile = os.path.join(targetdir, dirpath, root + theNewExt)
                    theCommand = theCommand.replace("$DEST", destfile, 1)
                    
                    genFile = os.path.join(dirpath, root + theNewExt)
                    if genFile.startswith('./'):
                        genFile = genFile[2:]
                    allGeneratedFiles.append(genFile )
            else:
                destfile = os.path.join(targetdir, dirpath, aFile)
                genFile = os.path.join(dirpath, aFile) 
                theCommand = "cp -f " + sourcefile + " " + destfile
                if genFile.startswith('./'):
                    genFile = genFile[2:]
                allGeneratedFiles.append(genFile)
            
            generateFile = False
            
            # If the file exists, check it's modified times.  If it doesn't exist, generate it
            if os.path.exists(destfile):
                if os.path.getmtime(sourcefile) > os.path.getmtime(destfile):
                    generateFile = True
                elif ext == 't2t':
                    generateFile = CheckTimestampsT2t(os.path.normpath(sourcefile), destfile)
            else:
                generateFile = True
                
            # generate the file now
            if generateFile is True:
                if generate(theCommand, destfile) is True:
                    pass
                else:
                    buildstatus = False
                    print "Error: generation of '" + sourcefile + "' to '" + destfile + "' failed."

                    
    return (buildstatus, allGeneratedFiles)


# This function opens sourcefile and checks every included file to see if the target file
# needs to be updated
def CheckTimestampsT2t(sourcefile, destfile, currentPath = None):
    sourcedir, sourcefile = os.path.split(sourcefile)
    
    if currentPath is None:
        currentPath = ""
    if os.path.getmtime(os.path.join(sourcedir, sourcefile) ) > os.path.getmtime(destfile):
        return True
    else:
        # if it's a txt2tags file, we need to scan for includes, in which case we just go ahead
        # and regenerate it because there's no sane way to handle it otherwise right now
        theFile = open(os.path.join(sourcedir, sourcefile), 'r')
        
        # Todo: turn this into a recursive function so it checks all included files, even files
        #   included by included files.
        for line in theFile:
            if line.lower().startswith('%!include:') or line.lower().startswith('%!includeconf:'):
                theInclude, theFileName = line.split()
                theDir, basename = os.path.split(theFileName)
                
                theFileName = os.path.join(sourcedir, theFileName.strip() )

                generateFile = CheckTimestampsT2t(theFileName, destfile)
                # Go ahead and return if we've got a match that says we need to generate
                if generateFile is True:
                    theFile.close()
                    return True
        
        return False
                
def Configure(confObj):
    global knownTools, defaultExtension
    print "Configuring gensite"
    if confObj.has_section('tools'):
        for opt in confObj.options('tools'):
            knownTools[opt] = confObj.get('tools',opt)
    if confObj.has_option('main', 'defaultextension'):
        theExt = confObj.get('main', 'defaultextension')
        if theExt.startswith("."):
            defaultExtension = theExt
        else:
            defaultExtension = "." + theExt
        
def GenerateDefaultConfig():
    theFileContents = '''[main]

# This is a list of directories to ignore.  They will not be processed, and if they're
# already in the destination location, they will not be pruned.
ignoredirs = templates

# This is the default extension to use for files that are not copied, but generated, if
# the commandline doesn't provide an extension.  This is a convenience only.
defaultextension = html

[baselayout]
# This section provides rules for the basic layout of a page.  Subdirectories can override this
# It should be the key "layout" followed by a comma-separated list of files that should
# be concatenated together, where $CONTENT is the page that contains the content of the
# file.  This isn't implemented yet
layout = header.t2t, $CONTENT, footer.t2t

# basedir is the directory where all of these files can be found.  It will be prepended
# to each filename, so it can be left blank if you don't have such a thing.  It will
# not be prepended to variables.
basedir = templates

[tools]
# This section contains tools referenced by lower-case extension that are used to generate
# the files for the site.  If a tool isn't found here, the file is just copied.  A tool
# here should provide a command line for the tool.
#
# $SAME means the tool is in the same path as the gensite script.
# $PATH means the system-wide $PATH variable should be used to find the tool - not implemented yet
# $SOURCE refers to the source file with extension
# $DEST refers to the destination file without extension.  You should append the
#       extension, i.e. $DEST.html.  If this is not followed by a . , then the global
#       setting will be used (which defaults to html).
#
# Gensite has some builtin support for some files, most notably txt2tags and will do extra
# work of its own to determine if the file needs to be generated.
t2t = $SAME/txt2tags --target xhtml --css-sugar -i $SOURCE -o $DEST

'''
    theFile = open("gensiterc", "w")
    theFile.write(theFileContents)
    theFile.close()
    
if __name__ == "__main__":
    fullbase = os.path.realpath(sys.path.pop(0) )
    gensiteBase = fullbase
    
    main()

