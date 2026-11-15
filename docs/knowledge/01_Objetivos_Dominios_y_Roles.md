---
type: matrix
project: AERO-IGNIS-SI
tags: [nasa/matrix, domains, objectives, ml-pipeline]
---

# Matriz Maestra: 24 Investigaciones PSI + 10 Recursos -> ML/DL -> Objetivos y Roles

Esta tabla fija que informacion extraemos de cada fuente oficial, que modelo propio la procesa, que objetivo del reto satisface y que perfil lidera su entrega. Ver conexiones visuales en [[00_MOC_Indice_Maestro_AERO_IGNIS]].

---

## 1. Las 24 Investigaciones de Combustion NASA PSI

| ID / Nota | Instalacion | Datos Utiles y Variables Clave | Entrenamiento ML / DL Propio | Objetivos | Dominio / Rol Lider |
| :--- | :--- | :--- | :--- | :---: | :--- |
| [[PSI-98_SAFFIRE-I]] | Cygnus | Tabla 13 cols; panel SIBAL $0.4\times 0.94\text{ m}$ a $20\text{ cm/s}$ | `M1` ($V_f$, Burn Time), `M2` (frames llama abierta), `M3` (TF-IDF) | `O1, O2, O3` | [[Rol_Combinado_Sinergia]] |
| [[PSI-101_SAFFIRE-II]] | Cygnus | 9 muestras (PMMA, SIBAL, Nomex, silicona), flujo concurrente/opuesto | `M1` (`RandomForestClassifier` materiales), `M3` | `O1, O2` | [[Rol_Combinado_Sinergia]] |
| [[PSI-102_SAFFIRE-III]] | Cygnus | Crecimiento acelerado de llama a flujo alto ($30\text{ cm/s}$) | `M1` ($V_f$), `M2` (cota ventilador en FSM), `M3` | `O1, O2, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-103_SAFFIRE-IV]] | Cygnus | Atmosferas enriquecidas $30\text{–}34\%\text{ O}_2$ y sensores de gases | `M1` (frontera lunar), `M2` (`DecisionTree` gases), `M3` | `O1, O2, O3` | [[Rol_Combinado_Sinergia]] |
| [[PSI-104_SAFFIRE-V]] | Cygnus | Presion reducida ($8.2\text{ psi}$) + $30\text{–}34\%\text{ O}_2$ en modulo lunar | `M1` (validacion subatmosferica), `M3` (`TOPSIS` + FMEA) | `O1, O2, O4` | [[Rol_Gestion_Industrial]] |
| [[PSI-105_SAFFIRE-VI]] | Cygnus | Perfiles de gases toxicos ($\text{CO}$, $\text{HF}$, $\text{HCl}$) post-incendio | `M2` (umbral `co_ppm`), `M3` + Severidad FMEA | `O1, O3, O4` | [[Rol_Gestion_Industrial]] |
| [[PSI-26_BASS]] | ISS-MSG | Paradoja flujo bajo ($<5\text{ cm/s}$): avivamiento breve al cortar flujo | `M1` (extincion baja vel.), `M2` (histeresis FSM), `M3` | `O1, O2, O3` | [[Rol_Combinado_Sinergia]] |
| [[PSI-25_BASS-II]] | ISS-MSG | **17 cols, >130 corridas**; curvas *quenching* vs *blowoff* | **Nucleo `M1`** (`RF` + `GBR`), `M2` (frames Colab), `M3` | `O1, O2, O3` | [[Rol_Combinado_Sinergia]] |
| [[PSI-146_ACME-Flame-Design]] | ISS-CIR | Llamas esfericas azules sin hollin (etileno/metano) | `M2` (`flame_cnn.onnx` clase `Llama Esferica Azul 0g`), `M3` | `O1, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-147_ACME-s-Flame]] | ISS-CIR | Radiometria y apagado por perdida radiativa $\propto T^4$ | `M1` (limite radiativo $\text{Da}$), `M2`, `M3` | `O1, O2, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-153_ACME-CLD-Flame]] | ISS-CIR | Formacion y oxidacion de hollin con laser 635 nm | `M2` (separacion llama limpia vs hollín), `M3` | `O1, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-154_ACME-E-FIELD]] | ISS-CIR | Viento ionico $\pm 10\text{ kV}$ para supresion y gravedad parcial | `M2`, `M3` + comparador supresores `E-FIELD vs PFE` | `O1, O3, O4` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-132_BRE]] | ISS-CIR | Quemador poroso plano; numero $B$ de Spalding | `M1` (parametro fisico de transferencia de masa), `M3` | `O1, O2` | [[Rol_Combinado_Sinergia]] |
| [[PSI-138_CFI-G]] | ISS-CIR | Llamas frias difusivas gaseosas hasta $85\%\text{ O}_2$ | `M2` (`Llama Fria NTC` + `DecisionTree`), `M3` | `O1, O3, O4` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-24_FLEX]] | ISS-CIR | Descubrimiento de **llamas frias ($500\text{–}800\text{ K}$)** y camara UV | **Nucleo clase `2: Llama Fria NTC`** en `M2` + bloqueo rearme FSM | `O1, O3, O4` | [[Rol_Combinado_Sinergia]] |
| [[PSI-27_FLEX-2]] | ISS-CIR | Gotas y dilucion con $\text{N}_2, \text{CO}_2, \text{He}, \text{Xe}$ | `M2` + matriz comparativa de agentes inertes, `M3` | `O1, O3` | [[Rol_Combinado_Sinergia]] |
| [[PSI-78_FLEX-2J]] | ISS-CIR | Propagacion entre arreglos de gotas (NASA-JAXA) | `M1` (propagacion multifoco), `M3` | `O1, O2` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-79_MDCA-FLEX-ICE]] | ISS-CIR | Gotas bicomponentes (ASI) y microexplosiones | `M1` (`Burn Time` en mezclas), `M3` | `O1, O2` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-126_SLICE]] | ISS-MSG | Desprendimiento (*liftoff*) y soplado (*blowout*) en gases | `M1` (cota superior $\text{Da}$), `M2` (flujo critico), `M3` | `O1, O2, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-129_SPICE]] | ISS-MSG | Punto de humo + complemento `SAME/DAFT` ($<0.1\,\mu\text{m}$) | **Nucleo `PRE_ALERTA`** (`submicron_aerosol`) en `M2` + `Node 9407` | `O1, O3, O4` | [[Rol_Combinado_Sinergia]] |
| [[PSI-107_CVB]] | ISS-MSG | Burbuja de vapor restringida e interferometria termica | `M1` (calibracion Peclet $\text{Pe}$), `M3` | `O1, O2` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-108_CVB-2]] | ISS-MSG | Peliculas liquidas en tubo termico en $0g$ | Fisica de evaporacion del extintor `PFE`, `M3` | `O1, O3` | [[Rol_Mecatronica_y_Control]] |
| [[PSI-109_NCA]] | Tierra $1g$ | Canal estrecho $1g$ que suprime conveccion para ensayos previos | `M1` (correlacion $1g \leftrightarrow 0g$), `M3` (`NASA-STD-6001`) | `O1, O2, O4` | [[Rol_Gestion_Industrial]] |
| [[PSI-110_MSC]] | STS / 0g | Combustion latente (*smoldering*) en espumas y transicion a llama | `M2` (`CO` alto sin luz visible -> `PRE_ALERTA`), `M3` + FMEA | `O1, O3, O4` | [[Rol_Combinado_Sinergia]] |

---

## 2. Los 10 Recursos Oficiales del Reto

| Recurso Oficial | Que Contiene | Uso en Arquitectura AERO-IGNIS | Rol Lider |
| :--- | :--- | :--- | :--- |
| **1. NASA PSI Combustion Repo** | 24 investigaciones `CC0-1.0`, DOI `10.60555`, ISA-Tab, tablas `.csv` | Base de datos maestra `psi_combustion_24.json` + entrenamiento `M1/M2/M3` | [[Rol_Combinado_Sinergia]] |
| **2. NASA Glenn Combustion** | Cinco pilares de investigacion y plataformas `CIR`, `MSG`, `Cygnus` | Taxonomia oficial y filtros por instalacion en `M3` | [[Rol_Gestion_Industrial]] |
| **3. ScienceCasts: ISS Combustion** | Explicacion visual de llamas esfericas azules y llamas frias ($3.6\text{ min}$) | Referencia para etiquetado de clases de la CNN `flame_cnn.onnx` | [[Rol_Mecatronica_y_Control]] |
| **4. Researcher's Guide ISS** | Ecuaciones $\text{Da}$, $\text{Pe}$, $\text{Gr}\to 0$ y diagnosticos orbitales | Implementacion exacta de `DimensionlessPhysicsCalculator` | [[Rol_Mecatronica_y_Control]] |
| **5. Apollo 1 Case Study** | $100\%\text{ O}_2$, $16.7\text{ psi}$, cable PTFE, origen de `NASA-STD-6001` | Preset forense 1-clic en Modulo 2 + control normativo en FMEA | [[Rol_Combinado_Sinergia]] |
| **6. Apollo 13 Case Study** | Tanque $\text{O}_2$ a $1,000\text{ psi}$, PTFE degradado a $>500\text{ °C}$ | Preset forense 1-clic en Modulo 2 + severidad electrica FMEA | [[Rol_Combinado_Sinergia]] |
| **7. Mir Station Fire (1997)** | Cartucho `SFOG Vika` ($\text{LiClO}_4$) auto-oxidante $14\text{ min}$, humo denso | Regla critica de que cortar aire no apaga fuegos auto-oxidantes (`PFE` necesario) | [[Rol_Combinado_Sinergia]] |
| **8. Spinoff Node 9582 (SCBA)** | Cilindros COPV $4,500\text{ psi}$; peso bombero de $33\text{ lb}$ a $20\text{ lb}$ (-40%) | Calculadora **Dual-Use** Tierra $\leftrightarrow$ Espacio (`O4`) | [[Rol_Gestion_Industrial]] |
| **9. Spinoff Node 9407 (Detector)** | Discriminador de particulas submicronicas $<0.1\,\mu\text{m}$ vs polvo | Umbral `submicron_aerosol` de `PRE_ALERTA` en `M2` + **Dual-Use** minas/servidores | [[Rol_Combinado_Sinergia]] |
| **10. Spinoff Node 9918 (PBI) + PFE** | Traje `PBI/Nomex` (-30% peso) + niebla fina $20\text{–}100\,\mu\text{m}$ (`PFE`) | Arbol de supresion (`PFE` vs `CO2` vs `E-FIELD`) + **Dual-Use** (`O4`) | [[Rol_Gestion_Industrial]] |
