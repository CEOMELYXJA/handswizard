@echo off
setlocal
cd /d "%~dp0"
echo [1] Webcam : mains libres (Python 3.15, aucun paquet Python a installer)
echo [2] iPhone : gyroscope (dependances additionnelles)
choice /C 12 /M "Mode"
if errorlevel 2 goto iphone
py -3.15 webcam_server.py
if errorlevel 1 echo Impossible de demarrer. Verifie que Python 3.15 est installe.
pause
exit /b
:iphone
if not exist ".venv-iphone\Scripts\python.exe" py -3.15 -m venv .venv-iphone
if errorlevel 1 goto error
.venv-iphone\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
.venv-iphone\Scripts\python.exe iphone_server.py
pause
exit /b
:error
echo Installation iPhone incomplete. Verifie Python et Internet.
pause
