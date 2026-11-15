---
title: "Especificación Técnica del Modelo Multicriterio AHP / TOPSIS"
subtitle: "Derivación de Pesos Consistentes (Saaty) y Jerarquización Vectorial de las 24 Investigaciones NASA PSI"
project: "AERO-IGNIS SI — NASA Space Apps Challenge 2026"
track: "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"
author: "Equipo AERO-IGNIS SI — Área de Ingeniería de Gestión Industrial"
version: "1.0.0"
date: "2026-11-14"
status: "APPROVED"
classification: "Operations Research & Decision Engineering Specification"
tags: [nasa, psi, ahp, topsis, operations-research, o1, writing-craft, academic]
---

# Especificación Técnica del Modelo Multicriterio AHP / TOPSIS

## 1. Propósito, Alcance Operativo y Arquitectura

Esta especificación formaliza el motor de decisión multicriterio del **Objetivo 1 (`O1`)** en **AERO-IGNIS SI**. El modelo híbrido **AHP–TOPSIS** ordena de forma determinista y auditable las **24 investigaciones de combustión en microgravedad de NASA PSI** (`data/psi_combustion_24.json`) sin recurrir a modelos comerciales externos de pago (`C-02`) y operando exclusivamente sobre entornos presurizados habitables de tripulación y transferencia terrestre (`C-01`).

```
+---------------------------------------------------------------------------------------------------+
|                           PIPELINE HIBRIDO DE DECISION AHP + TOPSIS                               |
|                                                                                                   |
|   [1] Matrices AHP (Saaty 1-9)          [2] Matriz de Decision X (24 x 4)                         |
|   4 Perfiles de Uso Operativo           Criterios: habitat, modeling, sensors, spinoff            |
|   Validacion: CR < 0.10                             |                                             |
|               |                                     v                                             |
|               |                         [3] Normalizacion Vectorial L2 (r_ij)                     |
|               +-----------------------> [4] Ponderacion: v_ij = w_j * r_ij                        |
|                                                     |                                             |
|                                                     v                                             |
|                                         [5] Soluciones Ideales (A+ y A-)                          |
|                                             Distancias Euclidianas (S_i+, S_i-)                   |
|                                                     |                                             |
|                                                     v                                             |
|                                         [6] Cercania Relativa C_i in [0, 1]                       |
|                                             TopsisMultiCriteriaRanker.rank()                      |
|                                             API: POST /api/v1/psi/rank-and-interpret              |
+---------------------------------------------------------------------------------------------------+
```

En la implementación de software, este algoritmo reside en la clase `TopsisMultiCriteriaRanker` ([backend/ranking_nlp.py](../../backend/ranking_nlp.py)) y se expone a través del contrato REST `POST /api/v1/psi/rank-and-interpret` definido en `SPEC.md` (`CriteriaWeightsDto` con validación Pydantic `extra="forbid"` y rango `[0.0, 100.0]`).

---

## 2. Criterios de Decisión y Matriz Base ($24 \times 4$)

Cada investigación $A_i$ ($i = 1, \dots, 24$) se evalúa respecto a cuatro criterios de beneficio (a mayor puntuación, mayor prioridad operativa), normalizados originalmente en $[0.0, 1.0]$ en `data/psi_combustion_24.json`:

| Clave de Criterio | Nombre Operativo | Naturaleza | Significado Físico e Industrial |
| :--- | :--- | :--- | :--- |
| **`habitat`** ($C_1$) | Afinidad a Entornos Habitables | Beneficio ($\max$) | Aplicabilidad directa a cabinas presurizadas (`ISS`, `Cygnus`), atmósferas hipobáricas enriquecidas ($30\text{–}34\%\text{ O}_2$, $8.2\text{–}10.2\text{ psi}$) y toxicidad ECLSS. |
| **`modeling`** ($C_2$) | Rigor para Modelado Físico (`M1`) | Beneficio ($\max$) | Volumen y granularidad de variables experimentales continuas ($V_f$, $\% \text{O}_2$, presión, espesor, velocidad de flujo) útiles para calibrar modelos y ecuaciones ($\text{Da}$, $\text{Pe}$). |
| **`sensors`** ($C_3$) | Instrumentación y Detección (`M2`) | Beneficio ($\max$) | Capacidad diagnóstica en condiciones críticas: aerosoles submicrónicos ($<0.1\,\mu\text{m}$), cámaras UV $\text{OH}^*$ ($310\text{ nm}$) y sensores electroquímicos ($\text{CO}, \text{HF}, \text{HCl}$). |
| **`spinoff`** ($C_4$) | Transferencia Terrestre (`O4`) | Beneficio ($\max$) | Potencial de transferencia dual hacia normativas industriales (`NFPA`, `NASA-STD-6001`), protección de bomberos, centros de datos y minería subterránea. |

