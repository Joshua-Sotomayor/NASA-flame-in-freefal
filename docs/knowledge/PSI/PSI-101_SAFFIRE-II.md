---
type: psi-investigation
psi_id: PSI-101
acronym: "SAFFIRE-II"
facility: "Cygnus (post-desacople ISS)"
domain: "Combinado"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-101"]
---

# PSI-101: SAFFIRE-II

**Instalacion:** `Cygnus (post-desacople ISS)` | **Dominio / Rol:** [[Rol_Combinado_Sinergia]] (`Combinado`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Tablas de 9 muestras multiples en ducto Cygnus, logs termicos, sensores de flujo y metadata ISA-Tab.

## 2. Informacion util y variables criticas
Compara PMMA plano y ranurado, tejido SIBAL, Nomex y silicona bajo flujo concurrente y opuesto para clasificar inflamabilidad por geometria y espesor.

## 3. Como alimenta el entrenamiento ML / DL propio
Etiqueta multiples materiales en `M1` (`RandomForestClassifier`) y cuantifica la importancia del espesor y direccion de flujo; alimenta criterios de materiales en `M3` (`TOPSIS`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]]
- **Investigaciones relacionadas:** [[PSI-98_SAFFIRE-I]], [[PSI-25_BASS-II]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
