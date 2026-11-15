---
title: "Matriz de Análisis de Modos de Falla y Efectos (FMEA / AMFE) — NASA-STD-6001"
subtitle: "Evaluación Cuantitativa de Riesgos de Combustión en Cabinas Habitables y Mitigación mediante Control e Inteligencia Propia"
project: "AERO-IGNIS SI — NASA Space Apps Challenge 2026"
track: "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"
author: "Equipo AERO-IGNIS SI — Área de Ingeniería de Gestión Industrial"
version: "1.0.0"
date: "2026-11-14"
status: "APPROVED"
classification: "Aerospace Industrial Safety & Risk Governance"
tags: [nasa, fmea, amfe, nasa-std-6001, eclss, o4, writing-craft, academic]
---

# Matriz FMEA / AMFE Basada en `NASA-STD-6001`

## 1. Marco Normativo, Alcance y Metodología de Evaluación

El estándar técnico **`NASA-STD-6001`** (evolución directa de la especificación `NHB 8060.1`, instituida tras la investigación del incendio del **Apollo 1** en 1967) establece los requisitos de inflamabilidad, desgasificación (*offgassing*) y compatibilidad térmica para materiales expuestos a atmósferas que soportan combustión en naves tripuladas y hábitats presurizados.

En **AERO-IGNIS SI**, el módulo de gobernanza `GovernanceAndSpinoffService` ([backend/governance.py](../../backend/governance.py)) implementa un modelo determinista de **Análisis de Modos de Falla y Efectos (FMEA / AMFE)** sobre los datos auditables de `data/cases_and_spinoffs.json`, cumpliendo estrictamente la restricción de dominio habitable (`C-01`, excluyendo motores cohete) y la directiva de costo nulo (`C-02`).

### 1.1 Fórmula del Número de Prioridad de Riesgo ($\text{NPR}$)

Cada modo de falla $k \in \{\text{FM-01}, \dots, \text{FM-06}\}$ se cuantifica mediante el producto de tres factores ordinales acotados en el rango entero $[1, 10]$:

$$\text{NPR}_k = S_k \times O_k \times D_k \in [1, 1000]$$

donde:
* **Severidad ($S \in [1, 10]$):** Gravedad del efecto sobre la integridad de la tripulación, la atmósfera del sistema de soporte vital (**ECLSS**) y la estructura presurizada ($10$ indica riesgo catastrófico o toxicidad aguda por fluoruros/monóxido de carbono).
* **Ocurrencia ($O \in [1, 10]$):** Probabilidad de aparición del mecanismo iniciador bajo condiciones de microgravedad o atmósferas enriquecidas ($\ge 30\%\text{ O}_2$).
* **Detección ($D \in [1, 10]$):** Dificultad de interceptación temprana antes de la propagación térmica ($10$ representa fenómenos ópticamente invisibles como llamas frías NTC o pirólisis latente sin luz).

La eficacia de la arquitectura de control de **AERO-IGNIS SI** se mide mediante la tasa porcentual de reducción del riesgo agregado:

$$\Delta \text{NPR}_{\%} = \frac{\sum_{k=1}^{6} \text{NPR}_{k,\text{base}} - \sum_{k=1}^{6} \text{NPR}_{k,\text{mitigado}}}{\sum_{k=1}^{6} \text{NPR}_{k,\text{base}}} \times 100\%$$

---

## 2. Matriz Maestra FMEA / AMFE (Línea Base vs. Sistema Mitigado)

```
+---------------------------------------------------------------------------------------------------+
|                       FLUJO DE MITIGACION FMEA EN AERO-IGNIS SI (NASA-STD-6001)                   |
|                                                                                                   |
|  [Riesgo Sin Mitigar: NPR = 1,901]                                                                |
|   |-- FM-04: Smoldering espuma MSC (NPR 432) ----+                                                |
|   |-- FM-03: Llama fria NTC invisible (NPR 405) -+--> [Capas de Defensa AERO-IGNIS SI]            |
|   |-- FM-01: Pirolisis PTFE >500 C (NPR 350) ----+     1. Aerosoles <0.1 um (Spinoff 9407 / SPICE)|
|   |-- FM-02: Flujo bajo BASS <3 cm/s (NPR 288) --+     2. CNN ONNX (flame_cnn.onnx) + Tree        |
|   |-- FM-06: Perdida enlace UART (NPR 216) ------+     3. FSM + Histeresis + Interlock EPLAN      |
|   +-- FM-05: Cartucho Vika LiClO4 (NPR 210) -----+     4. Supresion PFE (niebla 20-100 um)        |
|                                                               |                                   |
|                                                               v                                   |
|                                              [Riesgo Mitigado: NPR = 134 (-92.95%)]               |
+---------------------------------------------------------------------------------------------------+
```

