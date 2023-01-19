import sys
if __name__ == '__main__':
	print('Please run main.py to start the program!')
	sys.exit()

import os
import platform
import traceback
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog

try: temp_path = sys._MEIPASS
except AttributeError: temp_path = os.getcwd()

# main modules
try: import wmi
except ImportError:
	print('ERROR: No WMI module found!')
	tk.messagebox.showerror('Error', 'No WMI module found!')
	sys.exit()

import re
import math
import ctypes
import locale
import random
import shutil
import string
import getpass
import binascii
import tempfile
import win32file
import webbrowser
import collections
import configparser
from decimal import Decimal
from calendar import timegm
from datetime import datetime, timedelta, timezone

import winreg
from winreg import HKEY_CLASSES_ROOT as HKCR

name = 'RBEditor'

username = 'gamingwithevets'
repo_name = 'rbeditor'

version = 'Beta 1.3.0'
internal_version = 'b1.3.0'
prerelease = True

license = 'MIT'

try: import lang
except ImportError:
	err_text = f'Whoops! The script "lang.py" is required.\nCan you make sure the script is in "{temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
	print(err_text)
	tk.messagebox.showerror('Hmmm?', err_text)
	sys.exit()

def report_error(self = None, exc = None, val = None, tb = None):
	try: GUI.window.quit()
	except Exception: pass

	e = traceback.format_exc()
	err_text = f'Whoops! An error has occurred.\n\n{e}\nIf this error persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'

	print(err_text)
	tk.messagebox.showerror('Whoops!', err_text)
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

		self.rbdir = self.gui.rbdir = f'\\$RECYCLE.BIN\\{sid}'

	def get_bin_items(self):
		drives = self.get_drives()
		self.gui.corrupted_rbdir_drives = []
		bin_items_list = []
		dirlist = []
		errno_whitelist = [13, 2]
		for drive in drives:
			try: dirlist.extend(os.listdir(f'{drive}:{self.rbdir}'))
			except IOError as e:
				if e.errno not in errno_whitelist: self.gui.corrupted_rbdir_drives.append(drive)
		for f in dirlist:
			if f[:2] == '$I': bin_items_list.append(f[2:])

		self.gui.bin_items = {}
		bin_items_unsorted = {}
		for item in bin_items_list:
			filedata = self.read_metadata(item)
			if filedata['skip']:
				self.gui.enable_rbin_metadata_unsupported_version_msg = True
				continue
			if self.get_rb_path(item, 'R') == None: continue

			try: dirtest = os.path.isdir(self.get_rb_path(item, 'R'))
			except: dirtest = False

			ext = os.path.splitext(filedata['fname'])[1].lower()

			bin_items_unsorted[item] = {
			'ogname': os.path.basename(filedata['fname']),
			'type': self.gui.lang['ftype_desc_folder'] if dirtest else self.get_ftype_desc(ext),
			'ext': None if dirtest or not ext else ext,
			'oglocation': os.path.dirname(filedata['fname']),
			'size': filedata['fsize'],
			'deldate': filedata['deldate'].strftime(self.gui.date_format),
			'rbin_drive': self.get_rb_path(item)[0],
			'version': self.get_md_version(filedata['version']),
			}

		if len(bin_items_unsorted) > 0: self.gui.bin_items = dict(collections.OrderedDict(sorted(bin_items_unsorted.items(), key = lambda x: x[1]['ogname'].lower())))

	def get_md_version(self, version):
		if 'itemedit_version_'+str(version) in self.gui.lang: return f'{self.gui.lang["itemedit_version_text"]}{version} {self.gui.lang["itemedit_version_"+str(version)]}'
		else: return f'{self.gui.lang["itemedit_version_text"]}{version} {self.gui.lang["itemedit_version_text_unknown"]}'

	def get_ftype_desc(self, ext):
		if not ext: return self.gui.lang['ftype_desc_file']
		# translations for these extensions are stored in the language packs themselves,
		# therefore the file type descriptions need to be stored in the program itself.
		elif ext == '.txt': return self.gui.lang['ftype_desc_txt']
		elif ext == '.ini': return self.gui.lang['ftype_desc_ini']
		elif ext == '.ps1': return self.gui.lang['ftype_desc_ps1']
		elif ext == '.ico': return self.gui.lang['ftype_desc_ico']
		else:
			try:
				desc = winreg.QueryValue(HKCR, winreg.QueryValue(HKCR, ext))
				if desc: return desc
				else:
					if self.gui.lang['ftype_desc_file_right']: return f'{ext[1:].upper()} {self.gui.lang["ftype_desc_file"]}'
					else: return f'{self.gui.lang["ftype_desc_file"]} {ext[1:].upper()}'
			except Exception:
				if self.gui.lang['ftype_desc_file_right']: return f'{ext[1:].upper()} {self.gui.lang["ftype_desc_file"]}'
				else: return f'{self.gui.lang["ftype_desc_file"]} {ext[1:].upper()}'

	def get_os_version(self):
	    """
	    https://stackoverflow.com/a/22325767

	    Get's the OS major and minor versions.  Returns a tuple of
	    (OS_MAJOR, OS_MINOR).
	    """
	    os_version = OSVERSIONINFOEXW()
	    os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
	    retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))
	    if retcode != 0:
	        raise Exception("Failed to get OS version")

	    return os_version.dwMajorVersion, os_version.dwMinorVersion

	def get_drives(self):
		drives = []
		for drive in string.ascii_uppercase:
			if win32file.GetDriveType(drive+':') == win32file.DRIVE_FIXED: drives.append(drive)

		return drives

	def filetime_to_dt(self, ft):
		tz = self.gui.tz

		time_utc = datetime(1970, 1, 1) + timedelta(microseconds = (ft - 116444736000000000) // 10)
		time_utc = time_utc.replace(tzinfo = timezone.utc)
		return time_utc.astimezone(tz)

	def dt_to_filetime(self, dt):
		time_utc = dt.astimezone(timezone.utc)
		return 116444736000000000 + (timegm(dt.timetuple()) * 10000000)

	def convert_size(self, size_bytes):
		def f(s): return f'{s:n}'

		def add_digits(i, s):
			if i != 0:
				digits = 0
				s_temp = s
				while s_temp > 0:
					digits += 1
					s_temp //= 10

				if digits == 1: return f(Decimal(f'{s:.2f}'))
				elif digits == 2: return f(Decimal(f'{s:.1f}'))
				elif digits == 3: return str(s)

		def print_size(i, s, s_nostr, snl, mul): return f'{s if i <= len(snl) else f(round(size_bytes / math.pow(mul, len(snl))))} {snl[i-1] if i <= len(snl) else snl[-1]}'

		if size_bytes == 0: return f'0 {self.gui.lang["bytes"]}'
		elif size_bytes > 0:
			size_names_pow2 = ('KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')
			i_pow2 = int(math.floor(math.log(size_bytes, 1024)))
			s_pow2_notstr = size_bytes / math.pow(1024, i_pow2)

			size_names_pow10 = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'RB', 'QB')
			i_pow10 = int(math.floor(math.log(size_bytes, 1000)))
			s_pow10_notstr = size_bytes / math.pow(1000, i_pow10)

			s_pow2 = add_digits(i_pow2, s_pow2_notstr)
			s_pow10 = add_digits(i_pow10, s_pow10_notstr)

			if i_pow10 == 0: return f'{size_bytes:n} {self.gui.lang["bytes"]}'
			else:
				if i_pow2 == 0: return f'{print_size(i_pow10, s_pow10, s_pow10_notstr, size_names_pow10, 1000)} ({size_bytes:n} {self.gui.lang["bytes"]})'
				else: return f'{print_size(i_pow2, s_pow2, s_pow2_notstr, size_names_pow2, 1024)} ({print_size(i_pow10, s_pow10, s_pow10_notstr, size_names_pow10, 1000)} - {size_bytes:n} {self.gui.lang["bytes"]})'
		else: return f'{size_bytes} {self.gui.lang["bytes"]}'

	def read_metadata(self, file_to_read):
		# initialization
		fname = fsize = deldate = version = None
		skip = False

		file_path = self.get_rb_path(file_to_read)

		bytes_required = 44

		# avoid errors with empty/fake metadata files
		if os.path.getsize(file_path) < bytes_required:
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'$I{file_to_read}{self.gui.lang["msgbox_error_invalid_metadata"]}')
			skip = True
		else:
			file = open(file_path, 'rb')

			version_b = bytearray(file.read(8))
			version = int.from_bytes(version_b, 'little')
			if version == 2:
				fsize_b = bytearray(file.read(8))
				fsize_u = int.from_bytes(fsize_b, 'little')
				fsize = fsize_u if fsize_u < (1 << 64 - 1) else fsize_u - (1 << 64)
				deldate_b = bytearray(file.read(8))
				deldate = self.filetime_to_dt(int.from_bytes(deldate_b, 'little'))
				fnamelen_b = bytearray(file.read(4))
				fnamelen = int.from_bytes(fnamelen_b, 'little')
				fname = ''
				for i in range(fnamelen):
					char_b = file.read(2)
					if char_b == b'': tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'$I{file_to_read}{self.gui.lang["msgbox_error_incorrect_fnamelen"]}'); break
					if char_b == b'\x00\x00': break
					char = char_b.decode('utf-16le')
					fname += char

			elif version == 1:
				fsize_b = bytearray(file.read(8))
				fsize_u = int.from_bytes(fsize_b, 'little')
				fsize = fsize_u if fsize_u < (1 << 64 - 1) else fsize_u - (1 << 64)
				deldate_b = bytearray(file.read(8))
				deldate = self.filetime_to_dt(int.from_bytes(deldate_b, 'little'))
				fname = ''
				for i in range(260):
					char_b = file.read(2)
					if char_b == b'\x00\x00': break
					char = char_b.decode('utf-16le')
					fname += char

			else:
				self.gui.enable_rbin_metadata_unsupported_version_msg = True
				skip = True
				tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'$I{file_to_read}{self.gui.lang["msgbox_error_unsupported_version"]} (v{version})')

		return {'fname': fname, 'fsize': fsize, 'deldate': deldate, 'version': version, 'skip': skip}

	def write_metadata(self, version, fname, fsize, deldate, is_folder):
		file_data = b''

		file_data += version.to_bytes(8, 'little')
		if version == 2:
			file_data += fsize.to_bytes(8, 'little')
			file_data += self.dt_to_filetime(deldate).to_bytes(8, 'little')
			fnamelen = len(fname) + 1
			file_data += fnamelen.to_bytes(4, 'little')
			for char in fname:
				char_b = char.encode('utf-16le')
				file_data += char_b
			file_data += b'\x00\x00'
		elif version == 1:
			file_data += fsize.to_bytes(8, 'little')
			file_data += self.dt_to_filetime(deldate).to_bytes(8, 'little')
			fnamelen = len(fname)
			for char in fname:
				char_b = char.encode('utf-16le')
				file_data += char_b
			for i in range(260 - fnamelen): file_data += b'\x00\x00'

		drive = os.path.splitdrive(fname)[0]
		ext = os.path.splitext(fname)[1]
		ind_drive_rbdir = f'{drive}{self.rbdir}'
		f = os.listdir(ind_drive_rbdir)

		while True:
			random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
			if f'$I{random_str}{ext}' not in f: break

		with open(f'{ind_drive_rbdir}\\$I{random_str}{ext}', 'wb') as g: g.write(file_data)
		if is_folder: os.mkdir(f'{ind_drive_rbdir}\\$R{random_str}{ext}')
		else:
			with open(f'{ind_drive_rbdir}\\$R{random_str}{ext}', 'w') as g: pass

	def get_rb_path(self, file, typ = 'I'):
		drives = self.get_drives()

		fname = f'${typ}{file}'
		for drive in drives:
			ind_drive_rbdir = f'{drive}:{self.rbdir}'
			f = os.listdir(ind_drive_rbdir)
			if fname in f: return f'{ind_drive_rbdir}\\{fname}'

	def get_rb_path_friendly(self, file, typ = 'I'):
		file_path = os.path.dirname(self.get_rb_path(file, typ))
		if self.gui.lang['rbin_in_right']: return f'{file_path[:2]}{self.gui.lang["rbin_in"]} | {file_path}'
		else: return f'{self.gui.lang["rbin_in"]}{file_path[:2]} | {file_path}'

