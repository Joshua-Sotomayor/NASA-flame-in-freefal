# AERO-IGNIS SI — Plataforma de Seguridad contra Incendios en Microgravedad (`NASA + ENREDADOS`)

> **Reto:** NASA Space Apps Challenge 2026 — *Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*  
> **Equipo:** Ingeniero Mecatrónico y de Control (`meca`) + Ingeniero de Gestión Industrial (`ind`)  
> **Alcance (`C-01`):** Exclusivamente módulos habitables presurizados (`ISS`, `Cygnus`, hábitats lunares $\ge 30\%\text{ O}_2$ y $\le 10.2\text{ psi}$) y transferencia terrestre Spinoff. Excluye propulsores y vehículos lanzadores.  
> **Licencia y Costo (`C-02`):** Software **MIT** ([LICENSE](LICENSE)) · Datos científicos NASA PSI **CC0-1.0** · Operación **`$0 USD`** sin APIs externas ni LLMs de pago.

---

## 1. Resumen Ejecutivo

**AERO-IGNIS SI** transforma **24 investigaciones reales de combustión en microgravedad de NASA PSI** (DOIs `10.60555/...`), **566 corridas experimentales/calibradas de `BASS-II` y `Saffire I–VI`** y los **10 recursos oficiales del reto** en una plataforma web auditable compuesta por 5 vistas integradas:

1. **`01 · Museo y Glosario`:** Exhibición curada con 6 fotografías reales de ensayos NASA (`ISS`, `BASS-II`, `Saffire`, `CIR`, `Apollo 1`, `Mir`) y glosario interactivo de conceptos físicos.
2. **`02 · Explorador PSI, Clustering PCA y Ranking TOPSIS`:** Indexación de las 24 investigaciones (`CC0-1.0`), proyección `TF-IDF + PCA + K-Means`, ranking multicriterio **TOPSIS/AHP** y síntesis determinista (`TextRank` + plantillas `writing-craft`) para **Investigador**, **Estudiante** y **Gestor Industrial**.
3. **`03 · Simulador Predictivo de Inflamabilidad & Presets Forenses`:** Cálculo físico adimensional ($\text{Da}$, $\text{Pe}$, $V_f$) combinado con `RandomForestClassifier` y `GradientBoostingRegressor` (`BASS-II`/`Saffire`), con carga en 1 clic de **Apollo 1**, **Apollo 13**, **Mir** y **Hábitat Lunar Artemis**.
4. **`04 · Gemelo Digital de Ducto & FSM Determinista`:** Clasificación óptica (`flame_cnn.onnx` exportada desde PyTorch) + `DecisionTreeClassifier` de sensores ($\Delta T/\Delta t$, $\text{CO}$, aerosol $<0.1\,\mu\text{m}$, flujo) gobernando la máquina de estados (`NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA`) + respaldo hardware abierto (`SolidWorks` + esquemático, layout PCB y modelo 3D `.STEP`).
5. **`05 · Gobernanza FMEA, Supresión ECLSS y Calculadora Dual-Use`:** Evaluación de riesgo `NASA-STD-6001` (`FM-01..FM-06`), árbol determinista de supresión (`PFE` vs $\text{CO}_2$ vs `E-FIELD`) y calculadora cuantitativa para los Spinoffs **`9582`**, **`9407`**, **`9918`** y **`PFE`**.

---

## 2. Impacto *Dual-Use* en la Tierra (Spinoffs Verificados)

| ID Spinoff | Año | Tecnología Aeroespacial Transferida | Ahorro de Masa / Capacidad | Reducción de Riesgo | Experimento PSI Vinculado |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **`9582`** | `1976` | **Fireman's Air Tanks (`COPV / PLSS`):** Tanques compuestos de `2,216` a `4,500 psi` (`SCBA` de `33 lb` a `20 lb`) | **`13.0 lb/unidad`** (`-40%`) | **`-40.0%`** | `PSI-104` `SAFFIRE-V` (`10.60555/psi-104`) |
| **`9407`** | `1978` | **Incipient Fire Detector (`SAME` / Shuttle):** Discriminación temprana de aerosoles `<0.1 um` por pirólisis | `0.0 lb` *(detección temprana)* | **`-58.0%`** | `PSI-129` `SPICE` (`10.60555/psi-129`) |
| **`9918`** | `1977` | **Project `FIRES` (`PBI + Nomex`):** Trajes estructurales ignífugos tras `Apollo 1` sin gases tóxicos | **`11.5 lb/unidad`** (`>30%`) | **`-35.0%`** | `PSI-101` `SAFFIRE-II` (`10.60555/psi-101`) |
| **`PFE`** | `2010` | **ISS Portable Fire Extinguisher (`Fine Water Mist`):** Niebla Sauter `20-100 um`, expansión `1,700x`, sin `Halon` ni $\text{CO}_2$ | **`4.2 lb/unidad`** | **`-65.0%`** | `PSI-107` `CVB` (`10.60555/psi-107`) |

