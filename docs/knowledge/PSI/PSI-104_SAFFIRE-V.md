---
type: psi-investigation
psi_id: PSI-104
acronym: "SAFFIRE-V"
facility: "Cygnus (post-desacople ISS)"
domain: "Gestion Industrial"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-104"]
---

# PSI-104: SAFFIRE-V

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Gestion_Industrial]] (`Gestion Industrial`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Ensayos en atmosfera lunar (8.2 psi / 56.5 kPa y 30-34% O2) con registros de encendido, presion y consumo de oxigeno.

## 2. Informacion util y variables criticas
Referencia normativa directa para estandares NASA de habitats lunares y rovers presurizados; demuestra mayor rapidez de ignicion pese a menor presion total.

## 3. Como alimenta el entrenamiento ML / DL propio
Valida la region subatmosferica enriquecida de `M1` y alimenta los pesos `habitat` en `M3` (`TopsisMultiCriteriaRanker`) y la matriz FMEA (`NASA-STD-6001`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-103_SAFFIRE-IV]], [[PSI-105_SAFFIRE-VI]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
