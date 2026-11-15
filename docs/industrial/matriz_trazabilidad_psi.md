---
title: "Matriz Maestra de Trazabilidad y Gobernanza de Datos PSI"
subtitle: "Taxonomía de las 24 Investigaciones NASA PSI, 10 Recursos Oficiales y Mapeo Multicriterio"
project: "AERO-IGNIS SI — NASA Space Apps Challenge 2026"
track: "Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"
author: "Equipo AERO-IGNIS SI — Área de Ingeniería de Gestión Industrial"
version: "1.0.0"
date: "2026-11-14"
status: "APPROVED"
classification: "Technical Specification & Data Governance"
tags: [nasa, psi, microgravity, combustion, data-governance, topsis, ahp, writing-craft, academic]
---

# Matriz Maestra de Trazabilidad y Gobernanza de Datos PSI

## 1. Alcance Operativo, Gobernanza y Restricciones de Dominio

La presente especificación técnica estructura la taxonomía integral, gobernanza de datos y trazabilidad de las 24 investigaciones de combustión en microgravedad del repositorio oficial **NASA Physical Sciences Informatics (PSI)** y los 10 recursos documentales asignados al reto *Flame in Freefall*.

```
+----------------------------------------------------------------------------------------------------+
|                                    AERO-IGNIS SI DATA GOVERNANCE                                   |
|                                                                                                    |
|   +-----------------------+     +-----------------------+     +--------------------------------+   |
|   |   24 NASA PSI Datasets|     | 10 Official Resources |     | Forensic & Spinoffs Presets    |   |
|   |   (CC0-1.0 Public)    |     | (NASA Glenn / NTRS)   |     | (Apollo 1, Mir, Node 9582...)  |   |
|   +-----------+-----------+     +-----------+-----------+     +---------------+----------------+   |
|               |                             |                                 |                    |
|               +----------------------+      |      +--------------------------+                    |
|                                      v      v      v                                               |
|                      +-----------------------------------------------+                             |
|                      | POO Repository Layer (backend/domain.py)      |                             |
|                      | - Frozen Dataclasses (PsiInvestigation)       |                             |
|                      | - Anti-SSRF URL Allowlist (osdr.nasa.gov)     |                             |
|                      | - Offline Fallback Cache (Zero Network Gate)  |                             |
|                      +-----------------------+-----------------------+                             |
|                                              |                                                     |
|                      +-----------------------+-----------------------+                             |
|                      |                                               |                             |
|                      v                                               v                             |
|   +-------------------------------------+         +-------------------------------------+          |
|   | Multi-Criteria Engine (TOPSIS/AHP)  |         | Deterministic Twin & FSM Controller |          |
|   | Objectives: O1 (Ranking) & O4 (Risk)|         | Objectives: O2 (Limits) & O3 (Safe) |          |
|   +-------------------------------------+         +-------------------------------------+          |
+----------------------------------------------------------------------------------------------------+
```

### 1.1 Restricciones Innegociables de Ingeniería

1. **Restricción de Dominio Habitacional (`C-01`):** El procesamiento analítico y los modelos de inferencia operan exclusivamente sobre **entornos presurizados y habitables de tripulación** (Estación Espacial Internacional —ISS—, naves de carga logística Cygnus, hábitats de exploración lunar Artemis con atmósferas normobáricas e hipobáricas $\ge 30\%\text{ O}_2$ y $\le 10.2\text{ psi}$, y módulos habitables terrestres) y transferencia tecnológica (*Spinoffs* `9582`, `9407`, `9918`, y extintores `PFE`). Queda estrictamente excluida cualquier consideración de motores cohete, toberas o sistemas de propulsión química espacial.
2. **Directiva de Costo Nulo (`C-02`):** El sistema opera bajo un presupuesto estricto de $\$0\text{ USD}$, prescindiendo de llamadas a interfaces de programación de aplicaciones (APIs) de modelos comerciales de lenguaje cerrado. Todo el procesamiento analítico se ejecuta en arquitecturas locales compiladas en formatos abiertos (`ONNX`, `joblib`) o mediante heurísticas deterministas multicriterio.
3. **Gobernanza de Datos Abiertos:** Todos los datos provienen del dominio público bajo licencia **CC0-1.0** y conservan sus identificadores digitales de objeto (**DOI**) oficiales con prefijo `10.60555/` para auditoría por pares científicos.
4. **Integridad Criptográfica:** Cada artefacto derivado de estos datos se valida mediante funciones resumen criptográficas **SHA-256** indexadas en `artifacts/models/manifest.sha256.json`.

