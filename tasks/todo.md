# Backlog Auditable de Implementación — AERO-IGNIS SI (`tasks/todo.md`)

> **Regla de Ejecución (SDD + TDD Piramidal + `writing-craft` + Ponytail + Seguridad):** Cada tarea sigue el bucle **RED $\rightarrow$ GREEN $\rightarrow$ REFACTOR** (`~80%` Pruebas Unitarias en `tests/unit/` + `~15%` Pruebas de Integración en `tests/integration/`), redacta salidas textuales sin *AI slop* (`writing-craft`) y se cierra con un commit `<version> - <verbo> - <descripción>` en su rama temática hacia `dev`.

---

## Estado Actual del Ciclo
- [x] **Pre-Fase (Gate 1 Docs + Base Obsidian + GitHub):**
  - Remoto GitHub conectado (`origin`), licencia `MIT` (`LICENSE`) sincronizada en `main` (`0.1.1`) y `dev` (`0.2.3`).
  - Hub de Skills vinculado en [.agents/skills.json](file:///C:/Users/hp/OneDrive/Documentos/NASA/.agents/skills.json) (incluyendo **`writing-craft`** y **`test-driven-development`**).
  - Base de conocimiento completa en `Obsidian Vault\Proyectos\NASA_Flame_In_Freefall\` (24 fichas PSI, 10 nodos, Canvas, 3 grafos Graphviz `.dot/.svg/.png`) y notebook GPU [notebooks/AERO_IGNIS_Colab_Training.ipynb](file:///C:/Users/hp/OneDrive/Documentos/NASA/notebooks/AERO_IGNIS_Colab_Training.ipynb).
  - [SPEC.md](file:///C:/Users/hp/OneDrive/Documentos/NASA/SPEC.md) v1.1.0 y War Room [planning/index.html](file:///C:/Users/hp/OneDrive/Documentos/NASA/planning/index.html) actualizados.
- [x] **Aprobación Humana de `SPEC.md` v1.1.0:** Aprobado para iniciar la ejecución por *vertical slices* TDD.

---

## Fase 1: Cimientos de Datos y Seguridad (Viernes `H0–H4`)

### [x] Task 1 (`M-02` + `I-01` / `M-08`): Repositorio de Dominio POO y Dataset Maestro de las 24 PSI
- **Responsable:** Mecatrónico (POO `PsiRepository`) + Gestión Industrial (taxonomía y 10 recursos).
- **Alcance:** Crear `data/psi_combustion_24.json`, `data/bass_saffire_runs.csv` (muestras calibradas `BASS-II` 17 cols y `Saffire-I` 13 cols), `data/cases_and_spinoffs.json` y `backend/domain.py` (`PsiInvestigation`, `PsiRepository`, `OsdrApiClient` allowlisted).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_domain_unit.py`):** Inmutabilidad de `PsiInvestigation` (`frozen`), conteo exacto de 24 PSI únicas, paginación `pageSize <= 50` y bloqueo regex anti-SSRF en URLs ajenas a OSDR.
  - **Integración (`tests/integration/test_domain_repo_int.py`):** Lectura real de `data/psi_combustion_24.json` + `data/bass_saffire_runs.csv` y simulación de timeout OSDR con fallback local silencioso.
- **Verificación:** `pytest tests/unit/test_domain_unit.py tests/integration/test_domain_repo_int.py -v`
- **Commit Git:** `0.3.0 - add - estructurar dataset psi de 24 investigaciones y casos forenses con pruebas`

