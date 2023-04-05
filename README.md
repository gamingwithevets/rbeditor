**RBEditor** is a tool that can edit the Recycle Bin's contents and also open and edit files and folders inside the Recycle Bin.

NOTE: RBEditor is currently in beta; that means **bugs and glitches** may happen when you use the program.

**Supports Windows Vista - Windows 11**

![RBEditor Beta 1.3.0_01 GIF](https://drive.google.com/uc?export=view&id=1wgVq6eaBvKwZdjHlJ5HQAro90PKrwiAW)  
*(If the GIF doesn't show, click [here](https://drive.google.com/uc?export=view&id=1wgVq6eaBvKwZdjHlJ5HQAro90PKrwiAW) to see it)*

[Download for Windows Vista, 7, 8, 8.1, 10, 11](../../releases/latest)  
<details>
<summary><b>View compatibility list</b></summary><br>
<table style="width:100%">
  <tr>
    <th>RBEditor binary version</th>
    <th>Windows version required</th>
  </tr>
  <tr>
    <td>0.1.0+</td>
    <td>At least Windows Vista</td>
  </tr>
  <tr>
    <td>Beta 1.2.1_01 - Beta 1.4.0</td>
    <td>At least Windows 7</td>
  </tr>
  <tr>
    <td>Beta 1.1.0 - Beta 1.2.1</td>
    <td>At least Windows 10</td>
  </tr>
</table>
</details>

# Features
- Create files and folders in the Recycle Bin (without any deletion)
- Open and edit files and folders in the Recycle Bin
- Normal Recycle Bin actions (delete, restore)
- Edit Recycle Bin file metadata
- Multilanguage support

# Languages
RBEditor currently has these available languages:

| Language | Version Added |
|--|--|
| English (US) | Beta 1.0.0 |
| Japanese | Beta 1.3.0 |
| Vietnamese | Beta 1.0.0 |

# Running and building from source code
If you're just wanting to run RBEditor, download the appropriate EXE file in [the Releases page]((../../releases/latest)).

## Requirements
These are the minimum requirements to run and build RBEditor from source code:
- At least [Python 3.6.0](https://www.python.org/downloads/release/python-360/)
- [The WMI module](https://pypi.org/project/WMI/)
- [The PyInstaller module](https://pypi.org/project/pyinstaller/) (note: not required if you don't need to build)
- At least Windows Vista (note: RBEditor **cannot** be run on Unix-based systems)

However, to get the best experience possible, here are the recommended requirements:
- At least [Python 3.7.6](https://www.python.org/downloads/release/python-376/)
- [The WMI module](https://pypi.org/project/WMI/)
- [The Requests library](https://pypi.org/project/requests/) (required to check for updates)
- [The PyInstaller module](https://pypi.org/project/pyinstaller/) (note: not required if you don't need to build)
- At least Windows Vista (note: RBEditor **cannot** be run on Unix-based systems)

If you are willing to build a binary for use by the public, I used a **Windows Vista x64 virtual machine** equipped with **Python 3.7.6 x64 and x86**, both with **WMI, Requests and PyInstaller**.
- The need for Windows Vista is because binaries built on a Windows version will only work on that version and beyond. So Windows Vista binaries can run on Vista and higher, but Windows 10 and 11 binaries can only run on 10 and 11 and not older versions.
- The two architectures are to obviously compile both x64 and x86 binaries.

## Building
**Step 0:** Download the repository  
Pick your favorite method! You can pick either `git clone`, downloading a ZIP file or other means.

**Step 1:** Install the modules  
Open a command prompt at the root of the repo directory and run `python -m pip install -r requirements.txt`. This will only install necessary packages for *running* RBEditor, so make sure to also run `python -m pip install pyinstaller` as well!

**Step 2:** Test it  
Run `python main.py`. Now check that everything works.

**Step 2:** Build it  
After checking everything, run `python -m PyInstaller rbeditor.spec` (f you get `no module named PyInstaller`, that means you didn't install PyInstaller yet). Wait about 20 seconds for it to compile, and you are done!
