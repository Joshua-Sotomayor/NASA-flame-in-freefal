---
title: "Fichas Forenses Parametrizadas: Apollo 1, Apollo 13, Mir y Hábitat Lunar Artemis"
subtitle: "Especificación Técnica de Presets de Simulación en 1 Clic, Análisis Adimensional y Lecciones Normativas"
project: "AERO-IGNIS SI — NASA Space Apps Challenge 2026"
track: "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"
author: "Equipo AERO-IGNIS SI — Área de Ingeniería de Gestión Industrial"
version: "1.0.0"
date: "2026-11-14"
status: "APPROVED"
classification: "Forensic Case Engineering & Simulation Presets"
tags: [nasa, apollo-1, apollo-13, mir, artemis, forensic, nasa-std-6001, writing-craft, academic]
---

# Fichas Forenses Parametrizadas y Escenarios de Sensibilidad

## 1. Propósito, Alcance Operativo y Mapeo al Simulador

Esta especificación parametriza las condiciones atmosféricas, termofísicas y de ingeniería de materiales de los tres incidentes históricos oficiales de incendio espacial —**Apollo 1 (1967)**, **Apollo 13 (1970)** y **Estación Mir Kvant-1 (1997)**— junto con el escenario de referencia de exploración **Hábitat Lunar Artemis** ($34\%\text{ O}_2, 8.2\text{ psi}$).

Estos cuatro registros constituyen la sección `forensic_cases` de [cases_and_spinoffs.json](../../data/cases_and_spinoffs.json), alimentan los botones de carga en 1 clic del simulador de inflamabilidad (`POST /api/v1/sandbox/predict-flammability`) y cumplen estrictamente la restricción de dominio habitable (`C-01`, excluyendo motores cohete) y la directiva de costo nulo (`C-02`).

```
+---------------------------------------------------------------------------------------------------+
|                   ARQUITECTURA DE PARAMETRIZACION FORENSE (data/cases_and_spinoffs.json)          |
|                                                                                                   |
|  [Preset 1-Clic] ---> [AtmosphericState (@dataclass frozen)] ---> [DimensionlessPhysicsCalculator] |
|   - apollo_1           - Validacion rangos SPEC.md                 - Damkohler (Da), Peclet (Pe)   |
|   - apollo_13          - Mapeo simulator_material                  - Prior fisico monotono %O2     |
|   - mir_1997             (PTFE / SIBAL)                                     |                     |
|   - lunar_artemis                                                           v                     |
|         |                                                         [FlammabilityPredictor (RF+GBR)]|
|         +---> [flag auto_oxidizing] ---> [GovernanceAndSpinoffService]                            |
|                (true solo en Mir 1997)    - Exige niebla fina PFE (20-100 um)                     |
+---------------------------------------------------------------------------------------------------+
```

### 1.1 Reglas de Acotamiento en `AtmosphericState` (`SPEC.md`)

Para prevenir extrapolaciones fuera del dominio habitable presurizado, la clase inmutable `AtmosphericState` ([backend/physics_ml.py](../../backend/physics_ml.py)) impone límites estrictos:
* Concentración de oxígeno: $10.0\% \le \% \text{O}_2 \le 100.0\%$.
* Presión total de cabina: $1.0\text{ psi} \le P \le 30.0\text{ psi}$.
* Flujo convectivo forzado: $0.0\text{ cm/s} \le u_\infty \le 60.0\text{ cm/s}$.
* Gravedad discreta verificada: $g \in \{0.0, 0.16, 0.38, 1.0\}\text{ g}_0$.
* Material de entrada al regresor/clasificador (`simulator_material`): `Algodon` ($1.35$), `PMMA` ($1.15$), `SIBAL` ($1.05$), `Nomex` ($0.42$), `Kapton` ($0.35$) o `PTFE` ($0.25$).

---

## 2. Tabla Consolidada de Parámetros de Entrada y Resultados Empíricos

