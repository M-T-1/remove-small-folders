![GitHub top language](https://img.shields.io/github/languages/top/M-T-1/remove-small-folders)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/M-T-1/remove-small-folders)
# **remove-small-folders**
Remove folders with less than 2 items (files or folders) in them.     
Note: this number can be changed, see [Global Variables](#global-variables)

Disclaimer:
This is the first time I've used github and this is the closest I've ever come to a decent python script.


## How this script came to be:

I got bored of having a few dozen folders with a single file in it.
I was on a python kick and decided to automate the process of moving the contents up and deleting the folders.
Said folders were all over the directory tree of an external hard drive so I needed a way to find and handle them quickly.

## How to use this script:
Requirements: Python 3                     
Move the script anywhere and it **should** work as intended.
 
 ## ****What this script does: (TLDR version)****
If you put the script in a folder and run it:
The script will find any folders with less than 2 items (files or folders) and:
delete the folder, **after** moving the contents of the folder  to the parent folder and prefixing any files with the name of the folder.
e.g. \files\pics\apples.png to \files\pics-apples.png or \files\pics\orchard\ to \files\pics-orchard\
  
## Global Variables:
Lines 14 and 15 hold the settings dictionary.
You can edit the values quite easily, just beware of setting the threshold too high.

- The prompt_override key.
	Set the value to true and it will run without any user input.
	This is useful for if you want to pipe the output to a text file.
- The folders_get_prefixed key.
	Set the value to false and any folders that get moved won't be prefixed with the name of the parent folder that got deleted.
- The files_get_prefixed key.
	Set the value to false and any filesthat get moved won't be prefixed with the name of the parent folder that got deleted.
- The root_path key.
	Leave this blank to make the script run in the folder it is located in.
	Set it to a valid path and the script will run in that location instead of it's own location.
- The threshold key.
	This dictates the maximum number of items in a folder before the script decided that the folder needs deleting.
	e.g. if you set the threshold to 99, then the only folders left will be ones with 100 or more files and folders in them (note: the script doesn't count files inside folders inside the folder it is checking.





## ****What this script does: (in detail)****
I hope I put enough readable comments in the script that someone could read it and understand how ti works, but just in case:

It makes a list of every folder in the root directory (where the script is).
It then takes that list and transfers each item to a new list if it meets the following criteria:
 - does the folder contain less (or the same number of) items than the threshold value 

It then goes through each item in the list of folders that meet the criteria and moves the contents to a safe place (the folder that houses the folder it's selected from the list).
It then deletes the folder it selected from the list.

The script then finishes off by printing out all the data it's collected about it's run:
files and folders indexed, starting path, folders deleted,etc.



If anyone wants to improve these explanations, I'll merge just about any edits to this page.
