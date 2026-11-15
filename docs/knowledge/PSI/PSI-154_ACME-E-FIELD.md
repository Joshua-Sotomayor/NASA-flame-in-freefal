---
type: psi-investigation
psi_id: PSI-154
acronym: "ACME - E-FIELD"
facility: "ISS - CIR"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-154"]
---

# PSI-154: ACME - E-FIELD

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Logs electricos de electrodos de malla hasta +/-10 kV, corriente ionica, video de deformacion de llama y tasas de supresion.

## 2. Informacion util y variables criticas
Demuestra control y supresion de llamas mediante viento ionico sin piezas moviles y emulacion de gravedad parcial sin cambiar la orbita.

## 3. Como alimenta el entrenamiento ML / DL propio
Alimenta la estrategia alternativa de supresion `E-FIELD` frente a `PFE` en el modulo de gobernanza y amplia firmas deformadas en `M2`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-146_ACME-Flame-Design]], [[PSI-153_ACME-CLD-Flame]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
