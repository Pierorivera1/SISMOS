"""
Módulo de ingesta y preprocesamiento de datos sísmicos del IGP.
Proyecto: SISMOS (1960 - 2025)
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

# Definición de rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_RAW_PATH = BASE_DIR / "data" / "raw" / "IGP" / "IGP_catalogo_sismico_1960_ 2025_Dataset.csv"
DEFAULT_PROCESSED_PATH = BASE_DIR / "data" / "processed" / "sismos_limpios.csv"


def cargar_catalogo_crudo(ruta_csv=None) -> pd.DataFrame:
    """
    Carga el catálogo sísmico en formato CSV separado por punto y coma (';')
    y normaliza los nombres de las columnas.
    """
    if ruta_csv is None:
        ruta_csv = DEFAULT_RAW_PATH
    
    ruta_csv = Path(ruta_csv)
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos crudos en: {ruta_csv}")
    
    print(f"[*] Cargando catálogo crudo desde: {ruta_csv}")
    df = pd.read_csv(ruta_csv, sep=';')
    
    # Limpieza de nombres de columnas (quitar espacios en blanco al inicio/final)
    df.columns = [col.strip().upper() for col in df.columns]
    print(f"[+] Datos cargados exitosamente: {df.shape[0]:,} registros y {df.shape[1]} columnas.")
    
    return df


def limpiar_y_transformar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia tipos de datos, parsea fechas/horas a datetime UTC,
    extrae componentes temporales, filtra registros inconsistentes
    y crea la variable objetivo 'SISMO_SEVERO'.
    """
    df = df.copy()
    
    # 1. Asegurar tipos numéricos para variables clave
    cols_numericas = ['FECHA_UTC', 'HORA_UTC', 'LATITUD', 'LONGITUD', 'PROFUNDIDAD', 'MAGNITUD']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Parseo de FECHA_UTC (YYYYMMDD) y HORA_UTC (HHMMSS)
    # HORA_UTC numérica puede haber perdido ceros a la izquierda (ej. 803 -> 000803)
    fecha_str = df['FECHA_UTC'].dropna().astype(np.int64).astype(str)
    hora_str = df['HORA_UTC'].dropna().astype(np.int64).astype(str).str.zfill(6)
    
    timestamp_str = fecha_str + hora_str
    df['FECHA_HORA'] = pd.to_datetime(timestamp_str, format='%Y%m%d%H%M%S', errors='coerce')
    
    # 3. Filtrar valores nulos o inválidos generados en el parseo o en mediciones críticas
    n_inicial = len(df)
    df = df.dropna(subset=['FECHA_HORA', 'LATITUD', 'LONGITUD', 'PROFUNDIDAD', 'MAGNITUD'])
    
    # Filtro de coherencia física
    df = df[(df['PROFUNDIDAD'] >= 0) & (df['MAGNITUD'] > 0)]
    n_filtrados = n_inicial - len(df)
    if n_filtrados > 0:
        print(f"[!] Se descartaron {n_filtrados} registros nulos o con datos incoherentes.")

    # 4. Extraer variables temporales derivadas
    df['ANIO'] = df['FECHA_HORA'].dt.year
    df['MES'] = df['FECHA_HORA'].dt.month
    df['DIA'] = df['FECHA_HORA'].dt.day
    df['HORA'] = df['FECHA_HORA'].dt.hour

    # 5. Variable objetivo binaria de severidad (Magnitud >= 5.0 considerada moderada/fuerte en Perú)
    df['SISMO_SEVERO'] = (df['MAGNITUD'] >= 5.0).astype(int)

    # 6. Ordenar cronológicamente y reorganizar columnas
    df = df.sort_values(by='FECHA_HORA').reset_index(drop=True)
    
    columnas_ordenadas = [
        'ID', 'FECHA_HORA', 'ANIO', 'MES', 'DIA', 'HORA',
        'LATITUD', 'LONGITUD', 'PROFUNDIDAD', 'MAGNITUD',
        'SISMO_SEVERO'
    ]
    # Conservar FECHA_CORTE si existía
    if 'FECHA_CORTE' in df.columns:
        columnas_ordenadas.append('FECHA_CORTE')
        
    df = df[[c for c in columnas_ordenadas if c in df.columns]]
    print(f"[+] Transformación completada: {len(df):,} registros válidos.")
    
    return df


def guardar_procesado(df: pd.DataFrame, ruta_salida=None) -> Path:
    """
    Exporta el DataFrame procesado en formato CSV listo para modelado.
    Crea automáticamente las carpetas necesarias si no existen.
    """
    if ruta_salida is None:
        ruta_salida = DEFAULT_PROCESSED_PATH
        
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(ruta_salida, index=False)
    print(f"[+] Dataset procesado guardado con éxito en: {ruta_salida}")
    return ruta_salida


class IGPDataLoader:
    """
    Clase envolvente modular para ejecutar el pipeline de ingesta y preparación
    de datos sísmicos del IGP.
    """
    def __init__(self, ruta_raw=None, ruta_processed=None):
        self.ruta_raw = ruta_raw or DEFAULT_RAW_PATH
        self.ruta_processed = ruta_processed or DEFAULT_PROCESSED_PATH

    def ejecutar_pipeline(self) -> pd.DataFrame:
        df_raw = cargar_catalogo_crudo(self.ruta_raw)
        df_limpio = limpiar_y_transformar(df_raw)
        guardar_procesado(df_limpio, self.ruta_processed)
        return df_limpio


if __name__ == '__main__':
    print("=" * 60)
    print(" PIPELINE DE INGESTA Y LIMPIEZA - SISMOS IGP ")
    print("=" * 60)
    
    loader = IGPDataLoader()
    df_resultado = loader.ejecutar_pipeline()
    
    print("\n--- RESUMEN DEL DATASET PROCESADO ---")
    print(f"Dimensiones: {df_resultado.shape}")
    print(f"Rango temporal: {df_resultado['FECHA_HORA'].min()} a {df_resultado['FECHA_HORA'].max()}")
    print("\nDistribución de SISMO_SEVERO (Magnitud >= 5.0):")
    print(df_resultado['SISMO_SEVERO'].value_counts(normalize=True).mul(100).round(2).rename("Porcentaje (%)"))
    print("\nPrimeras 5 filas:")
    print(df_resultado.head())
    print("=" * 60)
