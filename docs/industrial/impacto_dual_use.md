# Modelo Cuantitativo de Impacto *Dual-Use* y Transferencia Spinoff NASA — Tarea `I-07`

> **Proyecto:** AERO-IGNIS SI (`NASA Space Apps Challenge 2026`)  
> **Perfil Responsable:** Ingeniería de Gestión Industrial (`ind`)  
> **Alcance (`C-01`):** Transferencia tecnológica terrestre derivada de investigación en entornos habitables presurizados (`Apollo`, `Space Shuttle`, `ISS`, `Cygnus`). Excluye propulsores y motores cohete.  
> **Implementación Verificada:** [`GovernanceAndSpinoffService.calculate_dual_use`](../../backend/governance.py) · Fuente oficial en [`data/cases_and_spinoffs.json`](../../data/cases_and_spinoffs.json) · Pruebas TDD en [`tests/unit/test_dual_use_spinoffs_unit.py`](../../tests/unit/test_dual_use_spinoffs_unit.py).

---

## 1. Propósito y Contrato Matemático de la Calculadora (`SPEC.md`)

La Calculadora de Impacto *Dual-Use* cuantifica el retorno operativo y ergonómico de cuatro tecnologías de seguridad contra incendios nacidas en misiones tripuladas NASA y adoptadas por cuerpos de bomberos, hospitales, minería e infraestructura crítica terrestre.

El servicio expone el método determinista `GovernanceAndSpinoffService.calculate_dual_use(spinoff_id, units)` servido por el endpoint `GET /api/v1/governance/fmea-and-spinoffs` (`backend/main.py`) y devuelve el objeto de valor inmutable `DualUseImpact` bajo las siguientes ecuaciones:

$$W_{\text{total}}(\text{id}, u) = w_{\text{unit}}(\text{id}) \times u, \qquad u \in \mathbb{Z} \cap [1,\, 10{,}000]$$

$$R(\text{id}) = r_{\text{mit}}(\text{id})\; [\%]$$

donde:
- $w_{\text{unit}}(\text{id})$ representa el ahorro unitario de masa en libras ($\text{lb}/\text{unidad}$; equivalencia SI: $1\text{ lb} = 0.4536\text{ kg}$),
- $u$ corresponde al lote de equipos desplegados (validado estrictamente como entero en $[1, 10{,}000]$, excluyendo valores booleanos o negativos mediante `ValueError`),
- $R(\text{id})$ expresa la reducción porcentual documentada de riesgo operativo o térmico atribuible al rediseño aeroespacial,
- `spinoff_id` acepta normalización de espacios y mayúsculas/minúsculas (con valor por defecto `"9582"` cuando se omite).

---

## 2. Catálogo Verificado de los 4 Spinoffs Oficiales NASA (`cases_and_spinoffs.json`)

