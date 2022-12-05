import os
import sys
import traceback
import tkinter as tk
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog

# main modules
try: import wmi
except ImportError: print('I need the WMI module, please install it w/ "pip install wmi".'); sys.exit()
import re
import math
import locale
import shutil
import string
import getpass
import binascii
import tempfile
import collections
import configparser
try: from lang import lang
except ImportError: tk.messagebox.showerror('Hmmm?', f'Whoops! The script "lang.py" is required.\nCan you make sure the script is in "{os.getcwd()}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues'); sys.exit()
from ctypes import windll
from datetime import datetime, timedelta, timezone

import winreg
from winreg import HKEY_CLASSES_ROOT as HKCR


name = 'RBEditor'
repo_name = 'rbeditor'
version = 'Beta 1.0.0'
about_msg = f'''\
{name} - {version}
Project page: https://github.com/gamingwithevets/{repo_name}

NOTE: This version is not final! Therefore it may have bugs and/or glitches.

Licensed under the MIT license

Copyright (c) 2022 GamingWithEvets Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the "Software"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all \
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.\
'''

def report_error(self = None, exc = None, val = None, tb = None):
	try: GUI.window.quit()
	except Exception: pass

	e = traceback.format_exc()

	print(f'Whoops! An error has occurred.\n\n{e}\nIf this error persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues')
	tk.messagebox.showerror('Whoops!', f'An error has occurred.\n\n{e}\nIf this error persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues')
	sys.exit()

tk.Tk.report_callback_exception = report_error

