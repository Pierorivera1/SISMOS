# Bitácora de Sesión: Kiara (Jupyter Interactive Environment, Geospatial EDA & Master Integrator)

- **ID de Conversación:** `2c18b352-afc2-4582-a6ea-c708a7dba92e`
- **Panel Herdr:** `w1:p8`
- **Nombre asignado por el usuario:** **Kiara** (renombrada mediante `/rename`)
- **Rol Principal:** Especialista en Entorno Interactivo Jupyter para VS Code, Análisis Exploratorio Geoespacial y Desarrollo del Cuaderno Maestro Integrador (`proyecto_integrador_sismos.ipynb`).

---

## 1. Configuración del Entorno de Trabajo (VS Code & Python)

Para que el usuario pudiera interactuar con el código exactamente como en **Google Colab** pero dentro de su entorno local de **VS Code**, se realizó una auditoría y aprovisionamiento completo del stack técnico:

1. **Extensión oficial de VS Code:**
   - Se detectó que el editor no disponía de soporte para notebooks.
   - Se instaló la extensión oficial de Microsoft: `ms-toolsai.jupyter` (junto con sus extensiones satélite `jupyter-renderers`, `jupyter-keymap` y `vscode-jupyter-cell-tags`).

2. **Núcleo de Ejecución de Python (`ipykernel`):**
   - Se instaló el paquete `ipykernel` sobre el entorno de Python administrado con `mise` (`python 3.14`).
   - Se registró formalmente el kernel en el sistema para permitir ejecución interactiva celda por celda:
     ```bash
     python3 -m ipykernel install --user --name python3 --display-name "Python 3 (ipykernel)"
     ```

3. **Instalación de Dependencias Científicas y de ML:**
   - Se instalaron todas las bibliotecas de `SISMOS/requirements.txt`:
     - `pandas` (3.0.6) y `numpy` (2.5.3): Manipulación tabular y cálculo matricial.
     - `scikit-learn` (1.9.1): Modelos predictivos, preprocesamiento y métricas.
     - `matplotlib` (3.11.2) y `seaborn` (0.13.2): Visualizaciones estadísticas y geoespaciales.
     - `openpyxl` (3.1.5): Lectura del diccionario de datos en Excel.
     - `joblib` (1.6.0): Serialización y despliegue del pipeline final.
     - `nbconvert` (7.17.1): Renderizado, validación y pre-ejecución no interactiva de los cuadernos.

---

## 2. Primer Cuaderno: `01_auditoria_y_exploracion.ipynb`

Se construyó y pre-ejecutó el primer cuaderno del proyecto en [`SISMOS/NOTEBOOKS/01_auditoria_y_exploracion.ipynb`](../NOTEBOOKS/01_auditoria_y_exploracion.ipynb), enfocado en la fase de auditoría inicial (siguiendo los Cuadernos 01 y 02 de la clase):

- **Ingesta del Catálogo Sísmico Oficial del IGP:**
  - Archivo fuente: `data/raw/IGP/IGP_catalogo_sismico_1960_ 2025_Dataset.csv` delimitado por punto y coma (`;`).
  - Cobertura: **24,289 observaciones** registradas entre 1960 y 2025, distribuidas en 8 columnas (`ID`, `FECHA_UTC`, `HORA_UTC`, `LATITUD`, `LONGITUD`, `PROFUNDIDAD`, `MAGNITUD`, `FECHA_CORTE`).
  - Inspección del diccionario de datos: `data/raw/IGP/IGP_catalogo_sismicos_desde_1960_ DiccionarioDatos.xlsx`.
- **Auditoría de Calidad:**
  - **0% de valores nulos** en las variables hipocentrales cuantitativas.
  - **0 registros duplicados exactos**.
- **Análisis Estadístico y Visual:**
  - **Magnitud:** Media de $4.5$, rango entre $\sim 3.0$ y $> 8.0$. Distribución asimétrica positiva conforme a la ley de Gutenberg-Richter.
  - **Profundidad:** Distribución bimodal marcada, con concentración de sismos someros ($< 60\text{ km}$) en la costa y eventos profundos ($> 500\text{ km}$) en la selva baja / frontera oriental.
  - **Mapeo Espacial Geoespacial:** Representación de `LONGITUD` vs `LATITUD` codificando profundidad y magnitud, reproduciendo con exactitud la fosa oceánica de subducción entre la Placa de Nazca y la Placa Sudamericana.

