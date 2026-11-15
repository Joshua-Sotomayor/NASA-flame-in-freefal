---
type: governance-and-history
tags: [nasa/forensic, apollo-1, apollo-13, mir, spinoffs, fmea, dual-use]
---

# Casos Forenses Historicos y Transferencia Dual-Use (Spinoffs)

Este bloque transforma el conocimiento cientifico de los 24 PSI en impacto industrial y salvamento de vidas en la Tierra (**Objetivo 4**), liderado por [[Rol_Gestion_Industrial]] y [[Rol_Combinado_Sinergia]].

---

## 1. Los 3 Incidentes Forenses (Presets del Simulador en 1 Clic)

| Incidente | Condiciones Reales Verificadas | Causa Raiz | Legado e Implementacion en AERO-IGNIS |
| :--- | :--- | :--- | :--- |
| **Apollo 1** *(27 ene 1967)* | Cabina a $100\%\text{ O}_2$ y $16.7\text{ psi}$ ($115\text{ kPa}$); la presion escalo a $29\text{ psi}$ en $15\text{ s}$ | Arco en cable PTFE encendio $>3.1\text{ m}^2$ de Velcro y espumas | Origen de **NHB 8060.1 / `NASA-STD-6001`**, mezcla $60\%\text{ O}_2 / 40\%\text{ N}_2$ al lanzar, escotilla $5\text{ s}$ y tejidos `PBI`. Preset critico en `M1`. |
| **Apollo 13** *(13 abr 1970)* | Tanque $\text{O}_2$ supercritico No. 2 a $\sim 1,000\text{ psi}$ | Calentadores $65\text{ V}$ vs $28\text{ V}$ degradaron aislamiento PTFE a $>500\text{ °C}$ en tierra | Demuestra que polimeros "incombustibles" arden en $\text{O}_2$ a alta presion tras dano termico. Fila de alto NPR electrico en FMEA. |
| **Mir Kvant-1** *(23 feb 1997)* | Cabina ISS/Mir; cartucho solido `SFOG Vika` ($\text{LiClO}_4$ + hierro) | Contaminacion organica genero soplete auto-oxidante de $1.5\text{ m}$ durante $14\text{ min}$ | Demuestra que cortar ventilacion **no apaga fuegos auto-oxidantes**; exige enfriamiento acuoso (`PFE`) y respiradores independientes. |

---

## 2. Cuatro Tecnologias Dual-Use (Spinoffs 9582, 9407, 9918 y PFE)

1. **Fireman's Air Tanks (`Spinoff Node 9582`, 1976):**
   - Origen: recipientes compuestos **COPV** y sistema `PLSS` del Apollo.
   - Impacto en Tierra: cilindros aluminio + fibra de vidrio/epoxi subieron la presion de $2,216$ a **$4,500\text{ psi}$**, bajando el peso del equipo SCBA de bomberos de **$33\text{ lb}$ a $20\text{ lb}$ (-40%)** con arnes de cadera.
2. **Fire Detector (`Spinoff Node 9407`, 1978, Brunswick / Space Shuttle):**
   - Origen: discriminador de particulas del Transbordador contra polvo flotante en avio-electronica.
   - Impacto en Tierra: detecta **aerosoles submicronicos invisibles ($<0.1\,\mu\text{m}$)** durante pirólisis temprana antes de llama abierta; desplegado en minas subterraneas, servidores y submarinos. Alimenta directamente el umbral `PRE_ALERTA` de `M2` junto con [[PSI-129_SPICE]] (`SAME`).
3. **New Technology for the Fire Attire (`Spinoff Node 9918`, 1977, Project FIRES):**
   - Origen: telas ignifugas post-Apollo 1.
   - Impacto en Tierra: fibra **PBI** + **Nomex** en trajes estructurales de bomberos de 3 capas, reduciendo peso en **$>30\%$** sin encoger ni liberar gases toxicos.
4. **Extintor Portatil de Niebla de Agua Fina (`ISS PFE`):**
   - Reemplazo al Halon 1301 (que genera $\text{HF}$/$\text{HBr}$ corrosivos) y al $\text{CO}_2$ (asfixiante en cabina).
   - Presurizado con $\text{N}_2$, genera gotas Sauter de **$20\text{–}100\,\mu\text{m}$**: enfria por alto calor latente ($2,260\text{ kJ/kg}$), diluye $\text{O}_2$ al expandirse vapor $1,700\times$, atenua radiacion y es seguro para avionica.

---

## 3. Conexion con Modelos y Objetivos

- **Objetivos:** [[O4_Spinoffs_Terrestres_y_Forense]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]].
- **Roles:** [[Rol_Gestion_Industrial]] (FMEA + calculadora Dual-Use) y [[Rol_Combinado_Sinergia]] (validacion forense en simulador).
