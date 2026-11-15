# Auditoría de Consistencia de Unidades y Alcance Estricto (`C-01`) — Tarea `I-09`

> **Proyecto:** AERO-IGNIS SI (`NASA Space Apps Challenge 2026`)  
> **Perfil Responsable:** Ingeniería de Gestión Industrial (`ind`)  
> **Alcance Auditado:** Datasets (`data/psi_combustion_24.json`, `data/bass_saffire_runs.csv`, `data/cases_and_spinoffs.json`), módulos `backend/*.py` y vistas `frontend/index.html`, `frontend/app.js`.  
> **Suite de Verificación Automatizada:** [`tests/unit/test_qa_units_scope_unit.py`](../../tests/unit/test_qa_units_scope_unit.py).

---

## 1. Resumen Ejecutivo de Auditoría

La auditoría física, dimensional y de dominio (`C-01`) confirma consistencia integral entre las unidades de entrada del usuario, las conversiones internas del vector `RandomForest`/`GBR`, los límites operativos de telemetría en ducto y la exclusión absoluta de motores cohete o sistemas de propulsión espacial.

---

## 2. Matriz de Consistencia Dimensional y Factores de Conversión

| Magnitud Física | Unidad de Entrada / API | Conversión Interna Verificada | Factor / Equivalencia Exacta | Rango Auditado | Módulo Verificado |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Concentración $\text{O}_2$** | `% O2` (`o2_pct`) | Normalización `o2_pct / 21.0` | Aire estándar = `21.0%` | `10.0–100.0%` (`PSI`: `14.0–85.0%`) | `backend/physics_ml.py`, `data/psi_combustion_24.json` |
| **Presión de cabina** | `psi` (`pressure_psi`) | `pressure_psi / 14.7` (`atm`) | $1\text{ atm} = 14.7\text{ psi} \approx 101.325\text{ kPa}$; $1\text{ psi} = 6.8948\text{ kPa}$ | `1.0–30.0 psi` (`PSI`: `7.3–29.4 psi`, `50.3–202.7 kPa`) | `AtmosphericState`, `DimensionlessPhysicsCalculator` |
| **Velocidad de flujo** | `cm/s` (`flow_cm_s`, `airflow_cm_s`) | `air_flow_cms` directa | $1\text{ cm/s} = 0.01\text{ m/s}$ | `0.0–60.0 cm/s` (`PSI`: `5.0–50.0 cm/s`) | `AtmosphericState`, `SensorTelemetryFrame` |
| **Aceleración gravitacional** | `g` (`gravity_g`) | Discreta $\in \{0.0, 0.16, 0.38, 1.0\}$ | ISS `0g`, Lunar `0.16g`, Marciana `0.38g`, Tierra `1.0g` | `0.0–1.0 g` | `VALID_GRAVITIES`, `bass_saffire_runs.csv` |
| **Espesor de muestra** | `mm` (`thickness_mm`) | `thickness_mm / 10.0` (`thickness_cm`) | $1\text{ cm} = 10.0\text{ mm}$ | `0.1–50.0 mm` | `AtmosphericState.to_feature_array()` |
| **Tasa de propagación ($V_f$)** | `mm/s` (`flame_spread_mm_s`) | Salida directa `round(..., 3)` | Coherente con `mm/s` de `BASS-II`/`Saffire` | $\ge 0.0\text{ mm/s}$ | `DimensionlessPhysicsCalculator`, `bass_saffire_runs.csv` |
| **Gradiente térmico ducto** | `°C/s` (`delta_t_dt`) | Vector sensor `(1, 4)` | Numericamente equivalente a `K/s` | `-5.0–100.0 °C/s` | `SensorTelemetryFrame` |
| **Monóxido / Aerosol** | `ppm` / `% relativo` | Vector sensor `(1, 4)` | `CO (0–5000 ppm)`, aerosol `<0.1 um` (`0–100`) | Verificado en rango completo | `SensorTelemetryFrame`, `SPICE PSI-129` |
| **Masa ahorrada Spinoff** | `lb` (`weight_saved_lb_per_unit`) | Escalamiento `lb_unit * units` | $1\text{ lb} = 0.453592\text{ kg}$ (conversión SI) | `0.0–13.0 lb/unidad`, `1–10,000` uds | `GovernanceAndSpinoffService`, `cases_and_spinoffs.json` |
| **Energía / Campo / Niebla** | `kJ/kg`, `kV`, `um` | Reglas ECLSS deterministas | Calor latente agua `2,260 kJ/kg`; campo `+/-10 kV`; gotas `20-100 um` | Trazado en `PFE` y `PSI-154` | `select_suppression_protocol`, `protocolo_supresion_eclss.md` |

---

## 3. Verificación de Regímenes de Cabina y Casos Forenses (`cases_and_spinoffs.json`)

- **`apollo_1`:** `100.0% O2`, `16.7 psi` (`115.1 kPa`), `5.0 cm/s`, `1.0 g`, `PTFE / Espuma y Velcro` (`2.0 mm`).
- **`apollo_13`:** `100.0% O2`, capado a `30.0 psi` (`206.8 kPa`) según límite de seguridad del simulador `SPEC.md` (documentando presión real criogénica de `~1,000 psi`).
- **`mir_1997`:** `21.0% O2`, `14.7 psi` (`101.4 kPa`), `12.0 cm/s`, `0.0 g`, cartucho `SFOG Vika (LiClO4)`.
- **`lunar_artemis`:** `34.0% O2`, `8.2 psi` (`56.5 kPa`), `12.0 cm/s`, `0.16 g`, `SIBAL` (`0.8 mm`).

---

## 4. Auditoría de Exclusión de Dominio (`C-01`: Cero Motores Cohete)

El barrido automatizado ejecutado por `test_domain_scope_c01_excludes_rocket_propulsion` sobre `data/psi_combustion_24.json`, `data/bass_saffire_runs.csv`, `data/cases_and_spinoffs.json`, los cinco módulos de lógica en `backend/` (`domain.py`, `physics_ml.py`, `duct_twin.py`, `ranking_nlp.py`, `governance.py`) y la interfaz `frontend/` (`index.html`, `app.js`) arrojó **`0` ocurrencias** de términos de propulsión o motores cohete (`motor cohete`, `rocket engine`, `thruster`, `tobera`, `solid rocket`, `liquid propellant`). Todas las referencias de combustión pertenecen estrictamente a:

1. **Entornos habitables presurizados** (`ISS-CIR`, `ISS-MSG`, `Cygnus/Saffire I–VI`, hábitats lunares Artemis).
2. **Transferencia tecnológica terrestre Spinoff** (`9582`, `9407`, `9918`, `PFE`).