---

## 3. Arranque Rápido y Reproducibilidad (`$0 USD`)

```bash
# 1. Instalar dependencias de desarrollo y ejecucion (Python 3.12+)
pip install -r requirements/dev.txt

# 2. (Opcional) Reentrenar modelos locales y regenerar manifiesto SHA-256
py -m backend.train_models

# 3. Ejecutar la plataforma web completa (API FastAPI + Dashboard en http://127.0.0.1:8000/)
cd backend && py main.py

# 4. Ejecutar piramide completa de pruebas unitarias e integracion TDD
py -m pytest -v
```

> Para entornos de solo producción sin suite de pruebas, instalar `pip install -r requirements/base.txt`.  
> **Controles OWASP integrados:** validación `SHA-256` contra `artifacts/models/manifest.sha256.json` antes de cargar `.joblib`/`.onnx`, DTOs Pydantic con `extra="forbid"`, tope de payload de `16 KB` (`HTTP 413`), *rate limiting* por IP (`HTTP 429`) y conector `OSDR` anti-SSRF con respaldo offline.

---

## 4. Citas a los 10 Recursos Oficiales NASA

| # | Categoría | Recurso Oficial NASA | Enlace Directo |
| :-: | :--- | :--- | :--- |
| 1 | `Dataset Principal` | NASA PSI Combustion Repository | https://psi.nasa.gov/physci/repo/search?q=combustion |
| 2 | `Ciencia Base` | NASA Glenn Combustion Science | https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/ |
| 3 | `Video Intro` | NASA ScienceCasts: ISS Combustion | https://www.youtube.com/watch?v=W1oXykoz9zg |
| 4 | `Guía 50+ Págs` | A Researcher's Guide to ISS Combustion Science | https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/ |
| 5 | `Forense 1967` | Apollo 1 Historical Case Study | https://sma.nasa.gov/sma-disciplines/accllp/apollo-1 |
| 6 | `Forense 1970` | Apollo 13 Historical Case Study | https://sma.nasa.gov/sma-disciplines/accllp/apollo-13 |
| 7 | `Forense 1997` | Fire Aboard Space Station Mir | https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/ |
| 8 | `Spinoff 9582` | Fireman's Air Tanks (COPV) | https://spinoff.nasa.gov/node/9582 |
| 9 | `Spinoff 9407` | Incipient Fire Detector (Space Shuttle) | https://spinoff.nasa.gov/node/9407 |
| 10 | `Spinoff 9918 + PFE` | Fire Attire PBI & Fine Water Mist | https://spinoff.nasa.gov/node/9918 |

---

## 5. Estructura del Repositorio y Guías Técnicas

```text
NASA/
├── README.md                                  # Guía ejecutiva, impacto y referencias oficiales
├── AGENTS.md                                  # Reglas operativas multi-perfil, OWASP, TDD y Git
├── SPEC.md                                    # Especificación SDD v1.1.0 (contratos REST + POO)
├── LICENSE                                    # Licencia MIT del software
├── requirements/                              # Dependencias separadas (base.txt / dev.txt)
├── backend/                                   # FastAPI, physics_ml.py, duct_twin.py, ranking_nlp.py, governance.py
│   └── main.py                                # Punto de entrada directo (`cd backend && py main.py`)
├── frontend/                                  # Dashboard web editorial NASA + ENREDADOS + Museo
├── data/                                      # psi_combustion_24.json, bass_saffire_runs.csv, cases_and_spinoffs.json
├── artifacts/models/                          # Pesos .joblib, flame_cnn.onnx y manifest.sha256.json
├── notebooks/AERO_IGNIS_Colab_Training.ipynb  # Pipeline reproducible en GPU T4 / CPU
├── planning/index.html                        # Tablero War Room interactivo de progreso
├── tasks/todo.md                              # Backlog auditable y bloqueos de archivos
├── docs/                                      # Conocimiento Obsidian (docs/knowledge/), grafos SVG e ingeniería industrial
└── tests/                                     # Pirámide TDD (tests/unit/ y tests/integration/)
```

### Documentos de Referencia Rápida
- **Arquitectura y Contratos:** [SPEC.md](SPEC.md) · [AGENTS.md](AGENTS.md) · [tasks/todo.md](tasks/todo.md) · [planning/index.html](planning/index.html) · [backend/main.py](backend/main.py)
- **Visualizaciones Graphviz:** [Mapa 24 PSI $\rightarrow$ ML/DL](docs/graphs/psi_knowledge_graph.svg) · [Pipeline Colab + SHA-256](docs/graphs/ml_dl_colab_pipeline.svg) · [Arquitectura TDD/SDD](docs/graphs/tdd_sdd_architecture.svg)
- **Licenciamiento:** Código fuente bajo **MIT** ([LICENSE](LICENSE)); investigaciones y tablas científicas NASA PSI bajo **CC0-1.0**.