class GUI:
	def __init__(self, window):
		self.version = version

		self.window = window

		try:
			import requests
			global requests
			self.updates = True
		except ImportError:
			self.updates = False
			print('ERROR: No "requests" module found! Update checking disabled.')
			tk.messagebox.showerror('Error', 'No "requests" module found! Update checking disabled.')
		#except: pass

		self.temp_path = temp_path

		self.display_w = 800
		self.display_h = 500

		self.dt_win_open = False

		tk_font = tk.font.nametofont('TkDefaultFont').actual()
		self.font_name = tk_font['family']
		self.font_size = tk_font['size']

		self.bold_font = (self.font_name, self.font_size, 'bold')

		self.init_window()
		self.init_protocols()

		# default settings
		self.default_date_format = '%c'
		self.date_format = self.default_date_format
		self.tz = datetime.now(timezone.utc).astimezone().tzinfo

		self.languages = lang.lang.keys()
		self.language_tk = tk.StringVar(); self.language_tk.set('system')
		self.language = ''
		self.system_language_unavailable = False

		self.auto_check_updates = tk.BooleanVar(); self.auto_check_updates.set(True)
		self.check_prerelease_version = tk.BooleanVar(); self.check_prerelease_version.set(False)

		self.enable_rbin_metadata_unsupported_version_msg = False

		self.language_names = {
		'en_US': 'English (US)',
		'ja_JP': '日本語',
		'vi_VN': 'Tiếng Việt',
		}

		self.language_labels = {
		'en_US': 'English',
		'ja_JP': 'Japanese',
		'vi_VN': 'Vietnamese',
		}

		self.appdata_folder = f'{os.getenv("LOCALAPPDATA")}\\RBEditor'
		self.ini = configparser.ConfigParser()
		self.parse_settings()

		self.refreshing = True

		self.rbhandler = RBHandler(self)
		self.itemedit = ItemEdit(self)
		self.dt_menu = DTMenu(self)
		self.new_item = NewItem(self)
		self.updater = Updater() # updater is seperated from the main program, therefore it does not need the GUI class

		self.rbhandler.get_rbdir()
		self.menubar()

	def start_main(self):
		if self.auto_check_updates.get(): self.check_updates(True)
		self.main()

	def parse_settings(self):
		try:
			self.ini.read(f'{self.appdata_folder}\\settings.ini')
			self.language_tk.set(self.ini['settings']['language'])
			self.date_format = self.ini['settings']['date_format'].replace('%%', '%')

			if 'updater' in self.ini:
				self.auto_check_updates.set(self.ini.getboolean('updater', 'auto_check_updates'))
				self.check_prerelease_version.set(self.ini.getboolean('updater', 'check_prerelease_version'))

		except Exception: print(traceback.format_exc())
		
		self.set_lang()

	def save_settings(self):
		# settings are set individually to retain compatibility between versions
		self.ini['settings'] = {}
		self.ini['settings']['language'] = self.language_tk.get()
		self.ini['settings']['date_format'] = self.date_format.replace('%', '%%')

		self.ini['updater'] = {}
		self.ini['updater']['auto_check_updates'] = str(self.auto_check_updates.get())
		self.ini['updater']['check_prerelease_version'] = str(self.check_prerelease_version.get())

		if not os.path.exists(self.appdata_folder): os.makedirs(self.appdata_folder)
		with open(f'{self.appdata_folder}\\settings.ini', 'w') as f: self.ini.write(f)

	def get_lang(self):
		slang = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
		if slang in self.languages: return slang
		else:
			self.system_language_unavailable = True
			return 'en_US'

	def set_lang(self):
		if self.language_tk.get() == 'system':
			self.language = self.get_lang()
			if self.system_language_unavailable:
				self.language_tk.set('en_US')
				self.save_settings()
				tk.messagebox.showwarning('Warning', f'Your system language is not available in this version of {name}.\n\n{name}\'s language has been set to English (US).')
		else: self.language = self.language_tk.get()

		locale.setlocale(locale.LC_ALL, self.language_labels[self.language])

		self.lang = lang.lang['en_US'].copy()
		lang_new = lang.lang[self.language].copy()
		for key in lang_new: self.lang[key] = lang_new[key]

	def change_lang(self):
		self.set_lang()
		self.save_settings()
		self.reload()

	def n_a(self): tk.messagebox.showinfo(self.lang['msgbox_n_a'], f'{self.lang["msgbox_n_a_desc"]}{name}{self.lang["msgbox_n_a_desc2"]}')

	def refresh(self, load_func = False, custom_func = None):
		self.refreshing = True

		for w in self.window.winfo_children(): w.destroy()
		self.menubar()

		if load_func:
			if custom_func == None: self.main()
			else: custom_func() 

	def set_title(self, custom_str = None): self.window.title(f'{name} {version}{" - " + custom_str if custom_str != None else ""}')

	def init_window(self):
		self.window.geometry(f'{self.display_w}x{self.display_h}')
		self.window.resizable(False, False)
		self.window.unbind_all('<<NextWindow>>') # disable TAB focus (only temporary, will be removed when TAB key functionality is developed)
		self.set_title()
		try: self.window.iconbitmap(f'{self.temp_path}\\icon.ico')
		except tk.TclError:
			err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues'
			print(err_text)
			tk.messagebox.showerror('Hmmm?', err_text)
			sys.exit()

	def init_protocols(self):
		self.window.protocol('WM_DELETE_WINDOW', self.quit)

	def quit(self):
		if not self.dt_win_open:
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

	def draw_blank(self, master = None):
		if master == None: master = self.window
		self.draw_label('', master = master)

	def about_menu(self): tk.messagebox.showinfo(f'{"" if self.lang["menubar_help_about_right"] else self.lang["menubar_help_about"]}{name}{self.lang["menubar_help_about"] if self.lang["menubar_help_about_right"] else ""}', f'''\
{name} - {version} ({'64' if sys.maxsize > 2**31-1 else '32'}-bit) - {'' if self.lang['about_running_on_right'] else self.lang['about_running_on']}{platform.system()} x{'64' if platform.machine().endswith('64') else '86'}{self.lang['about_running_on'] if self.lang['about_running_on_right'] else ''}
{self.lang['about_project_page']}https://github.com/{username}/{repo_name}
{self.lang['about_beta_build'] if prerelease else ''}
{self.lang['about_licensed']}{license}{self.lang['about_licensed2'] if self.lang['about_licensed_right'] else ''}

Copyright (c) 2022-2023 GamingWithEvets Inc.

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
''')

	def reload(self):
		tk.messagebox.showwarning(self.lang['msgbox_warning'], self.lang['msgbox_setting_change'])
		self.itemedit.show_advanced = False
		self.refresh(True)

	def menubar(self):
		menubar = tk.Menu()

		rbin_menu = tk.Menu(menubar, tearoff = False)
		rbin_menu.add_command(label = self.lang['menubar_rbin_reload'], command = self.reload)
		rbin_menu.add_command(label = self.lang['menubar_rbin_exit'], command = self.quit)
		menubar.add_cascade(label = self.lang['menubar_rbin'], menu = rbin_menu)

		settings_menu = tk.Menu(menubar, tearoff = False)
		settings_menu.add_command(label = self.lang['menubar_settings_dtformat'], command = self.dt_menu.init_window)

		self.lang_menu = tk.Menu(settings_menu, tearoff = False)
		self.lang_menu.add_radiobutton(label = self.lang['menubar_settings_language_system'], variable = self.language_tk, value = 'system', command = self.change_lang, state = 'disabled' if self.system_language_unavailable else 'normal')
		for i in self.language_names: self.lang_menu.add_radiobutton(label = self.language_names[i], variable = self.language_tk, value = i, command = self.change_lang)
		self.ena_dis_lang()
		settings_menu.add_cascade(label = self.lang['menubar_settings_language'], menu = self.lang_menu)

		updater_settings_menu = tk.Menu(settings_menu, tearoff = False)
		updater_settings_menu.add_checkbutton(label = self.lang['menubar_settings_updates_auto'], variable = self.auto_check_updates, command = self.save_settings)
		updater_settings_menu.add_checkbutton(label = self.lang['menubar_settings_updates_prerelease'], variable = self.check_prerelease_version, command = self.save_settings)
		settings_menu.add_cascade(label = self.lang['menubar_settings_updates'], menu = updater_settings_menu)

		menubar.add_cascade(label = self.lang['menubar_settings'], menu = settings_menu)

		help_menu = tk.Menu(menubar, tearoff = False)
		help_menu.add_command(label = self.lang['menubar_help_update'], command = self.check_updates, state = 'normal' if self.updates else 'disabled')
		help_menu.add_command(label = f'{"" if self.lang["menubar_help_about_right"] else self.lang["menubar_help_about"]}{name}{self.lang["menubar_help_about"] if self.lang["menubar_help_about_right"] else ""}', command = self.about_menu)
		menubar.add_cascade(label = self.lang['help'], menu = help_menu)

		self.window.config(menu = menubar)

	def ena_dis_lang(self):
		for name in self.language_names:
			# try-except nest used in case of an unused language in language_names
			try: self.lang_menu.entryconfig(name, state = 'normal')
			except Exception: pass

		if self.language_tk.get() == 'system': self.lang_menu.entryconfig(self.lang['menubar_settings_language_system'], state = 'disabled')
		else: self.lang_menu.entryconfig(self.language_names[self.language], state = 'disabled')

	def check_updates(self, auto = False):
		self.set_title(self.lang['main_updater'])
		update_info = self.updater.check_updates(self.check_prerelease_version.get())
		self.set_title()

		if update_info['error']:
			if not auto:
				if update_info['exceeded']: tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_updater_exceeded'])
				elif update_info['nowifi']: tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_updater_offline'])
				else: tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_updater_unknown_error'])
		elif update_info['newupdate']:
			if tk.messagebox.askyesno(self.lang['msgbox_updater_newupdate_title'], f'''\
{self.lang['msgbox_updater_newupdate']}

{self.lang['msgbox_updater_currver']} {self.version}{self.lang['msgbox_updater_prerelease'] if prerelease else ''}
{self.lang['msgbox_updater_newver']} {update_info['title']}{self.lang['msgbox_updater_prerelease'] if prerelease else ''}

{self.lang['msgbox_updater_prompt']}\
''', icon = 'info'): webbrowser.open_new_tab(f'https://github.com/gamingwithevets/rbeditor/releases/tag/{update_info["tag"]}')
		else:
			if not auto: tk.messagebox.showinfo(self.lang['msgbox_notice'], self.lang['msgbox_updater_latest'])

	def main(self):
		try: self.draw_label(self.lang['title'], font = self.bold_font)
		except Exception: self.draw_label(self.lang['title'])
		self.draw_blank()

		if self.refreshing:
			self.set_title(self.lang['main_loading'])
			self.rbhandler.get_bin_items()
			self.refreshing = False

		if len(self.corrupted_rbdir_drives) > 0:
			corrupted_text = f'{self.lang["main_warning"]}\n'
			for drive in self.corrupted_rbdir_drives: corrupted_text += f'{self.lang["main_rb_corrupt"]} {drive}: {self.lang["main_rb_corrupt_2"]}\n'
			corrupted_text = corrupted_text[:-1]
			self.draw_label(corrupted_text)
			self.draw_blank()

			if self.enable_rbin_metadata_unsupported_version_msg:
				self.draw_blank()
				self.draw_label(self.lang['main_rbin_metadata_unsupported_version'])
				self.enable_rbin_metadata_unsupported_version_msg = False

		if len(self.bin_items) > 0:
			button_frame = tk.Frame()
			ttk.Button(button_frame, text = self.lang['main_new_item'], command = self.new_item.create_item).pack(side = 'left')
			ttk.Button(button_frame, text = self.lang['main_restore_all'], command = self.restore_all).pack(side = 'left')
			ttk.Button(button_frame, text = self.lang['main_empty_rb'], command = self.delete_all).pack(side = 'right')
			button_frame.pack()
			self.draw_blank()

			frame = VerticalScrolledFrame(self.window)
			frame.pack(fill = 'both', expand = True)

			for item in self.bin_items:
				item_frame = tk.Frame(frame.interior)
				ttk.Button(item_frame, text = self.lang['main_properties'], command = lambda e = item: self.itemedit.show_properties(e)).pack(side = 'right')
				ttk.Button(item_frame, text = self.lang['main_delete'], command = lambda e = item: self.delete_item(e)).pack(side = 'right')
				ttk.Button(item_frame, text = self.lang['main_restore'], command = lambda e = item: self.restore_item(e)).pack(side = 'right')
				ttk.Button(item_frame, text = self.lang['main_open'], command = lambda e = item: self.open_item(e)).pack(side = 'right')
				self.draw_label(self.bin_items[item]['ogname'] if self.bin_items[item]['type'] != 'File folder' else f'{self.bin_items[item]["ogname"]} <folder>', side = 'left', anchor = 'midleft', master = item_frame)
				item_frame.pack(fill = 'both')

		else:
			ttk.Button(text = self.lang['main_new_item'], command = self.new_item.create_item).pack()
			self.draw_blank()
			self.draw_label(self.lang['main_rbin_empty'])

		self.set_title()
		self.window.mainloop()

	def check_item_exist(self, item):
		if not os.path.exists(f'{self.bin_items[item]["rbin_drive"]}:{self.rbdir}\\$R{item}'):
			tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_not_in_rb'])
			self.refresh(True)

	def open_item(self, item):
		def start(path, folder = False):
			if folder: subprocess.Popen(f'explorer "{path}"', shell=True)
			else: subprocess.Popen(path, shell=True)

		item_info = self.bin_items[item]
		ext = item_info['ext']
		drive = item_info['rbin_drive']

		path = f'{drive}:{self.rbdir}\\$R{item}'
		
		if os.path.isdir(path):
			if tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_folder_warn'], icon = 'warning', default = 'no'): start(path, True)
		else:
			if ext == '.lnk':
				if tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_lnk_warn'], icon = 'warning', default = 'no'): start(path)
			else: start(path)

	def get_item_info_str(self, item):
		item_info = self.bin_items[item]
		ogname = item_info['ogname']
		oglocation = item_info['oglocation']
		item_type = item_info['type']
		size = item_info['size']
		deldate = item_info['deldate']

		return f'{ogname}\n{self.lang["oglocation"]}: {oglocation}\n{self.lang["type"]}: {item_type}\n{self.lang["size"]}: {self.rbhandler.convert_size(size)}\n{self.lang["deldate"]}: {deldate}'

	def delete_item(self, item, no_prompt = False, no_refresh = False):		
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']

		path = f'{drive}:{self.rbdir}\\'

		if not no_prompt:
			if not tk.messagebox.askyesno(self.lang['msgbox_delete'], f'{self.lang["msgbox_delete_desc"]}\n\n{self.get_item_info_str(item)}', icon = 'warning', default = 'no'): return
		if os.path.isdir(path): shutil.rmtree(f'{path}$R{item}', ignore_errors = True)
		else:
			try: os.remove(f'{path}$R{item}')
			except OSError: pass
		try: os.remove(f'{path}$I{item}')
		except OSError: pass
		if not no_refresh: self.refresh(True)

	def restore_item(self, item, no_prompt = False, no_refresh = False):
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']
		ogname = item_info['ogname']
		oglocation = item_info['oglocation']

		path = f'{drive}:{self.rbdir}\\'
		ogpath = oglocation + '\\' + ogname

		if not no_prompt:
			if not tk.messagebox.askyesno(self.lang['msgbox_restore'], f'{self.lang["msgbox_restore_desc"]}\n\n{self.get_item_info_str(item)}'): return

		if os.path.exists(ogpath):
			if not tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_overwrite1']+ogname+self.lang['msgbox_overwrite2'], icon = 'warning'):
				if no_refresh: return
				else: self.refresh(True)
		try: shutil.move(f'{path}$R{item}', ogpath)
		except OSError: pass
		try: os.remove(f'{path}$I{item}')
		except OSError: pass
		if not no_refresh: self.refresh(True)

	def delete_all(self):
		if tk.messagebox.askyesno(self.lang['msgbox_delete_all'], self.lang['msgbox_delete_all_desc'], icon = 'warning', default = 'no'):
			for item in self.bin_items: self.delete_item(item, True, True)
		self.refresh(True)

	def restore_all(self):
		if tk.messagebox.askyesno(self.lang['msgbox_restore_all'], self.lang['msgbox_restore_all_desc']):
			for item in self.bin_items: self.restore_item(item, True, True)
		self.refresh(True)

