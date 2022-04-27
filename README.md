# Project M Raw Manager

Written by Samoe (John Sam Fuchs)

http://samoe.me/

WHAT DOES IT DO?

PM RAW Manager helps you manage multiple versions of Project M or Project + within one version of Dolphin.

Dolphin loads a file called “sd.raw” from the Dolphin/User/Wii folder. That sd.raw file contains all the data for the version of Project M you are attempting to play. It can be cumbersome to constantly swap which file you have in the User/Wii folder if you like to play different versions of the game. This program allows you to have multiple “.raw” files inside of the User/Wii folder, then select which version you want to play.

------------------------
SETUP

The first time you launch the program, it will ask you to set up a new version of Dolphin.

First, choose a name for this version. By default, it names it "Dolphin", but if you set up multiple
versions, you must choose a UNIQUE name for each. (Currently the program does not stop you from naming
them all the same thing, this will be fixed in the future.)

Now browse to the "Dolphin.exe" file for the version of the emulator you want to use.

The program assumes all of your ".raw" files are in your Dolphin folder, specifically in
{your-dolphin-install} / User / Wii
and automatically points to that folder. It detects all ".raw" files inside of the folder and lists
them below for you.

    NOTE: Please name all your .raw files with unique names, as that is what will show in the list.
    If you still have a file called "sd.raw" in the folder when you first launch Dolphin, it will
    be renamed to "OLDsd.raw". The first-time setup ignores "sd.raw" and "OLDsd.raw" files, so it
    will only show you .raw files with unique names.

You can also choose a custom icon image for this version of Dolphin. By default it'll use the Dolphin logo.

If everything looks okay, click "Submit" and the launcher will open. When you open the launcher in the
future, it will not ask you to setup again.

------------------------
HOW DOES IT WORK?

After the first time you use the program, it will remember which file is currently named "sd.raw",
then when you switch versions, it will rename that file back to its original name. For example, here
is a folder structure that has multiple .raw files :

 -- /User/Wii

 ---- /import/
 
 ---- /meta/
 
 ---- /shared1/
 
 ---- /shared2/
 
 ---- /sys/
 
 ---- /ticket/
 
 ---- /title/
 
 ---- /tmp/
 
 ---- /wfs/
 
 ---- pplus2.9.raw
 
 ---- pplusFingyBuild5.01.raw

If you use the launcher to run Dolphin with "pplus2.9", then the file will be renamed to "sd.raw"

    NOTE: A text file is created in your ".raw" file directory called "currentSDRaw.txt" that tells
    you the original filename of the current "sd.raw" file. If something goes wrong or you forget which
    version is currently loaded, you can use this text file to manually rename the "sd.raw" file back
    to its original unique name.

Next time you use the launcher, if you select "pplusFingyBuild5.01", then "sd.raw" will be renamed
back to "pplus2.9.raw" and the new correct file ("pplusFingyBuild5.01.raw") will be renamed to "sd.raw"

If used correctly, you should never "lose" any files. HOWEVER, if you manually change the "sd.raw"
file outside of the launcher, it will not correctly track which version is loaded and may screw up
the file names. For this reason, I HIGHLY RECOMMEND keeping a backup of all the ".raw" files you
may want to use. If it does get messed up, delete the "config.json" file inside of the launcher
folder and open the program, running through the first time setup again.

------------------------
KNOWN ISSUES / ODDITIES

- If you have two different versions of Dolphin that both have a .raw file that share the same name,
only one of those Dolphins will show that .raw file in their list.

- If you add a version of Dolphin that's already in the list but name it something else, they should
both work fine. I recommend against this, however, as I'm not sure what kinds of things could go
wrong.
