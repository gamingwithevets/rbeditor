# -*- mode: python ; coding: utf-8 -*-

# RBEditor SPEC file
# for use with PyInstaller

a = Analysis(['main.py', 'gui.py', 'lang.py'], datas = [('icon.ico', '.')], hiddenimports = ['wmi'])
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [], name='rbeditor', console=False, icon='icon.ico')
