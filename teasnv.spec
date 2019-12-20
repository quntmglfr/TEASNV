# -*- mode: python -*-
# test 123
from kivy.deps import sdl2, glew

block_cipher = None

a = Analysis(['teasnv\\main.py'],
             pathex=['C:\\Users\\T12\\code\\python\\teasnv'],
             binaries=[],
             datas=[('C:\\Users\\T12\\code\\python\\teasnv\\teasnv\\data',
                     'data')],
             hiddenimports=['requests', 'bs4', 'telnetlib'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]
          [],
          name='teasnv',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='teasnv\\data\\icon.ico')