class DTMenu:
	def __init__(self, gui):
		self.gui = gui
		self.preview_date_time = datetime(2021, 10, 4, 14, 0, 0)

	def init_window(self):
		if not self.gui.dt_win_open:
			self.gui.dt_win_open = True
			self.dt_preview = False

			self.dt_win = tk.Toplevel(self.gui.window)
			self.dt_win.geometry('500x500')
			self.dt_win.resizable(False, False)
			self.dt_win.protocol('WM_DELETE_WINDOW', self.quit)
			self.dt_win.title(self.gui.lang['title_dtformat'])
			try: self.dt_win.iconbitmap(f'{self.gui.temp_path}\\icon.ico')
			except tk.TclError:
				err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.gui.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/gamingwithevets/{repo_name}/issues'
				print(err_text)
				tk.messagebox.showerror('Hmmm?', err_text)
				sys.exit()

			self.draw_menu()

		self.dt_win.focus()
		self.dt_win.grab_set()
		self.dt_win.mainloop()

	def quit(self):
		self.dt_win.grab_release()
		self.dt_win.destroy()
		self.gui.dt_win_open = False

	def discard(self):
		if self.get_dt_entry() != self.gui.date_format:
			if tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_discard'], icon = 'warning', default = 'no'): self.quit()
		else: self.quit()

	def preview(self):
		self.text = self.get_dt_entry(True)
		if self.text_check():
			self.dt_preview = True
			self.draw_menu()
		else: return

	def save(self):
		self.text = self.get_dt_entry(True, True) 
		if self.text_check():
			if self.gui.date_format != self.text:
				self.gui.date_format = self.text
				self.quit()
				self.gui.reload()
			else: self.quit()
		else: return

	def text_check(self):
		if self.text == '':
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_blank'])
			return False
		if '%' not in self.text:
			if not tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_no_formatting'], icon = 'warning'): return False

		return True

	def get_dt_entry(self, show_warning = False, encode_check = False):
		try:
			dt_entry = self.dt_entry.get()
			return dt_entry
		except UnicodeDecodeError:
			if show_warning:
				tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_unicode_error'])
				self.text = self.gui.date_format
				self.draw_menu()

			dt_entry = self.gui.date_format
			return dt_entry

		if encode_check:
			try: self.preview_date_time.strftime(dt_entry)
			except UnicodeEncodeError:
				if show_warning:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_unicode_error'])
					self.text = self.gui.date_format
					self.draw_menu()

				dt_entry = self.gui.date_format
				return dt_entry

	def help(self):
		tk.messagebox.showinfo(self.gui.lang['help'], self.gui.lang['dtformat_guide'])

	def draw_menu(self):
		for w in self.dt_win.winfo_children(): w.destroy()

		self.gui.draw_label(self.gui.lang['title_dtformat'], font = self.gui.bold_font, master = self.dt_win)
		self.gui.draw_blank(self.dt_win)
		ttk.Button(self.dt_win, text = self.gui.lang['discard'], command = self.discard).pack(side = 'bottom')
		ttk.Button(self.dt_win, text = self.gui.lang['preview'], command = self.preview).pack(side = 'bottom')
		ttk.Button(self.dt_win, text = 'OK', command = self.save).pack(side = 'bottom')

		self.gui.draw_label(self.gui.lang['dtformat'], master = self.dt_win)

		scroll = ttk.Scrollbar(self.dt_win, orient = 'horizontal')
		self.dt_entry = ttk.Entry(self.dt_win, width = self.dt_win.winfo_width(), justify = 'center', xscrollcommand = scroll.set)
		try: self.dt_entry.insert(0, self.text)
		except AttributeError: self.dt_entry.insert(0, self.gui.date_format)
		self.dt_entry.pack()
		scroll.config(command = self.dt_entry.xview)
		scroll.pack(fill = 'x')
		ttk.Button(self.dt_win, text = self.gui.lang['help'], command = self.help).pack()

		if self.dt_preview:
			try: self.gui.draw_label(f'{self.gui.lang["dtformat_preview"]}\n{self.preview_date_time.strftime(self.text)}', master = self.dt_win)
			except UnicodeEncodeError:
				tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_unicode_error'])
				self.dt_preview = False
				self.draw_menu()