### 2.1 Tabla Consolidada de Modos de Falla Críticos

| ID | Subsistema / Escenario | Modo de Falla | Efecto en Cabina / ECLSS | Base ($S \times O \times D$) | $\text{NPR}_{\text{base}}$ | Acción Mitigadora Integrada en AERO-IGNIS SI | Mitigado ($S' \times O' \times D'$) | $\text{NPR}_{\text{mit}}$ | Reducción | Evidencia PSI |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **`FM-01`** | Arnés eléctrico en cabina enriquecida ($\ge 30\%\text{ O}_2$) | Sobrecarga y pirólisis de aislamiento PTFE ($>500\,^\circ\text{C}$) | Ignición rápida y liberación de fluoruros tóxicos ($\text{HF}$) en ECLSS | $10 \times 5 \times 7$ | **350** | Detección submicrónica $<0.1\,\mu\text{m}$ (*Spinoff 9407* / `SPICE`), corte por interlock EPLAN y aislamiento `PBI/Kapton` calificado `NASA-STD-6001` | $8 \times 2 \times 2$ | **32** | $-90.86\%$ | `PSI-129` (`10.60555/psi-129`) |
| **`FM-02`** | Ducto HVAC / Flujo bajo en microgravedad (`BASS`) | Ventilación estancada ($<3\text{ cm/s}$) sosteniendo llama esférica a bajo $\% \text{O}_2$ | Reignición transitoria si el ventilador se reactiva sin monitoreo térmico | $8 \times 6 \times 6$ | **288** | Histéresis temporal en `DeterministicFsmController` y cierre completo de compuerta en estado `CONTENCION` | $6 \times 2 \times 2$ | **24** | $-91.67\%$ | `PSI-25` (`10.60555/psi-25`) |
| **`FM-03`** | Vapores orgánicos / Combustible líquido (`FLEX` / `CFI-G`) | Llama fría NTC invisible ($500\text{–}800\text{ K}$) tras extinción aparente | Falsa percepción de extinción seguida de transición eruptiva a llama caliente | $9 \times 5 \times 9$ | **405** | Clasificador `flame_cnn.onnx` entrenado en clase `Llama Fria NTC` + bloqueo de rearme automático hasta $\Delta T/\Delta t \le 0$ | $7 \times 2 \times 2$ | **28** | $-93.09\%$ | `PSI-24` (`10.60555/psi-24`) |
| **`FM-04`** | Aislamiento de espuma porosa en rack avio-electrónico (`MSC`) | Combustión latente (*smoldering*) prolongada sin luz visible | Acumulación mortal de $\text{CO}$ y transición súbita al abrir acceso de aire | $9 \times 6 \times 8$ | **432** | Árbol de decisión tabular ($\text{CO ppm} + \Delta T/\Delta t + \text{aerosol}$) forzando `PRE_ALERTA` y corte HVAC | $7 \times 2 \times 2$ | **28** | $-93.52\%$ | `PSI-110` (`10.60555/psi-110`) |
| **`FM-05`** | Generador sólido de oxígeno (`Vika` / $\text{LiClO}_4$) | Contaminación orgánica y reacción auto-oxidante tipo soplete | Inmunidad al corte de ventilación HVAC; riesgo de perforación estructural | $10 \times 3 \times 7$ | **210** | Activación directa de supresión por niebla fina `PFE` (calor latente $2,260\text{ kJ/kg}$) + máscara de tripulación | $8 \times 1 \times 2$ | **16** | $-92.38\%$ | `PSI-105` (`10.60555/psi-105`) |
| **`FM-06`** | Enlace serial supervisor Python $\leftrightarrow$ Controlador de ducto | Pérdida de comunicación UART / congelamiento de *watchdog* | Indisponibilidad de cierre automático de compuerta y ventilador | $9 \times 4 \times 6$ | **216** | Enclavamiento cableado EPLAN (*hardwired interlock*) llevando la FSM inmediatamente a `FALLA_SEGURA` cuando `comm_ok=False` | $6 \times 1 \times 1$ | **6** | $-97.22\%$ | `PSI-98` (`10.60555/psi-98`) |
| **Total** | **Sistema Integral AERO-IGNIS SI** | — | — | — | **1,901** | **Arquitectura multicapa física + ML/DL + Control Determinista** | — | **134** | **$-92.95\%$** | — |

---

## 3. Análisis Técnico de Prioridades y Trazabilidad Forense

### 3.1 Modos de Falla Dominantes sin Mitigación ($\text{NPR} > 300$)

1. **`FM-04` ($\text{NPR}_{\text{base}} = 432$):** Constituye el riesgo principal debido a la combinación de alta ocurrencia ($O=6$) y baja detectabilidad óptica ($D=8$). La combustión latente en espumas de poliuretano (`PSI-110 MSC`) libera monóxido de carbono sin firma luminosa visible en el espectro RGB. El árbol de decisión en `SensorDecisionTreeModel` reduce el factor de detección de $8$ a $2$ al monitorear `co_ppm` y partículas submicrónicas.
2. **`FM-03` ($\text{NPR}_{\text{base}} = 405$):** Las llamas frías con coeficiente negativo de temperatura (**NTC**, $500\text{–}800\text{ K}$) descubiertas en `PSI-24 FLEX` presentan el puntaje de detección más crítico ($D=9$). Un controlador convencional que solo evalúe luminosidad visible reabriría la ventilación prematuramente, reactivando la llama caliente. La inclusión de la clase `2: Llama Fria NTC` en `flame_cnn.onnx` junto al bloqueo térmico $\Delta T/\Delta t \le 0$ en `DeterministicFsmController` abate el $\text{NPR}$ en un $93.09\%$.
3. **`FM-01` ($\text{NPR}_{\text{base}} = 350$):** Refleja directamente las lecciones forenses de **Apollo 1** ($100\%\text{ O}_2, 16.7\text{ psi}$) y **Apollo 13** (sobretensión en calentadores de teflón). La transición de aislamiento PTFE hacia polímeros certificados bajo `NASA-STD-6001` (`PBI` / `Kapton`) combinada con detección de aerosoles $<0.1\,\mu\text{m}$ (*Spinoff Node 9407*) reduce el riesgo residual a $\text{NPR} = 32$.

### 3.2 Salvaguardas Críticas de Control (`FM-05` y `FM-06`)

* **Fuego Auto-Oxidante (`FM-05`, Caso Mir 1997):** Cuando el combustible aporta su propio oxígeno químico (cartucho de perclorato de litio $\text{LiClO}_4$), el corte de ventilación HVAC resulta ineficaz. Por diseño normativo, la matriz FMEA vincula este modo con el protocolo obligatorio de niebla de agua fina **`ISS PFE`** ($20\text{–}100\,\mu\text{m}$, calor latente de vaporización $2,260\text{ kJ/kg}$).
* **Falla Segura Cableada (`FM-06`):** Para eliminar la dependencia única del software supervisor, la pérdida de comunicación serial (`comm_ok=False`) dispara la transición incondicional a `FALLA_SEGURA` mediante el *interlock* cableado validado en el Hardware Blueprint (`EPLAN`), logrando la mayor reducción porcentual individual ($-97.22\%$, $\text{NPR}_{\text{mit}} = 6$).

---

## 4. Verificación Automatizada y Contrato API

La integridad numérica de esta matriz se verifica de forma continua mediante dos capas de pruebas:
* **Pruebas Unitarias TDD ([test_fmea_unit.py](../../tests/unit/test_fmea_unit.py)):** Validan límites enteros $[1, 10]$, exactitud exacta de los totales (`1,901` $\rightarrow$ `134`, reducción promedio `92.95%`), vinculación con IDs PSI válidos y ausencia total de términos fuera de alcance (`C-01`).
* **Contrato REST:** El endpoint `GET /api/v1/governance/fmea-and-spinoffs?mitigated={bool}` expone estos resultados en tiempo real hacia el módulo de Gobernanza y Spinoffs del dashboard web.

Este documento completa formalmente el hito **`I-04`** del perfil de Ingeniería de Gestión Industrial y habilita la parametrización histórica de **`I-05`** (*Fichas Forenses: Apollo 1, Apollo 13 y Mir*).
