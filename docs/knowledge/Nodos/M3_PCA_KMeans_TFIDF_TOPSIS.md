---
type: nlp-model
model_id: M3
artifacts: [psi_tfidf_kmeans.joblib]
tags: [nasa/nlp, topsis, pca, kmeans, textrank, writing-craft]
---

# Modelo 3: Agrupamiento Vectorial, Resumen Extractivo y Ranking TOPSIS

Reemplaza cualquier llamada a LLMs externos por un motor NLP estadistico y determinista sobre los metadatos ISA-Tab de las 24 PSI.

## Pipeline Explicable
1. Vectorizacion `TF-IDF` + reduccion `PCA (2D)` + clustering `K-Means` sobre `Objectives`, `Approach`, `Earth Benefits` y sensores.
2. Ranking multicriterio `TOPSIS/AHP` ponderado por `Gestion Industrial`.
3. Extraccion `TextRank + Similitud de Coseno` formateada mediante plantillas **`writing-craft`** (`academic` para Investigador, `plain` para Estudiante y Gestor) garantizando **0 alucinaciones** y citas validas de DOI `10.60555`.

## Conexiones
- Cumple [[O1_Resumen_y_Ranking_PSI]] y apoya [[O4_Spinoffs_Terrestres_y_Forense]]
- Liderado por [[Rol_Gestion_Industrial]] y [[Rol_Mecatronica_y_Control]]
