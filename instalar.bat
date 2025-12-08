@echo off
chcp 65001 >nul
REM Script de instalación mejorado para Windows

echo =====================================================
echo   INSTALADOR - Analizador de Evaluaciones ESO
echo =====================================================
echo.
echo Este instalador verificara e instalara todo lo necesario
echo para ejecutar el programa.
echo.

REM Verificar si Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo   PYTHON NO ESTA INSTALADO
    echo ============================================================
    echo.
    echo Python es necesario para ejecutar este programa.
    echo.
    echo PASOS PARA INSTALAR PYTHON:
    echo.
    echo 1. Se abrira la pagina de descarga de Python
    echo 2. Descarga "Python 3.12" (version mas reciente)
    echo 3. IMPORTANTE: Durante la instalacion, marca la casilla
    echo    "Add Python to PATH" (Agregar Python al PATH)
    echo 4. Haz clic en "Install Now"
    echo 5. Espera a que termine la instalacion
    echo 6. Vuelve a ejecutar este instalador (instalar.bat)
    echo.
    echo ============================================================
    echo.
    set /p OPEN="Deseas abrir la pagina de descarga ahora? (S/N): "
    if /i "%OPEN%"=="S" (
        start https://www.python.org/downloads/
        echo.
        echo Pagina abierta en tu navegador.
        echo Despues de instalar Python, ejecuta este archivo de nuevo.
    ) else (
        echo.
        echo Puedes descargar Python manualmente desde:
        echo https://www.python.org/downloads/
    )
    echo.
    pause
    exit /b 1
)

echo   Python encontrado correctamente
python --version
echo.

REM Verificar pip
echo [2/4] Verificando pip (gestor de paquetes)...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   pip no encontrado, instalando...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
) else (
    echo   pip encontrado correctamente
    python -m pip --version
)
echo.

REM Instalar dependencias
echo [3/4] Instalando librerias necesarias...
echo   Esto puede tardar unos minutos...
echo.

python -m pip install --quiet --upgrade pandas matplotlib seaborn openpyxl

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta ejecutar manualmente:
    echo   python -m pip install pandas matplotlib seaborn openpyxl
    echo.
    pause
    exit /b 1
)

echo   Librerias instaladas correctamente
echo.

REM Verificar instalación
echo [4/4] Verificando instalacion...
python -c "import pandas, matplotlib, seaborn, openpyxl" 2>nul
if %errorlevel% neq 0 (
    echo   ADVERTENCIA: Algunas librerias no se importaron correctamente
    echo   El programa puede no funcionar correctamente
) else (
    echo   Todas las librerias verificadas correctamente
)

echo.
echo =====================================================
echo   INSTALACION COMPLETADA CON EXITO
echo =====================================================
echo.
echo El programa esta listo para usar.
echo.
echo PARA EJECUTAR EL PROGRAMA:
echo   - Opcion 1: Haz doble clic en "ejecutar.bat"
echo   - Opcion 2: Ejecuta: python analizador_evaluaciones.py
echo.
echo =====================================================
echo.
pause