---

## 3. Cuaderno Maestro Integrador: `proyecto_integrador_sismos.ipynb`

Atendiendo el consenso del equipo (siguiendo la plantilla maestra `cuadernos/cuaderno-13-proyecto-final.ipynb`), se condensó todo el ciclo de vida de Machine Learning en un único cuaderno reproducible de alto impacto en [`SISMOS/NOTEBOOKS/proyecto_integrador_sismos.ipynb`](../NOTEBOOKS/proyecto_integrador_sismos.ipynb).

### Estructura y Decisiones Técnicas:

1. **Carga de Datos Limpios:**
   - Fuente: `data/processed/sismos_limpios.csv` generado por el pipeline de Back.
2. **Definición de la Variable Objetivo ($y$):**
   - $\text{SISMO\_SEVERO} = 1$ si $\text{MAGNITUD} \ge 5.0$, sino $0$.
   - **Diagnóstico del Desbalance de Clases:**
     - Clase 0 (No Severo, $< 5.0$): **$19,184$ registros ($78.98\%$)**.
     - Clase 1 (Severo, $\ge 5.0$): **$5,105$ registros ($21.02\%$)**.
   - **Implicancia:** Se descartó el *Accuracy* como métrica decisoria principal debido al sesgo de clase mayoritaria. Se priorizó el **Recall / Sensibilidad** de la clase 1 (crítico en alertas sísmicas para minimizar falsos negativos) y el **ROC-AUC**.
3. **Control Estricto de Fuga de Información (*Data Leakage*):**
   - Se aisló de forma explícita la columna `MAGNITUD` (variable origen del target) para evitar cualquier fuga predictiva trivial.
   - Variables predictoras seleccionadas ($X$): `['LATITUD', 'LONGITUD', 'PROFUNDIDAD', 'HORA']`.
4. **Partición de Datos:**
   - División estratificada 80/20 con `train_test_split(..., test_size=0.2, random_state=42, stratify=y)`.
   - Tamaño de `X_train`: $19,431$ eventos.
   - Tamaño de `X_test`: $4,858$ eventos.
5. **Arquitectura de Preprocesamiento:**
   - Implementación de `ColumnTransformer` con `StandardScaler` sobre las variables cuantitativas dentro de pipelines desacoplados de Scikit-Learn, garantizando que medias y varianzas se calculen exclusivamente sobre el fold de entrenamiento.
6. **Modelos Entrenados y Comparados (Batería Cuaderno 11):**
   - **Regresión Logística:** `LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)`
   - **KNN:** `KNeighborsClassifier(n_neighbors=7)`
   - **Árbol de Decisión:** `DecisionTreeClassifier(max_depth=6, class_weight='balanced', random_state=42)`
   - **Random Forest:** `RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', random_state=42, n_jobs=-1)`
7. **Evaluación Integral y Validación Cruzada:**
   - Función `evaluar_modelo()` con reporte tabular comparativo de los 4 algoritmos.
   - Gráfico de barras comparativo de métricas (`Accuracy`, `Precision`, `Recall`, `F1-Score`, `ROC-AUC`).
   - 4 Matrices de confusión en subplot 2x2 con `ConfusionMatrixDisplay`.
   - **Validación Cruzada Estratificada de 5 pliegues (5-Fold Stratified CV)** con cálculo de medias y barras de error de desviación estándar.
   - Gráfico comparativo conjunto con las **4 Curvas ROC y valores AUC**.
8. **Optimización con GridSearchCV del Modelo Líder (Cuaderno 10):**
   - Búsqueda en grilla sobre Random Forest (`n_estimators: [50, 100]`, `max_depth: [8, 12]`, `min_samples_split: [2, 5]`) optimizando `scoring='roc_auc'` mediante 5-Fold CV.
   - Mejores hiperparámetros: `max_depth=12, min_samples_split=2, n_estimators=100` con ROC-AUC en CV de $0.600$.