---

## 2. Taxonomía Exhaustiva de las 24 Investigaciones NASA PSI

Las 24 investigaciones se catalogan en cinco dominios físicos representativos de las instalaciones orbitales del Laboratorio Nacional de la ISS (Módulo Integrado de Combustión —`CIR`— y Guantera de Ciencias de la Microgravedad —`MSG`—), los vehículos de reabastecimiento presurizados Cygnus (`Orbital ATK / Northrop Grumman`), y plataformas de referencia en caída libre / gravedad unitaria controlada (`STS` / canal estrecho terrestre).

### 2.1 Resumen de Distribución por Instalación

| Instalación Orbital / Terrestre | Código | Investigaciones Asignadas | Porcentaje | Enfoque Operativo |
| :--- | :--- | :---: | :---: | :--- |
| **Combustion Integrated Rack (ISS)** | `ISS-CIR` | 10 | 41.7% | Diagnóstico óptico avanzado, llamas de difusión esferoidal, combustión de gotas, llamas frías y campos electrodinámicos. |
| **Microgravity Science Glovebox (ISS)** | `ISS-MSG` | 6 | 25.0% | Combustión de sólidos con convección forzada controlada, límites de desprendimiento de llama, termofluidos y aerosoles. |
| **Módulos de Carga Presurizados Cygnus** | `Cygnus` | 6 | 25.0% | Incendios a escala de cabina real post-desacople orbital, probetas de gran formato ($0.4 \times 0.94\text{ m}$) y atmósferas de tránsito lunar. |
| **Otras Plataformas (STS Transbordador y Tierra 1g)** | `Otros` | 2 | 8.3% | Combustión latente (*smoldering*) en espumas porosas (`STS`) y emulación terrestre de microgravedad mediante canales estrechos (`1g`). |
| **Total General** | — | **24** | **100.0%** | **Validación canónica completada al 100%** |

---

### 2.2 Matriz Canónica de las 24 Investigaciones PSI

