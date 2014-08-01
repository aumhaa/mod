mod
===

monomodular b996+

How to make this work:

0)  You MUST be using the most current version of Live!  (as of this writing, version 9.14).  You should also install the latest version of Max (6.17, although I'm building against the beta of 6.18 at the moment....either should be fine).

1) It’s a good idea to keep a separate copy of Live for the new scripts just so you don’t mess with your b995 installation (if you have one). On OSX, you can do this simply by making a new copy of your Live.app bundle and naming it something different (option + drag and drop).  If that doesn't work for you, just back up your old Monomodular Python scripts and _Mono_Framework folder in MIDI Remote Scripts.

2) Remove old paths from Max>Options>File Preferences for aumhaa_blocks, and make sure there’s not a copy of aumhaa_blocks in Max’s search path. I’m going to rename everything for release, but in the meantime there are duplicates of files used by the newer version that will interfere with things.  Just make sure to move the "aumhaa_blocks" folder out of Max's search path....all the other files should be fine where they are, but please let me know if there are problems.

3) Download the repository, preferably with a github client as I’m making frequent changes and it will be easier to update for you if you find bugs that I can quickly fix. Put the “mod” or “mod-master” folder inside Max’s packages folder, which can either be in ~/Documents/Max/packages or /Applications/Max/packages (either path will work).

4) Copy all the folders from mod/Python Scripts to Live’s MIDI Remote Scripts folder.  There will be an installer for this at release time, but for now you'll have to do it manually.....if you're testing this stuff before release, I'm guess you know where that is.

Any help in testing is really awesome for me, please send me log.txt and Max window shots so I can trace things though, and as much detail as possible about how you broke something ;)

aumhaa@gmail.com



