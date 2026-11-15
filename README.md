# AERO-IGNIS SI — Plataforma de Seguridad contra Incendios en Microgravedad

> **Reto:** NASA Space Apps Challenge 2026 — *Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*  
> **Equipo:** Ingeniero Mecatrónico y de Sistemas de Control + Ingeniero de Gestión Industrial  
> **Estado Actual:** **Gate 1 (Documentación SDD, Base de Conocimiento y Arquitectura Listas)** — Pendiente aprobación para iniciar `Task 1`.

---

## 1. Qué es este proyecto (en 60 segundos)

**AERO-IGNIS SI** es una plataforma web interactiva (costo `$0`, sin llaves de API externas) que convierte las **24 investigaciones reales de combustión de NASA PSI** y los **10 recursos oficiales del reto** en 4 módulos integrados:

1. **Módulo 1 — Explorador, Clustering y Ranking PSI:** Ingiere las 24 investigaciones (`CC0-1.0`, DOIs `10.60555`), las agrupa (`PCA + K-Means + TF-IDF`), las ordena con ranking multicriterio **TOPSIS/AHP** y genera resúmenes extractivos (`TextRank`) adaptados a 3 audiencias (**Investigador**, **Estudiante**, **Gestor Industrial**).
2. **Módulo 2 — Sandbox Predictivo de Inflamabilidad & Forense:** Calcula números adimensionales ($\text{Da}$, $\text{Pe}$, $V_f$) junto con modelos `RandomForest` / `GradientBoosting` entrenados con datos de `BASS-II (PSI-25)` y `Saffire I–VI`, e incluye presets en 1 clic de **Apollo 1**, **Apollo 13** y **Mir**.
3. **Módulo 3 — Gemelo Digital de Ducto con FSM Determinista:** Clasificación óptica (`CNN PyTorch -> ONNX`) + `DecisionTreeClassifier` de sensores ($\Delta T/\Delta t$, $\text{CO}$, aerosol $<0.1\,\mu\text{m}$, flujo) gobernando una Máquina de Estados Finitos (`NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA`) en SVG isométrico + galería física (`SolidWorks/EPLAN/Proteus`).
4. **Módulo 4 — Gobernanza FMEA & Calculadora Dual-Use:** Matriz de riesgo `NASA-STD-6001`, selector de supresión (`PFE Niebla Fina`, $\text{CO}_2$, `E-FIELD`) y cuantificación de impacto terrestre (**Spinoffs `9582`, `9407`, `9918`**).

---

## 2. Guía Rápida para el Equipo y Agentes

### Dónde empezar según tu perfil

| Perfil | Qué abrir primero | Qué lideras |
| :--- | :--- | :--- |
| **Ingeniero de Gestión Industrial** | 1. [planning/index.html](planning/index.html) (ábrelo en tu navegador)<br>2. [docs/knowledge/01_Objetivos_Dominios_y_Roles.md](docs/knowledge/01_Objetivos_Dominios_y_Roles.md)<br>3. [docs/knowledge/07_Casos_Forenses_Apollo_Mir_y_Spinoffs_Terrestres.md](docs/knowledge/07_Casos_Forenses_Apollo_Mir_y_Spinoffs_Terrestres.md) | Tareas **`I-01` a `I-12`**: taxonomía de las 24 PSI, pesos `TOPSIS/AHP`, matriz `FMEA`, presets forenses, calculadora `Dual-Use`, reglas `writing-craft`, deck y pitch. |
| **Ingeniero Mecatrónico y Control** | 1. [SPEC.md](SPEC.md) (arquitectura POO + OWASP)<br>2. [tasks/todo.md](tasks/todo.md) (backlog TDD)<br>3. [notebooks/AERO_IGNIS_Colab_Training.ipynb](notebooks/AERO_IGNIS_Colab_Training.ipynb) | Tareas **`M-01` a `M-12`**: `PsiRepository`, `SecurityBoundaryGuard`, entrenamiento `RF/GBR` + `CNN .onnx`, física $\text{Da}/\text{Pe}$, `FSM`, FastAPI y Gemelo SVG. |
| **Agente de IA (Nuevo Contexto)** | Lee [AGENTS.md](AGENTS.md), [SPEC.md](SPEC.md) y [tasks/todo.md](tasks/todo.md) antes de tocar cualquier archivo. | Sigue SDD, POO, OWASP, TDD (`tests/unit/` + `tests/integration/`), `writing-craft` y commits `<version> - <verbo> - <descripción>`. |

---

## 3. Mapa del Repositorio

```text
NASA/
├── README.md                               # Este punto de entrada para equipo y agentes
├── AGENTS.md                               # Reglas obligatorias (POO, OWASP, TDD, writing-craft, Git)
├── SPEC.md                                 # Especificación técnica SDD v1.1.0 (contratos REST + POO)
├── PLAN_MAESTRO_FLAME_IN_FREEFALL.md       # Diagnóstico estratégico, 24 PSI, FURPS+ MoSCoW y cronograma
├── tasks/todo.md                           # Backlog auditable Task 1 -> Task 12 con pruebas TDD
├── planning/index.html                     # Tablero War Room interactivo (abrir en navegador)
├── notebooks/AERO_IGNIS_Colab_Training.ipynb # Entrenamiento ML/DL en Google Colab T4 + SHA-256
├── docs/
│   ├── graphs/                             # Diagramas Graphviz (.dot, .svg, .png)
│   └── knowledge/                          # Copia portable de la Base Obsidian (24 PSI + 10 nodos + Canvas)
├── LICENSE                                 # Licencia MIT
├── .gitignore & .env.example               # Protección de secretos y configuración segura
```

### Visualización Rápida de Arquitectura (Graphviz)
- [Mapa 24 PSI $\rightarrow$ Modelos ML/DL $\rightarrow$ Objetivos $\rightarrow$ Roles](docs/graphs/psi_knowledge_graph.svg)
- [Pipeline Dual Google Colab GPU / CPU Local + SHA-256](docs/graphs/ml_dl_colab_pipeline.svg)
- [Pirámide TDD + SDD + writing-craft + Git](docs/graphs/tdd_sdd_architecture.svg)

> **Tip para Obsidian:** Puedes abrir la carpeta `docs/knowledge/` directamente como Vault en Obsidian para explorar los 24 archivos `PSI/`, los `Nodos/` y el mapa interactivo `AERO_IGNIS_Conocimiento_y_ML.canvas`.

---

## 4. Flujo de Trabajo en Git (Obligatorio)

1. Trabaja siempre en una rama temática creada desde `dev` (ej. `feat/topsis-fmea`, `docs/pitch-deck`).
2. Formato estricto de commit:
   ```text
   <version> - <verbo> - <descripción>
   ```
   Verbos permitidos: `feat`, `design`, `refactor`, `add`, `fix`, `test`, `docs`, `ship`.
3. Antes de cada commit verifica que no existan credenciales (`git diff --staged -i -G'password|secret|api_key|token' --name-only`).
4. Licencia del código: **MIT** ([LICENSE](LICENSE)). Datos de NASA PSI: **CC0-1.0**.
