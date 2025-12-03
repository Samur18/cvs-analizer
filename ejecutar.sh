#!/bin/bash
# Script para ejecutar el Analizador de Evaluaciones

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ No se encontró el entorno virtual."
    echo "Por favor, ejecuta primero: ./instalar.sh"
    exit 1
fi

# Activar entorno virtual y ejecutar el programa
source venv/bin/activate
python3 analizador_evaluaciones.py
