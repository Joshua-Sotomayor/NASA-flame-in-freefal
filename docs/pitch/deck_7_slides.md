# Deck Ejecutivo de 7 Diapositivas — `AERO-IGNIS SI` (`I-11`)

> **Equipo:** `NASA + ENREDADOS` (Ingeniería Mecatrónica y de Control + Ingeniería de Gestión Industrial)  
> **Reto:** *Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data* (NASA Space Apps Challenge 2026)  
> **Uso:** Estructura visual y narrativa (`~2 min`) alineada a los 5 criterios oficiales NASA (**Impact**, **Creativity**, **Validity**, **Relevance**, **Presentation** — `20%` cada uno) bajo alcance de cabinas habitables presurizadas y operación `$0 USD`.

---

## Slide 1: Fuego en Caída Libre — ¿Qué Pasa Cuando Desaparece la Gravedad?

- **Criterios NASA:** `Relevance` · `Presentation`
- **Composición Visual:** Fondo claro editorial con cabecera `NASA + ENREDADOS` (`Geist Pixel`) y tríptico horizontal inspirado en `anatomy` mostrando tres fotografías reales de `frontend/assets/museum/` (`apollo_1_crew.jpg`, `mir_station.jpg`, `flame_0g.jpg`). A la derecha, tarjeta de contraste térmico `1g` (llama alargada) frente a `0g` (llama esférica estacionaria y llama fría invisible).
- **Puntos en Pantalla:**
  - En microgravedad no existe convección ascendente; las llamas rodean el combustible en forma esférica y re-ignitan en modo frío (`NTC`, `500–800 K`).
  - Precedentes críticos de cabina: **Apollo 1** (`100% O2`, `16.7 psi`), **Apollo 13** y el fuego químico en **Mir** (`LiClO4`).
  - **`AERO-IGNIS SI`:** transforma **`24`** investigaciones NASA `PSI` y **`566`** corridas `BASS-II`/`Saffire` en soporte de decisiones para cabinas habitables a **`$0`** costo.
- **Notas de Orador:** Imaginen escuchar una alarma de incendio a `80,000` millas de casa en **Artemis**, donde apagar la ventilación no siempre basta y la gravedad ya no eleva el humo hacia el techo. En **Apollo 1**, **Apollo 13** y **Mir**, los incendios en cabinas cerradas exigieron repensar materiales, detección y extinción. Con `AERO-IGNIS SI`, convertimos la evidencia experimental de NASA en decisiones rápidas de ingeniería y entrenamiento para cualquier usuario en `30` segundos.

---

## Slide 2: Inteligencia Científica Trazable Sobre las `24` Investigaciones `PSI`

