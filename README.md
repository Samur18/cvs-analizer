# Analizador de Evaluaciones ESO y Primaria

Herramienta de análisis y visualización para datos de evaluaciones académicas con interfaz gráfica intuitiva.

## 🚀 Inicio Rápido

### Windows:
1. Doble clic en **`instalar.bat`** (sigue las instrucciones si no tienes Python)
2. Doble clic en **`ejecutar.bat`**

### Linux/Mac:
```bash
chmod +x instalar.sh && ./instalar.sh
./ejecutar.sh
```

**📖 ¿Primera vez?** Lee la **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** para instrucciones detalladas.

---

## 📋 Características

- Carga múltiples archivos CSV de diferentes cursos académicos
- Visualizaciones interactivas con gráficos de barras y líneas
- Filtrado de datos por nivel, nacionalidad y consecuencias de evaluación
- Exportación a Excel de datos filtrados
- Comparaciones entre cursos para analizar evoluciones y tendencias
- Interfaz gráfica con 4 pestañas organizadas (Resumen, Gráficos, Datos, Comparaciones)

## 📦 Requisitos

- Python 3.7 o superior
- Sistema operativo: Windows, Linux, macOS, o WSL
- Librerías: pandas, matplotlib, seaborn, openpyxl (se instalan automáticamente)

## 📖 Documentación

- **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** - Guía detallada de instalación y uso
- **[INSTRUCCIONES_WINDOWS.txt](INSTRUCCIONES_WINDOWS.txt)** - Resumen rápido para Windows
- **[INSTRUCCIONES_ACTUALIZACION.txt](INSTRUCCIONES_ACTUALIZACION.txt)** - Cómo actualizar el programa
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios y versiones
- **README.md** (este archivo) - Referencia técnica

## 💻 Uso del Programa

### Pestañas Disponibles

1. **📊 Resumen** - Estadísticas básicas, totales por nivel y consecuencias de evaluación
2. **📈 Gráficos** - Visualizaciones por nivel, consecuencias y nacionalidad
3. **📋 Datos** - Tabla interactiva con filtros y exportación a Excel
4. **🔄 Comparaciones** - Compara evolución entre múltiples cursos académicos

Ver [GUIA_COMPLETA.md](GUIA_COMPLETA.md) para instrucciones detalladas de uso.

## 📁 Estructura de archivos CSV esperada

El programa espera archivos CSV con separador `;` y con las siguientes columnas:

- `Curs`: Año académico (ej: 2019/2020)
- `Centre Codi`: Código del centro educativo
- `Ensenyament Codi`: Código de enseñanza
- `Nivell`: Nivel educativo (1, 2, 3, 4)
- `Zona Nacionalitat (Agrupació)`: Zona de nacionalidad
- `Aula d'acollida`: Indicador de aula de acogida
- `Conseqüències de lAvaluació`: Resultado de la evaluación
- `Número Avaluats`: Número de estudiantes evaluados

## 🔧 Solución de Problemas

Ver la sección completa de solución de problemas en [GUIA_COMPLETA.md](GUIA_COMPLETA.md).

### Problemas comunes:
- **Error de encoding:** El programa intenta automáticamente con latin-1, utf-8 y cp1252
- **Gráficos no se muestran:** Reinstala matplotlib con `pip install --upgrade matplotlib`
- **Archivo muy grande:** La tabla muestra 1000 filas, pero las exportaciones incluyen todos los datos

## 📧 Información

- **Versión:** 1.0
- **Licencia:** Proyecto educativo de uso libre
- **Tecnologías:** Python, pandas, matplotlib, seaborn, tkinter, openpyxl
