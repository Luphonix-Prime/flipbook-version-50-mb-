import PyInstaller.__main__
import os
import shutil

print("Building PDF Flipbook Viewer EXE...")
print("=" * 50)

PyInstaller.__main__.run([
    'flipbook.py',
    '--onefile',
    '--windowed',
    '--name=FlipbookPDFViewer',
    '--icon=NONE',
    '--noconsole',
    '--add-data=sounds:sounds',
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',
    '--exclude-module=tensorflow',
    '--exclude-module=torch',
    '--strip',
    '--optimize=2',
    '--clean'
])

print("\n" + "=" * 50)
print("✅ Build complete!")
print("📁 EXE file location: dist/FlipbookPDFViewer.exe")
print("\nFeatures included:")
print("✓ PDF support with thumbnails")
print("✓ Page curl animation effect")
print("✓ Zoom controls")
print("✓ Fullscreen mode")
print("✓ Export to exe button")
print("\nExpected size: 20-30 MB (includes PDF rendering library)")
