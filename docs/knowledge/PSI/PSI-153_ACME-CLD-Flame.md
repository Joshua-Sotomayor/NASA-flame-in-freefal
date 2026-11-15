---
type: psi-investigation
psi_id: PSI-153
acronym: "ACME - CLD Flame"
facility: "ISS - CIR"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-153"]
---

# PSI-153: ACME - CLD Flame

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Imagenes de extincion laser de hollin (635 nm), camaras visibles y logs de co-flujo laminar en camara CIR.

## 2. Informacion util y variables criticas
Cuantifica la formacion y oxidacion de hollin en co-flujo laminar extendido en 0g; clave para distinguir llamas luminosas amarillas de llamas limpias.

## 3. Como alimenta el entrenamiento ML / DL propio
Mejora el contraste visual entre llama limpia y llama productora de hollin en `flame_cnn.onnx` (`M2`) y aporta variables opticas de hollín a `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-146_ACME-Flame-Design]], [[PSI-129_SPICE]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