### [x] Task 2 (`S-Sec` / Transversal): Módulo `SecurityBoundaryGuard` (Anti-DDoS, Anti-Inyección, SHA-256)
- **Responsable:** Mecatrónico.
- **Alcance:** Implementar `backend/security.py` con `RateLimiter` por ventana deslizante, `PayloadSizeMiddleware` (`16 KB` max), sanitizador/validador estricto, `SecurityHeadersMiddleware` (`CSP`, `DENY`, `nosniff`) y `ModelIntegrityVerifier` (`SHA-256`).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_security_unit.py`):** Lógica de ventana deslizante en `RateLimiter`, sanitización de cadenas XSS/SQLi y cómputo/fallo de digest `SHA-256`.
  - **Integración (`tests/integration/test_security_int.py`):** Frontera FastAPI devolviendo HTTP `413` (`>16 KB`), `429` (ráfaga IP), `422` (`extra="forbid"` / XSS / SQLi) e `IntegrityError` al alterar 1 byte en un artefacto de prueba.
- **Verificación:** `pytest tests/unit/test_security_unit.py tests/integration/test_security_int.py -v`
- **Commit Git:** `0.4.0 - feat - implementar capa security guard anti ddos anti inyeccion y sha256`

## Checkpoint 1 (Cimientos)
- [x] Todas las pruebas unitarias e de integración de `domain` y `security` pasan al 100%.
- [x] Revisión rápida con `git diff --staged -i -G'password|secret|api_key|token'`.

---

## Fase 2: Pipeline 100% ML/DL Propio (Colab / Local) & Motor Físico/FSM (Sábado AM `H5–H14`)

### [x] Task 3 (`M-07`): Entrenamiento Reproducible de los 3 Modelos Propios + Manifiesto SHA-256
- **Responsable:** Mecatrónico (entrenamiento Colab/Local + ONNX) + Gestión Industrial (sensibilidad y auditoría).
- **Alcance:** Implementar `backend/train_models.py` (CPU local `< 5 s`) sincronizado con `notebooks/AERO_IGNIS_Colab_Training.ipynb` (GPU T4 para *streaming* OSDR) generando `artifacts/models/manifest.sha256.json`:
  1. `flammability_rf.joblib` (`RandomForestClassifier`) + `burntime_gbr.joblib` (`GradientBoostingRegressor`).
  2. `flame_cnn.onnx` (PyTorch `FlameCnn` 4 clases) + `sensor_tree.joblib` (`DecisionTreeClassifier`).
  3. `psi_tfidf_kmeans.joblib` (`TfidfVectorizer` + `PCA` + `KMeans` sobre las 24 PSI).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_training_unit.py`):** Forma del tensor de entrada CNN `(1, 1, 64, 64)`, pesos totales `< 15 MB` y estructura válida de `manifest.sha256.json`.
  - **Integración (`tests/integration/test_models_integrity_int.py`):** Ejecución real de `train_models.py` + carga real vía `onnxruntime.InferenceSession` y `joblib.load` validados por `ModelIntegrityVerifier`.
- **Verificación:** `python -m backend.train_models && pytest tests/unit/test_training_unit.py tests/integration/test_models_integrity_int.py -v`
- **Commit Git:** `0.5.0 - feat - entrenar pipeline ml propio random forest cnn onnx y clustering tfidf`

### [x] Task 4 (`M-03` + `I-05`): `DimensionlessPhysicsCalculator` + `FlammabilityPredictor` + Presets Forenses
- **Responsable:** Mecatrónico + Gestión Industrial.
- **Alcance:** Implementar `backend/physics_ml.py` en POO uniendo ecuaciones ($\text{Da}$, $\text{Pe}$, $V_f$) con `RandomForest`/`GBR` y los 3 presets (**Apollo 1**, **Apollo 13**, **Mir**).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_physics_unit.py`):** Cálculos $\text{Da}/\text{Pe}$, monotonía al subir $\% \text{O}_2$, regímenes *Radiative Quenching* vs *Blowoff* y datos exactos de Apollo 1 ($100\%\text{ O}_2, 16.7\text{ psi}$).
  - **Integración (`tests/integration/test_flammability_int.py`):** Inferencia real con `.joblib` verificando retorno de `feature_importance` para Hábitat Lunar ($34\%\text{ O}_2, 8.2\text{ psi}$) y Apollo 1.
- **Verificación:** `pytest tests/unit/test_physics_unit.py tests/integration/test_flammability_int.py -v`
- **Commit Git:** `0.6.0 - feat - implementar motor fisico adimensional y predictor random forest en poo`

### [x] Task 5 (`M-04` + `M-05`): `DuctSafetyOrchestrator` (CNN ONNX + Decision Tree + FSM Determinista)
- **Responsable:** Mecatrónico y Control.
- **Alcance:** Implementar `backend/duct_twin.py` con `OnnxFlameVisionModel`, `SensorDecisionTreeModel` y `DeterministicFsmController` (`NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA` con histéresis temporal e interlock `comm_ok=False`).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_fsm_unit.py`):** Cada transición de estado, contador de histéresis (evita falsos disparos), bloqueo de rearme ante llama fría NTC (`FLEX`) y disparo inmediato a `FALLA_SEGURA` si `comm_ok=False`.
  - **Integración (`tests/integration/test_duct_orchestrator_int.py`):** Pipeline completo `flame_cnn.onnx` + `sensor_tree.joblib` + `DeterministicFsmController` exponiendo `tree_rule_path` y `cnn_probs[4]`.