9. **Importancia de Variables / Feature Importances (Cuaderno 08):**
   - Extracción de pesos de contribución:
     - `LATITUD`: **$31.24\%$**
     - `LONGITUD`: **$30.33\%$**
     - `PROFUNDIDAD`: **$25.24\%$**
     - `HORA`: **$13.19\%$**
   - Confirmación geofísica: más del **$86\%$** del poder predictivo reside en la ubicación tridimensional del hipocentro en la zona de subducción.
10. **Selección Justificada y Serialización:**
    - Selección de **Random Forest Optimizado** como el mejor clasificador global ($\text{ROC-AUC} \sim 0.603$ en test y $0.601$ en 5-Fold CV).
    - Serialización del pipeline completo mediante `joblib.dump` en:
      `SISMOS/models/pipeline_sismos_final.joblib` (**8.8 MB**).
11. **Simulación de Inferencia en Tiempo Real:**
    - Carga del modelo persistido con `joblib.load`.
    - Evaluación probabilística sobre 3 escenarios hipotéticos reales:
      - **Costa Central (Frente a Lima/Callao, somero, $25\text{ km}$):** Predicción de probabilidad evaluada.
      - **Sur del Perú (Arequipa/Moquegua, intermedio, $85\text{ km}$):** Evaluación de nivel de riesgo.
      - **Selva / Amazonía (Frontera Este, muy profundo, $580\text{ km}$):** Predicción de atenuación superficial.

---

## 4. Tabla Comparativa de Rendimiento (Los 4 Modelos de Cuaderno 11)

| Modelo Evaluado | Accuracy | Precision (Severo) | Recall (Severo) | F1-Score (Severo) | ROC-AUC (Test) | ROC-AUC (5-Fold CV) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Regresión Logística** | 0.546 | 0.227 | 0.484 | 0.309 | 0.531 | $0.546 \pm 0.010$ |
| **KNN (k=7)** | **0.768** | 0.289 | 0.070 | 0.112 | 0.560 | $0.559 \pm 0.009$ |
| **Árbol de Decisión** | 0.509 | 0.229 | **0.563** | 0.326 | 0.541 | $0.566 \pm 0.012$ |
| **Random Forest (Ganador)** | 0.676 | **0.300** | 0.405 | **0.344** | **0.603** | **$0.601 \pm 0.015$** |

---

## 5. Archivo Formal de Auditoría de Fuentes (`Auditoria_Fuentes_IGP.xlsx`)

Tomando como referencia el entregable `Pipeline-riesgo-bancario/Auditoria_Fuentes_ProyectoIA.xlsx` y los metadatos oficiales del IGP (`DiccionarioDatos.xlsx` y `Metadatos_0.docx`), se diseñó y generó mediante `openpyxl` el archivo formal de auditoría en:
[`SISMOS/Auditoria_Fuentes_IGP.xlsx`](../Auditoria_Fuentes_IGP.xlsx)

El libro de cálculo cuenta con diseño ejecutivo profesional (paleta institucional azul marino, tipografía Calibri, alineación optimizada, bordes y badges de conformidad) estructurado en 3 hojas:

1. **`Ficha_Fuente`:**
   - Entidad emisora: Instituto Geofísico del Perú (IGP) - CENSIS.
   - Dataset: Catálogo Sísmico Instrumental 1960 - 2025 (ID de recurso: 9786, Datos Abiertos Perú).
   - Volumen: 24,289 eventos sísmicos analizados en 8 columnas originales.
   - Licencia: Open Data Commons Attribution License.
   - Dictamen: CONFORME (100% íntegro y apto para modelado).
2. **`Auditoria_Variables`:**
   - Matriz detallada de especificación para las 8 variables: `Variable`, `Tipo_Original`, `Descripcion_Oficial`, `Unidades`, `Porcentaje_Nulos` (0.00% en todas), `Porcentaje_Duplicados` (0.00%), `Rango_Valores` y `Transformacion_Aplicada` (justificando el aislamiento de `MAGNITUD` y la estandarización de variables hipocentrales).
3. **`Control_Calidad`:**
   - Batería de 8 controles de integridad física y geofísica (QC-01 al QC-08):
     - Latitud dentro de límites territoriales y fosa oceánica ($-19.98^\circ$ a $-0.05^\circ$): 100% cumplimiento.
     - Longitud en territorio peruano y mar de Grau ($-83.56^\circ$ a $-68.01^\circ$): 100% cumplimiento.
     - Profundidad estrictamente positiva física ($1.0$ a $699.0\text{ km}$): 100% cumplimiento.
     - Magnitudes dentro de límites instrumentales ($3.0$ a $8.4\text{ Mw}$): 100% cumplimiento.
     - Unicidad, completitud y consistencia temporal (1960 - 2025): 100% cumplimiento.

