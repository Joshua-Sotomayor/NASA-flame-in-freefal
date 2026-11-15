---
type: psi-investigation
psi_id: PSI-26
acronym: "BASS"
facility: "ISS - MSG"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-26"]
---

# PSI-26: BASS

**Instalacion:** `ISS - MSG` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Matrices ISA-Tab, videos de llamas en varillas/esferas/laminas de PMMA, algodon y SIBAL en Microgravity Science Glovebox (MSG).

## 2. Informacion util y variables criticas
Demostro la paradoja de flujo bajo: a velocidades < 5 cm/s en 0g ciertos solidos arden a menor %O2 que en 1g y apagar el ventilador puede avivar brevemente la llama.

## 3. Como alimenta el entrenamiento ML / DL propio
Sustenta la histeresis temporal en `M2` (`DeterministicFsmController`) al reducir ventilador, aporta casos de extincion a flujo bajo en `M1` y forma nucleo del cluster solidos en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-25_BASS-II]], [[PSI-98_SAFFIRE-I]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
