# Historial de Cambios

Todos los cambios importantes del proyecto se documentan en este archivo.

---

## [1.0.0] - 2024-12-08

### ✨ Lanzamiento Inicial

#### Añadido
- **Interfaz gráfica completa** con 4 pestañas principales
  - 📊 Pestaña Resumen: Estadísticas básicas y totales
  - 📈 Pestaña Gráficos: 3 tipos de visualizaciones interactivas
  - 📋 Pestaña Datos: Tabla con filtros y exportación
  - 🔄 Pestaña Comparaciones: Análisis multi-curso

- **Carga de archivos CSV**
  - Soporte para un solo archivo o múltiples archivos
  - Detección automática de encoding (latin-1, utf-8, cp1252)
  - Manejo de errores con mensajes claros

- **Visualizaciones**
  - Gráfico de barras por nivel educativo
  - Gráfico de barras por consecuencias de evaluación
  - Gráfico de barras por nacionalidad (Top 15)
  - Gráficos comparativos entre cursos (líneas y barras)

- **Funcionalidades**
  - Filtrado de datos por nivel educativo
  - Exportación a Excel (.xlsx)
  - Estadísticas automáticas por nivel y consecuencias
  - Comparación de evolución temporal

- **Scripts de instalación**
  - `instalar.bat` para Windows con detección automática de Python
  - `instalar.sh` para Linux/Mac con creación de entorno virtual
  - `ejecutar.bat` para Windows (ejecución con un clic)
  - `ejecutar.sh` para Linux/Mac

- **Documentación completa**
  - README.md (referencia rápida)
  - GUIA_COMPLETA.md (guía detallada paso a paso)
  - INSTRUCCIONES_WINDOWS.txt (resumen para Windows)
  - Comentarios en el código fuente

#### Características Técnicas
- Python 3.7+ compatible
- Dependencias: pandas, matplotlib, seaborn, openpyxl
- Interfaz tkinter nativa
- Optimización para archivos grandes (>50,000 registros)
- Límite de visualización de tabla: 1,000 filas (sin límite en exportaciones)

---

## Formato del Historial

Este archivo sigue el formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

### Tipos de Cambios
- **Añadido** - para nuevas funcionalidades
- **Cambiado** - para cambios en funcionalidades existentes
- **Obsoleto** - para funcionalidades que pronto se eliminarán
- **Eliminado** - para funcionalidades eliminadas
- **Corregido** - para corrección de errores
- **Seguridad** - para vulnerabilidades de seguridad

---

## [Próximas Versiones]

### Ideas para Futuras Actualizaciones
- [ ] Exportación a PDF de gráficos
- [ ] Más tipos de gráficos (circular, dispersión)
- [ ] Filtros avanzados (múltiples criterios)
- [ ] Guardado de sesiones de trabajo
- [ ] Temas de colores personalizables
- [ ] Soporte para otros formatos (Excel directo)
- [ ] Estadísticas avanzadas (desviación estándar, percentiles)
- [ ] Exportación de gráficos en alta resolución

---

## Cómo Reportar Problemas

Si encuentras algún error o tienes sugerencias:
1. Verifica que estés usando la versión más reciente (ver VERSION.txt)
2. Lee la sección de solución de problemas en GUIA_COMPLETA.md
3. Documenta el error con capturas de pantalla si es posible
4. Contacta al desarrollador o abre un issue

---

**Última actualización:** 2024-12-08