---

## 3. Derivación de Pesos mediante AHP (*Analytic Hierarchy Process*)

Para evitar ponderaciones arbitrarias, se emplea el **Proceso Analítico Jerárquico (AHP)** de Thomas L. Saaty con escala fundamental $1\text{–}9$. Dada una matriz recíproca de comparación por pares $\mathbf{M} = [m_{jk}]_{4 \times 4}$ donde $m_{kj} = 1 / m_{jk}$ y $m_{jj} = 1$, el vector propio de prioridades normalizado $\mathbf{w} = [w_1, w_2, w_3, w_4]^T$ satisface:

$$\mathbf{M} \mathbf{w} = \lambda_{\max} \mathbf{w}, \qquad \sum_{j=1}^{4} w_j = 1, \quad w_j > 0$$

La coherencia lógica de los juicios pareados se audita mediante el **Índice de Consistencia ($\text{CI}$)** y la **Razón de Consistencia ($\text{CR}$)** utilizando el índice aleatorio de Saaty para $n = 4$ ($\text{RI}_4 = 0.90$):

$$\text{CI} = \frac{\lambda_{\max} - n}{n - 1}, \qquad \text{CR} = \frac{\text{CI}}{\text{RI}_4} < 0.10$$

### 3.1 Perfiles de Ponderación Calibrados y Consistentes

#### Perfil A — Seguridad en Hábitats de Tripulación (`Habitat Safety`)
Prioriza experimentos a escala de cabina real y condiciones hipobáricas lunares tipo Artemis.

$$\mathbf{M}_{\text{hab}} = \begin{pmatrix}
1 & 3 & 4 & 5 \\
1/3 & 1 & 2 & 3 \\
1/4 & 1/2 & 1 & 2 \\
1/5 & 1/3 & 1/2 & 1
\end{pmatrix}$$

* **Vector de pesos ($\mathbf{w}_{\text{hab}}$):** `habitat = 0.5462`, `modeling = 0.2323`, `sensors = 0.1377`, `spinoff = 0.0838`
* **Auditoría de consistencia:** $\lambda_{\max} = 4.0511$, $\text{CI} = 0.0170$, **$\text{CR} = 0.0189 < 0.10$ (Consistente)**.

#### Perfil B — Modelado Físico y Simulación (`Physical Modeling`)
Prioriza conjuntos de datos densos para calibración de `RandomForest`, `GradientBoostingRegressor` y números adimensionales ($\text{Da}, \text{Pe}$).

$$\mathbf{M}_{\text{mod}} = \begin{pmatrix}
1 & 1/3 & 2 & 3 \\
3 & 1 & 4 & 5 \\
1/2 & 1/4 & 1 & 2 \\
1/3 & 1/5 & 1/2 & 1
\end{pmatrix}$$

* **Vector de pesos ($\mathbf{w}_{\text{mod}}$):** `habitat = 0.2323`, `modeling = 0.5462`, `sensors = 0.1377`, `spinoff = 0.0838`
* **Auditoría de consistencia:** $\lambda_{\max} = 4.0511$, $\text{CI} = 0.0170$, **$\text{CR} = 0.0189 < 0.10$ (Consistente)**.

#### Perfil C — Detección Temprana e Instrumentación (`Early Sensors`)
Prioriza investigaciones de llamas frías invisibles ($500\text{–}800\text{ K}$), pirólisis latente y partículas submicrónicas para el gemelo digital (`M2`).

$$\mathbf{M}_{\text{sen}} = \begin{pmatrix}
1 & 2 & 1/3 & 2 \\
1/2 & 1 & 1/4 & 1 \\
3 & 4 & 1 & 3 \\
1/2 & 1 & 1/3 & 1
\end{pmatrix}$$

* **Vector de pesos ($\mathbf{w}_{\text{sen}}$):** `habitat = 0.2257`, `modeling = 0.1235`, `sensors = 0.5166`, `spinoff = 0.1341`
* **Auditoría de consistencia:** $\lambda_{\max} = 4.0458$, $\text{CI} = 0.0153$, **$\text{CR} = 0.0170 < 0.10$ (Consistente)**.