class ItemEdit:
	def __init__(self, gui):
		self.gui = gui

		self.draw_label = self.gui.draw_label
		self.draw_blank = self.gui.draw_blank
		self.bold_font = self.gui.bold_font

		self.refresh = self.gui.refresh

		self.show_advanced = False

	def show_properties(self, item):
		item_info = self.gui.bin_items[item]

		self.refresh()
		self.draw_label(self.gui.lang['itemedit_properties'], font = self.bold_font)
		self.draw_blank()
		ttk.Button(text = self.gui.lang['back'], command = self.quit).pack(side = 'bottom')

		ogname_frame = tk.Frame()
		self.draw_label(self.gui.lang['itemedit_ogname'], font = self.bold_font, side = 'left', master = ogname_frame)
		self.draw_label(item_info['ogname'], side = 'right', master = ogname_frame)
		ogname_frame.pack(fill = 'x')

		oglocation_frame = tk.Frame()
		self.draw_label(self.gui.lang['oglocation'], font = self.bold_font, side = 'left', master = oglocation_frame)
		self.draw_label(item_info['oglocation'], side = 'right', master = oglocation_frame)
		oglocation_frame.pack(fill = 'x')

		type_frame = tk.Frame()
		self.draw_label(self.gui.lang['type'], font = self.bold_font, side = 'left', master = type_frame)
		self.draw_label(f'{item_info["type"]}{"" if item_info["ext"] == None else " (" + item_info["ext"].lower() + ")"}', side = 'right', master = type_frame)
		type_frame.pack(fill = 'x')

		size = item_info['size']
		size_frame = tk.Frame()
		self.draw_label(self.gui.lang['size'], font = self.bold_font, side = 'left', master = size_frame)
		self.draw_label(self.gui.rbhandler.convert_size(size), side = 'right', master = size_frame)
		size_frame.pack(fill = 'x')

		size_disk_frame = tk.Frame()
		self.draw_label(self.gui.lang['itemedit_size_disk'], font = self.bold_font, side = 'left', master = size_disk_frame)
		self.draw_label(self.gui.rbhandler.convert_size(os.path.getsize(self.gui.rbhandler.get_rb_path(item)) + os.path.getsize(self.gui.rbhandler.get_rb_path(item, 'R'))), side = 'right', master = size_disk_frame)
		size_disk_frame.pack(fill = 'x')

		deldate_frame = tk.Frame()
		self.draw_label(self.gui.lang['deldate'], font = self.bold_font, side = 'left', master = deldate_frame)
		self.draw_label(item_info['deldate'], side = 'right', master = deldate_frame)
		deldate_frame.pack(fill = 'x')

		if self.show_advanced:
			self.draw_blank()

			rbin_name_i_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemedit_rbin_name_i'], font = self.bold_font, side = 'left', master = rbin_name_i_frame)
			self.draw_label(f'$I{item}', side = 'right', master = rbin_name_i_frame)
			rbin_name_i_frame.pack(fill = 'x')

			rbin_name_r_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemedit_rbin_name_r'], font = self.bold_font, side = 'left', master = rbin_name_r_frame)
			self.draw_label(f'$R{item}', side = 'right', master = rbin_name_r_frame)
			rbin_name_r_frame.pack(fill = 'x')

			rbin_location_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemedit_rbin_location'], font = self.bold_font, side = 'left', master = rbin_location_frame)
			self.draw_label('*', side = 'left', master = rbin_location_frame)
			self.draw_label(self.gui.rbhandler.get_rb_path_friendly(item), side = 'right', master = rbin_location_frame)
			rbin_location_frame.pack(fill = 'x')

			real_size = os.path.getsize(self.gui.rbhandler.get_rb_path(item, 'R'))
			if real_size != size:
				real_size_frame = tk.Frame()
				self.draw_label(self.gui.lang['itemedit_real_size'], font = self.bold_font, side = 'left', master = real_size_frame)
				self.draw_label(self.gui.rbhandler.convert_size(real_size), side = 'right', master = real_size_frame)
				real_size_frame.pack(fill = 'x')

			metadata_size_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemedit_metadata_size'], font = self.bold_font, side = 'left', master = metadata_size_frame)
			self.draw_label(self.gui.rbhandler.convert_size(os.path.getsize(self.gui.rbhandler.get_rb_path(item))), side = 'right', master = metadata_size_frame)
			metadata_size_frame.pack(fill = 'x')

			version_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemedit_version'], font = self.bold_font, side = 'left', master = version_frame)
			self.draw_label(item_info['version'], side = 'right', master = version_frame)
			version_frame.pack(fill = 'x')

			self.draw_label(self.gui.lang['itemedit_location_asterisk'])

			ttk.Button(text = self.gui.lang['itemedit_reduced'], command = lambda e = item: self.set_advanced(e, False)).pack()
		else: ttk.Button(text = self.gui.lang['itemedit_advanced'], command = lambda e = item: self.set_advanced(e)).pack()

	def set_advanced(self, item, val = True):
		self.show_advanced = val
		self.show_properties(item)

	def quit(self):
		self.show_advanced = False
		self.refresh(True)