La siguiente matriz reúne los parámetros exactos almacenados en `data/cases_and_spinoffs.json` y las salidas verificadas directamente mediante `FlammabilityPredictor` (`flammability_rf.joblib` + `burntime_gbr.joblib` + `DimensionlessPhysicsCalculator`):

| ID Caso | Evento Histórico / Referencia | $\% \text{O}_2$ | Presión Simulador | Flujo / Dir. | Gravedad | Material Descriptivo (`simulator_material`) | Espesor | $\text{Da}$ | $\text{Pe}$ | Régimen Clasificado | $P_{\text{ext}}$ | $V_f$ ($\text{mm/s}$) | $t_{\text{comb}}$ ($\text{s}$) | Auto-Oxidante |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **`apollo_1`** | **Apollo 1** (27 Ene 1967) | $100.0\%$ | $16.7\text{ psi}$ | $5.0\text{ cm/s}$ · `concurrent` | $1.0\text{ g}$ | `PTFE / Espuma y Velcro` (`PTFE`) | $2.0\text{ mm}$ | `2.4127` | `18.8889` | `Propagación Acelerada` | `5.46%` | `19.949` | `31.02` | `false` |
| **`apollo_13`** | **Apollo 13** (13 Abr 1970) | $100.0\%$ | $30.0\text{ psi}^*$ | $2.0\text{ cm/s}$ · `opposed` | $0.0\text{ g}$ | `PTFE` (`PTFE`) | $1.2\text{ mm}$ | `14.5471` | `1.3333` | `Propagación Acelerada` | `2.11%` | `19.167` | `14.87` | `false` |
| **`mir_1997`** | **Mir Kvant-1** (23 Feb 1997) | $21.0\%$ | $14.7\text{ psi}$ | $12.0\text{ cm/s}$ · `concurrent` | $0.0\text{ g}$ | `Cartucho SFOG Vika (LiClO4)` (`SIBAL`) | $5.0\text{ mm}$ | `0.4922` | `33.3333` | `Extinción Radiativa (Quenching)`$^{**}$ | `38.27%` | `2.000` | `103.68` | **`true`** |
| **`lunar_artemis`** | **Hábitat Lunar Artemis** | $34.0\%$ | $8.2\text{ psi}$ | $12.0\text{ cm/s}$ · `concurrent` | $0.16\text{ g}$ | `SIBAL` (`SIBAL`) | $0.8\text{ mm}$ | `0.6842` | `6.8120` | `Propagación Acelerada` | `0.02%` | `9.182` | `12.90` | `false` |

> $^*$ **Acotamiento de presión en `apollo_13`:** El tanque criogénico real No. 2 operó a $\sim 1,000\text{ psi}$ ($\sim 6.89\text{ MPa}$); el simulador acota la entrada a $30.0\text{ psi}$ por contrato de cabina habitable en `SPEC.md` preservando la nota histórica en `pressure_note`.  
> $^{**}$ **Advertencia de oxidante interno en `mir_1997`:** Un modelo puramente atmosférico predice `Quenching` a $21\%\text{ O}_2$; sin embargo, la bandera `auto_oxidizing = true` activa en gobernanza el protocolo obligatorio `PFE` al reconocer generación interna de $\text{O}_2$ por $\text{LiClO}_4$.

### 2.1 Importancia Relativa de Variables (`RandomForestClassifier.feature_importances_`)

El predictor tabular expone en cada consulta la ponderación normalizada de las variables aprendidas sobre `data/bass_saffire_runs.csv` ($566$ corridas experimentales). Las tres variables dominantes concentran el **$82.23\%$** de la capacidad discriminativa:

1. **Concentración $\text{O}_2$ ($\%$):** `0.4325` ($43.25\%$)
2. **Reactividad del Material:** `0.2118` ($21.18\%$)
3. **Espesor de Muestra ($\text{cm}$):** `0.1780` ($17.80\%$)

---

## 3. Fichas Forenses Detalladas e Integración PSI

