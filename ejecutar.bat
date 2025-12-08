@echo off
chcp 65001 >nul
REM Script para ejecutar el Analizador de Evaluaciones en Windows

echo =====================================================
echo   Analizador de Evaluaciones ESO - Iniciando...
echo =====================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo.
    echo Por favor, ejecuta primero "instalar.bat" para instalar Python
    echo y las dependencias necesarias.
    echo.
    pause
    exit /b 1
)

REM Verificar si el archivo principal existe
if not exist "analizador_evaluaciones.py" (
    echo ERROR: No se encuentra el archivo "analizador_evaluaciones.py"
    echo.
    echo Asegurate de ejecutar este script desde la carpeta del proyecto.
    echo.
    pause
    exit /b 1
)

REM Ejecutar el programa
echo Ejecutando el programa...
echo.
python analizador_evaluaciones.py

REM Si el programa termina con error
if %errorlevel% neq 0 (
    echo.
    echo =====================================================
    echo   El programa termino con errores
    echo =====================================================
    echo.
    echo Posibles soluciones:
    echo 1. Ejecuta "instalar.bat" nuevamente
    echo 2. Verifica que todas las librerias esten instaladas
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   Programa finalizado
echo =====================================================
echo.
pause
