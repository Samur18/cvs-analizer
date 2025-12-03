# 📁 ÍNDICE DE ARCHIVOS - Analizador de Evaluaciones

## 🚀 PARA EMPEZAR RÁPIDO:

### Si usas Windows:
1. Descarga todos los archivos
2. Haz doble clic en: **instalar.bat**
3. Ejecuta: **analizador_evaluaciones.py**

### Si usas Linux/Mac:
1. Descarga todos los archivos
2. Abre terminal en la carpeta
3. Ejecuta: `chmod +x instalar.sh && ./instalar.sh`
4. Ejecuta: `python3 analizador_evaluaciones.py`

---

## 📄 DESCRIPCIÓN DE ARCHIVOS

### 🔧 Archivos Ejecutables

| Archivo | Descripción | ¿Cuándo usarlo? |
|---------|-------------|-----------------|
| **analizador_evaluaciones.py** | Programa principal | Después de instalar dependencias |
| **instalar.bat** | Instalador Windows | Primera vez, en Windows |
| **instalar.sh** | Instalador Linux/Mac | Primera vez, en Linux/Mac |

### 📚 Archivos de Documentación

| Archivo | Contenido | ¿Quién debería leerlo? |
|---------|-----------|------------------------|
| **RESUMEN_PROYECTO.md** | **LEE ESTO PRIMERO** - Resumen general | Todos |
| **GUIA_RAPIDA.md** | Tutorial paso a paso | Usuarios nuevos |
| **README.md** | Documentación técnica | Desarrolladores |
| **VISTA_PREVIA_INTERFAZ.md** | Cómo se ve el programa | Curiosos |
| **LEEME_PRIMERO.md** | Este archivo | Punto de inicio |

### ⚙️ Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| **requirements.txt** | Lista de dependencias Python |

---

## 🎯 FLUJO DE TRABAJO RECOMENDADO

```
1. INSTALACIÓN
   └─► Lee: RESUMEN_PROYECTO.md
       └─► Ejecuta: instalar.bat (Windows) o instalar.sh (Linux/Mac)
           └─► Verifica instalación exitosa

2. PRIMERA EJECUCIÓN
   └─► Lee: GUIA_RAPIDA.md
       └─► Ejecuta: analizador_evaluaciones.py
           └─► Carga tu primer archivo CSV

3. USO DIARIO
   └─► Ejecuta: analizador_evaluaciones.py
       └─► Carga archivos
           └─► Explora pestañas
               └─► Genera gráficos
                   └─► Exporta resultados

4. PROBLEMAS
   └─► Consulta: README.md (sección "Solución de problemas")
       └─► Verifica: requirements.txt (dependencias instaladas)
```

---

## 📖 ORDEN DE LECTURA RECOMENDADO

### Para usuarios nuevos:
1. **LEEME_PRIMERO.md** (este archivo) ← Estás aquí
2. **RESUMEN_PROYECTO.md** ← Visión general
3. **GUIA_RAPIDA.md** ← Tutorial práctico
4. Ejecutar el programa
5. **VISTA_PREVIA_INTERFAZ.md** (opcional) ← Referencia visual

### Para usuarios experimentados:
1. **requirements.txt** ← Instalar dependencias
2. **analizador_evaluaciones.py** ← Ejecutar directamente
3. **README.md** (si hay dudas) ← Referencia técnica

### Para desarrolladores:
1. **README.md** ← Documentación técnica
2. **analizador_evaluaciones.py** ← Código fuente
3. **requirements.txt** ← Dependencias

---

## 🎨 CARACTERÍSTICAS DEL PROGRAMA

✅ Interfaz gráfica intuitiva con 4 pestañas
✅ Carga de archivos CSV con encoding automático
✅ Gráficos profesionales (barras, líneas)
✅ Filtrado y búsqueda de datos
✅ Exportación a Excel
✅ Comparación entre múltiples cursos
✅ Estadísticas detalladas

---

## 📊 DATOS COMPATIBLES

El programa funciona con archivos CSV que tengan:
- ✅ Datos de evaluaciones ESO
- ✅ Datos de evaluaciones Primaria
- ✅ Datos de competencias básicas
- ✅ Separador: punto y coma (;)
- ✅ Encoding: latin-1, utf-8, o cp1252

**Columnas esperadas:**
- Curs (curso académico)
- Nivell (nivel educativo)
- Número Avaluats (número de estudiantes)
- Conseqüències de lAvaluació (resultado)
- Zona Nacionalitat (nacionalidad)

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Necesito conocimientos de programación?**
R: No, la interfaz gráfica es muy intuitiva.

**P: ¿Funciona en mi ordenador?**
R: Sí, funciona en Windows, Mac y Linux con Python 3.7+

**P: ¿Puedo analizar archivos muy grandes?**
R: Sí, el programa está optimizado para archivos grandes.

**P: ¿Es gratis?**
R: Sí, completamente gratis y de código abierto.

**P: ¿Puedo modificarlo?**
R: Sí, el código es tuyo para modificar como quieras.

---

## 🆘 SI TIENES PROBLEMAS

1. **Error al instalar:**
   - Verifica que Python 3.7+ esté instalado
   - Ejecuta `python --version` para verificar

2. **Error al ejecutar:**
   - Asegúrate de haber instalado las dependencias
   - Ejecuta `pip install -r requirements.txt`

3. **Error al cargar CSV:**
   - Verifica que el archivo sea CSV válido
   - Comprueba que use punto y coma (;) como separador

4. **Otras dudas:**
   - Lee README.md sección "Solución de problemas"
   - Revisa GUIA_RAPIDA.md sección "Preguntas Frecuentes"

---

## 🎓 EJEMPLOS DE USO

### Ejemplo 1: Análisis rápido
```
1. Abre analizador_evaluaciones.py
2. Clic en "Cargar CSV"
3. Selecciona tu archivo
4. Ve a pestaña "Gráficos"
5. Genera los 3 gráficos
→ ¡Listo! Tienes una visión completa
```

### Ejemplo 2: Comparación de años
```
1. Abre analizador_evaluaciones.py
2. Clic en "Cargar Múltiples CSV"
3. Selecciona archivos de 2019, 2020, 2021
4. Ve a pestaña "Comparaciones"
5. Genera gráficos de evolución
→ Verás tendencias a lo largo del tiempo
```

### Ejemplo 3: Exportar datos
```
1. Abre analizador_evaluaciones.py
2. Carga tu archivo CSV
3. Ve a pestaña "Datos"
4. Selecciona filtro (ej: Nivel 1)
5. Clic en "Exportar a Excel"
→ Datos filtrados guardados en Excel
```

---

## 🎉 ¡ESTÁS LISTO!

Todo está preparado para que empieces a usar el programa.

**Siguiente paso recomendado:**
1. Si es tu primera vez: Lee **GUIA_RAPIDA.md**
2. Si quieres empezar ya: Ejecuta **instalar.bat** (Windows) o **instalar.sh** (Linux/Mac)
3. Si tienes dudas: Lee **RESUMEN_PROYECTO.md**

---

## 📧 INFORMACIÓN DEL PROYECTO

- **Versión:** 1.0
- **Fecha:** Diciembre 2024
- **Lenguaje:** Python 3.7+
- **Librerías:** pandas, matplotlib, seaborn, tkinter, openpyxl
- **Licencia:** Uso libre (educativo)

---

**¡Bienvenido al Analizador de Evaluaciones! 🎓📊**

Si tienes alguna duda, consulta los archivos de documentación.
¡Buena suerte con tu análisis de datos educativos!
