#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Datos Educativos - ESO y Primaria
Herramienta para analizar evaluaciones académicas y competencias básicas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from enum import Enum

# Configurar estilo de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class TipoCSV(Enum):
    """Tipos de CSV soportados"""
    EVALUACION = "evaluacion"  # Dades avaluació ESO/PRI
    COMPETENCIAS = "competencias"  # Dades competències bàsiques
    DESCONOCIDO = "desconocido"


class AnalizadorEducativo:
    def __init__(self):
        self.dataframes = {}
        self.df_actual = None
        self.nombre_archivo_actual = None
        self.tipo_csv_actual = TipoCSV.DESCONOCIDO

    def detectar_tipo_csv(self, df):
        """Detecta el tipo de CSV basándose en las columnas"""
        columnas = df.columns.tolist()
        columnas_str = ' '.join(columnas).lower()

        # Buscar indicadores de CSV de Evaluación
        tiene_consecuencias = any('conseq' in col.lower() and 'avalua' in col.lower()
                                 for col in columnas)
        tiene_aula_acollida = any('aula' in col.lower() and 'acollida' in col.lower()
                                 for col in columnas)

        # Buscar indicadores de CSV de Competencias
        tiene_catala_mitjana = any('catal' in col.lower() and 'mitjana' in col.lower()
                                   for col in columnas)
        tiene_castella_mitjana = any('castell' in col.lower() and 'mitjana' in col.lower()
                                     for col in columnas)

        if tiene_consecuencias or tiene_aula_acollida:
            return TipoCSV.EVALUACION
        elif tiene_catala_mitjana or tiene_castella_mitjana:
            return TipoCSV.COMPETENCIAS
        else:
            return TipoCSV.DESCONOCIDO

    def cargar_csv(self, ruta_archivo):
        """Carga un archivo CSV con detección automática de tipo"""
        try:
            # Intentar con diferentes encodings
            for encoding in ['latin-1', 'utf-8', 'cp1252']:
                try:
                    df = pd.read_csv(ruta_archivo, sep=';', encoding=encoding)
                    nombre = Path(ruta_archivo).stem

                    # Detectar tipo de CSV
                    tipo_csv = self.detectar_tipo_csv(df)

                    self.dataframes[nombre] = {'df': df, 'tipo': tipo_csv}
                    self.df_actual = df
                    self.nombre_archivo_actual = nombre
                    self.tipo_csv_actual = tipo_csv

                    tipo_str = "Evaluación" if tipo_csv == TipoCSV.EVALUACION else \
                              "Competencias Básicas" if tipo_csv == TipoCSV.COMPETENCIAS else \
                              "Desconocido"

                    return True, f"Archivo cargado ({tipo_str}): {len(df)} registros"
                except UnicodeDecodeError:
                    continue
            return False, "Error: No se pudo decodificar el archivo"
        except Exception as e:
            return False, f"Error al cargar archivo: {str(e)}"

    def obtener_estadisticas_basicas(self):
        """Obtiene estadísticas básicas del dataframe actual"""
        if self.df_actual is None:
            return None

        stats = {
            'total_registros': len(self.df_actual),
            'columnas': list(self.df_actual.columns),
            'valores_unicos': {col: self.df_actual[col].nunique()
                              for col in self.df_actual.columns},
            'tipo_csv': self.tipo_csv_actual
        }
        return stats

    def buscar_columna(self, patrones):
        """Busca una columna que coincida con los patrones dados"""
        if self.df_actual is None:
            return None

        for col in self.df_actual.columns:
            if all(patron.lower() in col.lower() for patron in patrones):
                return col
        return None

    # ========== MÉTODOS PARA CSV DE EVALUACIÓN ==========

    def obtener_resumen_por_nivel_evaluacion(self):
        """Obtiene resumen de evaluaciones por nivel"""
        if self.df_actual is None or 'Nivell' not in self.df_actual.columns:
            return None

        col_numero = self.buscar_columna(['mero', 'Avalua'])
        if col_numero is None:
            return None

        resumen = self.df_actual.groupby('Nivell')[col_numero].sum()
        return resumen

    def obtener_resumen_por_consecuencia(self):
        """Obtiene resumen por consecuencias de evaluación"""
        if self.df_actual is None:
            return None

        col_consecuencias = self.buscar_columna(['Conseq', 'Avalua'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])

        if col_consecuencias is None or col_numero is None:
            return None

        resumen = self.df_actual.groupby(col_consecuencias)[col_numero].sum()
        return resumen

    def obtener_estadisticas_sudamerica(self):
        """Obtiene estadísticas específicas de CENTRE I SUDAMÈRICA"""
        if self.df_actual is None:
            return None

        col_nacionalidad = self.buscar_columna(['Zona', 'Nacionalitat'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])

        if col_nacionalidad is None or col_numero is None:
            return None

        # Filtrar por CENTRE I SUDAMERICA (buscar variantes)
        df_sudamerica = self.df_actual[
            self.df_actual[col_nacionalidad].str.contains('CENTRE I SUDAM', na=False, case=False)
        ]

        if len(df_sudamerica) == 0:
            return None

        stats = {
            'total_estudiantes': df_sudamerica[col_numero].sum(),
            'porcentaje_total': (df_sudamerica[col_numero].sum() / self.df_actual[col_numero].sum() * 100),
        }

        # Por nivel
        if 'Nivell' in df_sudamerica.columns:
            stats['por_nivel'] = df_sudamerica.groupby('Nivell')[col_numero].sum()

        # Por consecuencias
        col_consecuencias = self.buscar_columna(['Conseq', 'Avalua'])
        if col_consecuencias:
            stats['por_consecuencias'] = df_sudamerica.groupby(col_consecuencias)[col_numero].sum()

            # Calcular tasa de promoción
            total_sudamerica = df_sudamerica[col_numero].sum()
            promovidos = df_sudamerica[
                df_sudamerica[col_consecuencias].str.contains('Promociona', na=False)
            ][col_numero].sum()
            stats['tasa_promocion'] = (promovidos / total_sudamerica * 100) if total_sudamerica > 0 else 0

        return stats

    def obtener_competencias_sudamerica(self):
        """Obtiene competencias específicas de CENTRE I SUDAMÈRICA"""
        if self.df_actual is None:
            return None

        col_nacionalidad = self.buscar_columna(['Zona', 'nacionalitat'])
        if col_nacionalidad is None:
            return None

        # Filtrar por CENTRE I SUDAMERICA
        df_sudamerica = self.df_actual[
            self.df_actual[col_nacionalidad].str.contains('CENTRE I SUDAM', na=False, case=False)
        ]

        if len(df_sudamerica) == 0:
            return None

        stats = {}

        # Català
        col_num_cat = self.buscar_columna(['mero', 'alumnes', 'Catal'])
        col_mit_cat = self.buscar_columna(['Catal', 'mitjana'])

        if col_num_cat and col_mit_cat:
            mitjana_cat_num = pd.to_numeric(df_sudamerica[col_mit_cat], errors='coerce')
            num_cat_num = pd.to_numeric(df_sudamerica[col_num_cat], errors='coerce')

            stats['Català'] = {
                'total_alumnos': num_cat_num.sum(),
                'media': mitjana_cat_num.mean(),
                'mediana': mitjana_cat_num.median()
            }

        # Castellà
        col_num_cas = self.buscar_columna(['mero', 'alumnes', 'Castell'])
        col_mit_cas = self.buscar_columna(['Castell', 'mitjana'])

        if col_num_cas and col_mit_cas:
            mitjana_cas_num = pd.to_numeric(df_sudamerica[col_mit_cas], errors='coerce')
            num_cas_num = pd.to_numeric(df_sudamerica[col_num_cas], errors='coerce')

            stats['Castellà'] = {
                'total_alumnos': num_cas_num.sum(),
                'media': mitjana_cas_num.mean(),
                'mediana': mitjana_cas_num.median()
            }

        return stats if stats else None

    # ========== MÉTODOS PARA CSV DE COMPETENCIAS ==========

    def obtener_resumen_por_nivel_competencias(self):
        """Obtiene resumen de competencias por nivel"""
        if self.df_actual is None or 'Nivell' not in self.df_actual.columns:
            return None

        resumen = {}

        # Crear copia del dataframe para trabajar
        df_trabajo = self.df_actual.copy()

        # Buscar columnas de competencias
        col_num_catala = self.buscar_columna(['mero', 'alumnes', 'Catal'])
        col_mitjana_catala = self.buscar_columna(['Catal', 'mitjana'])
        col_num_castella = self.buscar_columna(['mero', 'alumnes', 'Castell'])
        col_mitjana_castella = self.buscar_columna(['Castell', 'mitjana'])

        if col_num_catala and col_mitjana_catala:
            # Convertir a numérico (manejar comas decimales)
            df_trabajo[col_num_catala] = pd.to_numeric(df_trabajo[col_num_catala], errors='coerce')
            df_trabajo[col_mitjana_catala] = pd.to_numeric(df_trabajo[col_mitjana_catala], errors='coerce')

            resumen_catala = df_trabajo.groupby('Nivell').agg({
                col_num_catala: 'sum',
                col_mitjana_catala: 'mean'
            })
            resumen['Català'] = resumen_catala

        if col_num_castella and col_mitjana_castella:
            # Convertir a numérico
            df_trabajo[col_num_castella] = pd.to_numeric(df_trabajo[col_num_castella], errors='coerce')
            df_trabajo[col_mitjana_castella] = pd.to_numeric(df_trabajo[col_mitjana_castella], errors='coerce')

            resumen_castella = df_trabajo.groupby('Nivell').agg({
                col_num_castella: 'sum',
                col_mitjana_castella: 'mean'
            })
            resumen['Castellà'] = resumen_castella

        return resumen if resumen else None

    def obtener_estadisticas_competencias(self):
        """Obtiene estadísticas de competencias básicas"""
        if self.df_actual is None:
            return None

        stats = {}

        # Català
        col_num_catala = self.buscar_columna(['mero', 'alumnes', 'Catal'])
        col_mitjana_catala = self.buscar_columna(['Catal', 'mitjana'])

        if col_num_catala and col_mitjana_catala:
            # Convertir a numérico (las columnas pueden venir como string)
            mitjana_catala_num = pd.to_numeric(self.df_actual[col_mitjana_catala], errors='coerce')
            num_catala_num = pd.to_numeric(self.df_actual[col_num_catala], errors='coerce')

            stats['Català'] = {
                'total_alumnos': num_catala_num.sum(),
                'media_global': mitjana_catala_num.mean(),
                'mediana': mitjana_catala_num.median(),
                'std': mitjana_catala_num.std()
            }

        # Castellà
        col_num_castella = self.buscar_columna(['mero', 'alumnes', 'Castell'])
        col_mitjana_castella = self.buscar_columna(['Castell', 'mitjana'])

        if col_num_castella and col_mitjana_castella:
            # Convertir a numérico
            mitjana_castella_num = pd.to_numeric(self.df_actual[col_mitjana_castella], errors='coerce')
            num_castella_num = pd.to_numeric(self.df_actual[col_num_castella], errors='coerce')

            stats['Castellà'] = {
                'total_alumnos': num_castella_num.sum(),
                'media_global': mitjana_castella_num.mean(),
                'mediana': mitjana_castella_num.median(),
                'std': mitjana_castella_num.std()
            }

        return stats if stats else None


