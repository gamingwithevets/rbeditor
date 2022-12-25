import sys
import os
if os.name != 'nt':
	print('This program is only available for Windows systems. Sorry!')
	sys.exit()

python_requirement = '3.7.0'

import platform
if platform.python_version() < python_requirement:
	if platform.python_version() < '3.10.0':
		print('Oops! Your Python version is too old.\n')
		print(f'Requirement: Python {python_requirement}+\nYou have   : Python {platform.python_version()}')
		print('\nGet a newer version!')
		sys.exit()

try: import tkinter as tk
except ImportError:
	print('''Oooh no you don't have Tkinter.
Don't worry! It's super easy. Just search "install tkinter" on Google and you\'ll find it!

Now scram!''')
	sys.exit()
	
import os
import traceback

try: temp_path = sys._MEIPASS
except AttributeError: temp_path = os.getcwd()

import tkinter.messagebox
try: from gui import GUI, repo_name, report_error
except ImportError:
	err_text = f'Whoops! The script "gui.py" is required.\nCan you make sure the script is in "{temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues'
	print(err_text)
	tk.messagebox.showerror('Hmmm?', err_text)
	sys.exit()

try: g = GUI(tk.Tk())
except Exception: report_error()