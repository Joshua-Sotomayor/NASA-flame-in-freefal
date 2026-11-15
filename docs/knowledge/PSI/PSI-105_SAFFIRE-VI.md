---
type: psi-investigation
psi_id: PSI-105
acronym: "SAFFIRE-VI"
facility: "Cygnus (post-desacople ISS)"
domain: "Gestion Industrial"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-105"]
---

# PSI-105: SAFFIRE-VI

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Gestion_Industrial]] (`Gestion Industrial`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Ultima campana Cygnus con sensores quimicos de CO, HF, HCl, oxigeno residual, presion y perfiles termicos multi-muestra.

## 2. Informacion util y variables criticas
Cuantifica la toxicidad por gases acidos y monoxido de carbono en cabinas tras un incendio electrico o polimerico, esencial para protocolos de recuperacion y ECLSS.

## 3. Como alimenta el entrenamiento ML / DL propio
Define el umbral critico `co_ppm` en el `DecisionTreeClassifier` de `M2` y parametriza la severidad de toxicidad en la matriz `FMEA` del Objetivo 4.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-104_SAFFIRE-V]], [[PSI-110_MSC]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
