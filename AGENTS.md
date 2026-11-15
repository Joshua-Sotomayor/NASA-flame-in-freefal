# AGENTS.md — Instrucciones Operativas del Repositorio AERO-IGNIS SI

> Cualquier agente de desarrollo que trabaje en este repositorio debe leer este archivo junto con `SPEC.md` y `tasks/todo.md` antes de escribir o modificar código.

---

## 1. Contexto del Proyecto y Alcance Estricto

- **Reto:** NASA Space Apps Challenge 2026 — *Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*.
- **Equipo:** Ingeniero Mecatrónico y de Control + Ingeniero de Gestión Industrial.
- **Restricción de Dominio (`C-01`):** Tratar **únicamente entornos habitables de tripulación** (ISS, Cygnus, hábitats lunares $\ge 30\%\text{ O}_2$ y $\le 10.2\text{ psi}$, rovers presurizados) y Spinoffs terrestres (`9582`, `9407`, `9918`, `PFE`). **Prohibido** incluir motores cohete o propulsores.
- **Restricción de Costo (`C-02`):** Directiva `$0 USD`. Usar exclusivamente librerías MIT/Apache/CC0 y cero APIs LLM externas de pago.

---

## 2. Arquitectura y Reglas de Ingeniería

1. **Spec-Driven Development (SDD):**
   - No inventes endpoints ni esquemas fuera de [SPEC.md](SPEC.md).
   - Ejecuta las tareas de [tasks/todo.md](tasks/todo.md) en *vertical slices* atómicos (un módulo completo con sus pruebas por iteración).
2. **Programación Orientada a Objetos (POO):**
   - Usa principios **SOLID**, objetos de valor inmutables (`@dataclass(frozen=True)`) e inyección de dependencias por constructor.
   - Evita variables globales mutables o lógica de negocio suelta en rutas FastAPI.
3. **Pipeline 100% ML/DL Propio (Cero LLMs Externos):**
   - **Modelo 1:** `RandomForestClassifier` + `GradientBoostingRegressor` (`BASS-II` / `Saffire I–VI`).
   - **Modelo 2:** CNN ligera PyTorch $\rightarrow$ `flame_cnn.onnx` + `DecisionTreeClassifier` + `DeterministicFsmController`.
   - **Modelo 3:** `TF-IDF + PCA + K-Means + TextRank + TOPSIS/AHP`.
   - Entrenamiento pesado en [notebooks/AERO_IGNIS_Colab_Training.ipynb](notebooks/AERO_IGNIS_Colab_Training.ipynb) (Colab T4) y réplica rápida en CPU local (`backend/train_models.py`).
4. **Seguridad OWASP / STRIDE Obligatoria:**
   - **Cero secretos/API keys** en código o Git.
   - **Anti-DDoS:** `RateLimiter` por IP (`60 req/min` general, `20 req/min` ML), tope `MAX_PAYLOAD_BYTES = 16384` (HTTP `413`), `pageSize <= 50`.
   - **Anti-Inyección:** DTOs Pydantic con `extra="forbid"`, validación por `Enum`/rangos, prohibido `eval()`, `exec()`, `shell=True`, SQL concatenado o `innerHTML` con datos sin escapar.
   - **Deserialización Segura:** Validar `SHA-256` contra `artifacts/models/manifest.sha256.json` antes de cargar cualquier `.joblib` o `.onnx` (prohibidos `.pkl`/`.pickle`).
   - **Anti-SSRF:** Conector OSDR limitado a `https://osdr.nasa.gov` y `https://visualization.osdr.nasa.gov` con `allow_redirects=False` y timeout `3.0s`.
5. **Calidad TDD Piramidal (`pytest`):**
   - Sigue el ciclo **RED $\rightarrow$ GREEN $\rightarrow$ REFACTOR** y el patrón **Prove-It** (test de reproducción antes de corregir bugs).
   - **~80% Unitarias (`tests/unit/`):** rápidas, sin red ni E/S externas.
   - **~15% Integración (`tests/integration/`):** `FastAPI TestClient`, carga real `.joblib`/`.onnx`, verificación `413/422/429/IntegrityError`.
   - **~5% E2E:** flujo en navegador headless (`LCP < 2.5s`, `0` errores de consola, modo offline).
6. **Disciplina Editorial `writing-craft`:**
   - Modo **`academic`** para perfiles de Investigador y documentación científica (verbos calibrados a la evidencia, conservación de DOIs `10.60555` y unidades).
   - Modo **`plain`** para Estudiantes, UI y resúmenes ejecutivos (oraciones $< 25$ palabras, voz activa).
   - Cero *AI slop* (*"en el panorama actual"*, *"sin fisuras"*, *"piedra angular"*, *"cambio de paradigma"*, *"revolucionario"*).

---

## 3. Convención Git Obligatoria

- **Ramas:** `topic branch` (`feat/...`, `docs/...`, `fix/...`) $\rightarrow$ `dev` $\rightarrow$ `main`.
- **Formato de Commit:** `<version> - <verbo> - <descripción>` en minúsculas (`feat|design|refactor|add|fix|test|docs|ship`).
- **Base de Conocimiento:** Toda la investigación de las 24 PSI y los 10 recursos está disponible de forma portable en `docs/knowledge/`.

---

## 4. Protocolo Multi-Perfil, Bloqueo de Archivos y Ramas Independientes

> El equipo comparte cuenta y repositorio entre dos roles. Para evitar colisiones o sobrescrituras entre sesiones paralelas:

1. **Detección Obligatoria de Perfil al Abrir un Nuevo Chat:**
   - Si el primer mensaje del usuario no especifica el rol activo, el agente **debe preguntar explícitamente antes de editar código o planes** desde qué perfil opera esa sesión:
     - **Perfil A — Ingeniero Mecatrónico y de Control (`meca`)**
     - **Perfil B — Ingeniero de Gestión Industrial (`ind`)**
     - **Coordinación Conjunta (`joint`)**
2. **Aislamiento de Tareas por Rama y Bloqueo Lógico de Archivos (*File Locks*):**
   - Cada sesión ejecuta **únicamente tareas de su perfil activo** y crea su propia rama temática (`feat/meca-<id>-<slug>`, `feat/ind-<id>-<slug>`, `docs/...`) desde `dev` actualizado (`git fetch origin && git pull --rebase origin dev`).
   - Antes de iniciar una tarea, consultar los **módulos y archivos asignados (`modules` / lock)** en [tasks/todo.md](tasks/todo.md) y [planning/index.html](planning/index.html), además de revisar `git branch -a` para comprobar qué ramas están activas.
   - **Regla de no colisión:** Mientras una tarea de un perfil esté en curso, sus archivos asignados quedan lógicamente bloqueados para el otro perfil (ej. `frontend/*` bajo `M-13` no debe editarse desde una rama `feat/ind-*`, y `docs/industrial/*` / `README.md` bajo `I-10` no debe editarse desde `feat/meca-*`).
   - **Archivos de tablero compartidos (`planning/index.html`, `tasks/todo.md`):** Se modifican exclusivamente al cerrar la tarea en curso, haciendo `git fetch origin && git pull --rebase origin dev` justo antes del merge a `dev`.

