---
type: psi-investigation
psi_id: PSI-109
acronym: "NCA"
facility: "Otros / Analogo 1g (NASA GRC)"
domain: "Gestion Industrial"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-109"]
---

# PSI-109: NCA

**Instalacion:** `Otros / Analogo 1g (NASA GRC)` | **Dominio / Rol:** [[Rol_Gestion_Industrial]] (`Gestion Industrial`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Datos comparativos entre canal estrecho terrestre (1g con conveccion suprimida entre placas frias) y corridas orbitales BASS/ISS.

## 2. Informacion util y variables criticas
Valida un metodo terrestre economico para certificar materiales bajo `NASA-STD-6001` antes de enviarlos en cohete a pruebas orbitales.

## 3. Como alimenta el entrenamiento ML / DL propio
Permite calibrar factor de correlacion `1g analogo -> 0g` en `M1` y justificar ahorro de costos de certificacion en el enfoque de Gestion Industrial (`M3`).

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M1_RandomForest_GBR_Inflamabilidad]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O4_Spinoffs_Terrestres_y_Forense]]
- **Investigaciones relacionadas:** [[PSI-25_BASS-II]], [[PSI-26_BASS]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
