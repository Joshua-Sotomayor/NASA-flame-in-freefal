---
type: psi-investigation
psi_id: PSI-110
acronym: "MSC"
facility: "Otros / STS - Microgravedad"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-110"]
---

# PSI-110: MSC

**Instalacion:** `Otros / STS - Microgravedad` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Termopares internos, perfiles de oxigeno y velocidad de frente sin llama (*smoldering*) en espumas porosas de poliuretano y transicion a llama abierta.

## 2. Informacion util y variables criticas
Demuestra combustion latente silenciosa sin luz visible que emite CO sostenido y puede detonar en llama abierta al aumentar el flujo de aire.

## 3. Como alimenta el entrenamiento ML / DL propio
Entrena el detector tabular temprano (`PRE_ALERTA` con `co_ppm` elevado pero camara optica `Nominal`) en `M2` (`DecisionTreeClassifier`) y nutre el FMEA.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-129_SPICE]], [[PSI-105_SAFFIRE-VI]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
