---
type: psi-investigation
psi_id: PSI-78
acronym: "FLEX-2J"
facility: "ISS - CIR (MDCA)"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-78"]
---

# PSI-78: FLEX-2J

**Instalacion:** `ISS - CIR (MDCA)` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Datos conjuntos NASA-JAXA de propagacion de llama a lo largo de arreglos lineales y planos de gotas de combustible en 0g.

## 2. Informacion util y variables criticas
Entrega velocidades discretas de salto de llama entre gotas (percolacion termica), utiles para modelar propagacion en neblinas o derrames dispersos.

## 3. Como alimenta el entrenamiento ML / DL propio
Enriquece la regresion de tasa de propagacion en `M1` para escenarios con multiples focos cercanos y amplifica la cobertura internacional en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]]
- **Investigaciones relacionadas:** [[PSI-27_FLEX-2]], [[PSI-79_MDCA-FLEX-ICE]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
