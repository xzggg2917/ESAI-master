# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ESAI application.
This ensures the installer and application are in English regardless of system locale.
"""

block_cipher = None

# Analysis: collect all necessary files
a = Analysis(
    ['run_esai.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('rj.png', '.'),
        ('logo.ico', '.'),
        ('save.png', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_pdf',
        'numpy',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        'unittest',
        'unittest.mock',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ESAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression to prevent interpreter errors
    console=False,  # No console window for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',
    version='version_info.txt',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # Disable UPX compression
    upx_exclude=[],
    name='ESAI',
)