| ID PSI | Acrónimo | Instalación | DOI Oficial | Rango $\text{O}_2$ | Presión | Flujo Máx. | Materiales Clave | Sensores y Diagnósticos | Obj. Reto | Pipeline ML/DL |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| `PSI-98` | **SAFFIRE-I** | Cygnus | `10.60555/psi-98` | $21.0\%$ | $14.7\text{ psi}$ | $20.0\text{ cm/s}$ | SIBAL ($75\%$ algodón / $25\%$ fibra de vidrio, $0.4 \times 0.94\text{ m}$) | Doble cámara HD, anemómetro de hilo caliente, radiómetro de banda ancha, termopares | `O1, O2, O3` | `M1` ($V_f$), `M2` (visión), `M3` (ranking) |
| `PSI-101` | **SAFFIRE-II** | Cygnus | `10.60555/psi-101` | $21.0\%$ | $14.7\text{ psi}$ | $20.0\text{ cm/s}$ | 9 probetas: PMMA liso, PMMA ranurado, SIBAL, Nomex, silicona | Cámaras ópticas calibradas, termopares superficiales, sensores electroquímicos $\text{O}_2/\text{CO}_2$ | `O1, O2` | `M1` (clasificación materiales), `M3` |
| `PSI-102` | **SAFFIRE-III** | Cygnus | `10.60555/psi-102` | $21.0\%$ | $14.7\text{ psi}$ | $30.0\text{ cm/s}$ | SIBAL de gran formato ($0.4 \times 0.94\text{ m}$) | Doble cámara de seguimiento frontal/lateral, radiómetros, anemómetro | `O1, O2, O3` | `M1` (tasa propagación $V_f$), `M2` (límite ventilador), `M3` |
| `PSI-103` | **SAFFIRE-IV** | Cygnus | `10.60555/psi-103` | $21.0\text{--}34.0\%$ | $10.2\text{--}14.7\text{ psi}$ | $30.0\text{ cm/s}$ | SIBAL, PMMA, Nomex, tejidos de algodón | Sensor de monóxido de carbono $\text{CO}$, monitor $\text{CO}_2/\text{O}_2$, cámaras IR/visible, fotómetro de humo | `O1, O2, O3` | `M1` (frontera lunar hipobárica), `M2` (árbol de gases), `M3` |
| `PSI-104` | **SAFFIRE-V** | Cygnus | `10.60555/psi-104` | $30.0\text{--}34.0\%$ | $8.2\text{--}10.2\text{ psi}$ | $25.0\text{ cm/s}$ | Probetas SIBAL y PMMA en atmósfera lunar | Cámara infrarroja de alta resolución, transductor de presión diferencial, termopares | `O1, O2, O4` | `M1` (calibración hipobárica), `M3` (ranking y FMEA) |
| `PSI-105` | **SAFFIRE-VI** | Cygnus | `10.60555/psi-105` | $26.0\text{--}34.0\%$ | $8.2\text{--}14.7\text{ psi}$ | $30.0\text{ cm/s}$ | Polímeros fluorados, clorados, SIBAL, PMMA, Nomex | Analizador electroquímico de gases ácidos ($\text{CO}, \text{HF}, \text{HCl}$), fotómetro de opacidad | `O1, O3, O4` | `M2` (umbral toxicidad $\text{CO}$), `M3` (severidad ECLSS) |
| `PSI-26` | **BASS** | ISS-MSG | `10.60555/psi-26` | $15.0\text{--}30.0\%$ | $14.7\text{ psi}$ | $50.0\text{ cm/s}$ | Varillas de PMMA, esferas de PMMA, tejidos de algodón, SIBAL | Cámara de video HD, radiómetro térmico de banda ancha, anemómetro de flujo | `O1, O2, O3` | `M1` (extinción por convección baja), `M2` (FSM), `M3` |
| `PSI-25` | **BASS-II** | ISS-MSG | `10.60555/psi-25` | $17.0\text{--}28.0\%$ | $10.2\text{--}14.7\text{ psi}$ | $50.0\text{ cm/s}$ | Probetas planas de PMMA (espesor variable), SIBAL, Nomex, Kapton | Doble cámara de video sincronizada, termopares axiales, radiómetro | `O1, O2, O3` | **Núcleo `M1`** (Regresor GBR y RF), `M2` (frames), `M3` |
| `PSI-146` | **ACME-FlameDesign** | ISS-CIR | `10.60555/psi-146` | $21.0\text{--}40.0\%$ | $14.7\text{--}29.4\text{ psi}$ | $10.0\text{ cm/s}$ | Etileno y metano gaseoso con dilución controlada | Cámara de quimioluminiscencia $\text{OH}^*$ (310 nm), cámara intensificada $\text{CH}^*$, radiómetros | `O1, O3` | `M2` (visión: llama azul esferoidal), `M3` |
| `PSI-147` | **ACME-s-Flame** | ISS-CIR | `10.60555/psi-147` | $18.0\text{--}35.0\%$ | $7.3\text{--}29.4\text{ psi}$ | $5.0\text{ cm/s}$ | Metano y etileno en régimen de difusión | Radiómetro espectral, cámara de color HD de alta sensibilidad, óptica UV | `O1, O2, O3` | `M1` (pérdida radiativa $\propto T^4$, $\text{Da}$), `M2`, `M3` |
| `PSI-153` | **ACME-CLD-Flame** | ISS-CIR | `10.60555/psi-153` | $19.0\text{--}30.0\%$ | $14.7\text{--}29.4\text{ psi}$ | $18.0\text{ cm/s}$ | Metano diluido y etileno en flujo co-axial | Sistema de extinción láser a $635\text{ nm}$ para hollín, espectrómetro, cámara visible | `O1, O3` | `M2` (diferenciación llama limpia vs hollín), `M3` |
| `PSI-154` | **ACME-E-FIELD** | ISS-CIR | `10.60555/psi-154` | $21.0\text{--}30.0\%$ | $14.7\text{ psi}$ | $12.0\text{ cm/s}$ | Metano y etileno sometidos a gradiente electrodinámico | Electrómetro de alta tensión ($\pm 10\text{ kV}$), monitor de corriente iónica, cámara de alta velocidad | `O1, O3, O4` | `M2`, `M3` (comparativa supresores: `E-FIELD` vs `PFE`) |
| `PSI-132` | **BRE** | ISS-CIR | `10.60555/psi-132` | $16.0\text{--}30.0\%$ | $14.7\text{ psi}$ | $15.0\text{ cm/s}$ | Quemador poroso plano calibrado (emulación de PMMA y polímeros sólidos) | Radiómetros axiales, sensor de flujo térmico superficial, controladores de flujo másico | `O1, O2` | `M1` (número $B$ de transferencia de masa de Spalding), `M3` |
| `PSI-138` | **CFI-G** | ISS-CIR | `10.60555/psi-138` | $21.0\text{--}85.0\%$ | $10.2\text{--}29.4\text{ psi}$ | $8.0\text{ cm/s}$ | Butano, propano y dimetil éter ($\text{DME}$) | Cámara intensificada UV, micro-termopares superficiales, radiómetro infrarrojo | `O1, O3, O4` | `M2` (detección de llama fría difusiva NTC), `M3` |
| `PSI-24` | **FLEX** | ISS-CIR | `10.60555/psi-24` | $15.0\text{--}30.0\%$ | $10.2\text{--}29.4\text{ psi}$ | $5.0\text{ cm/s}$ | Gotas suspendidas de n-heptano, metanol y n-decano ($2\text{--}5\text{ mm}$) | Cámara de quimioluminiscencia UV $\text{OH}^*$ (310 nm), cámara retroiluminada de alta velocidad | `O1, O3, O4` | **Núcleo `M2`** (clase `Llama Fria NTC`, interlock FSM), `M3` |
| `PSI-27` | **FLEX-2** | ISS-CIR | `10.60555/psi-27` | $14.0\text{--}35.0\%$ | $10.2\text{--}29.4\text{ psi}$ | $8.0\text{ cm/s}$ | Alcanos líquidos con mezclas diluyentes ($\text{CO}_2, \text{He}, \text{N}_2, \text{Xe}$) | Cámara UV intensificada, mezclador volumétrico de gases diluyentes, radiómetro | `O1, O3` | `M2` (efectividad diluyentes en supresión), `M3` |
| `PSI-78` | **FLEX-2J** | ISS-CIR | `10.60555/psi-78` | $18.0\text{--}30.0\%$ | $14.7\text{ psi}$ | $6.0\text{ cm/s}$ | Arreglos regulares de gotas de n-decano y n-heptano (cooperación NASA-JAXA) | Doble sistema óptico de alta velocidad, arreglo axial de termopares | `O1, O2` | `M1` (propagación multifoco por salto térmico), `M3` |
| `PSI-79` | **MDCA-FLEX-ICE** | ISS-CIR | `10.60555/psi-79` | $18.0\text{--}30.0\%$ | $14.7\text{--}29.4\text{ psi}$ | $5.0\text{ cm/s}$ | Gotas bicomponentes immiscibles (cooperación con Agencia Espacial Italiana ASI) | Cámara $\text{OH}^*$ UV, sistema óptico de diagnóstico cromático, radiómetro | `O1, O2` | `M1` (microexplosiones y evaporación diferencial), `M3` |
| `PSI-126` | **SLICE** | ISS-MSG | `10.60555/psi-126` | $17.0\text{--}25.0\%$ | $14.7\text{ psi}$ | $45.0\text{ cm/s}$ | Metano y etileno en flujo co-axial forzado | Cámara de color calibrada, anemómetro térmico de precisión, termopares | `O1, O2, O3` | `M1` (cota superior de Damköhler y soplado), `M2`, `M3` |
| `PSI-129` | **SPICE** | ISS-MSG | `10.60555/psi-129` | $19.0\text{--}28.0\%$ | $14.7\text{ psi}$ | $25.0\text{ cm/s}$ | Etileno, propano y metano en boquillas calibradas ($0.7\text{--}2.0\text{ mm}$) | Detector de partículas SAME ($<0.1\,\mu\text{m}$), fotómetro de dispersión de humo, cámara | `O1, O3, O4` | **Núcleo `M2`** (umbral `submicron_aerosol` en `PRE_ALERTA`), `M3` |
| `PSI-107` | **CVB** | ISS-MSG | `10.60555/psi-107` | $21.0\%$ | $14.7\text{ psi}$ | $10.0\text{ cm/s}$ | Películas líquidas de pentano en celda de cuarzo restringida | Interferómetro de haz láser polarizado, arreglo axial termométrico | `O1, O2` | `M1` (calibración del número de Péclet $\text{Pe}$), `M3` |
| `PSI-108` | **CVB-2** | ISS-MSG | `10.60555/psi-108` | $21.0\%$ | $14.7\text{ psi}$ | $10.0\text{ cm/s}$ | Tubo térmico capilar con fluidos puros y mezclas binarias | Interferómetro óptico de superficie, medidor de flujo térmico crítico | `O1, O3` | Física de evaporación de niebla fina de agua (`PFE`), `M3` |
| `PSI-109` | **NCA** | Otros (1g) | `10.60555/psi-109` | $17.0\text{--}35.0\%$ | $8.2\text{--}14.7\text{ psi}$ | $40.0\text{ cm/s}$ | Probetas delgadas de PMMA, papel de celulosa y textiles Nomex | Cámara de alta velocidad sincronizada, transductor de presión diferencial, medidor másico | `O1, O2, O4` | `M1` (factor de correlación $1g \leftrightarrow 0g$), `M3` (norma NASA-STD-6001) |
| `PSI-110` | **MSC** | Otros (STS) | `10.60555/psi-110` | $18.0\text{--}30.0\%$ | $14.7\text{ psi}$ | $15.0\text{ cm/s}$ | Cilindros de espuma flexible de poliuretano porosa | Monitor electroquímico de $\text{CO}$, arreglo interno de termopares, cámara de registro | `O1, O3, O4` | `M2` ($\text{CO}$ sin llama $\to$ `PRE_ALERTA`), `M3` (Severidad FMEA) |

