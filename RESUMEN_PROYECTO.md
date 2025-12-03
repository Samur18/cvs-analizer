# 🎓 Analizador de Evaluaciones ESO y Primaria - RESUMEN DEL PROYECTO

## 📦 Archivos Incluidos

1. **analizador_evaluaciones.py** - Programa principal con interfaz gráfica
2. **README.md** - Documentación técnica completa
3. **GUIA_RAPIDA.md** - Guía de inicio rápido para usuarios
4. **requirements.txt** - Lista de dependencias Python
5. **instalar.sh** - Script de instalación para Linux/Mac
6. **instalar.bat** - Script de instalación para Windows

## 🚀 Instalación Rápida

### Opción 1: Instalación automática

**Windows:**
```
instalar.bat
```

**Linux/Mac:**
```bash
chmod +x instalar.sh
./instalar.sh
```

### Opción 2: Instalación manual
```bash
pip install -r requirements.txt
```

## 🎯 ¿Qué hace este programa?

El programa analiza archivos CSV de evaluaciones educativas (ESO y Primaria) y proporciona:

### ✨ Funcionalidades principales:

1. **📊 Análisis estadístico**
   - Total de estudiantes evaluados
   - Distribución por niveles
   - Resultados de evaluación
   - Distribución demográfica

2. **📈 Visualizaciones gráficas**
   - Gráfico de barras por nivel
   - Gráfico de barras por consecuencias de evaluación
   - Gráfico de barras por nacionalidad

3. **🔍 Exploración de datos**
   - Tabla interactiva
   - Filtros por nivel educativo
   - Búsqueda y ordenación

4. **💾 Exportación**
   - Exportar a Excel (.xlsx)
   - Mantiene formato y filtros aplicados

5. **🔄 Comparaciones**
   - Comparar múltiples cursos académicos
   - Evolución temporal de estudiantes
   - Tasas de promoción entre años

## 📊 Datos de Ejemplo (tu archivo)

He analizado tu archivo `Dades_avaluació_ESO_curs_2019-2020.csv`:

- **Total de registros:** 24,406
- **Total de estudiantes:** 212,992
- **Niveles analizados:** 1º, 2º, 3º y 4º ESO

### Distribución por nivel:
- Nivel 1: 54,467 estudiantes
- Nivel 2: 54,538 estudiantes
- Nivel 3: 53,498 estudiantes
- Nivel 4: 50,489 estudiantes

### Top 3 resultados:
1. Promociona al curso siguiente: 111,001 (52.1%)
2. Obtiene título de ESO: 39,458 (18.5%)
3. Promociona según plan individualizado: 20,346 (9.6%)

### Top 3 nacionalidades:
1. España: 185,695 estudiantes (87.2%)
2. Centro y Sudamérica: 8,090 estudiantes (3.8%)
3. Magreb: 6,398 estudiantes (3.0%)

## 🎨 Características de la Interfaz

### Pestaña 1: Resumen 📊
- Muestra estadísticas textuales completas
- Información organizada por categorías
- Formato fácil de leer

### Pestaña 2: Gráficos 📈
- 3 tipos de gráficos interactivos
- Colores profesionales
- Valores numéricos en las barras
- Fácil de exportar (clic derecho → guardar)

### Pestaña 3: Datos 📋
- Tabla con todos los registros
- Filtro por nivel
- Scroll horizontal y vertical
- Botón de exportación a Excel

### Pestaña 4: Comparaciones 🔄
- Requiere 2+ archivos cargados
- Gráficos de evolución temporal
- Comparación de tasas de promoción

## 💡 Casos de Uso

### Para Directores de Centro:
- Analizar rendimiento académico del centro
- Identificar niveles problemáticos
- Preparar informes para la administración

### Para Investigadores:
- Estudiar tendencias educativas
- Comparar evolución en varios años
- Análisis demográfico del alumnado

### Para Profesores:
- Conocer composición del alumnado
- Identificar grupos que necesitan apoyo
- Preparar estrategias educativas

## 🔧 Requisitos Técnicos

- **Python:** 3.7 o superior
- **RAM:** Mínimo 2 GB (recomendado 4 GB para archivos grandes)
- **Espacio en disco:** 100 MB (más espacio para archivos CSV)
- **Sistema operativo:** Windows, Linux, o macOS

### Dependencias:
- pandas (análisis de datos)
- matplotlib (gráficos)
- seaborn (estilización de gráficos)
- openpyxl (exportación a Excel)

## 📚 Documentación Adicional

- **README.md**: Documentación técnica completa
- **GUIA_RAPIDA.md**: Tutorial paso a paso para usuarios
- Comentarios en el código fuente

## 🎓 Formato de Archivos CSV

El programa acepta archivos CSV con las siguientes columnas:

```
Curs | Centre Codi | Ensenyament Codi | Nivell | Zona Nacionalitat (Agrupació) | 
Aula d'acollida | Conseqüències de lAvaluació | Número Avaluats
```

### Características:
- Separador: punto y coma (`;`)
- Encoding: latin-1, utf-8, o cp1252
- Con o sin cabecera

## 🛠️ Solución de Problemas Comunes

### Error: "No module named 'pandas'"
**Solución:** Ejecuta `pip install -r requirements.txt`

### Error: "No such file or directory"
**Solución:** Asegúrate de estar en el directorio correcto

### Gráficos no se muestran
**Solución:** Verifica que tkinter esté instalado (viene con Python)

### Archivo muy lento
**Solución:** El programa está optimizado para archivos grandes, pero archivos de 100,000+ registros pueden tardar unos segundos

## 🎉 ¡Listo para Usar!

Todo está preparado. Simplemente:

1. Instala las dependencias (`instalar.bat` o `instalar.sh`)
2. Ejecuta `python analizador_evaluaciones.py`
3. Carga tus archivos CSV
4. ¡Explora tus datos!

## 📧 Soporte

Este es un proyecto educativo creado para facilitar el análisis de datos académicos.
Puedes modificar el código según tus necesidades específicas.

---

**Creado con:** Python, pandas, matplotlib, seaborn, tkinter
**Versión:** 1.0
**Última actualización:** Diciembre 2024

¡Disfruta analizando tus datos! 📊📈
