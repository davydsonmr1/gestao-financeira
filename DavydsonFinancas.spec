# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Adicionar o diretório src como dados
src_dir = Path('src')
src_tree = [(str(src_dir), 'src')]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=src_tree,
    hiddenimports=[
        'src',
        'src.controllers',
        'src.database',
        'src.views',
        'src.views.dashboard',
        'src.views.forms',
        'src.views.settings',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DavydsonFinancas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