class NewItem:
	def __init__(self, gui):
		self.gui = gui
		self.ntfs_blacklist = '\\/:*?"<>|'
		self.supported_versions = (1, 2)

		self.return_mode = False
		self.discarded = False

	def create_item(self):
		version = '1' if self.gui.rbhandler.get_os_version() <= (6, 3) else '2'
		name = self.gui.lang['new_item_name']
		location = 'C:'
		is_folder = False
		size = 0
		deldate = datetime.utcnow().replace(tzinfo = timezone.utc)

		tuple_here = self.item_maker(False, version, name, location, is_folder, size, deldate)

	def create_item_call(self, version, name, location, is_folder, size, deldate):
		if not self.discarded: file_data = self.gui.rbhandler.write_metadata(version, location+'\\'+name, size, deldate, is_folder)
		self.end()

	def edit_item(self, name, location, is_folder, size, deldate): pass

	def item_maker(self, return_mode, version, name, location, is_folder, size, deldate):
		if return_mode:
			for i in range(1): # allows using break to skip code
				try: size_int = int(size)
				except ValueError:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_size_int_error'])
					break

				try: version_int = int(size)
				except ValueError:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_error_unsupported_version_friendly'])
					break
				if version_int not in self.supported_versions:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_error_unsupported_version_friendly'])
					break

				self.create_item_call(version_int, name, location, is_folder, size_int, deldate)
		else:
			self.version_TEMP = version
			self.name_TEMP = name
			self.location_TEMP = location
			self.is_folder_TEMP = tk.BooleanVar(); self.is_folder_TEMP.set(is_folder)
			self.size_TEMP = size
			self.deldate_TEMP = deldate

			deldate_TEMP_str = self.deldate_TEMP.astimezone().strftime(self.gui.date_format)

			self.gui.refresh()
			self.gui.window.protocol('WM_DELETE_WINDOW', lambda: self.discard(True))
			self.gui.draw_label(self.gui.lang['main_new_item'], font = self.gui.bold_font)
			self.gui.draw_blank()
			ttk.Button(text = self.gui.lang['discard'], command = self.discard).pack(side = 'bottom')
			ok_button = ttk.Button(text = 'OK', command = self.set_return)
			ok_button.pack(side = 'bottom')

			ogname_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['itemedit_ogname'], font = self.gui.bold_font, side = 'left', master = ogname_frame)
			self.ogname_entry = ttk.Entry(ogname_frame, width = 30, justify = 'right')
			self.ogname_entry.insert(0, self.name_TEMP)
			self.ogname_entry.pack(side = 'right')
			ogname_frame.pack(fill = 'x')

			oglocation_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['oglocation'], font = self.gui.bold_font, side = 'left', master = oglocation_frame)
			self.oglocation_entry = ttk.Entry(oglocation_frame, width = 30, justify = 'right')
			self.oglocation_entry.insert(0, self.location_TEMP)
			self.oglocation_entry.pack(side = 'right')
			oglocation_frame.pack(fill = 'x')

			is_folder_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['new_item_folder'], font = self.gui.bold_font, side = 'left', master = is_folder_frame)
			ttk.Checkbutton(is_folder_frame, variable = self.is_folder_TEMP).pack(side = 'right')
			is_folder_frame.pack(fill = 'x')

			size_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['size'], font = self.gui.bold_font, side = 'left', master = size_frame)
			self.gui.draw_label(self.gui.lang['new_item_bytes_note'], side = 'left', master = size_frame)
			self.size_entry = ttk.Entry(size_frame, width = 30, justify = 'right')
			self.size_entry.insert(0, self.size_TEMP)
			self.size_entry.pack(side = 'right')
			size_frame.pack(fill = 'x')

			deldate_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['deldate'], font = self.gui.bold_font, side = 'left', master = deldate_frame)
			ttk.Button(deldate_frame, text = self.gui.lang['edit'], command = self.datetime_editor).pack(side = 'right')
			self.gui.draw_label(deldate_TEMP_str, side = 'right', master = deldate_frame)
			deldate_frame.pack(fill = 'x')

			version_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['itemedit_version'], font = self.gui.bold_font, side = 'left', master = version_frame)
			self.version_entry = ttk.Entry(version_frame, width = 30, justify = 'right')
			self.version_entry.insert(0, self.version_TEMP)
			self.version_entry.pack(side = 'right')
			version_frame.pack(fill = 'x')

			self.gui.window.mainloop()

	def set_return(self): self.item_maker(True, self.version_entry.get(), self.ogname_entry.get(), self.oglocation_entry.get(), self.is_folder_TEMP.get(), self.size_entry.get(), self.deldate_TEMP)

	def datetime_editor(self): self.gui.n_a()

	def validate_text(self, text, blacklist):
		for char in text:
			if char in blacklist: return False
			else: return True

	def discard(self, delete_window = False):
		if tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_discard_item'], icon = 'warning', default = 'no'):
			self.discarded = True
			if delete_window: sys.exit()
			else: self.end()

	def end(self):
		self.gui.window.protocol('WM_DELETE_WINDOW', self.gui.quit)
		self.gui.refresh(True)

