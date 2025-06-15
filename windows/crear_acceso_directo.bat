@echo off
title Crear Acceso Directo - Reproductor Jellyfin
echo.
echo ================================================
echo    Creando Acceso Directo - Reproductor Jellyfin
echo ================================================
echo.

REM Obtener la ruta actual
set "CURRENT_DIR=%~dp0"
set "BAT_FILE=%CURRENT_DIR%ejecutar_simple.bat"

REM Verificar si el archivo .bat existe
if not exist "%BAT_FILE%" (
    echo ERROR: No se encuentra ejecutar_simple.bat
    echo Asegúrate de ejecutar este script desde la carpeta del proyecto
    pause
    exit /b 1
)

REM Obtener la ruta del escritorio
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

if not defined DESKTOP (
    echo ERROR: No se pudo encontrar la carpeta del escritorio
    pause
    exit /b 1
)

REM Crear el archivo .lnk usando PowerShell
echo Creando acceso directo en el escritorio...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Reproductor Jellyfin.lnk'); $Shortcut.TargetPath = '%BAT_FILE%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Reproductor jellyStream'; $Shortcut.Save()"

if errorlevel 1 (
    echo ERROR: No se pudo crear el acceso directo
    pause
    exit /b 1
)

echo.
echo ================================================
echo    ¡Acceso directo creado exitosamente!
echo ================================================
echo.
echo El acceso directo se encuentra en: %DESKTOP%\Reproductor Jellyfin.lnk
echo.
echo Ahora puedes hacer doble clic en el acceso directo para ejecutar la aplicación
echo.
pause 