class RBHandler:
	def __init__(self, gui): self.gui = gui

	def get_rbdir(self):
		username = getpass.getuser()
		wmic = wmi.WMI()
		for user in wmic.Win32_UserAccount():
			if user.Name == username:
				sid = user.SID
				break

		self.rbdir = f':\\$RECYCLE.BIN\\{sid}'
		self.rbdir_c = f'C:\\$Recycle.Bin\\{sid}'

	def get_bin_items(self):
		drives = self.get_drives()
		self.corrupted_rbdir_drives = []
		bin_items_list = []
		dirlist = []
		errno_whitelist = [13, 2]
		for drive in drives:
			try: dirlist.extend(os.listdir(f'{drive}{self.rbdir}'))
			except IOError as e:
				if e.errno not in errno_whitelist: self.corrupted_rbdir_drives.append(drive)
		for f in dirlist:
			if f[:2] == '$I': bin_items_list.append(f[2:])

		self.bin_items = {}
		bin_items_unsorted = {}
		for item in bin_items_list:
			filedata = self.read_metadata(item)
			if filedata == None: continue
			if os.path.exists(filedata['fname']): continue
			if self.get_rb_path(item, 'R') == None: continue

			try: dirtest = os.path.isdir(self.get_rb_path(item, 'R'))
			except: dirtest = False

			ext = os.path.splitext(filedata['fname'])[1].lower()

			bin_items_unsorted[item] = {
			'ogname': os.path.basename(filedata['fname']),
			'type': self.gui.lang['ftype_desc_folder'] if dirtest else self.get_ftype_desc(ext),
			'ext': None if dirtest else ext,
			'oglocation': os.path.dirname(filedata['fname']),
			'size': filedata['fsize'],
			'deldate': filedata['deldate'].strftime(self.date_format),
			'rbin_drive': self.get_rb_path(item)[0]
			}

			self.bin_items = collections.OrderedDict(sorted(bin_items_unsorted.items(), key = lambda x: x[1]['ogname'].lower()))

	def get_ftype_desc(self, ext):
		if not ext: return 'File'
		# in case UWP Windows Notepad is installed, the extension descriptions for
		# .txt, .ini and .ps1 are embedded into the program itself.
		elif ext == '.txt': return self.gui.lang['ftype_desc_txt']
		elif ext == '.ini': return 'Configuration settings'
		elif ext == '.ini': return self.gui.lang['ftype_desc_ps1']
		else:
			try:
				desc = winreg.QueryValue(HKCR, winreg.QueryValue(HKCR, ext))
				if desc: return desc
				else: return f'{ext.upper()} File'
			except Exception: return f'{ext.upper()} File'

	def get_drives(self):
		drives = []
		bitmask = windll.kernel32.GetLogicalDrives()
		for letter in string.ascii_uppercase:
			if bitmask & 1: drives.append(letter)
			bitmask >>= 1

		return drives

	def filetime_to_dt(self, ft):
		time_utc = datetime(1970, 1, 1) + timedelta(microseconds = (ft - 116444736000000000) // 10)
		time_utc = time_utc.replace(tzinfo = timezone.utc)
		return time_utc.astimezone()

	def convert_size(self, size_bytes):
		def add_digits(i, s, p):
			if i != 0:
				digits = 0
				while(s > 0):
					digits += 1
					s //= 10
				if digits == 1:
					s = round(size_bytes / p, 2)
					if str(s).endswith('.0') or str(s).endswith('.1') or str(s).endswith('.2') or str(s).endswith('.3') or str(s).endswith('.4') or str(s).endswith('.5') or str(s).endswith('.6') or str(s).endswith('.7') or str(s).endswith('.8') or str(s).endswith('.9'): return s
				elif digits == 2: s = round(size_bytes / p, 1)
				elif digits == 3: s = round(size_bytes / p)

			return s

		if size_bytes == 0: return f'0 {self.gui.lang["bytes"]}'

		size_names_pow2 = ('KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')
		i_pow2 = int(math.floor(math.log(size_bytes, 1024)))
		p_pow2 = math.pow(1024, i_pow2)
		s_pow2 = round(size_bytes / p_pow2)

		size_names_pow10 = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
		i_pow10 = int(math.floor(math.log(size_bytes, 1000)))
		p_pow10 = math.pow(1000, i_pow10)
		s_pow10 = round(size_bytes / p_pow10)

		s_pow2 = add_digits(i_pow2, s_pow2, p_pow2)
		s_pow10 = add_digits(i_pow10, s_pow10, p_pow10)

		if i_pow10 == 0: return f'{size_bytes} {self.gui.lang["bytes"]}'
		else:	
			if i_pow2 == 0: return f'{s_pow2} {size_names_pow2[i]} ({size_bytes} {self.gui.lang["bytes"]})'
			else: return f'{s_pow2} {size_names_pow2[i_pow2 - 1]} ({s_pow10} {size_names_pow10[i_pow10 - 1]} - {size_bytes} {self.gui.lang["bytes"]})'

	def read_metadata(self, file_to_read):
		file_path = self.get_rb_path(file_to_read)

		file = open(file_path, 'rb')
		if file.read(8) != b'\x02\x00\x00\x00\x00\x00\x00\x00': return

		fsize_b = bytearray(file.read(8))
		fsize = int.from_bytes(fsize_b, 'little')
		deldate_b = bytearray(file.read(8))
		deldate = self.filetime_to_dt(int.from_bytes(deldate_b, 'little'))
		fnamelen_b = bytearray(file.read(4))
		fnamelen = int.from_bytes(fnamelen_b, 'little')
		fname = ''
		for i in range(fnamelen):
			char_b = bytearray(file.read(2))
			if char_b == b'\x00\x00' and i == fnamelen - 1: break
			char_b.reverse()
			char_h = char_b.hex()
			exec(f'global char; char = u"\\u{char_h}"')
			fname += char

		return {'fname': fname, 'fsize': fsize, 'deldate': deldate}

	def get_rb_path(self, file, typ = 'I'):
		drives = self.get_drives()

		fname = f'${typ}{file}'
		for drive in drives:
			if drive == os.getenv('systemdrive')[0]: ind_drive_rbdir = self.rbdir_c
			else: ind_drive_rbdir = f'{drive}{self.rbdir}'
			try:
				f = os.listdir(ind_drive_rbdir)
				if fname in f: return f'{ind_drive_rbdir}\\{fname}'
			except: pass

	def get_rb_path_friendly(file, typ = 'I'):
		file_path = os.path.dirname(self.get_rb_path(file, typ))
		return f'Recycle Bin in {file_path[:2]} | {file_path}'

class GUI(RBHandler):
	def __init__(self, window):
		self.version = version
		self.window = window

		self.display_w = 800
		self.display_h = 500

		tk_font = tk.font.nametofont('TkDefaultFont').actual()
		self.font_name = tk_font['family']
		self.font_size = tk_font['size']

		self.default_date_format = '%d/%m/%Y %H:%M:%S'
		self.languages = lang.keys()
		self.language = tk.StringVar()

		self.appdata_folder = f'{os.getenv("LOCALAPPDATA")}\\RBEditor'
		self.ini = configparser.ConfigParser()
		self.parse_settings()

		super().__init__(self)

		self.get_rbdir()
		self.init_window()
		self.init_protocols()

		self.main()	

	def parse_settings(self):
		try:
			self.ini.read(f'{self.appdata_folder}\\settings.ini')
			self.language.set(self.ini['settings']['language'])
			self.date_format = self.ini['settings']['date_format'].replace('%%', '%')

		except Exception:
			self.language.set(self.get_lang())
		
		self.set_lang()
		self.date_format = self.default_date_format

	def save_settings(self):
		self.ini['settings'] = {'language': self.language.get(), 'date_format': self.date_format.replace('%', '%%')}
		if not os.path.exists(self.appdata_folder): os.makedirs(self.appdata_folder)
		with open(f'{self.appdata_folder}\\settings.ini', 'w') as f: self.ini.write(f)

	def get_lang(self):
		lang = locale.windows_locale[windll.kernel32.GetUserDefaultUILanguage()]
		return lang if lang in self.languages else 'en_US'

	def set_lang(self):
		self.lang = lang['en_US'].copy()
		lang_new = lang[self.language.get()].copy()
		for key in lang_new: self.lang[key] = lang_new[key]
		
	def change_lang(self):
		self.set_lang()
		self.save_settings()
		tk.messagebox.showwarning(self.lang['msgbox_warning'], self.lang['msgbox_setting_change'])
		self.refresh(True)

	def n_a(self): tk.messagebox.showinfo(self.lang['msgbox_n_a'], f'{self.lang["msgbox_n_a_desc"]}{name}. {self.lang["msgbox_n_a_desc2"]}!')

	def refresh(self, load_func = False, custom_func = None):
		for w in self.window.winfo_children(): w.destroy()
		self.menubar()
		self.set_title()

		if load_func:
			if custom_func == None: self.main()
			else: custom_func() 

	def set_title(self): self.window.title(f'{name} {version}')

	def init_window(self):
		self.window.geometry(f'{self.display_w}x{self.display_h}')
		self.window.resizable(False, False)
		self.menubar()
		self.set_title()
		self.window.iconbitmap('icon.ico')

	def init_protocols(self):
		self.window.protocol('WM_DELETE_WINDOW', self.quit)

	def quit(self):
		self.window.quit()
		sys.exit()

	def draw_label(self, text, font = None, color = 'black', bg = None, side = 'top', anchor = 'center', recwidth = None, recheight = None, master = None):
		if master == None: master = self.window

		def conv_anchor(a):
			if a == 'topleft': return 'nw'
			elif a == 'midtop': return 'n' 
			elif a == 'topright': return 'ne'
			elif a == 'midleft': return 'w'
			elif a == 'midright': return 'e'
			elif a == 'bottomleft': return 'sw'
			elif a == 'midbottom': return 's'
			elif a == 'bottomright': return 'se'
			else: return a

		anc = conv_anchor(anchor)
		text = tk.Label(master, text = text, font = font, fg = color, bg = bg, width = recwidth, height = recheight, anchor = anc)
		text.pack(side = side, anchor = anc)

	def draw_blank(self, side = 'top', anchor = 'center', recwidth = None, recheight = None, master = None):
		if master == None: master = self.window
		self.draw_label('', side = side, anchor = anchor, recwidth = recwidth, recheight = recheight, master = master)

	def about_menu(self): tk.messagebox.showinfo(f'{self.lang["menubar_help_about"]}{name}', about_msg)

	def reload(self): self.refresh(True)

	def menubar(self):
		menubar = tk.Menu()

		file_menu = tk.Menu(menubar, tearoff = False)
		file_menu.add_command(label = self.lang['menubar_file_exit'], command = self.quit)
		menubar.add_cascade(label = self.lang['menubar_file'], menu = file_menu)

		edit_menu = tk.Menu(menubar, tearoff = False)
		edit_menu.add_command(label = self.lang['menubar_edit_reload'], command = self.reload)
		menubar.add_cascade(label = self.lang['menubar_edit'], menu = edit_menu)

		settings_menu = tk.Menu(menubar, tearoff = False)
		settings_menu.add_command(label = self.lang['menubar_settings_dtformat'], command = self.n_a)

		lang_menu = tk.Menu(settings_menu, tearoff = False)
		lang_menu.add_radiobutton(label = 'English (US)', variable = self.language, value = 'en_US', command = self.change_lang)
		lang_menu.add_radiobutton(label = 'Tiếng Việt', variable = self.language, value = 'vi_VN', command = self.change_lang)
		settings_menu.add_cascade(label = self.lang['menubar_settings_language'], menu = lang_menu)

		menubar.add_cascade(label = self.lang['menubar_settings'], menu = settings_menu)

		help_menu = tk.Menu(menubar, tearoff = False)
		help_menu.add_command(label = self.lang['menubar_help_update'], command = self.n_a)
		help_menu.add_command(label = f'{self.lang["menubar_help_about"]}{name}', command = self.about_menu)
		menubar.add_cascade(label = self.lang['menubar_help'], menu = help_menu)

		self.window.config(menu = menubar)

	def main(self):
		try: self.draw_label(self.lang['title'], font = (self.font_name, self.font_size, 'bold'))
		except Exception: self.draw_label(self.lang['title'])
		self.draw_blank()
		tk.Button(text = self.lang['main_new_item'], command = self.n_a).pack()

		self.get_bin_items()

		if len(self.corrupted_rbdir_drives) > 0:
			corrupted_text = 'WARNING:\n'
			for drive in self.corrupted_rbdir_drives: corrupted_text += f'The Recycle Bin on drive {drive}: is corrupted.\n'
			corrupted_text = corrupted_text[:-1]
			self.draw_label(corrupted_text)

		if len(self.bin_items) > 0:
			frame = ScrollableFrame(self.window)

			for item in self.bin_items:
				item_frame = tk.Frame(frame.scrollable_frame)
				tk.Button(item_frame, text = self.lang['main_properties'], command = self.n_a).pack(side = 'right')
				tk.Button(item_frame, text = self.lang['main_delete'], command = lambda e = item: self.delete_item(e)).pack(side = 'right')
				tk.Button(item_frame, text = self.lang['main_restore'], command = lambda e = item: self.restore_item(e)).pack(side = 'right')
				tk.Button(item_frame, text = self.lang['main_open'], command = lambda e = item: self.open_item(e)).pack(side = 'right')
				self.draw_label(self.bin_items[item]['ogname'] if self.bin_items[item]['type'] != 'File folder' else f'{self.bin_items[item]["ogname"]} <folder>', side = 'left', master = item_frame)
				item_frame.pack(fill = 'both')

			frame.scrollable_frame.pack(fill = 'both')
			frame.pack(fill = 'both')

		else: self.draw_label(self.lang['main_rbin_empty'])

		self.window.mainloop()

	def check_item_exist(self, item):
		if not os.path.exists(f'{self.bin_items[item]["rbin_drive"]}{self.rbdir}\\$R{item}'):
			tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_not_in_rb'])
			self.refresh(True)

	def open_item(self, item):
		def start(path): os.system(f'start "" "{path}" >nul 2>&1')
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		ext = item_info['ext']
		drive = item_info['rbin_drive']

		path = f'{drive}{self.rbdir}\\$R{item}'
		
		if os.path.isdir(path):
			if tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_folder_warn'], icon = 'warning', default = 'no'): os.system(f'start "" explorer "{path}"')
		else:
			if ext == '.lnk':
				if tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_lnk_warn'], icon = 'warning', default = 'no'):
					start(path)
					self.refresh(True)

	def get_item_info_str(self, item):
		item_info = self.bin_items[item]
		ogname = item_info['ogname']
		oglocation = item_info['oglocation']
		item_type = item_info['type']
		size = item_info['size']
		deldate = item_info['deldate']

		return f'{ogname}\n{self.lang["oglocation"]}: {oglocation}\n{self.lang["type"]}: {item_type}\n{self.lang["size"]}: {self.convert_size(size)}\n{self.lang["deldate"]}: {deldate}'

	def delete_item(self, item):		
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']
		ogname = item_info['ogname']
		oglocation = item_info['oglocation']
		item_type = item_info['type']
		size = item_info['size']
		deldate = item_info['deldate']

		path = f'{drive}{self.rbdir}\\'

		if tk.messagebox.askyesno(self.lang['msgbox_delete'], f'{self.lang["msgbox_delete_desc"]}\n\n{self.get_item_info_str(item)}', icon = 'warning'):
			if os.path.isdir(path): shutil.rmtree(f'{path}$R{item}', ignore_errors = True)
			else: os.remove(f'{path}$R{item}')
			os.remove(f'{path}$I{item}')
			self.refresh(True)

	def restore_item(self, item):
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']
		ogname = item_info['ogname']
		oglocation = item_info['oglocation']

		path = f'{drive}{self.rbdir}\\'
		ogpath = oglocation + ogname

		if tk.messagebox.askyesno(self.lang['msgbox_restore'], f'{self.lang["msgbox_restore_desc"]}\n\n{self.get_item_info_str(item)}'):
			shutil.move(f'{path}$R{item}', ogpath)
			os.remove(f'{path}$I{item}')
			self.refresh(True)

# unfinished!
class ItemEdit:
	def __init__(self, gui):
		self.gui = gui

		self.draw_label = self.gui.draw_label
		self.draw_blank = self.gui.draw_blank
		self.refresh = self.gui.refresh

	def show_properties(self, item):
		item_info = self.gui.bin_items[item]

		self.refresh()
		self.draw_label('Item properties', font = (self.font_name, self.font_size, 'bold'))
		self.draw_blank()
		self.draw_label(item_info['ogname'])
		self.draw_label(f'Original location: {item_info["oglocation"]}')

# https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(tk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		canvas = tk.Canvas(self)
		scrollbar = tk.Scrollbar(self, orient = 'vertical', command = canvas.yview)
		self.scrollable_frame = tk.Frame(canvas)
		self.scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
		canvas.create_window((0, 0), window = self.scrollable_frame, anchor = 'nw')
		canvas.configure(yscrollcommand = scrollbar.set)
		canvas.pack(side = 'left', fill = 'both', expand = True)
		scrollbar.pack(side = 'right', fill = 'y')