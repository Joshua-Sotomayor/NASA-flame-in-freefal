---
type: engineering-standard
skills: [test-driven-development, writing-craft, security-and-hardening, ponytail]
tags: [nasa/tdd, writing-craft, pytest, integration-tests, anti-slop]
---

# Estrategia TDD (Piramide Unitaria e Integracion) y Disciplina `writing-craft`

Este documento integra las dos skills solicitadas desde `Obsidian Vault/agents` antes de pasar a la fase de codigo (`Task 1`). Ver el grafo compilado: `![[grafos/tdd_sdd_architecture.svg]]`.

---

## 1. Integracion de `test-driven-development` (Calidad de Software)

Ninguna funcion de fisica, modelo ML, regla de FSM, frontera de seguridad o endpoint REST se implementa sin su prueba que falle primero (**RED -> GREEN -> REFACTOR**). Para bugs descubiertos durante el hackathon se aplica el **patron Prove-It**: reproducir el bug en un test que falle antes de tocar la implementacion.

### Piramide de Pruebas para AERO-IGNIS SI (`pytest`)

```text
          /\            E2E (~5% — Large)
         /  \           Navegador / Chrome DevTools: flujo completo <3 min, LCP <2.5s
        /----\
       /      \         Integracion (~15% — Medium)
      /--------\        tests/integration/: FastAPI TestClient <-> POO, SHA-256, 413/422/429
     /          \
    /------------\      Unitarias (~80% — Small, <10ms c/u, sin red ni disco externo)
   /______________\     tests/unit/: Fisica Da/Pe, FSM, TOPSIS, TextRank, writing-craft, Sanitizer
```

### Matriz de Pruebas por Modulo (Unitarias vs. Integracion)

| Modulo / Clase POO | Pruebas Unitarias (`tests/unit/`, Aisladas, ms) | Pruebas de Integracion (`tests/integration/`, Fronteras reales) |
| :--- | :--- | :--- |
| **`SecurityBoundaryGuard`** | Limite de `RateLimiter` en ventana deslizante; sanitizador XSS/SQLi; rechazo de hosts SSRF no permitidos. | `FastAPI TestClient` devolviendo `413` si payload `> 16 KB`, `429` ante rafaga, `422` ante `extra="forbid"`, e `IntegrityError` si se altera 1 byte de un `.joblib`/`.onnx`. |
| **`PsiRepository`** | Inmutabilidad de `PsiInvestigation` (`frozen`), filtros por instalacion y paginacion acotada (`pageSize <= 50`). | Carga real de `data/psi_combustion_24.json` verificando 24 IDs unicos, DOIs `10.60555` y bloqueo SSRF real en `OsdrApiClient`. |
| **`DimensionlessPhysicsCalculator` + `FlammabilityPredictor`** | Calculo exacto de $\text{Da}$, $\text{Pe}$, $V_f$; monotonía de riesgo al subir $\% \text{O}_2$; bordes de *quenching* vs *blowoff*. | Carga real de `flammability_rf.joblib` y `burntime_gbr.joblib` via `/api/v1/sandbox/predict-flammability` validando presets Apollo 1, Apollo 13 y Mir. |
| **`DuctSafetyOrchestrator` + `DeterministicFsmController`** | Transiciones `NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA`; histeresis temporal; bloqueo de rearme ante llama fria; corte inmediato por `comm_ok=False`. | Carga real de `flame_cnn.onnx` con `onnxruntime` + `sensor_tree.joblib` via `POST /api/v1/twin/step-fsm` validando salida JSON exacta. |
| **`TopsisMultiCriteriaRanker` + `ExtractiveNlpEngine`** | Determinismo del ranking ante cambios de pesos; extraccion `TextRank` y validacion de cero IDs PSI inventados ni *AI slop*. | Carga real de `psi_tfidf_kmeans.joblib` via `POST /api/v1/psi/rank-and-interpret` probando las 3 audiencias (`Investigador`, `Estudiante`, `Gestor`). |
| **`GovernanceAndSpinoffService`** | Formula `NPR = S * O * D` antes/despues de controles y calculo de ahorro de peso SCBA/PBI. | Contrato `GET /api/v1/governance/fmea-and-spinoffs` y validacion de alcance `C-01` (cero terminos de cohetes/propulsores). |

