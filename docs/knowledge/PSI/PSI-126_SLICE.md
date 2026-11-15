---
type: psi-investigation
psi_id: PSI-126
acronym: "SLICE"
facility: "ISS - MSG"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-126"]
---

# PSI-126: SLICE

**Instalacion:** `ISS - MSG` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Imagenes de estructura termica y datos de flujo en hardware compartido MSG para metano y etileno con co-flujo laminar.

## 2. Informacion util y variables criticas
Cuantifica la altura de desprendimiento de base de llama (`liftoff`) y el punto exacto de soplado (`blowout`) cuando sube la velocidad de ventilacion.

## 3. Como alimenta el entrenamiento ML / DL propio
Define la frontera superior `Blowoff` del parametro adimensional $\text{Da}$ en `M1` y estabiliza el control de velocidad de ventilador en `M2`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-129_SPICE]], [[PSI-25_BASS-II]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
