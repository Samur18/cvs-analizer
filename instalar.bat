@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM =====================================================
REM  INSTALADOR INTELIGENTE - Analizador de Evaluaciones
REM =====================================================
REM
REM Este instalador se adapta automaticamente a tu sistema:
REM - Si tienes Python: instala solo las librerias
REM - Si no tienes Python + tienes permisos admin: lo instala automaticamente
REM - Si no tienes Python + sin permisos admin: te guia para instalarlo manualmente
REM

echo =====================================================
echo   INSTALADOR INTELIGENTE - Analizador de Evaluaciones
echo =====================================================
echo.
echo Detectando configuracion de tu sistema...
echo.

REM ============================================
REM PASO 1: Verificar si Python está instalado
REM ============================================
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   Python encontrado correctamente
    python --version
    echo.
    goto :InstalarLibrerias
)

echo   Python no esta instalado
echo.

REM ============================================
REM PASO 2: Python no instalado - Verificar permisos de administrador
REM ============================================
echo [2/5] Verificando permisos de administrador...
net session >nul 2>&1
if %errorlevel% neq 0 (
    REM No tiene permisos de admin
    echo   No tienes permisos de administrador
    echo.
    goto :InstalacionManual
)

echo   Permisos de administrador detectados
echo.

REM ============================================
REM PASO 3: Instalar Python automaticamente
REM ============================================
echo [3/5] Instalando Python automaticamente...
echo.
echo   Esto descargara e instalara Python 3.12 (~30 MB)
echo   El proceso puede tardar 10-15 minutos.
echo.
set /p CONTINUAR="Deseas continuar con la instalacion automatica? (S/N): "
if /i not "%CONTINUAR%"=="S" (
    echo.
    echo Instalacion automatica cancelada.
    echo.
    goto :InstalacionManual
)

echo.
echo   Descargando Python 3.12.0...
echo   Por favor, espera...
echo.

REM Crear carpeta temporal
set TEMP_DIR=%TEMP%\python_installer
if not exist "!TEMP_DIR!" mkdir "!TEMP_DIR!"

REM URL del instalador de Python
set PYTHON_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
set INSTALLER_PATH=!TEMP_DIR!\python_installer.exe

REM Descargar con PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_PATH%' -UseBasicParsing } catch { exit 1 }}"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo descargar Python.
    echo.
    echo Posibles causas:
    echo - Sin conexion a Internet
    echo - Firewall bloqueando la descarga
    echo.
    goto :InstalacionManual
)

echo   Descarga completada.
echo   Instalando Python... (esto puede tardar varios minutos)
echo.

REM Instalar Python silenciosamente
"!INSTALLER_PATH!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0 Include_pip=1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: La instalacion de Python fallo.
    echo.
    goto :InstalacionManual
)

echo   Python instalado correctamente.
echo.

REM Limpiar archivos temporales
del /q "!INSTALLER_PATH!" 2>nul

REM Actualizar PATH para esta sesión
set PATH=%PATH%;%ProgramFiles%\Python312;%ProgramFiles%\Python312\Scripts

REM Verificar instalación
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   NOTA: Python se instalo correctamente pero necesitas:
    echo   1. Cerrar esta ventana
    echo   2. Abrir una nueva ventana de terminal
    echo   3. Ejecutar "instalar.bat" de nuevo
    echo.
    pause
    exit /b 0
)

echo   Python verificado y listo para usar
python --version
echo.

REM ============================================
REM PASO 4: Instalar librerias de Python
REM ============================================
:InstalarLibrerias
echo [4/5] Verificando pip (gestor de paquetes)...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   pip no encontrado, instalando...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip --quiet
) else (
    echo   pip encontrado correctamente
    python -m pip --version
)
echo.

echo [5/5] Instalando librerias necesarias...
echo   Esto puede tardar unos minutos...
echo.

python -m pip install --quiet --upgrade pandas matplotlib seaborn openpyxl

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    echo.
    echo Intenta ejecutar manualmente:
    echo   python -m pip install pandas matplotlib seaborn openpyxl
    echo.
    pause
    exit /b 1
)

echo   Librerias instaladas correctamente
echo.

REM Verificar instalación completa
echo Verificando instalacion completa...
python -c "import pandas, matplotlib, seaborn, openpyxl" 2>nul
if %errorlevel% neq 0 (
    echo   ADVERTENCIA: Algunas librerias no se importaron correctamente
    echo   El programa puede no funcionar correctamente
    echo.
) else (
    echo   Todas las librerias verificadas correctamente
    echo.
)

REM ============================================
REM Instalación completada con éxito
REM ============================================
echo =====================================================
echo   INSTALACION COMPLETADA CON EXITO
echo =====================================================
echo.
echo Todo esta listo para usar el programa.
echo.
echo PARA EJECUTAR EL PROGRAMA:
echo   - Opcion 1: Haz doble clic en "ejecutar.bat"
echo   - Opcion 2: Ejecuta: python analizador_evaluaciones.py
echo.
echo =====================================================
echo.
pause
endlocal
exit /b 0

REM ============================================
REM Instalación manual (sin permisos de admin)
REM ============================================
:InstalacionManual
echo.
echo ============================================================
echo   INSTALACION MANUAL DE PYTHON
echo ============================================================
echo.
echo No tienes permisos de administrador o la instalacion
echo automatica fallo. Necesitas instalar Python manualmente.
echo.
echo PASOS PARA INSTALAR PYTHON:
echo.
echo 1. Se abrira la pagina de descarga de Python
echo 2. Descarga "Python 3.12" (version mas reciente)
echo 3. IMPORTANTE: Durante la instalacion, marca la casilla
echo    "Add Python to PATH" (Agregar Python al PATH)
echo 4. Haz clic en "Install Now"
echo 5. Espera a que termine la instalacion
echo 6. Cierra esta ventana y ejecuta "instalar.bat" de nuevo
echo.
echo ============================================================
echo.
set /p ABRIR="Deseas abrir la pagina de descarga ahora? (S/N): "
if /i "%ABRIR%"=="S" (
    start https://www.python.org/downloads/
    echo.
    echo Pagina abierta en tu navegador.
    echo.
    echo Despues de instalar Python:
    echo 1. Cierra esta ventana
    echo 2. Ejecuta "instalar.bat" de nuevo
    echo.
) else (
    echo.
    echo Puedes descargar Python manualmente desde:
    echo https://www.python.org/downloads/
    echo.
    echo Despues de instalarlo, ejecuta "instalar.bat" de nuevo.
    echo.
)
pause
endlocal
exit /b 1
