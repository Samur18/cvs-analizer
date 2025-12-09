# 🌍 Guía Completa - Analizador de Datos Educativos

## 📚 ANALIZADOR UNIFICADO

### **analizador_evaluaciones.py** - Análisis Completo e Integrado
- ✅ 8 pestañas con todas las funcionalidades
- ✅ Análisis general de evaluaciones
- ✅ Análisis detallado de aulas de acogida
- ✅ Análisis completo de diversidad e inclusión
- ✅ Gráficos, tablas y comparativas

**Ejecutar:**
```bash
python analizador_evaluaciones.py
```

O con el entorno virtual:
```bash
./venv/bin/python analizador_evaluaciones.py
```

---

## 🎯 PESTAÑAS DISPONIBLES

1. **📊 Resumen** - Estadísticas generales
2. **📈 Gráficos** - Visualizaciones de competencias y aulas de acogida
3. **📋 Datos** - Visualización de datos crudos
4. **🔄 Comparaciones** - Comparativas entre cursos y niveles
5. **🏫 Aulas Acogida Detalle** - Análisis detallado (nivel, nacionalidad, progresión)
6. **🌍 Diversidad Cultural** - Españoles vs extranjeros, top nacionalidades
7. **⚖️ Comparativa Grupos** - Comparación entre grupos culturales
8. **🏢 Análisis por Centro** - Búsqueda y rankings de centros

---

## 📊 ANALIZADOR DE DIVERSIDAD - Pestañas Disponibles

### **PESTAÑA 1: 🏫 Aulas Acogida Detalle** ⭐ NUEVO

Análisis completo de estudiantes en aulas de acogida: curso, nacionalidad y progresión.

#### **📊 Análisis Completo**
Muestra análisis textual detallado:
- Distribución por nivel educativo
- Distribución por nacionalidad (top 10)
- Distribución por consecuencias de evaluación
- Tabla cruzada: nivel × nacionalidad
- Tabla cruzada: nacionalidad × consecuencias

#### **📈 Por Nivel y Nacionalidad**
Dos gráficos visuales:
- Estudiantes por nivel educativo (barras)
- Top 8 nacionalidades (barras horizontales)

#### **✅ Promoción por Nacionalidad**
Tasas de éxito con código de colores:
- 🟢 Verde: Tasa > 90%
- 🟠 Naranja: Tasa 75-90%
- 🔴 Rojo: Tasa < 75%

#### **📋 Tabla Detallada**
Tabla completa nivel × nacionalidad con todos los cruces de datos.

---

### **PESTAÑA 2: 🌍 Diversidad Cultural**

#### **📊 Resumen Diversidad**
Muestra:
- Total de estudiantes españoles vs extranjeros
- Top 10 nacionalidades con números y porcentajes
- Estadísticas completas de diversidad

**Ejemplo de salida:**
```
======================================================================
🌍 RESUMEN DE DIVERSIDAD CULTURAL
======================================================================

Total estudiantes: 229,406
Españoles: 191,995 (83.7%)
Extranjeros: 37,411 (16.3%)

TOP 10 NACIONALIDADES:
----------------------------------------------------------------------
 1. ESPANYA                                    191,995 (83.72%)
 2. MAGREB                                      13,287 ( 5.79%)
 3. CENTRE I SUDAMÈRICA                          9,321 ( 4.06%)
 4. RESTA UNIÓ EUROPEA                           7,421 ( 3.23%)
 5. ÀSIA I OCEANIA                               5,166 ( 2.25%)
```

#### **🥧 Gráfico Circular**
- Gráfico de pastel con distribución porcentual
- Top 7 nacionalidades + "Otros"
- España destacada (explode)

#### **📊 Top 10 Orígenes**
- Gráfico de barras horizontales
- Con números absolutos y porcentajes
- Colores degradados

#### **📈 Evolución por Nivel**
- Gráfico de barras apiladas
- Muestra cómo cambia la diversidad de 1º a 6º
- Top 6 nacionalidades representadas

---

### **PESTAÑA 3: ⚖️ Comparativa Grupos**

#### **📊 Tabla Comparativa**
Compara 6 grupos culturales:
- ESPAÑA
- MAGREB
- AMÉRICA
- EUROPA
- ASIA/OCEANÍA
- RESTO ÁFRICA

**Muestra:**
- Total de estudiantes
- Número que promocionan
- Tasa de promoción (%)
- Número que repiten
- Tasa de repetición (%)

