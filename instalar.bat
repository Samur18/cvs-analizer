@echo off
setlocal EnableDelayedExpansion

echo =====================================================
echo   INSTALADOR INTELIGENTE
echo =====================================================
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   Python encontrado
    python --version
    goto :InstalarLibrerias
)

echo   Python no esta instalado
echo.

echo [2/5] Verificando permisos de administrador...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo   No tienes permisos de administrador
    goto :InstalacionManual
)

echo   Permisos detectados
echo.

:InstalarLibrerias
echo [4/5] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    python -m ensurepip --default-pip
)
echo.

echo [5/5] Instalando librerias...
python -m pip install --quiet --upgrade pandas matplotlib seaborn openpyxl

echo.
echo =====================================================
echo   INSTALACION COMPLETADA
echo =====================================================
echo.
pause
exit /b 0

:InstalacionManual
echo.
echo Necesitas instalar Python manualmente
echo.
set /p ABRIR="Abrir pagina de descarga? (S/N): "
if /i "%ABRIR%"=="S" start https://www.python.org/downloads/
echo.
pause
exit /b 1