### 3.1 Ficha Forense 1 — Apollo 1 (27 de enero de 1967)
* **Parámetros Verificados:** $100.0\%\text{ O}_2$ puro, presión de prueba en plataforma $16.7\text{ psi}$ ($115.1\text{ kPa}$), flujo convectivo $5.0\text{ cm/s}$, gravedad terrestre $1.0\text{ g}$, aislamiento `PTFE` / espumas y cierres de Velcro ($2.0\text{ mm}$).
* **Mecanismo de Falla:** Un arco eléctrico en cableado recubierto de `PTFE` bajo atmósfera de oxígeno puro provocó la ignición de $>3.1\text{ m}^2$ de materiales poliméricos en cabina, escalando la presión interna de $16.7\text{ psi}$ a $29\text{ psi}$ en $15\text{ s}$ hasta la ruptura del casco.
* **Comportamiento en Simulador:** Con `PTFE` (`reactividad = 0.25`) en condiciones normales de aire la inflamabilidad sería baja; sin embargo, el término hiperóxico $(100 / 21)^{2.1}$ eleva $\text{Da} = 2.4127$ y acelera el frente de llama a $19.949\text{ mm/s}$ con probabilidad de extinción de solo $5.46\%$.
* **Investigaciones PSI Vinculadas:** `PSI-104` (`10.60555/psi-104`), `PSI-109` (`10.60555/psi-109`), `PSI-25` (`10.60555/psi-25`).
* **Legado Normativo y Dual-Use:** Establecimiento de `NHB 8060.1` / **`NASA-STD-6001`**, adopción de atmósfera $60\%\text{ O}_2 / 40\%\text{ N}_2$ durante el lanzamiento, escotilla de apertura rápida ($5\text{ s}$) y reemplazo de tejidos inflamables por fibras **`PBI`** (*Spinoff Node 9918*).

### 3.2 Ficha Forense 2 — Apollo 13 (13 de abril de 1970)
* **Parámetros Verificados:** $100.0\%\text{ O}_2$, presión real de tanque $\sim 1,000\text{ psi}$ (modelada a la cota superior de cabina $30.0\text{ psi}$), flujo opuesto $2.0\text{ cm/s}$, microgravedad $0.0\text{ g}$, aislamiento `PTFE` ($1.2\text{ mm}$).
* **Mecanismo de Falla:** Durante pruebas previas en tierra con alimentación de $65\text{ V}$ sobre interruptores termostáticos diseñados para $28\text{ V}$, los contactos se soldaron cerrados y sometieron el aislamiento de teflón (`PTFE`) a temperaturas $>500\,^\circ\text{C}$. Al energizar el ventilador en vuelo en oxígeno supercrítico, el `PTFE` degradado ardió violentamente provocando la ruptura del tanque de oxígeno No. 2.
* **Comportamiento en Simulador:** Registra el número de Damköhler más alto de los cuatro escenarios ($\text{Da} = 14.5471$) debido a la combinación de flujo convectivo mínimo ($2.0\text{ cm/s}$), $100\%\text{ O}_2$ y presión elevada ($30.0\text{ psi}$), produciendo una probabilidad de extinción de $2.11\%$.
* **Investigaciones PSI Vinculadas:** `PSI-138` (`10.60555/psi-138`), `PSI-25` (`10.60555/psi-25`), `PSI-105` (`10.60555/psi-105`).
* **Legado de Ingeniería:** Demuestra que polímeros clasificados como auto-extinguibles en aire normobárico ($21\%\text{ O}_2$) pierden su margen de seguridad cuando sufren daño térmico previo en atmósferas hiperóxicas o presurizadas (fila `FM-01` en la matriz FMEA).

