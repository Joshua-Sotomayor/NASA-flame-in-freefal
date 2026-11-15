---
type: psi-investigation
psi_id: PSI-132
acronym: "BRE (ACME)"
facility: "ISS - CIR"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-132"]
---

# PSI-132: BRE (ACME)

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Datos de quemador plano poroso alimentado con gas en CIR, flujo de calor superficial y numero B de Spalding equivalente.

## 2. Informacion util y variables criticas
Emula materiales solidos y liquidos en estado estacionario sin destruir muestras, conectando quimica gaseosa con inflamabilidad de solidos.

## 3. Como alimenta el entrenamiento ML / DL propio
Enriquece el dominio fisico del numero $B$ de transferencia de masa en `M1` (`DimensionlessPhysicsCalculator`) y vincula clusters solidos/gases en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]]
- **Investigaciones relacionadas:** [[PSI-25_BASS-II]], [[PSI-146_ACME-Flame-Design]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
