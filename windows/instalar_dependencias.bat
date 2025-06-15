@echo off
title Instalador de Dependencias - Reproductor Jellyfin
echo.
echo ================================================
echo    Instalador de Dependencias - Reproductor Jellyfin
echo ================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

echo Verificando Python...
python --version
echo.

REM Verificar si pip está disponible
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no está disponible
    echo Por favor, instala pip o actualiza Python
    pause
    exit /b 1
)

echo Instalando dependencias...
echo.

REM Instalar dependencias desde requirements.txt
if exist "requirements.txt" (
    echo Instalando desde requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Fallo al instalar dependencias
        pause
        exit /b 1
    )
) else (
    echo Instalando dependencias manualmente...
    pip install PyQt5 python-vlc requests Pillow
    if errorlevel 1 (
        echo ERROR: Fallo al instalar dependencias
        pause
        exit /b 1
    )
)

echo.
echo Creando íconos de respaldo...
python create_icons.py

echo.
echo ================================================
echo    ¡Instalación completada exitosamente!
echo ================================================
echo.
echo Ahora puedes ejecutar 'ejecutar_reproductor.bat' para iniciar la aplicación
echo.
pause 