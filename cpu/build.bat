@echo off
setlocal
cd /d "%~dp0"

".\Scripts\python.exe" -m PyInstaller --clean --noconfirm main.spec
if errorlevel 1 goto :error

copy /y "icon.ico" "dist\Audio 2 MIDI (CPU)\icon.ico" >nul
if errorlevel 1 goto :error
echo Build complete: dist\Audio 2 MIDI (CPU)
exit /b 0

:error
echo Build failed with exit code %errorlevel%.
exit /b %errorlevel%