- **Verificación:** `pytest tests/unit/test_fsm_unit.py tests/integration/test_duct_orchestrator_int.py -v`
- **Commit Git:** `0.6.1 - feat - implementar orquestador fsm determinista con cnn onnx y arbol de sensores`

### [x] Task 6 (`I-02` + `I-04` + `I-06` + `I-07` + `I-08`): Ranking TOPSIS, NLP (`writing-craft`) y Gobernanza FMEA/Spinoffs
- **Responsable:** Gestión Industrial + Mecatrónico.
- **Alcance:** Implementar `backend/ranking_nlp.py` (`TOPSIS/AHP + TF-IDF/TextRank/K-Means` + plantillas **`writing-craft`** para Investigador `academic`, Estudiante `plain` y Gestor `plain+proposal`) y `backend/governance.py` (`FMEA NASA-STD-6001`, protocolo `PFE/CO2/E-FIELD` y calculadora `Dual-Use` para Spinoffs `9582, 9407, 9918`).
- **Pruebas TDD (Escribir RED primero):**
  - **Unitarias (`tests/unit/test_ranking_and_writing_unit.py`):** Determinismo TOPSIS, fórmulas FMEA (`NPR`) / Spinoff (-40% peso SCBA) y **reglas anti-*AI slop* (`writing-craft`)** (prohibido inventar IDs PSI o incluir muletillas de `ai-tells-es-en.md`).
  - **Integración (`tests/integration/test_ranking_governance_int.py`):** Carga real de `psi_tfidf_kmeans.joblib` + `PsiRepository` + `GovernanceAndSpinoffService` en las 3 audiencias.
- **Verificación:** `pytest tests/unit/test_ranking_and_writing_unit.py tests/integration/test_ranking_governance_int.py -v`
- **Commit Git:** `0.6.2 - feat - implementar ranking topsis textrank writing-craft y gobernanza fmea spinoffs`

## Checkpoint 2 (Core ML/DL, Física & TDD)
- [x] Gate 2 (`J-02`): 100% de pruebas unitarias e de integración en verde sin red externa.

---

## Fase 3: API Blindada & Dashboard Web Interactivo (Sábado PM `H15–H26`)

### [x] Task 7 (`S-API`): Ensamblaje FastAPI POO y Pruebas de Contrato/Abuso (Integración)
- **Responsable:** Mecatrónico.
- **Alcance:** Crear `backend/main.py` conectando todas las clases POO, `SecurityBoundaryGuard` y rutas `/api/v1/*`.
- **Pruebas TDD (`tests/integration/test_api_contracts_int.py`):**
  - Todas las rutas responden según los DTOs de `SPEC.md` (`extra="forbid"`), aplican cabeceras `CSP/DENY/nosniff` y rechazan ataques simulados (`413`, `422`, `429`).
- **Verificación:** `pytest tests/integration/test_api_contracts_int.py -v`
- **Commit Git:** `0.7.0 - feat - ensamblar api fastapi poo con contratos estrictos y proteccion owasp`

### [x] Task 8 (`M-06` + `M-09` + `U-01`): Dashboard Web WAI-ARIA + Gemelo Digital Isométrico SVG (`anatomy`)
- **Responsable:** Mecatrónico + Gestión Industrial (QA textos `writing-craft` y unidades).
- **Alcance:** Crear `frontend/` (`index.html`, `styles.css`, `app.js`) con los 4 módulos integrados, animaciones GPU `60fps`, contraste WCAG AA y cero `innerHTML` inseguro.
- **Pruebas TDD + E2E (~5% Pirámide):**
  - Verificación en navegador (`0` errores de consola, carga DOM `691 ms`, navegación por teclado y recorrido completo por los 4 módulos + Hardware Blueprint).
- **Commit Git:** `0.8.0 - design - construir dashboard web aero ignis con gemelo digital svg contorno e interlock blueprint`

