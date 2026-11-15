# Protocolo Determinista de Supresion de Incendios en Entornos ECLSS (`PFE` vs $\text{CO}_2$ vs `E-FIELD`) — Tarea `I-06`

> **Proyecto:** AERO-IGNIS SI (`NASA Space Apps Challenge 2026`)  
> **Perfil Responsable:** Ingeniería de Gestión Industrial (`ind`)  
> **Alcance (`C-01`):** Exclusivamente módulos habitables presurizados (`ISS`, `Cygnus`, hábitats lunares $\ge 30\%\text{ O}_2$ y $\le 10.2\text{ psi}$) y transferencia terrestre Spinoff. Excluye propulsores y motores cohete.  
> **Implementación Verificada:** [`GovernanceAndSpinoffService.select_suppression_protocol`](../../backend/governance.py) · Pruebas TDD en [`tests/unit/test_suppression_protocol_unit.py`](../../tests/unit/test_suppression_protocol_unit.py).

---

## 1. Propósito y Naturaleza Determinista del Árbol

En un sistema cerrado de soporte vital y control ambiental (`ECLSS`), la selección de un agente extintor no depende únicamente de extinguir la llama visible, sino de evitar contaminación ácida irreversible, asfixia por desplazamiento gaseoso y daño secundario sobre la aviónica.

A diferencia de los clasificadores estadísticos del pipeline ML/DL (como `RandomForestClassifier` sobre `BASS-II`/`Saffire` o `flame_cnn.onnx`), el árbol de supresión `I-06` se modela como una **lógica de decisión 100% determinista e inmutable** (`SuppressionRecommendation`). Esta arquitectura elimina cualquier varianza estocástica en decisiones críticas de vida o muerte y garantiza trazabilidad auditable para ingeniería de seguridad (`NASA-STD-6001`) y enlace directo con las transiciones de contención de `DeterministicFsmController` (Mecatrónica `M-08`).

---

## 2. Árbol de Decisión Determinista (`select_suppression_protocol`)

La evaluación sigue un orden estricto de precedencia diseñado bajo principio de falla segura (*fail-safe*): validar la integridad de entrada, proteger contra eventos auto-oxidantes inmunes al corte de ventilación, habilitar mitigación sin consumo cuando aplica física electrohidrodinámica en microgravedad (`0g`), restringir $\text{CO}_2$ a volúmenes estrictamente aislados y prescribir niebla fina `PFE` como respaldo universal libre de haluros corrosivos.

```text
Entradas: fire_type (str), habitable_crew (bool = True), auto_oxidizing (bool = False)
   │
   ├─► [0] ¿fire_type.strip() == ""?
   │        └─ SÍ ──► raise ValueError("fire_type no puede estar vacio.")
   │
   ├─► [1] ¿auto_oxidizing == True O fire_type ∈ {"auto_oxidizing", "vika", "liclo4", "smoldering"}?
   │        └─ SÍ ──► AGENTE: PFE | eclss_safe = True
   │                  (Niebla fina 20-100 um; calor latente 2,260 kJ/kg;
   │                   enfriamiento en reacciones Vika/LiClO4 y brasas latentes)
   │
   ├─► [2] ¿fire_type ∈ {"laminar_diffusion", "electronic_clean", "efield"}?
   │        └─ SÍ ──► AGENTE: E-FIELD | eclss_safe = True
   │                  (Campo electrico +/-10 kV ACME PSI-154; viento ionico en 0g
   │                   sin consumo de agente ni sobrecarga de depuradores ECLSS)
   │
   ├─► [3] ¿habitable_crew == False Y fire_type ∈ {"uncrewed_rack", "cargo_co2"}?
   │        └─ SÍ ──► AGENTE: CO2 | eclss_safe = False
   │                  (Permitido unicamente en compartimento aislado no tripulado;
   │                   riesgo agudo de hipercapnia en volumen habitable)
   │
   └─► [4] Respaldo universal (incluye "halon", "halon_1301", incendios generales de cabina
            y solicitudes cargo_co2/uncrewed_rack cuando habitable_crew == True):
            └─────► AGENTE: PFE | eclss_safe = True
                    (Extintor estandar ISS PFE; seguro para avionica y libre de HF/HBr)
```

---

## 3. Matriz Comparativa Fisicoquímica y Toxicológica (`ECLSS`)

| Criterio Técnico | `PFE` (ISS Portable Fire Extinguisher) | `E-FIELD` (Supresión Electrohidrodinámica) | $\text{CO}_2$ (Dióxido de Carbono) | `Halon 1301` (Excluido en Cabina ISS) |
| :--- | :--- | :--- | :--- | :--- |
| **Mecanismo físico primario** | Atomización de niebla de agua fina (`20-100 um`); enfriamiento evaporativo (`2,260 kJ/kg`) y expansión a vapor `1,700x` | Viento iónico por campo eléctrico de alto voltaje (`+/-10 kV`) que deforma y extingue llamas laminares | Desplazamiento de $\text{O}_2$ e inhibición térmica diluyente | Inhibición química radicalaria de cadena |
| **Seguridad en volumen tripulado (`eclss_safe`)** | `True` — No tóxico, compatible con depuradores `ECLSS` | `True` — Cero emisión de residuos químicos o gases | `False` — Riesgo grave de hipercapnia e hipoxia tripulada | `False` — Prohibido por descomposición térmica en ácidos corrosivos |
| **Subproductos tóxicos en incendio** | Ninguno corrosivo | Ninguno (requiere control de arco en electrónica) | Acumulación directa de $\text{CO}_2$ en lazo cerrado | Liberación de fluoruro y bromuro de hidrógeno (`HF` / `HBr`) |
| **Efectividad en fuego auto-oxidante (`Vika` / $\text{LiClO}_4$)** | **Alta** (`FM-05`): enfría la fuente sólida cuando cortar `HVAC` falla | Insuficiente ante dardos auto-oxidantes presurizados | Insuficiente: la combustión genera su propio $\text{O}_2$ | Ineficaz e inseguro por acidez secundaria |
| **Impacto en aviónica crítica** | Seguro a dosis certificada por baja conductividad inicial y evaporación rápida | Óptimo en recintos limpios sin masa extintora consumible | Seguro eléctricamente, pero restringido a racks herméticos sin personal | Corrosión acelerada sobre tarjetas electrónicas y sellos |
| **Respaldo científico PSI / Fuente** | `PSI-105` (`10.60555/psi-105`), `PSI-107` (`10.60555/psi-107`), `PSI-108` (`10.60555/psi-108`), Spinoff `PFE` | `PSI-154` `ACME-E-FIELD` (`10.60555/psi-154`) | `PSI-27` `FLEX-2` (`10.60555/psi-27`, mezcla controlada de diluyentes) | Referencia histórica de rechazo ISS frente a `PFE` |

