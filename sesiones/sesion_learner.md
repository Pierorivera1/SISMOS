# Bitácora de Sesión: Learner (ML Architect & Coordinator)

- **ID de Conversación:** `4724f47d-d763-4afe-b0cf-81db46b2dc43`
- **Panel Herdr:** `w1:p3` (Workspace: `w1`, Tab: `Questions` / `w1:t3`)
- **Rol Principal:** Arquitecto de Machine Learning, Coordinador del Equipo y Estratega Metodológico.

---

## 1. Contexto Inicial y Aprendizaje de los Cuadernos de Clase

El objetivo inicial consistió en absorber todo el conocimiento pedagógico contenido en la carpeta `cuadernos/` (15 notebooks del curso de IA) para garantizar que todo el desarrollo posterior respetara estrictamente las técnicas, bibliotecas y buenas prácticas enseñadas:

- **Cuadernos 01 y 02 (EDA y Visualización):** Exploración estructural (`shape`, `dtypes`, `describe`, `isna`) y visualización estadística con `matplotlib` y `seaborn` (histogramas, boxplots, mapas de calor).
- **Cuaderno 03 (Transformación de Datos y Feature Engineering):** Tratamiento de nulos, variables derivadas, escalado (`StandardScaler`, `MinMaxScaler`) y el principio cardinal de **evitar Data Leakage** (nunca ajustar escaladores antes de la división de datos).
- **Cuaderno 04 (División de Datos y Validación Cruzada):** Uso de `train_test_split(..., stratify=y, random_state=42)` y validación cruzada con `StratifiedKFold`.
- **Cuadernos 05 al 09 (Modelos Supervisados y No Supervisados):** Regresión Lineal, Regresión Logística, KNN, Árboles de Decisión, Random Forest y K-Means.
- **Cuadernos 10 y 11 (Pipelines y Comparación de Modelos):** Integración limpia mediante `ColumnTransformer` y `Pipeline`, optimización con `GridSearchCV`, reporte de clasificación, matrices de confusión y curvas ROC/AUC.
- **Cuaderno 12 (Persistencia de Modelos):** Serialización del `Pipeline` completo (preprocesamiento + modelo) con `joblib.dump` y `joblib.load` para inferencia con datos crudos.
- **Cuaderno 13 (Proyecto Integrador):** Plantilla maestra end-to-end que sirvió de guía directa para este proyecto.

---

## 2. Coordinación Multi-Agente y Orquestación con Herdr

Se identificó la infraestructura de terminales y agentes gestionada por **Herdr (v0.8.2)** y el bus de mensajería inter-sesión de **Antigravity**:
- **Learner (`w1:p3`):** Sesión actual (Coordinación y arquitectura ML).
- **Kiara (`w1:p8`):** Especialista en experimentación interactiva en notebooks y análisis exploratorio/modelado.
- **Back (`w1:p1`):** Ingeniero de backend, pipelines de datos y scripts de producción.

Se utilizó `send_message` acoplado con `herdr agent prompt` / `herdr pane run` para sincronizar las tres terminales sin requerir intervención manual del usuario para desbloquear colas de entrada.

---

## 3. Decisiones Metodológicas y Mejores Prácticas Adoptadas

1. **Replicación Estructural:** Se tomó como base `Pipeline-riesgo-bancario` para organizar la carpeta `SISMOS/` (`data/raw/IGP`, `data/processed/`, `NOTEBOOKS/`, `src/data/`, `src/models/`, `models/`, `sesiones/`).
2. **Cuaderno Único Integrador:** En lugar de crear múltiples cuadernos fragmentados, se siguió la mejor práctica de condensar el flujo científico en un único archivo de alto impacto: `NOTEBOOKS/proyecto_integrador_sismos.ipynb` (análogo al Cuaderno 13).
3. **Manejo del Desbalance Sísmico:** Se identificó que los sismos severos ($\ge 5.0$) representan solo el **21.01%** del catálogo. Por ello, la métrica crítica seleccionada fue el **Recall (Sensibilidad)** de la clase 1 y el **AUC-ROC**, priorizando evitar falsos negativos en alertas sísmicas.
4. **Separación de Responsabilidades:** El análisis visual y la justificación de selección residen en el notebook; la lógica reproducible y productiva reside en `src/data/igp_loader.py` y `src/models/predict.py`.

---

## 4. Validación de Resultados del Modelo

Se verificó la ejecución exitosa del pipeline completo:
- **Artefacto generado:** `SISMOS/models/pipeline_sismos_final.joblib` (7.9 MB), que encapsula el `ColumnTransformer` (estandarización de latitud, longitud, profundidad y hora) y el clasificador `RandomForestClassifier(class_weight='balanced')`.
- **Rendimiento:** ROC-AUC de ~0.60 superando a la Regresión Logística (~0.53) y capturando patrones no lineales de subducción en el Perú.
- **Prueba de Inferencia:** Se ejecutó con éxito `python3 SISMOS/src/models/predict.py`, confirmando la predicción en tiempo real con probabilidades estimadas para un sismo simulado en la costa central.