## Checkpoint 3 (MVP MUST-HAVE)
- [x] Gate 3 (`J-03`): Flujo E2E completo de los 4 módulos verificado en navegador.

---

## Fase 4: Blueprint Físico, Auditoría, Despliegue y Pitch (Domingo `H27–H48`)

### [x] Task 9 (`M-10` + `I-09` + `I-10`): Pestaña *Hardware Blueprint*, QA `writing-craft` y `README.md`
- **Criterios:** Evidencias `SolidWorks/EPLAN/Proteus` integradas en pestaña Blueprint (`M-10` listo), cero contenido de motores cohete (`C-01`), QA de unidades (`I-09`), los 10 recursos NASA citados y `README.md` auditado con `writing-craft` (`I-10`).
- **Commit Git:** `0.9.11 - merge - consolidar ramas industriales i01 a i10 y mecatronica m14 en dev`

### [x] Task 10 (`M-11`): Auditoría `/ponytail-audit` + Suite TDD Completa & Offline
- **Criterios:** Pirámide completa `pytest tests/unit tests/integration -v` al 100% (`33 passed`), JS limpio (`node --check frontend/app.js`), auditoría anti-slop / cero código muerto / seguridad OWASP verificada.
- **Commit Git:** `0.9.1 - test - validar suite tdd completa offline y auditoria ponytail`

### [x] Task 10B (`M-13` + pulido `M-14` `0.9.4` — Completada · Mecatrónica): Refactor Visual, Paleta NASA e Interactividad Web (UI/UX)
- **Responsable:** Mecatrónico y de Control (`meca`).
- **Ramas:** `feat/meca-m13-ui-refactor` (`0.9.3`) $\rightarrow$ `feat/meca-m14-ux-nasa-palette` (`0.9.4`).
- **Módulos / Archivos:** `frontend/*`, `frontend/assets/museum/*`, `backend/main.py`, `backend/train_models.py`, `backend/ranking_nlp.py`, `backend/physics_ml.py`, `requirements/*`, `requirements.txt`, `tests/integration/test_frontend_and_audit_int.py`.
- **Alcance:** Cabecera centrada `NASA [Logo] + ENREDADOS` en `Geist Pixel` con sombras en capas, paleta fría azul/rojo del emblema NASA y cursiva editorial; eliminación de insignias técnicas del encabezado; pestaña `01 Museo y Glosario` al inicio; mapa PCA sin solapes de texto con líneas guía y aro #1; selector curado de temas y sliders en tiempo real alineados al estudio #1; contorno dinámico de inflamabilidad y factores de influencia sensibles al escenario; comparador FMEA (`NPR base` vs `activo`), redacción humanizada `writing-craft` y veredicto triple de agente extintor.
- **Commits Git:** `0.9.3 - refactor - redisenar interfaz web nasa enredados con mini museo glosario y arranque directo` y `0.9.4 - refactor - pulir interactividad ux paleta nasa sombras cursivas y orden de museo`

### [ ] Task 11 (`M-12` + `J-04`): Despliegue Público HTTPS y Tag `v1.0.0` en `main` (`origin` GitHub)
- **Responsable:** Mecatrónico (`M-12`) + Conjunta (`J-04`).
- **Rama dedicada:** `feat/meca-m12-deploy-render-netlify` $\rightarrow$ `release/v1.0.0`
- **Módulos / Archivos bloqueados (Lock):** `Dockerfile`, `render.yaml`, `netlify.toml` (o `_redirects` proxy `/api/*`), `backend/main.py` (CORS), `backend/security.py`, `frontend/app.js`.
- **Criterios:** Despliegue en **Render** (todo-en-uno FastAPI + `frontend/`) o **Netlify (CDN `frontend/`) + Render (API FastAPI)** a `$0 USD`, merge `dev -> main`, tag `v1.0.0`, push a `origin` y URL HTTPS verificada en modo incógnito.
- **Commit Git:** `1.0.0 - ship - liberar plataforma aero-ignis si v1.0.0 en produccion`

### [ ] Task 12 (`I-11` + `I-12` + `J-05` + `J-06`): Deck 7 Slides, Video Demo 1080p y Envío Oficial
- **Responsable:** Gestión Industrial (`I-11`, `I-12`) + Conjunta (`J-05`, `J-06`).
- **Criterios:** Video exportado (`30s`/`2min`), envío completado 2h antes del cierre en Space Apps.