### 3.3 Ficha Forense 3 — Estación Mir, Módulo Kvant-1 (23 de febrero de 1997)
* **Parámetros Verificados:** Atmósfera nominal de cabina $21.0\%\text{ O}_2$, $14.7\text{ psi}$ ($101.3\text{ kPa}$), ventilación $12.0\text{ cm/s}$ en microgravedad $0.0\text{ g}$, cartucho generador sólido de oxígeno `SFOG Vika` ($\text{LiClO}_4$ + polvo de hierro, espesor equivalente $5.0\text{ mm}$).
* **Mecanismo de Falla:** Contaminación orgánica en un cartucho de perclorato de litio desencadenó una reacción exotérmica auto-oxidante tipo soplete de $1.5\text{ m}$ de longitud sostenida durante $14\text{ minutos}$ con emisión densa de humo en cabina.
* **Comportamiento en Simulador y Regla de Gobernanza:** Evaluado como textil convencional (`SIBAL`) a $21\%\text{ O}_2$, `FlammabilityPredictor` estima un régimen conservador (`Extinción Radiativa`, $P_{\text{ext}} = 38.27\%$). Sin embargo, la propiedad `auto_oxidizing: true` advierte explícitamente que **cortar el flujo HVAC no apaga reacciones químicas generadoras de oxígeno**. En consecuencia, `GovernanceAndSpinoffService` impone la descarga inmediata de niebla de agua fina **`ISS PFE`** ($20\text{–}100\,\mu\text{m}$, calor latente $2,260\text{ kJ/kg}$) y mascarillas respiratorias autónomas para la tripulación (fila `FM-05` en FMEA).
* **Investigaciones PSI Vinculadas:** `PSI-105` (`10.60555/psi-105`), `PSI-110` (`10.60555/psi-110`), `PSI-27` (`10.60555/psi-27`).

### 3.4 Ficha Forense / Referencia 4 — Hábitat Lunar Artemis ($34\%\text{ O}_2, 8.2\text{ psi}$)
* **Parámetros Verificados:** Atmósfera de exploración hipobárica enriquecida a $34.0\%\text{ O}_2$ y $8.2\text{ psi}$ ($56.5\text{ kPa}$), gravedad lunar $0.16\text{ g}$, flujo $12.0\text{ cm/s}$ concurrente sobre tejido `SIBAL` ($0.8\text{ mm}$).
* **Justificación Operativa:** Reduce el tiempo de pre-respiración requerido para actividades extravehiculares (EVA) previniendo la enfermedad por descompresión, pero incrementa sustancialmente la velocidad de propagación frente al aire estándar de la ISS ($21\%\text{ O}_2, 14.7\text{ psi}$).
* **Comportamiento en Simulador:** Con una fracción de oxígeno de $34\%$ y espesor delgado ($0.8\text{ mm}$), el modelo clasifica el escenario como `Propagación Acelerada`, con probabilidad de extinción cercana a cero ($0.02\%$) y velocidad de frente de $9.182\text{ mm/s}$.
* **Investigaciones PSI Vinculadas:** Validación experimental directa a escala de vehículo en `PSI-103` (`SAFFIRE-IV`, `10.60555/psi-103`), `PSI-104` (`SAFFIRE-V`, `10.60555/psi-104`) y correlación de sólidos en `PSI-25` (`BASS-II`, `10.60555/psi-25`).

---

## 4. Verificación Automatizada

El cumplimiento de los parámetros físicos, la compatibilidad del campo `simulator_material` con `AtmosphericState`, la vinculación con IDs PSI reales y el disparo del protocolo `PFE` para el caso auto-oxidante `mir_1997` se validan mediante las pruebas unitarias en [test_physics_unit.py](../../tests/unit/test_physics_unit.py) y [test_forensic_presets_unit.py](../../tests/unit/test_forensic_presets_unit.py), además de las pruebas de integración en [test_flammability_int.py](../../tests/integration/test_flammability_int.py).

Este documento formaliza la entrega del hito **`I-05`** y sirve de enlace directo hacia la especificación del protocolo de supresión **`I-06`** (`PFE` vs $\text{CO}_2$ vs `E-FIELD`).
