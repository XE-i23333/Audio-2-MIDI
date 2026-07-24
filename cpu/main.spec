# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

app_name = 'Audio 2 MIDI (CPU)'
datas = [
    ('ffmpeg', 'ffmpeg'),
    ('icon.ico', '.'),
    ('Lib\\site-packages\\basic_pitch\\saved_models\\icassp_2022', 'basic_pitch/saved_models/icassp_2022'),
]
binaries = []
hiddenimports = ['torch', 'onnxruntime', 'numpy', 'soundfile']

for package in ('audio_separator', 'basic_pitch', 'torch', 'torchvision', 'onnxruntime'):
    package_data, package_binaries, package_hiddenimports = collect_all(package)
    datas += package_data
    binaries += package_binaries
    hiddenimports += package_hiddenimports

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