- **Criterios NASA:** `Validity` · `Relevance`
- **Composición Visual:** Captura de la pestaña `02 · Explorador PSI y Ranking` mostrando a la izquierda el mapa `PCA + K-Means` de `4` grupos sin etiquetas solapadas (`anatomy` con líneas guía limpias y aro de foco en el estudio #1) y a la derecha el selector de audiencia (**Investigador**, **Estudiante**, **Gestor Industrial**) con pesos **TOPSIS/AHP**.
- **Puntos en Pantalla:**
  - Ingestión directa de los `24` estudios `PSI` (`14–85% O2`, `7.3–29.4 psi`, `10.60555/psi-98` a `10.60555/psi-154`) y los `10` recursos oficiales del reto.
  - Ranking multicriterio **TOPSIS** en `<50 ms` combinando seguridad en cabina, modelado físico, sensores e impacto terrestre.
  - Síntesis determinista `TextRank` sin APIs externas ni alucinaciones: lenguaje académico con DOIs `10.60555/` para investigación y oraciones claras (`<25` palabras) para estudiantes.
- **Notas de Orador:** El investigador o estudiante no necesita revisar cientos de tablas dispersas para saber qué ensayo de NASA aplica a su problema. Nuestro explorador agrupa las `24` investigaciones en cuatro familias mediante clustering local y las ordena en tiempo real con **TOPSIS**. Al elegir una audiencia, el sistema adapta el resumen citando exclusivamente experimentos y DOIs reales `10.60555/`, sin inventar datos ni depender de servicios de pago.

---

## Slide 3: Simulador Predictivo de Inflamabilidad y Validación Forense en 1 Clic

- **Criterios NASA:** `Validity` · `Creativity`
- **Composición Visual:** Diagrama partido (`anatomy` de dos columnas): a la izquierda, panel de controles interactivos (`% O2`, `psi`, flujo `cm/s`, gravedad `0g / 0.16g / 0.38g / 1g`, material) con los botones de preset histórico (**Apollo 1**, **Apollo 13**, **Mir**, **Hábitat Lunar Artemis**); a la derecha, curva dinámica de contorno de inflamabilidad (Extinción Radiativa vs Propagación Estable vs Soplado) y barras locales de *Feature Importance*.
- **Puntos en Pantalla:**
  - Modelo híbrido: ecuaciones adimensionales de **Damköhler ($\text{Da}$)** y **Péclet ($\text{Pe}$)** + `RandomForestClassifier` y `GradientBoostingRegressor` entrenados sobre **`566`** corridas calibradas `BASS-II` (`PSI-25`) y `Saffire I–VI`.
  - Carga instantánea de **Apollo 1** (`100% O2`, `16.7 psi`), **Mir** (`21% O2`, `14.7 psi`) y **Hábitat Lunar Artemis** (`34% O2`, `8.2 psi`, `SIBAL`).
  - Explicabilidad local inmediata: revela si domina el oxígeno, la ventilación o la reactividad del material (`PTFE`, `PMMA`, `SIBAL`, `Nomex`, `Kapton`).
- **Notas de Orador:** Más allá de leer cifras estáticas, el usuario prueba escenarios reales *"What-If"* en segundos. Al pulsar el preset **Hábitat Lunar Artemis** (`34% O2` a `8.2 psi`), el motor físico calcula $\text{Da}$, $\text{Pe}$ y tasa de propagación mientras el predictor muestra por qué el enriquecimiento de oxígeno eleva el riesgo frente al aire estándar de la `ISS`. También reproduce al instante por qué los aislamientos `PTFE` fallaron en **Apollo 1** y **Apollo 13**.

---

## Slide 4: Gemelo Digital de Ducto con Visión Óptica y `FSM` Determinista

- **Criterios NASA:** `Creativity` · `Validity`
- **Composición Visual:** Esquema isométrico limpio SVG del ducto (`anatomy` de flujo con flechas direccionales): ventilador variable (`0–60 cm/s`), muestra en cámara, sensor óptico (`flame_cnn.onnx`), sensores de $\text{CO}$, aerosol `<0.1 um` y compuerta/boquilla `PFE`. Debajo, diagrama de transición `NORMAL -> PRE_ALERTA -> CONTENCION -> FALLA_SEGURA` junto a miniaturas hardware (`SolidWorks`, `EPLAN`, `Proteus`).
- **Puntos en Pantalla:**
  - Visión computacional ligera (`CNN PyTorch -> flame_cnn.onnx`) detectando `4` regímenes: Nominal, Llama Esférica `0g`, **Llama Fría NTC** (`500–800 K`) y Propagación Abierta.
  - Fusión multisensor (`DecisionTreeClassifier`) sobre gradiente térmico, $\text{CO}$ (`ppm`), partículas `<0.1 um` (`SPICE PSI-129`, `10.60555/psi-129`) y flujo `cm/s`.
  - **Control determinista seguro ante fallos:** bloqueo de rearme ante llama fría `NTC` y enclavamiento cableado a `FALLA_SEGURA` si falla la comunicación (`comm_ok=False`).
- **Notas de Orador:** En microgravedad una llama fría `NTC` casi invisible puede permanecer activa tras desaparecer la llama caliente. Nuestro Gemelo Digital combina una red neuronal compacta en `ONNX` con un árbol de sensores auditable y una máquina de estados finitos con histéresis: impide reactivar el ventilador prematuramente y lleva la compuerta a cierre seguro por hardware si se pierde la señal serial.

---

## Slide 5: Gobernanza `FMEA` (`NASA-STD-6001`) y Supresión Segura en `ECLSS`

- **Criterios NASA:** `Validity` · `Impact`
- **Composición Visual:** Tablero comparativo de dos bloques: arriba, barras de severidad comparando `NPR Base` (`1901`) frente a `NPR Mitigado` (`134`) en los `6` modos de falla (`FM-01..FM-06`); abajo, árbol visual compacto de supresión eligiendo entre **`PFE`** (niebla fina), **`E-FIELD`** (`PSI-154`, `10.60555/psi-154`) y **$\text{CO}_2$** (bloqueado cuando `habitable_crew=True`).
- **Puntos en Pantalla:**
  - Matriz `FMEA` cuantitativa (`FM-01..FM-06`): reducción del `NPR` acumulado de **`1901` a `134`** (**`-92.95%`** promedio) al integrar detección temprana e interlocks.
  - Árbol determinista de supresión `ECLSS`: prescribe **`PFE`** (`20–100 um`, `2,260 kJ/kg`) ante reacciones auto-oxidantes tipo **Mir** (`Vika / LiClO4`, `FM-05`) y rechaza `Halon 1301` (`HF`/`HBr` corrosivo).
  - Bloquea $\text{CO}_2$ por riesgo de hipercapnia en módulos tripulados y habilita **`E-FIELD`** (`+/-10 kV` sin consumo de agente) para llamas laminares limpias.
- **Notas de Orador:** Apagar un incendio dentro de una estación cerrada no puede envenenar ni asfixiar a la tripulación. Nuestra matriz `FMEA` reduce el riesgo acumulado `NPR` en **`92.95%`** y nuestro árbol de supresión decide bajo reglas estrictas: bloquea $\text{CO}_2$ si hay astronautas, evita halones corrosivos y exige niebla fina `PFE` en cartuchos auto-oxidantes como ocurrió en **Mir**, reservando el campo eléctrico **`E-FIELD`** de `PSI-154` para llamas laminares en aviónica limpia.

---

## Slide 6: Impacto *Dual-Use* — De las Misiones NASA a Ciudades e Industria en la Tierra

- **Criterios NASA:** `Impact` · `Relevance`
- **Composición Visual:** Infografía de cuatro tarjetas con puente horizontal Espacio $\rightarrow$ Tierra (`anatomy` comparativo con métricas destacadas en tipografía monoespaciada): **`9582`**, **`9407`**, **`9918`** y **`PFE`**, vinculando cada tecnología con un icono de aplicación terrestre (bomberos, centros de datos/minas, trajes térmicos y salas eléctricas).
- **Puntos en Pantalla:**
  - **Spinoff `9582` (`COPV / PLSS`, `PSI-104`):** elevó presión de `2,216` a `4,500 psi`, ahorrando **`13.0 lb`** por equipo `SCBA` (**`-40%`** peso, `-40.0%` riesgo).
  - **Spinoff `9407` (`SAME <0.1 um`, `PSI-129`):** detección submicrónica de pirólisis antes de llama visible en minas y hospitales (**`-58.0%`** riesgo).
  - **Spinoff `9918` (`Project FIRES / PBI`, `PSI-101`):** trajes estructurales ignífugos ahorrando **`11.5 lb`** por conjunto (**`-35.0%`** riesgo).
  - **Spinoff `PFE` (`ISS Fine Water Mist`, `PSI-107`):** microgotas `20–100 um` con expansión `1,700x` seguras en turbinas y electrónica (**`4.2 lb`** ahorradas, **`-65.0%`** riesgo).
- **Notas de Orador:** La ciencia espacial de combustión salva vidas todos los días en la Tierra. En nuestra Calculadora *Dual-Use*, al equipar una estación de bomberos con `100` cilindros `SCBA` derivados del nodo **`9582`**, reducimos **`1,300 lb`** de carga física sobre los rescatistas. Sumamos detectores submicrónicos **`9407`**, textiles ignífugos **`9918`** nacidos tras **Apollo 1** y extintores de niebla limpia **`PFE`**, trazando cada beneficio a experimentos `PSI` reales.

---

## Slide 7: Arquitectura Auditable, Seguridad OWASP y Demo Lista en `30` Segundos

- **Criterios NASA:** `Presentation` · `Validity` · `Creativity`
- **Composición Visual:** Diagrama limpio de cuatro capas (`Frontend Editorial NASA + ENREDADOS` $\rightarrow$ `API FastAPI POO` $\rightarrow$ `Modelos .joblib / .onnx con SHA-256` $\rightarrow$ `Datos CC0-1.0 y 10 Recursos NASA`), acompañado del sello `0` costos externos (`$0 USD` · `MIT` + `CC0-1.0`).
- **Puntos en Pantalla:**
  - **Seguridad y confiabilidad:** validación `SHA-256` previa a inferencia, límites anti-DDoS (`16 KB` / rate limiting), DTOs estrictos `extra="forbid"` y conector `OSDR` con respaldo offline completo.
  - **Calidad verificada por ingeniería:** pirámide automatizada de pruebas unitarias e integración cubriendo física, `FSM`, supresión `ECLSS`, `Dual-Use`, `writing-craft` y auditoría `C-01` (exclusión total de motores de propulsión).
  - **Cierre accionable:** plataforma abierta bajo licencia **MIT** y datos **CC0-1.0**, lista para ejecutarse con un comando (`cd backend && py main.py`) o probarse en línea sin registros ni llaves de pago.
- **Notas de Orador:** `AERO-IGNIS SI` no es una maqueta conceptual ni un envoltorio de modelos externos: corre completo a costo **`$0`**, funciona incluso sin conexión gracias a sus modelos ligeros verificados por `SHA-256`, y respalda cada gráfica con ecuaciones verificables, ingeniería de riesgos `NASA-STD-6001` y pruebas automatizadas en verde. Cuando las próximas tripulaciones viajen hacia la Luna y Marte, la seguridad contra incendios empezará con decisiones explicables como esta. Muchas gracias.
