# Backlog Auditable de Implementación — AERO-IGNIS SI (`tasks/todo.md`)

> **Regla de Ejecución (SDD + Ponytail + Seguridad):** Cada tarea implementa un *vertical slice* atómico en POO, incluye pruebas de seguridad/abuso y se cierra con un commit `<version> - <verbo> - <descripción>` en su rama temática hacia `dev`.

---

## Estado Actual del Ciclo
- [x] **Pre-Fase (Gate 1 Docs):** `PLAN_MAESTRO_FLAME_IN_FREEFALL.md`, War Room `planning/index.html`, `.gitignore`, `.env.example` y `SPEC.md` creados.
- [ ] **Aprobación Humana de `SPEC.md`:** Confirmar antes de iniciar `Task 1`.

---

## Fase 1: Cimientos de Datos y Seguridad (Viernes `H0–H4`)

### Task 1 (`M-02` + `I-01`): Repositorio de Dominio POO y Dataset Maestro de las 24 PSI
- **Responsable:** Mecatrónico (POO `PsiRepository`) + Gestión Industrial (taxonomía y 10 recursos).
- **Alcance:** Crear `data/psi_combustion_24.json`, `data/bass_saffire_runs.csv` (muestras reales de `BASS-II` 17 cols y `Saffire-I` 13 cols), `data/cases_and_spinoffs.json` y `backend/domain.py` (`PsiInvestigation`, `PsiRepository`, `OsdrApiClient` allowlisted).
- **Criterios de Aceptación:**
  - [ ] Exactamente 24 investigaciones PSI con IDs, instalaciones (`CIR`, `MSG`, `Cygnus`, `Otros`), DOIs `10.60555` y metadatos ISA-Tab completos.
  - [ ] `PsiRepository` expone copias inmutables y paginación acotada (`pageSize <= 50`).
  - [ ] `OsdrApiClient` bloquea cualquier host fuera de `osdr.nasa.gov` / `visualization.osdr.nasa.gov` (anti-SSRF).
- **Verificación:** `pytest tests/test_domain_repo.py -v`
- **Commit Git:** `0.3.0 - add - estructurar dataset psi de 24 investigaciones y casos forenses con pruebas`

### Task 2 (`S-Sec` / Transversal): Módulo `SecurityBoundaryGuard` (Anti-DDoS, Anti-Inyección, SHA-256)
- **Responsable:** Mecatrónico.
- **Alcance:** Implementar `backend/security.py` con `RateLimiter` por ventana deslizante, `PayloadSizeMiddleware` (16 KB max), sanitizador/validador estricto, `SecurityHeadersMiddleware` (CSP, DENY, nosniff) y `ModelIntegrityVerifier` (SHA-256).
- **Criterios de Aceptación:**
  - [ ] Petición >16 KB retorna `413 Payload Too Large`.
  - [ ] Exceso de peticiones por IP retorna `429 Too Many Requests`.
  - [ ] Cadenas con payloads XSS/SQLi o parámetros fuera de rango retornan `422` sin stack trace.
  - [ ] Archivo `.joblib`/`.onnx` con hash alterado falla de inmediato con `IntegrityError`.
- **Verificación:** `pytest tests/test_security_hardening.py -v`
- **Commit Git:** `0.4.0 - feat - implementar capa security guard anti ddos anti inyeccion y sha256`

## Checkpoint 1 (Cimientos)
- [ ] Todos los tests de `domain` y `security` pasan al 100%.
- [ ] Revisión rápida con `git diff --staged -i -G'password|secret|api_key|token'`.

---

## Fase 2: Pipeline 100% ML/DL Propio & Motor Físico/FSM (Sábado AM `H5–H14`)

