---
type: moc
project: AERO-IGNIS-SI
challenge: "NASA Space Apps 2026 - Flame in Freefall"
status: "SDD Gate 1 + Knowledge Base Activa"
tags: [nasa/space-apps-2026, moc, graphviz, ml-pipeline, tdd, writing-craft]
---

# Indice Maestro — Base de Conocimiento AERO-IGNIS SI

Este nodo conecta las **24 investigaciones de combustion de NASA PSI**, los **10 recursos oficiales**, los **3 modelos ML/DL propios**, la estrategia dual **Local CPU + Google Colab GPU**, la **piramide TDD** y la disciplina editorial **`writing-craft`**. Presiona `Ctrl + G` en Obsidian para ver el grafo completo de conexiones, o abre [[AERO_IGNIS_Conocimiento_y_ML.canvas]].

---

## 1. Mapa de Notas Principales (Dominios y Metodologia)

1. [[01_Objetivos_Dominios_y_Roles]] — Matriz completa que cruza 24 PSI + 10 recursos -> datos utiles -> modelos ML/DL -> Objetivos (`O1`-`O4`) -> rol lider.
2. [[02_Campanas_Saffire_I_a_VI_Cygnus]] — Analisis de `SAFFIRE-I` a `VI` (13 columnas, tejido SIBAL, atmosferas $30\text{–}34\%\text{ O}_2$, gases $\text{CO}/\text{HF}/\text{HCl}$).
3. [[03_Solidos_en_Microgravedad_BASS_BRE_MSC_NCA]] — Analisis de `BASS`, `BASS-II` (17 cols, $>130$ corridas), `BRE`, `MSC` (*smoldering*) y `NCA` ($1g$ analogo).
4. [[04_Gotas_y_Llamas_Frias_FLEX_CFIG]] — Llamas frias ($500\text{–}800\text{ K}$) en `FLEX`, `FLEX-2`, `FLEX-2J`, `MDCA-FLEX-ICE` y `CFI-G`.
5. [[05_Llamas_Gaseosas_Hollin_y_Campos_ACME_SLICE_SPICE]] — Suite `ACME` (`Flame Design`, `s-Flame`, `CLD`, `E-FIELD`), `SLICE`, `SPICE` y `SAME/DAFT` ($<0.1\,\mu\text{m}$).
6. [[06_Termofluidos_Interfaciales_CVB_y_CVB2]] — Evaporacion interfacial en `CVB` y `CVB-2`, base termica del Peclet y del extintor `PFE`.
7. [[07_Casos_Forenses_Apollo_Mir_y_Spinoffs_Terrestres]] — Incidentes Apollo 1, Apollo 13 y Mir + Spinoffs `9582`, `9407`, `9918` y `PFE`.
8. [[08_Plan_Entrenamiento_ML_DL_y_Google_Colab]] — Cuando usar **Google Colab T4** vs **CPU local**, manejo de datos OSDR sin descargar 255 GB y manifiesto `SHA-256`.
9. [[09_Estrategia_TDD_y_Redaccion_Writing_Craft]] — Piramide TDD (`80% Unit / 15% Integration / 5% E2E`), ciclo `RED -> GREEN -> REFACTOR` y reglas editoriales `writing-craft`.

---

## 2. Grafos Visuales Compilados con Graphviz (`dot.exe`)

### Grafo 1: 24 PSI -> 3 Modelos ML/DL -> 4 Objetivos -> Roles
![[grafos/psi_knowledge_graph.svg]]

### Grafo 2: Pipeline Dual Google Colab / CPU Local y Blindaje OWASP
![[grafos/ml_dl_colab_pipeline.svg]]

### Grafo 3: Arquitectura TDD (Unitaria + Integracion) + SDD + writing-craft
![[grafos/tdd_sdd_architecture.svg]]

---

## 3. Nodos Hub (Objetivos, Modelos y Roles)

- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]] | [[O2_Prediccion_Inflamabilidad_Habitats]] | [[O3_Deteccion_Supresion_Gemelo_FSM]] | [[O4_Spinoffs_Terrestres_y_Forense]]
- **Modelos Propios:** [[M1_RandomForest_GBR_Inflamabilidad]] | [[M2_CNN_ONNX_DecisionTree_FSM]] | [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Liderazgo del Equipo:** [[Rol_Mecatronica_y_Control]] | [[Rol_Gestion_Industrial]] | [[Rol_Combinado_Sinergia]]

---

## 4. Consultas Dinamicas Obsidian (`dataview`)

```dataview
TABLE psi_id AS "ID", facility AS "Instalacion", domain AS "Dominio"
FROM "Proyectos/NASA_Flame_In_Freefall/PSI"
SORT psi_id ASC
```
