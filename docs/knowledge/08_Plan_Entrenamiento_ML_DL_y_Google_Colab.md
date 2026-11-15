---
type: ml-training-plan
tags: [nasa/ml, google-colab, gpu, onnx, sha256, offline-first]
---

# Plan de Entrenamiento ML/DL y Uso Estrategico de Google Colab

Los paquetes completos de NASA PSI alcanzan `255.77 GB` (`BASS-II`) por video crudo de alta velocidad. Descargar todo a disco local durante un hackathon de 48h bloquea el avance sin mejorar la precision en tiempo de entrega. Este documento fija **cuando usar Google Colab (GPU T4)**, **cuando entrenar en CPU local** y como unificar ambos en artefactos verificados por `SHA-256`.

Ver diagrama compilado: `![[grafos/ml_dl_colab_pipeline.svg]]` y el notebook ejecutable en el repositorio: `notebooks/AERO_IGNIS_Colab_Training.ipynb`.

---

## 1. Decision Tecnica: Google Colab vs. CPU Local por Modelo

| Modelo | Algoritmo | Donde Entrenar | Por Que Esa Eleccion | Artefacto Exportado |
| :--- | :--- | :--- | :--- | :--- |
| **[[M1_RandomForest_GBR_Inflamabilidad]]** | `RandomForestClassifier` + `GradientBoostingRegressor` (`scikit-learn`) | **CPU Local** (`backend/train_models.py`) + validacion cruzada en **Colab** | Tablas `BASS-II` (>130 corridas, 17 cols) y `Saffire` pesan <1 MB y entrenan en `< 2 s` con reproducibilidad por semilla (`SEED=42`). | `flammability_rf.joblib`, `burntime_gbr.joblib` |
| **[[M2_CNN_ONNX_DecisionTree_FSM]] (Rama Optica)** | CNN ligera en **PyTorch** (`FlameCnn`) exportada a **ONNX** | **Google Colab T4 GPU** (streaming OSDR) + **CPU Local** (fallback reproducible) | Si extraemos parches reales de video desde `OSDR API v2` / `s3://nasa-osdr/`, la GPU T4 de Colab evita saturar la RAM del portatil y permite *data augmentation* rotacional $0g$ en segundos. | `flame_cnn.onnx` |
| **[[M2_CNN_ONNX_DecisionTree_FSM]] (Rama Sensores)** | `DecisionTreeClassifier` (`max_depth=4`) | **CPU Local** (`train_models.py`) | Entrena sobre umbrales fisicos ($\Delta T/\Delta t$, $\text{CO}$, aerosol $<0.1\,\mu\text{m}$, flujo) en `< 0.2 s` y genera arbol de reglas legible. | `sensor_tree.joblib` |
| **[[M3_PCA_KMeans_TFIDF_TOPSIS]]** | `TfidfVectorizer` + `PCA(2)` + `KMeans` + `TextRank` | **CPU Local** (`train_models.py`) | Corpus de 24 investigaciones ISA-Tab pesa <100 KB; entrena y calcula similitud coseno en `< 0.5 s`. | `psi_tfidf_kmeans.joblib` |

---

## 2. Flujo Practico en Google Colab (`AERO_IGNIS_Colab_Training.ipynb`)

1. **Ingesta Selectiva (Anti-SSRF y Cero Descarga Masiva):**
   - Usar `fetch_osdr_safe()` restringido por *allowlist* a `https://osdr.nasa.gov/` y `https://visualization.osdr.nasa.gov/`.
   - Leer por streaming exclusivamente archivos `.csv` (*Experimental Tables*), metadatos `ISA-Tab` y frames clave (`.png`/`.jpg`) representativos de las 4 clases:
     - `0: Nominal` (sin combustion activa)
     - `1: Llama Esferica Azul 0g` (`[[PSI-146_ACME-Flame-Design]]`, `[[PSI-147_ACME-s-Flame]]`)
     - `2: Llama Fria NTC` (`[[PSI-24_FLEX]]`, `[[PSI-138_CFI-G]]`)
     - `3: Propagacion Abierta` (`[[PSI-98_SAFFIRE-I]]`, `[[PSI-25_BASS-II]]`)
2. **Data Augmentation Fisicamente Valido en Microgravedad:**
   - Como $\text{Gr} \to 0$ elimina el "arriba/abajo" convectivo en gotas y llamas esfericas, rotaciones de $90^\circ / 180^\circ / 270^\circ$ y volteos horizontales/verticales preservan la fisica real y multiplican por 8 las muestras sin distorsionar etiquetas.
3. **Exportacion Ligera y Sello Criptografico (`SHA-256`):**
   - Exportar el modelo PyTorch a `flame_cnn.onnx` (`opset_version=17`) y todos los `.joblib`.
   - Verificar peso total `< 15 MB` para subirlo limpiamente a GitHub sin LFS ni costo.
   - Generar `artifacts/models/manifest.sha256.json`. El servidor FastAPI **nunca** cargara un modelo si su hash real difiere del manifiesto.

---

## 3. Regla de Resiliencia para Pruebas TDD (`pytest`)

- Ni las pruebas unitarias ni las pruebas de integracion pueden depender de conexion a Google Colab ni a internet.
- `backend/train_models.py` comparte las mismas arquitecturas y clases de `AERO_IGNIS_Colab_Training.ipynb` para reconstruir pesos validos en `< 5 s` sobre `data/bass_saffire_runs.csv` y firmas opticas calibradas si se ejecuta en entorno aislado CI/TDD.

---

## 4. Reparto de Responsabilidades

- **[[Rol_Mecatronica_y_Control]]:** Ejecucion de Colab T4 / `train_models.py`, calibracion CNN ONNX, ajuste de hiperparametros RF/GBR y registro `SHA-256`.
- **[[Rol_Gestion_Industrial]]:** Validacion de matrices de confusion, lectura de `feature_importances_`, coherencia de pesos `TOPSIS` y auditoria de metricas en FMEA (`NASA-STD-6001`).