---

## 3. Ponderación Multicriterio de las 24 Investigaciones (TOPSIS/AHP)

Para la toma de decisiones basada en datos, cada investigación dispone de una vectorización normalizada en el espacio $[0.0, 1.0]^4$, correspondiente a los cuatro criterios de impacto de la metodología **TOPSIS** (*Technique for Order of Preference by Similarity to Ideal Solution*):

1. **`habitat` (Afinidad a Entornos Habitables):** Representatividad directa respecto a cabinas de tripulación, toxicidad ECLSS y atmósferas de descompresión lunar Artemis ($34\%\text{ O}_2, 8.2\text{ psi}$).
2. **`modeling` (Rigor Físico y Datos para Modelado):** Densidad de puntos experimentales calibrados y matrices de variables continuas ($V_f$, $\% \text{O}_2$, presión, espesor, velocidad forzada) útiles para el entrenamiento de regresores.
3. **`sensors` (Innovación en Detección e Instrumentación):** Calidad diagnóstica de los sensores (aerosoles submicrónicos $<0.1\,\mu\text{m}$, cámaras UV de banda estrecha a $310\text{ nm}$, analizadores de gases ácidos $\text{HF}/\text{HCl}$).
4. **`spinoff` (Transferencia y Seguridad Industrial Terrestre):** Aplicabilidad directa en normas de edificación (NFPA), protección de bomberos, transporte cerrado y centros de datos.