---

## 5. Instrucciones para Refrescar Contexto Futuro

Al retomar este proyecto en una nueva sesión o turnos futuros:
1. Leer `SISMOS/sesiones/README.md` para el mapa general del equipo.
2. Comprobar que los datos limpios estén en `SISMOS/data/processed/sismos_limpios.csv`.
3. Para reentrenar o extender el análisis: abrir `SISMOS/NOTEBOOKS/proyecto_integrador_sismos.ipynb` en VS Code (kernel `Python 3 (ipykernel)`).
4. Para realizar inferencias en producción: ejecutar `python3 SISMOS/src/models/predict.py`.


---

## 6. Actualización: Batería Multimodelo Completa (Cuadernos 08, 10 y 11)

Siguiendo de forma rigurosa el temario de la clase, se completó la comparación de los **4 modelos de clasificación** y la optimización:

### 1. Comparativa de Modelos en Test (Cuaderno 11)
- **Regresión Logística:** Accuracy 0.546 | Recall 0.484 | F1 0.309 | ROC-AUC 0.531
- **KNN (k=7):** Accuracy 0.768 | Recall 0.070 | F1 0.112 | ROC-AUC 0.560
- **Árbol de Decisión (profundidad 6):** Accuracy 0.509 | Recall 0.563 | F1 0.326 | ROC-AUC 0.541
- **Random Forest (100 estimadores):** Accuracy 0.676 | Recall 0.405 | F1 0.344 | ROC-AUC 0.603

### 2. Validación Cruzada Estratificada (5 Folds - ROC-AUC)
- Regresión Logística: 0.5464 ± 0.0103
- KNN: 0.5586 ± 0.0086
- Árbol de Decisión: 0.5655 ± 0.0124
- Random Forest: 0.6014 ± 0.0155 (Ganador en estabilidad y discriminación)

### 3. Optimización con GridSearchCV (Cuaderno 10)
- Parámetros óptimos: , , .
- ROC-AUC alcanzado en CV: ~0.6033.

### 4. Importancia de Variables Geofísicas (Cuaderno 08)
- **Latitud:** 31.24% (segmentación a lo largo de la fosa de subducción)
- **Longitud:** 30.33% (distancia costa afuera frente al continente)
- **Profundidad:** 25.24% (hipocentros someros interplaca vs profundos intraplaca)
- **Hora:** 13.19%
- **Conclusión Geofísica:** Más del 86% de la capacidad predictiva reside en la localización tridimensional del sismo.


---

## 6. Actualización: Batería Multimodelo Completa (Cuadernos 08, 10 y 11)

Siguiendo de forma rigurosa el temario de la clase, se completó la comparación de los **4 modelos de clasificación** y la optimización:

### 1. Comparativa de Modelos en Test (Cuaderno 11)
- **Regresión Logística:** Accuracy 0.546 | Recall 0.484 | F1 0.309 | ROC-AUC 0.531
- **KNN (k=7):** Accuracy 0.768 | Recall 0.070 | F1 0.112 | ROC-AUC 0.560
- **Árbol de Decisión (profundidad 6):** Accuracy 0.509 | Recall 0.563 | F1 0.326 | ROC-AUC 0.541
- **Random Forest (100 estimadores):** Accuracy 0.676 | Recall 0.405 | F1 0.344 | ROC-AUC 0.603

### 2. Validación Cruzada Estratificada (5 Folds - ROC-AUC)
- Regresión Logística: 0.5464 ± 0.0103
- KNN: 0.5586 ± 0.0086
- Árbol de Decisión: 0.5655 ± 0.0124
- Random Forest: 0.6014 ± 0.0155 (Ganador en estabilidad y discriminación)

### 3. Optimización con GridSearchCV (Cuaderno 10)
- Parámetros óptimos: `max_depth: 12`, `min_samples_split: 2`, `n_estimators: 100`.
- ROC-AUC alcanzado en CV: ~0.6033.

### 4. Importancia de Variables Geofísicas (Cuaderno 08)
- **Latitud:** 31.24% (segmentación a lo largo de la fosa de subducción)
- **Longitud:** 30.33% (distancia costa afuera frente al continente)
- **Profundidad:** 25.24% (hipocentros someros interplaca vs profundos intraplaca)
- **Hora:** 13.19%
- **Conclusión Geofísica:** Más del 86% de la capacidad predictiva reside en la localización tridimensional del sismo.
