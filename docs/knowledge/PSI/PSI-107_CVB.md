---
type: psi-investigation
psi_id: PSI-107
acronym: "CVB"
facility: "ISS - MSG"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-107"]
---

# PSI-107: CVB

**Instalacion:** `ISS - MSG` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Datos de interferometria optica, temperatura axial y dinamica de burbuja de vapor restringida (pentano) en tubo termico de cuarzo.

## 2. Informacion util y variables criticas
Modela transferencia termica interfacial, evaporacion y condensacion en ausencia de gravedad hidrostatica.

## 3. Como alimenta el entrenamiento ML / DL propio
Aporta base fisica de difusion termica ($	ext{Pe}$) y evaporacion interfacial en `M1` y separa el cluster termofluido en `M3` (`PCA + K-Means`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]]
- **Investigaciones relacionadas:** [[PSI-108_CVB-2]], [[PSI-24_FLEX]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