#### Perfil D — Transferencia Dual-Use y Normativa Industrial (`Dual-Use Spinoffs`)
Prioriza estudios con impacto directo en equipamiento terrestre, detección industrial temprana y supresión sin residuos.

$$\mathbf{M}_{\text{spi}} = \begin{pmatrix}
1 & 2 & 1 & 1/3 \\
1/2 & 1 & 1/2 & 1/4 \\
1 & 2 & 1 & 1/3 \\
3 & 4 & 3 & 1
\end{pmatrix}$$

* **Vector de pesos ($\mathbf{w}_{\text{spi}}$):** `habitat = 0.1894`, `modeling = 0.1054`, `sensors = 0.1894`, `spinoff = 0.5158`
* **Auditoría de consistencia:** $\lambda_{\max} = 4.0206$, $\text{CI} = 0.0069$, **$\text{CR} = 0.0076 < 0.10$ (Consistente)**.

---

## 4. Formulación Matemática del Algoritmo TOPSIS

Dado un vector de pesos arbitrario ingresado por el usuario en la API o derivado por AHP, `TopsisMultiCriteriaRanker` ejecuta seis etapas vectoriales deterministas:

1. **Normalización de pesos del usuario ($\tilde{w}_j$):**
   Para cualquier entrada no negativa con al menos un componente positivo ($\sum_j \max(0, w_j^{\text{raw}}) > 0$):
   $$\tilde{w}_j = \frac{\max(0, w_j^{\text{raw}})}{\sum_{k=1}^{4} \max(0, w_k^{\text{raw}})}$$
   Esta propiedad garantiza invariancia exacta ante escalado positivo (por ejemplo, `{60, 20, 10, 10}` y `{0.6, 0.2, 0.1, 0.1}` producen puntuaciones idénticas). Si todos los pesos son $\le 0$, el método lanza `ValueError`.

2. **Construcción y normalización euclidiana ($L_2$) de la matriz de decisión $\mathbf{X} = [x_{ij}]_{24 \times 4}$:**
   $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{24} x_{ij}^2}}, \qquad i = 1,\dots,24; \; j = 1,\dots,4$$

3. **Matriz de decisión normalizada ponderada:**
   $$v_{ij} = \tilde{w}_j \cdot r_{ij}$$

4. **Determinación de las soluciones ideal positiva ($A^+$) y anti-ideal ($A^-$):**
   Dado que los cuatro criterios son de beneficio:
   $$A^+ = \left\{ \max_i v_{ij} \;\middle|\; j \in \{1..4\} \right\}, \qquad A^- = \left\{ \min_i v_{ij} \;\middle|\; j \in \{1..4\} \right\}$$

5. **Cálculo de las distancias euclidianas ($S_i^+$ y $S_i^-$):**
   $$S_i^+ = \sqrt{\sum_{j=1}^{4} (v_{ij} - v_j^+)^2}, \qquad S_i^- = \sqrt{\sum_{j=1}^{4} (v_{ij} - v_j^-)^2}$$

6. **Coeficiente de cercanía relativa a la solución ideal ($C_i$):**
   $$C_i = \begin{cases} \dfrac{S_i^-}{S_i^+ + S_i^-}, & \text{si } S_i^+ + S_i^- > 0 \\ 0.5, & \text{si } S_i^+ + S_i^- = 0 \end{cases}$$
   Se cumple estrictamente $0 \le C_i \le 1$. Las investigaciones se ordenan de forma descendente por $C_i$, resolviendo cualquier empate matemático de manera determinista por orden lexicográfico ascendente de `psi_id`.

---

## 5. Análisis de Sensibilidad Empírico sobre las 24 PSI

Al ejecutar `TopsisMultiCriteriaRanker` sobre `data/psi_combustion_24.json` con los cuatro vectores AHP certificados ($\text{CR} < 0.02$), se verifican desplazamientos físicos coherentes en los primeros cinco puestos:

