# Bitácora de Sesión: Backend & Data Engineering (Back)

**Proyecto:** SISMOS - Análisis, Pipeline y Predicción de Eventos Sísmicos (IGP 1960 - 2025)  
**Rol:** Backend & Data Engineering  
**Ubicación de Proyecto:** `/home/pierooo/Projects/ai_model/SISMOS`  
**Fecha:** 26 de Septiembre de 2026  

---

## 1. Rol y Responsabilidades
En este proyecto, la sesión de **Backend** se encargó de:
1. Arquitectura de carpetas y estandarización del proyecto siguiendo el modelo de referencia `Pipeline-riesgo-bancario`.
2. Ingesta, saneamiento y transformación de datos brutos del Instituto Geofísico del Perú (IGP).
3. Construcción del pipeline modular de datos y persistencia del dataset limpio procesado.
4. Creación de la infraestructura de modelos e implementación del módulo de inferencia en producción (`predict.py`) para consumir los modelos serializados (`.joblib`).
5. Comunicación y sincronización continua con la sesión de Ciencia de Datos (Kiara).

---

## 2. Reestructuración y Organización Inicial del Proyecto
Siguiendo las pautas de ingeniería del proyecto `Pipeline-riesgo-bancario`, se transformó el espacio de trabajo que inicialmente tenía archivos sueltos en una arquitectura limpia y desacoplada:

### Estructura Implementada
```text
/home/pierooo/Projects/ai_model/SISMOS/
├── data/
│   ├── raw/
│   │   └── IGP/
│   │       ├── IGP_catalogo_sismico_1960_ 2025_Dataset.csv
│   │       ├── IGP_catalogo_sismicos_desde_1960_ DiccionarioDatos.xlsx
│   │       └── IGP_catalogo_sismicos_desde_1960_ Metadatos_0.docx
│   └── processed/
│       └── sismos_limpios.csv
├── models/
│   └── pipeline_sismos_final.joblib
├── NOTEBOOKS/
│   ├── 01_auditoria_y_exploracion.ipynb
│   └── proyecto_integrador_sismos.ipynb
├── sesiones/
│   └── sesion_back.md
├── src/
│   ├── data/
│   │   └── igp_loader.py
│   └── models/
│       └── predict.py
├── README.md
└── requirements.txt
```

