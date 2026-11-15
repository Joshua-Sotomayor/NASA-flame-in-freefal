---
type: psi-investigation
psi_id: PSI-129
acronym: "SPICE"
facility: "ISS - MSG"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-129"]
---

# PSI-129: SPICE

**Instalacion:** `ISS - MSG` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Tablas de altura de llama y punto de humo (*smoke point*) en boquillas 0.7-2.0 mm con etileno, propano y metano (complementado con SAME/DAFT).

## 2. Informacion util y variables criticas
Establece cuando una llama empieza a liberar hollin y aerosoles submicronicos (<0.1 um en SAME/Node 9407) capaces de saturar filtros HEPA del ECLSS.

## 3. Como alimenta el entrenamiento ML / DL propio
Calibra el umbral `submicron_aerosol` de alerta temprana (`PRE_ALERTA`) en `M2` (`DecisionTreeClassifier`) y enlaza con `Spinoff Node 9407`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-126_SLICE]], [[PSI-153_ACME-CLD-Flame]], [[PSI-110_MSC]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