# 99% of code copied from Sneky
class Updater:
	def __init__(self):
		self.username, self.reponame = username, repo_name
		self.request_limit = 5

	def check_internet(self):
		try:
			requests.get('https://google.com')
			return True
		except Exception: return False

	def check_updates(self, prerelease):
		if not self.check_internet():
			return {
			'newupdate': False,
			'error': True,
			'exceeded': False,
			'nowifi': True
			}
		try:
			versions = []
			if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
			
			for i in range(self.request_limit):
				try:
					response = requests.get(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases')
					break
				except Exception:
					if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

			for info in response.json(): versions.append(info['tag_name'])

			if internal_version not in versions:
				try:
					testvar = response.json()['message']
					if 'API rate limit exceeded for' in testvar:
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else: return {'newupdate': False, 'error': False}
				except Exception: return {'newupdate': False, 'error': False}
			if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

			for i in range(self.request_limit):
				try:
					response = requests.get(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/tags/{internal_version}')
					break
				except Exception:
					if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
			try:
				testvar = response.json()['message']
				if 'API rate limit exceeded for' in testvar:
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else: return {'newupdate': False, 'error': False}
			except Exception: pass
			currvertime = response.json()['published_at']
			if not prerelease:
				if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

				for i in range(self.request_limit):
					try:
						response = requests.get(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/latest')
						break
					except Exception:
						if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
				try:
					testvar = response.json()['message']
					if 'API rate limit exceeded for' in testvar:
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else: return {'newupdate': False, 'error': False}
				except Exception: pass
				if response.json()['tag_name'] != internal_version and response.json()['published_at'] > currvertime:
					return {
					'newupdate': True,
					'prerelease': False,
					'error': False,
					'title': response.json()['name'],
					'tag': response.json()['tag_name']
					}
				else:
					return {
					'newupdate': False,
					'unofficial': False,
					'error': False
					}
			else:
				for version in versions:
					if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

					for i in range(self.request_limit):
						try:
							response = requests.get(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/tags/{version}')
							break
						except:
							if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
					try:
						testvar = response.json()['message']
						if 'API rate limit exceeded for' in testvar:
							return {
							'newupdate': False,
							'error': True,
							'exceeded': True
							}
						else: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': False}
					except Exception: pass
					if currvertime < response.json()['published_at']:
						return {
						'newupdate': True,
						'prerelease': response.json()['prerelease'],
						'error': False,
						'title': response.json()['name'],
						'tag': response.json()['tag_name']
						}
					else:
						return {
						'newupdate': False,
						'unofficial': False,
						'error': False
						}
		except Exception:
			return {
			'newupdate': False,
			'error': True,
			'exceeded': False,
			'nowifi': False
			}

# https://stackoverflow.com/a/22325767
class OSVERSIONINFOEXW(ctypes.Structure):
    _fields_ = [('dwOSVersionInfoSize', ctypes.c_ulong),
                ('dwMajorVersion', ctypes.c_ulong),
                ('dwMinorVersion', ctypes.c_ulong),
                ('dwBuildNumber', ctypes.c_ulong),
                ('dwPlatformId', ctypes.c_ulong),
                ('szCSDVersion', ctypes.c_wchar*128),
                ('wServicePackMajor', ctypes.c_ushort),
                ('wServicePackMinor', ctypes.c_ushort),
                ('wSuiteMask', ctypes.c_ushort),
                ('wProductType', ctypes.c_byte),
                ('wReserved', ctypes.c_byte)]

# https://stackoverflow.com/a/16198198
class VerticalScrolledFrame(tk.Frame):
	def __init__(self, parent, *args, **kw):
		tk.Frame.__init__(self, parent, *args, **kw)

		vscrollbar = tk.Scrollbar(self, orient = 'vertical')
		vscrollbar.pack(fill = 'y', side = 'right')
		canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
		canvas.pack(side = 'left', fill = 'both', expand = True)
		vscrollbar.config(command = canvas.yview)

		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		self.interior = interior = tk.Frame(canvas)
		interior_id = canvas.create_window(0, 0, window = interior, anchor = 'nw')

		def _configure_interior(event):
			size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
			canvas.config(scrollregion = '0 0 %s %s' % size)
			if interior.winfo_reqwidth() != canvas.winfo_width():
				canvas.config(width=interior.winfo_reqwidth())
		interior.bind('<Configure>', _configure_interior)

		def _configure_canvas(event):
			if interior.winfo_reqwidth() != canvas.winfo_width():
				canvas.itemconfigure(interior_id, width=canvas.winfo_width())
		canvas.bind('<Configure>', _configure_canvas)