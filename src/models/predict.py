"""
Módulo de inferencia y predicción sísmica en producción.
Proyecto: SISMOS
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union
import joblib
import numpy as np
import pandas as pd

# Definición de rutas base
BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = BASE_DIR / "models" / "pipeline_sismos_final.joblib"


def cargar_modelo(ruta_modelo: Optional[Union[str, Path]] = None) -> Any:
    """
    Carga el pipeline/modelo serializado con joblib.
    
    Args:
        ruta_modelo: Ruta al archivo .joblib o .pkl. Si es None, usa la ruta por defecto.
        
    Returns:
        El objeto pipeline/modelo cargado.
    """
    if ruta_modelo is None:
        ruta_modelo = DEFAULT_MODEL_PATH
        
    ruta_modelo = Path(ruta_modelo)
    if not ruta_modelo.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo del modelo en: '{ruta_modelo}'. "
            "Asegúrate de haber ejecutado el cuaderno de entrenamiento o guardado el pipeline primero."
        )
        
    print(f"[*] Cargando modelo desde: {ruta_modelo}")
    modelo = joblib.load(ruta_modelo)
    print("[+] Modelo cargado exitosamente.")
    return modelo


def predecir_sismo(
    modelo: Any,
    latitud: float,
    longitud: float,
    profundidad: float,
    hora: int = 12,
    mes: int = 1
) -> Dict[str, Any]:
    """
    Realiza la inferencia para un evento sísmico a partir de sus parámetros geofísicos y temporales.
    
    Args:
        modelo: Pipeline o estimador de scikit-learn ya entrenado.
        latitud: Latitud geográfica en grados decimales (ej. -12.05 para Lima).
        longitud: Longitud geográfica en grados decimales (ej. -77.04 para Lima).
        profundidad: Profundidad del foco sísmico en km.
        hora: Hora del evento en formato 0-23 (default: 12).
        mes: Mes del año 1-12 (default: 1).
        
    Returns:
        Diccionario con la predicción (0 o 1), probabilidades estimadas y etiqueta descriptiva.
    """
    # Construcción de DataFrame con nombres estándar de columnas
    datos_dict = {
        'LATITUD': [float(latitud)],
        'LONGITUD': [float(longitud)],
        'PROFUNDIDAD': [float(profundidad)],
        'HORA': [int(hora)],
        'MES': [int(mes)]
    }
    
    # Compatibilidad: si el estimador espera nombres en minúsculas
    if hasattr(modelo, "feature_names_in_"):
        nombres_esperados = list(modelo.feature_names_in_)
        # Si las columnas del modelo están en minúsculas
        if any(c.islower() for c in nombres_esperados):
            datos_dict = {k.lower(): v for k, v in datos_dict.items() if k.lower() in nombres_esperados}
        else:
            datos_dict = {k: v for k, v in datos_dict.items() if k in nombres_esperados}
            
    df_input = pd.DataFrame(datos_dict)
    
    # Predicción de clase
    pred_clase = int(modelo.predict(df_input)[0])
    
    # Estimación de probabilidades si el modelo lo soporta
    prob_no_severo, prob_severo = None, None
    if hasattr(modelo, "predict_proba"):
        probabilidades = modelo.predict_proba(df_input)[0]
        # Si es clasificación binaria
        if len(probabilidades) == 2:
            prob_no_severo = float(probabilidades[0])
            prob_severo = float(probabilidades[1])
        else:
            prob_severo = float(probabilidades[pred_clase])
            
    resultado = {
        'parametros_entrada': {
            'latitud': latitud,
            'longitud': longitud,
            'profundidad_km': profundidad,
            'hora': hora,
            'mes': mes
        },
        'es_severo': pred_clase,
        'etiqueta': "SEVERO (Magnitud >= 5.0)" if pred_clase == 1 else "LEVE / MODERADO (Magnitud < 5.0)",
        'probabilidad_severo': prob_severo,
        'probabilidad_no_severo': prob_no_severo
    }
    
    return resultado


if __name__ == '__main__':
    print("=" * 65)
    print(" SISTEMA DE INFERENCIA SÍSMICA - IGP (PRODUCCIÓN) ")
    print("=" * 65)
    
    # Parámetros de prueba: evento frente a la costa central (Lima)
    test_lat = -12.05
    test_lon = -77.04
    test_prof = 35.0  # sismo superficial típico de subducción
    test_hora = 14
    test_mes = 6
    
    print("\n[i] Parámetros de sismo de prueba:")
    print(f"    - Ubicación: Latitud {test_lat}, Longitud {test_lon} (Costa de Lima)")
    print(f"    - Profundidad: {test_prof} km")
    print(f"    - Hora: {test_hora}:00 UTC | Mes: {test_mes}")
    
    try:
        modelo = cargar_modelo()
        print("\n[*] Ejecutando predicción con el modelo en producción...")
        resultado = predecir_sismo(
            modelo,
            latitud=test_lat,
            longitud=test_lon,
            profundidad=test_prof,
            hora=test_hora,
            mes=test_mes
        )
        print("\n--- RESULTADO DE LA PREDICCIÓN ---")
        print(f"Clasificación      : {resultado['etiqueta']}")
        print(f"Flag Binario       : {resultado['es_severo']}")
        if resultado['probabilidad_severo'] is not None:
            print(f"Prob. Sismo Severo : {resultado['probabilidad_severo'] * 100:.2f}%")
            print(f"Prob. Sismo Leve   : {resultado['probabilidad_no_severo'] * 100:.2f}%")
        print("=" * 65)
        
    except FileNotFoundError as e:
        print("\n[!] AVISO INFORMATIVO:")
        print(f"    {e}")
        print("\n[i] El módulo está 100% listo para producción. Una vez que el cuaderno")
        print(f"    guarde el archivo en '{DEFAULT_MODEL_PATH}',")
        print("    este script cargará el pipeline y ejecutará las inferencias en tiempo real.")
        print("=" * 65)
