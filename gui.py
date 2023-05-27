import sys
if __name__ == '__main__':
	print('Please run main.py to start the program!')
	sys.exit()

import os
import platform
import traceback
import tkinter as tk
from tkinter import ttk
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
import glob
import math
import time
import json
import ctypes
import locale
import random
import shutil
import string
import getpass
import binascii
import tempfile
import winsound
import threading
import win32file
import subprocess
import webbrowser
import collections
import configparser
import urllib.request
from queue import Queue
from decimal import Decimal
from datetime import datetime, timedelta, timezone

import winreg
from winreg import HKEY_CLASSES_ROOT as HKCR
from winreg import HKEY_CURRENT_USER as HKCU

name = 'RBEditor'

username = 'gamingwithevets'
repo_name = 'rbeditor'

version = '1.0.0-dev3.1'
internal_version = 'v1.0.0-dev3.1'
prerelease = True

license = 'MIT'

try: import lang
except ImportError:
	err_text = f'Whoops! The script "lang.py" is required.\nCan you make sure the script is in "{temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
	print(err_text)
	tk.messagebox.showerror('Hmmm?', err_text)
	sys.exit()

def report_error(self = None, exc = None, val = None, tb = None, term = True):
	try: GUI.window.quit()
	except AttributeError: pass

	e = traceback.format_exc()
	err_text = f'Whoops! An error has occurred.\n\n{e}\nIf this error persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'

	print(err_text)
	tk.messagebox.showerror('Whoops!', err_text)
	if term: sys.exit()

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

		self.gui.sid = sid

		self.rbdir = self.gui.rbdir = f'\\$RECYCLE.BIN\\{sid}'
		self.rbdir_c = f'\\$Recycle.Bin\\{sid}'

	def get_bin_items(self):
		drives = self.get_drives()
		self.gui.corrupted_rbdir_drives = []
		bin_items_list = []
		dirlist = []
		errno_whitelist = [13, 2]
		for drive in drives:
			try: dirlist.extend(glob.glob(f'{drive}:{self.rbdir}\\*'))
			except IOError as e:
				if e.errno not in errno_whitelist: self.gui.corrupted_rbdir_drives.append(drive)

		bin_paths = {}
		for f in dirlist:
			if os.path.basename(f)[:2] == '$I' and os.path.exists(f'{os.path.dirname(f)}\\$R{os.path.basename(f)[2:]}'):
				bin_items_list.append(os.path.basename(f)[2:])
				bin_paths[os.path.basename(f)[2:]] = os.path.dirname(f)

		self.gui.bin_items = {}
		bin_items_unsorted = {}
		for item in bin_items_list:
			filedata = self.read_metadata(f'{bin_paths[item]}\\$I{item}')
			if filedata['skip']:
				self.gui.enable_rbin_metadata_unsupported_version_msg = True
				continue

			try: dirtest = os.path.isdir(f'{bin_paths[item]}\\$R{item}')
			except: dirtest = False

			ext = os.path.splitext(filedata['fname'])[1].lower()

			bin_items_unsorted[item] = {
			'ogpath': filedata['fname'],
			'unterminated_str': filedata['unterminated_str'],
			'type': self.gui.lang['ftype_desc_folder'] if dirtest else self.get_ftype_desc(ext),
			'ext': None if dirtest or not ext else ext,
			'isdir': dirtest,
			'size': filedata['fsize'],
			'deldate': filedata['deldate'],
			'rbin_drive': bin_paths[item][0],
			'version': filedata['version'],
			}

		if len(bin_items_unsorted) > 0:
			if self.gui.sort_method == 'natsort':
				if self.gui.folders_first: self.gui.bin_items = dict(collections.OrderedDict((k, bin_items_unsorted[k]) for k in natsorted(bin_items_unsorted.keys(), alg=ns.N | ns.P | ns.IC, key=lambda x: (not bin_items_unsorted[x]['isdir'], os.path.basename(bin_items_unsorted[x]['ogpath'].lower())))))
				else: self.gui.bin_items = dict(collections.OrderedDict((k, bin_items_unsorted[k]) for k in natsorted(bin_items_unsorted.keys(), alg=ns.N | ns.P | ns.IC, key=lambda x: os.path.basename(bin_items_unsorted[x]['ogpath'].lower()))))
			# fallback
			else:
				if self.gui.folders_first: self.gui.bin_items = dict(collections.OrderedDict(sorted(bin_items_unsorted.items(), key=lambda x: (not x[1]['isdir'], os.path.basename(x[1]['ogpath'].lower())))))
				else: self.gui.bin_items = dict(collections.OrderedDict(sorted(bin_items_unsorted.items(), key = lambda x: os.path.basename(x[1]['ogpath'].lower()))))

	def get_md_version(self, version): return f'{self.gui.lang["itemproperties_version_text"]}{version}'

	def get_ftype_desc(self, ext):
		if not ext: return self.gui.lang['ftype_desc_file']
		# translations for these extensions are stored in the language packs themselves,
		# therefore the file type descriptions also need to be stored in the program itself.
		elif ext == '.txt': return self.gui.lang['ftype_desc_txt']
		elif ext == '.ini': return self.gui.lang['ftype_desc_ini']
		elif ext == '.ps1': return self.gui.lang['ftype_desc_ps1']
		elif ext == '.ico': return self.gui.lang['ftype_desc_ico']
		else:
			try:
				desc = winreg.QueryValue(HKCR, winreg.QueryValue(HKCR, ext))
				if desc: return desc
				else: return self.gui.lang['ftype_desc_file_space'].format(ext[1:].upper())
			except: return self.gui.lang['ftype_desc_file_space'].format(ext[1:].upper())

	# https://stackoverflow.com/a/22325767 (modified)
	@staticmethod
	def get_os_version():
		os_version = OSVERSIONINFOEXW()
		os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
		retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))
		if retcode != 0:
			raise RuntimeError('Failed to get Windows NT version')

		return os_version.dwMajorVersion, os_version.dwMinorVersion

	@staticmethod
	def get_drives():
		drives = []
		for drive in string.ascii_uppercase:
			if win32file.GetDriveType(drive+':') == win32file.DRIVE_FIXED: drives.append(drive)

		return drives

	def filetime_to_dt(self, ft):
		time_utc = datetime(1970, 1, 1) + timedelta(microseconds = (ft - 116444736000000000) // 10)
		time_utc = time_utc.replace(tzinfo = timezone.utc)
		return time_utc.astimezone(self.gui.tz)

	@staticmethod
	def dt_to_filetime(dt):
		ft = 116444736000000000 + int((dt - datetime(1970, 1, 1, tzinfo = timezone.utc)).total_seconds() * 10000000)
		return ft

	def convert_size(self, size_bytes, extras = True):
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
			size_names_pow2 = tuple(self.gui.lang[_] for _ in ('KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'))
			i_pow2 = int(math.floor(math.log(size_bytes, 1024)))
			s_pow2_notstr = size_bytes / math.pow(1024, i_pow2)

			size_names_pow10 = tuple(self.gui.lang[_] for _ in ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'))
			i_pow10 = int(math.floor(math.log(size_bytes, 1000)))
			s_pow10_notstr = size_bytes / math.pow(1000, i_pow10)

			s_pow2 = add_digits(i_pow2, s_pow2_notstr)
			s_pow10 = add_digits(i_pow10, s_pow10_notstr)

			if i_pow10 == 0: return f'{size_bytes:n} {self.gui.lang["bytes"]}'
			else:
				if i_pow2 == 0:
					string = f'{print_size(i_pow10, s_pow10, s_pow10_notstr, size_names_pow10, 1000)}'
					if extras: string += f' ({size_bytes:n} {self.gui.lang["bytes"]})'
				else:
					string = f'{print_size(i_pow2, s_pow2, s_pow2_notstr, size_names_pow2, 1024)}'
					if extras: string += f' ({print_size(i_pow10, s_pow10, s_pow10_notstr, size_names_pow10, 1000)} - {size_bytes:n} {self.gui.lang["bytes"]})'
		else: string = f'{size_bytes} {self.gui.lang["bytes"]}'

		return string

	def read_metadata(self, file_path):
		file_to_read = os.path.basename(file_path)

		# initialization
		fname = fsize = deldate = version = None
		unterminated_str = False
		skip = False

		bytes_required = 20

		# avoid errors with empty/fake metadata files
		if os.path.getsize(file_path) < bytes_required:
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'$I{file_to_read}{self.gui.lang["msgbox_error_invalid_metadata"]}')
			skip = True
		else:
			file = open(file_path, 'rb')

			version_b = bytearray(file.read(8))
			version = int.from_bytes(version_b, 'little')
			if version == 2:
				try:
					fsize_b = bytearray(file.read(8))
					fsize_u = int.from_bytes(fsize_b, 'little')
					fsize = fsize_u if fsize_u < (1 << 64 - 1) else fsize_u - (1 << 64)
					deldate_b = bytearray(file.read(8))
					deldate = self.filetime_to_dt(int.from_bytes(deldate_b, 'little'))
					fnamelen_b = bytearray(file.read(4))
					fnamelen = int.from_bytes(fnamelen_b, 'little')

					fname = ''
					fname_raw_b = file.read()
					fname_raw = fname_raw_b.decode('utf-16le')
					for char in fname_raw:
						if char == '\x00': break
						fname += char
					if len(fname) != fnamelen - 1 and fnamelen > 0: unterminated_str = True
				except:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'Error in metadata v2 read operation, file {file_to_read}, drive {os.path.splitdrive(file_path)[0]}\n{traceback.format_exc()}')
					skip = True
					self.gui.enable_rbin_metadata_unsupported_version_msg = True

			elif version == 1:
				try:
					fsize_b = bytearray(file.read(8))
					fsize_u = int.from_bytes(fsize_b, 'little')
					fsize = fsize_u if fsize_u < (1 << 64 - 1) else fsize_u - (1 << 64)
					deldate_b = bytearray(file.read(8))
					deldate = self.filetime_to_dt(int.from_bytes(deldate_b, 'little'))

					fname = ''
					fname_raw_b = file.read()
					fname_raw = fname_raw_b.decode('utf-16le')
					for char in fname_raw:
						if char == '\x00': break
						fname += char
				except:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'Error in metadata v1 read operation, file {file_to_read}, drive {os.path.splitdrive(file_path)[0]}\n{traceback.format_exc()}')
					skip = True
					self.gui.enable_rbin_metadata_unsupported_version_msg = True
			else:
				self.gui.enable_rbin_metadata_unsupported_version_msg = True
				skip = True
				tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{file_to_read}{self.gui.lang["msgbox_error_unsupported_version"]} (v{version})')

		return {'fname': fname, 'fsize': fsize, 'deldate': deldate, 'version': version, 'unterminated_str': unterminated_str, 'skip': skip}

	def write_metadata(self, version, fname, fsize, deldate, is_folder, terminator = True):
		file_data = b''

		file_data += version.to_bytes(8, 'little')
		if version == 2:
			file_data += fsize.to_bytes(8, 'little')
			file_data += self.dt_to_filetime(deldate).to_bytes(8, 'little')
			fnamelen = len(fname)
			fname += '\x00'
			if terminator: fnamelen += 1
			file_data += fnamelen.to_bytes(4, 'little')
			fname_b = fname.encode('utf-16le')
			file_data += fname_b
		elif version == 1:
			file_data += fsize.to_bytes(8, 'little')
			file_data += self.dt_to_filetime(deldate).to_bytes(8, 'little')
			fnamelen = len(fname)
			fname_b = fname.encode('utf-16le')
			file_data += fname_b
			for i in range(260 - fnamelen): file_data += b'\x00\x00'

		return file_data

	def get_rb_path(self, item, typ = 'I'):
		drive = self.gui.bin_items[item]['rbin_drive']

		return f'{drive}:{self.rbdir_c if drive == os.getenv("SYSTEMDRIVE")[0] else self.rbdir}\\${typ}{item}'

	def get_rb_path_friendly(self, item):
		fpath = os.path.dirname(self.get_rb_path(item))
		drive = fpath[:2]

		return f'{self.gui.lang["rbin_in"].format(self.unicode_filter(drive))} | {self.unicode_filter(fpath)}'

	def unicode_filter(self, string):
		return ''.join(['□' if ord(c) > 0xFFFF else c for c in string]) if self.gui.unsupported_tcl else string

	def format_date(self, date, fm = None): 
		if fm == None: fm = self.gui.date_format
		return date.strftime(fm.encode('unicode-escape').decode()).encode().decode('unicode-escape')

	def get_all_childrens(self, w):
		widgets = w.winfo_children()
		for w in widgets: widgets += self.get_all_childrens(w)

		return widgets