---

## Mapa de Propiedad de Módulos, Bloqueos y Ramas (Pendientes Multi-Perfil)

> Regla: antes de trabajar, todo nuevo chat pregunta el perfil activo (`meca` / `ind` / `joint`) y respeta los archivos bloqueados por cada rama. Los archivos del tablero ([planning/index.html](planning/index.html), [tasks/todo.md](tasks/todo.md)) solo se editan al cerrar una tarea tras `git pull --rebase origin dev`.

| ID | Perfil | Rama Dedicada | Módulos / Archivos Bloqueados (*Lock*) | Estado |
| :--- | :---: | :--- | :--- | :---: |
| **`M-13`** | `meca` | `feat/meca-m13-ui-refactor` $\rightarrow$ `feat/meca-m14-ux-nasa-palette` | `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`, `tests/integration/test_frontend_and_audit_int.py` | **Listo [x]** |
| **`M-12`** | `meca` | `feat/meca-m12-deploy-render-netlify` | `Dockerfile`, `render.yaml`, `netlify.toml`, `backend/main.py` (CORS), `backend/security.py`, `frontend/app.js` | Pendiente |
| **`I-01`** | `ind` | `feat/ind-i01-psi-taxonomy` | `docs/industrial/matriz_trazabilidad_psi.md`, `data/psi_combustion_24.json` (solo lectura/validación) | **Listo [x]** |
| **`I-02`** | `ind` | `feat/ind-i02-topsis-spec` | `docs/industrial/especificacion_topsis.md`, `tests/unit/test_ranking_and_writing_unit.py` | **Listo [x]** |
| **`I-04`** | `ind` | `feat/ind-i04-fmea-matrix` | `docs/industrial/fmea_nasa_std_6001.md`, `data/cases_and_spinoffs.json` (sección FMEA), `tests/unit/test_fmea_unit.py` | **Listo [x]** |
| **`I-05`** | `ind` | `feat/ind-i05-forensic-presets` | `docs/industrial/fichas_forenses.md`, `data/cases_and_spinoffs.json` (sección `forensic_presets`), `tests/unit/test_forensic_presets_unit.py` | **Listo [x]** |
| **`I-06`** | `ind` | `feat/ind-i06-suppression-tree` | `docs/industrial/protocolo_supresion_eclss.md`, `backend/governance.py`, `tests/unit/test_suppression_protocol_unit.py` | **Listo [x]** |
| **`I-07`** | `ind` | `feat/ind-i07-dual-use-spinoffs` | `docs/industrial/impacto_dual_use.md`, `data/cases_and_spinoffs.json` (sección `spinoffs`), `tests/unit/test_dual_use_spinoffs_unit.py` | **Listo [x]** |
| **`I-08`** | `ind` | `feat/ind-i08-writing-craft-templates` | `docs/industrial/plantillas_writing_craft.md`, `backend/ranking_nlp.py` (plantillas), `tests/unit/test_ranking_and_writing_unit.py` | **Listo [x]** |
| **`I-09`** | `ind` | `feat/ind-i09-qa-units-scope` | `docs/industrial/qa_unidades_alcance.md`, `tests/unit/test_qa_units_scope_unit.py` | **Listo [x]** |
| **`I-10`** | `ind` | `feat/ind-i10-readme-ejecutivo` | `README.md`, `tests/unit/test_readme_and_resources_unit.py` | **Listo [x]** |
| **`I-11`** | `ind` | `feat/ind-i11-pitch-deck` | `docs/pitch/deck_7_slides.md`, `tests/unit/test_pitch_deck_unit.py` | **Listo [x]** |
| **`I-12`** | `ind` | `feat/ind-i12-video-script` | `docs/pitch/guion_video_demo.md` | Pendiente |
| **`J-04`** | `joint` | `release/v1.0.0` | `planning/index.html`, `tasks/todo.md`, tag `v1.0.0` (después de merge `dev -> main`) | Pendiente |
| **`J-05`** | `joint` | `docs/joint-j05-video-checklist` | `docs/pitch/checklist_grabacion.md` | Pendiente |
| **`J-06`** | `joint` | `docs/joint-j06-submission` | `docs/pitch/submission_space_apps.md` | Pendiente |
