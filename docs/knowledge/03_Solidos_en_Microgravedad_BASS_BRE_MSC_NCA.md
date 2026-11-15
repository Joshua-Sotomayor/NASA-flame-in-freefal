---
type: domain-analysis
facility: "ISS-MSG / STS / Analogo 1g"
investigations: [PSI-25, PSI-26, PSI-132, PSI-109, PSI-110]
tags: [nasa/solids, bass-ii, bre, smoldering, nca]
---

# Solidos en Microgravedad, Emulador Poroso y Combustion Latente

Este grupo explica cuando un material solido se apaga solo (*radiative quenching* o *blowoff*) y cuando progresa de pirolisis silenciosa a incendio abierto.

---

## 1. Investigaciones del Bloque y Variables Extraidas

1. **[[PSI-26_BASS]] y [[PSI-25_BASS-II]] (ISS-MSG):**
   - `BASS-II` suma `255.77 GB` en bruto, pero su **Experimental Table** concentra en pocas decenas de KB **mas de 130 corridas con 17 columnas exactas**: `Material` (PMMA, SIBAL, Nomex, Kapton), `Sample Thickness (cm)`, `Air Flow (cm/s)`, `Flow Direction`, `Percent O2`, `Pressure (atm)`, `Burn Time (s)` y `Extinguished (Yes/No)`.
   - **Hallazgo de control critico (Paradoja de flujo bajo):** A velocidades $<5\text{ cm/s}$, los solidos arden a menor $\% \text{O}_2$ que en $1g$; ademas, cortar bruscamente un ventilador puede reavivar brevemente una llama debil antes del apagado radiativo.
2. **[[PSI-132_BRE]] (ISS-CIR):**
   - Usa un quemador plano poroso de bronce alimentado con gas para igualar el **numero $B$ de Spalding** y estudiar solidos en estado estacionario sin consumir decenas de probetas.
3. **[[PSI-110_MSC]] (STS / Microgravedad):**
   - Mide combustion latente (*smoldering*) en espumas de poliuretano sin llama visible, documentando emision sostenida de $\text{CO}$ y su transicion violenta a llama abierta si entra ventilacion adicional.
4. **[[PSI-109_NCA]] (Canal Estrecho $1g$):**
   - Placas frias muy cercanas suprimen la conveccion natural en la Tierra para emular $0g$, validando ensayos economicos previos a la norma `NASA-STD-6001`.

---

## 2. Uso Directo en Entrenamiento ML/DL

- **Entrenamiento Local CPU (`backend/train_models.py`) y Google Colab:**
  - `BASS-II` es el conjunto de entrenamiento principal de **`flammability_rf.joblib`** (`RandomForestClassifier` que predice `Extinguished`) y **`burntime_gbr.joblib`** (`GradientBoostingRegressor` que predice `Burn Time` y tasa $V_f$).
  - Permite calcular **Feature Importance / SHAP** sin cajas negras (demostrando cuantitativamente cuanto pesa `Percent O2` frente a `Air Flow` o `Sample Thickness`).
- **Seguridad en FSM ([[M2_CNN_ONNX_DecisionTree_FSM]]):**
  - `MSC` entrena la rama del `DecisionTreeClassifier` que detecta **smoldering oculto** (`CO` elevado + aerosol submicrónico aun con `cnn_class == 0: Nominal`).
  - `BASS` justifica la **histeresis temporal** en `DeterministicFsmController` al pasar a `CONTENCION` (cierre de compuerta y apagado sostenido de ventilador).

---

## 3. Roles y Objetivos

- **Objetivos:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]], [[O4_Spinoffs_Terrestres_y_Forense]].
- **Dominios:** [[Rol_Combinado_Sinergia]] (`BASS`, `BASS-II`, `BRE`, `MSC`) y [[Rol_Gestion_Industrial]] (`NCA` reduccion de costo de certificacion).
