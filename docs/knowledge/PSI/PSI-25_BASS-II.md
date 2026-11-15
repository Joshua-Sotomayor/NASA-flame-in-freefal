---
type: psi-investigation
psi_id: PSI-25
acronym: "BASS-II"
facility: "ISS - MSG"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-25"]
---

# PSI-25: BASS-II

**Instalacion:** `ISS - MSG` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
255.77 GB totales (videos HD + radiometros + camaras 1/2), mas Experimental Table curada de 17 columnas y >130 corridas en PMMA, SIBAL, Nomex y Kapton.

## 2. Informacion util y variables criticas
Dataset tabular columna vertebral del proyecto: define curvas exactas de radiative quenching (bajo flujo) vs. blowoff (alto flujo), %O2 (17-28%), espesor y variable objetivo Extinguished.

## 3. Como alimenta el entrenamiento ML / DL propio
Conjunto primario de entrenamiento de `M1` (`flammability_rf.joblib` y `burntime_gbr.joblib`); frames streaming en Colab para `M2` (`flame_cnn.onnx`); fuente alta en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-26_BASS]], [[PSI-98_SAFFIRE-I]], [[PSI-109_NCA]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