### Task 3 (`M-07`): Entrenamiento Reproducible de los 3 Modelos Propios + Manifiesto SHA-256
- **Responsable:** Mecatrónico (entrenamiento/ONNX) + Gestión Industrial (pesos y análisis de sensibilidad).
- **Alcance:** Crear `backend/train_models.py` que entrena y exporta con `manifest.sha256.json`:
  1. `flammability_rf.joblib` (`RandomForestClassifier` sobre `BASS-II`/`Saffire`) + `burntime_gbr.joblib` (`GradientBoostingRegressor`).
  2. `flame_cnn.onnx` (CNN ligera en PyTorch exportada a ONNX: 4 clases de llama) + `sensor_tree.joblib` (`DecisionTreeClassifier`).
  3. `psi_tfidf_kmeans.joblib` (`TfidfVectorizer` + `PCA` + `KMeans` sobre las 24 PSI).
- **Criterios de Aceptación:**
  - [ ] Todos los modelos exportados pesan `< 15 MB` en conjunto y generan su digest en `artifacts/models/manifest.sha256.json`.
  - [ ] Matrices de confusión y `feature_importances_` quedan registradas y auditables.
- **Verificación:** `python -m backend.train_models && pytest tests/test_models_integrity.py -v`
- **Commit Git:** `0.5.0 - feat - entrenar pipeline ml propio random forest cnn onnx y clustering tfidf`

### Task 4 (`M-03` + `I-05`): `DimensionlessPhysicsCalculator` + `FlammabilityPredictor` + Presets Forenses
- **Responsable:** Mecatrónico + Gestión Industrial.
- **Alcance:** Implementar `backend/physics_ml.py` en POO uniendo ecuaciones ($\text{Da}$, $\text{Pe}$, $V_f$) con `RandomForest`/`GBR` y los 3 presets históricos (**Apollo 1**, **Apollo 13**, **Mir**).
- **Criterios de Aceptación:**
  - [ ] Escenario Apollo 1 ($100\%\text{ O}_2$, $16.7\text{ psi}$) y Hábitat Lunar ($34\%\text{ O}_2$, $8.2\text{ psi}$) reportan riesgo crítico/elevado coherente con `BASS-II`.
  - [ ] Retorna lista ordenada de `feature_importance` explicando la predicción.
- **Verificación:** `pytest tests/test_physics_and_ml.py -v`
- **Commit Git:** `0.6.0 - feat - implementar motor fisico adimensional y predictor random forest en poo`

### Task 5 (`M-04` + `M-05`): `DuctSafetyOrchestrator` (CNN ONNX + Decision Tree + FSM Determinista)
- **Responsable:** Mecatrónico y Control.
- **Alcance:** Implementar `backend/duct_twin.py` con `OnnxFlameVisionModel`, `SensorDecisionTreeModel` y `DeterministicFsmController` (`NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA` con histéresis e interlock de pérdida serial).
- **Criterios de Aceptación:**
  - [ ] Cada transición expone la rama exacta del árbol físico y probabilidades de la CNN ONNX.
  - [ ] Pérdida de comunicación (`comm_ok=False`) fuerza transición inmediata a `FALLA_SEGURA` (ventilador OFF + compuerta cerrada).
- **Verificación:** `pytest tests/test_duct_fsm.py -v`
- **Commit Git:** `0.6.1 - feat - implementar orquestador fsm determinista con cnn onnx y arbol de sensores`

### Task 6 (`I-02` + `I-04` + `I-06` + `I-07` + `I-08`): `TopsisMultiCriteriaRanker`, `ExtractiveNlpEngine` y `GovernanceAndSpinoffService`
- **Responsable:** Gestión Industrial + Mecatrónico.
- **Alcance:** Implementar `backend/ranking_nlp.py` (`TOPSIS/AHP + TF-IDF/TextRank/K-Means + plantillas deterministas por audiencia`) y `backend/governance.py` (`FMEA NASA-STD-6001`, protocolo `PFE/CO2/E-FIELD` y calculadora `Dual-Use` para Spinoffs `9582, 9407, 9918`).
- **Criterios de Aceptación:**
  - [ ] Ranking TOPSIS es determinista y cita únicamente IDs/DOIs presentes en `PsiRepository`.
  - [ ] Síntesis cambia su redacción para `Investigador`, `Estudiante` y `Gestor Industrial` usando las métricas reales de `Feature Importance` y `TOPSIS`.