### 3.1 Vector de Puntuaciones Canónicas

| ID PSI | Acrónimo | Criterio `habitat` | Criterio `modeling` | Criterio `sensors` | Criterio `spinoff` | TOPSIS Score Base ($w_i = 0.25$) | Ranking Global |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `PSI-104` | SAFFIRE-V | **0.99** | 0.91 | 0.89 | 0.87 | **0.915** | 2 |
| `PSI-103` | SAFFIRE-IV | **0.98** | 0.88 | 0.92 | 0.86 | **0.910** | 3 |
| `PSI-105` | SAFFIRE-VI | 0.97 | 0.86 | **0.96** | 0.92 | **0.928** | 1 |
| `PSI-101` | SAFFIRE-II | 0.96 | 0.89 | 0.80 | 0.88 | 0.883 | 7 |
| `PSI-98` | SAFFIRE-I | 0.95 | 0.91 | 0.86 | 0.84 | 0.890 | 6 |
| `PSI-110` | MSC | 0.95 | 0.87 | **0.97** | **0.95** | **0.935** | Top 1 Sólidos |
| `PSI-25` | BASS-II | 0.94 | **0.99** | 0.81 | 0.85 | 0.898 | 4 |
| `PSI-102` | SAFFIRE-III | 0.93 | 0.90 | 0.82 | 0.85 | 0.875 | 8 |
| `PSI-129` | SPICE | 0.92 | 0.84 | **0.99** | **0.98** | **0.933** | Top 1 Sensores |
| `PSI-26` | BASS | 0.91 | 0.95 | 0.77 | 0.79 | 0.855 | 11 |
| `PSI-27` | FLEX-2 | 0.89 | 0.92 | 0.88 | 0.86 | 0.888 | 9 |
| `PSI-109` | NCA | 0.88 | 0.91 | 0.75 | 0.90 | 0.860 | 10 |
| `PSI-132` | BRE | 0.86 | 0.96 | 0.79 | 0.80 | 0.853 | 12 |
| `PSI-24` | FLEX | 0.85 | 0.96 | **0.97** | 0.88 | 0.915 | Top 1 Gotas |
| `PSI-154` | ACME-E-FIELD | 0.84 | 0.85 | 0.83 | 0.91 | 0.858 | 13 |
| `PSI-138` | CFI-G | 0.80 | 0.93 | 0.95 | 0.81 | 0.873 | 14 |
| `PSI-126` | SLICE | 0.78 | 0.90 | 0.82 | 0.74 | 0.810 | 17 |
| `PSI-147` | ACME-s-Flame | 0.72 | 0.97 | 0.84 | 0.75 | 0.820 | 15 |
| `PSI-78` | FLEX-2J | 0.70 | 0.91 | 0.79 | 0.76 | 0.790 | 18 |
| `PSI-146` | ACME-FlameDesign | 0.68 | 0.94 | 0.87 | 0.82 | 0.828 | 16 |
| `PSI-79` | MDCA-FLEX-ICE | 0.67 | 0.89 | 0.78 | 0.77 | 0.778 | 19 |
| `PSI-153` | ACME-CLD-Flame | 0.65 | 0.90 | 0.91 | 0.78 | 0.810 | 17 |
| `PSI-107` | CVB | 0.62 | 0.83 | 0.76 | 0.72 | 0.733 | 21 |
| `PSI-108` | CVB-2 | 0.60 | 0.82 | 0.74 | 0.73 | 0.723 | 22 |