**Ejemplo de salida:**
```
==================================================================================
⚖️ TABLA COMPARATIVA DE GRUPOS CULTURALES
==================================================================================

Grupo                     Total  Promocionan  Tasa %    Repiten  Tasa %
----------------------------------------------------------------------------------
ESPAÑA                  191,995      191,257    99.6        738    0.4
MAGREB                   13,287       13,157    99.0        130    1.0
AMÉRICA                   9,321        9,242    99.2         79    0.8
EUROPA                    7,421        7,383    99.5         38    0.5
ASIA/OCEANÍA              5,166        5,128    99.3         38    0.7
RESTO ÁFRICA              2,216        2,186    98.6         30    1.4
```

#### **📈 Tasas de Promoción**
- Gráfico horizontal comparando tasas
- Verde si > 85% (éxito)
- Rojo si < 85% (necesita atención)
- Línea de referencia en 85%

#### **📉 Brechas Educativas**
Dos gráficos lado a lado:

**Izquierda:** Brecha de promoción
- Diferencia de cada grupo con la media
- Verde = Por encima de la media
- Rojo = Por debajo de la media

**Derecha:** Brecha de repetición
- Rojo = Más repetición que la media
- Verde = Menos repetición que la media

---

### **PESTAÑA 4: 🏢 Análisis por Centro**

#### **🔍 Buscar Centro**
Ingresa código de centro (ej: 8000013) y obtén:
- Total de estudiantes
- Distribución por nacionalidad
- Número en aulas de acogida

**Ejemplo de salida:**
```
======================================================================
🏢 ANÁLISIS DEL CENTRO: 8000013
======================================================================

Total de estudiantes: 487
Total de registros: 52

Estudiantes en aulas de acogida: 3

DISTRIBUCIÓN POR NACIONALIDAD:
----------------------------------------------------------------------
  ESPANYA                                       412 ( 84.6%)
  MAGREB                                         45 (  9.2%)
  CENTRE I SUDAMÈRICA                            18 (  3.7%)
  ÀSIA I OCEANIA                                 12 (  2.5%)
```

#### **📊 Top Centros Diversos**
Lista de Top 20 centros más diversos:
- Ordenados por % de extranjeros
- Solo centros con 50+ estudiantes
- Muestra total, extranjeros y porcentaje

**Ejemplo de salida:**
```
================================================================================
📊 TOP 20 CENTROS MÁS DIVERSOS
================================================================================

#    Centro       Total  Extranjeros  % Extran.
--------------------------------------------------------------------------------
1    8012345        523          342       65.4%
2    8023456        612          387       63.2%
3    8034567        458          275       60.0%
```

#### **🏫 Centros con Aulas Acogida**
Top 20 centros con más estudiantes en aulas de acogida

---

## 💡 CASOS DE USO PRÁCTICOS

### **Caso 1: Evaluar Diversidad en tu Escuela**

1. Ejecuta `python analizador_diversidad.py`
2. Carga el archivo CSV de tu curso
3. Ve a **🏢 Análisis por Centro**
4. Ingresa tu código de centro
5. Analiza la distribución de nacionalidades

**Resultado:** Verás qué tan diverso es tu centro comparado con otros

---

### **Caso 2: Identificar Brechas Educativas**

1. Ejecuta `python analizador_diversidad.py`
2. Carga archivo CSV
3. Ve a **⚖️ Comparativa Grupos**
4. Clic en **"📉 Brechas Educativas"**
5. Observa qué grupos están por debajo de la media

**Acción:** Identifica grupos que necesitan más apoyo

---

### **Caso 3: Análisis Completo de Aulas de Acogida**

1. Ejecuta `python analizador_evaluaciones.py`
2. Carga archivo CSV
3. Ve a **📈 Gráficos**
4. Clic en **"🏫 Aulas de Acogida"**
5. Visualiza el gráfico completo con 3 paneles

**Resultado:** Análisis visual completo del programa de acogida

---

### **Caso 4: Comparar Primaria vs ESO en Diversidad**

1. Ejecuta `python analizador_diversidad.py`
2. Carga archivo de Primaria
3. Ve a **🌍 Diversidad Cultural** → **"📊 Resumen"**
4. Anota el % de extranjeros
5. Carga archivo de ESO
6. Compara los porcentajes

**Insight:** La diversidad suele disminuir de Primaria a ESO

---

### **Caso 5: Encontrar Centros Modélicos en Inclusión**

1. Ejecuta `python analizador_diversidad.py`
2. Carga archivo CSV
3. Ve a **🏢 Análisis por Centro**
4. Clic en **"📊 Top Centros Diversos"**
5. Identifica centros con alta diversidad y buenas tasas

**Uso:** Estudiar buenas prácticas de estos centros

---

## 🔄 INTEGRACIÓN ENTRE AMBOS ANALIZADORES

Ambos analizadores **comparten la misma lógica** de análisis:

