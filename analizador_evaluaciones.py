#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 Analizador de Datos Educativos - ESO y Primaria
Herramienta para analizar evaluaciones académicas, competencias básicas,
diversidad cultural e inclusión educativa
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
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

    def obtener_estadisticas_aulas_acollida(self):
        """Obtiene estadísticas de estudiantes en Aulas de Acogida"""
        if self.df_actual is None:
            return None

        col_aula_acollida = self.buscar_columna(['Aula', 'acollida'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])

        if col_aula_acollida is None or col_numero is None:
            return None

        stats = {}

        # Total por aula de acogida (Sí/No)
        resumen_aula = self.df_actual.groupby(col_aula_acollida)[col_numero].sum()
        stats['por_aula_acollida'] = resumen_aula

        # Filtrar estudiantes en aula de acogida
        df_acollida = self.df_actual[
            self.df_actual[col_aula_acollida].str.contains('S', na=False, case=False)
        ]

        if len(df_acollida) > 0:
            total_acollida = df_acollida[col_numero].sum()
            total_general = self.df_actual[col_numero].sum()

            stats['total_acollida'] = total_acollida
            stats['porcentaje_acollida'] = (total_acollida / total_general * 100) if total_general > 0 else 0

            # Por nivel
            if 'Nivell' in df_acollida.columns:
                stats['por_nivel'] = df_acollida.groupby('Nivell')[col_numero].sum()

            # Por consecuencias
            col_consecuencias = self.buscar_columna(['Conseq', 'Avalua'])
            if col_consecuencias:
                stats['por_consecuencias'] = df_acollida.groupby(col_consecuencias)[col_numero].sum()

                # Calcular tasa de promoción en aula de acogida
                promovidos = df_acollida[
                    df_acollida[col_consecuencias].str.contains('Promociona', na=False)
                ][col_numero].sum()
                stats['tasa_promocion_acollida'] = (promovidos / total_acollida * 100) if total_acollida > 0 else 0

        return stats if stats else None

    def obtener_analisis_detallado_aulas_acollida(self):
        """Obtiene análisis detallado de estudiantes en aulas de acogida:
        nivel, nacionalidad y consecuencias de evaluación"""
        if self.df_actual is None:
            return None

        col_aula = self.buscar_columna(['Aula', 'acollida'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])
        col_nacionalidad = self.buscar_columna(['Zona', 'Nacionalitat'])
        col_nivel = 'Nivell'
        col_consecuencias = self.buscar_columna(['Conseq', 'Avalua'])

        if col_aula is None or col_numero is None:
            return None

        # Filtrar solo estudiantes en aulas de acogida
        df_acollida = self.df_actual[
            self.df_actual[col_aula].str.contains('S', na=False, case=False)
        ]

        if len(df_acollida) == 0:
            return None

        resultado = {}

        # 1. Análisis por nivel
        if col_nivel in df_acollida.columns:
            resultado['por_nivel'] = df_acollida.groupby(col_nivel)[col_numero].sum().sort_index()

        # 2. Análisis por nacionalidad
        if col_nacionalidad:
            resultado['por_nacionalidad'] = df_acollida.groupby(col_nacionalidad)[col_numero].sum().sort_values(ascending=False)

        # 3. Análisis por consecuencias (promocionan o no)
        if col_consecuencias:
            resultado['por_consecuencias'] = df_acollida.groupby(col_consecuencias)[col_numero].sum().sort_values(ascending=False)

            # Clasificar en promocionan vs no promocionan
            # En catalán: "Accedeix", "Obté el títol", "Passa de curs" = promociona
            # Pero NO "Roman" (permanece), "No passa", "No obté", "No accedeix"

            # Filtrar promocionados (incluir los que pasan)
            patron_promocion = r'Accedeix al curs següent|Passa de curs|Obté el títol'

            # Filtrar NO promocionados (excluir explícitamente)
            patron_no_promocion = r'Roman|No passa|No obté|No accedeix'

            promovidos = df_acollida[
                (df_acollida[col_consecuencias].str.contains(patron_promocion, na=False, case=False, regex=True)) &
                (~df_acollida[col_consecuencias].str.contains(patron_no_promocion, na=False, case=False, regex=True))
            ][col_numero].sum()

            no_promovidos = df_acollida[
                (~df_acollida[col_consecuencias].str.contains(patron_promocion, na=False, case=False, regex=True)) |
                (df_acollida[col_consecuencias].str.contains(patron_no_promocion, na=False, case=False, regex=True))
            ][col_numero].sum()

            resultado['resumen_promocion'] = {
                'promocionan': promovidos,
                'no_promocionan': no_promovidos,
                'tasa_promocion': (promovidos / (promovidos + no_promovidos) * 100) if (promovidos + no_promovidos) > 0 else 0
            }

        # 4. Análisis cruzado: nivel x nacionalidad
        if col_nivel in df_acollida.columns and col_nacionalidad:
            nivel_nacionalidad = df_acollida.groupby([col_nivel, col_nacionalidad])[col_numero].sum()
            resultado['nivel_x_nacionalidad'] = nivel_nacionalidad

        # 5. Análisis cruzado: nacionalidad x consecuencias
        if col_nacionalidad and col_consecuencias:
            nac_consec = df_acollida.groupby([col_nacionalidad, col_consecuencias])[col_numero].sum()
            resultado['nacionalidad_x_consecuencias'] = nac_consec

        # 6. Total de estudiantes
        resultado['total_estudiantes'] = df_acollida[col_numero].sum()

        return resultado

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
            # En catalán: "Accedeix", "Obté el títol", "Passa de curs" = promociona
            # Pero NO "Roman" (permanece), "No passa", "No obté", "No accedeix"
            total_sudamerica = df_sudamerica[col_numero].sum()

            # Filtrar promocionados (incluir los que pasan)
            patron_promocion = r'Accedeix al curs següent|Passa de curs|Obté el títol'

            # Filtrar NO promocionados (excluir explícitamente)
            patron_no_promocion = r'Roman|No passa|No obté|No accedeix'

            promovidos = df_sudamerica[
                (df_sudamerica[col_consecuencias].str.contains(patron_promocion, na=False, case=False, regex=True)) &
                (~df_sudamerica[col_consecuencias].str.contains(patron_no_promocion, na=False, case=False, regex=True))
            ][col_numero].sum()

            stats['tasa_promocion'] = (promovidos / total_sudamerica * 100) if total_sudamerica > 0 else 0

        return stats

    def obtener_competencias_sudamerica(self, por_nivel=False):
        """Obtiene competencias específicas de CENTRE I SUDAMÈRICA

        Args:
            por_nivel: Si es True, devuelve estadísticas separadas por nivel
        """
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

        if por_nivel and 'Nivell' in df_sudamerica.columns:
            # Devolver estadísticas separadas por nivel
            stats_por_nivel = {}

            for nivel in sorted(df_sudamerica['Nivell'].unique()):
                df_nivel = df_sudamerica[df_sudamerica['Nivell'] == nivel]
                stats = {}

                # Català
                col_num_cat = self.buscar_columna(['mero', 'alumnes', 'Catal'])
                col_mit_cat = self.buscar_columna(['Catal', 'mitjana'])

                if col_num_cat and col_mit_cat:
                    mitjana_cat_num = pd.to_numeric(df_nivel[col_mit_cat], errors='coerce')
                    num_cat_num = pd.to_numeric(df_nivel[col_num_cat], errors='coerce')

                    stats['Català'] = {
                        'total_alumnos': num_cat_num.sum(),
                        'media': mitjana_cat_num.mean(),
                        'mediana': mitjana_cat_num.median()
                    }

                # Castellà
                col_num_cas = self.buscar_columna(['mero', 'alumnes', 'Castell'])
                col_mit_cas = self.buscar_columna(['Castell', 'mitjana'])

                if col_num_cas and col_mit_cas:
                    mitjana_cas_num = pd.to_numeric(df_nivel[col_mit_cas], errors='coerce')
                    num_cas_num = pd.to_numeric(df_nivel[col_num_cas], errors='coerce')

                    stats['Castellà'] = {
                        'total_alumnos': num_cas_num.sum(),
                        'media': mitjana_cas_num.mean(),
                        'mediana': mitjana_cas_num.median()
                    }

                if stats:
                    stats_por_nivel[nivel] = stats

            return stats_por_nivel if stats_por_nivel else None

        else:
            # Devolver estadísticas globales (comportamiento original)
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

    def obtener_competencias_espana(self, por_nivel=False):
        """Obtiene competencias específicas de estudiantes de ESPAÑA

        Args:
            por_nivel: Si es True, devuelve estadísticas separadas por nivel
        """
        if self.df_actual is None:
            return None

        col_nacionalidad = self.buscar_columna(['Zona', 'nacionalitat'])
        if col_nacionalidad is None:
            return None

        # Filtrar por ESPAÑA (puede aparecer como ESPANYA, ESPAÑA, etc.)
        df_espana = self.df_actual[
            self.df_actual[col_nacionalidad].str.contains('ESPAN', na=False, case=False)
        ]

        if len(df_espana) == 0:
            return None

        if por_nivel and 'Nivell' in df_espana.columns:
            # Devolver estadísticas separadas por nivel
            stats_por_nivel = {}

            for nivel in sorted(df_espana['Nivell'].unique()):
                df_nivel = df_espana[df_espana['Nivell'] == nivel]
                stats = {}

                # Català
                col_num_cat = self.buscar_columna(['mero', 'alumnes', 'Catal'])
                col_mit_cat = self.buscar_columna(['Catal', 'mitjana'])

                if col_num_cat and col_mit_cat:
                    mitjana_cat_num = pd.to_numeric(df_nivel[col_mit_cat], errors='coerce')
                    num_cat_num = pd.to_numeric(df_nivel[col_num_cat], errors='coerce')

                    stats['Català'] = {
                        'total_alumnos': num_cat_num.sum(),
                        'media': mitjana_cat_num.mean(),
                        'mediana': mitjana_cat_num.median()
                    }

                # Castellà
                col_num_cas = self.buscar_columna(['mero', 'alumnes', 'Castell'])
                col_mit_cas = self.buscar_columna(['Castell', 'mitjana'])

                if col_num_cas and col_mit_cas:
                    mitjana_cas_num = pd.to_numeric(df_nivel[col_mit_cas], errors='coerce')
                    num_cas_num = pd.to_numeric(df_nivel[col_num_cas], errors='coerce')

                    stats['Castellà'] = {
                        'total_alumnos': num_cas_num.sum(),
                        'media': mitjana_cas_num.mean(),
                        'mediana': mitjana_cas_num.median()
                    }

                if stats:
                    stats_por_nivel[nivel] = stats

            return stats_por_nivel if stats_por_nivel else None

        else:
            # Devolver estadísticas globales (comportamiento original)
            stats = {}

            # Català
            col_num_cat = self.buscar_columna(['mero', 'alumnes', 'Catal'])
            col_mit_cat = self.buscar_columna(['Catal', 'mitjana'])

            if col_num_cat and col_mit_cat:
                mitjana_cat_num = pd.to_numeric(df_espana[col_mit_cat], errors='coerce')
                num_cat_num = pd.to_numeric(df_espana[col_num_cat], errors='coerce')

                stats['Català'] = {
                    'total_alumnos': num_cat_num.sum(),
                    'media': mitjana_cat_num.mean(),
                    'mediana': mitjana_cat_num.median()
                }

            # Castellà
            col_num_cas = self.buscar_columna(['mero', 'alumnes', 'Castell'])
            col_mit_cas = self.buscar_columna(['Castell', 'mitjana'])

            if col_num_cas and col_mit_cas:
                mitjana_cas_num = pd.to_numeric(df_espana[col_mit_cas], errors='coerce')
                num_cas_num = pd.to_numeric(df_espana[col_num_cas], errors='coerce')

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

    # ========== MÉTODOS PARA ANÁLISIS DE DIVERSIDAD ====================

    def obtener_resumen_diversidad(self):
        """Obtiene resumen completo de diversidad"""
        if self.df_actual is None:
            return None

        col_nacionalidad = self.buscar_columna(['Zona', 'Nacionalitat'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])

        if col_nacionalidad is None or col_numero is None:
            return None

        stats = {}

        # Total general
        stats['total_estudiantes'] = self.df_actual[col_numero].sum()

        # Españoles vs Extranjeros
        df_espana = self.df_actual[
            self.df_actual[col_nacionalidad].str.contains('ESPANYA', na=False, case=False)
        ]
        total_espana = df_espana[col_numero].sum()
        total_extranjeros = stats['total_estudiantes'] - total_espana

        stats['total_espana'] = total_espana
        stats['total_extranjeros'] = total_extranjeros
        stats['porcentaje_espana'] = (total_espana / stats['total_estudiantes'] * 100) if stats['total_estudiantes'] > 0 else 0
        stats['porcentaje_extranjeros'] = (total_extranjeros / stats['total_estudiantes'] * 100) if stats['total_estudiantes'] > 0 else 0

        # Top nacionalidades
        resumen_nacionalidad = self.df_actual.groupby(col_nacionalidad)[col_numero].sum()
        stats['top_nacionalidades'] = resumen_nacionalidad.sort_values(ascending=False)

        return stats

    def obtener_comparativa_grupos(self):
        """Obtiene comparativa de rendimiento entre grupos culturales"""
        if self.df_actual is None:
            return None

        col_nacionalidad = self.buscar_columna(['Zona', 'Nacionalitat'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])
        col_consecuencias = self.buscar_columna(['Conseq', 'Avalua'])

        if col_nacionalidad is None or col_numero is None or col_consecuencias is None:
            return None

        # Definir grupos culturales
        grupos = {
            'ESPAÑA': ['ESPANYA'],
            'MAGREB': ['MAGREB'],
            'AMÉRICA': ['CENTRE I SUDAM', 'AMÈRICA'],
            'EUROPA': ['RESTA UNIÓ EUROPEA', 'EUROPA'],
            'ASIA/OCEANÍA': ['ÀSIA', 'OCEANIA'],
            'RESTO ÁFRICA': ['RESTA ÀFRICA'],
        }

        resultados = {}

        for grupo, patrones in grupos.items():
            # Filtrar por grupo
            mascara = pd.Series([False] * len(self.df_actual))
            for patron in patrones:
                mascara |= self.df_actual[col_nacionalidad].str.contains(patron, na=False, case=False)

            df_grupo = self.df_actual[mascara]

            if len(df_grupo) > 0:
                total = df_grupo[col_numero].sum()

                # En catalán: "Accedeix", "Obté el títol", "Passa de curs" = promociona
                # Pero NO "Roman" (permanece), "No passa", "No obté", "No accedeix"

                # Filtrar promocionados (incluir los que pasan)
                patron_promocion = r'Accedeix al curs següent|Passa de curs|Obté el títol'

                # Filtrar NO promocionados (excluir explícitamente)
                patron_no_promocion = r'Roman|No passa|No obté|No accedeix'

                promovidos = df_grupo[
                    (df_grupo[col_consecuencias].str.contains(patron_promocion, na=False, case=False, regex=True)) &
                    (~df_grupo[col_consecuencias].str.contains(patron_no_promocion, na=False, case=False, regex=True))
                ][col_numero].sum()

                # Repiten: buscar "Roman", "Repeteix", "Repetir", "No passa"
                repiten = df_grupo[
                    df_grupo[col_consecuencias].str.contains('Roman|Repeteix|Repetir|No passa', na=False, case=False, regex=True)
                ][col_numero].sum()

                resultados[grupo] = {
                    'total': total,
                    'promovidos': promovidos,
                    'tasa_promocion': (promovidos / total * 100) if total > 0 else 0,
                    'repiten': repiten,
                    'tasa_repeticion': (repiten / total * 100) if total > 0 else 0
                }

        return resultados if resultados else None

    def obtener_analisis_por_centro(self, codigo_centro=None):
        """Obtiene análisis por centro educativo"""
        if self.df_actual is None:
            return None

        col_centro = self.buscar_columna(['Centre', 'Codi'])
        col_numero = self.buscar_columna(['mero', 'Avalua'])
        col_nacionalidad = self.buscar_columna(['Zona', 'Nacionalitat'])
        col_aula = self.buscar_columna(['Aula', 'acollida'])

        if col_centro is None or col_numero is None:
            return None

        if codigo_centro:
            # Análisis de un centro específico
            df_centro = self.df_actual[self.df_actual[col_centro] == codigo_centro]

            if len(df_centro) == 0:
                return None

            stats = {
                'total_estudiantes': df_centro[col_numero].sum(),
                'registros': len(df_centro)
            }

            if col_nacionalidad:
                stats['por_nacionalidad'] = df_centro.groupby(col_nacionalidad)[col_numero].sum()

            if col_aula:
                df_acollida = df_centro[
                    df_centro[col_aula].str.contains('S', na=False, case=False)
                ]
                stats['en_aula_acollida'] = df_acollida[col_numero].sum() if len(df_acollida) > 0 else 0

            return stats
        else:
            # Top centros diversos
            if col_nacionalidad:
                # Calcular % extranjeros por centro
                centros_stats = []

                for centro in self.df_actual[col_centro].unique():
                    df_centro = self.df_actual[self.df_actual[col_centro] == centro]
                    total_centro = df_centro[col_numero].sum()

                    if total_centro >= 50:  # Solo centros con al menos 50 estudiantes
                        df_espana = df_centro[
                            df_centro[col_nacionalidad].str.contains('ESPANYA', na=False, case=False)
                        ]
                        total_espana = df_espana[col_numero].sum()
                        total_extranjeros = total_centro - total_espana
                        porcentaje_extranjeros = (total_extranjeros / total_centro * 100) if total_centro > 0 else 0

                        centros_stats.append({
                            'centro': centro,
                            'total': total_centro,
                            'extranjeros': total_extranjeros,
                            'porcentaje': porcentaje_extranjeros
                        })

                # Ordenar por % extranjeros
                centros_stats.sort(key=lambda x: x['porcentaje'], reverse=True)
                return centros_stats[:20]  # Top 20

            return None


