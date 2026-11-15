---
type: psi-investigation
psi_id: PSI-27
acronym: "FLEX-2"
facility: "ISS - CIR (MDCA)"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-27"]
---

# PSI-27: FLEX-2

**Instalacion:** `ISS - CIR (MDCA)` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Matrices de pares de gotas y dilucion con gases inertes (N2, CO2, He, Xe), mas curvas de extincion por radiacion y dilucion.

## 2. Informacion util y variables criticas
Cuantifica la eficiencia relativa de supresores gaseosos (N2 vs CO2) frente a llamas de gotas y el acoplamiento termico entre gotas vecinas.

## 3. Como alimenta el entrenamiento ML / DL propio
Alimenta las reglas de comparacion de supresores (`CO2` vs `PFE` vs `N2`) y provee trayectorias de extincion con diluyente para `M2`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-24_FLEX]], [[PSI-78_FLEX-2J]], [[PSI-79_MDCA-FLEX-ICE]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