```
analizador_evaluaciones.py
    ├── AnalizadorEducativo (clase principal)
    ├── obtener_estadisticas_aulas_acollida()
    ├── obtener_resumen_diversidad()
    ├── obtener_comparativa_grupos()
    └── obtener_analisis_por_centro()
           ↑
           │ (importa y usa)
           │
analizador_diversidad.py
    └── VentanaDiversidad (interfaz especializada)
```

**Ventaja:** Si actualizas la lógica en `analizador_evaluaciones.py`, automáticamente se actualiza en `analizador_diversidad.py`

---

## 📈 FUNCIONALIDADES COMPARTIDAS

Ambos analizadores pueden:
- ✅ Cargar archivos CSV de evaluación
- ✅ Detectar automáticamente tipo de archivo
- ✅ Manejar diferentes encodings (latin-1, utf-8, cp1252)
- ✅ Analizar Primaria y ESO
- ✅ Analizar aulas de acogida
- ✅ Calcular estadísticas de diversidad

---

## 🚀 INICIO RÁPIDO

### **Para Análisis General:**
```bash
cd "Dades 2025_10_Misaki Kamiya/interactive-csv-data"
python analizador_evaluaciones.py
```

### **Para Análisis de Diversidad:**
```bash
cd "Dades 2025_10_Misaki Kamiya/interactive-csv-data"
python analizador_diversidad.py
```

### **Desde Python (análisis programático):**
```python
from analizador_evaluaciones import AnalizadorEducativo

analizador = AnalizadorEducativo()
analizador.cargar_csv("archivo.csv")

# Obtener estadísticas
div = analizador.obtener_resumen_diversidad()
print(f"Extranjeros: {div['porcentaje_extranjeros']:.1f}%")

# Comparativa
comp = analizador.obtener_comparativa_grupos()
for grupo, datos in comp.items():
    print(f"{grupo}: {datos['tasa_promocion']:.1f}% promoción")
```

---

## 🎓 INTERPRETACIÓN DE RESULTADOS

### **Diversidad Cultural**
- **> 20% extranjeros** → Centro muy diverso
- **10-20% extranjeros** → Diversidad moderada
- **< 10% extranjeros** → Baja diversidad

### **Brechas Educativas**
- **Brecha < 2 puntos** → Equidad alta
- **Brecha 2-5 puntos** → Atención requerida
- **Brecha > 5 puntos** → Intervención urgente

### **Aulas de Acogida**
- **Tasa éxito similar al resto** → Programa efectivo
- **Tasa éxito menor** → Necesitan más apoyo
- **Tasa éxito mayor** → Programa muy exitoso

---

## ⚙️ REQUISITOS TÉCNICOS

Ambos analizadores usan las mismas dependencias:
```bash
pip install pandas matplotlib seaborn openpyxl
```

O usa el entorno virtual incluido:
```bash
./venv/bin/python analizador_diversidad.py
```

---

## 📞 SOPORTE Y AYUDA

### **Archivos Incluidos:**
- `analizador_evaluaciones.py` - Analizador general con aulas de acogida
- `analizador_diversidad.py` - Analizador especializado en diversidad
- `README_DIVERSIDAD.md` - Esta guía
- `NUEVAS_FUNCIONALIDADES.md` - Documentación técnica
- `funciones_diversidad_pendientes.py` - Referencia de código

### **Estructura del Proyecto:**
```
interactive-csv-data/
├── analizador_evaluaciones.py  (Analizador general - 7 pestañas)
├── analizador_diversidad.py    (Diversidad - 3 pestañas)
├── README_DIVERSIDAD.md         (Esta guía)
├── NUEVAS_FUNCIONALIDADES.md   (Documentación técnica)
└── venv/                        (Entorno virtual Python)
```

---

## 🎯 RESUMEN EJECUTIVO

### **¿Qué tengo?**
✅ DOS analizadores completos y funcionales
✅ Análisis de aulas de acogida integrado
✅ Análisis completo de diversidad cultural
✅ Comparativa entre grupos culturales
✅ Análisis por centro educativo

### **¿Qué puedo hacer?**
✅ Analizar evaluaciones ESO y Primaria
✅ Visualizar diversidad cultural
✅ Identificar brechas educativas
✅ Comparar rendimiento entre grupos
✅ Buscar centros específicos
✅ Generar reportes de inclusión

### **¿Cómo empiezo?**
1. Ejecuta `python analizador_diversidad.py`
2. Carga un archivo CSV
3. Explora las 3 pestañas
4. ¡Analiza la diversidad de tu centro!

---

**🌍 ¡Listo para analizar diversidad e inclusión educativa!**