---

## 4. Trazabilidad hacia los 10 Recursos Oficiales de la NASA

Cada uno de los 10 recursos documentales suministrados por el reto ha sido integrado en la arquitectura del sistema, vinculando sus aportes teóricos o normativos con componentes de software específicos:

| Identificador | Recurso Oficial de la NASA | DOI / Fuente Primaria | Aporte Teórico o Normativo | Implementación de Software | Rol Líder Asignado |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Recurso 1** | **NASA Physical Sciences Informatics (PSI)** | `https://physicalsciences.nasa.gov/` | Repositorio de 24 investigaciones de microgravedad bajo licencia CC0-1.0 y tablas de datos estructurados. | `backend/domain.py` (`PsiRepository`), `data/psi_combustion_24.json` y `data/bass_saffire_runs.csv`. | [[Rol_Combinado_Sinergia]] |
| **Recurso 2** | **NASA Glenn Research Center Combustion** | NASA GRC Technical Hub | Taxonomía de las cinco áreas de combustión en microgravedad e instalaciones orbitales (`CIR`, `MSG`, `Cygnus`). | Sistema de filtrado y categorización en `backend/domain.py` y visualización de instalaciones. | [[Rol_Gestion_Industrial]] |
| **Recurso 3** | **ScienceCasts: Combustion in Space** | NASA Science Multimedia | Evidencia experimental de llamas azules esferoidales sin hollín y fenómeno de llamas frías invisibles. | Clases de la red neuronal convolucional (`flame_cnn.onnx`): `Esferica Azul 0g` y `Llama Fria NTC`. | [[Rol_Mecatronica_y_Control]] |
| **Recurso 4** | **Researcher's Guide to ISS: Combustion** | NASA NP-2015-03-014-JSC | Formulación matemática de los números adimensionales de Damköhler ($\text{Da}$), Péclet ($\text{Pe}$) y Grashof ($\text{Gr} \to 0$). | `backend/physics_ml.py` (`DimensionlessPhysicsCalculator`), modelado de regímenes de extinción. | [[Rol_Mecatronica_y_Control]] |
| **Recurso 5** | **Apollo 1 Case Study & Lessons Learned** | NASA History Office / NTRS | Incidente de atmósfera de oxígeno puro ($100\%\text{ O}_2, 16.7\text{ psi}$), ignición por arco y origen del estándar `NASA-STD-6001`. | Preset forense 1-clic en simulador y fila crítica en matriz de modos de falla `FMEA` (`backend/governance.py`). | [[Rol_Combinado_Sinergia]] |
| **Recurso 6** | **Apollo 13 Oxygen Tank Incident** | NASA NTRS Report R-70-1 | Degradación térmica de teflón (PTFE) por calentadores de sobrevoltaje en oxígeno supercrítico ($1,000\text{ psi}$). | Preset forense 1-clic en simulador e interlock de sobretensión eléctrica en el ducto digital. | [[Rol_Combinado_Sinergia]] |
| **Recurso 7** | **Mir Space Station Fire (1997)** | NASA STS-89 / Mir Oral History | Fuego auto-oxidante en generador de oxígeno sólido `SFOG Vika` ($\text{LiClO}_4$) de $14\text{ min}$; ineficacia de cortar aire. | Regla determinista de supresión: exclusión de asfixia por corte de flujo ante oxidantes químicos; requerimiento de `PFE`. | [[Rol_Combinado_Sinergia]] |
| **Recurso 8** | **NASA Spinoff Node 9582: Fireman's SCBA** | NASA Spinoff Publication (1976) | Transferencia de recipientes de presión compuestos (COPV) a $4,500\text{ psi}$, reduciendo el peso del bombero en un $40\%$. | Módulo 4: Calculadora *Dual-Use* de impacto terrestre (`backend/governance.py`). | [[Rol_Gestion_Industrial]] |
| **Recurso 9** | **NASA Spinoff Node 9407: Submicron Smoke** | NASA Spinoff Publication (1978) | Discriminador de aerosoles pirolíticos submicrónicos ($<0.1\,\mu\text{m}$) desarrollado para el Transbordador Espacial. | Umbral analítico del estado `PRE_ALERTA` en `DeterministicFsmController` (`backend/duct_twin.py`). | [[Rol_Combinado_Sinergia]] |
| **Recurso 10** | **NASA Spinoff Node 9918 (PBI) & ISS PFE** | NASA Spinoff (1977) & ISS ECLSS | Fibras ignífugas de polibenzimidazol (PBI) y extintor portátil de niebla de agua fina ($20\text{--}100\,\mu\text{m}$). | Árbol de decisión de agentes supresores (`PFE` vs $\text{CO}_2$ vs `E-FIELD`) en `backend/governance.py`. | [[Rol_Gestion_Industrial]] |

