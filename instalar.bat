@echo off
REM Script de instalación para Windows

echo ================================================
echo Instalador - Analizador de Evaluaciones ESO
echo ================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Por favor, instala Python 3.7 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo Python encontrado
python --version
echo.

REM Verificar pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no esta instalado
    pause
    exit /b 1
)

echo pip encontrado
pip --version
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo.

pip install --upgrade pandas
pip install --upgrade matplotlib
pip install --upgrade seaborn
pip install --upgrade openpyxl

echo.
echo ================================================
echo Instalacion completada con exito!
echo ================================================
echo.
echo Para ejecutar el programa, usa:
echo   python analizador_evaluaciones.py
echo.
pause