---

## 6. Publicación y Versionado en GitHub

Conforme a las instrucciones del usuario, se creó y publicó el repositorio oficial para el proyecto en la cuenta de GitHub `Pierorivera1`:

- **Repositorio Oficial:** [`https://github.com/Pierorivera1/SISMOS`](https://github.com/Pierorivera1/SISMOS)
- **Rama Principal:** `main`
- **Exclusiones en `.gitignore`:**
  - `PROYECTO DE INVESTIGACIÓN EN INTELIGENCIA ARTIFICIAL.pdf` (solicitado explícitamente) y `*.pdf`.
  - Entornos virtuales (`.venv/`, `venv/`), cachés compiladas de Python (`__pycache__/`, `*.pyc`), checkpoints de Jupyter (`.ipynb_checkpoints/`) y configuraciones de entorno (`.vscode/`).
- **Commits Registrados en GitHub:**
  - `ab5512f`: *feat: proyecto integral de machine learning para prediccion sismica IGP* (commit inicial de 17 archivos).
  - `680fb1e`: *docs: actualizar bitacora de kiara con enlace al repositorio oficial en GitHub*.
  - `fa60fd8`: *docs: corregir formato de SISMO_SEVERO y remover seccion de bitacoras en README* (corrección del error de renderizado en LaTeX `_ allowed only in math mode` y retiro de la sección interna de bitácoras del README público).
- **Push Remoto:** Ejecutado y verificado exitosamente mediante `gh repo create SISMOS --public --source=. --remote=origin --push`.
- **Estructura Académica Futura:** Se tomó conocimiento del archivo institucional `PROYECTO DE INVESTIGACIÓN EN INTELIGENCIA ARTIFICIAL.pdf` (24 secciones de metodología y rigor experimental) que regirá la documentación formal en la siguiente etapa.

---

## 7. Guía de Restauración de Contexto (Context Refresh Guide)

Si una nueva sesión o agente necesita retomar este componente del proyecto, seguir los siguientes pasos:

1. **Ubicación del Cuaderno Principal y Auditoría:**
   - Repositorio GitHub: [`https://github.com/Pierorivera1/SISMOS`](https://github.com/Pierorivera1/SISMOS)
   - Cuaderno Maestro: [`SISMOS/NOTEBOOKS/proyecto_integrador_sismos.ipynb`](../NOTEBOOKS/proyecto_integrador_sismos.ipynb).
   - Auditoría de Fuentes: [`SISMOS/Auditoria_Fuentes_IGP.xlsx`](../Auditoria_Fuentes_IGP.xlsx).
   - Asegurarse de que el kernel seleccionado en VS Code sea **Python 3 (ipykernel)**.
2. **Re-ejecutar el Cuaderno vía Terminal si es necesario:**
   ```bash
   cd /home/pierooo/Projects/ai_model/SISMOS/NOTEBOOKS
   python3 -m jupyter nbconvert --to notebook --execute proyecto_integrador_sismos.ipynb --inplace
   ```
3. **Probar el Modelo Guardado en Producción:**
   ```python
   import joblib, pandas as pd
   model = joblib.load('/home/pierooo/Projects/ai_model/SISMOS/models/pipeline_sismos_final.joblib')
   nuevo_evento = pd.DataFrame([{'LATITUD': -12.10, 'LONGITUD': -77.50, 'PROFUNDIDAD': 25.0, 'HORA': 14}])
   print("Predicción:", model.predict(nuevo_evento))
   print("Probabilidades:", model.predict_proba(nuevo_evento))
   ```
4. **Coordinación:**
   - La arquitectura y pipeline productivo residen en `SISMOS/src/data/igp_loader.py` y `SISMOS/src/models/predict.py` (desarrollados por Back).
   - La coordinación y bitácora general se consultan en [`sesion_learner.md`](sesion_learner.md) y [`sesion_back.md`](sesion_back.md).