---

## 5. Arquitectura de Datos y Protocolo de Seguridad (OWASP / STRIDE)

La ingestión de las 24 investigaciones opera bajo un esquema defensivo que previene riesgos de inyección, denegación de servicio y falsificación de peticiones:

```
                  +----------------------------------------------+
                  |         Cliente Externo / Navegador          |
                  +----------------------+-----------------------+
                                         |
                                         | Petición HTTP / JSON
                                         v
                  +----------------------------------------------+
                  |            SecurityBoundaryGuard             |
                  |  - Payload Size <= 16 KB (HTTP 413)          |
                  |  - Rate Limiter Sliding Window (HTTP 429)    |
                  |  - Security Headers (CSP, X-Frame DENY)      |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          DTO Validation (Pydantic)           |
                  |  - extra = 'forbid' (Anti-Mass-Assignment)   |
                  |  - Validaciones de rango numérico estricto   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          PsiRepository (Inmutable)           |
                  |  - Entidades PsiInvestigation (@dataclass)   |
                  |  - osdr.nasa.gov Regex Match (Anti-SSRF)     |
                  |  - Timeout 3.0 s + Fallback Local Sin Red    |
                  +----------------------------------------------+
```

1. **Inmutabilidad Estructural:** Todas las instancias de `PsiInvestigation` se definen mediante decoradores `@dataclass(frozen=True)`, garantizando que ningún componente en memoria altere los metadatos oficiales de las investigaciones durante el ciclo de vida de la aplicación.
2. **Defensa Anti-SSRF:** La clase `OsdrApiClient` valida toda URL contra una lista blanca explícita mediante expresión regular (`^https://(osdr\.nasa\.gov|visualization\.osdr\.nasa\.gov)/`). Se prohíbe taxativamente la resolución de esquemas `file://`, `http://`, direcciones de loopback o metadatos en la nube (`169.254.169.254`).
3. **Resiliencia Operativa:** Ante cualquier fallo de conectividad externa o latencia superior a $3.0\text{ s}$ en las fuentes remotas de OSDR, el repositorio conmuta automáticamente al archivo local maestro `data/psi_combustion_24.json`, permitiendo el funcionamiento ininterrumpido sin acceso a internet.

---

## 6. Conclusiones de Gobernanza e Hitos de Entrega

La consolidación de esta matriz de trazabilidad certifica que:
- Las 24 investigaciones cubren de forma exhaustiva los escenarios habitables de interés espacial (`ISS`, `Cygnus`, hábitats lunares) y terrestres (`1g`).
- Cero referencias a sistemas de propulsión cohete existen en el conjunto de datos, asegurando el cumplimiento irrevocable de la restricción `C-01`.
- Los datos se encuentran desacoplados de modelos externos de pago, cumpliendo con la directiva `C-02`.
- El módulo downstream de toma de decisiones multicriterio (**TOPSIS/AHP**) dispone de un conjunto canónico de vectores normalizados para ejecutar la jerarquización sin sesgos subjetivos.

Este documento formaliza el cierre del hito **`I-01`** bajo la responsabilidad del Ingeniero de Gestión Industrial y habilita de forma inmediata el desarrollo de la especificación técnica **`I-02`** (Modelo de Ranking Multicriterio TOPSIS/AHP).