| Puesto | Perfil A: `Habitat Safety` | Perfil B: `Physical Modeling` | Perfil C: `Early Sensors` | Perfil D: `Dual-Use Spinoffs` |
| :---: | :--- | :--- | :--- | :--- |
| **#1** | **`PSI-104` SAFFIRE-V** ($C_i = 0.9001$) | **`PSI-25` BASS-II** ($C_i = 0.8018$) | **`PSI-110` MSC** ($C_i = 0.8796$) | **`PSI-129` SPICE** ($C_i = 0.8868$) |
| **#2** | `PSI-103` SAFFIRE-IV ($C_i = 0.8817$) | `PSI-24` FLEX ($C_i = 0.7260$) | `PSI-129` SPICE ($C_i = 0.8654$) | `PSI-110` MSC ($C_i = 0.8707$) |
| **#3** | `PSI-105` SAFFIRE-VI ($C_i = 0.8691$) | `PSI-104` SAFFIRE-V ($C_i = 0.7036$) | `PSI-105` SAFFIRE-VI ($C_i = 0.8593$) | `PSI-105` SAFFIRE-VI ($C_i = 0.7933$) |
| **#4** | `PSI-110` MSC ($C_i = 0.8509$) | `PSI-26` BASS ($C_i = 0.6918$) | `PSI-24` FLEX ($C_i = 0.7866$) | `PSI-154` ACME-E-FIELD ($C_i = 0.6601$) |
| **#5** | `PSI-98` SAFFIRE-I ($C_i = 0.8463$) | `PSI-132` BRE ($C_i = 0.6714$) | `PSI-103` SAFFIRE-IV ($C_i = 0.7551$) | `PSI-104` SAFFIRE-V ($C_i = 0.6473$) |

### Interpretación Técnica de la Sensibilidad

1. **Bajo prioridad de hábitat (`Perfil A`):** Emergen en las tres primeras posiciones las campañas **Saffire V, IV y VI** (`10.60555/psi-104`, `10.60555/psi-103`, `10.60555/psi-105`), únicas investigaciones ejecutadas a escala de módulo real Cygnus bajo atmósferas enriquecidas ($30\text{–}34\%\text{ O}_2$) y presiones lunares reducidas ($8.2\text{–}10.2\text{ psi}$).
2. **Bajo prioridad de modelado (`Perfil B`):** Lidera **`PSI-25` (`BASS-II`, `10.60555/psi-25`)**, que aporta la matriz experimental de $17$ columnas y $>130$ corridas necesaria para calibrar los límites radiativos y de soplado del predictor `M1`, seguido de **`PSI-24` (`FLEX`, `10.60555/psi-24`)**.
3. **Bajo prioridad sensorial (`Perfil C`):** Encabezan **`PSI-110` (`MSC`, `10.60555/psi-110`)**, enfocada en detección de $\text{CO}$ durante combustión latente sin llama, y **`PSI-129` (`SPICE`, `10.60555/psi-129`)**, base empírica para la detección de aerosoles submicrónicos ($<0.1\,\mu\text{m}$).
4. **Bajo transferencia terrestre (`Perfil D`):** Lidera **`PSI-129` (`SPICE`)** por su vínculo directo con el discriminador de partículas del *Spinoff Node 9407*, seguida de **`PSI-110` (`MSC`)**, **`PSI-105` (`SAFFIRE-VI`)** y **`PSI-154` (`ACME-E-FIELD`, `10.60555/psi-154`)** sobre supresión electrodinámica sin residuos químicos.

---

## 6. Verificación TDD y Requisitos de Rendimiento

La verificación del modelo se ejecuta en `tests/unit/test_ranking_and_writing_unit.py` e incluye las siguientes aserciones verificables sin red externa:

* **`test_topsis_determinism_and_latency`:** Garantiza latencia de ordenamiento completa $< 50.0\text{ ms}$ (presupuesto de `SPEC.md`) y determinismo idempotente entre ejecuciones repetidas.
* **`test_topsis_scale_invariance_and_edge_cases`:** Valida manejo seguro de listas vacías (`[]`), rechazo mediante `ValueError` de pesos nulos/negativos, acotamiento $C_i \in [0.0, 1.0]$ e invariancia exacta ante escalado positivo de pesos.
* **`test_topsis_ahp_profiles_sensitivity_and_consistency`:** Verifica que los cuatro vectores AHP consistentes ($\text{CR} < 0.10$) reproducen exactamente los líderes esperados (`PSI-104`, `PSI-25`, `PSI-110`, `PSI-129`).

Este documento cierra formalmente el hito **`I-02`** del perfil de Ingeniería de Gestión Industrial y sienta la base cuantitativa para las plantillas interpretativas de **`I-08`** (`writing-craft` sobre salidas TOPSIS).
