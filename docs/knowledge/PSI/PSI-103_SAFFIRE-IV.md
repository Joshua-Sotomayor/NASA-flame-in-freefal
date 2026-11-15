---
type: psi-investigation
psi_id: PSI-103
acronym: "SAFFIRE-IV"
facility: "Cygnus (post-desacople ISS)"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-103"]
---

# PSI-103: SAFFIRE-IV

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Logs de presion, oxigeno enriquecido (30-34% O2), concentraciones de gases post-incendio y diagnosticos de supresion en modulo Cygnus.

## 2. Informacion util y variables criticas
Mide el comportamiento de atmosferas de exploracion Artemis/lunares enriquecidas en oxigeno y la respuesta de sensores de gases en volumen habitable cerrado.

## 3. Como alimenta el entrenamiento ML / DL propio
Dato critico de frontera para `M1` en escenarios lunares (O2 > 30%) y calibracion de alertas tempranas de gases en `M2` (`DecisionTreeClassifier`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-104_SAFFIRE-V]], [[PSI-105_SAFFIRE-VI]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
