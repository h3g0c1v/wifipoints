@echo off
REM Script para comprimir todos los backups creados en el directorio backups/

setlocal enabledelayedexpansion

REM Configurando la ruta de backups
set "backup_dir=..\backups"

REM Ruta al ejecutable de WinRAR
set "winrar_path=C:\Program Files\WinRAR\WinRAR.exe"

REM Comprobar si WinRAR está instalado
if not exist "%winrar_path%" (
    echo [!] WinRAR no encontrado en "%winrar_path%"
    exit /b
)

REM Recorre cada subcarpeta dentro del directorio de backups
for /d %%D in ("%backup_dir%\*") do (
    set "folder_name=%%~nxD"
    set "zip_file=%%D\!folder_name!.zip"

    REM Verificar si hay archivos .txt en la carpeta
    dir "%%D\*.txt" >nul 2>&1
    if errorlevel 1 (
        echo [i] No hay archivos .txt en la carpeta !folder_name!, saltando...
    ) else (
        echo [+] Comprimendo archivos .txt de la carpeta: !folder_name!

        REM Comprimir todos los archivos .txt de la carpeta en un archivo zip dentro de la misma carpeta
        "%winrar_path%" a -r -afzip "!zip_file!" "%%D\*.txt"

        if exist "!zip_file!" (
            echo [*] Archivos .txt comprimidos en !zip_file!

            REM Eliminar archivos .txt después de la compresión
            del "%%D\*.txt" /Q

            echo [*] Archivos .txt eliminados de la carpeta !folder_name!
        ) else (
            echo [!] Error al comprimir la carpeta !folder_name!
        )
    )
)

echo [i] Proceso completado.
echo.

pause
