---
type: psi-investigation
psi_id: PSI-102
acronym: "SAFFIRE-III"
facility: "Cygnus (post-desacople ISS)"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-102"]
---

# PSI-102: SAFFIRE-III

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Registros de camaras y telemetria de flujo alto (30 cm/s) sobre panel grande SIBAL en ducto cerrrado.

## 2. Informacion util y variables criticas
Valida la aceleracion de la llama cuando sube la velocidad del ventilador de 20 cm/s a 30 cm/s y define la cota maxima de flujo seguro antes de cerrar compuerta.

## 3. Como alimenta el entrenamiento ML / DL propio
Ajusta curvas de regresion $V_f$ en `M1` y calibra los umbrales de flujo y $\Delta T/\Delta t$ que activan el estado `CONTENCION` en `M2` (`DeterministicFsmController`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-98_SAFFIRE-I]], [[PSI-103_SAFFIRE-IV]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
