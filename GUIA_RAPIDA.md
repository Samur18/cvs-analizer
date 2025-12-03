# 🚀 Guía Rápida de Uso

## Paso 1: Instalación

### En Windows:
1. Haz doble clic en `instalar.bat`
2. Espera a que se instalen las dependencias

### En Linux/Mac/WSL:

**1. Instalar dependencias del sistema (solo la primera vez):**
```bash
sudo apt update
sudo apt install python3-venv python3-pip python3-tk
```

**2. Ejecutar el instalador:**
```bash
chmod +x instalar.sh
./instalar.sh
```

El instalador creará un entorno virtual y instalará todas las librerías necesarias.

**⚠️ Nota para WSL:** Si el instalador falla, ejecuta primero:
```bash
rm -rf venv
```
Y vuelve a ejecutar `./instalar.sh`

## Paso 2: Ejecutar el programa

### Opción recomendada (con el script):
```bash
./ejecutar.sh
```

### Opción manual:
```bash
source venv/bin/activate
python3 analizador_evaluaciones.py
```

## Paso 3: Cargar tus datos

### Opción A: Un solo archivo
1. Clic en el botón **"Cargar CSV"**
2. Selecciona tu archivo CSV (ejemplo: `Dades_avaluació_ESO_curs_2019-2020.csv`)
3. El programa cargará automáticamente los datos

### Opción B: Múltiples archivos para comparar
1. Clic en el botón **"Cargar Múltiples CSV"**
2. Mantén presionado `Ctrl` (Windows/Linux) o `Cmd` (Mac)
3. Selecciona todos los archivos CSV que quieras comparar:
   - `Dades_avaluació_ESO_curs_2019-2020.csv`
   - `Dades_avaluació_ESO_curs_2020-2021.csv`
   - `Dades_avaluació_ESO_curs_2021-2022.csv`
   - etc.

## Paso 4: Explorar los datos

### 📊 Pestaña Resumen
Aquí verás:
- Total de estudiantes evaluados
- Distribución por niveles (1º, 2º, 3º, 4º ESO)
- Resultados de evaluación (promociona, repite, etc.)

**Ejemplo de información que verás:**
```
Total de registros: 24,406
Nivel 1: 8,500 estudiantes
Nivel 2: 7,200 estudiantes
...
```

### 📈 Pestaña Gráficos
Tres tipos de gráficos disponibles:

1. **Gráfico por Nivel**
   - Muestra cuántos estudiantes hay en cada nivel
   - Útil para ver la distribución

2. **Gráfico por Consecuencias**
   - Muestra resultados: promociona, repite, titula, etc.
   - Identifica tasas de éxito/fracaso

3. **Gráfico por Nacionalidad**
   - Top 15 zonas de nacionalidad más representadas
   - Análisis demográfico

### 📋 Pestaña Datos
- Tabla interactiva con todos los datos
- **Filtrar por nivel**: Usa el desplegable para ver solo 1º, 2º, 3º o 4º ESO
- **Exportar a Excel**: Guarda los datos filtrados en formato .xlsx

**Cómo exportar:**
1. Selecciona el filtro que quieras (opcional)
2. Clic en "Exportar a Excel"
3. Elige dónde guardar el archivo

### 🔄 Pestaña Comparaciones
*Disponible solo si has cargado 2 o más archivos*

1. **Comparar Evolución por Nivel**
   - Gráfico de líneas mostrando cambios entre cursos
   - Identifica tendencias de crecimiento o decrecimiento

2. **Comparar Tasas de Promoción**
   - Gráfico de barras comparando % de promoción
   - Identifica mejoras o empeoramientos entre cursos

## 💡 Consejos y Trucos

### Para análisis rápidos:
1. Carga un solo archivo
2. Ve directamente a "Gráficos"
3. Genera los 3 gráficos para tener una visión completa

### Para análisis profundos:
1. Carga múltiples archivos de diferentes años
2. Explora la pestaña "Resumen" de cada archivo
3. Usa "Comparaciones" para ver evoluciones temporales
4. Exporta datos específicos con filtros para análisis externo

### Para presentaciones:
1. Genera los gráficos que necesites
2. Haz capturas de pantalla (o exporta con el botón derecho)
3. Los gráficos están diseñados para ser profesionales

## ❓ Preguntas Frecuentes

**P: ¿Puedo cargar archivos de Primaria y ESO juntos?**
R: Sí, pero ten en cuenta que los niveles son diferentes. Es mejor analizarlos por separado.

**P: ¿Los gráficos se pueden guardar?**
R: Sí, haz clic derecho en el gráfico y selecciona "Guardar imagen"

**P: ¿Hay límite de archivos que puedo cargar?**
R: No hay límite técnico, pero para mejor rendimiento se recomienda no más de 10 archivos simultáneos.

**P: ¿Puedo modificar los colores de los gráficos?**
R: Sí, editando el archivo `analizador_evaluaciones.py`. Los colores están definidos en cada función de gráfico.

**P: ¿Funciona con archivos muy grandes?**
R: Sí, pero la tabla de datos solo muestra las primeras 1000 filas. Los gráficos y exportaciones usan todos los datos.

## 🎯 Casos de Uso Reales

### Caso 1: Director de centro educativo
**Objetivo**: Analizar resultados del último curso
**Pasos**:
1. Cargar CSV del curso actual
2. Revisar pestaña "Resumen"
3. Generar "Gráfico por Consecuencias" para ver tasas de éxito
4. Exportar datos de niveles problemáticos a Excel

### Caso 2: Investigador educativo
**Objetivo**: Estudiar evolución de 5 años
**Pasos**:
1. Cargar múltiples CSV (2018-2023)
2. Usar "Comparar Evolución por Nivel"
3. Usar "Comparar Tasas de Promoción"
4. Exportar gráficos para informe

### Caso 3: Profesor/Tutor
**Objetivo**: Analizar composición del alumnado
**Pasos**:
1. Cargar CSV del curso
2. Generar "Gráfico por Nacionalidad"
3. Filtrar por nivel específico en "Datos"
4. Exportar a Excel para compartir con equipo docente

## 📞 ¿Necesitas ayuda?

Si encuentras algún problema:
1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de que tus archivos CSV tengan el formato correcto
3. Revisa el README.md para más detalles técnicos

¡Buena suerte con tu análisis! 📊
