#!/bin/bash
# Script de instalación mejorado para Analizador de Evaluaciones

echo "================================================"
echo "Instalador - Analizador de Evaluaciones ESO"
echo "================================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 no está instalado."
    echo "Por favor, instala Python 3.7 o superior desde https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python encontrado: $PYTHON_VERSION"
echo ""

# Verificar si ya existe un entorno virtual
if [ -d "venv" ]; then
    echo "ℹ️  Entorno virtual ya existe. Usándolo..."
else
    echo "📦 Creando entorno virtual..."

    # Intentar crear entorno virtual
    if ! python3 -m venv venv 2>/dev/null; then
        echo ""
        echo "⚠️  No se pudo crear el entorno virtual."
        echo ""
        echo "Necesitas instalar python3-venv. Ejecuta:"
        echo ""
        echo "  sudo apt update"
        echo "  sudo apt install python3-venv python3-pip"
        echo ""
        echo "Después, vuelve a ejecutar este script."
        exit 1
    fi

    echo "✅ Entorno virtual creado"
fi

echo ""
echo "🔧 Activando entorno virtual..."

# Activar entorno virtual
source venv/bin/activate

echo "✅ Entorno virtual activado"
echo ""

# Actualizar pip dentro del venv
echo "📦 Actualizando pip..."
python -m pip install --upgrade pip --quiet

# Instalar dependencias desde requirements.txt
echo "📦 Instalando dependencias..."
echo ""

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    # Instalación manual si no existe requirements.txt
    pip install pandas>=1.3.0
    pip install matplotlib>=3.4.0
    pip install seaborn>=0.11.0
    pip install openpyxl>=3.0.0
fi

echo ""
echo "================================================"
echo "✅ Instalación completada con éxito!"
echo "================================================"
echo ""
echo "Para ejecutar el programa, usa:"
echo "  ./ejecutar.sh"
echo ""
echo "O manualmente:"
echo "  source venv/bin/activate"
echo "  python3 analizador_evaluaciones.py"
echo ""