### Acciones Iniciales
- **Carpetas creadas:** `data/raw/IGP/`, `NOTEBOOKS/`, `src/data/`, `models/`, `src/models/`, `sesiones/`.
- **Archivos organizados:** Se reubicaron los archivos crudos del IGP dentro de `data/raw/IGP/`.
- **Configuración inicial:**
  - `requirements.txt`: Inclusión de librerías (`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `openpyxl`, `joblib`).
  - `README.md`: Documentación del objetivo del proyecto, estructura del repositorio e instrucciones de uso.

---

## 3. Módulo de Ingesta y Limpieza: `src/data/igp_loader.py`
Se desarrolló un módulo de ingeniería de datos totalmente reutilizable y modular, compuesto por funciones puras y la clase orquestadora `IGPDataLoader`.

### Lógica Clave Implementada:
1. **Lectura y Normalización de Encabezados:**
   - Carga con delimitador `;`.
   - Limpieza de nombres de columnas eliminando espacios en blanco y estandarizando en mayúsculas.
2. **Tratamiento Crítico de Fechas y Horas:**
   - En el archivo crudo, `HORA_UTC` es numérico (`int`), por lo que horas como las 00:08:03 figuraban como `803`.
   - Se implementó relleno de ceros a la izquierda mediante `.str.zfill(6)` para recomponer el formato `HHMMSS`.
   - Concatenación de `FECHA_UTC` (formato `YYYYMMDD`) y `HORA_UTC` (`HHMMSS`), parseándolas con `pd.to_datetime(..., format='%Y%m%d%H%M%S')` en la columna `FECHA_HORA`.
3. **Variables Temporales Derivadas:**
   - Extracción de componentes útiles para análisis y modelado: `ANIO`, `MES`, `DIA`, `HORA`.
4. **Coherencia Física y Tipado Numérico:**
   - Conversión de variables a numéricas (`LATITUD`, `LONGITUD`, `PROFUNDIDAD`, `MAGNITUD`).
   - Filtrado de valores físicamente inconsistentes (`PROFUNDIDAD >= 0`, `MAGNITUD > 0`).
5. **Creación de Variable Objetivo (Target):**
   - Creación de la etiqueta binaria `SISMO_SEVERO = (MAGNITUD >= 5.0).astype(int)`.
6. **Persistencia Automática:**
   - Exportación a `data/processed/sismos_limpios.csv` con creación automática de directorios.

### Resultados de la Ingesta:
- **Total registros procesados:** 24,289 eventos (0 registros nulos descartados).
- **Rango temporal:** 13 de Enero de 1960 a 31 de Diciembre de 2025.
- **Distribución de severidad:**
  - Sismos no severos ($< 5.0$ Mw): 78.99% (19,185 eventos).
  - Sismos severos ($\ge 5.0$ Mw): 21.01% (5,104 eventos).

---

## 4. Infraestructura de Inferencia: `src/models/predict.py`
Para llevar los modelos generados por la sesión de Data Science a un entorno productivo, se implementó el módulo de inferencia.

### Funcionalidades:
- **`cargar_modelo(ruta_modelo=None)`:**
  - Utiliza `joblib.load` para deserializar el pipeline completo (preprocesador + modelo).
  - Manejo robusto de rutas relativas y absolutas con `pathlib.Path`.
  - Notificación amigable mediante excepciones si el artefacto aún no ha sido entrenado.
- **`predecir_sismo(modelo, latitud, longitud, profundidad, hora, mes)`:**
  - Construye el vector de características en un `DataFrame`.
  - Mapeo dinámico e insensible a mayúsculas/minúsculas para adaptarse a las columnas que espera el pipeline (`feature_names_in_`).
  - Obtiene la clase predicha (`predict`) y las probabilidades de severidad (`predict_proba`).
  - Retorna un diccionario estructurado con las probabilidades, el flag binario y una etiqueta amigable.
- **Bloque de Ejecución (`__main__`):**
  - Permite evaluar sismos directamente desde la terminal.

---

## 5. Pruebas y Validaciones de Punta a Punta
Una vez que el cuaderno `proyecto_integrador_sismos.ipynb` exportó el artefacto entrenado a `models/pipeline_sismos_final.joblib` (7.9 MB), se probó la inferencia en producción ejecutando `python3 src/models/predict.py`:

```bash
$ python3 /home/pierooo/Projects/ai_model/SISMOS/src/models/predict.py
```
**Salida de la prueba:**
- **Ubicación:** Latitud -12.05, Longitud -77.04 (Costa de Lima).
- **Profundidad:** 35.0 km | Hora: 14:00 UTC | Mes: Junio.
- **Carga de artefacto:** Exitosa (`models/pipeline_sismos_final.joblib`).
- **Predicción generada (Modelo Optimizado 8.8 MB con GridSearchCV):**
  - Clasificación: `LEVE / MODERADO (Magnitud < 5.0)`
  - Flag Binario: `0`
  - Probabilidad Sismo Severo: `46.72%`
  - Probabilidad Sismo Leve: `53.28%`

---

## 6. Documentación Técnica del Proyecto (`README.md`)
Se redactó y estructuró el archivo principal `SISMOS/README.md` con un estándar formal de ingeniería:
- **Resumen Ejecutivo:** Descripción del catálogo sísmico instrumental del IGP (1960–2025, 24,289 observaciones).
- **Estructura del Proyecto:** Desglose del árbol de directorios con sus roles.
- **Tabla Comparativa de Modelos:** Integración de la tabla de rendimiento de los 4 clasificadores (Logística, KNN, Árbol y Random Forest).
- **Importancia de Variables y Optimización:** Documentación de los resultados de `GridSearchCV` y desglose de pesos geofísicos.
- **Instrucciones de Reproducción:** Pasos exactos para clonar, instalar dependencias, ejecutar notebooks y realizar inferencias por terminal o script.

---

## 7. Refactorización y Limpieza de Código
A solicitud del usuario, se realizó una auditoría y limpieza de comentarios en todo el proyecto:
- Se eliminaron todos los comentarios redundantes en bloques de importación (tales como `# Tratamiento de datos y álgebra lineal`, `# Visualización gráfica`, `# Scikit-Learn: Algoritmos de Clasificación`, `# Manejo y estructuración de datos`, etc.) en los cuadernos `01_auditoria_y_exploracion.ipynb` y `proyecto_integrador_sismos.ipynb`.
- Se preservaron íntegramente las salidas (`outputs`) ejecutadas y el renderizado de gráficos/tablas en los cuadernos.
- Se mantuvieron intactos los docstrings formales y aquellos comentarios esenciales que justifican la lógica de negocio (por ejemplo, el tratamiento de relleno de ceros en `HORA_UTC`, validaciones de coherencia geofísica y configuración de parámetros).

---

## 8. Arquitectura y Visualización Dataflow con Archify
Para maximizar la claridad visual y el estándar de documentación del pipeline:
- Se modeló y validó el diagrama de arquitectura y flujo del pipeline usando **Archify** (perfil showcase con 9/9 validaciones exitosas, 0 errores, 0 warnings).
- Se compiló el entregable interactivo HTML en:
  `docs/pipeline_arquitectura.html`
- Se generó el render visual embebido directamente en la sección de arquitectura de `README.md` junto con el enlace al visor interactivo.
- Se sincronizaron los cambios con el repositorio remoto de GitHub ([commit `692c051`](https://github.com/Pierorivera1/SISMOS/commit/692c051)).

---

## 9. Guía Rápida para Refrescar Contexto en Futuras Sesiones
Si se retoma este repositorio en una sesión futura o con otro agente:

1. **Rutas principales:**
   - Raíz del proyecto: `/home/pierooo/Projects/ai_model/SISMOS/`
   - Datos crudos: `data/raw/IGP/`
   - Dataset limpio: `data/processed/sismos_limpios.csv`
   - Modelos exportados: `models/pipeline_sismos_final.joblib`
   - Código fuente backend: `src/data/igp_loader.py` y `src/models/predict.py`
   - Cuadernos: `NOTEBOOKS/01_auditoria_y_exploracion.ipynb` y `NOTEBOOKS/proyecto_integrador_sismos.ipynb`
   - Bitácoras: `sesiones/sesion_back.md`

2. **Comandos clave de verificación:**
   ```bash
   # Re-ejecutar el pipeline de datos completo
   python3 src/data/igp_loader.py

   # Ejecutar inferencia en producción con el modelo actual
   python3 src/models/predict.py
   ```

3. **Flujo de trabajo para nuevas mejoras:**
   - Si se agregan nuevas variables (ej. distancia a la fosa de subducción o tasas sísmicas móviles), agregarlas en `limpiar_y_transformar` dentro de `src/data/igp_loader.py`.
   - Reentrenar el pipeline en `NOTEBOOKS/proyecto_integrador_sismos.ipynb` para que sobrescriba `models/pipeline_sismos_final.joblib`.
   - `src/models/predict.py` continuará funcionando automáticamente sirviendo las predicciones.