### Reglas Operativas de TDD en el Equipo
- **Test de Estado, no de Interaccion:** Verificar el resultado devuelto y cambios de estado observable (no espiar llamadas internas salvo fronteras externas).
- **DAMP sobre DRY en Tests:** Cada caso de prueba describe claramente el escenario fisico o de seguridad sin ocultar datos en *helpers* opacos.
- **Implementaciones Reales > Fakes > Stubs > Mocks:** Usar modelos reales ligeros y el `TestClient` real; reservar mocks unicamente para timeouts de la API externa NASA OSDR.

---

## 2. Integracion de `writing-craft` (Skill de Redaccion y Rigor Tecnico)

`writing-craft` gobierna dos capas criticas del proyecto: toda nuestra documentacion/pitch (**Build-Time**) y la salida generada por las plantillas deterministas del motor **SI (`ExtractiveNlpEngine`)** (**Run-Time**).

### Jerarquia de Resolucion
1. **Integridad de Citas y Datos (Prioridad maxima):** Prohibido alterar, redondear o inventar cifras, unidades ($\text{psi}, \text{kPa}, \text{cm/s}, \%\text{O}_2$), DOIs (`10.60555/...`) ni identificadores PSI.
2. **Precision sin Grandilocuencia:** Cada afirmacion empirica se ata a su experimento (`BASS-II`, `Saffire-V`, `FLEX`) o norma (`NASA-STD-6001`).

### Los 3 Modos Aplicados al Proyecto

| Audiencia / Contexto | Modo `writing-craft` | Reglas Concretas Aplicadas |
| :--- | :--- | :--- |
| **Perfil `Investigador` + `SPEC.md` + Fichas Cientificas** | **`academic`** | Verbos calibrados (*"indica"*, *"es consistente con Table 2 de BASS-II"* en lugar de *"demuestra universalmente"*). Preservar incertidumbre cientifica (*"podria reactivarse"*) y notacion $\text{Da}/\text{Pe}$ verbatim. |
| **Perfil `Estudiante` + `README.md` + Textos UI** | **`plain`** | Oraciones $< 25$ palabras; verbos activos directos en lugar de nominalizaciones (*"evaluar"* en lugar de *"realizar una evaluacion"*); una idea por oracion. |
| **Perfil `Gestor Industrial` + Guion de Pitch (30s / 2min)** | **`plain` + `proposal` (`style-edit`)** | Vincular metas operativas con evidencia preliminar y costo/impacto (`NPR`, `-40% peso SCBA`, `PFE`), respetando la voz tecnica propia del equipo sin muletillas roboticas. |

### Filtro Determinista Anti-*AI Slop* (`references/ai-tells-es-en.md`)
Antes de cerrar cualquier plantilla de texto SI o documento `README`/Deck, verificamos (incluso mediante test unitario en `tests/unit/test_writing_craft_quality.py`) la ausencia de:
- **Aperturas teatrales / rellenos:** *"En el panorama actual..."*, *"Sin mas preambulos..."*, *"Cabe destacar que..."*, *"Let's dive in"*.
- **Vocabulario inflado:** *revolucionario, cambio de paradigma, piedra angular, sin fisuras, intrincado, apalancar, de suma importancia, groundbreaking, seamless, tapestry, delve*.
- **Falsos contrastes y triadas forzadas:** *"No se trata solo de X, sino de Y"* cuando nadie afirmo X; adjetivos en grupos mecanicos de tres (*"rapido, seguro y escalable"*).
- **Residuos de formato artificial:** encabezados en Title Case decorativo en espanol (usar estilo oracion: `## Estrategia de pruebas`), abuso de rayas (`—`) o listas donde la negrita repite la primera palabra.