class GUI:
	def __init__(self, window):
		self.version = version

		try:
			global natsorted, ns
			from natsort import natsorted, ns
			self.enable_natural_sort = True
		except ImportError: self.enable_natural_sort = False

		self.window = window

		self.temp_path = temp_path

		self.display_w = 800
		self.display_h = 600

		self.dt_win_open = False
		self.updater_win_open = False
		self.locale_chooser_open = False
		self.dt_picker_open = False

		tk_font = tk.font.nametofont('TkDefaultFont')

		self.bold_font = tk_font.copy()
		self.bold_font.config(weight = 'bold')
		self.underline_font = tk_font.copy()
		self.underline_font.config(underline = True)

		self.init_window()
		self.init_protocols()

		# default settings

		self.rbin_view_default = 'felike'
		self.rbin_view_tk = tk.StringVar(); self.rbin_view_tk.set(self.rbin_view_default)
		self.rbin_view = self.rbin_view_tk.get()
		self.rbin_view_options = ['felike', 'legacy']

		self.sort_method_default = 'lexico'
		self.sort_method_tk = tk.StringVar()
		if self.enable_natural_sort: self.sort_method_tk.set('natsort')
		else: self.sort_method_tk.set(self.sort_method_default)
		self.sort_method = self.sort_method_tk.get()
		self.sort_method_options = ['natsort', 'lexico']

		self.folders_first_tk = tk.BooleanVar(); self.folders_first_tk.set(False)
		self.folders_first = self.folders_first_tk.get()

		self.default_date_format = '%c'
		self.date_format = self.default_date_format
		self.tz = datetime.now(timezone.utc).astimezone().tzinfo

		self.languages = {
		'en': 'English',
		'fr': 'Français',
		'ja': '日本語',
		'vi': 'Tiếng Việt',
		}

		self.language_fallback_locales = {
		'en': 'en-US',
		'fr': 'fr-FR',
		'ja': 'ja-JP',
		'vi': 'vi-VN',
		}

		self.language_tk = tk.StringVar(); self.language_tk.set('system')
		self.language = ''
		self.system_language_unavailable = False

		self.locales = [
		'af',
		'af-ZA',
		'ar',
		'ar-AE',
		'ar-BH',
		'ar-DZ',
		'ar-EG',
		'ar-IQ',
		'ar-JO',
		'ar-KW',
		'ar-LB',
		'ar-LY',
		'ar-MA',
		'ar-OM',
		'ar-QA',
		'ar-SA',
		'ar-SY',
		'ar-TN',
		'ar-YE',
		'az',
		'az-AZ',
		'az-AZ',
		'be',
		'be-BY',
		'bg',
		'bg-BG',
		'bs-BA',
		'ca',
		'ca-ES',
		'cs',
		'cs-CZ',
		'cy',
		'cy-GB',
		'da',
		'da-DK',
		'de',
		'de-AT',
		'de-CH',
		'de-DE',
		'de-LI',
		'de-LU',
		'dv',
		'dv-MV',
		'el',
		'el-GR',
		'en',
		'en-AU',
		'en-BZ',
		'en-CA',
		'en-CB',
		'en-GB',
		'en-IE',
		'en-JM',
		'en-NZ',
		'en-PH',
		'en-TT',
		'en-US',
		'en-ZA',
		'en-ZW',
		'eo',
		'es',
		'es-AR',
		'es-BO',
		'es-CL',
		'es-CO',
		'es-CR',
		'es-DO',
		'es-EC',
		'es-ES',
		'es-ES',
		'es-GT',
		'es-HN',
		'es-MX',
		'es-NI',
		'es-PA',
		'es-PE',
		'es-PR',
		'es-PY',
		'es-SV',
		'es-UY',
		'es-VE',
		'et',
		'et-EE',
		'eu',
		'eu-ES',
		'fa',
		'fa-IR',
		'fi',
		'fi-FI',
		'fo',
		'fo-FO',
		'fr',
		'fr-BE',
		'fr-CA',
		'fr-CH',
		'fr-FR',
		'fr-LU',
		'fr-MC',
		'gl',
		'gl-ES',
		'gu',
		'gu-IN',
		'he',
		'he-IL',
		'hi',
		'hi-IN',
		'hr',
		'hr-BA',
		'hr-HR',
		'hu',
		'hu-HU',
		'hy',
		'hy-AM',
		'id',
		'id-ID',
		'is',
		'is-IS',
		'it',
		'it-CH',
		'it-IT',
		'ja',
		'ja-JP',
		'ka',
		'ka-GE',
		'kk',
		'kk-KZ',
		'kn',
		'kn-IN',
		'ko',
		'ko-KR',
		'kok',
		'kok-IN',
		'ky',
		'ky-KG',
		'lt',
		'lt-LT',
		'lv',
		'lv-LV',
		'mi',
		'mi-NZ',
		'mk',
		'mk-MK',
		'mn',
		'mn-MN',
		'mr',
		'mr-IN',
		'ms',
		'ms-BN',
		'ms-MY',
		'mt',
		'mt-MT',
		'nb',
		'nb-NO',
		'nl',
		'nl-BE',
		'nl-NL',
		'nn-NO',
		'ns',
		'ns-ZA',
		'pa',
		'pa-IN',
		'pl',
		'pl-PL',
		'ps',
		'ps-AR',
		'pt',
		'pt-BR',
		'pt-PT',
		'qu',
		'qu-BO',
		'qu-EC',
		'qu-PE',
		'ro',
		'ro-RO',
		'ru',
		'ru-RU',
		'sa',
		'sa-IN',
		'se',
		'se-FI',
		'se-FI',
		'se-FI',
		'se-NO',
		'se-NO',
		'se-NO',
		'se-SE',
		'se-SE',
		'se-SE',
		'sk',
		'sk-SK',
		'sl',
		'sl-SI',
		'sq',
		'sq-AL',
		'sr-BA',
		'sr-BA',
		'sr-SP',
		'sr-SP',
		'sv',
		'sv-FI',
		'sv-SE',
		'sw',
		'sw-KE',
		'syr',
		'syr-SY',
		'ta',
		'ta-IN',
		'te',
		'te-IN',
		'th',
		'th-TH',
		'tl',
		'tl-PH',
		'tn',
		'tn-ZA',
		'tr',
		'tr-TR',
		'tt',
		'tt-RU',
		'ts',
		'uk',
		'uk-UA',
		'ur',
		'ur-PK',
		'uz',
		'uz-UZ',
		'uz-UZ',
		'vi',
		'vi-VN',
		'xh',
		'xh-ZA',
		'zh',
		'zh-CN',
		'zh-HK',
		'zh-MO',
		'zh-SG',
		'zh-TW',
		'zu',
		'zu-ZA',
		]
		self.locale_default = 'en'
		try: locale.setlocale(locale.LC_ALL, 'en')
		except:
			for l in self.locales:
				if '-' not in l: self.locales.remove(l)
			self.locale_default = 'en-US'

		self.locale_tk = tk.StringVar(); self.locale_tk.set(self.locale_default)
		self.locale = self.locale_tk.get()
		self.locale_option = tk.StringVar(); self.locale_option.set('lang')

		self.auto_check_updates = tk.BooleanVar(); self.auto_check_updates.set(True)
		self.check_prerelease_version = tk.BooleanVar(); self.check_prerelease_version.set(False)

		self.enable_rbin_metadata_unsupported_version_msg = False

		self.appdata_folder = f'{os.getenv("LOCALAPPDATA")}\\{name}'
		self.ini = configparser.ConfigParser()
		self.parse_settings()

		self.refreshing = True
		self.reload_confirm_func = self.reload_confirm_default

		self.context_menu_open = False

		self.rbhandler = RBHandler(self)
		self.itemproperties = ItemProperties(self)
		self.dt_menu = DTMenu(self)
		self.new_item = NewItem(self)
		self.locale_chooser = LocaleChooser(self)
		self.updater_gui = UpdaterGUI(self)

		self.unsupported_tcl = False
		if sys.version_info < (3, 7, 6):
			if tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_unsupported_tcl'].format(platform.python_version()), icon = 'warning'): self.unsupported_tcl = True
			else: self.quit()

		self.rbhandler.get_rbdir()
		self.menubar()

	def start_main(self):
		if self.auto_check_updates.get(): self.updater_gui.init_window(True)
		self.main()

	def parse_settings(self):
		self.save_to_cwd = False

		# load override settings
		if os.path.exists(os.path.join(os.getcwd(), 'settings.ini')):
			self.ini.read('settings.ini')
			self.save_to_cwd = True
		# load normal settings
		else: self.ini.read(f'{self.appdata_folder}\\settings.ini')

		sects = self.ini.sections()
		if sects:
			if 'settings' in sects:
				try: self.language_tk.set(self.ini['settings']['language'].replace('_', '-'))
				except: pass
				try:
					self.locale_tk.set(self.ini['settings']['locale'])
					if self.locale_tk.get() not in self.locales: self.locale_tk.set(self.locale_default)
					self.locale = self.locale_tk.get()
				except: pass
				try:
					self.locale_option.set(self.ini['settings']['locale_option'])
					if self.locale_option.get() not in ['lang', 'system', 'custom']: self.locale_option.set('lang')
					self.prev_locale_option = self.locale_option.get()
				except: pass
				try: self.date_format = self.ini['settings']['date_format'].encode().decode('unicode-escape').replace('%%', '%')
				except: pass
				try:
					self.rbin_view_tk.set(self.ini['settings']['rbin_view'])
					if self.rbin_view_tk.get() not in self.rbin_view_options: self.rbin_view_tk.set(self.rbin_view_default)
					self.rbin_view = self.rbin_view_tk.get()
				except: pass
				try:
					self.sort_method_tk.set(self.ini['settings']['sort_method'])
					if self.sort_method_tk.get() == 'natsort' and not self.enable_natural_sort: self.sort_method_tk.set(self.sort_method_default)
					elif self.sort_method_tk.get() not in self.sort_method_options:
						if self.enable_natural_sort: self.sort_method_tk.set('natsort')
						else: self.sort_method_tk.set(self.sort_method_default)
					self.sort_method = self.sort_method_tk.get()
				except: pass
				try:
					self.folders_first_tk.set(self.ini.getboolean('settings', 'folders_first'))
					self.folders_first = self.folders_first_tk.get()
				except: pass

			if 'updater' in sects:
				try: self.auto_check_updates.set(self.ini.getboolean('updater', 'auto_check_updates'))
				except: pass
				try: self.check_prerelease_version.set(self.ini.getboolean('updater', 'check_prerelease_version'))
				except: pass

		self.set_lang()
		self.set_locale()
		self.save_settings()

	def save_settings(self):
		# settings are set individually to retain compatibility between versions
		self.ini['settings'] = {}
		self.ini['settings']['language'] = self.language_tk.get()
		self.ini['settings']['locale'] = self.locale_tk.get()
		self.ini['settings']['locale_option'] = self.locale_option.get()
		self.ini['settings']['date_format'] = self.date_format.replace('%', '%%').encode('unicode-escape').decode()
		self.ini['settings']['rbin_view'] = self.rbin_view_tk.get()
		self.ini['settings']['sort_method'] = self.sort_method_tk.get()
		self.ini['settings']['folders_first'] = str(self.folders_first_tk.get())

		self.ini['updater'] = {}
		self.ini['updater']['auto_check_updates'] = str(self.auto_check_updates.get())
		self.ini['updater']['check_prerelease_version'] = str(self.check_prerelease_version.get())

		if self.save_to_cwd:
			with open(os.path.join(os.getcwd(), 'settings.ini'), 'w') as f: self.ini.write(f)

		if not os.path.exists(self.appdata_folder): os.makedirs(self.appdata_folder)
		with open(f'{self.appdata_folder}\\settings.ini', 'w') as f: self.ini.write(f)

	def get_lang(self):
		slang = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
		if slang[:2] in self.languages: return slang[:2]
		else:
			self.system_language_unavailable = True
			return 'en'

	def set_lang(self, change = False):
		if self.language_tk.get() == 'system':
			self.language = self.get_lang()
			if self.system_language_unavailable:
				self.language_tk.set('en')
				tk.messagebox.showwarning('Warning', f'Your system language is not available in this version of {name}.\n\n{name}\'s language has been set to English.')
		else:
			self.language = self.language_tk.get()
			if self.language_tk.get() not in self.languages:
				self.language_tk.set('en')
				self.save_settings()

		if not change:
			self.lang = lang.lang['en'].copy()
			if self.language in lang.lang:
				lang_new = lang.lang[self.language].copy()
				for key in lang_new: self.lang[key] = lang_new[key]

	def set_locale(self):
		lo = self.locale_option.get()
		if lo == 'lang':
			try: locale.setlocale(locale.LC_ALL, self.language)
			except: locale.setlocale(locale.LC_ALL, self.language_fallback_locales[self.language])
		elif lo == 'system': locale.setlocale(locale.LC_ALL, '')
		elif lo == 'custom': locale.setlocale(locale.LC_ALL, self.locale)

	def set_prev_locale_option(self):
		self.prev_locale_option = self.locale_option.get()
		self.setting_change()

	def change_lang(self):
		self.set_lang(True)
		self.setting_change()

	def n_a(self): tk.messagebox.showinfo(self.lang['msgbox_n_a'], self.lang['msgbox_n_a_desc'].format(name))

	def refresh(self, load_func = False):
		self.refreshing = True

		for w in self.window.winfo_children(): w.destroy()
		self.menubar()

		self.window.protocol('WM_DELETE_WINDOW', self.quit)
		self.reload_confirm_func = self.reload_confirm_default

		if load_func: self.main()

	def set_title(self, custom_str = None): self.window.title(f'{name} {version}{" - " + custom_str if custom_str != None else ""}')

	# no tab! (sorry keyboard users...)
	@staticmethod
	def disable_all_widgets():
		def set_takefocus_false(widget_class):
			orig_init = widget_class.__init__
			def new_init(self, *args, **kwargs):
				orig_init(self, *args, **kwargs)
				self.config(takefocus = False)
			widget_class.__init__ = new_init

		set_takefocus_false(tk.Widget)
		set_takefocus_false(ttk.Widget)

	def init_window(self):
		self.window.geometry(f'{self.display_w}x{self.display_h}')
		self.window.resizable(False, False)
		self.window.bind('<F5>', self.reload_confirm)
		self.window.bind('<F12>', self.version_details)
		self.window.bind('<Button-3>', self.playsound)
		self.window.option_add('*tearOff', False)
		
		self.disable_all_widgets()

		self.set_title()
		try: self.window.iconbitmap(f'{self.temp_path}\\icon.ico')
		except tk.TclError:
			err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
			print(err_text)
			tk.messagebox.showerror('Hmmm?', err_text)
			sys.exit()

	def init_protocols(self):
		self.window.protocol('WM_DELETE_WINDOW', self.quit)

	def quit(self):
		if not any([
			self.dt_win_open,
			self.updater_win_open,
			self.locale_chooser_open,
			self.dt_picker_open,
			]): sys.exit()

	def playsound(self, event):
		if self.context_menu_open: self.context_menu_open = False
		else: winsound.PlaySound('.Default', winsound.SND_ASYNC)

	def draw_label(self, text, font = None, color = 'black', bg = None, side = 'top', anchor = 'center', recwidth = None, recheight = None, justify = None, master = None):
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
		text = ttk.Label(master, text = text, font = font, foreground = color, background = bg, width = recwidth, height = recheight, justify = justify, anchor = anc)
		text.pack(side = side, anchor = anc)

	def draw_blank(self, side = 'top', master = None):
		if master == None: master = self.window
		self.draw_label('', side = side, master = master)

	def about_menu(self):
		syst = platform.system(); syst += ' x64' if platform.machine().endswith('64') else ' x86'
		tk.messagebox.showinfo(self.lang['menubar_help_about'].format(name), f'''\
{name} - {version} ({'64' if sys.maxsize > 2**31-1 else '32'}-bit) - {self.lang['about_running_on'].format(syst)}
{self.lang['about_project_page']}https://github.com/{username}/{repo_name}
{self.lang['about_beta_build'] if prerelease else ''}
{self.lang['about_licensed'].format(license)}

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

	def version_details(self, event = None):
		dnl = '\n\n'
		tk.messagebox.showinfo(f'{name} version details', f'''\
{name} {version}{" (prerelease)" if prerelease else ""}
Internal version: {internal_version}

Python version information:
Python {platform.python_version()} ({'64' if sys.maxsize > 2**31-1 else '32'}-bit)
Tkinter (Tcl/Tk) version {self.window.tk.call('info', 'patchlevel')}{" (most Unicode chars not supported)" if self.unsupported_tcl else ""}

Operating system information:
{platform.system()} {platform.release()}
{'NT version: ' if os.name == 'nt' else ''}{platform.version()}
Architecture: {platform.machine()}{dnl+"Settings file is saved to working directory" if self.save_to_cwd else ""}\
''')

	def reload(self):
		self.itemproperties.show_advanced = False
		self.refresh(True)

	def reload_confirm(self, event = None):
		if self.reload_confirm_func(): self.reload()

	def reload_confirm_default(self): return tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_reload_confirm'], icon = 'warning')

	def setting_change(self):
		self.save_settings()
		self.menubar() # update the menubar
		tk.messagebox.showinfo(self.lang['msgbox_notice'], self.lang['msgbox_reload_next_reboot'])

	def menubar(self):
		menubar = tk.Menu()

		rbin_menu = tk.Menu(menubar)
		rbin_menu.add_command(label = self.lang['menubar_rbin_sid'] + self.sid, state = 'disabled')
		rbin_menu.add_separator()
		rbin_menu.add_command(label = self.lang['menubar_rbin_reload'], command = self.reload_confirm, accelerator = 'F5')
		rbin_menu.add_command(label = self.lang['menubar_rbin_explorer_bin'], command = lambda: subprocess.Popen('explorer shell:recyclebinfolder', shell = True))
		rbin_menu.add_separator()
		rbin_menu.add_command(label = self.lang['menubar_rbin_exit'], command = self.quit)
		menubar.add_cascade(label = 'RBEditor', menu = rbin_menu)

		settings_menu = tk.Menu(menubar)

		rbin_view_menu =  tk.Menu(menubar)
		for i in self.rbin_view_options: rbin_view_menu.add_radiobutton(label = self.lang[f'menubar_settings_rbin_view_{i}'], variable = self.rbin_view_tk, value = i, command = self.setting_change)
		settings_menu.add_cascade(label = self.lang['menubar_settings_rbin_view'], menu = rbin_view_menu)

		sort_method_menu =  tk.Menu(menubar)
		for i in self.sort_method_options: sort_method_menu.add_radiobutton(label = self.lang[f'menubar_settings_sort_method_{i}'], variable = self.sort_method_tk, value = i, command = self.setting_change, state = 'disabled' if i == 'natsort' and not self.enable_natural_sort else 'normal')
		sort_method_menu.add_separator()
		sort_method_menu.add_checkbutton(label = self.lang['menubar_settings_sort_method_folders_first'], variable = self.folders_first_tk, command = self.setting_change)
		settings_menu.add_cascade(label = self.lang['menubar_settings_sort_method'], menu = sort_method_menu)
		
		settings_menu.add_separator()

		settings_menu.add_command(label = self.lang['menubar_settings_dtformat'], command = self.dt_menu.init_window)

		settings_menu.add_separator()

		self.lang_menu = tk.Menu(settings_menu)
		self.lang_menu.add_command(label = self.lang['menubar_settings_language_info'], command = lambda: tk.messagebox.showinfo(self.lang['menubar_help_about'].format(self.languages[self.language]), self.lang['info']))
		self.lang_menu.add_separator()
		self.lang_menu.add_radiobutton(label = self.lang['menubar_settings_language_system'], variable = self.language_tk, value = 'system', command = self.change_lang, state = 'disabled' if self.system_language_unavailable else 'normal')
		for i in self.languages: self.lang_menu.add_radiobutton(label = self.languages[i], variable = self.language_tk, value = i, command = self.change_lang)
		self.ena_dis_lang()
		settings_menu.add_cascade(label = self.lang['menubar_settings_language'], menu = self.lang_menu)

		locale_menu = tk.Menu(settings_menu)
		locale_menu.add_radiobutton(label = self.lang['menubar_settings_locale_lang'], variable = self.locale_option, value = 'lang', command = self.set_prev_locale_option)
		locale_menu.add_radiobutton(label = self.lang['menubar_settings_locale_system'], variable = self.locale_option, value = 'system', command = self.set_prev_locale_option)
		locale_menu.add_radiobutton(label = f'{self.lang["menubar_settings_locale_custom"]}{self.lang["menubar_settings_locale_custom2"].format(self.locale_tk.get()) if self.locale_option.get() == "custom" else ""}', variable = self.locale_option, value = 'custom', command = self.locale_chooser.init_window)
		settings_menu.add_cascade(label = self.lang['menubar_settings_locale'], menu = locale_menu)

		settings_menu.add_separator()

		updater_settings_menu = tk.Menu(settings_menu)
		updater_settings_menu.add_checkbutton(label = self.lang['menubar_settings_updates_auto'], variable = self.auto_check_updates, command = self.save_settings)
		updater_settings_menu.add_checkbutton(label = self.lang['menubar_settings_updates_prerelease'], variable = self.check_prerelease_version, command = self.save_settings)
		settings_menu.add_cascade(label = self.lang['menubar_settings_updates'], menu = updater_settings_menu)

		menubar.add_cascade(label = self.lang['menubar_settings'], menu = settings_menu)

		help_menu = tk.Menu(menubar)
		help_menu.add_command(label = self.lang['menubar_help_update'], command = self.updater_gui.init_window)
		help_menu.add_command(label = self.lang['menubar_help_about'].format(name), command = self.about_menu)
		menubar.add_cascade(label = self.lang['help'], menu = help_menu)

		self.window.config(menu = menubar)

	def ena_dis_lang(self):
		for i in self.languages:
			# try-except nest used in case of an unused language in language_names
			try: self.lang_menu.entryconfig(i, state = 'normal')
			except: pass

	def main(self):
		try: self.draw_label(self.lang['title'], font = self.bold_font)
		except: self.draw_label(self.lang['title'])
		self.draw_blank()

		loading_text = ttk.Label(text = self.lang['main_loading']); loading_text.pack()
		self.window.update()

		if self.refreshing:
			self.rbhandler.get_bin_items()
			self.refreshing = False

		loading_text.destroy()

		if self.enable_rbin_metadata_unsupported_version_msg:
			self.draw_label(self.lang['main_rbin_metadata_unsupported_version'])
			self.enable_rbin_metadata_unsupported_version_msg = False

		if len(self.corrupted_rbdir_drives) > 0:
			corrupted_text = f'{self.lang["main_warning"]}\n'
			for drive in self.corrupted_rbdir_drives: corrupted_text += f'{self.lang["main_rb_corrupt"].format(drive + ":")}\n'
			corrupted_text = corrupted_text[:-1]
			self.draw_label(corrupted_text)
			self.draw_blank()

		if len(self.bin_items) > 0:
			button_frame = tk.Frame()
			ttk.Button(button_frame, text = self.lang['main_new_item'], command = self.new_item.create_item).pack(side = 'left')
			ttk.Button(button_frame, text = self.lang['main_restore_all'], command = self.restore_all).pack(side = 'left')
			ttk.Button(button_frame, text = self.lang['main_empty_rb'], command = self.delete_all).pack(side = 'right')
			button_frame.pack()
			self.draw_blank()

			frame = VerticalScrolledFrame(self.window)
			frame.pack(fill = 'both', expand = True)

			if self.rbin_view == 'legacy':
				# copied over from v0.1.2 tag
				for item in self.bin_items:
					item_frame = tk.Frame(frame.interior)
					ttk.Button(item_frame, text = self.lang['main_properties'], command = lambda e = item: self.itemproperties.show_properties(e)).pack(side = 'right')
					ttk.Button(item_frame, text = self.lang['main_delete'], command = lambda e = item: self.delete_item(e)).pack(side = 'right')
					ttk.Button(item_frame, text = self.lang['main_restore'], command = lambda e = item: self.restore_item(e)).pack(side = 'right')
					ttk.Button(item_frame, text = self.lang['main_open'], command = lambda e = item: self.open_item(e)).pack(side = 'right')
					self.draw_label(f'{self.rbhandler.unicode_filter(os.path.basename(self.bin_items[item]["ogpath"]))}   {self.lang["main_folder"]}' if self.bin_items[item]['isdir'] else self.rbhandler.unicode_filter(os.path.basename(self.bin_items[item]["ogpath"])), side = 'left', anchor = 'midleft', master = item_frame)
					item_frame.pack(fill = 'both')			
			# fallback/default view
			else:
				for item in self.bin_items:
					item_frame = FExplorerFrame(frame.interior, self, item, f'{self.rbhandler.unicode_filter(os.path.basename(self.bin_items[item]["ogpath"]))}   {self.lang["main_folder"]}' if self.bin_items[item]['isdir'] else self.rbhandler.unicode_filter(os.path.basename(self.bin_items[item]["ogpath"])))
					item_frame.pack(fill = 'both')
		else:
			ttk.Button(text = self.lang['main_new_item'], command = self.new_item.create_item).pack()
			self.draw_blank()
			self.draw_label(self.lang['main_rbin_empty'])

		self.set_title()
		self.window.mainloop()

	def check_item_exist(self, item):
		if not os.path.exists(f'{self.bin_items[item]["rbin_drive"]}:{self.rbdir}\\$I{item}') or not os.path.exists(f'{self.bin_items[item]["rbin_drive"]}:{self.rbdir}\\$R{item}'):
			tk.messagebox.showerror(self.lang['msgbox_error'], self.lang['msgbox_not_in_rb'])
			self.refresh(True)

	def open_item(self, item):
		def start(path, folder = False):
			if folder: subprocess.Popen(f'explorer "{path}"', shell = True)
			else:
				try: os.startfile(path)
				except OSError as e: tk.messagebox.showerror(self.lang['msgbox_error'], f'Error in open operation:\n{e.strerror.replace("%1", e.filename)} ({e.errno})')

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
		ogname = os.path.basename(item_info['ogpath'])
		oglocation = os.path.dirname(item_info['ogpath'])
		item_type = item_info['type']
		size = item_info['size']
		deldate = self.rbhandler.format_date(item_info['deldate'])

		return f'{ogname}\n{self.lang["oglocation"]}: {oglocation}\n{self.lang["type"]}: {item_type}\n{self.lang["size"]}: {self.rbhandler.convert_size(size, False)}\n{self.lang["deldate"]}: {deldate}'

	def delete_item(self, item, no_prompt = False, no_refresh = False):		
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']

		path = f'{drive}:{self.rbdir}\\'

		if not no_prompt:
			if not tk.messagebox.askyesno(self.lang['msgbox_delete'], f'{self.lang["msgbox_delete_desc"]}\n\n{self.get_item_info_str(item)}', icon = 'warning', default = 'no'): return
		try: os.remove(f'{path}$I{item}')
		except OSError as e: tk.messagebox.showerror(self.lang['msgbox_error'], f'Error in delete operation:\n{e.filename}\n{e.strerror} ({e.errno})')

		if not no_refresh: self.refresh(True)

	def restore_item(self, item, no_prompt = False, no_refresh = False):
		self.check_item_exist(item)

		item_info = self.bin_items[item]
		drive = item_info['rbin_drive']
		ogpath = item_info['ogpath']
		ogname = os.path.basename(ogpath)
		oglocation = os.path.dirname(ogpath)

		path = f'{drive}:{self.rbdir}\\'
		if os.path.splitdrive(oglocation)[0] == '': restore_path = f'{os.getenv("USERPROFILE")}\\Desktop\\{ogpath}'
		else: restore_path = ogpath

		if not no_prompt:
			if not tk.messagebox.askyesno(self.lang['msgbox_restore'], f'{self.lang["msgbox_restore_desc"]}\n\n{self.get_item_info_str(item)}'): return

		if not os.path.exists(oglocation):
			try: os.makedirs(oglocation)
			except OSError as e:
				tk.messagebox.showerror(self.lang['msgbox_error'], f'Error in makedirs operation:\n{e.filename}\n{e.strerror} ({e.errno})')
				if no_refresh: return
				else: self.refresh(True)

		if os.path.exists(restore_path) and os.path.isdir(restore_path) == item_info['isdir']:
			if not tk.messagebox.askyesno(self.lang['msgbox_warning'], self.lang['msgbox_overwrite'].format(ogname), icon = 'warning'):
				if no_refresh: return
				else: self.refresh(True)

		try: shutil.move(f'{path}$R{item}', restore_path)
		except OSError as e:
			tk.messagebox.showerror(self.lang['msgbox_error'], f'Error in move operation:\n{e.filename}\n{e.strerror} ({e.errno})')
			if no_refresh: return
			else: self.refresh(True)

		try: os.remove(f'{path}$I{item}')
		except OSError as e: tk.messagebox.showerror(self.lang['msgbox_error'], f'Error in delete operation:\n{e.filename}\n{e.strerror} ({e.errno})')

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
		self.preview_date_time = datetime(2007, 1, 30, 12, 34, 56, 123456, tzinfo = timezone(timedelta(hours = 7)))

	def init_window(self):
		if not self.gui.dt_win_open:
			self.gui.dt_win_open = True
			self.dt_preview = False

			self.win = tk.Toplevel(self.gui.window)
			self.win.geometry('500x500')
			self.win.resizable(False, False)
			self.win.protocol('WM_DELETE_WINDOW', self.quit)
			self.win.title(self.gui.lang['title_dtformat'])
			try: self.win.iconbitmap(f'{self.gui.temp_path}\\icon.ico')
			except tk.TclError:
				err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.gui.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
				print(err_text)
				tk.messagebox.showerror('Hmmm?', err_text)
				sys.exit()

			self.draw_menu()

			self.win.focus()
			self.win.grab_set()
			self.win.mainloop()

	def quit(self):
		self.win.grab_release()
		self.win.destroy()
		self.gui.dt_win_open = False

	def discard(self):
		if self.get_dt_entry() != self.gui.date_format:
			if tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_discard'], icon = 'warning', default = 'no'): self.quit()
		else: self.quit()

	def preview(self):
		self.text = self.get_dt_entry()
		if self.text_check():
			self.dt_preview = True
			self.text = self.gui.rbhandler.unicode_filter(self.text)
			self.draw_menu()
		else: return

	def reset(self):
		self.text = self.gui.default_date_format
		self.draw_menu()

	def save(self):
		self.text = self.get_dt_entry() 
		if self.text_check():
			if self.gui.date_format != self.text:
				if self.gui.unsupported_tcl: tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_error_unicode'])
				else:
					self.gui.date_format = self.gui.rbhandler.unicode_filter(self.text)
					self.gui.save_settings()
					self.quit()
					self.gui.setting_change()
			else: self.quit()
		else: return

	def text_check(self):
		if self.text == '':
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_blank'])
			return False
		if '%' not in self.text:
			if not tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_no_formatting'], icon = 'warning'): return False

		return True

	def get_dt_entry(self):
		dt_entry = self.dt_entry.get()
		return dt_entry

	def help(self):
		tk.messagebox.showinfo(self.gui.lang['help'], self.gui.lang['dtformat_guide'])

	def draw_menu(self):
		for w in self.win.winfo_children(): w.destroy()

		self.gui.draw_label(self.gui.lang['title_dtformat'], font = self.gui.bold_font, master = self.win)
		self.gui.draw_blank(master = self.win)
		button_frame = tk.Frame(self.win); button_frame.pack(side = 'bottom')
		ttk.Button(button_frame, text = 'OK', command = self.save).pack(side = 'left')
		ttk.Button(button_frame, text = self.gui.lang['discard'], command = self.discard).pack(side = 'right')
		self.gui.draw_blank(side = 'bottom', master = self.win)
		ttk.Button(self.win, text = self.gui.lang['reset'], command = self.reset).pack(side = 'bottom')
		ttk.Button(self.win, text = self.gui.lang['preview'], command = self.preview).pack(side = 'bottom')

		self.gui.draw_label(self.gui.lang['dtformat'], master = self.win)

		scroll = ttk.Scrollbar(self.win, orient = 'horizontal')
		self.dt_entry = ttk.Entry(self.win, width = self.win.winfo_width(), justify = 'center', xscrollcommand = scroll.set)
		try: self.dt_entry.insert(0, self.gui.rbhandler.unicode_filter(self.text))
		except AttributeError: self.dt_entry.insert(0, self.gui.date_format)
		self.dt_entry.pack()
		scroll.config(command = self.dt_entry.xview)
		scroll.pack(fill = 'x')
		ttk.Button(self.win, text = self.gui.lang['help'], command = self.help).pack()

		if self.dt_preview:
			if self.gui.unsupported_tcl: tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_error_unicode'])
			# https://stackoverflow.com/a/49791321
			else: self.gui.draw_label(f'{self.gui.lang["dtformat_preview"]}\n{self.gui.rbhandler.format_date(self.preview_date_time, self.text)}', justify = 'center', master = self.win)


class ItemProperties:
	def __init__(self, gui):
		self.gui = gui

		self.draw_label = self.gui.draw_label
		self.draw_blank = self.gui.draw_blank
		self.bold_font = self.gui.bold_font

		self.refresh = self.gui.refresh

		self.show_advanced = False

	def show_properties(self, item):
		self.gui.check_item_exist(item)

		item_info = self.gui.bin_items[item]

		self.refresh()
		self.draw_label(self.gui.lang['itemproperties_properties'], font = self.bold_font)
		self.draw_blank()
		ttk.Button(text = self.gui.lang['back'], command = self.quit).pack(side = 'bottom')
		self.draw_blank(side = 'bottom')
		ttk.Button(text = self.gui.lang['edit'], command = lambda: self.gui.new_item.edit_item(item)).pack(side = 'bottom')

		ogname = os.path.basename(item_info['ogpath'])

		ogname_frame = tk.Frame()
		self.draw_label(self.gui.lang['itemproperties_ogname'], font = self.bold_font, side = 'left', master = ogname_frame)
		if item_info['unterminated_str'] and ogname != '': self.draw_label(self.gui.lang['itemproperties_ogname_unterminated'], side = 'left', master = ogname_frame)
		self.draw_label(self.gui.rbhandler.unicode_filter(ogname), side = 'right', master = ogname_frame)
		ogname_frame.pack(fill = 'x')

		oglocation_frame = tk.Frame()
		self.draw_label(self.gui.lang['oglocation'], font = self.bold_font, side = 'left', master = oglocation_frame)
		if item_info['unterminated_str'] and ogname == '': self.draw_label(self.gui.lang['itemproperties_ogname_unterminated'], side = 'left', master = oglocation_frame)
		self.draw_label('*', side = 'left', master = oglocation_frame)
		self.draw_label(self.gui.rbhandler.unicode_filter(os.path.dirname(item_info['ogpath'])), side = 'right', master = oglocation_frame)
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
		self.draw_label(self.gui.lang['itemproperties_size_disk'], font = self.bold_font, side = 'left', master = size_disk_frame)
		self.draw_label(self.gui.rbhandler.convert_size(os.path.getsize(self.gui.rbhandler.get_rb_path(item)) + os.path.getsize(self.gui.rbhandler.get_rb_path(item, 'R'))), side = 'right', master = size_disk_frame)
		size_disk_frame.pack(fill = 'x')

		deldate_frame = tk.Frame()
		self.draw_label(self.gui.lang['deldate'], font = self.bold_font, side = 'left', master = deldate_frame)
		self.draw_label(self.gui.rbhandler.unicode_filter(item_info['deldate'].strftime(self.gui.date_format.encode('unicode-escape').decode()).encode().decode('unicode-escape')), side = 'right', master = deldate_frame)
		deldate_frame.pack(fill = 'x')

		if self.show_advanced:
			itemname = self.gui.rbhandler.unicode_filter(item)

			self.draw_blank()

			rbin_name_i_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemproperties_rbin_name_i'], font = self.bold_font, side = 'left', master = rbin_name_i_frame)
			self.draw_label(f'$I{itemname}', side = 'right', master = rbin_name_i_frame)
			rbin_name_i_frame.pack(fill = 'x')

			rbin_name_r_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemproperties_rbin_name_r'], font = self.bold_font, side = 'left', master = rbin_name_r_frame)
			self.draw_label(f'$R{itemname}', side = 'right', master = rbin_name_r_frame)
			rbin_name_r_frame.pack(fill = 'x')

			rbin_location_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemproperties_rbin_location'], font = self.bold_font, side = 'left', master = rbin_location_frame)
			self.draw_label('**', side = 'left', master = rbin_location_frame)
			self.draw_label(self.gui.rbhandler.get_rb_path_friendly(item), side = 'right', master = rbin_location_frame)
			rbin_location_frame.pack(fill = 'x')

			real_size = os.path.getsize(self.gui.rbhandler.get_rb_path(item, 'R'))
			if real_size != size:
				real_size_frame = tk.Frame()
				self.draw_label(self.gui.lang['itemproperties_real_size'], font = self.bold_font, side = 'left', master = real_size_frame)
				self.draw_label(self.gui.rbhandler.convert_size(real_size), side = 'right', master = real_size_frame)
				real_size_frame.pack(fill = 'x')

			metadata_size_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemproperties_metadata_size'], font = self.bold_font, side = 'left', master = metadata_size_frame)
			self.draw_label(self.gui.rbhandler.convert_size(os.path.getsize(self.gui.rbhandler.get_rb_path(item))), side = 'right', master = metadata_size_frame)
			metadata_size_frame.pack(fill = 'x')

			version_frame = tk.Frame()
			self.draw_label(self.gui.lang['itemproperties_version'], font = self.bold_font, side = 'left', master = version_frame)
			self.draw_label(self.gui.rbhandler.get_md_version(item_info['version']), side = 'right', master = version_frame)
			version_frame.pack(fill = 'x')

		self.draw_label(self.gui.lang['itemproperties_location_asterisk'])
		if self.show_advanced:
			self.draw_label(self.gui.lang['itemproperties_location_asterisk_2'])
			ttk.Button(text = self.gui.lang['itemproperties_reduced'], command = lambda e = item: self.set_advanced(e, False)).pack()
		else: ttk.Button(text = self.gui.lang['itemproperties_advanced'], command = lambda e = item: self.set_advanced(e)).pack()

	def set_advanced(self, item, val = True):
		self.show_advanced = val
		self.show_properties(item)

	def quit(self):
		self.show_advanced = False
		self.refresh(True)

class NewItem:
	def __init__(self, gui):
		self.gui = gui
		self.ntfs_blacklist = '/:*?"<>|'
		self.supported_versions = (1, 2)

		self.return_mode = False
		self.discarded = False

		self.dt_picker = DTPicker(self.gui)

	def create_item(self):
		version = '1' if self.gui.rbhandler.get_os_version() <= (6, 3) else '2'
		path = 'C:\\' + self.gui.lang['new_item_name']
		is_folder = False
		size = 0
		deldate = datetime.utcnow().replace(tzinfo = timezone.utc)

		self.item_maker(False, version, path, is_folder, size, deldate)

	def create_item_call(self, version, path, is_folder, size, deldate, no_terminator = False):
		if not self.discarded:
			file_data = self.gui.rbhandler.write_metadata(version, path, size, deldate, is_folder, not no_terminator)

			drive = os.path.splitdrive(path)[0]
			if drive != '':
				if drive[0] not in self.gui.rbhandler.get_drives(): drive = 'C:'
			ext = os.path.splitext(path)[1]
			rbdir = f'{drive}{self.gui.rbdir}'
			f = os.listdir(rbdir)

			while True:
				random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
				if f'$I{random_str}{ext}' not in f: break

			rbname = random_str + ext
			with open(f'{rbdir}\\$I{random_str}{ext}', 'wb') as g: g.write(file_data)
			if is_folder: os.mkdir(f'{rbdir}\\$R{random_str}{ext}')
			else:
				with open(f'{rbdir}\\$R{random_str}{ext}', 'w') as g: pass

		self.end()

	def edit_item(self, item):
		self.gui.itemproperties.show_advanced = False
		
		e = self.gui.bin_items[item]

		self.old_drive_TEMP = e['rbin_drive'] + ':'

		self.item_maker(False, e['version'], e['ogpath'], e['isdir'], e['size'], e['deldate'], item, True)

	def edit_item_call(self, version, path, is_folder, size, deldate, random_str, old_ext, no_terminator = False):
		if not self.discarded:
			file_data = self.gui.rbhandler.write_metadata(version, path, size, deldate, is_folder, not no_terminator)

			ext = os.path.splitext(path)[1]
			rbdir = f'{self.old_drive_TEMP}{self.gui.rbdir}'
			rbname = random_str + old_ext

			if not is_folder and os.path.exists(f'{rbdir}\\$I{rbname}') and os.path.exists(f'{rbdir}\\$R{rbname}') and ext != old_ext:
				if tk.messagebox.askyesno(self.gui.lang['msgbox_notice'], self.gui.lang['msgbox_rbin_name_change'], icon = 'info'):
					os.rename(f'{rbdir}\\$I{rbname}', f'{rbdir}\\$I{random_str}{ext}')
					os.rename(f'{rbdir}\\$R{rbname}', f'{rbdir}\\$R{random_str}{ext}')
					rbname = random_str + ext

			with open(f'{rbdir}\\$I{rbname}', 'wb') as g: g.write(file_data)
			
			if (not is_folder and os.path.isdir(f'{rbdir}\\$R{rbname}')) or (is_folder and not os.path.isdir(f'{rbdir}\\$R{rbname}')):
				if tk.messagebox.askyesno(self.gui.lang['msgbox_notice'], self.gui.lang['msgbox_rbin_name_change_2'], icon = 'warning'):
					os.remove(f'{rbdir}\\$R{rbname}')
					if is_folder and not os.path.isdir(f'{rbdir}\\$R{rbname}'): os.mkdir(f'{rbdir}\\$R{rbname}')
					elif not is_folder and os.path.isdir(f'{rbdir}\\$R{rbname}'):
						with open(f'{rbdir}\\$R{rbname}', 'w') as g: pass
		self.end()

	def item_maker(self, return_mode, version, path, is_folder, size, deldate, random_str = None, edit_mode = False, hacker_mode = False, no_terminator = False):
		if return_mode:
			for i in range(1): # allows using break to skip code
				if not hacker_mode:
					if path == '':
						tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_path"]}: {self.gui.lang["msgbox_blank"]}\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
						break

					if not os.path.isabs(path):
						tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_invalid_path_4"]}\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
						break

					path_drive, path_nodr = os.path.splitdrive(path)

					if path_drive != '':
						if path_drive[0].upper() not in self.gui.rbhandler.get_drives():
							tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_invalid_path_3"]}\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
							break

					if not self.validate_text(path_nodr, self.ntfs_blacklist):
						tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_invalid_path"]}\n/ : * ? " < > |\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
						break
					if path_nodr == '':
						tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_invalid_path_2"]}\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
						break
					# check if path_nodr only has backslashes
					path_nodr_onlybslash = True
					for char in path_nodr:
						if char == '\\': continue
						else:
							path_nodr_onlybslash = False
							break
					if path_nodr_onlybslash:
						tk.messagebox.showerror(self.gui.lang['msgbox_error'], f'{self.gui.lang["new_item_invalid_path_2"]}\n\n{self.gui.lang["new_item_hacker_mode_note"]}')
						break

					if no_terminator: no_terminator = False

				for char in path:
					if ord(char) > 0xFFFF and self.gui.unsupported_tcl: tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['msgbox_error_unicode'])

				try: size_int = int(size)
				except ValueError:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['new_item_size_int_error'])
					break

				if size_int not in range(-abs(2**63), 2**63):
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['new_item_size_out_of_range'])
					break

				try: version_int = int(version)
				except ValueError:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['new_item_error_unsupported_version'])
					break
				if version_int not in self.supported_versions:
					tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['new_item_error_unsupported_version'])
					break
				elif version_int == 2 and self.gui.rbhandler.get_os_version() <= (6, 3):
					if not tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['new_item_version_warning'], icon = 'warning'): break

				if edit_mode: self.edit_item_call(version_int, path, is_folder, size_int, deldate, *os.path.splitext(random_str), no_terminator)
				else: self.create_item_call(version_int, path, is_folder, size_int, deldate, no_terminator)
		else:
			self.version_TEMP = version
			self.path_TEMP = path
			self.is_folder_TEMP = tk.BooleanVar(); self.is_folder_TEMP.set(is_folder)
			self.size_TEMP = size
			self.deldate_TEMP = deldate
			self.random_str_TEMP = random_str
			self.edit_mode_TEMP = edit_mode
			self.hacker_mode_TEMP = tk.BooleanVar(); self.hacker_mode_TEMP.set(hacker_mode)
			self.no_terminator_TEMP = tk.BooleanVar(); self.no_terminator_TEMP.set(no_terminator)

			deldate_TEMP_str = self.deldate_TEMP.astimezone(self.gui.tz).strftime(self.gui.date_format.encode('unicode-escape').decode()).encode().decode('unicode-escape')

			self.gui.refresh()
			self.gui.window.protocol('WM_DELETE_WINDOW', lambda: self.discard(True))
			self.gui.reload_confirm_func = self.discard_confirm
			if self.edit_mode_TEMP: self.gui.draw_label(self.gui.lang['new_item_edit'], font = self.gui.bold_font)
			else: self.gui.draw_label(self.gui.lang['main_new_item'], font = self.gui.bold_font)
			self.gui.draw_blank()
			ttk.Button(text = self.gui.lang['discard'], command = lambda: self.discard()).pack(side = 'bottom')
			ok_button = ttk.Button(text = 'OK', command = self.set_return)
			ok_button.pack(side = 'bottom')

			path_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['new_item_path'], font = self.gui.bold_font, side = 'left', master = path_frame)
			self.path_entry = ttk.Entry(path_frame, width = 30, justify = 'right')
			self.path_entry.insert(0, self.path_TEMP)
			self.path_entry.pack(side = 'right')
			path_frame.pack(fill = 'x')

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
			ttk.Button(deldate_frame, text = self.gui.lang['edit'], command = self.dt_picker.init_window).pack(side = 'right')
			self.gui.draw_label(self.gui.rbhandler.unicode_filter(deldate_TEMP_str), side = 'right', master = deldate_frame)
			deldate_frame.pack(fill = 'x')

			version_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['itemproperties_version'], font = self.gui.bold_font, side = 'left', master = version_frame)
			self.version_entry = ttk.Entry(version_frame, width = 30, justify = 'right')
			self.version_entry.insert(0, self.version_TEMP)
			self.version_entry.pack(side = 'right')
			version_frame.pack(fill = 'x')

			self.gui.draw_blank()
			self.gui.draw_label(self.gui.lang['new_item_hacker_mode'], font = self.gui.bold_font)

			hacker_mode_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['new_item_hacker_mode_enable'], side = 'left', master = hacker_mode_frame)
			ttk.Checkbutton(hacker_mode_frame, variable = self.hacker_mode_TEMP, command = lambda: self.set_hacker(self.hacker_mode_TEMP.get())).pack(side = 'right')
			hacker_mode_frame.pack(fill = 'x')

			no_terminator_frame = tk.Frame()
			self.gui.draw_label(self.gui.lang['new_item_hacker_mode_no_terminator'], side = 'left', master = no_terminator_frame)
			no_terminator_checkbox = ttk.Checkbutton(no_terminator_frame, variable = self.no_terminator_TEMP)
			if not self.hacker_mode_TEMP.get(): no_terminator_checkbox.config(state = 'disabled')
			no_terminator_checkbox.pack(side = 'right')
			no_terminator_frame.pack(fill = 'x')

			self.gui.window.mainloop()

	def set_return(self): self.item_maker(True, self.version_entry.get(), self.path_entry.get(), self.is_folder_TEMP.get(), self.size_entry.get(), self.deldate_TEMP, self.random_str_TEMP, self.edit_mode_TEMP, self.hacker_mode_TEMP.get(), self.no_terminator_TEMP.get())

	def set_hacker(self, value):
		self.hacker_mode_TEMP.set(value)
		self.reload()

	def reload(self): self.item_maker(False, self.version_entry.get(), self.path_entry.get(), self.is_folder_TEMP.get(), self.size_entry.get(), self.deldate_TEMP, self.random_str_TEMP, self.edit_mode_TEMP, self.hacker_mode_TEMP.get(), self.no_terminator_TEMP.get())

	def validate_text(self, text, blacklist):
		for char in text:
			if char in blacklist: return False

		return True

	def discard(self, delete_window = False):
		if self.discard_confirm():
			self.discarded = True
			if delete_window: sys.exit()
			else: self.end()

	def discard_confirm(self): return tk.messagebox.askyesno(self.gui.lang['msgbox_warning'], self.gui.lang['msgbox_discard'] if self.edit_mode_TEMP else self.gui.lang['msgbox_discard_item'], icon = 'warning', default = 'no')

	def end(self):
		self.gui.window.protocol('WM_DELETE_WINDOW', self.gui.quit)
		self.gui.refresh(True)

class LocaleChooser:
	def __init__(self, gui): self.gui = gui

	def init_window(self):
		if not self.gui.locale_chooser_open:
			self.gui.locale_chooser_open = True

			self.win = tk.Toplevel(self.gui.window)
			self.win.geometry('300x120')
			self.win.resizable(False, False)
			self.win.protocol('WM_DELETE_WINDOW', self.quit)
			self.win.title(self.gui.lang['locale_chooser_title'])
			try: self.win.iconbitmap(f'{self.gui.temp_path}\\icon.ico')
			except tk.TclError:
				err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.gui.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
				print(err_text)
				tk.messagebox.showerror('Hmmm?', err_text)
				sys.exit()

			self.draw_menu()
			
			self.win.focus()
			self.win.grab_set()
			self.win.mainloop()

	def quit(self):
		self.win.grab_release()
		self.win.destroy()
		self.gui.locale_chooser_open = False

	def save(self):
		self.quit()
		self.gui.setting_change()

	def cancel(self):
		self.gui.locale_tk.set(self.old_locale)
		self.gui.locale_option.set(self.gui.prev_locale_option)
		self.quit()

	def draw_menu(self):
		for w in self.win.winfo_children(): w.destroy()

		self.old_locale = self.gui.locale_tk.get()

		self.gui.draw_label(self.gui.lang['locale_chooser_choose'], justify = 'center', master = self.win)
		ttk.Combobox(self.win, textvariable = self.gui.locale_tk, values = self.gui.locales).pack()
		button_frame = tk.Frame(self.win); button_frame.pack(side = 'bottom')
		ttk.Button(button_frame, text = 'OK', command = self.save).pack(side = 'left')
		ttk.Button(button_frame, text = self.gui.lang['cancel'], command = self.cancel).pack(side = 'right')

class DTPicker:
	def __init__(self, gui):
		self.gui = gui

		self.type = 'basic'
		self.types = ['basic', 'ft']
		self.types_names = [self.gui.lang[_] for _ in ['dtpicker_type_basic']]; self.types_names.append('FILETIME')
		self.type_name = tk.StringVar(); self.type_name.set(self.types_names[self.types.index(self.type)])


	def init_window(self):
		if not self.gui.dt_picker_open:
			self.gui.dt_picker_open = True

			self.win = tk.Toplevel(self.gui.window)
			self.win.geometry('400x400')
			self.win.resizable(False, False)
			self.win.protocol('WM_DELETE_WINDOW', self.quit)
			self.win.title(self.gui.lang['dtpicker_title'])
			try: self.win.iconbitmap(f'{self.gui.temp_path}\\icon.ico')
			except tk.TclError:
				err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.gui.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
				print(err_text)
				tk.messagebox.showerror('Hmmm?', err_text)
				sys.exit()

			self.draw_menu()
			
			self.win.focus()
			self.win.grab_set()
			self.win.mainloop()

	def quit(self):
		self.win.grab_release()
		self.win.destroy()
		self.gui.dt_picker_open = False

	def draw_menu(self):
		self.deldate_aware = self.gui.new_item.deldate_TEMP.astimezone(self.gui.tz)

		self.header_frame = tk.Frame(self.win); self.header_frame.pack()
		self.gui.draw_label(self.gui.lang['dtpicker_title'], font = self.gui.bold_font, master = self.header_frame)
		self.gui.draw_blank(master = self.header_frame)
		self.type_frame = tk.Frame(self.win); self.type_frame.pack()
		self.gui.draw_label(self.gui.lang['dtpicker_type'] + ' ', side = 'left', master = self.type_frame)
		type_cb = ttk.Combobox(self.type_frame, textvariable = self.type_name, values = self.types_names)
		type_cb.bind('<<ComboboxSelected>>', lambda x: self.load_type())
		type_cb.pack()

		self.load_type()

	def load_type(self):
		for w in self.win.winfo_children():
			if w not in (self.type_frame, self.header_frame): w.destroy()

		button_frame = tk.Frame(self.win); button_frame.pack(side = 'bottom')
		self.ok_button = ttk.Button(button_frame, text = 'OK', command = lambda: tk.messagebox.showerror(*[self.gui.lang['qmark']]*2)); self.ok_button.pack(side = 'left')
		ttk.Button(button_frame, text = self.gui.lang['cancel'], command = self.quit).pack(side = 'right')

		self.type = self.types[self.types_names.index(self.type_name.get())]

		if self.type == 'basic': self.basic_type()
		elif self.type == 'ft': self.ft_type()

	def basic_type(self):
		self.gui.draw_blank(master = self.win)

		dmy_frame = tk.Frame(self.win)

		day_frame = tk.Frame(dmy_frame)
		self.gui.draw_label(self.gui.lang['dtpicker_day'], side = 'top', master = day_frame)
		self.basic_day_entry = ttk.Entry(day_frame, width = 2)
		self.basic_day_entry.insert(0, self.deldate_aware.day)
		self.basic_day_entry.pack(side = 'bottom')
		day_frame.pack(side = 'left')

		month_frame = tk.Frame(dmy_frame)
		self.gui.draw_label(self.gui.lang['dtpicker_month'], side = 'top', master = month_frame)
		self.basic_month_entry = ttk.Entry(month_frame, width = 2)
		self.basic_month_entry.insert(0, self.deldate_aware.month)
		self.basic_month_entry.pack(side = 'bottom')
		month_frame.pack(side = 'left')

		year_frame = tk.Frame(dmy_frame)
		self.gui.draw_label(self.gui.lang['dtpicker_year'], side = 'top', master = year_frame)
		self.basic_year_entry = ttk.Entry(year_frame, width = 4)
		self.basic_year_entry.insert(0, self.deldate_aware.year)
		self.basic_year_entry.pack(side = 'bottom')
		year_frame.pack(side = 'right')

		dmy_frame.pack()

		self.gui.draw_blank(master = self.win)

		hm_frame = tk.Frame(self.win)

		hour_frame = tk.Frame(hm_frame)
		self.gui.draw_label(self.gui.lang['dtpicker_hour'], side = 'top', master = hour_frame)
		self.basic_hour_entry = ttk.Entry(hour_frame, width = 2)
		self.basic_hour_entry.insert(0, self.deldate_aware.hour)
		self.basic_hour_entry.pack(side = 'bottom')
		hour_frame.pack(side = 'left')

		minute_frame = tk.Frame(hm_frame)
		self.gui.draw_label(self.gui.lang['dtpicker_minute'], side = 'top', master = minute_frame)
		self.basic_minute_entry = ttk.Entry(minute_frame, width = 2)
		self.basic_minute_entry.insert(0, self.deldate_aware.minute)
		self.basic_minute_entry.pack(side = 'bottom')
		minute_frame.pack(side = 'right')

		hm_frame.pack()

		self.ok_button.config(command = self.basic_save)

	def basic_save(self):
		test_deldate = self.deldate_aware.replace()
		try:
			test_deldate = test_deldate.replace(
				year = int(self.basic_year_entry.get()),
				month = int(self.basic_month_entry.get()),
				day = int(self.basic_day_entry.get()),
				hour = int(self.basic_hour_entry.get()),
				minute = int(self.basic_minute_entry.get())
				)

			self.gui.new_item.deldate_TEMP = test_deldate.replace()
		except Exception:
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], 'Invalid date!')
			return			

		# this code will only run if no exception occurs (due to return statement)
		self.quit()
		self.gui.new_item.reload()			

	def ft_type(self):
		self.gui.draw_blank(master = self.win)
		self.gui.draw_label(self.gui.lang['dtpicker_ft_header'], master = self.win)
		self.ft_entry = ttk.Entry(self.win, width = self.win.winfo_width(), justify = 'center')
		self.ft_entry.insert(0, str(self.gui.rbhandler.dt_to_filetime(self.gui.new_item.deldate_TEMP)))
		self.ft_entry.pack()
		self.gui.draw_blank(master = self.win)
		
		learn_more_label = ttk.Label(self.win, text = self.gui.lang['dtpicker_ft_learn_more'], font = self.gui.underline_font, foreground = 'blue', justify = 'center')
		learn_more_label.bind('<Button-1>', lambda x: webbrowser.open_new_tab('https://learn.microsoft.com/windows/win32/sysinfo/file-times'))
		learn_more_label.pack()

		self.ok_button.config(command = self.ft_save)

	def ft_save(self):
		try: ft_val = int(self.ft_entry.get())
		except ValueError:
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['dtpicker_ft_int_error'])
			return

		try: self.gui.new_item.deldate_TEMP = self.gui.rbhandler.filetime_to_dt(ft_val)
		except OverflowError:
			tk.messagebox.showerror(self.gui.lang['msgbox_error'], self.gui.lang['dtpicker_ft_out_of_range'])
			return

		# this code will only run if no exception occurs (due to return statement)
		self.quit()
		self.gui.new_item.reload()

class UpdaterGUI:
	def __init__(self, gui):
		self.gui = gui

		self.auto = False
		self.after_ms = 100

		self.updater = Updater()

	def init_window(self, auto = False):
		if not self.gui.updater_win_open:
			self.gui.updater_win_open = True

			if auto: self.auto = True

			self.win = tk.Toplevel(self.gui.window)
			self.win.geometry('300x120')
			self.win.resizable(False, False)
			self.win.protocol('WM_DELETE_WINDOW', self.quit)
			self.win.title(self.gui.lang['updater_title'])
			try: self.win.iconbitmap(f'{self.gui.temp_path}\\icon.ico')
			except tk.TclError:
				err_text = f'Whoops! The icon file "icon.ico" is required.\nCan you make sure the file is in "{self.gui.temp_path}"?\n\n{traceback.format_exc()}\nIf this problem persists, please report it here:\nhttps://github.com/{username}/{repo_name}/issues'
				print(err_text)
				tk.messagebox.showerror('Hmmm?', err_text)
				sys.exit()

			if self.auto:
				self.win.withdraw()
				self.gui.set_title(self.gui.lang['updater_checking'])
			self.win.focus()
			self.win.grab_set()
			self.main()

	def quit(self):
		self.win.grab_release()
		self.win.destroy()
		self.gui.updater_win_open = False
		if self.auto:
			self.auto = False
			self.gui.main()

	def main(self):
		self.update_thread = ThreadWithResult(target = self.updater.check_updates, args = (self.gui.check_prerelease_version.get(),))

		self.draw_check()
		self.win.after(1, self.start_thread)
		self.win.mainloop()

	def start_thread(self):
		self.update_thread.start()
		while self.update_thread.is_alive():
			self.win.update_idletasks()
			self.progressbar['value'] = self.updater.progress
		self.progressbar['value'] = 100
		self.update_thread.join()
		update_info = self.update_thread.result

		if update_info['error']:
			if update_info['exceeded']: self.draw_msg(self.gui.lang['updater_exceeded'])
			elif update_info['nowifi']: self.draw_msg(self.gui.lang['updater_offline'])
			else: self.draw_msg(self.gui.lang['updater_unknown_error'])
		elif update_info['newupdate']: self.draw_download_msg(update_info['title'], update_info['tag'], update_info['prerelease'])
		else: self.draw_msg(self.gui.lang['updater_latest'])

	def draw_check(self):
		for w in self.win.winfo_children(): w.destroy()

		self.gui.draw_label(self.gui.lang['updater_checking'], master = self.win)
		self.progressbar = ttk.Progressbar(self.win, orient = 'horizontal', length = 100, mode = 'determinate')
		self.progressbar.pack()
		self.gui.draw_label(self.gui.lang['updater_donotclose'], font = self.gui.bold_font, justify = 'center', side = 'bottom', master = self.win)

	def draw_msg(self, msg):
		if self.auto:
			self.gui.set_title()
			self.quit()
		else:
			for w in self.win.winfo_children(): w.destroy()
			self.gui.draw_label(msg, justify = 'center', master = self.win)
			ttk.Button(self.win, text = self.gui.lang['back'], command = self.quit).pack(side = 'bottom')

	def draw_download_msg(self, title, tag, prever):
		if self.auto:
			self.win.deiconify()
			self.gui.set_title()
		for w in self.win.winfo_children(): w.destroy()
		self.gui.draw_label(f'''\
{self.gui.lang['updater_newupdate']}
{self.gui.lang['updater_currver']}{self.gui.version}{self.gui.lang['updater_prerelease'] if prerelease else ''}
{self.gui.lang['updater_newver']}{title}{self.gui.lang['updater_prerelease'] if prever else ''}\
''', justify = 'center', master = self.win)
		ttk.Button(self.win, text = self.gui.lang['cancel'], command = self.quit).pack(side = 'bottom')
		ttk.Button(self.win, text = self.gui.lang['updater_download'], command = lambda: self.open_download(tag)).pack(side = 'bottom')
		
		if self.auto: self.win.deiconify()

	def open_download(self, tag):
		webbrowser.open_new_tab(f'https://github.com/{username}/{repo_name}/releases/tag/{tag}')
		self.quit()

class Updater:
	def __init__(self):
		self.username, self.reponame = username, repo_name
		self.request_limit = 5

		self.progress = 0
		self.progress_inc = 25

	def check_internet(self):
		try:
			self.request('https://google.com', True)
			return True
		except: return False

	def request(self, url, testing = False):
		success = False
		for i in range(self.request_limit):
			try:
				r = urllib.request.urlopen(url)
				success = True
				break
			except:
				if not testing:
					if not self.check_internet(): return
		if success:
			if not testing:
				d = r.read().decode()
				return json.loads(d)

	def check_updates(self, prerelease):
		self.progress = 0

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
			
			response = self.request(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases')
			if response is None: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

			for info in response: versions.append(info['tag_name'])

			# UPDATE POINT 1
			self.progress += self.progress_inc

			if internal_version not in versions:
				try:
					testvar = response['message']
					if 'API rate limit exceeded for' in testvar:
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else: return {'newupdate': False, 'error': False}
				except: return {'newupdate': False, 'error': False}
			if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

			# UPDATE POINT 2
			self.progress += self.progress_inc

			response = self.request(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/tags/{internal_version}')
			if response is None: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}\

			try:
				testvar = response['message']
				if 'API rate limit exceeded for' in testvar:
					return {
					'newupdate': False,
					'error': True,
					'exceeded': True
					}
				else: return {'newupdate': False, 'error': False}
			except: pass

			currvertime = response['published_at']

			# UPDATE POINT 3
			self.progress += self.progress_inc

			if not prerelease:
				if not self.check_internet(): return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}

				response = self.request(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/latest')
				if response is None: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
				try:
					testvar = response['message']
					if 'API rate limit exceeded for' in testvar:
						return {
						'newupdate': False,
						'error': True,
						'exceeded': True
						}
					else: return {'newupdate': False, 'error': False}
				except: pass
				if response['tag_name'] != internal_version and response['published_at'] > currvertime:
					return {
					'newupdate': True,
					'prerelease': False,
					'error': False,
					'title': response['name'],
					'tag': response['tag_name']
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

					response = self.request(f'https://api.github.com/repos/{self.username}/{self.reponame}/releases/tags/{version}')
					if response is None: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': True}
					try:
						testvar = response['message']
						if 'API rate limit exceeded for' in testvar:
							return {
							'newupdate': False,
							'error': True,
							'exceeded': True
							}
						else: return {'newupdate': False, 'error': True, 'exceeded': False, 'nowifi': False}
					except: pass
					if currvertime < response['published_at']:
						return {
						'newupdate': True,
						'prerelease': response['prerelease'],
						'error': False,
						'title': response['name'],
						'tag': response['tag_name']
						}
					else:
						return {
						'newupdate': False,
						'unofficial': False,
						'error': False
						}
		except:
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

class FExplorerFrame(tk.Frame):
	def __init__(self, master, gui, item, text, **kw):
		tk.Frame.__init__(self, master, **kw)
		self.gui = gui
		self.item = item

		self.hover_color = '#E5F3FF'
		self.select_color = '#CCE8FF'
		self.highlight_color = '#99D1FF'
		self.norm_color = self.cget('bg')

		self.config(highlightthickness = 1)
		self.config(highlightcolor = self.highlight_color)

		self.hovered = False
		self.selected = False

		self.label = ttk.Label(self, text = text, anchor = 'nw')
		self.label.pack(side = 'left', anchor = 'nw')
		self.label.bind('<Button-1>', self.select)
		self.label.bind('<Button-3>', self.rclick_menu)

		style = ttk.Style()
		style.configure('Sel.TButton', background = self.select_color, height = 10)

		self.blank = ttk.Label(self, background = self.select_color, anchor = 'sw')
		self.button_frame = tk.Frame(self)
		ttk.Button(self.button_frame, text = self.gui.lang['main_restore'], style = 'Sel.TButton', command = lambda: self.gui.restore_item(item)).pack(side = 'left')
		ttk.Button(self.button_frame, text = self.gui.lang['main_delete'], style = 'Sel.TButton', command = lambda: self.gui.delete_item(item)).pack(side = 'right')

		self.context_menu = tk.Menu(self, tearoff = False)
		self.context_menu.add_command(label = self.gui.lang['main_open'], font = self.gui.bold_font, command = lambda: self.gui.open_item(item))
		self.context_menu.add_command(label = self.gui.lang['edit'], command = self.edit_item)
		self.context_menu.add_separator()
		self.context_menu.add_command(label = self.gui.lang['main_restore'], command = lambda: self.gui.restore_item(item))
		self.context_menu.add_command(label = self.gui.lang['main_delete'], command = lambda: self.gui.delete_item(item))
		self.context_menu.add_separator()
		self.context_menu.add_command(label = self.gui.lang['main_properties'], command = self.show_properties)

		self.bind('<Enter>', self.hover_enter)
		self.bind('<Leave>', self.hover_leave)
		self.bind('<Button-1>', self.select)
		self.bind('<Double-1>', lambda x: self.gui.open_item(item))

	def show_properties(self):
		self.gui.window.unbind('<Button-1>')
		self.gui.itemproperties.show_properties(self.item)

	def edit_item(self):
		item_info = self.gui.bin_items[self.item]

		self.gui.window.unbind('<Button-1>')
		self.gui.new_item.edit_item(self.item)

	def hover_enter(self, event):
		if not self.selected:
			self.hovered = True
			self.config(bg = self.hover_color)
			self.label.config(background = self.hover_color)

	def hover_leave(self, event):
		if not self.selected:
			self.hovered = False
			self.config(bg = self.norm_color)
			self.label.config(background = self.norm_color)

	def select(self, event = None):
		self.after(10, self.deselect_all)
		self.selected = True
		self.config(bg = self.select_color)
		self.label.config(background = self.select_color)
		self.blank.pack()
		self.button_frame.pack(side = 'right')
		self.focus_set()
		self.bind('<Button-3>', self.rclick_menu)
		self.bind('<Return>', lambda e: self.gui.open_item(self.item))
		self.bind('<Delete>', lambda e: self.gui.delete_item(self.item))
		try: self.bind('<KP_Delete>', lambda e: self.gui.delete_item(self.item))
		except: pass
		self.gui.window.bind('<Button-1>', self.deselect_init)

	def deselect_init(self, event):
		if self.winfo_exists():
			if self.selected and self.winfo_containing(event.x_root, event.y_root) not in self.gui.rbhandler.get_all_childrens(self) + [self]: self.after(10, self.deselect)
		else: self.gui.window.unbind('<Button-1>')

	def deselect(self, event = None):
		self.selected = False
		self.config(bg = self.norm_color)
		self.label.config(background = self.norm_color)
		self.button_frame.pack_forget()
		self.blank.pack_forget()
		self.unbind('<Button-3>')
		self.unbind('<Return>')
		self.unbind('<Delete>')
		try: self.unbind('<KP_Delete>')
		except: pass

	def deselect_all(self):
		for w in self.master.winfo_children():
			if isinstance(w, FExplorerFrame) and w != self:
				if w.selected:
					w.selected = False
					w.config(bg = self.norm_color)
					w.label.config(background = self.norm_color)
					w.button_frame.pack_forget()
					w.blank.pack_forget()
					w.unbind('<Button-3>')
					w.unbind('<Return>')
					w.unbind('<Delete>')
					try: w.unbind('<KP_Delete>')
					except: pass

	def rclick_menu(self, event):
		if not self.selected: self.select()
		self.gui.context_menu_open = True
		self.context_menu.tk_popup(event.x_root, event.y_root)

# https://stackoverflow.com/a/65447493
class ThreadWithResult(threading.Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
		def function(): self.result = target(*args, **kwargs)
		super().__init__(group=group, target=function, name=name, daemon=daemon)
