# Registro de Sesiones y Arquitectura de Trabajo - Proyecto SISMOS

Este directorio consolida las bitácoras detalladas de cada sesión/agente que participó en el desarrollo del proyecto de Machine Learning para el catálogo sísmico del **Instituto Geofísico del Perú (IGP)**.

---

## 👥 Equipo de Sesiones y Roles

| Agente / Sesión | ID de Conversación | Panel Herdr | Rol Principal | Archivo de Bitácora |
| :--- | :--- | :--- | :--- | :--- |
| **Learner** | `4724f47d-d763-4afe-b0cf-81db46b2dc43` | `w1:p3` | Arquitectura de ML, Coordinación, Integración y Mejores Prácticas | [`sesion_learner.md`](sesion_learner.md) |
| **Kiara** | `2c18b352-afc2-4582-a6ea-c708a7dba92e` | `w1:p8` | Entorno Interactivo Jupyter, EDA Geoespacial y Cuaderno Maestro Integrador | [`sesion_kiara.md`](sesion_kiara.md) |
| **Back** | `fc04c5fa-4adf-4fdd-86cd-d913256e11e3` | `w1:p1` | Reorganización Estructural, Pipeline de Ingesta (`igp_loader.py`) e Inferencia (`predict.py`) | [`sesion_back.md`](sesion_back.md) |

---

## 🔄 Infraestructura y Canales de Comunicación

1. **Multiplexor de Terminales:** [Herdr](https://herdr.dev) (`v0.8.2`) gestionando los tres paneles en el workspace `w1`.
2. **Bus de Mensajería:** Protocolo inter-agente nativo de Antigravity (`send_message`) para delegación y sincronización de tareas en segundo plano.
3. **Persistencia y Reproducibilidad:**
   - Datos crudos: `SISMOS/data/raw/IGP/`
   - Datos procesados: `SISMOS/data/processed/sismos_limpios.csv`
   - Laboratorio visual: `SISMOS/NOTEBOOKS/proyecto_integrador_sismos.ipynb`
   - Código productivo: `SISMOS/src/data/igp_loader.py` y `SISMOS/src/models/predict.py`
   - Modelo serializado: `SISMOS/models/pipeline_sismos_final.joblib`