- **Verificación:** `pytest tests/test_ranking_nlp.py tests/test_governance.py -v`
- **Commit Git:** `0.6.2 - feat - implementar ranking topsis textrank por perfil y gobernanza fmea spinoffs`

## Checkpoint 2 (Core ML/DL & Física)
- [ ] Gate 2 (`J-02`): Todos los escenarios físicos, FSM, ML y FMEA pasan al 100% sin red externa.

---

## Fase 3: API Blindada & Dashboard Web Interactivo (Sábado PM `H15–H26`)

### Task 7 (`S-API`): Ensamblaje FastAPI POO y Pruebas de Contrato/Abuso
- **Responsable:** Mecatrónico.
- **Alcance:** Crear `backend/main.py` conectando todas las clases POO, `SecurityBoundaryGuard` y rutas `/api/v1/*` definidas en `SPEC.md`.
- **Criterios de Aceptación:**
  - [ ] Todas las rutas validan contratos Pydantic (`extra="forbid"`), respetan CORS explícito y aplican cabeceras de seguridad.
- **Verificación:** `pytest tests/test_api_contracts.py -v`
- **Commit Git:** `0.7.0 - feat - ensamblar api fastapi poo con contratos estrictos y proteccion owasp`

### Task 8 (`M-06` + `M-09` + `U-01`): Dashboard Web WAI-ARIA + Gemelo Digital Isométrico SVG (`anatomy`)
- **Responsable:** Mecatrónico + Gestión Industrial (QA de texto/unidades).
- **Alcance:** Crear `frontend/` (`index.html`, `styles.css`, `app.js`) con los 4 módulos integrados (`Explorador/Ranking PSI`, `Sandbox Inflamabilidad + Forense`, `Gemelo Digital Ducto FSM`, `FMEA + Spinoffs`), animaciones GPU `60fps` (`animation-design`), contraste WCAG AA y cero uso inseguro de `innerHTML`.
- **Criterios de Aceptación:**
  - [ ] Funciona en `1440px` y `1024px`, teclado completo, `prefers-reduced-motion`, y sin dependencias pagadas (`Costo $0`).
  - [ ] Ninguna cadena de usuario se inyecta sin sanitización/DOM textContent.
- **Verificación:** Inspección en navegador headless (`0` errores de consola, `LCP < 2.5s`)
- **Commit Git:** `0.8.0 - design - construir dashboard web aero-ignis con gemelo digital svg y graficas`

## Checkpoint 3 (MVP MUST-HAVE)
- [ ] Gate 3 (`J-03`): Flujo completo de los 4 módulos probado en navegador en `<3 minutos`.

---

## Fase 4: Blueprint Físico, Auditoría, Despliegue y Pitch (Domingo `H27–H48`)

### Task 9 (`M-10` + `I-09` + `I-10`): Pestaña *Hardware Blueprint*, QA de Alcance y `README.md`
- **Criterios:** Evidencias de `SolidWorks/EPLAN/Proteus` integradas, cero contenido de motores cohete (`C-01`), los 10 recursos NASA citados en `README.md`.
- **Commit Git:** `0.9.0 - docs - integrar hardware blueprint y readme ejecutivo con 10 recursos nasa`

### Task 10 (`M-11`): Auditoría `/ponytail-audit` + Pruebas de Penetración & Offline
- **Criterios:** Auditoría de seguridad y simplificación aprobada; prueba completa desconectando Wi-Fi.
- **Commit Git:** `0.9.1 - test - validar suite completa de seguridad offline y auditoria ponytail`

### Task 11 (`M-12` + `J-04`): Despliegue Público HTTPS y Tag `v1.0.0` en `main`
- **Criterios:** Merge `dev -> main`, tag `v1.0.0`, URL HTTPS verificada en modo incógnito.
- **Commit Git:** `1.0.0 - ship - liberar plataforma aero-ignis si v1.0.0 en produccion`

### Task 12 (`I-11` + `I-12` + `J-05` + `J-06`): Deck 7 Slides, Video Demo 1080p y Envío Oficial
- **Criterios:** Video exportado (`30s`/`2min`), envío completado 2h antes del cierre en Space Apps.
