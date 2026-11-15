---
type: psi-investigation
psi_id: PSI-98
acronym: "SAFFIRE-I"
facility: "Cygnus (post-desacople ISS)"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-98"]
---

# PSI-98: SAFFIRE-I

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Paquete CC0-1.0 de 11.41 GB con ISA-Tab (`i_investigation.txt`, `s_study.txt`, `a_assay.txt`), Experimental Table de 13 columnas, dos camaras opticas, anemometria, termopares y radiometros.

## 2. Informacion util y variables criticas
Panel grande de tejido SIBAL (0.4 x 0.94 m) a flujo forzado de 20 cm/s y 21% O2. Permite medir crecimiento de llama a escala de cabina sin riesgos para la tripulacion.

## 3. Como alimenta el entrenamiento ML / DL propio
Alimenta `M1` (`RandomForest`/`GBR`) para escalar velocidad de propagacion $V_f$ y `Burn Time`; entrega frames de propagacion abierta para `M2` (`flame_cnn.onnx`); nutre corpus `M3` (`TF-IDF` + `TOPSIS`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-101_SAFFIRE-II]], [[PSI-102_SAFFIRE-III]], [[PSI-25_BASS-II]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
