# Reglas de Interpretación Determinista y Plantillas `writing-craft` — Tarea `I-08`

> **Proyecto:** AERO-IGNIS SI (`NASA Space Apps Challenge 2026`)  
> **Perfil Responsable:** Ingeniería de Gestión Industrial (`ind`)  
> **Alcance (`C-01`, `C-02`):** Síntesis extractiva 100% local (`$0 USD`, sin APIs LLM externas) sobre investigaciones en cabinas habitables y Spinoffs terrestres.  
> **Implementación Verificada:** [`ExtractiveNlpEngine.summarize_for_persona`](../../backend/ranking_nlp.py) · Pruebas TDD en [`tests/unit/test_ranking_and_writing_unit.py`](../../tests/unit/test_ranking_and_writing_unit.py).

---

## 1. Principio de Síntesis Determinista (*Zero-Hallucination*)

Para eliminar alucinaciones numéricas y garantizar trazabilidad científica ante el jurado, la generación textual de `AERO-IGNIS SI` prescinde de modelos generativos externos. En su lugar, combina extracción no supervisada con plantillas deterministas parametrizadas:

$$S_{\text{comb}}(i) = 0.70 \cdot C_i^{\text{TOPSIS}} + 0.30 \cdot \cos\big(\mathbf{v}_{\text{query}}, \mathbf{v}_{\text{TF-IDF}, i}\big)$$

1. Se ordenan las 24 investigaciones por $S_{\text{comb}}(i)$ y se toma el subconjunto candidato superior (`top_pool` de 6 estudios).
2. Un grafo de similitud TF-IDF ejecuta **centralidad TextRank** ($d = 0.85$, 12 iteraciones) para elegir los 3 estudios representativos (`primary`, `secondary`, `tertiary`) junto con sus `doi` (`10.60555/...`) reales.
3. El método auxiliar `_resolve_topsis_and_driver` extrae el índice exacto `TOPSIS` del estudio líder y la variable física dominante desde `feature_importance` (o, en su ausencia, el criterio multicriterio principal de la investigación).

---

## 2. Mapeo Explicable de *Feature Importance* y Criterios TOPSIS

| Clave de Entrada (`ML / TOPSIS`) | Etiqueta Normalizada en Español | Fuente del Dato |
| :--- | :--- | :--- |
| `o2_pct` | `concentracion de O2` | Importancia de variables (`RandomForestClassifier` / `GBR`) |
| `pressure_psi` | `presion de cabina` | Importancia de variables (`BASS-II` / `Saffire`) |
| `flow_cm_s` | `flujo de ventilacion` | Importancia de variables (`BASS-II` / `Saffire`) |
| `gravity_g` | `nivel de gravedad` | Importancia de variables (`0g`, `0.16g`, `0.38g`, `1g`) |
| `thickness_mm` | `espesor de muestra` | Importancia de variables (`Sample Thickness`) |
| `habitat` *(fallback sin FI)* | `seguridad en cabina habitable` | Puntuación curada en `psi_combustion_24.json` |
| `modeling` *(fallback sin FI)* | `calibracion adimensional` | Puntuación curada en `psi_combustion_24.json` |
| `sensors` *(fallback sin FI)* | `deteccion de llama y humo` | Puntuación curada en `psi_combustion_24.json` |
| `spinoff` *(fallback sin FI)* | `impacto dual-use` | Puntuación curada en `psi_combustion_24.json` |

---

## 3. Reglas Editoriales `writing-craft` por Audiencia

| Audiencia (`persona`) | Registro Editorial | Restricciones Estructurales | Uso de Evidencia y Unidades |
| :--- | :--- | :--- | :--- |
| **`Investigador`** | **`academic`** | Verbos calibrados (`indica`, `sugiere`, `identifica`, `es consistente con`); cero lenguaje promocional | Cita `TOPSIS` ($C_i$), predictor dominante (`%`), rangos exactos (`% O2`, `cm/s`, `psi`), límites $\text{Da}/\text{Pe}$ y todos los `doi` `10.60555/...` |
| **`Estudiante`** | **`plain`** | **Todas las oraciones $< 25$ palabras**, voz activa directa, sin jerga innecesaria | Explica física `0g` (ausencia de convección caliente), `TOPSIS`, factor clave, beneficio terrestre y sensor recomendado (`primary.sensors[0]` con respaldo seguro) |
| **`Gestor Industrial`** | **`plain + proposal`** | Orientado a decisión cuantitativa, mitigación de riesgo y retorno terrestre medible | Conecta `TOPSIS` + predictor dominante con reducción de `NPR` (`FMEA NASA-STD-6001`), protocolo `PFE` (`I-06`) y transferencia `Spinoff` (`I-07`) |

---

## 4. Salvaguardas Anti-*AI Slop* y Verificación TDD

1. **Bloqueo Léxico (`BANNED_AI_SLOP`):** Ninguna salida puede contener fórmulas vacías como *"en el panorama actual"*, *"sin fisuras"*, *"piedra angular"*, *"cambio de paradigma"*, *"revolucionario/a"*, *"demuestra universalmente"*, *"game-changer"* o *"paradigm shift"*.
2. **Integridad de Citas y Dominio (`C-01`):** Cada `PSI-ID` y `DOI` presente en `bullets`, `evidence_ids` y `cited_dois` proviene exclusivamente del catálogo validado `data/psi_combustion_24.json`; las entradas vacías (`ranked=[]`) o audiencias fuera de `VALID_PERSONAS` disparan `ValueError` explícito.
3. **Verificación Automatizada (`4` pruebas en [test_ranking_and_writing_unit.py](../../tests/unit/test_ranking_and_writing_unit.py)):**
   - Determinismo y latencia `< 50 ms` de `TopsisMultiCriteriaRanker`.
   - Cumplimiento de longitud `< 25` palabras/oración en `Estudiante`, validez de `DOI` y ausencia de *AI slop* en las 3 audiencias.
   - Inyección determinista de `TOPSIS` y `feature_importance` + rechazo de `ranked=[]` y audiencia inválida.
