@echo off
echo ========================================
echo Installing Transfer Scheduling Data + FSRS
echo ========================================
echo.

REM Find Anki addons folder
set "ANKI_ADDONS=%APPDATA%\Anki2\addons21"

if not exist "%ANKI_ADDONS%" (
    echo ERROR: Anki addons folder not found at:
    echo %ANKI_ADDONS%
    echo.
    echo Please install Anki first or check the path.
    pause
    exit /b 1
)

echo Anki addons folder found: %ANKI_ADDONS%
echo.

REM Create addon folder
set "ADDON_FOLDER=%ANKI_ADDONS%\transfer_scheduling_fsrs"
echo Creating addon folder: %ADDON_FOLDER%
if not exist "%ADDON_FOLDER%" mkdir "%ADDON_FOLDER%"

REM Copy files
echo.
echo Copying files...
copy /Y "__init__.py" "%ADDON_FOLDER%\"
copy /Y "config.json" "%ADDON_FOLDER%\"
copy /Y "manifest.json" "%ADDON_FOLDER%\"
copy /Y "meta.json" "%ADDON_FOLDER%\"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart Anki
echo 2. Open Browser (Browse button)
echo 3. Go to Cards menu - you should see:
echo    - "Scheduling data : Transfer from" (Ctrl+Alt+C)
echo    - "Scheduling data : Transfer to" (Ctrl+Alt+V)
echo.
echo See INSTALLATION.md for usage instructions.
echo.
pause
