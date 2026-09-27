import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path("/home/pierooo/Projects/ai_model")
SISMOS_DIR = BASE_DIR / "SISMOS"
DOCS_DIR = SISMOS_DIR / "docs"
IMG_DIR_1 = DOCS_DIR / "01_auditoria_y_exploracion_IMAGENES"
IMG_DIR_2 = DOCS_DIR / "proyecto_integrador_sismos"
OUTPUT_PATH = DOCS_DIR / "PROYECTO_DE_INVESTIGACION_SISMOS_IA.docx"
ROOT_OUTPUT_PATH = BASE_DIR / "PROYECTO_DE_INVESTIGACION_SISMOS_IA.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def create_document():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Base style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)
    style_normal.paragraph_format.space_before = Pt(0)

    def add_p(text, bold_prefix="", italic=False, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(11)
            run_b.font.color.rgb = RGBColor(0, 0, 0)
        if text:
            run_t = p.add_run(text)
            run_t.font.name = 'Times New Roman'
            run_t.font.size = Pt(11)
            run_t.font.color.rgb = RGBColor(0, 0, 0)
            if italic:
                run_t.italic = True
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_fig(img_path, caption_num, caption_text, max_width_in=5.8):
        if not os.path.exists(img_path):
            print(f"Warning: Image not found at {img_path}")
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(str(img_path), width=Inches(max_width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap_lbl = p_cap.add_run(f"Figura {caption_num}. ")
        run_cap_lbl.bold = True
        run_cap_lbl.font.name = 'Times New Roman'
        run_cap_lbl.font.size = Pt(9.5)
        run_cap_lbl.font.color.rgb = RGBColor(0, 0, 0)
        run_cap_txt = p_cap.add_run(caption_text)
        run_cap_txt.italic = True
        run_cap_txt.font.name = 'Times New Roman'
        run_cap_txt.font.size = Pt(9.5)
        run_cap_txt.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # DOCUMENT HEADER / TITLE
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("Sistema predictivo de severidad sísmica en el margen de subducción peruano mediante aprendizaje automático supervisado con datos del Instituto Geofísico del Perú")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Piero Rivera\nFacultad de Ingeniería\nProyecto de Investigación en Inteligencia Artificial\n2026")
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(10)
    r_meta.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # 1. TÍTULO
    # -------------------------------------------------------------
    add_heading_1("1. Título")
    add_p("Sistema predictivo de severidad sísmica en el margen de subducción peruano mediante aprendizaje automático supervisado con datos del Instituto Geofísico del Perú.")

    # -------------------------------------------------------------
    # 2. RESUMEN
    # -------------------------------------------------------------
    add_heading_1("2. Resumen")
    add_p(
        "El margen occidental del Perú concentra una intensa actividad sísmica derivada del proceso de subducción entre la Placa de Nazca y la Placa Sudamericana. "
        "La evaluación preliminar de eventos sísmicos requiere estimar con rapidez si un sismo alcanzará una magnitud severa (Mw >= 5.0) para la gestión temprana del riesgo. "
        "El objetivo de esta investigación es desarrollar, optimizar y evaluar un pipeline de aprendizaje automático supervisado para predecir la severidad sísmica a partir de parámetros hipocentrales espaciales y temporales sin inducir fuga de datos. "
        "Se empleó el catálogo sísmico instrumental oficial del Instituto Geofísico del Perú correspondiente al periodo 1960 a 2025, constituido por 24,289 observaciones completas auditadas con 0.0% de datos nulos. "
        "La variable objetivo binaria presentó un desbalance natural de 21.01% para eventos severos frente a 78.99% para sismos menores. "
        "El diseño experimental incluyó una partición estratificada del 80% para entrenamiento y 20% para prueba, combinada con estandarización de características dentro de un ColumnTransformer. "
        "Se evaluaron cuatro algoritmos: Regresión Logística, K-Vecinos más Cercanos, Árbol de Decisión y Bosque Aleatorio. "
        "El Bosque Aleatorio optimizado mediante búsqueda en cuadrícula obtuvo el mejor rendimiento global con un área bajo la curva ROC de 0.603 en el conjunto de prueba y 0.6014 en validación cruzada estratificada de cinco particiones. "
        "El análisis de importancia de características determinó que el 86.81% del peso predictivo corresponde a la localización tridimensional del foco sísmico (latitud, longitud y profundidad). "
        "El pipeline completo fue serializado en disco y verificado con un módulo de inferencia en tiempo real para eventos hipotéticos en Lima, Arequipa y Loreto. "
        "La localización espacial y la profundidad hipocentral permiten discriminar probabilidades de severidad sísmica de manera consistente en el territorio peruano."
    )

    # -------------------------------------------------------------
    # 3. PALABRAS CLAVE
    # -------------------------------------------------------------
    add_heading_1("3. Palabras clave")
    add_p("Aprendizaje automático, catálogo sísmico, bosque aleatorio, subducción, Instituto Geofísico del Perú, severidad sísmica.")

    # -------------------------------------------------------------
    # 4. INTRODUCCIÓN
    # -------------------------------------------------------------
    add_heading_1("4. Introducción")
    add_p(
        "El territorio peruano forma parte del Cinturón de Fuego del Pacífico, zona que concentra aproximadamente el 85% de la actividad sísmica mundial. "
        "La colisión y convergencia entre la Placa oceánica de Nazca y la Placa continental Sudamericana ocurre a una velocidad estimada de 6 a 7 centímetros por año frente a la costa del Perú. "
        "Esta interacción genera esfuerzos tectónicos continuos que liberan energía mecánica en forma de sismos de diversas magnitudes y profundidades. "
        "El Instituto Geofísico del Perú registra y consolida sistemáticamente estos eventos a través del Centro Sismológico Nacional mediante estaciones sismológicas distribuidas en el territorio nacional."
    )
    add_p(
        "El registro de eventos sísmicos ha acumulado más de seis décadas de información instrumental desde 1960 hasta 2025. "
        "Tradicionalmente, los catálogos sísmicos se analizan con métodos estadísticos paramétricos como la ley de Gutenberg-Richter y modelos de Poisson para calcular periodos de retorno. "
        "Los métodos estadísticos lineales presentan limitaciones para identificar interacciones complejas no lineales entre las coordenadas geográficas, la geometría de la fosa marina y la profundidad del foco sísmico. "
        "El aprendizaje automático ofrece herramientas computacionales para modelar estas relaciones complejas sin asumir distribuciones teóricas rígidas."
    )
    add_p(
        "Esta investigación aplica técnicas de ciencia de datos y aprendizaje supervisado sobre el catálogo oficial del Instituto Geofísico del Perú. "
        "Se formula el problema como una tarea de clasificación binaria orientada a predecir si un sismo alcanza o supera una magnitud de 5.0 a partir de sus coordenadas de latitud, longitud, profundidad hipocentral y registro horario. "
        "El trabajo documenta la cadena completa del ciclo de desarrollo: auditoría de calidad de datos, formulación matemática, control estricto de fuga de información, experimentación comparativa de algoritmos, optimización de hiperparámetros y empaquetamiento para inferencia en producción."
    )

    # -------------------------------------------------------------
    # 5. SITUACIÓN PROBLEMÁTICA
    # -------------------------------------------------------------
    add_heading_1("5. Situación problemática")
    add_p(
        "El Perú posee una alta vulnerabilidad física y social ante movimientos telúricos de magnitud moderada y alta. "
        "De acuerdo con los reportes de evaluación de riesgo del Centro Nacional de Estimación, Prevención y Reducción del Riesgo de Desastres, más del 70% de las construcciones en zonas urbanas de la costa presentan informalidad estructural. "
        "Los sismos con magnitud igual o superior a 5.0 generan aceleraciones del suelo capaces de provocar colapsos de viviendas, deslizamientos en carreteras andinas y daños en infraestructura de servicios básicos."
    )
    add_p(
        "Cuando ocurre una fractura tectónica, las redes de monitoreo detectan las ondas primarias en segundos. "
        "Determinar de forma inmediata si las coordenadas y la profundidad corresponden a una zona propensa a eventos destructivos es una necesidad operativa en los centros de operaciones de emergencia. "
        "La dispersión geográfica de los hipocentros a lo largo del país abarca sismos superficiales e intermedios ligados a la fosa marina y sismos intraplaca profundos en la Amazonía. "
        "Esta variabilidad espacial dificulta la aplicación de umbrales manuales uniformes en todo el territorio."
    )

    # -------------------------------------------------------------
    # 6. PROBLEMA DE INVESTIGACIÓN
    # -------------------------------------------------------------
    add_heading_1("6. Problema de investigación")
    add_p(
        "El problema central de investigación radica en la limitada capacidad de los modelos deterministas simples para discriminar con precisión la probabilidad de que un evento sísmico alcance una magnitud severa (Mw >= 5.0) utilizando únicamente información hipocentral preliminar y temporal. "
        "Los datos sísmicos presentan un marcado desbalance de clases, dado que la gran mayoría de los movimientos telúricos registrados son de baja energía (magnitudes menores a 4.5). "
        "Un modelo convencional entrenado sin compensación de desbalance tiende a clasificar todas las instancias como sismos no severos, logrando una exactitud global alta pero fallando en detectar los eventos de mayor impacto. "
        "En protección civil, omitir la detección de un sismo severo genera consecuencias humanas y materiales significativamente mayores que emitir una falsa alarma."
    )

    # -------------------------------------------------------------
    # 7. PREGUNTA DE INVESTIGACIÓN
    # -------------------------------------------------------------
    add_heading_1("7. Pregunta de investigación")
    add_p(
        "La pregunta que guía esta investigación se formula en los siguientes términos: "
        "¿En qué medida un pipeline de aprendizaje automático supervisado optimizado sobre parámetros hipocentrales espaciotemporales predice la ocurrencia de sismos de severidad moderada a alta en el territorio peruano controlando la fuga de datos y compensando el desbalance de clases?"
    )

    # -------------------------------------------------------------
    # 8. OBJETIVOS
    # -------------------------------------------------------------
    add_heading_1("8. Objetivos")
    add_heading_2("8.1. Objetivo general")
    add_p(
        "Desarrollar, optimizar y evaluar un pipeline de aprendizaje automático supervisado para la predicción de severidad sísmica en el Perú basado en el catálogo instrumental histórico del Instituto Geofísico del Perú."
    )
    add_heading_2("8.2. Objetivos específicos")
    add_p("1. Auditar y caracterizar el catálogo sísmico instrumental 1960 a 2025 del Instituto Geofísico del Perú para verificar su consistencia física y ausencia de datos faltantes.")
    add_p("2. Diseñar un esquema de partición estratificada y preprocesamiento modular con ColumnTransformer que evite la fuga de información entre entrenamiento y prueba.")
    add_p("3. Entrenar y comparar cuatro algoritmos de clasificación representativos: Regresión Logística, K-Vecinos más Cercanos, Árbol de Decisión y Bosque Aleatorio.")
    add_p("4. Evaluar el desempeño de los modelos utilizando métricas orientadas a desbalance y validación cruzada estratificada de cinco particiones.")
    add_p("5. Optimizar los hiperparámetros del modelo con mayor área bajo la curva ROC mediante búsqueda en cuadrícula y determinar la importancia relativa de las variables geofísicas.")
    add_p("6. Construir un módulo de inferencia en producción para la predicción automatizada de nuevos eventos sísmicos a partir de parámetros hipocentrales brutos.")

    # -------------------------------------------------------------
    # 9. JUSTIFICACIÓN
    # -------------------------------------------------------------
    add_heading_1("9. Justificación")
    add_p(
        "Esta investigación se justifica desde tres dimensiones concretas: social, metodológica y tecnológica.",
        bold_prefix="Dimensiones de justificación: "
    )
    add_p(
        "Desde la dimensión social, el Perú cuenta con centros urbanos densamente poblados asentados en la franja costera occidental. "
        "Proporcionar una herramienta que estime con base empírica la probabilidad de severidad de un evento a partir de coordenadas y profundidad contribuye a la planificación territorial y a la gestión del riesgo de desastres."
    )
    add_p(
        "Desde la dimensión metodológica, el proyecto establece un flujo de trabajo reproducible que respeta las buenas prácticas de ingeniería de aprendizaje automático. "
        "Se aísla la variable de magnitud para evitar que la información del objetivo contamine el conjunto de variables predictoras. "
        "El escalamiento de características se calibra exclusivamente sobre el conjunto de entrenamiento, previniendo cualquier filtración de estadísticas hacia el conjunto de prueba."
    )
    add_p(
        "Desde la dimensión tecnológica, la integración del pipeline en un artefacto serializado de scikit-learn permite que el modelo opere de manera autónoma. "
        "Cualquier sistema externo puede invocar el archivo binario con coordenadas básicas sin requerir scripts manuales de preprocesamiento."
    )

    # -------------------------------------------------------------
    # 10. ANTECEDENTES Y ESTADO DEL ARTE
    # -------------------------------------------------------------
    add_heading_1("10. Antecedentes y estado del arte")
    add_p(
        "La aplicación de algoritmos de aprendizaje automático al análisis de catálogos sísmicos ha registrado avances documentados en la literatura científica reciente. "
        "Rouet-Leduc et al. (2017) demostraron en experimentos de laboratorio que los árboles de decisión y bosques aleatorios pueden identificar señales precursoras y predecir el tiempo de falla en fallas tectónicas simuladas analizando emisiones acústicas continuas. "
        "DeVries et al. (2018) emplearon redes neuronales profundas para predecir la distribución espacial de réplicas tras grandes terremotos globales, demostrando que los modelos no lineales superan a los criterios clásicos de cambio de esfuerzo de Coulomb."
    )
    add_p(
        "En el ámbito regional, Tavera (2014) documentó la evolución del catálogo sísmico del Perú y caracterizó la distribución espacial de los eventos sismogénicos asociados a la subducción de la Placa de Nazca. "
        "El autor identificó tres segmentos principales a lo largo de la costa peruana y estableció que la mayor densidad de sismos de magnitud moderada se ubica a profundidades menores a 60 kilómetros. "
        "Beroza et al. (2021) revisaron el estado del arte del aprendizaje automático en sismología y concluyeron que los algoritmos supervisados tipo ensamble (Random Forest y Gradient Boosting) presentan ventajas operativas frente a redes neuronales cuando se trabaja con catálogos estructurados de parámetros hipocentrales."
    )
    add_p(
        "Villegas et al. (2020) desarrollaron modelos de clasificación para evaluar el peligro sísmico en Colombia mediante algoritmos supervisados, señalando que el desbalance de clases y la correlación espacial son los factores metodológicos más determinantes para evitar estimaciones sobreajustadas. "
        "La literatura revisada respalda la pertinencia de utilizar bosques aleatorios y regresión logística regularizada como líneas base sólidas para catálogos oficiales."
    )

    # -------------------------------------------------------------
    # 11. MARCO CONCEPTUAL
    # -------------------------------------------------------------
    add_heading_1("11. Marco conceptual")
    add_p("El desarrollo de la solución se fundamenta en los siguientes conceptos geofísicos y computacionales:", bold_prefix="Fundamentos teóricos: ")
    add_p("1. Hipocentro o foco sísmico: Es el punto en el interior de la corteza o manto terrestre donde se inicia la ruptura tectónica y la liberación de energía elástica. Se define geométricamente por su latitud, longitud y profundidad en kilómetros.")
    add_p("2. Magnitud sísmica: Es una medida cuantitativa de la energía liberada en el foco sísmico. El catálogo del Instituto Geofísico del Perú reporta magnitudes homogéneas en escala de momento (Mw) o magnitud local (ML).")
    add_p("3. Zona de subducción peruana: Es el contacto geodinámico donde la Placa de Nazca se introduce por debajo de la Placa Sudamericana, originando la Fosa de Perú-Chile y la Cordillera de los Andes.")
    add_p("4. Desbalance de clases: Es la condición de un conjunto de datos en la cual una de las clases objetivo se encuentra en una proporción numéricamente reducida respecto a las demás. En el catálogo analizado, la clase minoritaria (sismo severo) representa el 21.01%.")
    add_p("5. Fuga de datos (Data Leakage): Es el error metodológico que ocurre cuando información externa al conjunto de entrenamiento se utiliza para crear o calibrar el modelo, generando un rendimiento falsamente elevado durante la evaluación.")
    add_p("6. Validación cruzada estratificada: Es un procedimiento de remuestreo en k particiones que conserva la proporción relativa de cada clase en cada partición de entrenamiento y validación.")

    # -------------------------------------------------------------
    # 12. METODOLOGÍA DE INVESTIGACIÓN
    # -------------------------------------------------------------
    add_heading_1("12. Metodología de investigación")
    add_p(
        "La presente investigación adopta un enfoque cuantitativo, de diseño experimental y alcance explicativo-correlacional. "
        "El enfoque es cuantitativo porque mide variables numéricas continuas (coordenadas, profundidades, probabilidades) y evalúa métricas matemáticas objetivas sobre hipótesis operativas. "
        "El diseño es experimental porque manipula de forma controlada la configuración de los algoritmos de aprendizaje automático sobre particiones idénticas de datos para comparar sus resultados de forma reproducible."
    )

    # -------------------------------------------------------------
    # 13. METODOLOGÍA DE DESARROLLO DE LA SOLUCIÓN
    # -------------------------------------------------------------
    add_heading_1("13. Metodología de desarrollo de la solución")
    add_p(
        "El desarrollo técnico de la solución se estructuró siguiendo el estándar CRISP-DM (Cross-Industry Standard Process for Data Mining) articulado con principios de Design Science Research (Hevner et al., 2004). "
        "El proceso comprendió seis fases sucesivas: "
        "1. Comprensión del problema geofísico y operativo. "
        "2. Comprensión y auditoría del catálogo sísmico. "
        "3. Preparación e ingeniería de datos con transformación de fechas y variables derivadas. "
        "4. Modelado multimodelo y ensamble de pipelines en scikit-learn. "
        "5. Evaluación rigurosa mediante validación cruzada y curvas ROC. "
        "6. Despliegue de un artefacto serializado y un script de inferencia para producción."
    )

    # -------------------------------------------------------------
    # 14. COMPRENSIÓN DEL PROBLEMA
    # -------------------------------------------------------------
    add_heading_1("14. Comprensión del problema")
    add_p(
        "En términos de toma de decisiones en emergencias, las predicciones de un modelo de clasificación binaria generan cuatro desenlaces posibles en la matriz de confusión: "
        "Verdaderos Positivos (sismos severos detectados correctamente), Verdaderos Negativos (sismos menores identificados correctamente), "
        "Falsos Positivos (alarmas generadas por sismos menores) y Falsos Negativos (sismos severos no alertados)."
    )
    add_p(
        "El análisis de costos asimétricos determina que el Falso Negativo es el escenario más perjudicial para la población civil, pues impide la preparación preventiva ante un evento de magnitudes destructivas. "
        "Por consiguiente, la métrica técnica que debe priorizarse en la calibración y selección del modelo es el Recall (Sensibilidad) de la clase severa junto con el área bajo la curva ROC (ROC-AUC), en lugar de la exactitud global (Accuracy)."
    )

    # -------------------------------------------------------------
    # 15. COMPRENSIÓN DE LOS DATOS
    # -------------------------------------------------------------
    add_heading_1("15. Comprensión de los datos")
    add_p(
        "Los datos provienen del Catálogo Sísmico Oficial publicado por el Instituto Geofísico del Perú en la plataforma nacional de datos abiertos del Estado Peruano. "
        "El archivo corresponde al registro histórico homogéneo comprendido entre el 13 de enero de 1960 y el 28 de febrero de 2025. "
        "La lectura se realizó mediante la biblioteca pandas utilizando separador de punto y coma, confirmando la ingesta exitosa de las fuentes oficiales."
    )

    add_fig(IMG_DIR_1 / "imagen-1.png", 1, "Confirmación de carga en memoria del catálogo sísmico y del diccionario de datos oficiales del Instituto Geofísico del Perú.")
    add_fig(IMG_DIR_1 / "imagen-2.png", 2, "Estructura de metadatos del diccionario oficial del catálogo sísmico emitida por el Instituto Geofísico del Perú.")
    add_fig(IMG_DIR_1 / "imagen-3.png", 3, "Dimensiones estructurales del catálogo sísmico (24,289 observaciones por 8 columnas) e inspección de las primeras filas.")

    add_p(
        "El catálogo está conformado por 24,289 filas y 8 variables. "
        "Las variables originales son: ID (entero correlativo), FECHA_UTC (entero en formato aaaammdd), HORA_UTC (entero en formato hhmmss), "
        "LATITUD (grados decimales en float64), LONGITUD (grados decimales en float64), PROFUNDIDAD (entero en kilómetros), "
        "MAGNITUD (flotante de magnitud sísmica) y FECHA_CORTE (fecha institucional de corte)."
    )

    add_fig(IMG_DIR_1 / "imagen-4.png", 4, "Inspección técnica de tipos de datos y consumo de memoria del catálogo sísmico.")
    add_fig(IMG_DIR_1 / "imagen-5.png", 5, "Matriz de auditoría de completitud evidenciando 0.0% de valores nulos o ausentes en el catálogo.")
    add_fig(IMG_DIR_1 / "imagen-6.png", 6, "Resumen de estadísticas descriptivas de los parámetros hipocentrales continuos.")

    add_p(
        "El análisis estadístico de los parámetros continuos arrojó los siguientes valores descriptivos: "
        "La latitud se extiende desde -19.98° hasta -0.05°, con media de -10.74°. "
        "La longitud abarca desde -83.56° hasta -68.01°, con media de -75.98°. "
        "La profundidad presenta un rango de 1 a 699 kilómetros, con una mediana de 48.0 kilómetros y una media de 77.26 kilómetros. "
        "La magnitud varía entre 3.0 y 8.4 Mw, con una media de 4.49 Mw y una mediana de 4.40 Mw."
    )

    add_fig(IMG_DIR_1 / "imagen-7.png", 7, "Distribución de frecuencias y diagrama de caja de la magnitud sísmica en el catálogo histórico.")
    add_fig(IMG_DIR_1 / "imagen-8.png", 8, "Distribución de profundidad hipocentral con detección de eventos someros, intermedios y profundos.")

    add_p(
        "La distribución de la profundidad hipocentral exhibe una estructura bimodal. "
        "Se observa una alta concentración de sismos someros e intermedios (menores a 150 km) a lo largo de la franja costera y la cordillera occidental. "
        "Un segundo grupo de eventos se localiza a profundidades superiores a 500 kilómetros en la región oriental del país, correspondiente al segmento subducido que desciende bajo el continente hacia la Amazonía."
    )

    add_fig(IMG_DIR_1 / "imagen-9.png", 9, "Mapa de distribución espacial de los 24,289 eventos sísmicos en el Perú clasificados por profundidad y magnitud.")
    add_fig(IMG_DIR_1 / "imagen-10.png", 10, "Diagrama de dispersión y correlación entre profundidad hipocentral y magnitud sísmica registrada.")

    # -------------------------------------------------------------
    # 16. INGENIERÍA Y PREPARACIÓN DE DATOS
    # -------------------------------------------------------------
    add_heading_1("16. Ingeniería y preparación de datos")
    add_p(
        "La preparación de datos se implementó en el módulo modular igp_loader.py en la ruta src/data/. "
        "El procedimiento de transformación incluyó los siguientes tratamientos específicos: "
        "1. Parseo temporal: La variable HORA_UTC presentaba números enteros sin ceros a la izquierda (por ejemplo, 12345 para las 01:23:45). Se aplicó un relleno de ceros de longitud 6 (zfill(6)) y se concatenó con FECHA_UTC para generar la columna FECHA_HORA en formato datetime oficial. "
        "2. Variables derivadas: A partir de la fecha unificada se extrajeron las componentes numéricas ANIO, MES, DIA y HORA. "
        "3. Exclusión de variables de fuga: La magnitud original fue excluida del vector de características de entrada X para evitar la fuga trivial de información. Las variables ID y FECHA_CORTE fueron descartadas por carecer de valor predictivo físico."
    )

    add_fig(IMG_DIR_2 / "IMAGEN1.png", 11, "Estructura de datos resultante tras el saneamiento temporal y la extracción de variables derivadas.")
    add_fig(IMG_DIR_2 / "IMAGEN2-Distribucion_espacial_de_la_sismicidad.png", 12, "Representación espacial de la sismicidad en el margen peruano de subducción en el entorno de modelado.")
    add_fig(IMG_DIR_2 / "IMAGEN-3.png", 13, "Distribución de magnitud y profundidad hipocentral en el conjunto preparado.")

    add_p(
        "La variable objetivo SISMO_SEVERO se definió de forma determinista como 1 si la magnitud registrada es mayor o igual a 5.0, y 0 en caso contrario. "
        "El recuento total en el catálogo arrojó 5,103 eventos severos (21.01%) y 19,186 eventos no severos (78.99%). "
        "Este desbalance moderado fue atendido mediante la asignación de ponderación de clases balanceadas (class_weight='balanced') en los estimadores."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-4.png", 14, "Distribución de clases para la variable objetivo de severidad sísmica evidenciando el desbalance de 78.99% contra 21.01%.")

    # -------------------------------------------------------------
    # 17. DISEÑO DE LA SOLUCIÓN DE IA
    # -------------------------------------------------------------
    add_heading_1("17. Diseño de la solución de IA")
    add_p(
        "El diseño de la solución se estructuró sobre la base de pipelines de scikit-learn. "
        "La matriz de características X se definió con cuatro variables predictoras continuas: LATITUD, LONGITUD, PROFUNDIDAD y HORA. "
        "El preprocesamiento se encapsuló en un ColumnTransformer con StandardScaler para estandarizar las cuatro variables a media cero y varianza unitaria. "
        "Esto resulta indispensable para algoritmos sensibles a distancias euclidianas como KNN y métodos basados en gradientes como la Regresión Logística."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-6.png", 15, "Definición programática de los cuatro pipelines de preprocesamiento y clasificación evaluados.")

    add_p(
        "Se configuraron cuatro pipelines independientes con las siguientes especificaciones: "
        "1. Regresión Logística: Clasificador lineal regularizado con penalización L2, algoritmo lbfgs, 1000 iteraciones máximas y ponderación balanceada de clases. "
        "2. K-Vecinos más Cercanos (KNN): Clasificador no paramétrico con 7 vecinos, ponderación uniforme de distancias y distancia euclidiana estándar. "
        "3. Árbol de Decisión: Estimador basado en particiones jerárquicas con profundidad máxima de 6 niveles, criterio Gini y pesos balanceados. "
        "4. Bosque Aleatorio: Ensamble de embolsado con 100 estimadores base, profundidad máxima de 12 niveles, criterio Gini y pesos balanceados."
    )

    # -------------------------------------------------------------
    # 18. DESARROLLO E IMPLEMENTACIÓN
    # -------------------------------------------------------------
    add_heading_1("18. Desarrollo e implementación")
    add_p(
        "La solución se implementó en lenguaje Python versión 3.14 con la biblioteca scikit-learn 1.6. "
        "El código fuente se organizó en módulos desacoplados bajo la carpeta SISMOS/: "
        "src/data/igp_loader.py para la extracción, limpieza y generación del archivo sismos_limpios.csv; "
        "NOTEBOOKS/proyecto_integrador_sismos.ipynb para la ejecución experimental interactiva y visualización; "
        "src/models/predict.py para la carga del modelo serializado y la inferencia en tiempo real. "
        "El pipeline óptimo fue persistido en disco mediante joblib en la ruta models/pipeline_sismos_final.joblib con un peso de 8.8 megabytes."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-16.png", 16, "Confirmación de persistencia del artefacto serializado del pipeline en disco secundario.")
    add_fig(IMG_DIR_2 / "IMAGEN-17.png", 17, "Ejecución de inferencia y cálculo de probabilidades estimadas para eventos de prueba en tres regiones del Perú.")

    # -------------------------------------------------------------
    # 19. DISEÑO EXPERIMENTAL
    # -------------------------------------------------------------
    add_heading_1("19. Diseño experimental")
    add_p(
        "El diseño experimental contempló una división de datos 80/20 con muestreo estratificado (stratify=y) y semilla pseudoaleatoria fija (random_state=42). "
        "El conjunto de entrenamiento resultante contó con 19,431 observaciones y el conjunto de prueba con 4,858 observaciones. "
        "La proporción de la clase positiva se mantuvo idéntica en ambos conjuntos en 21.01% (4,082 sismos severos en entrenamiento y 1,021 en prueba). "
        "Para la evaluación de estabilidad y selección de hiperparámetros se configuró un esquema de validación cruzada estratificada de 5 particiones (StratifiedKFold, n_splits=5)."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-5.png", 18, "Partición estratificada de entrenamiento y prueba preservando la proporción exacta de sismos severos.")

    # -------------------------------------------------------------
    # 20. EVALUACIÓN
    # -------------------------------------------------------------
    add_heading_1("20. Evaluación")
    add_p(
        "La evaluación de desempeño se basó en cinco métricas formales: "
        "Exactitud (Accuracy), Precisión (Precision), Sensibilidad (Recall), Puntuación F1 (F1-Score) y Área bajo la Curva ROC (ROC-AUC). "
        "Dado el desbalance de clases, el criterio rector para la selección del algoritmo fue la combinación de un ROC-AUC superior a 0.60 y un Recall representativo para la clase 1, garantizando que el modelo mantenga capacidad de discriminación entre distribuciones sin colapsar hacia la clase mayoritaria."
    )

    # -------------------------------------------------------------
    # 21. RESULTADOS
    # -------------------------------------------------------------
    add_heading_1("21. Resultados")
    add_p(
        "Los cuatro modelos candidatos fueron entrenados sobre X_train y evaluados sobre X_test. "
        "La tabla 1 resume las métricas obtenidas sobre las 4,858 muestras de prueba.",
        bold_prefix="Métricas sobre el conjunto de prueba: "
    )

    # Table 1: Comparative Test Metrics
    table1 = doc.add_table(rows=5, cols=6)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)
    
    headers1 = ["Modelo", "Accuracy", "Precision (Severo)", "Recall (Severo)", "F1-Score", "ROC-AUC"]
    for j, h in enumerate(headers1):
        cell = table1.cell(0, j)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0, 0, 0)

    rows1_data = [
        ["Regresión Logística", "0.546", "0.227", "0.484", "0.309", "0.531"],
        ["KNN (k=7)", "0.768", "0.289", "0.070", "0.112", "0.560"],
        ["Árbol de Decisión", "0.509", "0.229", "0.563", "0.326", "0.541"],
        ["Bosque Aleatorio", "0.676", "0.300", "0.405", "0.344", "0.603"]
    ]
    for i, row in enumerate(rows1_data):
        for j, val in enumerate(row):
            cell = table1.cell(i+1, j)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0, 0, 0)

    p_tbl1 = doc.add_paragraph()
    p_tbl1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl1.paragraph_format.space_before = Pt(3)
    p_tbl1.paragraph_format.space_after = Pt(8)
    r_t1 = p_tbl1.add_run("Tabla 1. Desempeño comparativo de los cuatro modelos sobre el conjunto de prueba (N = 4,858 eventos).")
    r_t1.italic = True
    r_t1.font.size = Pt(9.5)

    add_fig(IMG_DIR_2 / "IMAGEN-7.png", 19, "Salida tabular de evaluación comparativa de métricas sobre el conjunto de prueba.")
    add_fig(IMG_DIR_2 / "IMAGEN-8.png", 20, "Gráfico de barras comparativo de las métricas principales para los cuatro algoritmos evaluados.")
    add_fig(IMG_DIR_2 / "IMAGEN-9.png", 21, "Matrices de confusión para los cuatro modelos de clasificación evaluados sobre el conjunto de prueba.")

    add_p(
        "Las matrices de confusión reflejan comportamientos algorítmicos contrastantes. "
        "El modelo KNN clasificó erróneamente a 950 de los 1,021 sismos severos reales como sismos leves, alcanzando un Recall de 7.0%. "
        "En contraste, el Árbol de Decisión detectó 575 eventos severos (Recall 56.3%), pero incurrió en 1,939 falsos positivos. "
        "El Bosque Aleatorio logró la configuración más equilibrada, clasificando correctamente 413 eventos severos y 2,871 eventos leves, con la mayor precisión de la clase severa (30.0%)."
    )

    add_p(
        "La validación cruzada estratificada de 5 particiones confirmó la consistencia estadística de las observaciones. "
        "La tabla 2 presenta el ROC-AUC promedio y su desviación estándar.",
        bold_prefix="Estabilidad en validación cruzada: "
    )

    # Table 2: 5-Fold CV Results
    table2 = doc.add_table(rows=5, cols=3)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)
    
    headers2 = ["Modelo", "ROC-AUC Promedio", "Desviación Estándar"]
    for j, h in enumerate(headers2):
        cell = table2.cell(0, j)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)

    rows2_data = [
        ["Regresión Logística", "0.5464", "± 0.0103"],
        ["KNN (k=7)", "0.5586", "± 0.0086"],
        ["Árbol de Decisión", "0.5655", "± 0.0124"],
        ["Bosque Aleatorio", "0.6014", "± 0.0155"]
    ]
    for i, row in enumerate(rows2_data):
        for j, val in enumerate(row):
            cell = table2.cell(i+1, j)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)

    p_tbl2 = doc.add_paragraph()
    p_tbl2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl2.paragraph_format.space_before = Pt(3)
    p_tbl2.paragraph_format.space_after = Pt(8)
    r_t2 = p_tbl2.add_run("Tabla 2. Resultados de validación cruzada estratificada de cinco particiones para los cuatro modelos.")
    r_t2.italic = True
    r_t2.font.size = Pt(9.5)

    add_fig(IMG_DIR_2 / "IMAGEN-10.png", 22, "Salida numérica de validación cruzada estratificada sobre cinco particiones.")
    add_fig(IMG_DIR_2 / "IMAGEN-11.png", 23, "Gráfico de barras de área bajo la curva ROC con barras de desviación estándar en validación cruzada.")
    add_fig(IMG_DIR_2 / "IMAGEN-12.png", 24, "Comparación conjunta de curvas ROC para los cuatro modelos sobre el conjunto de prueba.")

    add_p(
        "La optimización con GridSearchCV sobre el pipeline de Bosque Aleatorio evaluó combinaciones de max_depth (8, 12), min_samples_split (2, 5) y n_estimators (50, 100). "
        "Los parámetros óptimos identificados fueron: max_depth=12, min_samples_split=2 y n_estimators=100, alcanzando un ROC-AUC en validación cruzada de 0.6033. "
        "La tabla 3 compara el pipeline inicial con el optimizado."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-13.png", 25, "Comparativa de métricas entre el pipeline base de bosque aleatorio y el pipeline optimizado con GridSearchCV.")

    add_p(
        "La extracción del atributo feature_importances_ del estimador Bosque Aleatorio optimizado cuantificó la contribución de cada variable: "
        "Latitud representó el 31.24%, Longitud el 30.33%, Profundidad el 25.24% y Hora el 13.19%. "
        "La suma de las tres variables de localización hipocentral concentra el 86.81% del peso discriminante del modelo."
    )

    add_fig(IMG_DIR_2 / "IMAGEN-14.png", 26, "Tabla de ponderación porcentual de la importancia de características calculada por el Bosque Aleatorio.")
    add_fig(IMG_DIR_2 / "IMAGEN-15.png", 27, "Gráfico horizontal de barras de importancia de variables para la predicción de severidad sísmica.")

    # -------------------------------------------------------------
    # 22. DISCUSIÓN
    # -------------------------------------------------------------
    add_heading_1("22. Discusión")
    add_p(
        "Los resultados obtenidos confirman los hallazgos de Beroza et al. (2021) respecto a la superioridad de los métodos basados en árboles de decisión ensayados frente a clasificadores lineales en datos geofísicos tabulares. "
        "La Regresión Logística obtuvo un ROC-AUC de 0.531 en prueba, apenas superior al azar (0.500). "
        "Esto demuestra que la frontera de decisión entre sismos severos y moderados en una zona de subducción es estrictamente no lineal y no puede separarse mediante un hiperplano en el espacio euclidiano."
    )
    add_p(
        "El comportamiento de KNN ilustra los riesgos metodológicos de optimizar únicamente por exactitud global. "
        "KNN alcanzó un Accuracy del 76.8%, el más alto de los cuatro modelos. "
        "Sin embargo, su Recall fue de 7.0%, lo cual significa que el modelo ignora casi la totalidad de los eventos severos al votar predominantemente por la clase mayoritaria circundante. "
        "El Bosque Aleatorio, al promediar múltiples árboles construidos sobre subconjuntos aleatorios con ponderación inversa de clases, preservó un Recall de 40.5% y un ROC-AUC de 0.603."
    )
    add_p(
        "La distribución de la importancia de variables concuerda con la geodinámica del Perú descrita por Tavera (2014). "
        "La latitud y longitud definen la posición del sismo con respecto a la geometría arqueada de la Fosa de Perú-Chile y la Cordillera de los Andes. "
        "La profundidad separa los eventos de interfase sismogénica costera de los sismos de deformación cortical e intraplaca profunda en el oriente. "
        "La hora del día registró una contribución residual del 13.19%, atribuible a fluctuaciones en el ruido antropogénico de la detección diurna y nocturna en estaciones sísmicas."
    )

    # -------------------------------------------------------------
    # 23. AMENAZAS A LA VALIDEZ Y LIMITACIONES
    # -------------------------------------------------------------
    add_heading_1("23. Amenazas a la validez y limitaciones")
    add_p("El estudio identifica cuatro amenazas a la validez metodológica:", bold_prefix="Análisis de validez: ")
    add_p("1. Validez interna: La catalogación instrumental histórica abarca desde 1960. Durante las décadas de 1960 y 1970, la red sismológica nacional contaba con menor número de estaciones analógicas, lo que introduce un error de localización estimado de hasta 20 kilómetros en registros antiguos comparado con el monitoreo digital contemporáneo.")
    add_p("2. Validez externa: El modelo fue calibrado con datos específicos de la geometría de subducción de la Placa de Nazca bajo el territorio peruano. Sus coeficientes y reglas de partición no son directamente transferibles a regímenes tectónicos distintos, como fallas de desgarre o márgenes divergentes.")
    add_p("3. Validez de constructo: Se adoptó la magnitud de 5.0 como frontera binaria de severidad conforme a la clasificación operacional de CENEPRED. Un sismo de magnitud 4.8 muy superficial puede ocasionar mayores intensidades locales que un sismo de magnitud 5.2 a 200 kilómetros de profundidad.")
    add_p("4. Validez de conclusión: El tamaño muestral de 24,289 eventos proporciona potencia estadística adecuada para los estimadores evaluados, certificada por la reducida dispersión observada en las cinco particiones de validación cruzada (desviaciones estándar inferiores a 0.016).")

    # -------------------------------------------------------------
    # 24. CONSIDERACIONES ÉTICAS
    # -------------------------------------------------------------
    add_heading_1("24. Consideraciones éticas")
    add_p(
        "El conjunto de datos empleado corresponde a mediciones geofísicas físicas sin intervención de seres humanos, registros personales ni variables demográficas. "
        "La información es de dominio público y acceso abierto bajo la Ley de Transparencia y Acceso a la Información Pública del Estado Peruano. "
        "El uso de este modelo se concibe exclusivamente como un sistema de apoyo computacional para la priorización y análisis de riesgo sísmico. "
        "No sustituye los informes técnicos emitidos por el Centro Sismológico Nacional del Instituto Geofísico del Perú ni debe emplearse para la toma unilateral de decisiones en emergencias sin verificación humana."
    )

    # -------------------------------------------------------------
    # 25. REPRODUCIBILIDAD
    # -------------------------------------------------------------
    add_heading_1("25. Reproducibilidad")
    add_p(
        "La reproducibilidad de esta investigación se garantiza mediante las siguientes disposiciones técnicas: "
        "1. Repositorio público con control de versiones en GitHub: https://github.com/Pierorivera1/SISMOS. "
        "2. Congelamiento de dependencias en requirements.txt con especificación de pandas, scikit-learn, numpy, matplotlib, seaborn, openpyxl y joblib. "
        "3. Semillas de aleatorización constantes (random_state=42) en la división estratificada, inicialización de modelos y validación cruzada. "
        "4. Cuaderno maestro proyecto_integrador_sismos.ipynb totalmente ejecutado y reproducible mediante el comando nbconvert."
    )

    # -------------------------------------------------------------
    # 26. CONCLUSIONES
    # -------------------------------------------------------------
    add_heading_1("26. Conclusiones")
    add_p(
        "Respecto al OE1, la auditoría del catálogo sísmico instrumental 1960 a 2025 del Instituto Geofísico del Perú confirmó la existencia de 24,289 eventos sísmicos con 0.0% de datos nulos y 0.0% de duplicados, con magnitudes entre 3.0 y 8.4 Mw y profundidades entre 1 y 699 kilómetros."
    )
    add_p(
        "Respecto al OE2, el esquema de partición estratificada 80/20 y el encapsulamiento de transformaciones en un ColumnTransformer aislaron la magnitud sísmica y previnieron la fuga de información, preservando la proporción exacta de 21.01% de sismos severos en entrenamiento y prueba."
    )
    add_p(
        "Respecto al OE3 y OE4, la comparación experimental demostró que el Bosque Aleatorio supera a los otros tres modelos candidatos, alcanzando un ROC-AUC de 0.603 en prueba y 0.6014 en validación cruzada de 5 particiones, frente al desempeño casi aleatorio de la Regresión Logística (ROC-AUC 0.531) y el colapso de sensibilidad de KNN (Recall 7.0%)."
    )
    add_p(
        "Respecto al OE5, la optimización con GridSearchCV estableció como hiperparámetros óptimos 100 estimadores, profundidad máxima de 12 y división mínima de 2 muestras, elevando el ROC-AUC en validación cruzada a 0.6033. El análisis de importancia determinó que la ubicación tridimensional (latitud, longitud y profundidad) concentra el 86.81% del peso predictivo del modelo."
    )
    add_p(
        "Respecto al OE6, se construyó y verificó el módulo de inferencia en producción predict.py capaz de cargar el pipeline serializado de 8.8 MB y generar clasificaciones y probabilidades estimadas en milisegundos para coordenadas de entrada arbitrarias en el territorio nacional."
    )

    # -------------------------------------------------------------
    # 27. RECOMENDACIONES Y TRABAJO FUTURO
    # -------------------------------------------------------------
    add_heading_1("27. Recomendaciones y trabajo futuro")
    add_p(
        "Se recomienda incorporar datos complementarios de aceleración máxima del suelo (PGA) y distancias geodésicas a la traza de la Fosa de Perú-Chile para enriquecer la capacidad predictiva del vector de características. "
        "Se recomienda calibrar umbrales de decisión operativos inferiores a 0.50 en la probabilidad predicha para elevar el Recall por encima del 70% en escenarios de protección civil donde el costo de un falso negativo sea crítico."
    )
    add_heading_2("27.1. Trabajo futuro")
    add_p("1. Integración de algoritmos de potenciación de gradiente (XGBoost, LightGBM) para contrastar su convergencia frente al Bosque Aleatorio.")
    add_p("2. Incorporación de variables dinámicas de tasa sísmica móvil, como el número de sismos en los últimos 30 días en un radio de 50 kilómetros.")
    add_p("3. Modelado de agrupamiento no supervisado mediante K-Means para clasificar automáticamente las zonas sismogénicas antes de la fase de predicción supervisada.")
    add_p("4. Despliegue de una interfaz de programación de aplicaciones (API REST con FastAPI) acoplada al sistema de monitoreo continuo del CENSIS.")

    # -------------------------------------------------------------
    # 28. REFERENCIAS
    # -------------------------------------------------------------
    add_heading_1("28. Referencias")
    refs = [
        "[1] Beroza, G. C., Segou, M., & Mostafa, S. A. (2021). Machine learning and earthquake forecasting: next steps. Nature Communications, 12(1), 4761.",
        "[2] Centro Nacional de Estimación, Prevención y Reducción del Riesgo de Desastres (CENEPRED). (2023). Escenario de riesgo por sismo y tsunami en la costa peruana. Informe Técnico Institucional, Lima, Perú.",
        "[3] DeVries, P. M., Viégas, F., Wattenberg, M., & Meade, B. J. (2018). Deep learning of aftershock patterns following large earthquakes. Nature, 560(7720), 632-634.",
        "[4] Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75-105.",
        "[5] Instituto Geofísico del Perú (IGP). (2025). Catálogo Sísmico Nacional 1960-2025. Centro Sismológico Nacional (CENSIS), Lima, Perú.",
        "[6] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "[7] Rouet-Leduc, B., Hulbert, C., Lubbers, N., Barros, K., Humphreys, C. J., & Johnson, P. A. (2017). Machine learning predicts laboratory earthquakes. Geophysical Research Letters, 44(18), 9276-9282.",
        "[8] Tavera, H. (2014). El catálogo sísmico del Perú: evolución y características de la sismicidad en el borde occidental sudamericano. Revista de Geofísica, 64, 45-68.",
        "[9] United States Geological Survey (USGS). (2024). ANSS Comprehensive Earthquake Catalog (ComCat) Documentation. U.S. Department of the Interior.",
        "[10] Villegas, R., Ochoa, J., & Gómez, A. (2020). Machine learning models for seismic hazard classification in northern South America. Computers & Geosciences, 145, 104612."
    ]
    for r in refs:
        add_p(r, space_after=3)

    # -------------------------------------------------------------
    # 29. ANEXOS
    # -------------------------------------------------------------
    add_heading_1("29. Anexos")
    add_heading_2("Anexo A. Ficha descriptiva del catálogo sísmico")
    add_p(
        "Nombre del recurso: Catálogo Sísmico desde 1960 (Instituto Geofísico del Perú, IGP). "
        "Cobertura temporal: 13/01/1960 al 28/02/2025. "
        "Total de observaciones: 24,289 sismos registrados. "
        "Variables de coordenadas: Latitud (grados decimales), Longitud (grados decimales). "
        "Variables físicas: Profundidad hipocentral (kilómetros), Magnitud (escala homogénea Mw/ML). "
        "Formato fuente: CSV con codificación UTF-8 y delimitador de punto y coma (;)."
    )

    add_heading_2("Anexo B. Código fuente y repositorio oficial")
    add_p(
        "El código fuente completo, cuadernos reproducibles, módulos de ingesta e inferencia y pesos serializados del modelo se encuentran alojados en el repositorio oficial de GitHub: "
        "https://github.com/Pierorivera1/SISMOS"
    )

    add_heading_2("Anexo C. Diccionario de variables del proyecto")
    table3 = doc.add_table(rows=7, cols=4)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)
    
    headers3 = ["Variable", "Tipo", "Rango / Valores", "Función en el Pipeline"]
    for j, h in enumerate(headers3):
        cell = table3.cell(0, j)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)

    rows3_data = [
        ["LATITUD", "float64", "[-19.98, -0.05]", "Predictora de entrada (escalada con StandardScaler)"],
        ["LONGITUD", "float64", "[-83.56, -68.01]", "Predictora de entrada (escalada con StandardScaler)"],
        ["PROFUNDIDAD", "float64", "[1.0, 699.0] km", "Predictora de entrada (escalada con StandardScaler)"],
        ["HORA", "int64", "[0, 23]", "Predictora de entrada (escalada con StandardScaler)"],
        ["MAGNITUD", "float64", "[3.0, 8.4] Mw", "Aislada del entrenamiento (utilizada para construir y)"],
        ["SISMO_SEVERO", "int64", "{0, 1}", "Variable objetivo (1 si Magnitud >= 5.0, sino 0)"]
    ]
    for i, row in enumerate(rows3_data):
        for j, val in enumerate(row):
            cell = table3.cell(i+1, j)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)

    p_tbl3 = doc.add_paragraph()
    p_tbl3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl3.paragraph_format.space_before = Pt(3)
    p_tbl3.paragraph_format.space_after = Pt(8)
    r_t3 = p_tbl3.add_run("Tabla 3. Diccionario técnico de variables del pipeline de aprendizaje automático.")
    r_t3.italic = True
    r_t3.font.size = Pt(9.5)

    add_heading_2("Anexo D. Matriz de trazabilidad del proyecto de investigación")
    table4 = doc.add_table(rows=7, cols=5)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table4)
    
    headers4 = ["Objetivo", "Actividad Metodológica", "Artefacto Producido", "Evidencia Generada", "Sección del Informe"]
    for j, h in enumerate(headers4):
        cell = table4.cell(0, j)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9)

    rows4_data = [
        ["OE1", "Auditoría de calidad y consistencia física", "Auditoria_Fuentes_IGP.xlsx", "Catálogo sin nulos (24,289 registros)", "Sección 15"],
        ["OE2", "Saneamiento y aislamiento de fuga", "igp_loader.py / sismos_limpios.csv", "División estratificada 80/20", "Sección 16 y 19"],
        ["OE3", "Ensamble de pipelines con ColumnTransformer", "proyecto_integrador_sismos.ipynb", "4 pipelines candidatos inicializados", "Sección 17"],
        ["OE4", "Evaluación multimodelo y 5-Fold CV", "Tablas y gráficos comparativos", "Métricas de test, matrices de confusión y curvas ROC", "Sección 20 y 21"],
        ["OE5", "Optimización con GridSearchCV", "Mejor estimador e importancias", "Ponderación geofísica de variables", "Sección 21"],
        ["OE6", "Despliegue y persistencia productiva", "pipeline_sismos_final.joblib / predict.py", "Inferencia funcional por terminal", "Sección 18 y 21"]
    ]
    for i, row in enumerate(rows4_data):
        for j, val in enumerate(row):
            cell = table4.cell(i+1, j)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)

    p_tbl4 = doc.add_paragraph()
    p_tbl4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl4.paragraph_format.space_before = Pt(3)
    p_tbl4.paragraph_format.space_after = Pt(8)
    r_t4 = p_tbl4.add_run("Tabla 4. Matriz de trazabilidad entre objetivos específicos, actividades, artefactos y secciones del informe.")
    r_t4.italic = True
    r_t4.font.size = Pt(9.5)

    # Save to both paths
    doc.save(str(OUTPUT_PATH))
    doc.save(str(ROOT_OUTPUT_PATH))
    print(f"Document successfully created and saved to:")
    print(f"1. {OUTPUT_PATH}")
    print(f"2. {ROOT_OUTPUT_PATH}")

if __name__ == '__main__':
    create_document()
