# Analizador de Evaluaciones ESO y Primaria

Herramienta de análisis y visualización para datos de evaluaciones académicas.

## 📋 Características

- **Carga múltiples archivos CSV** de diferentes cursos académicos
- **Visualizaciones interactivas** con gráficos de barras, líneas y comparaciones
- **Filtrado de datos** por nivel, nacionalidad y consecuencias de evaluación
- **Exportación a Excel** de datos filtrados
- **Comparaciones entre cursos** para analizar evoluciones y tendencias
- **Interfaz gráfica intuitiva** con pestañas organizadas

## 🚀 Instalación

### Requisitos previos

- Python 3.7 o superior
- Sistema operativo: Windows, Linux, macOS, o WSL

### Método 1: Instalación automática (recomendado)

#### En Windows:
```bash
instalar.bat
```

#### En Linux/Mac/WSL:

**Paso 1:** Instalar dependencias del sistema
```bash
sudo apt update
sudo apt install python3-venv python3-pip python3-tk
```

**Paso 2:** Ejecutar instalador
```bash
chmod +x instalar.sh
./instalar.sh
```

Este método crea un entorno virtual aislado con todas las dependencias necesarias.

### Método 2: Instalación manual

```bash
pip install pandas>=1.3.0 matplotlib>=3.4.0 seaborn>=0.11.0 openpyxl>=3.0.0
```

**Nota:** En sistemas modernos de Python (3.11+), se recomienda usar entornos virtuales:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar el programa

#### Opción 1: Con el script de ejecución
```bash
./ejecutar.sh  # Linux/Mac/WSL
```

#### Opción 2: Manualmente
```bash
python3 analizador_evaluaciones.py
```

#### Opción 3: Con entorno virtual activado
```bash
source venv/bin/activate
python3 analizador_evaluaciones.py
```

### Funcionalidades principales

#### 1. **Pestaña Resumen (📊)**
   - Muestra estadísticas básicas del archivo cargado
   - Total de registros
   - Columnas disponibles
   - Resumen por nivel educativo
   - Resumen por consecuencias de evaluación

#### 2. **Pestaña Gráficos (📈)**
   - **Gráfico por Nivel**: Distribución de estudiantes por nivel educativo
   - **Gráfico por Consecuencias**: Resultados de las evaluaciones (promociona, repite, etc.)
   - **Gráfico por Nacionalidad**: Distribución por zonas de nacionalidad

#### 3. **Pestaña Datos (📋)**
   - Visualización en tabla de los datos cargados
   - Filtros por nivel educativo
   - Exportación a Excel
   - Limitado a primeras 1000 filas para mejor rendimiento

#### 4. **Pestaña Comparaciones (🔄)**
   - Compara múltiples archivos CSV (diferentes cursos)
   - Evolución de estudiantes por nivel
   - Comparación de tasas de promoción entre cursos

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

## 🎯 Casos de uso

### Caso 1: Análisis de un solo curso
1. Clic en "Cargar CSV"
2. Seleccionar el archivo
3. Explorar las pestañas de Resumen y Gráficos

### Caso 2: Comparación entre múltiples cursos
1. Clic en "Cargar Múltiples CSV"
2. Seleccionar todos los archivos CSV que quieras comparar
3. Ir a la pestaña "Comparaciones"
4. Generar gráficos comparativos

### Caso 3: Exportar datos filtrados
1. Cargar archivo CSV
2. Ir a la pestaña "Datos"
3. Seleccionar filtro por nivel
4. Clic en "Exportar a Excel"

## 🔧 Solución de problemas

### Error de encoding
El programa intenta automáticamente con diferentes encodings (latin-1, utf-8, cp1252).
Si aún así hay problemas, verifica que tu archivo CSV esté correctamente codificado.

### Gráficos no se muestran
Asegúrate de tener instalado matplotlib y tkinter:
```bash
pip install matplotlib
```

### Archivo muy grande
Para archivos con más de 50,000 registros, la tabla de datos solo muestra las primeras 1000 filas para mantener el rendimiento. Usa los filtros para ver datos específicos o exporta a Excel.

## 📊 Ejemplos de análisis

### Análisis de rendimiento académico
- Identifica niveles con mayor tasa de repetición
- Compara resultados entre diferentes zonas de nacionalidad
- Analiza la evolución temporal de las tasas de promoción

### Análisis demográfico
- Distribución de estudiantes por nacionalidad
- Proporción de estudiantes en aulas de acogida
- Tendencias de matrícula por nivel

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de modificarlo y adaptarlo a tus necesidades.

## 📝 Notas

- Los gráficos se pueden maximizar para mejor visualización
- La exportación a Excel mantiene todos los datos (no está limitada a 1000 filas)
- Los colores de los gráficos son personalizables modificando el código

## 📧 Soporte

Para cualquier problema o sugerencia, revisa el código o modifica según tus necesidades específicas.
