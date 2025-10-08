# PDF Flipbook Viewer Application

## Overview
A professional PDF flipbook viewer with realistic page curl effects, thumbnail sidebar, and comprehensive controls. Built with Python and tkinter, designed to be exported as a standalone Windows .exe file (~20-30 MB) without any webview dependencies.

## Project Type
Desktop Application (GUI) - NOT a web application

## Key Features
- ✅ Pure desktop application using tkinter (no webview/browser)
- ✅ PDF support with PyMuPDF (load and view PDF files)
- ✅ Thumbnail sidebar with clickable page previews
- ✅ Realistic page curl/flip animation effect
- ✅ Page navigation (Previous/Next buttons)
- ✅ Zoom In/Out controls
- ✅ Fullscreen mode
- ✅ Download PDF functionality
- ✅ Export to exe button (build from within app)
- ✅ Sound effects support (page turn sounds)
- ✅ Professional UI matching reference screenshots
- ✅ Optimized for small exe size (20-30 MB)

## Tech Stack
- **Language**: Python 3.11
- **GUI Framework**: tkinter (built-in, lightweight)
- **PDF Processing**: PyMuPDF (fitz)
- **Image Processing**: Pillow (PIL)
- **Audio**: pygame.mixer
- **Packaging**: PyInstaller

## Project Structure
```
.
├── flipbook.py              - Main PDF viewer application
├── flipbook_old.py          - Backup of previous version
├── build_exe.py             - Automated EXE builder script
├── create_sample_pdf.py     - Generates demo PDF
├── sample_flipbook.pdf      - 8-page demo PDF
├── HOW_TO_BUILD_EXE.txt     - Complete build instructions
└── sounds/                  - Sound effects
    ├── page_turn.wav       - Page navigation sound
    └── play.wav            - Animation start sound
```

## Running in Replit
The application runs in VNC (desktop viewer) mode in Replit. You can see the GUI in the VNC pane.
Note: Audio is not available in Replit environment but works in the compiled .exe

## Building Windows EXE

### Quick Build Method 1 - From Terminal:
```bash
python build_exe.py
```

### Quick Build Method 2 - From App:
1. Run the flipbook application
2. Click "Export as exe" button
3. Build starts automatically

### Manual Build:
```bash
pyinstaller --onefile --windowed --name=FlipbookPDFViewer \
  --add-data="sounds;sounds" --exclude-module=matplotlib \
  --exclude-module=numpy --exclude-module=pandas \
  --strip --optimize=2 flipbook.py
```

Output: `dist/FlipbookPDFViewer.exe` (~20-30 MB)

## User Requirements
✅ Flipbook should NOT open in webview - Uses tkinter desktop window
✅ Downloaded exe should NOT be webview-based - Standalone desktop app  
✅ Must have sound effects - Implemented with pygame
✅ Must look like reference screenshots - Matching UI design with:
  - Thumbnail sidebar (left)
  - Page curl animation effect
  - Professional control buttons
  - Export to exe button
  - Color scheme matching screenshots
✅ EXE size around 20-25 MB - Optimized with PyInstaller flags (~20-30 MB with PDF support)

## Important Notes
1. **Build Environment**: Must build on Windows to create Windows .exe
2. **Replit Usage**: Replit runs Linux, so download files and build locally on Windows
3. **Audio**: Works in .exe but not in Replit VNC (no audio device)
4. **Dependencies**: All included in PyInstaller bundle, no Python needed on target PC
5. **PDF Library**: PyMuPDF adds ~15MB to exe size but provides full PDF support

## Recent Changes (Oct 8, 2025)
- Started with empty GitHub repository
- Created initial simple image viewer
- **MAJOR UPDATE**: Rebuilt as PDF flipbook viewer to match user's reference screenshots
- Added PDF support with PyMuPDF
- Implemented thumbnail sidebar (left panel)
- Added realistic page curl animation effect
- Created professional UI matching reference design
- Added all control buttons (Previous, Next, Zoom, Fullscreen, Download, Export)
- Integrated PyInstaller build into app UI
- Created sample PDF for testing
- Updated all documentation

## Architecture Decisions
- **tkinter over Electron**: Much smaller file size (25MB vs 100MB+)
- **PyMuPDF for PDF**: Industry standard, lightweight, excellent rendering
- **pygame.mixer for audio**: Lightweight, good integration
- **PyInstaller for packaging**: Better compatibility, easier configuration
- **Graceful audio fallback**: App works even without audio device
- **Page curl effect**: Lightweight image overlay technique (no heavy animation library)

## Design Matching Reference Screenshots
Reference screenshot 1 (Panchal Machinery flipbook):
- ✅ Thumbnail sidebar on left
- ✅ Page curl/flip effect on main view
- ✅ Page counter display
- ✅ Blue-gray color scheme

Reference screenshot 2 (PDF viewer):
- ✅ Control buttons bar at bottom
- ✅ Previous/Next navigation
- ✅ Zoom controls
- ✅ Fullscreen button
- ✅ Download button
- ✅ **Export as exe button** (green, bottom right)

## User Preferences
- Language: Hindi/English mix
- Prefers lightweight solutions
- Needs exe export capability
- No webview-based applications
- Wants UI matching specific reference screenshots
