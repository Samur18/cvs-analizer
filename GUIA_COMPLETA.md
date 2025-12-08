# Guía Completa - Analizador de Evaluaciones ESO y Primaria

Esta guía te mostrará cómo instalar y usar el programa paso a paso, tanto en Windows como en Linux/Mac.

---

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
   - [Windows](#en-windows)
   - [Linux/Mac](#en-linuxmac)
2. [Ejecutar el Programa](#ejecutar-el-programa)
3. [Usar el Programa](#usar-el-programa)
4. [Solución de Problemas](#solución-de-problemas)
5. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Instalación

### En Windows

#### Instalación Automática (Recomendada)

**Paso 1: Ejecutar el instalador**
1. Haz doble clic en el archivo **`instalar.bat`**
2. Se abrirá una ventana negra (terminal)

**Paso 2: Seguir las instrucciones**

**Si Python NO está instalado:**
- El instalador te preguntará si quieres abrir la página de descarga
- Escribe `S` y presiona Enter
- Se abrirá tu navegador con la página de Python

**Para instalar Python:**
1. Haz clic en el botón amarillo "Download Python 3.12.x"
2. Una vez descargado, abre el archivo
3. **MUY IMPORTANTE:** Marca la casilla "Add Python to PATH"
4. Haz clic en "Install Now"
5. Espera a que termine (5-10 minutos)
6. Vuelve a hacer doble clic en `instalar.bat`

**Si Python YA está instalado:**
- El instalador lo detectará automáticamente
- Instalará todas las librerías necesarias
- Verás "INSTALACION COMPLETADA CON EXITO"

#### Instalación Manual (Windows)

Si prefieres hacerlo manualmente:

1. **Instalar Python:**
   - Ve a https://www.python.org/downloads/
   - Descarga Python 3.12
   - **IMPORTANTE:** Marca "Add Python to PATH"
   - Instala

2. **Verificar Python:**
   - Presiona `Windows + R`
   - Escribe `cmd` y presiona Enter
   - Escribe: `python --version`
   - Deberías ver: "Python 3.12.x"

3. **Instalar librerías:**
   En el símbolo del sistema, ejecuta:
   ```
   python -m pip install pandas matplotlib seaborn openpyxl
   ```

---

### En Linux/Mac

#### Instalación Automática (Recomendada)

**Paso 1: Instalar dependencias del sistema**
```bash
sudo apt update
sudo apt install python3-venv python3-pip python3-tk
```

**Paso 2: Ejecutar instalador**
```bash
chmod +x instalar.sh
./instalar.sh
```

El instalador creará un entorno virtual y instalará todas las dependencias.

**Nota para WSL:** Si el instalador falla, ejecuta primero:
```bash
rm -rf venv
```
Y vuelve a ejecutar `./instalar.sh`

#### Instalación Manual (Linux/Mac)

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib seaborn openpyxl
```

---

## Ejecutar el Programa

### En Windows

**Forma más fácil:**
1. Haz doble clic en **`ejecutar.bat`**
2. El programa se abrirá automáticamente

**Forma alternativa:**
1. Abre el Símbolo del sistema (cmd)
2. Navega a la carpeta del proyecto
3. Ejecuta: `python analizador_evaluaciones.py`

### En Linux/Mac

**Opción 1: Con el script**
```bash
./ejecutar.sh
```

**Opción 2: Manual**
```bash
source venv/bin/activate
python3 analizador_evaluaciones.py
```

---

## Usar el Programa

### 1. Cargar Archivos CSV

#### Cargar un solo archivo:
1. Clic en **"Cargar CSV"**
2. Selecciona tu archivo CSV
3. El programa cargará los datos automáticamente

#### Cargar múltiples archivos (para comparar):
1. Clic en **"Cargar Múltiples CSV"**
2. Mantén presionado `Ctrl` (Windows/Linux) o `Cmd` (Mac)
3. Selecciona todos los archivos que quieras comparar

### 2. Explorar las Pestañas

#### 📊 Pestaña Resumen
Muestra estadísticas básicas:
- Total de estudiantes evaluados
- Distribución por niveles (1º, 2º, 3º, 4º)
- Resultados de evaluación
- Distribución por nacionalidad

#### 📈 Pestaña Gráficos
Tres tipos de visualizaciones:

1. **Gráfico por Nivel**
   - Haz clic en "Generar Gráfico por Nivel"
   - Muestra distribución de estudiantes por nivel

2. **Gráfico por Consecuencias**
   - Haz clic en "Generar Gráfico por Consecuencias"
   - Muestra resultados: promociona, repite, titula, etc.

3. **Gráfico por Nacionalidad**
   - Haz clic en "Generar Gráfico por Nacionalidad"
   - Muestra top 15 zonas de nacionalidad

**Guardar gráficos:**
- Haz clic derecho en el gráfico
- Selecciona "Guardar imagen"

#### 📋 Pestaña Datos
Tabla interactiva con filtros:

1. **Filtrar por nivel:**
   - Usa el menú desplegable
   - Selecciona "Todos" o un nivel específico (1, 2, 3, 4)

2. **Exportar a Excel:**
   - Selecciona el filtro deseado (opcional)
   - Haz clic en "Exportar a Excel"
   - Elige dónde guardar el archivo .xlsx

#### 🔄 Pestaña Comparaciones
*Solo disponible si cargaste 2 o más archivos*

1. **Comparar Evolución por Nivel:**
   - Gráfico de líneas mostrando cambios entre cursos
   - Identifica tendencias de crecimiento/decrecimiento

2. **Comparar Tasas de Promoción:**
   - Gráfico de barras comparando % de promoción
   - Identifica mejoras entre cursos

---

## Solución de Problemas

### Windows

#### "Python no se reconoce como comando"
**Causa:** Python no está en el PATH

**Solución:**
1. Desinstala Python desde Panel de Control
2. Descarga Python nuevamente
3. Al instalar, marca "Add Python to PATH"

#### "No module named 'pandas'"
**Causa:** Librerías no instaladas

**Solución:**
```
python -m pip install pandas matplotlib seaborn openpyxl
```

#### El programa se cierra inmediatamente
**Causa:** Error en la ejecución

**Solución:**
- Usa `ejecutar.bat` en lugar de hacer doble clic en el .py
- O ejecuta desde el terminal para ver errores

#### Error de permisos al instalar
**Solución:**
1. Haz clic derecho en `instalar.bat`
2. Selecciona "Ejecutar como administrador"

### Linux/Mac

#### Error al instalar dependencias del sistema
**Solución:**
```bash
sudo apt update
sudo apt install python3-venv python3-pip python3-tk
```

#### Error: "Permission denied"
**Solución:**
```bash
chmod +x instalar.sh
chmod +x ejecutar.sh
```

### Problemas Comunes (Todos los Sistemas)

#### Error de encoding al cargar CSV
**Causa:** El archivo tiene caracteres especiales

**Solución:** El programa intenta automáticamente con latin-1, utf-8 y cp1252. Si falla, abre el CSV en Excel y guárdalo como "CSV UTF-8".

#### Gráficos no se muestran
**Solución:**
```bash
pip uninstall matplotlib
pip install matplotlib
```

#### El programa está muy lento
**Causa:** Archivo muy grande

**Nota:** Para archivos de más de 50,000 registros, la tabla solo muestra las primeras 1,000 filas. Los gráficos y exportaciones usan todos los datos.

---

## Preguntas Frecuentes

### General

**P: ¿Necesito conocimientos de programación?**
R: No, la interfaz es completamente gráfica e intuitiva.

**P: ¿Funciona sin Internet?**
R: Sí, una vez instalado puedes usarlo sin conexión.

**P: ¿Cuánto espacio ocupa?**
R: Python + librerías: ~600 MB

**P: ¿Puedo desinstalar Python después?**
R: Sí, desde Panel de Control > Programas (Windows) o con `apt remove` (Linux).

### Sobre los Archivos

**P: ¿Qué formato deben tener los CSV?**
R: Separador punto y coma (`;`), encoding latin-1/utf-8/cp1252

**P: ¿Puedo mezclar archivos de ESO y Primaria?**
R: Sí, pero es mejor analizarlos por separado ya que tienen niveles diferentes.

**P: ¿Hay límite de archivos que puedo cargar?**
R: No hay límite técnico, pero se recomienda no más de 10 para mejor rendimiento.

### Sobre las Funcionalidades

**P: ¿Los gráficos se pueden modificar?**
R: Los colores y estilos se pueden cambiar editando el código Python.

**P: ¿Puedo exportar los gráficos?**
R: Sí, haz clic derecho en el gráfico y "Guardar imagen".

**P: ¿La exportación a Excel tiene límite de filas?**
R: No, exporta todos los datos (sin el límite de 1,000 filas de la tabla).

---

## Casos de Uso Ejemplo

### Caso 1: Director de Centro
**Objetivo:** Analizar rendimiento del último curso

**Pasos:**
1. Cargar CSV del curso actual
2. Revisar pestaña "Resumen"
3. Generar "Gráfico por Consecuencias"
4. Exportar datos de niveles problemáticos

### Caso 2: Investigador
**Objetivo:** Estudiar evolución de 5 años

**Pasos:**
1. Cargar múltiples CSV (2018-2023)
2. Ir a pestaña "Comparaciones"
3. Generar gráficos de evolución
4. Exportar gráficos para informe

### Caso 3: Profesor
**Objetivo:** Analizar composición del alumnado

**Pasos:**
1. Cargar CSV del curso
2. Generar "Gráfico por Nacionalidad"
3. Filtrar por nivel específico
4. Exportar a Excel

---

## Resumen Rápido

### Para empezar:
1. **Instalar:** Doble clic en `instalar.bat` (Windows) o `./instalar.sh` (Linux/Mac)
2. **Ejecutar:** Doble clic en `ejecutar.bat` (Windows) o `./ejecutar.sh` (Linux/Mac)
3. **Cargar datos:** Botón "Cargar CSV"
4. **Explorar:** Navega por las pestañas

### Orden de trabajo típico:
1. Cargar archivo(s)
2. Revisar Resumen
3. Generar Gráficos
4. Filtrar y Exportar datos específicos

---

## Ayuda Adicional

- **Documentación técnica completa:** README.md
- **Requisitos del sistema:** README.md
- **Estructura de código:** Comentarios en analizador_evaluaciones.py

---

## Actualizaciones del Programa

### ¿Cómo saber si hay actualizaciones?

1. Abre el archivo **VERSION.txt** en tu carpeta del programa
2. Compara con la versión más reciente disponible
3. Lee **CHANGELOG.md** para ver qué cambió

### ¿Cómo actualizar?

**Método Recomendado (Más Seguro):**

1. **Respalda tus datos CSV** en otra carpeta
2. **Descarga** la nueva versión completa del programa
3. **Descomprime** en una carpeta nueva
4. **Copia** tus archivos CSV de vuelta
5. **Ejecuta** `instalar.bat` (Windows) o `./instalar.sh` (Linux/Mac)
6. **Ejecuta** el programa normalmente

**Instrucciones Detalladas:**
Lee el archivo **INSTRUCCIONES_ACTUALIZACION.txt** para guía completa paso a paso.

### Historial de Versiones

Consulta **CHANGELOG.md** para ver:
- Todas las versiones publicadas
- Cambios en cada versión
- Correcciones de errores
- Nuevas funcionalidades

---

**Versión Actual:** 1.0.0
**Fecha de Lanzamiento:** 2024-12-08
**Última actualización de esta guía:** Diciembre 2024

¡Disfruta analizando tus datos! 📊📈
