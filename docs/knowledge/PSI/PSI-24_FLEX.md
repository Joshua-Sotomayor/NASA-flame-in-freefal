---
type: psi-investigation
psi_id: PSI-24
acronym: "FLEX"
facility: "ISS - CIR (MDCA)"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-24"]
---

# PSI-24: FLEX

**Instalacion:** `ISS - CIR (MDCA)` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Videos radiometricos, camaras UV OH* (310 nm) y curvas $d(t)^2$ de gotas aisladas (heptano, metanol, decano de 2-5 mm) en MDCA.

## 2. Informacion util y variables criticas
Descubrio las llamas frias (500-800 K) invisibles al ojo humano tras la aparente extincion de una llama caliente, con riesgo de re-ignicion.

## 3. Como alimenta el entrenamiento ML / DL propio
Pieza central para la clase `2: Llama Fria NTC` en `M2` (`flame_cnn.onnx`) y para que la `FSM` prohiba regresar a `NORMAL` sin enfriamiento confirmado.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-27_FLEX-2]], [[PSI-138_CFI-G]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
