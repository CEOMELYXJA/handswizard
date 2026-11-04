@echo off
setlocal
cd /d "%~dp0"
set "HW_PYTHON="
py -3.15 -c "import sys" >nul 2>&1
if not errorlevel 1 set "HW_PYTHON=py -3.15"
if defined HW_PYTHON goto menu
py -3 -c "import sys; assert sys.version_info >= (3, 10)" >nul 2>&1
if not errorlevel 1 set "HW_PYTHON=py -3"
if defined HW_PYTHON goto menu
set "HW_BUNDLED=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%HW_BUNDLED%" set "HW_PYTHON=""%HW_BUNDLED%"""
if defined HW_PYTHON goto menu
echo.
echo Python est introuvable. Installe Python 3.15 depuis python.org,
echo puis relance ce fichier. Coche l'option du lanceur Python pendant l'installation.
pause
exit /b 1
:menu
echo.
echo [1] Webcam : mains libres
echo [2] iPhone : gyroscope
choice /C 12 /M "Mode"
if errorlevel 2 goto iphone
echo.
echo Demarrage de la webcam. Garde cette fenetre ouverte.
%HW_PYTHON% -u webcam_server.py
if errorlevel 1 echo Le demarrage a echoue. Lis le message ci-dessus.
pause
exit /b
:iphone
if not exist ".venv-iphone\Scripts\python.exe" %HW_PYTHON% -m venv .venv-iphone
if errorlevel 1 goto error
.venv-iphone\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
.venv-iphone\Scripts\python.exe iphone_server.py
pause
exit /b
:error
echo Installation iPhone incomplete. Verifie Python et Internet.
pause

