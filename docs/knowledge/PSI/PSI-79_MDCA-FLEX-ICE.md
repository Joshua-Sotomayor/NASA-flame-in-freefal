---
type: psi-investigation
psi_id: PSI-79
acronym: "MDCA-FLEX-ICE"
facility: "ISS - CIR (MDCA)"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-79"]
---

# PSI-79: MDCA-FLEX-ICE

**Instalacion:** `ISS - CIR (MDCA)` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Registros experimentales ASI/NASA sobre gotas bicomponentes (mezclas multicomponente) con evaporacion preferencial y microexplosiones.

## 2. Informacion util y variables criticas
Explica cambios abruptos en tasa de quemado cuando dos liquidos de distinta volatilidad se mezclan en microgravedad.

## 3. Como alimenta el entrenamiento ML / DL propio
Aporta casos multicomponente para generalizacion de `Burn Time` en `M1` y alimenta el cluster de combustion de gotas en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]]
- **Investigaciones relacionadas:** [[PSI-27_FLEX-2]], [[PSI-78_FLEX-2J]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