| ID Spinoff | Año | Tecnología Terrestre y Origen Aeroespacial | Ahorro de Masa ($w_{\text{unit}}$) | Reducción de Riesgo ($R$) | Experimento PSI Vinculado (DOI) | Fuente Oficial NASA |
| :---: | :---: | :--- | :---: | :---: | :--- | :--- |
| **`9582`** | `1976` | **Fireman's Air Tanks (`COPV / PLSS`):** Elevó presión de servicio de `2,216` a `4,500 psi`, reduciendo el equipo `SCBA` de `33 lb` a `20 lb` (`-40%`) desde tanques compuestos del programa `Apollo` | `13.0 lb` (`5.90 kg`) | `40.0%` | `PSI-104` `SAFFIRE-V` (`10.60555/psi-104`) | [Spinoff Node 9582](https://spinoff.nasa.gov/node/9582) |
| **`9407`** | `1978` | **Incipient Fire Detector (`Space Shuttle / SAME`):** Discriminador submicrónico (`<0.1 um`) que detecta aerosoles por pirólisis antes de llama visible en minas y centros de datos | `0.0 lb` *(sensor neutro en masa)* | `58.0%` | `PSI-129` `SPICE` (`10.60555/psi-129`) | [Spinoff Node 9407](https://spinoff.nasa.gov/node/9407) |
| **`9918`** | `1977` | **Project `FIRES` / Trajes Ignífugos `PBI + Nomex`:** Textiles estructurados desarrollados tras `Apollo 1` que reducen el peso del equipo estructural en `>30%` sin encoger ni emitir gases tóxicos | `11.5 lb` (`5.22 kg`) | `35.0%` | `PSI-101` `SAFFIRE-II` (`10.60555/psi-101`) | [Spinoff Node 9918](https://spinoff.nasa.gov/node/9918) |
| **`PFE`** | `2010` | **ISS Portable Fire Extinguisher (`Fine Water Mist`):** Atomización de microgotas Sauter `20-100 um` segura para electrónica crítica con expansión vapor `1,700x`, sin `Halon` ni asfixia por $\text{CO}_2$ | `4.2 lb` (`1.91 kg`) | `65.0%` | `PSI-107` `CVB` (`10.60555/psi-107`) | [ISS Combustion Guide](https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/) |

---

## 3. Ejemplos de Escalamiento Cuantitativo por Flota Operativa

| Escenario Operativo Terrestre | Spinoff | Unidades ($u$) | Masa Ahorrada Total (`lb`) | Equivalente SI (`kg`) | Reducción de Riesgo | Trazabilidad `PSI` / `FMEA` |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Estación de bomberos municipal (equipos `SCBA` estándar) | `9582` | `25` | `325.0 lb` | `147.4 kg` | `40.0%` | `PSI-104` (`8.2-10.2 psi`, `30-34% O2`) |
| Brigada metropolitana (`SCBA` compuesto) | `9582` | `100` | `1,300.0 lb` | `589.7 kg` | `40.0%` | `PSI-104` / Mitigación ergonómica |
| Centro de datos o red hospitalaria (`<0.1 um`) | `9407` | `500` | `0.0 lb` | `0.0 kg` | `58.0%` | `PSI-129` (`FM-01` pirólisis `PTFE`) |
| Batallón con trajes estructurales `PBI + Nomex` | `9918` | `40` | `460.0 lb` | `208.7 kg` | `35.0%` | `PSI-101` (`FM-01` selección textil) |
| Subestación o sala limpia equipada con niebla `PFE` | `PFE` | `10` | `42.0 lb` | `19.1 kg` | `65.0%` | `PSI-107` / Árbol de supresión `I-06` |

---

## 4. Criterios de Validación y Seguridad (`OWASP` + `TDD`)

1. **Inmutabilidad y Determinismo:** `DualUseImpact` utiliza `@dataclass(frozen=True)` y redondea `weight_saved_lb_total` y `risk_reduction_pct` a dos decimales en `to_dict()`, asegurando consistencia exacta entre cálculo en Python y visualización en el panel web.
2. **Validación Estricta de Límites (`CWE-20`):**
   - `units` rechaza booleanos (`True`/`False`), tipos no enteros y valores fuera de `[1, 10000]` con `ValueError`.
   - En la capa API (`backend/main.py`), `spinoff_id` está restringido por esquema estricto al conjunto `{"9582", "9407", "9918", "PFE"}` (`422 Unprocessable Entity` ante identificadores arbitrarios).
   - En el servicio interno, cadenas con espacios o minúsculas (p. ej. `" pfe "`) se normalizan de forma segura y códigos inexistentes disparan `KeyError`.
3. **Cobertura TDD Independiente:** [test_dual_use_spinoffs_unit.py](../../tests/unit/test_dual_use_spinoffs_unit.py) ejecuta **13 pruebas unitarias** sobre inmutabilidad, escalamiento lineal de los 4 nodos, normalización de IDs, rechazo de booleanos/límites, existencia real de `PSI-104/129/101/107` y ausencia total de términos fuera del dominio `C-01`.