---

## 4. Justificación por Escenarios Forenses y Modos de Falla (`FMEA`)

1. **Prioridad 1 — Combustión Auto-Oxidante y Latente (`FM-04`, `FM-05`):**  
   El incidente de la estación espacial `Mir` (1997, cartucho `SFOG Vika` con perclorato de litio $\text{LiClO}_4$) demostró que apagar la ventilación `HVAC` no extingue una reacción generadora de oxígeno. Del mismo modo, la combustión latente (*smoldering*, `PSI-110`, `10.60555/psi-110`) acumula monóxido de carbono ($\text{CO}$) y puede re-encenderse violentamente al restablecer flujo. Por ello, la rama `[1]` del árbol impone `PFE` independientemente del parámetro `habitable_crew` o del subtipo de rack.

2. **Prioridad 2 — Llamas Laminares de Difusión y Electrónica Limpia (`PSI-154`):**  
   Los experimentos `ACME-E-FIELD` (`PSI-154`, DOI `10.60555/psi-154`) en la facilidad `ISS-CIR` (`21.0–30.0% O2`, `14.7 psi`, flujo hasta `12.0 cm/s`) demostraron que los campos eléctricos de `+/-10 kV` deforman la zona de reacción mediante viento iónico en microgravedad sin consumir masa extintora ni saturar filtros del `ECLSS`. La rama `[2]` habilita `E-FIELD` siempre que no exista oxidante interno (`auto_oxidizing=False`).

3. **Prioridad 3 — Contención Gaseosa con $\text{CO}_2$ en Carga o Racks No Habitados (`PSI-27`):**  
   Aunque `FLEX-2` (`PSI-27`, DOI `10.60555/psi-27`) caracteriza concentraciones diluyentes de $\text{CO}_2$, $\text{N}_2$, $\text{He}$ y $\text{Xe}$ para extinguir llamas calientes y frías (`PSI-24`, DOI `10.60555/psi-24`, `500-800 K`), liberar $\text{CO}_2$ en una cabina tripulada induce hipercapnia en minutos. El árbol bloquea `CO2` siempre que `habitable_crew=True`, redirigiendo la operación al respaldo seguro `PFE`, y marca explícitamente `eclss_safe=False` cuando se autoriza en compartimentos aislados no tripulados (`uncrewed_rack`, `cargo_co2`).

4. **Prioridad 4 — Prohibición de `Halon 1301` y Respaldo Universal `PFE` (`FM-01`, `PSI-107`, `PSI-129`):**  
   Los ensayos con polímeros en `SAFFIRE-VI` (`PSI-105`, DOI `10.60555/psi-105`) y pirólisis de cables `PTFE` (`>500 °C`, `FM-01`, `PSI-129` `10.60555/psi-129`) evidencian la liberación de especies fluoradas altamente tóxicas (`HF`). El uso de `Halon 1301` agravaría la acidificación por `HF` y `HBr` dentro del circuito cerrado. En consecuencia, entradas como `halon` o `halon_1301` convergen al agente `PFE` (`eclss_safe=True`), aprovechando gotas Sauter de `20-100 um` y la transferencia evaporativa interfacial estudiada en `CVB` (`PSI-107`, DOI `10.60555/psi-107`) y `CVB-2` (`PSI-108`, DOI `10.60555/psi-108`).

---

## 5. Verificación TDD e Integración de Sistema

La especificación queda cubierta por **17 pruebas unitarias aisladas** en [`tests/unit/test_suppression_protocol_unit.py`](../../tests/unit/test_suppression_protocol_unit.py) bajo ciclo estricto `RED -> GREEN -> REFACTOR`:

- Inmutabilidad de `SuppressionRecommendation` (`FrozenInstanceError`).
- Anulación forzada a `PFE` en escenarios `auto_oxidizing`, `vika`, `liclo4` y `smoldering`.
- Selección de `E-FIELD` únicamente cuando `auto_oxidizing=False` para `laminar_diffusion`, `electronic_clean` y `efield`.
- Bloqueo incondicional de `CO2` cuando `habitable_crew=True` y emisión con advertencia `eclss_safe=False` únicamente en `habitable_crew=False`.
- Rechazo seguro de `halon` / `halon_1301` hacia `PFE` libre de `HF/HBr`.
- Validación temprana (`ValueError`) ante cadenas vacías o espacios en `fire_type`.

Con el cierre de `I-06`, la ruta industrial se integra directamente con la siguiente tarea **`I-07`** (Calculadora de Impacto *Dual-Use* de los Spinoffs `9582`, `9407`, `9918` y `PFE`).
