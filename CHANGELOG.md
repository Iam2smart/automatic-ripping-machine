# Changelog
## Current pre-release v2.4
 - Adding bypass for db.session.commit() error for movies (WIP only MakeMKV and part of handbrake is coded)
 - Abandon job option added to main ARM ui page (for now this only sets job to failed no processes are cancelled)
 - Typo fixes (ARM ui images has some typos these have been updated and corrected)
 - ARM ui now shows CPU temps
 - ARM ui now uses percentage bars to more clearly display storage and RAM usage 
 - ARM ui now correclty deals with setup (it should now create all necessary folders and do so without errors) 
 - Bugfix (ARM ui will not correctly display ram usage)
 - Bugfix (ARM will no longer log failures when opening sdx or hdx devices)

## v2.3.4
 - Travisci/flake8 code fixes
 - github actions added
 - Bugfix(small bugfix for datadiscs)
 - Bugfix (old versions of yaml would cause Exceptions)
 - Bugfix (db connections are now closed properly for CD's)
 - added bypass for music CD's erroring when trying to commit to the db at the same time

## v2.3.3

 - A smaller more manageable update this time 
 - Early changes for cleaner looking log output
  - Security (HandBrake.py outputs the new prettytable format)
  - Bugfix (Transcode limit is now respected) 
  - Bugfix (Bluray disc with no titles will now be handled correctly and will not throw an exception )
  - Bugfix (abcde.config now correctly uses musicbrainz)

## v2.3.2
 - Added prettytables for logging
 - Remove api/keys from the Config class string printout 
  - Security (HandBrake.py was still outputting all api key and secrets to log file. This has now been fixed)
  - Bugfix (Transcode limit is now respected) 
  - Bugfix (Bluray disc with no titles will now be handled correctly and will not throw an exception ) 

## v2.2.0
 - Added Apprise notifications
  - Added more to the Basic web framework (flask_login)
    - Added login/admin account
    - Added dynamic websever ip to notifications
    - Allow Deleting entries from the db (also warning for both the page and every delete)
    - Added music CD covers (provied by musicbrainz & coverartarchive.org)
    - Added CPU/RAM info on index page
    - Added some clearer display for the listlogs page 
    - Bugfix (Mainfeature now works when updating in the ui) 
    - Bugfix (Job is no longer added twice when updated in ui) 
    - ALPHA: Added ARM settings page (This only shows settings for the moment, no editing)
  - Added Intel QuickSync Video support
  - Added AMD VCE support
  - Added desktop notifications
  - Added user table to the sqlite db
  - Added Debian Installer Script
  - Added Ubuntu Installer Script
  - Added Auto Identfy of music CD's
  - Made changes to the setup logging to allow music CD's to use the their artist name and album name as the log file 
  - Added abcde config file overide (This lets you give a custom config file to abcde from anywhere)
  - Added log cleaner function to strip out secret keys (This isnt complete yet)
  - Bugfix (datadiscs with no label no longer fail) 
  - Bugfix (NONE_(timestamp).log will no longer be generated ) 

## v2.1.0
 - Added new package (armui) for web user interface
  - Basic web framework (Flask, Bootstrap)
    - Retitle functionality
    - View or download logs of active and past rips
  - sqlite db

## v2.0.1
 - Fixed crash inserting bluray when bdmt_eng.xml file is not present
 - Fixed error when deleting non-existent raw files
 - Fixed file extension config parameter not being honored when RIPMETHOD='mkv'
 - Fixed media not being moved when skip_transcode=True
 - Added logic for when skip_trancode=True to make it consistant with standard processing
 - Removed systemd and reimplemented arm_wrapper.sh (see Readme for upgrade instructions)

## v2.0.0
 - Rewritten completely in Python
 - Run as non-root
 - Seperate HandBrake arguments and profiles for DVD's and Bluray's
 - Set video type or automatically identify
 - Better logging
-  Auto download latest keys_hashed.txt and KEYDB.cfg

## v1.3.0
 - Get Title for DVD and Blu-Rays so that media servesr can identify them easily.
 - Determine if video is Movie or TV-Show from OMDB API query so that different actions can be taken (TV shows usually require manual episode identification)
 - Option for MakeMKV to rip using backup method.
 - Option to rip only main feature if so desired.

## v1.2.0
- Distinguish UDF data from UDF video discs

## v1.1.1

- Added devname to abcde command
- Added logging stats (timers). "grep STAT" to see parse them out.

## v1.1.0

- Added ability to rip from multiple drives at the same time
- Added a config file for parameters
- Changed logging
  - Log name is based on ID_FS_LABEL (dvd name) variable set by udev in order to isolate logging from multiple process running simultaneously
  - Log file name and path set in config file
  - Log file cleanup based on parameter set in config file
- Added phone notification options for Pushbullet and IFTTT
- Remove MakeMKV destination directory after HandBrake finishes transcoding
- Misc stuff

## v1.0.1

- Fix ripping "Audio CDs" in ISO9660 format like LOTR.

## v1.0.0

- Initial Release
