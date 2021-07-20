# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\james\\OneDrive\\Documents\\Coding Projects\\Walker Telecomm Automation\\ProjectManagementTools\\WorkLog_Converter\\worklog_main.py'],
             pathex=['C:\\Users\\james\\OneDrive\\Documents\\Coding Projects\\Walker Telecomm Automation\\ProjectManagementTools\\WorkLog_Converter'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='worklog_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='worklog_main')
