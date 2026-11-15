---
type: psi-investigation
psi_id: PSI-138
acronym: "CFI-G"
facility: "ISS - CIR"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-138"]
---

# PSI-138: CFI-G

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Series termicas de camara esferica hasta 85% O2 con butano, propano y DME; diagnosticos UV y de cinetica NTC.

## 2. Informacion util y variables criticas
Demuestra llamas frías difusivas en gases (inside-out flames) sin ignicion caliente previa; impacto directo en motores HCCI limpios y riesgos de fugas de gas.

## 3. Como alimenta el entrenamiento ML / DL propio
Refuerza la clase `2: Llama Fria NTC` de `M2` (`flame_cnn.onnx` + baja emision luminosa con gradiente termico moderado en `DecisionTree`) y Spinoffs de combustion limpia.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-24_FLEX]], [[PSI-27_FLEX-2]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
