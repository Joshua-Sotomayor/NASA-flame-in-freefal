---
type: psi-investigation
psi_id: PSI-147
acronym: "ACME - s-Flame"
facility: "ISS - CIR"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-147"]
---

# PSI-147: ACME - s-Flame

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Registros de radiometria, evolucion radial de llamas esfericas de metano/etileno y tablas de validacion cinetica.

## 2. Informacion util y variables criticas
Mide con precision cuando las perdidas radiativas (proporcionales a $T^4$) extinguen una llama difusiva esferica sin flotabilidad.

## 3. Como alimenta el entrenamiento ML / DL propio
Calibra el limite de apagado radiativo ($	ext{Da}$ critico) en `M1`, aporta ejemplos negativos/extincion a `M2` y posiciona el cluster gaseoso en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-146_ACME-Flame-Design]], [[PSI-24_FLEX]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