class VentanaAnalisis:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Datos Educativos - ESO y Primaria")
        self.root.geometry("1400x900")

        self.analizador = AnalizadorEducativo()
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""

        # Frame superior - Controles
        frame_superior = ttk.Frame(self.root, padding="10")
        frame_superior.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))

        # Botones de carga
        ttk.Button(frame_superior, text="Cargar CSV",
                   command=self.cargar_archivo).grid(row=0, column=0, padx=5)

        ttk.Button(frame_superior, text="Cargar Múltiples CSV",
                   command=self.cargar_multiples_archivos).grid(row=0, column=1, padx=5)

        # Label de archivo actual
        self.label_archivo = ttk.Label(frame_superior, text="Ningún archivo cargado",
                                       font=('Arial', 10, 'bold'))
        self.label_archivo.grid(row=0, column=2, padx=20)

        # Label de tipo de CSV
        self.label_tipo = ttk.Label(frame_superior, text="",
                                    font=('Arial', 9), foreground='blue')
        self.label_tipo.grid(row=0, column=3, padx=10)

        # Frame central - Notebook con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Crear pestañas
        self.crear_pestana_resumen()
        self.crear_pestana_visualizaciones()
        self.crear_pestana_datos()
        self.crear_pestana_comparaciones()

    def crear_pestana_resumen(self):
        """Crea la pestaña de resumen estadístico"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Resumen")

        # Text widget para mostrar estadísticas
        self.texto_resumen = tk.Text(frame, wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.texto_resumen.yview)
        self.texto_resumen.configure(yscrollcommand=scrollbar.set)

        self.texto_resumen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def crear_pestana_visualizaciones(self):
        """Crea la pestaña de visualizaciones"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📈 Gráficos")

        # Frame de controles
        self.frame_controles_graficos = ttk.Frame(frame)
        self.frame_controles_graficos.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Los botones se crearán dinámicamente según el tipo de CSV

        # Frame para el gráfico
        self.frame_grafico = ttk.Frame(frame)
        self.frame_grafico.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

    def crear_pestana_datos(self):
        """Crea la pestaña de visualización de datos en tabla"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Datos")

        # Frame de controles
        frame_controles = ttk.Frame(frame)
        frame_controles.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame_controles, text="Filtrar por Nivel:").grid(row=0, column=0, padx=5)
        self.combo_nivel = ttk.Combobox(frame_controles, state='readonly', width=15)
        self.combo_nivel.grid(row=0, column=1, padx=5)
        self.combo_nivel.bind('<<ComboboxSelected>>', self.actualizar_tabla)

        ttk.Button(frame_controles, text="Mostrar Todos",
                   command=self.mostrar_todos_datos).grid(row=0, column=2, padx=5)

        ttk.Button(frame_controles, text="Exportar a Excel",
                   command=self.exportar_excel).grid(row=0, column=3, padx=5)

        # Treeview para mostrar datos
        self.tree = ttk.Treeview(frame, show='headings')
        scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=1, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=2, column=0, sticky=(tk.W, tk.E))

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

    def crear_pestana_comparaciones(self):
        """Crea la pestaña para comparar múltiples archivos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔄 Comparaciones")

        ttk.Label(frame, text="Comparación entre diferentes cursos académicos",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)

        # Frame de controles (se actualizará dinámicamente)
        self.frame_controles_comparacion = ttk.Frame(frame)
        self.frame_controles_comparacion.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Frame para gráfico de comparación
        self.frame_comparacion = ttk.Frame(frame)
        self.frame_comparacion.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

    def actualizar_botones_graficos(self):
        """Actualiza los botones de gráficos según el tipo de CSV"""
        # Limpiar botones anteriores
        for widget in self.frame_controles_graficos.winfo_children():
            widget.destroy()

        if self.analizador.tipo_csv_actual == TipoCSV.EVALUACION:
            # Botones para CSV de Evaluación
            ttk.Button(self.frame_controles_graficos, text="Gráfico por Nivel",
                       command=self.grafico_por_nivel).grid(row=0, column=0, padx=5)

            ttk.Button(self.frame_controles_graficos, text="Gráfico por Consecuencias",
                       command=self.grafico_por_consecuencias).grid(row=0, column=1, padx=5)

            ttk.Button(self.frame_controles_graficos, text="Gráfico por Nacionalidad",
                       command=self.grafico_por_nacionalidad).grid(row=0, column=2, padx=5)

            # NUEVO: Botón específico para Sudamérica
            ttk.Button(self.frame_controles_graficos, text="📊 Análisis Sudamérica",
                       command=self.grafico_sudamerica_evaluacion).grid(row=0, column=3, padx=5)

        elif self.analizador.tipo_csv_actual == TipoCSV.COMPETENCIAS:
            # Botones para CSV de Competencias
            ttk.Button(self.frame_controles_graficos, text="Gráfico Medias por Nivel",
                       command=self.grafico_competencias_por_nivel).grid(row=0, column=0, padx=5)

            ttk.Button(self.frame_controles_graficos, text="Comparación Català vs Castellà",
                       command=self.grafico_comparacion_lenguas).grid(row=0, column=1, padx=5)

            ttk.Button(self.frame_controles_graficos, text="Distribución de Notas",
                       command=self.grafico_distribucion_notas).grid(row=0, column=2, padx=5)

            # NUEVO: Botón específico para Sudamérica
            ttk.Button(self.frame_controles_graficos, text="📊 Análisis Sudamérica",
                       command=self.grafico_sudamerica_competencias).grid(row=0, column=3, padx=5)

    def actualizar_botones_comparacion(self):
        """Actualiza los botones de comparación según el tipo de CSV"""
        # Limpiar botones anteriores
        for widget in self.frame_controles_comparacion.winfo_children():
            widget.destroy()

        if self.analizador.tipo_csv_actual == TipoCSV.EVALUACION:
            ttk.Button(self.frame_controles_comparacion, text="Comparar Evolución por Nivel",
                       command=self.comparar_evolucion_niveles).grid(row=0, column=0, padx=5)

            ttk.Button(self.frame_controles_comparacion, text="Comparar Tasas de Promoción",
                       command=self.comparar_tasas_promocion).grid(row=0, column=1, padx=5)

        elif self.analizador.tipo_csv_actual == TipoCSV.COMPETENCIAS:
            ttk.Button(self.frame_controles_comparacion, text="Evolución de Medias",
                       command=self.comparar_evolucion_competencias).grid(row=0, column=0, padx=5)

    def cargar_archivo(self):
        """Carga un archivo CSV individual"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if ruta:
            exito, mensaje = self.analizador.cargar_csv(ruta)
            if exito:
                tipo_str = "Evaluación" if self.analizador.tipo_csv_actual == TipoCSV.EVALUACION else \
                          "Competencias Básicas" if self.analizador.tipo_csv_actual == TipoCSV.COMPETENCIAS else \
                          "Desconocido"

                self.label_archivo.config(text=f"Archivo: {self.analizador.nombre_archivo_actual}")
                self.label_tipo.config(text=f"Tipo: {tipo_str}")

                self.actualizar_resumen()
                self.actualizar_filtros()
                self.actualizar_botones_graficos()
                self.actualizar_botones_comparacion()
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)

    def cargar_multiples_archivos(self):
        """Carga múltiples archivos CSV"""
        rutas = filedialog.askopenfilenames(
            title="Seleccionar archivos CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if rutas:
            cargados = 0
            for ruta in rutas:
                exito, _ = self.analizador.cargar_csv(ruta)
                if exito:
                    cargados += 1

            messagebox.showinfo("Éxito", f"{cargados} archivos cargados correctamente")
            self.actualizar_resumen()
            self.actualizar_filtros()
            self.actualizar_botones_graficos()
            self.actualizar_botones_comparacion()

    def actualizar_resumen(self):
        """Actualiza el texto del resumen estadístico"""
        self.texto_resumen.delete(1.0, tk.END)

        if self.analizador.df_actual is None:
            self.texto_resumen.insert(tk.END, "No hay datos cargados")
            return

        stats = self.analizador.obtener_estadisticas_basicas()

        texto = ""

        # Si hay múltiples archivos cargados, mostrar la lista
        if len(self.analizador.dataframes) > 1:
            texto += f"{'='*70}\n"
            texto += f"ARCHIVOS CARGADOS EN SESIÓN: {len(self.analizador.dataframes)}\n"
            texto += f"{'='*70}\n"
            for i, (nombre, info) in enumerate(self.analizador.dataframes.items(), 1):
                tipo_archivo = info['tipo']
                tipo_str = "Evaluación" if tipo_archivo == TipoCSV.EVALUACION else \
                          "Competencias" if tipo_archivo == TipoCSV.COMPETENCIAS else \
                          "Desconocido"
                marcador = "→ " if nombre == self.analizador.nombre_archivo_actual else "  "
                num_registros = len(info['df'])
                texto += f"{marcador}{i}. {nombre}\n"
                texto += f"   Tipo: {tipo_str} | Registros: {num_registros:,}\n"
            texto += f"\n{'='*70}\n"
            texto += f"DETALLE DEL ARCHIVO ACTUAL → {self.analizador.nombre_archivo_actual}\n"
            texto += f"{'='*70}\n\n"
        else:
            texto += f"{'='*70}\n"
            texto += f"RESUMEN DEL ARCHIVO: {self.analizador.nombre_archivo_actual}\n"
            texto += f"{'='*70}\n\n"

        tipo_str = "Evaluación" if stats['tipo_csv'] == TipoCSV.EVALUACION else \
                  "Competencias Básicas" if stats['tipo_csv'] == TipoCSV.COMPETENCIAS else \
                  "Desconocido"
        texto += f"Tipo de archivo: {tipo_str}\n"
        texto += f"Total de registros: {stats['total_registros']:,}\n\n"
        texto += f"Columnas disponibles:\n"
        for i, col in enumerate(stats['columnas'], 1):
            valores_unicos = stats['valores_unicos'][col]
            texto += f"  {i}. {col}: {valores_unicos} valores únicos\n"

        # Resumen específico según el tipo
        if self.analizador.tipo_csv_actual == TipoCSV.EVALUACION:
            texto += self.generar_resumen_evaluacion()
        elif self.analizador.tipo_csv_actual == TipoCSV.COMPETENCIAS:
            texto += self.generar_resumen_competencias()

        self.texto_resumen.insert(tk.END, texto)

    def generar_resumen_evaluacion(self):
        """Genera resumen para CSV de evaluación"""
        texto = f"\n{'='*70}\n"
        texto += "RESUMEN POR NIVEL\n"
        texto += f"{'='*70}\n"

        resumen_nivel = self.analizador.obtener_resumen_por_nivel_evaluacion()
        if resumen_nivel is not None:
            for nivel, total in resumen_nivel.items():
                texto += f"  Nivel {nivel}: {total:,} estudiantes evaluados\n"

        texto += f"\n{'='*70}\n"
        texto += "RESUMEN POR CONSECUENCIAS DE EVALUACIÓN\n"
        texto += f"{'='*70}\n"

        resumen_consec = self.analizador.obtener_resumen_por_consecuencia()
        if resumen_consec is not None:
            for consec, total in resumen_consec.items():
                texto += f"  {consec}: {total:,} estudiantes\n"

        # NUEVA SECCIÓN: Análisis específico de CENTRE I SUDAMÈRICA
        texto += f"\n{'='*70}\n"
        texto += "📊 ANÁLISIS ESPECÍFICO: CENTRE I SUDAMÈRICA\n"
        texto += f"{'='*70}\n"

        stats_sudamerica = self.analizador.obtener_estadisticas_sudamerica()
        if stats_sudamerica:
            texto += f"\nTotal estudiantes: {stats_sudamerica['total_estudiantes']:,}\n"
            texto += f"Porcentaje del total: {stats_sudamerica['porcentaje_total']:.2f}%\n"

            if 'tasa_promocion' in stats_sudamerica:
                texto += f"Tasa de promoción: {stats_sudamerica['tasa_promocion']:.2f}%\n"

            if 'por_nivel' in stats_sudamerica:
                texto += f"\nDistribución por nivel:\n"
                for nivel, total in stats_sudamerica['por_nivel'].items():
                    texto += f"  Nivel {nivel}: {total:,} estudiantes\n"

            if 'por_consecuencias' in stats_sudamerica:
                texto += f"\nPrincipales consecuencias:\n"
                top_consec = stats_sudamerica['por_consecuencias'].sort_values(ascending=False).head(5)
                for consec, total in top_consec.items():
                    texto += f"  {consec}: {total:,}\n"
        else:
            texto += "\nNo hay datos de CENTRE I SUDAMÈRICA en este archivo.\n"

        return texto

    def generar_resumen_competencias(self):
        """Genera resumen para CSV de competencias"""
        texto = f"\n{'='*70}\n"
        texto += "RESUMEN DE COMPETENCIAS BÁSICAS\n"
        texto += f"{'='*70}\n"

        stats_comp = self.analizador.obtener_estadisticas_competencias()
        if stats_comp:
            for lengua, datos in stats_comp.items():
                texto += f"\n{lengua}:\n"
                texto += f"  Total alumnos: {datos['total_alumnos']:,.0f}\n"
                texto += f"  Media global: {datos['media_global']:.2f}\n"
                texto += f"  Mediana: {datos['mediana']:.2f}\n"
                texto += f"  Desviación estándar: {datos['std']:.2f}\n"

        texto += f"\n{'='*70}\n"
        texto += "MEDIAS POR NIVEL\n"
        texto += f"{'='*70}\n"

        resumen_nivel = self.analizador.obtener_resumen_por_nivel_competencias()
        if resumen_nivel:
            for lengua, df_resumen in resumen_nivel.items():
                texto += f"\n{lengua}:\n"
                for nivel, row in df_resumen.iterrows():
                    col_num = [c for c in df_resumen.columns if 'mero' in c][0]
                    col_mit = [c for c in df_resumen.columns if 'mitjana' in c][0]
                    texto += f"  Nivel {nivel}: {row[col_num]:,.0f} alumnos, media {row[col_mit]:.2f}\n"

        # NUEVA SECCIÓN: Análisis específico de CENTRE I SUDAMÈRICA
        texto += f"\n{'='*70}\n"
        texto += "📊 ANÁLISIS ESPECÍFICO: CENTRE I SUDAMÈRICA\n"
        texto += f"{'='*70}\n"

        stats_sudamerica = self.analizador.obtener_competencias_sudamerica()
        if stats_sudamerica:
            for lengua, datos in stats_sudamerica.items():
                texto += f"\n{lengua}:\n"
                texto += f"  Total alumnos: {datos['total_alumnos']:,.0f}\n"
                texto += f"  Media: {datos['media']:.2f}\n"
                texto += f"  Mediana: {datos['mediana']:.2f}\n"
        else:
            texto += "\nNo hay datos de CENTRE I SUDAMÈRICA en este archivo.\n"

        return texto

    def actualizar_filtros(self):
        """Actualiza los valores de los filtros (comboboxes)"""
        if self.analizador.df_actual is not None and 'Nivell' in self.analizador.df_actual.columns:
            niveles = ['Todos'] + sorted(self.analizador.df_actual['Nivell'].unique().tolist())
            self.combo_nivel['values'] = niveles
            self.combo_nivel.current(0)

    # ========== GRÁFICOS PARA EVALUACIÓN ==========

    def grafico_por_nivel(self):
        """Genera gráfico de barras por nivel (Evaluación)"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))

        resumen = self.analizador.obtener_resumen_por_nivel_evaluacion()
        if resumen is not None:
            resumen.plot(kind='bar', ax=ax, color='steelblue')
            ax.set_title('Número de Estudiantes Evaluados por Nivel', fontsize=14, fontweight='bold')
            ax.set_xlabel('Nivel', fontsize=12)
            ax.set_ylabel('Número de Estudiantes', fontsize=12)
            ax.tick_params(axis='x', rotation=0)

            # Añadir valores en las barras
            for i, v in enumerate(resumen):
                ax.text(i, v + max(resumen)*0.01, f'{int(v):,}',
                       ha='center', va='bottom', fontsize=10)

            plt.tight_layout()

            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_por_consecuencias(self):
        """Genera gráfico por consecuencias de evaluación"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))

        resumen = self.analizador.obtener_resumen_por_consecuencia()
        if resumen is not None:
            resumen = resumen.sort_values(ascending=False)
            resumen.plot(kind='barh', ax=ax, color='coral')
            ax.set_title('Distribución por Consecuencias de Evaluación',
                        fontsize=14, fontweight='bold')
            ax.set_xlabel('Número de Estudiantes', fontsize=12)
            ax.set_ylabel('Consecuencia', fontsize=12)

            # Añadir valores en las barras
            for i, v in enumerate(resumen):
                ax.text(v + max(resumen)*0.01, i, f'{int(v):,}',
                       ha='left', va='center', fontsize=9)

            plt.tight_layout()

            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Advertencia", "No se encontró la columna de consecuencias")

    def grafico_por_nacionalidad(self):
        """Genera gráfico por zona de nacionalidad"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        col_nacionalidad = self.analizador.buscar_columna(['Zona', 'Nacionalitat'])
        col_numero = self.analizador.buscar_columna(['mero', 'Avalua'])

        if col_nacionalidad is None or col_numero is None:
            messagebox.showwarning("Advertencia", "Columnas necesarias no encontradas")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))

        resumen = self.analizador.df_actual.groupby(col_nacionalidad)[col_numero].sum()
        resumen = resumen.sort_values(ascending=False).head(15)  # Top 15

        resumen.plot(kind='barh', ax=ax, color='mediumseagreen')
        ax.set_title('Top 15 Zonas de Nacionalidad',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Número de Estudiantes', fontsize=12)
        ax.set_ylabel('Zona de Nacionalidad', fontsize=12)

        # Añadir valores
        for i, v in enumerate(resumen):
            ax.text(v + max(resumen)*0.01, i, f'{int(v):,}',
                   ha='left', va='center', fontsize=9)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ========== GRÁFICOS PARA COMPETENCIAS ==========

    def grafico_competencias_por_nivel(self):
        """Genera gráfico de medias de competencias por nivel"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))

        resumen = self.analizador.obtener_resumen_por_nivel_competencias()
        if resumen:
            x = np.arange(len(resumen.get('Català', pd.DataFrame()).index))
            width = 0.35

            if 'Català' in resumen:
                df_cat = resumen['Català']
                col_mit_cat = [c for c in df_cat.columns if 'mitjana' in c][0]
                medias_cat = df_cat[col_mit_cat].values
                ax.bar(x - width/2, medias_cat, width, label='Català', color='steelblue')

            if 'Castellà' in resumen:
                df_cas = resumen['Castellà']
                col_mit_cas = [c for c in df_cas.columns if 'mitjana' in c][0]
                medias_cas = df_cas[col_mit_cas].values
                ax.bar(x + width/2, medias_cas, width, label='Castellà', color='coral')

            ax.set_xlabel('Nivel', fontsize=12)
            ax.set_ylabel('Media', fontsize=12)
            ax.set_title('Medias de Competencias por Nivel', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(df_cat.index if 'Català' in resumen else df_cas.index)
            ax.legend()
            ax.set_ylim(0, 100)
            ax.grid(axis='y', alpha=0.3)

            plt.tight_layout()

            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Advertencia", "No se pudieron calcular las competencias")

    def grafico_comparacion_lenguas(self):
        """Genera gráfico comparando Català y Castellà"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        stats = self.analizador.obtener_estadisticas_competencias()
        if not stats:
            messagebox.showwarning("Advertencia", "No se pudieron calcular estadísticas")
            return

        # Crear figura con 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        lenguas = list(stats.keys())
        medias = [stats[l]['media_global'] for l in lenguas]
        colores = ['steelblue', 'coral']

        # Gráfico 1: Medias globales
        bars = ax1.bar(lenguas, medias, color=colores)
        ax1.set_title('Comparación de Medias Globales', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Media', fontsize=11)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)

        for bar, media in zip(bars, medias):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{media:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Gráfico 2: Desviaciones estándar
        stds = [stats[l]['std'] for l in lenguas]
        bars2 = ax2.bar(lenguas, stds, color=colores, alpha=0.7)
        ax2.set_title('Desviación Estándar', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Desviación Estándar', fontsize=11)
        ax2.grid(axis='y', alpha=0.3)

        for bar, std in zip(bars2, stds):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{std:.2f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_distribucion_notas(self):
        """Genera histograma de distribución de notas"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        col_cat = self.analizador.buscar_columna(['Catal', 'mitjana'])
        col_cas = self.analizador.buscar_columna(['Castell', 'mitjana'])

        if col_cat is None and col_cas is None:
            messagebox.showwarning("Advertencia", "No se encontraron columnas de medias")
            return

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))

        if col_cat:
            # Convertir a numérico antes de graficar
            datos_cat = pd.to_numeric(self.analizador.df_actual[col_cat], errors='coerce').dropna()
            ax.hist(datos_cat, bins=20, alpha=0.6,
                   label='Català', color='steelblue', edgecolor='black')

        if col_cas:
            # Convertir a numérico antes de graficar
            datos_cas = pd.to_numeric(self.analizador.df_actual[col_cas], errors='coerce').dropna()
            ax.hist(datos_cas, bins=20, alpha=0.6,
                   label='Castellà', color='coral', edgecolor='black')

        ax.set_title('Distribución de Notas Medias', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nota Media', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ========== GRÁFICOS ESPECÍFICOS PARA SUDAMÉRICA ==========

    def grafico_sudamerica_evaluacion(self):
        """Genera gráfico comparativo para CENTRE I SUDAMÈRICA (Evaluación)"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        stats_sudamerica = self.analizador.obtener_estadisticas_sudamerica()
        if not stats_sudamerica:
            messagebox.showwarning("Advertencia", "No hay datos de CENTRE I SUDAMÈRICA en este archivo")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura con 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Gráfico 1: Distribución por nivel (Sudamérica vs Total)
        resumen_total = self.analizador.obtener_resumen_por_nivel_evaluacion()
        resumen_sudamerica = stats_sudamerica['por_nivel']

        x = np.arange(len(resumen_total))
        width = 0.35

        ax1.bar(x - width/2, resumen_total.values, width, label='Total', color='steelblue', alpha=0.7)
        ax1.bar(x + width/2, resumen_sudamerica.values, width, label='CENTRE I SUDAMÈRICA', color='coral')

        ax1.set_xlabel('Nivel', fontsize=12)
        ax1.set_ylabel('Número de Estudiantes', fontsize=12)
        ax1.set_title('Comparación por Nivel', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(resumen_total.index)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # Gráfico 2: Porcentaje y Tasa de Promoción
        categorias = ['% del Total', 'Tasa Promoción']
        valores = [stats_sudamerica['porcentaje_total'], stats_sudamerica.get('tasa_promocion', 0)]

        bars = ax2.bar(categorias, valores, color=['mediumseagreen', 'gold'], edgecolor='darkgreen', linewidth=2)
        ax2.set_ylabel('Porcentaje (%)', fontsize=12)
        ax2.set_title('Indicadores CENTRE I SUDAMÈRICA', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)

        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_sudamerica_competencias(self):
        """Genera gráfico comparativo para CENTRE I SUDAMÈRICA (Competencias)"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        stats_sudamerica = self.analizador.obtener_competencias_sudamerica()
        if not stats_sudamerica:
            messagebox.showwarning("Advertencia", "No hay datos de CENTRE I SUDAMÈRICA en este archivo")
            return

        stats_total = self.analizador.obtener_estadisticas_competencias()

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))

        lenguas = list(stats_sudamerica.keys())
        x = np.arange(len(lenguas))
        width = 0.35

        medias_total = [stats_total[l]['media_global'] for l in lenguas]
        medias_sudamerica = [stats_sudamerica[l]['media'] for l in lenguas]

        bars1 = ax.bar(x - width/2, medias_total, width, label='Media Global', color='steelblue', alpha=0.7)
        bars2 = ax.bar(x + width/2, medias_sudamerica, width, label='CENTRE I SUDAMÈRICA', color='coral')

        ax.set_xlabel('Lengua', fontsize=12)
        ax.set_ylabel('Media', fontsize=12)
        ax.set_title('Comparación de Medias: CENTRE I SUDAMÈRICA vs Total', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(lenguas)
        ax.legend()
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)

        # Añadir valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ========== TABLA DE DATOS ==========

    def actualizar_tabla(self, event=None):
        """Actualiza la tabla de datos según filtros"""
        if self.analizador.df_actual is None:
            return

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener filtro
        nivel_seleccionado = self.combo_nivel.get()

        # Filtrar datos
        if nivel_seleccionado == 'Todos' or nivel_seleccionado == '':
            df_filtrado = self.analizador.df_actual
        else:
            df_filtrado = self.analizador.df_actual[
                self.analizador.df_actual['Nivell'] == nivel_seleccionado
            ]

        # Configurar columnas
        self.tree['columns'] = list(df_filtrado.columns)
        for col in df_filtrado.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Insertar datos (limitar a primeras 1000 filas para performance)
        for idx, row in df_filtrado.head(1000).iterrows():
            self.tree.insert('', 'end', values=list(row))

    def mostrar_todos_datos(self):
        """Muestra todos los datos sin filtrar"""
        self.combo_nivel.set('Todos')
        self.actualizar_tabla()

    def exportar_excel(self):
        """Exporta los datos filtrados a Excel"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if ruta:
            try:
                nivel_seleccionado = self.combo_nivel.get()
                if nivel_seleccionado == 'Todos' or nivel_seleccionado == '':
                    df_exportar = self.analizador.df_actual
                else:
                    df_exportar = self.analizador.df_actual[
                        self.analizador.df_actual['Nivell'] == nivel_seleccionado
                    ]

                df_exportar.to_excel(ruta, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    # ========== COMPARACIONES ==========

    def comparar_evolucion_niveles(self):
        """Compara la evolución de estudiantes por nivel entre diferentes cursos (Evaluación)"""
        if len(self.analizador.dataframes) < 2:
            messagebox.showwarning("Advertencia",
                                 "Necesitas cargar al menos 2 archivos para comparar")
            return

        # Limpiar frame anterior
        for widget in self.frame_comparacion.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 7))

        # Recopilar datos de todos los archivos de tipo EVALUACION
        datos_comparacion = {}
        for nombre, info in self.analizador.dataframes.items():
            df = info['df']
            tipo = info['tipo']

            if tipo == TipoCSV.EVALUACION:
                col_numero = self.analizador.buscar_columna(['mero', 'Avalua'])
                if 'Nivell' in df.columns and col_numero:
                    resumen = df.groupby('Nivell')[col_numero].sum()
                    datos_comparacion[nombre] = resumen

        if not datos_comparacion:
            messagebox.showwarning("Advertencia", "No hay suficientes archivos de evaluación")
            return

        # Crear gráfico de líneas
        for nombre, datos in datos_comparacion.items():
            ax.plot(datos.index, datos.values, marker='o', label=nombre, linewidth=2)

        ax.set_title('Evolución de Estudiantes por Nivel (Comparación entre Cursos)',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Nivel', fontsize=12)
        ax.set_ylabel('Número de Estudiantes', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_comparacion)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def comparar_tasas_promocion(self):
        """Compara tasas de promoción entre diferentes cursos"""
        if len(self.analizador.dataframes) < 2:
            messagebox.showwarning("Advertencia",
                                 "Necesitas cargar al menos 2 archivos para comparar")
            return

        # Limpiar frame anterior
        for widget in self.frame_comparacion.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 7))

        # Calcular tasas de promoción
        datos_promocion = {}
        for nombre, info in self.analizador.dataframes.items():
            df = info['df']
            tipo = info['tipo']

            if tipo == TipoCSV.EVALUACION:
                # Buscar columnas correctas
                col_consecuencias = None
                col_numero = None

                for col in df.columns:
                    if 'Conseq' in col and 'Avalua' in col:
                        col_consecuencias = col
                    if 'mero' in col and 'Avalua' in col:
                        col_numero = col

                if col_consecuencias and col_numero:
                    total = df[col_numero].sum()
                    promovidos = df[df[col_consecuencias].str.contains('Promociona', na=False)][col_numero].sum()
                    tasa = (promovidos / total * 100) if total > 0 else 0
                    datos_promocion[nombre] = tasa

        if not datos_promocion:
            messagebox.showwarning("Advertencia", "No se pudieron calcular las tasas de promoción")
            return

        # Crear gráfico de barras
        cursos = list(datos_promocion.keys())
        tasas = list(datos_promocion.values())

        bars = ax.bar(range(len(cursos)), tasas, color='lightgreen', edgecolor='darkgreen')
        ax.set_xticks(range(len(cursos)))
        ax.set_xticklabels(cursos, rotation=45, ha='right')
        ax.set_title('Comparación de Tasas de Promoción entre Cursos',
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Tasa de Promoción (%)', fontsize=12)
        ax.set_ylim(0, 100)

        # Añadir valores en las barras
        for i, (bar, tasa) in enumerate(zip(bars, tasas)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{tasa:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_comparacion)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def comparar_evolucion_competencias(self):
        """Compara la evolución de las medias de competencias entre cursos"""
        if len(self.analizador.dataframes) < 2:
            messagebox.showwarning("Advertencia",
                                 "Necesitas cargar al menos 2 archivos para comparar")
            return

        # Limpiar frame anterior
        for widget in self.frame_comparacion.winfo_children():
            widget.destroy()

        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Recopilar datos
        datos_catala = {}
        datos_castella = {}

        for nombre, info in self.analizador.dataframes.items():
            df = info['df']
            tipo = info['tipo']

            if tipo == TipoCSV.COMPETENCIAS:
                # Buscar columnas
                for col in df.columns:
                    if 'Catal' in col and 'mitjana' in col:
                        # Convertir a numérico antes de calcular media
                        datos_catala[nombre] = pd.to_numeric(df[col], errors='coerce').mean()
                    if 'Castell' in col and 'mitjana' in col:
                        # Convertir a numérico antes de calcular media
                        datos_castella[nombre] = pd.to_numeric(df[col], errors='coerce').mean()

        if not datos_catala and not datos_castella:
            messagebox.showwarning("Advertencia", "No hay suficientes archivos de competencias")
            return

        # Gráfico Català
        if datos_catala:
            cursos = list(datos_catala.keys())
            medias = list(datos_catala.values())
            ax1.plot(range(len(cursos)), medias, marker='o', linewidth=2, color='steelblue')
            ax1.set_xticks(range(len(cursos)))
            ax1.set_xticklabels(cursos, rotation=45, ha='right')
            ax1.set_title('Evolución Media Català', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Media', fontsize=11)
            ax1.set_ylim(0, 100)
            ax1.grid(True, alpha=0.3)

            for i, media in enumerate(medias):
                ax1.text(i, media + 2, f'{media:.1f}', ha='center', fontsize=9)

        # Gráfico Castellà
        if datos_castella:
            cursos = list(datos_castella.keys())
            medias = list(datos_castella.values())
            ax2.plot(range(len(cursos)), medias, marker='o', linewidth=2, color='coral')
            ax2.set_xticks(range(len(cursos)))
            ax2.set_xticklabels(cursos, rotation=45, ha='right')
            ax2.set_title('Evolución Media Castellà', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Media', fontsize=11)
            ax2.set_ylim(0, 100)
            ax2.grid(True, alpha=0.3)

            for i, media in enumerate(medias):
                ax2.text(i, media + 2, f'{media:.1f}', ha='center', fontsize=9)

        plt.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_comparacion)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = VentanaAnalisis(root)
    root.mainloop()


if __name__ == "__main__":
    main()
