# Contributing
## Translation
If you want to help translate RBEditor, or add a custom language to RBEditor:

`lang.py` has a single `lang` variable, which is a dictionary that contains all localized strings in RBEditor. To add a custom language, follow these steps:
1. Make sure you are using the source code version of RBEditor. Open the `lang.py` script in a text editor.
2. Just before the end of the `lang` dictionary, create a new key. The key name will be a IETF BCP 47 language tag (2 or 3 letters, must be all lowercase) for the language to want to add (**IMPORTANT!**) that must be one of the locales in `self.locales` (in the `__init__` function of the `GUI` class in `gui.py`).
3. The value of the key will be a dictionary. Inside it, you can add key-value pairs corresponding to strings in RBEditor.<br>The key is a string name, and the value is the content of the string. The string name has to correspond to a string name in the `en` dictionary key. If a string is not included, the string from the `en` key will be used instead.
4. In `gui.py`, in the `__init__` function of the `GUI` class, add a new key-value pair to `self.languages` and `self.language_fallback_locales`. The key name will be the same as the one you set in Step 1.<br>The value for `self.languages` is the language name, which will be displayed in Settings \> Language.<br>The value for `self.language_fallback_locales` is, well, a fallback locale from `self.locales` to use, in case the 2-letter and 3-letter locales aren't supported (this is the case with older versions of Windows). The fallback locale must be in the format `xx-XX` or `xxx-XX`.
5. You're done! Now just set the language in Settings \> Language and restart the program. Make any changes to the key you made in `lang.py` as needed.

To add an official translation to RBEditor, fork this repository, do the steps above, commit, and send a pull request.

## Bug hunting
While using RBEditor, make sure to look out for exceptions. Usually, an exception will be caught by the program, which will show a messagebox containing the traceback. When you see this, do these steps:

**Step 1: Check if you're using an old version of RBEditor**  
If you haven't already, first go to Settings \> Updates, and enable pre-release versions if you haven't already.  
Now, click on Help \> Check for updates. This will bring up the updater window. **Do not close RBEditor when checking for updates!**  
If a new update is found, click on Visit download page and download the new version.

**Step 2: Check if the error still occurs**  
Make sure you are on the latest pre-release version of RBEditor. Check if the error you encountered still occurs. If it still occurs, that means it hasn't been fixed. [Create an issue](https://github.com/gamingwithevets/rbeditor/issues) immediately so I can fix it!