class VentanaAnalisis:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 Analizador de Datos Educativos - Diversidad e Inclusión")
        self.root.geometry("1400x900")

        self.analizador = AnalizadorEducativo()
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""

        # Frame superior - Controles
        frame_superior = ttk.Frame(self.root, padding="10")
        frame_superior.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))

        # Botones de carga
        ttk.Button(frame_superior, text="📁 Cargar CSV",
                   command=self.cargar_archivo).grid(row=0, column=0, padx=5)

        ttk.Button(frame_superior, text="📂 Cargar Múltiples CSV",
                   command=self.cargar_multiples_archivos).grid(row=0, column=1, padx=5)

        ttk.Button(frame_superior, text="🗑️ Limpiar Datos",
                   command=self.limpiar_datos).grid(row=0, column=2, padx=5)

        # Label de archivo actual
        self.label_archivo = ttk.Label(frame_superior, text="Ningún archivo cargado",
                                       font=('Arial', 10, 'bold'))
        self.label_archivo.grid(row=0, column=3, padx=20)

        # Label de tipo de CSV
        self.label_tipo = ttk.Label(frame_superior, text="",
                                    font=('Arial', 9), foreground='blue')
        self.label_tipo.grid(row=0, column=4, padx=10)

        # Frame central - Notebook con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Crear pestañas (ahora con enfoque en diversidad e inclusión)
        self.crear_pestana_resumen()
        self.crear_pestana_visualizaciones()
        self.crear_pestana_datos()
        self.crear_pestana_comparaciones()
        self.crear_pestana_aulas_acogida_detalle()
        self.crear_pestana_diversidad_cultural()
        self.crear_pestana_comparativa_grupos()
        self.crear_pestana_analisis_centros()

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

            # NUEVO: Botón para Aulas de Acogida
            ttk.Button(self.frame_controles_graficos, text="🏫 Aulas de Acogida",
                       command=self.grafico_aulas_acollida).grid(row=0, column=3, padx=5)

            # NUEVO: Botón específico para Sudamérica
            ttk.Button(self.frame_controles_graficos, text="📊 Análisis Sudamérica",
                       command=self.grafico_sudamerica_evaluacion).grid(row=0, column=4, padx=5)

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

    def limpiar_datos(self):
        """Limpia todos los datos cargados y reinicia la interfaz"""
        # Confirmar con el usuario
        respuesta = messagebox.askyesno(
            "Confirmar limpieza",
            "¿Estás seguro de que quieres borrar todos los datos cargados?\n\n"
            "Esta acción no se puede deshacer."
        )

        if not respuesta:
            return

        # Limpiar datos del analizador
        self.analizador.dataframes = {}
        self.analizador.df_actual = None
        self.analizador.nombre_archivo_actual = None
        self.analizador.tipo_csv_actual = TipoCSV.DESCONOCIDO

        # Actualizar labels
        self.label_archivo.config(text="Ningún archivo cargado")
        self.label_tipo.config(text="")

        # Limpiar todas las pestañas
        self.texto_resumen.delete(1.0, tk.END)
        self.texto_resumen.insert(tk.END, "No hay datos cargados")

        self.texto_datos.delete(1.0, tk.END)
        self.texto_datos.insert(tk.END, "No hay datos cargados")

        # Limpiar frames de visualización
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()

        for widget in self.frame_comparacion.winfo_children():
            widget.destroy()

        for widget in self.frame_contenido_aulas_detalle.winfo_children():
            widget.destroy()

        for widget in self.frame_contenido_diversidad.winfo_children():
            widget.destroy()

        for widget in self.frame_contenido_grupos.winfo_children():
            widget.destroy()

        for widget in self.frame_contenido_centros.winfo_children():
            widget.destroy()

        # Actualizar filtros
        self.actualizar_filtros()

        # Mensaje de confirmación
        messagebox.showinfo("Limpieza completada", "Todos los datos han sido eliminados correctamente")

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

        # NUEVA SECCIÓN: Análisis de Aulas de Acogida
        texto += f"\n{'='*70}\n"
        texto += "🏫 ANÁLISIS: AULAS DE ACOGIDA\n"
        texto += f"{'='*70}\n"

        stats_acollida = self.analizador.obtener_estadisticas_aulas_acollida()
        if stats_acollida and 'total_acollida' in stats_acollida:
            texto += f"\nTotal estudiantes en Aulas de Acogida: {stats_acollida['total_acollida']:,}\n"
            texto += f"Porcentaje del total: {stats_acollida['porcentaje_acollida']:.2f}%\n"

            if 'tasa_promocion_acollida' in stats_acollida:
                texto += f"Tasa de promoción: {stats_acollida['tasa_promocion_acollida']:.2f}%\n"

            if 'por_nivel' in stats_acollida:
                texto += f"\nDistribución por nivel:\n"
                for nivel, total in stats_acollida['por_nivel'].items():
                    texto += f"  Nivel {nivel}: {total:,} estudiantes\n"

            if 'por_consecuencias' in stats_acollida:
                texto += f"\nDistribución por consecuencias:\n"
                all_consec = stats_acollida['por_consecuencias'].sort_values(ascending=False)
                total_acollida = stats_acollida.get('total_acollida', all_consec.sum())
                for consec, total in all_consec.items():
                    porcentaje = (total / total_acollida * 100) if total_acollida > 0 else 0
                    texto += f"  {consec}: {total:,} ({porcentaje:.1f}%)\n"
                # Verificación
                suma_consec = all_consec.sum()
                texto += f"\n  Total verificado: {suma_consec:,} estudiantes\n"
        elif stats_acollida and 'por_aula_acollida' in stats_acollida:
            texto += f"\nResumen general:\n"
            for aula, total in stats_acollida['por_aula_acollida'].items():
                texto += f"  {aula}: {total:,} estudiantes\n"
        else:
            texto += "\nNo hay datos de Aulas de Acogida en este archivo.\n"

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
                texto += f"\nDistribución por consecuencias:\n"
                all_consec = stats_sudamerica['por_consecuencias'].sort_values(ascending=False)
                for consec, total in all_consec.items():
                    porcentaje = (total / stats_sudamerica['total_estudiantes'] * 100)
                    texto += f"  {consec}: {total:,} ({porcentaje:.1f}%)\n"
                # Verificación
                suma_consec = all_consec.sum()
                texto += f"\n  Total verificado: {suma_consec:,} estudiantes\n"
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

        # NUEVA SECCIÓN: Evolución entre niveles
        texto += f"\n{'='*70}\n"
        texto += "📈 EVOLUCIÓN ENTRE NIVELES (4º → 6º)\n"
        texto += f"{'='*70}\n"

        if resumen_nivel:
            for lengua, df_resumen in resumen_nivel.items():
                if len(df_resumen) >= 2:
                    col_mit = [c for c in df_resumen.columns if 'mitjana' in c][0]
                    niveles = sorted(df_resumen.index)

                    if len(niveles) == 2:
                        nivel_4 = df_resumen.loc[niveles[0], col_mit]
                        nivel_6 = df_resumen.loc[niveles[1], col_mit]
                        diferencia = nivel_6 - nivel_4

                        texto += f"\n{lengua}:\n"
                        texto += f"  Nivel {niveles[0]}: {nivel_4:.2f}\n"
                        texto += f"  Nivel {niveles[1]}: {nivel_6:.2f}\n"
                        texto += f"  Diferencia: {diferencia:+.2f} puntos "

                        if diferencia > 0:
                            texto += "(✅ mejora)\n"
                        elif diferencia < 0:
                            texto += "(⚠️ empeora)\n"
                        else:
                            texto += "(→ se mantiene)\n"

                        porcentaje_cambio = (diferencia / nivel_4 * 100) if nivel_4 > 0 else 0
                        texto += f"  Cambio porcentual: {porcentaje_cambio:+.2f}%\n"

        # NUEVA SECCIÓN: Distribución por rangos de notas
        texto += f"\n{'='*70}\n"
        texto += "📊 DISTRIBUCIÓN POR RANGOS DE NOTAS\n"
        texto += f"{'='*70}\n"

        # Calcular rangos para cada lengua
        if self.analizador.df_actual is not None:
            col_catala = self.analizador.buscar_columna(['Català', 'competència'])
            col_castella = self.analizador.buscar_columna(['Castellà', 'competència'])
            col_numero = self.analizador.buscar_columna(['mero', 'avaluats'])

            if col_numero:
                for nombre_lengua, col_lengua in [('Català', col_catala), ('Castellà', col_castella)]:
                    if col_lengua:
                        df_lengua = self.analizador.df_actual[[col_lengua, col_numero]].copy()
                        df_lengua = df_lengua[df_lengua[col_lengua].notna()]

                        # Definir rangos
                        total = df_lengua[col_numero].sum()
                        if total > 0:
                            texto += f"\n{nombre_lengua}:\n"

                            # Suspenso (0-49)
                            suspensos = df_lengua[df_lengua[col_lengua] < 50][col_numero].sum()
                            texto += f"  Suspenso (0-49):  {suspensos:>8,.0f} ({suspensos/total*100:5.1f}%)\n"

                            # Aprobado (50-69)
                            aprobados = df_lengua[(df_lengua[col_lengua] >= 50) & (df_lengua[col_lengua] < 70)][col_numero].sum()
                            texto += f"  Aprobado (50-69): {aprobados:>8,.0f} ({aprobados/total*100:5.1f}%)\n"

                            # Notable (70-89)
                            notables = df_lengua[(df_lengua[col_lengua] >= 70) & (df_lengua[col_lengua] < 90)][col_numero].sum()
                            texto += f"  Notable (70-89):  {notables:>8,.0f} ({notables/total*100:5.1f}%)\n"

                            # Excelente (90-100)
                            excelentes = df_lengua[df_lengua[col_lengua] >= 90][col_numero].sum()
                            texto += f"  Excelente (90-100):{excelentes:>8,.0f} ({excelentes/total*100:5.1f}%)\n"

        # NUEVA SECCIÓN: Análisis específico de CENTRE I SUDAMÈRICA
        texto += f"\n{'='*70}\n"
        texto += "📊 ANÁLISIS ESPECÍFICO: CENTRE I SUDAMÈRICA\n"
        texto += f"{'='*70}\n"

        # Obtener estadísticas por nivel
        stats_sudamerica_por_nivel = self.analizador.obtener_competencias_sudamerica(por_nivel=True)

        if stats_sudamerica_por_nivel:
            # Obtener también las medias globales por nivel para comparación
            resumen_nivel = self.analizador.obtener_resumen_por_nivel_competencias()

            for nivel in sorted(stats_sudamerica_por_nivel.keys()):
                texto += f"\n--- Nivel {nivel} ---\n"
                stats_nivel = stats_sudamerica_por_nivel[nivel]

                for lengua, datos in stats_nivel.items():
                    texto += f"\n{lengua}:\n"
                    texto += f"  Total alumnos: {datos['total_alumnos']:,.0f}\n"
                    texto += f"  Media: {datos['media']:.2f}\n"
                    texto += f"  Mediana: {datos['mediana']:.2f}\n"

                    # Añadir comparativa con media global del mismo nivel
                    if resumen_nivel and lengua in resumen_nivel:
                        df_resumen = resumen_nivel[lengua]
                        if nivel in df_resumen.index:
                            col_mit = [c for c in df_resumen.columns if 'mitjana' in c][0]
                            media_global_nivel = df_resumen.loc[nivel, col_mit]
                            diferencia = datos['media'] - media_global_nivel
                            texto += f"  Media global (Nivel {nivel}): {media_global_nivel:.2f}\n"
                            texto += f"  Diferencia: {diferencia:+.2f} puntos "

                            if abs(diferencia) < 2:
                                texto += "(→ similar)\n"
                            elif diferencia > 0:
                                texto += "(✅ superior)\n"
                            else:
                                texto += "(⚠️ inferior)\n"

            # Añadir análisis de evolución entre niveles para CENTRE I SUDAMÈRICA
            niveles_ordenados = sorted(stats_sudamerica_por_nivel.keys())
            if len(niveles_ordenados) >= 2:
                texto += f"\n{'─'*70}\n"
                texto += f"📈 Evolución CENTRE I SUDAMÈRICA ({niveles_ordenados[0]} → {niveles_ordenados[-1]}):\n"
                texto += f"{'─'*70}\n"

                nivel_inicial = niveles_ordenados[0]
                nivel_final = niveles_ordenados[-1]

                for lengua in stats_sudamerica_por_nivel[nivel_inicial].keys():
                    if lengua in stats_sudamerica_por_nivel[nivel_final]:
                        media_inicial = stats_sudamerica_por_nivel[nivel_inicial][lengua]['media']
                        media_final = stats_sudamerica_por_nivel[nivel_final][lengua]['media']
                        diferencia = media_final - media_inicial
                        porcentaje = (diferencia / media_inicial * 100) if media_inicial > 0 else 0

                        texto += f"\n{lengua}:\n"
                        texto += f"  Nivel {nivel_inicial}: {media_inicial:.2f}\n"
                        texto += f"  Nivel {nivel_final}: {media_final:.2f}\n"
                        texto += f"  Cambio: {diferencia:+.2f} puntos ({porcentaje:+.2f}%) "

                        if diferencia > 0:
                            texto += "✅\n"
                        elif diferencia < 0:
                            texto += "⚠️\n"
                        else:
                            texto += "→\n"
        else:
            texto += "\nNo hay datos de CENTRE I SUDAMÈRICA en este archivo.\n"

        # NUEVA SECCIÓN: Análisis específico de ESPAÑA
        texto += f"\n{'='*70}\n"
        texto += "📊 ANÁLISIS ESPECÍFICO: ESPAÑA\n"
        texto += f"{'='*70}\n"

        # Obtener estadísticas por nivel
        stats_espana_por_nivel = self.analizador.obtener_competencias_espana(por_nivel=True)

        if stats_espana_por_nivel:
            # Obtener también las medias globales por nivel para comparación
            resumen_nivel = self.analizador.obtener_resumen_por_nivel_competencias()

            for nivel in sorted(stats_espana_por_nivel.keys()):
                texto += f"\n--- Nivel {nivel} ---\n"
                stats_nivel = stats_espana_por_nivel[nivel]

                for lengua, datos in stats_nivel.items():
                    texto += f"\n{lengua}:\n"
                    texto += f"  Total alumnos: {datos['total_alumnos']:,.0f}\n"
                    texto += f"  Media: {datos['media']:.2f}\n"
                    texto += f"  Mediana: {datos['mediana']:.2f}\n"

                    # Añadir comparativa con media global del mismo nivel
                    if resumen_nivel and lengua in resumen_nivel:
                        df_resumen = resumen_nivel[lengua]
                        if nivel in df_resumen.index:
                            col_mit = [c for c in df_resumen.columns if 'mitjana' in c][0]
                            media_global_nivel = df_resumen.loc[nivel, col_mit]
                            diferencia = datos['media'] - media_global_nivel
                            texto += f"  Media global (Nivel {nivel}): {media_global_nivel:.2f}\n"
                            texto += f"  Diferencia: {diferencia:+.2f} puntos "

                            if abs(diferencia) < 2:
                                texto += "(→ similar)\n"
                            elif diferencia > 0:
                                texto += "(✅ superior)\n"
                            else:
                                texto += "(⚠️ inferior)\n"

            # Añadir análisis de evolución entre niveles para ESPAÑA
            niveles_ordenados = sorted(stats_espana_por_nivel.keys())
            if len(niveles_ordenados) >= 2:
                texto += f"\n{'─'*70}\n"
                texto += f"📈 Evolución ESPAÑA ({niveles_ordenados[0]} → {niveles_ordenados[-1]}):\n"
                texto += f"{'─'*70}\n"

                nivel_inicial = niveles_ordenados[0]
                nivel_final = niveles_ordenados[-1]

                for lengua in stats_espana_por_nivel[nivel_inicial].keys():
                    if lengua in stats_espana_por_nivel[nivel_final]:
                        media_inicial = stats_espana_por_nivel[nivel_inicial][lengua]['media']
                        media_final = stats_espana_por_nivel[nivel_final][lengua]['media']
                        diferencia = media_final - media_inicial
                        porcentaje = (diferencia / media_inicial * 100) if media_inicial > 0 else 0

                        texto += f"\n{lengua}:\n"
                        texto += f"  Nivel {nivel_inicial}: {media_inicial:.2f}\n"
                        texto += f"  Nivel {nivel_final}: {media_final:.2f}\n"
                        texto += f"  Cambio: {diferencia:+.2f} puntos ({porcentaje:+.2f}%) "

                        if diferencia > 0:
                            texto += "✅\n"
                        elif diferencia < 0:
                            texto += "⚠️\n"
                        else:
                            texto += "→\n"
        else:
            texto += "\nNo hay datos de ESPAÑA en este archivo.\n"

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

    def grafico_aulas_acollida(self):
        """Genera gráfico para Aulas de Acogida"""
        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        stats_acollida = self.analizador.obtener_estadisticas_aulas_acollida()
        if not stats_acollida or 'total_acollida' not in stats_acollida:
            messagebox.showwarning("Advertencia", "No hay datos de Aulas de Acogida en este archivo")
            return

        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Crear figura con 3 subplots
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        ax1 = fig.add_subplot(gs[0, :])  # Gráfico superior ocupa toda la fila
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])

        # Gráfico 1: Resumen general (Sí vs No)
        if 'por_aula_acollida' in stats_acollida:
            resumen = stats_acollida['por_aula_acollida']
            colores = ['#ff6b6b' if 'S' in str(idx) else '#51cf66' for idx in resumen.index]
            bars = ax1.bar(resumen.index, resumen.values, color=colores, edgecolor='black', linewidth=1.5)
            ax1.set_title('Estudiantes en Aulas de Acogida - Resumen General',
                         fontsize=14, fontweight='bold')
            ax1.set_ylabel('Número de Estudiantes', fontsize=12)
            ax1.set_xlabel('Aula de Acogida', fontsize=12)
            ax1.grid(axis='y', alpha=0.3)

            for bar, valor in zip(bars, resumen.values):
                height = bar.get_height()
                porcentaje = (valor / resumen.sum() * 100)
                ax1.text(bar.get_x() + bar.get_width()/2., height + max(resumen.values)*0.02,
                        f'{int(valor):,}\n({porcentaje:.1f}%)',
                        ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Gráfico 2: Distribución por nivel (solo estudiantes en aula de acogida)
        if 'por_nivel' in stats_acollida:
            resumen_nivel = stats_acollida['por_nivel'].sort_index()
            bars2 = ax2.bar(resumen_nivel.index, resumen_nivel.values, color='coral', edgecolor='darkred')
            ax2.set_title('Distribución por Nivel\n(Aulas de Acogida)', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Nivel', fontsize=11)
            ax2.set_ylabel('Número de Estudiantes', fontsize=11)
            ax2.grid(axis='y', alpha=0.3)

            for bar, valor in zip(bars2, resumen_nivel.values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + max(resumen_nivel.values)*0.02,
                        f'{int(valor):,}', ha='center', va='bottom', fontsize=9)

        # Gráfico 3: Indicadores clave
        categorias = ['% del Total', 'Tasa Promoción']
        valores = [
            stats_acollida.get('porcentaje_acollida', 0),
            stats_acollida.get('tasa_promocion_acollida', 0)
        ]
        colores_indicadores = ['#4dabf7', '#ffd43b']
        bars3 = ax3.bar(categorias, valores, color=colores_indicadores, edgecolor='black', linewidth=1.5)
        ax3.set_title('Indicadores Aulas de Acogida', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Porcentaje (%)', fontsize=11)
        ax3.set_ylim(0, 100)
        ax3.grid(axis='y', alpha=0.3)

        for bar, valor in zip(bars3, valores):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Añadir información adicional como texto
        info_text = f"Total estudiantes en Aulas de Acogida: {stats_acollida['total_acollida']:,}"
        fig.text(0.5, 0.02, info_text, ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

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

    # ==================== PESTAÑA 5: AULAS DE ACOGIDA DETALLADO ====================

    def crear_pestana_aulas_acogida_detalle(self):
        """Crea la pestaña de análisis detallado de aulas de acogida"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏫 Aulas Acogida Detalle")

        # Frame de controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(frame_controles, text="📊 Análisis Completo",
                   command=self.mostrar_analisis_completo_aulas).grid(row=0, column=0, padx=5)
        ttk.Button(frame_controles, text="📈 Por Nivel y Nacionalidad",
                   command=self.grafico_nivel_nacionalidad_aulas).grid(row=0, column=1, padx=5)
        ttk.Button(frame_controles, text="✅ Promoción por Nacionalidad",
                   command=self.grafico_promocion_por_nacionalidad_aulas).grid(row=0, column=2, padx=5)
        ttk.Button(frame_controles, text="📊 Tabla Detallada",
                   command=self.mostrar_tabla_detallada_aulas).grid(row=0, column=3, padx=5)

        # Frame para contenido
        self.frame_contenido_aulas_detalle = ttk.Frame(frame)
        self.frame_contenido_aulas_detalle.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def mostrar_analisis_completo_aulas(self):
        """Muestra análisis textual completo de aulas de acogida"""
        for widget in self.frame_contenido_aulas_detalle.winfo_children():
            widget.destroy()

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_aulas_detalle, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        datos = self.analizador.obtener_analisis_detallado_aulas_acollida()
        if not datos:
            texto_widget.insert(tk.END, "No hay datos de aulas de acogida")
            return

        texto = ""
        texto += "="*80 + "\n"
        texto += "🏫 ANÁLISIS DETALLADO: ESTUDIANTES EN AULAS DE ACOGIDA\n"
        texto += "="*80 + "\n\n"

        texto += f"Total de estudiantes: {int(datos['total_estudiantes']):,}\n\n"

        # 1. Por nivel (curso)
        if 'por_nivel' in datos:
            texto += "="*80 + "\n"
            texto += "📚 DISTRIBUCIÓN POR NIVEL (CURSO)\n"
            texto += "="*80 + "\n"
            for nivel, total in datos['por_nivel'].items():
                porcentaje = (total / datos['total_estudiantes'] * 100)
                texto += f"  Nivel {nivel}: {int(total):>4,} estudiantes ({porcentaje:5.1f}%)\n"
            texto += "\n"

        # 2. Por nacionalidad
        if 'por_nacionalidad' in datos:
            texto += "="*80 + "\n"
            texto += "🌍 DISTRIBUCIÓN POR NACIONALIDAD\n"
            texto += "="*80 + "\n"
            for nac, total in datos['por_nacionalidad'].head(10).items():
                porcentaje = (total / datos['total_estudiantes'] * 100)
                texto += f"  {nac:40s} {int(total):>4,} ({porcentaje:5.1f}%)\n"
            texto += "\n"

        # 3. Por consecuencias (¿Pasan de curso?)
        if 'resumen_promocion' in datos:
            texto += "="*80 + "\n"
            texto += "✅ ¿PASAN DE CURSO?\n"
            texto += "="*80 + "\n"
            prom = datos['resumen_promocion']
            texto += f"  SÍ promocionan:  {int(prom['promocionan']):>4,} estudiantes\n"
            texto += f"  NO promocionan:  {int(prom['no_promocionan']):>4,} estudiantes\n"
            texto += f"  Tasa de éxito:   {prom['tasa_promocion']:>5.1f}%\n"
            texto += "\n"

        if 'por_consecuencias' in datos:
            texto += "Detalle de consecuencias:\n"
            for consec, total in datos['por_consecuencias'].head(5).items():
                texto += f"  • {consec}: {int(total):,}\n"
            texto += "\n"

        # 4. Análisis cruzado: NACIONALIDAD x CONSECUENCIAS
        if 'nacionalidad_x_consecuencias' in datos:
            texto += "="*80 + "\n"
            texto += "🌍 ANÁLISIS DETALLADO POR NACIONALIDAD Y TIPO DE PROGRESIÓN\n"
            texto += "="*80 + "\n\n"

            nac_consec = datos['nacionalidad_x_consecuencias']

            # Agrupar por tipo de consecuencia
            consecuencias_dict = {}
            for (nac, consec), total in nac_consec.items():
                if consec not in consecuencias_dict:
                    consecuencias_dict[consec] = []
                consecuencias_dict[consec].append((nac, int(total)))

            # Mostrar cada tipo de consecuencia con sus nacionalidades
            for consec, nacionalidades in sorted(consecuencias_dict.items(),
                                                key=lambda x: sum([n[1] for n in x[1]]),
                                                reverse=True):
                total_consec = sum([n[1] for n in nacionalidades])
                texto += f"📋 {consec}\n"
                texto += f"   Total: {total_consec} estudiantes\n"
                texto += "-"*80 + "\n"

                # Ordenar nacionalidades por número de estudiantes
                nacionalidades_ordenadas = sorted(nacionalidades, key=lambda x: x[1], reverse=True)

                for nac, total in nacionalidades_ordenadas:
                    porcentaje = (total / total_consec * 100)
                    texto += f"   • {nac:45s} {total:>3,} estudiantes ({porcentaje:5.1f}%)\n"
                texto += "\n"

        # 5. Análisis cruzado: nivel x nacionalidad
        if 'nivel_x_nacionalidad' in datos:
            texto += "="*80 + "\n"
            texto += "📊 CRUCE: NIVEL x NACIONALIDAD (Top combinaciones)\n"
            texto += "="*80 + "\n"
            top_cruces = datos['nivel_x_nacionalidad'].sort_values(ascending=False).head(10)
            for (nivel, nac), total in top_cruces.items():
                texto += f"  Nivel {nivel} + {nac}: {int(total):,}\n"

        texto_widget.insert(tk.END, texto)

    def grafico_nivel_nacionalidad_aulas(self):
        """Gráfico de distribución por nivel y nacionalidad"""
        for widget in self.frame_contenido_aulas_detalle.winfo_children():
            widget.destroy()

        datos = self.analizador.obtener_analisis_detallado_aulas_acollida()
        if not datos or 'nivel_x_nacionalidad' not in datos:
            messagebox.showwarning("Advertencia", "No hay datos suficientes")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Gráfico 1: Por nivel
        if 'por_nivel' in datos:
            niveles = datos['por_nivel']
            bars = ax1.bar(range(len(niveles)), niveles.values, color='#4dabf7', edgecolor='black')
            ax1.set_xticks(range(len(niveles)))
            ax1.set_xticklabels(niveles.index)
            ax1.set_title('📚 Estudiantes por Nivel', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Nivel', fontsize=11)
            ax1.set_ylabel('Número de Estudiantes', fontsize=11)
            ax1.grid(axis='y', alpha=0.3)

            for bar, valor in zip(bars, niveles.values):
                ax1.text(bar.get_x() + bar.get_width()/2., valor,
                        f'{int(valor)}', ha='center', va='bottom', fontsize=10)

        # Gráfico 2: Top 8 nacionalidades
        if 'por_nacionalidad' in datos:
            top_nac = datos['por_nacionalidad'].head(8)
            colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(top_nac)))
            bars = ax2.barh(range(len(top_nac)), top_nac.values, color=colors, edgecolor='black')
            ax2.set_yticks(range(len(top_nac)))
            ax2.set_yticklabels([nac[:25] for nac in top_nac.index])
            ax2.set_title('🌍 Top 8 Nacionalidades', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Número de Estudiantes', fontsize=11)
            ax2.grid(axis='x', alpha=0.3)

            for i, valor in enumerate(top_nac.values):
                ax2.text(valor + max(top_nac.values)*0.01, i,
                        f'{int(valor)}', ha='left', va='center', fontsize=9)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_aulas_detalle)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_promocion_por_nacionalidad_aulas(self):
        """Gráfico de tasas de promoción por nacionalidad en aulas de acogida"""
        for widget in self.frame_contenido_aulas_detalle.winfo_children():
            widget.destroy()

        datos = self.analizador.obtener_analisis_detallado_aulas_acollida()
        if not datos or 'nacionalidad_x_consecuencias' not in datos:
            messagebox.showwarning("Advertencia", "No hay datos suficientes")
            return

        # Calcular tasa de promoción por nacionalidad
        nac_consec = datos['nacionalidad_x_consecuencias']

        tasas_por_nac = {}
        for (nac, consec), total in nac_consec.items():
            if nac not in tasas_por_nac:
                tasas_por_nac[nac] = {'total': 0, 'promocionan': 0}

            tasas_por_nac[nac]['total'] += total

            # En catalán: "Accedeix", "Obté el títol", "Passa de curs" = promociona
            # Pero NO "Roman" (permanece), "No passa", "No obté", "No accedeix"
            if (('Accedeix al curs següent' in consec or 'Passa de curs' in consec or 'Obté el títol' in consec) and
                ('Roman' not in consec and 'No passa' not in consec and 'No obté' not in consec and 'No accedeix' not in consec)):
                tasas_por_nac[nac]['promocionan'] += total

        # Calcular porcentajes
        for nac in tasas_por_nac:
            total = tasas_por_nac[nac]['total']
            prom = tasas_por_nac[nac]['promocionan']
            tasas_por_nac[nac]['tasa'] = (prom / total * 100) if total > 0 else 0

        # Ordenar por total de estudiantes y tomar top 8
        tasas_ordenadas = sorted(tasas_por_nac.items(),
                                key=lambda x: x[1]['total'],
                                reverse=True)[:8]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        nacionalidades = [nac for nac, _ in tasas_ordenadas]
        tasas = [datos['tasa'] for _, datos in tasas_ordenadas]
        totales = [datos['total'] for _, datos in tasas_ordenadas]

        # Gráfico 1: Tasas de promoción
        colores = ['#51cf66' if tasa >= 90 else '#ff8c42' if tasa >= 75 else '#ff6b6b' for tasa in tasas]
        bars1 = ax1.barh(range(len(nacionalidades)), tasas, color=colores, edgecolor='black')
        ax1.set_yticks(range(len(nacionalidades)))
        ax1.set_yticklabels([nac[:25] for nac in nacionalidades])
        ax1.set_xlabel('Tasa de Promoción (%)', fontsize=11)
        ax1.set_title('✅ Tasa de Promoción por Nacionalidad', fontsize=12, fontweight='bold')
        ax1.set_xlim(0, 100)
        ax1.grid(axis='x', alpha=0.3)
        ax1.axvline(x=90, color='gray', linestyle='--', alpha=0.5)

        for i, tasa in enumerate(tasas):
            ax1.text(tasa + 1, i, f'{tasa:.1f}%',
                    ha='left', va='center', fontsize=9, fontweight='bold')

        # Gráfico 2: Total de estudiantes por nacionalidad
        bars2 = ax2.barh(range(len(nacionalidades)), totales, color='#4dabf7', edgecolor='black')
        ax2.set_yticks(range(len(nacionalidades)))
        ax2.set_yticklabels([nac[:25] for nac in nacionalidades])
        ax2.set_xlabel('Número de Estudiantes', fontsize=11)
        ax2.set_title('📊 Total de Estudiantes', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)

        for i, total in enumerate(totales):
            ax2.text(total + max(totales)*0.01, i, f'{int(total)}',
                    ha='left', va='center', fontsize=9)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_aulas_detalle)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def mostrar_tabla_detallada_aulas(self):
        """Muestra tabla detallada con nivel, nacionalidad y promoción"""
        for widget in self.frame_contenido_aulas_detalle.winfo_children():
            widget.destroy()

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_aulas_detalle, wrap=tk.WORD, font=('Courier', 9))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        datos = self.analizador.obtener_analisis_detallado_aulas_acollida()
        if not datos or 'nivel_x_nacionalidad' not in datos:
            texto_widget.insert(tk.END, "No hay datos suficientes para tabla detallada")
            return

        texto = ""
        texto += "="*95 + "\n"
        texto += "📋 TABLA DETALLADA: NIVEL x NACIONALIDAD\n"
        texto += "="*95 + "\n\n"

        texto += f"{'Nivel':<8} {'Nacionalidad':<40} {'Estudiantes':>12}\n"
        texto += "-"*95 + "\n"

        # Mostrar todos los cruces ordenados por nivel y luego por total
        nivel_nac = datos['nivel_x_nacionalidad'].sort_index()

        for (nivel, nac), total in nivel_nac.items():
            texto += f"{nivel:<8} {nac[:40]:<40} {int(total):>12,}\n"

        texto += "\n" + "="*95 + "\n"
        texto += f"TOTAL: {int(datos['total_estudiantes']):,} estudiantes\n"
        texto += "="*95 + "\n"

        texto_widget.insert(tk.END, texto)

    # ==================== PESTAÑA 6: DIVERSIDAD CULTURAL ====================

    def crear_pestana_diversidad_cultural(self):
        """Crea la pestaña de diversidad cultural"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌍 Diversidad Cultural")

        # Frame de controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(frame_controles, text="📊 Resumen Diversidad",
                   command=self.mostrar_resumen_diversidad).grid(row=0, column=0, padx=5)
        ttk.Button(frame_controles, text="🥧 Gráfico Circular",
                   command=self.grafico_circular_diversidad).grid(row=0, column=1, padx=5)
        ttk.Button(frame_controles, text="📊 Top 10 Orígenes",
                   command=self.grafico_top_origenes).grid(row=0, column=2, padx=5)
        ttk.Button(frame_controles, text="📈 Evolución por Nivel",
                   command=self.grafico_diversidad_por_nivel).grid(row=0, column=3, padx=5)

        # Frame para contenido
        self.frame_contenido_diversidad = ttk.Frame(frame)
        self.frame_contenido_diversidad.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def mostrar_resumen_diversidad(self):
        """Muestra resumen de diversidad"""
        for widget in self.frame_contenido_diversidad.winfo_children():
            widget.destroy()

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_diversidad, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        stats = self.analizador.obtener_resumen_diversidad()
        if not stats:
            texto_widget.insert(tk.END, "No hay datos disponibles")
            return

        texto = ""
        texto += "="*70 + "\n"
        texto += "🌍 RESUMEN DE DIVERSIDAD CULTURAL\n"
        texto += "="*70 + "\n\n"

        texto += f"Total estudiantes: {int(stats['total_estudiantes']):,}\n"
        texto += f"Españoles: {int(stats['total_espana']):,} ({stats['porcentaje_espana']:.1f}%)\n"
        texto += f"Extranjeros: {int(stats['total_extranjeros']):,} ({stats['porcentaje_extranjeros']:.1f}%)\n\n"

        texto += "TOP 10 NACIONALIDADES:\n"
        texto += "-"*70 + "\n"
        for i, (origen, total) in enumerate(stats['top_nacionalidades'].head(10).items(), 1):
            porcentaje = (total / stats['total_estudiantes'] * 100)
            texto += f"{i:2d}. {origen:40s} {int(total):8,} ({porcentaje:5.2f}%)\n"

        texto_widget.insert(tk.END, texto)

    def grafico_circular_diversidad(self):
        """Gráfico circular de diversidad"""
        for widget in self.frame_contenido_diversidad.winfo_children():
            widget.destroy()

        stats = self.analizador.obtener_resumen_diversidad()
        if not stats:
            messagebox.showwarning("Advertencia", "No hay datos disponibles")
            return

        fig, ax = plt.subplots(figsize=(10, 8))

        # Top 7 + Otros
        top7 = stats['top_nacionalidades'].head(7)
        otros = stats['top_nacionalidades'][7:].sum()

        labels = list(top7.index) + ['Otros']
        sizes = list(top7.values) + [otros]

        # Colores
        colors = plt.cm.Set3(range(len(labels)))

        # Explotar España
        explode = [0.1 if 'ESPANYA' in label else 0 for label in labels]

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, explode=explode, shadow=True)
        ax.set_title('🥧 Distribución por Nacionalidad', fontsize=14, fontweight='bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_diversidad)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_top_origenes(self):
        """Gráfico Top 10 orígenes"""
        for widget in self.frame_contenido_diversidad.winfo_children():
            widget.destroy()

        stats = self.analizador.obtener_resumen_diversidad()
        if not stats:
            messagebox.showwarning("Advertencia", "No hay datos disponibles")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        top10 = stats['top_nacionalidades'].head(10)

        bars = ax.barh(range(len(top10)), top10.values,
                      color=plt.cm.viridis(np.linspace(0.3, 0.9, len(top10))))
        ax.set_yticks(range(len(top10)))
        ax.set_yticklabels(top10.index)
        ax.set_title('📊 Top 10 Orígenes', fontsize=14, fontweight='bold')
        ax.set_xlabel('Número de Estudiantes', fontsize=12)
        ax.grid(axis='x', alpha=0.3)

        for i, (bar, valor) in enumerate(zip(bars, top10.values)):
            porcentaje = (valor / stats['total_estudiantes'] * 100)
            ax.text(valor + max(top10.values)*0.01, i,
                   f'{int(valor):,} ({porcentaje:.1f}%)',
                   ha='left', va='center', fontsize=10)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_diversidad)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_diversidad_por_nivel(self):
        """Gráfico de evolución de diversidad por nivel"""
        for widget in self.frame_contenido_diversidad.winfo_children():
            widget.destroy()

        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        col_nivel = 'Nivell'
        col_nacionalidad = self.analizador.buscar_columna(['Zona', 'Nacionalitat'])
        col_numero = self.analizador.buscar_columna(['mero', 'Avalua'])

        if col_nacionalidad is None or col_numero is None or col_nivel not in self.analizador.df_actual.columns:
            messagebox.showwarning("Advertencia", "Columnas necesarias no encontradas")
            return

        fig, ax = plt.subplots(figsize=(12, 7))

        # Obtener top 6 nacionalidades
        top6 = self.analizador.df_actual.groupby(col_nacionalidad)[col_numero].sum().sort_values(ascending=False).head(6).index

        # Preparar datos por nivel
        niveles = sorted(self.analizador.df_actual[col_nivel].unique())
        datos_por_nac = {nac: [] for nac in top6}

        for nivel in niveles:
            df_nivel = self.analizador.df_actual[self.analizador.df_actual[col_nivel] == nivel]
            for nac in top6:
                total = df_nivel[df_nivel[col_nacionalidad] == nac][col_numero].sum()
                datos_por_nac[nac].append(total)

        # Crear gráfico de barras apiladas
        x = np.arange(len(niveles))
        width = 0.6

        bottom = np.zeros(len(niveles))
        colors = plt.cm.tab10(range(len(top6)))

        for i, (nac, valores) in enumerate(datos_por_nac.items()):
            ax.bar(x, valores, width, label=nac, bottom=bottom, color=colors[i])
            bottom += valores

        ax.set_xlabel('Nivel', fontsize=12)
        ax.set_ylabel('Número de Estudiantes', fontsize=12)
        ax.set_title('📈 Evolución de Diversidad por Nivel', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(niveles)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_diversidad)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================== PESTAÑA 6: COMPARATIVA GRUPOS ====================

    def crear_pestana_comparativa_grupos(self):
        """Crea la pestaña de comparativa entre grupos culturales"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚖️ Comparativa Grupos")

        frame_controles = ttk.Frame(frame)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(frame_controles, text="📊 Tabla Comparativa",
                   command=self.mostrar_tabla_comparativa).grid(row=0, column=0, padx=5)
        ttk.Button(frame_controles, text="📈 Tasas de Promoción",
                   command=self.grafico_tasas_promocion).grid(row=0, column=1, padx=5)
        ttk.Button(frame_controles, text="📉 Brechas Educativas",
                   command=self.grafico_brechas).grid(row=0, column=2, padx=5)

        self.frame_contenido_comparativa = ttk.Frame(frame)
        self.frame_contenido_comparativa.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def mostrar_tabla_comparativa(self):
        """Muestra tabla comparativa de grupos"""
        for widget in self.frame_contenido_comparativa.winfo_children():
            widget.destroy()

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_comparativa, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        stats = self.analizador.obtener_comparativa_grupos()
        if not stats:
            texto_widget.insert(tk.END, "No hay datos disponibles")
            return

        texto = ""
        texto += "="*90 + "\n"
        texto += "⚖️ TABLA COMPARATIVA DE GRUPOS CULTURALES\n"
        texto += "="*90 + "\n\n"

        texto += f"{'Grupo':<20} {'Total':>10} {'Promocionan':>12} {'Tasa %':>8} {'Repiten':>10} {'Tasa %':>8}\n"
        texto += "-"*90 + "\n"

        for grupo, datos in stats.items():
            texto += f"{grupo:<20} "
            texto += f"{int(datos['total']):>10,} "
            texto += f"{int(datos['promovidos']):>12,} "
            texto += f"{datos['tasa_promocion']:>8.1f} "
            texto += f"{int(datos['repiten']):>10,} "
            texto += f"{datos['tasa_repeticion']:>8.1f}\n"

        texto_widget.insert(tk.END, texto)

    def grafico_tasas_promocion(self):
        """Gráfico de tasas de promoción"""
        for widget in self.frame_contenido_comparativa.winfo_children():
            widget.destroy()

        stats = self.analizador.obtener_comparativa_grupos()
        if not stats:
            messagebox.showwarning("Advertencia", "No hay datos disponibles")
            return

        fig, ax = plt.subplots(figsize=(12, 7))

        grupos = list(stats.keys())
        tasas = [stats[g]['tasa_promocion'] for g in grupos]

        # Colores según tasa (verde si > 85%, rojo si < 85%)
        colores = ['#51cf66' if tasa >= 85 else '#ff6b6b' for tasa in tasas]

        bars = ax.barh(range(len(grupos)), tasas, color=colores, edgecolor='black')
        ax.set_yticks(range(len(grupos)))
        ax.set_yticklabels(grupos)
        ax.set_xlabel('Tasa de Promoción (%)', fontsize=12)
        ax.set_title('📈 Tasas de Promoción por Grupo Cultural', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

        # Línea de referencia en 85%
        ax.axvline(x=85, color='gray', linestyle='--', linewidth=2, alpha=0.5)

        for i, (bar, tasa) in enumerate(zip(bars, tasas)):
            ax.text(tasa + 1, i, f'{tasa:.1f}%',
                   ha='left', va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_comparativa)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def grafico_brechas(self):
        """Gráfico de brechas educativas"""
        for widget in self.frame_contenido_comparativa.winfo_children():
            widget.destroy()

        stats = self.analizador.obtener_comparativa_grupos()
        if not stats:
            messagebox.showwarning("Advertencia", "No hay datos disponibles")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

        grupos = list(stats.keys())
        tasas_promocion = [stats[g]['tasa_promocion'] for g in grupos]
        tasas_repeticion = [stats[g]['tasa_repeticion'] for g in grupos]

        # Calcular medias
        media_promocion = np.mean(tasas_promocion)
        media_repeticion = np.mean(tasas_repeticion)

        # Brechas
        brechas_promocion = [tasa - media_promocion for tasa in tasas_promocion]
        brechas_repeticion = [tasa - media_repeticion for tasa in tasas_repeticion]

        # Gráfico 1: Brecha de promoción
        colores1 = ['#51cf66' if b >= 0 else '#ff6b6b' for b in brechas_promocion]
        bars1 = ax1.barh(range(len(grupos)), brechas_promocion, color=colores1, edgecolor='black')
        ax1.set_yticks(range(len(grupos)))
        ax1.set_yticklabels(grupos)
        ax1.set_xlabel('Diferencia con la Media (puntos)', fontsize=11)
        ax1.set_title('📉 Brecha de Promoción', fontsize=12, fontweight='bold')
        ax1.axvline(x=0, color='black', linestyle='-', linewidth=1)
        ax1.grid(axis='x', alpha=0.3)

        for i, (bar, brecha) in enumerate(zip(bars1, brechas_promocion)):
            ax1.text(brecha + (0.2 if brecha >= 0 else -0.2), i,
                    f'{brecha:+.1f}', ha='left' if brecha >= 0 else 'right',
                    va='center', fontsize=9, fontweight='bold')

        # Gráfico 2: Brecha de repetición
        colores2 = ['#ff6b6b' if b >= 0 else '#51cf66' for b in brechas_repeticion]
        bars2 = ax2.barh(range(len(grupos)), brechas_repeticion, color=colores2, edgecolor='black')
        ax2.set_yticks(range(len(grupos)))
        ax2.set_yticklabels(grupos)
        ax2.set_xlabel('Diferencia con la Media (puntos)', fontsize=11)
        ax2.set_title('📉 Brecha de Repetición', fontsize=12, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)
        ax2.grid(axis='x', alpha=0.3)

        for i, (bar, brecha) in enumerate(zip(bars2, brechas_repeticion)):
            ax2.text(brecha + (0.05 if brecha >= 0 else -0.05), i,
                    f'{brecha:+.1f}', ha='left' if brecha >= 0 else 'right',
                    va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_contenido_comparativa)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================== PESTAÑA 7: ANÁLISIS POR CENTRO ====================

    def crear_pestana_analisis_centros(self):
        """Crea la pestaña de análisis por centro educativo"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏢 Análisis por Centro")

        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(frame, text="🔍 Buscar Centro", padding="10")
        frame_busqueda.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_busqueda, text="Código de Centro:").grid(row=0, column=0, padx=5)
        self.entry_codigo_centro = ttk.Entry(frame_busqueda, width=15)
        self.entry_codigo_centro.grid(row=0, column=1, padx=5)
        ttk.Button(frame_busqueda, text="Buscar",
                   command=self.buscar_centro).grid(row=0, column=2, padx=5)

        # Frame de controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(frame_controles, text="📊 Top Centros Diversos",
                   command=self.mostrar_top_centros_diversos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_controles, text="🏫 Centros con Aulas Acogida",
                   command=self.mostrar_centros_aulas).grid(row=0, column=1, padx=5)

        self.frame_contenido_centros = ttk.Frame(frame)
        self.frame_contenido_centros.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def buscar_centro(self):
        """Busca un centro específico"""
        for widget in self.frame_contenido_centros.winfo_children():
            widget.destroy()

        codigo = self.entry_codigo_centro.get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Ingresa un código de centro")
            return

        # Convertir a int si es posible
        try:
            codigo = int(codigo)
        except:
            pass

        stats = self.analizador.obtener_analisis_por_centro(codigo)

        if not stats:
            messagebox.showinfo("No encontrado", f"No se encontró el centro {codigo}")
            return

        # Mostrar resultados
        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_centros, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        texto = ""
        texto += "="*70 + "\n"
        texto += f"🏢 ANÁLISIS DEL CENTRO: {codigo}\n"
        texto += "="*70 + "\n\n"

        texto += f"Total de estudiantes: {int(stats['total_estudiantes']):,}\n"
        texto += f"Total de registros: {stats['registros']:,}\n\n"

        if 'en_aula_acollida' in stats:
            texto += f"Estudiantes en aulas de acogida: {int(stats['en_aula_acollida']):,}\n\n"

        if 'por_nacionalidad' in stats:
            texto += "DISTRIBUCIÓN POR NACIONALIDAD:\n"
            texto += "-"*70 + "\n"
            for origen, total in stats['por_nacionalidad'].sort_values(ascending=False).items():
                porcentaje = (total / stats['total_estudiantes'] * 100)
                texto += f"  {origen:40s} {int(total):6,} ({porcentaje:5.1f}%)\n"

        texto_widget.insert(tk.END, texto)

    def mostrar_top_centros_diversos(self):
        """Muestra top centros más diversos"""
        for widget in self.frame_contenido_centros.winfo_children():
            widget.destroy()

        centros = self.analizador.obtener_analisis_por_centro()

        if not centros:
            messagebox.showwarning("Advertencia", "No hay datos disponibles")
            return

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_centros, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        texto = ""
        texto += "="*80 + "\n"
        texto += "📊 TOP 20 CENTROS MÁS DIVERSOS\n"
        texto += "="*80 + "\n\n"

        texto += f"{'#':<4} {'Centro':<12} {'Total':>10} {'Extranjeros':>12} {'% Extran.':>10}\n"
        texto += "-"*80 + "\n"

        for i, centro in enumerate(centros[:20], 1):
            texto += f"{i:<4} {str(centro['centro']):<12} "
            texto += f"{int(centro['total']):>10,} "
            texto += f"{int(centro['extranjeros']):>12,} "
            texto += f"{centro['porcentaje']:>10.1f}%\n"

        texto_widget.insert(tk.END, texto)

    def mostrar_centros_aulas(self):
        """Muestra centros con más estudiantes en aulas de acogida"""
        for widget in self.frame_contenido_centros.winfo_children():
            widget.destroy()

        if self.analizador.df_actual is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return

        col_centro = self.analizador.buscar_columna(['Centre', 'Codi'])
        col_aula = self.analizador.buscar_columna(['Aula', 'acollida'])
        col_numero = self.analizador.buscar_columna(['mero', 'Avalua'])

        if not all([col_centro, col_aula, col_numero]):
            messagebox.showwarning("Advertencia", "Columnas necesarias no encontradas")
            return

        # Filtrar solo estudiantes en aulas de acogida
        df_acollida = self.analizador.df_actual[
            self.analizador.df_actual[col_aula].str.contains('S', na=False, case=False)
        ]

        if len(df_acollida) == 0:
            messagebox.showinfo("Info", "No hay estudiantes en aulas de acogida")
            return

        # Agrupar por centro
        centros_aulas = df_acollida.groupby(col_centro)[col_numero].sum().sort_values(ascending=False)

        texto_widget = scrolledtext.ScrolledText(self.frame_contenido_centros, wrap=tk.WORD, font=('Courier', 10))
        texto_widget.pack(fill=tk.BOTH, expand=True)

        texto = ""
        texto += "="*70 + "\n"
        texto += "🏫 TOP 20 CENTROS CON MÁS ESTUDIANTES EN AULAS DE ACOGIDA\n"
        texto += "="*70 + "\n\n"

        texto += f"{'#':<4} {'Centro':<12} {'Estudiantes':>15}\n"
        texto += "-"*70 + "\n"

        for i, (centro, total) in enumerate(centros_aulas.head(20).items(), 1):
            texto += f"{i:<4} {str(centro):<12} {int(total):>15,}\n"

        texto_widget.insert(tk.END, texto)


def main():
    root = tk.Tk()
    app = VentanaAnalisis(root)
    root.mainloop()


if __name__ == "__main__":
    main()
