# Especificación Técnica de Tareas Externas (`SolidWorks`, `EPLAN`, `Proteus`) — Subclase `externas`

> **Proyecto:** AERO-IGNIS SI (`NASA Space Apps Challenge 2026 — Flame in Freefall`)  
> **Alcance Estricto (`C-01`):** Entornos habitables presurizados (`ISS-CIR`, `ISS-MSG`, `Cygnus/Saffire`, hábitats lunares Artemis) y transferencia terrestre `Spinoff`. Excluye sistemas de propulsión espacial.  
> **Política de Costo (`C-02`):** Software de diseño disponible en estación de trabajo del equipo, recursos CAD/ECAD gratuitos y evidencias integradas en el repositorio/pestaña `Blueprint` (`F-08 COULD HAVE`), sin enlace serial `COMPIM` en vivo (`F-09 WON'T HAVE`).

---

## 1. Asignación Oficial de Perfiles y Trazabilidad en War Room

| ID | Perfil Asignado | Herramienta Externa | Prioridad MoSCoW | Rol en el Proyecto |
| :--- | :---: | :--- | :---: | :--- |
| **`EXT-01`** | **Perfil B — Gestión Industrial (`ind`)** | **SolidWorks** (CAD 3D + BOM + Plano 2D) | **COULD HAVE (`F-08`)** | Envolvente física del ducto de ventilación, disposición ergonómica/mantenibilidad de sensores, bridas `ISPR` y boquilla atomizadora `PFE`. |
| **`EXT-02`** | **Perfil A — Mecatrónica y Control (`meca`)** | **EPLAN Electric P8** (Esquema `IEC 60617` / `24 VDC`) | **SHOULD HAVE (`F-04`/`F-08`)** | Enclavamiento eléctrico cableado de falla segura (*Fail-Safe*), relé Watchdog `K1-WD` e interlock mecánico/eléctrico independiente del software. |
| **`EXT-03`** | **Perfil A — Mecatrónica y Control (`meca`)** | **Proteus ISIS** (Simulación MCU + Sensores) | **COULD HAVE (`F-08`)** | Validación de acondicionamiento analógico (`dT/dt`, `CO`, `<0.1 µm`, flujo), muestreo a `100 ms` y trama serial `CRC-8` a `115200 bps`. |
| **`J-04`..`J-06`** | **Coordinación Conjunta (`joint`)** | **Render + UptimeRobot + OBS/Video + Space Apps** | **MUST HAVE (`C-03`)** | Activación del despliegue público HTTPS, grabación demo 1080p y envío oficial 2h antes del cierre. |

---

## 2. Detalle Profundo — `EXT-01`: Modelado CAD 3D en SolidWorks (Perfil B `ind`)

### 2.1 Propósito y Alcance
Materializar la contraparte mecánica del Gemelo Digital mostrado en el Módulo 3 (`frontend/index.html` `#ductDigitalTwinSvg`) y en la pestaña `Blueprint` (`Sección 250 × 250 mm · Brida Compuerta`).
- **Dentro del alcance:** Ensamblaje paramétrico funcional del módulo de prueba en ducto a escala de banco/rack (`250 × 250 × 600 mm`) basado en la arquitectura de flujo de `Saffire I–VI (PSI-98..105)` y `BASS-II (PSI-25)`.
- **Fuera del alcance:** Simulación CFD completa de combustión (SolidWorks Flow Simulation con reacción química), piezas con tolerancias de manufactura de vuelo certificadas NASA, o cualquier componente de propulsión espacial (`C-01`).

### 2.2 Cómo Realizarlo Paso a Paso
1. **Crear el proyecto de ensamblaje (`aero_ignis_duct_assy.SLDASM`)** en sistema `MMGS` (milímetros, gramos, segundos).
2. **Pieza 1 — Carcasa Principal del Ducto (`01_duct_housing.SLDPRT`):**
   - Extruir perfil cuadrado hueco de `250 × 250 mm` internos, espesor de pared `3.0 mm` (exterior `256 × 256 mm`) y longitud total `600 mm`.
   - Material asignado en SolidWorks: **Aluminio `6061-T6`** (compatible con estructuras ligeras de cabina).
   - Añadir bridas perimetrales de acoplamiento rápido de `15 mm` en entrada (`Z = 0 mm`) y salida (`Z = 600 mm`) con patrón de 8 barrenos `Ø 6.5 mm` para tornillería `M6`.
   - Practicar ventana lateral opcional de inspección o corte de sección para que el interior sea visible en render.
3. **Pieza 2 — Etapa de Ventilación y Enderezador de Flujo (`02_hvac_fan_honeycomb.SLDPRT`):**
   - En la zona de entrada (`Z = 40..90 mm`), montar un ventilador axial `24 VDC` simplificado (carcasa `220 × 220 × 38 mm`, 5 álabes) seguido de una rejilla enderezadora (*honeycomb* de paso `10 mm`) para garantizar flujo laminar uniforme (`0–60 cm/s`) como en `BASS-II` y `Saffire`.
4. **Pieza 3 — Portamuestras Modular de Combustible (`03_sample_holder.SLDPRT`):**
   - En la zona central (`Z = 250 mm`), modelar mordazas de sujeción aisladas térmicamente (base cerámica/acero inox `316L`) capaces de fijar láminas planas `PMMA` o tejido `SIBAL` de espesor parametrizable (`0.2 a 10.0 mm`).
5. **Pieza 4 — Mirilla Óptica y Puertos de Sensores (`04_sensor_ports.SLDPRT`):**
   - Sobre el techo superior (`Z = 250 mm`), colocar una mirilla sellada con anillo O-ring y vidrio de cuarzo (`Ø 60 mm`) y soporte para el módulo de cámara óptica `CNN`.
   - Aguas abajo (`Z = 370 mm`, es decir `+120 mm` respecto a la muestra), ubicar 3 boquillas roscadas `M12` para: (a) termopar Tipo K ($\Delta T/\Delta t$), (b) sensor electroquímico $\text{CO}$, y (c) cámara óptica/sonda de aerosol submicrónico `< 0.1 µm` (`Spinoff 9407`).
   - En la entrada (`Z = 130 mm`), añadir puerto de sonda de velocidad de aire (`0–60 cm/s`).
6. **Pieza 5 — Compuerta Cortafuego Motorizada con Retorno por Resorte (`05_fire_damper.SLDPRT`):**
   - En `Z = 470 mm` (`+220 mm` respecto a la muestra), modelar una compuerta de guillotina o mariposa en acero inoxidable `304` con perímetro sellado en elastómero fluorado (`Viton` / silicona de alta temperatura).
   - Montar actuador exterior solenoide/motorizado con muelle mecánico de retorno (*spring-return fail-safe*): energizado mantiene abierta la compuerta; sin energía cierra herméticamente el ducto.
   - Incorporar interruptor fin de carrera `SQ-DMP-CLOSED` en el tope inferior para confirmar cierre físico antes de descargar `PFE`.
7. **Pieza 6 — Boquilla Atomizadora de Niebla Fina `PFE` (`06_pfe_nozzle.SLDPRT`):**
   - Ubicada en `Z = 435 mm` (aguas arriba de la compuerta cerrada para confinar la nube dentro de la cámara de prueba), inclinada exactamente a **`30°`** hacia el portamuestras para dispersar microgotas de `20–100 µm`.
8. **Relaciones de Posición (Mates) y Verificación:**
   - Aplicar relaciones concéntricas/coincidentes sin grados de libertad residuales en piezas fijas y un límite angular/lineal (`0–100%` carrera) en la compuerta.
   - Ejecutar `Evaluar -> Detección de interferencias` (`0 interferencias`) y `Propiedades físicas` para registrar masa estimada del ensamble.

### 2.3 Requisitos que Debe Cumplir
- **Geométricos:** Sección interna `250 × 250 mm`, inclinación `30°` en boquilla `PFE`, visibilidad directa de la muestra desde la mirilla superior (`FOV` despejado).
- **Orden de Seguridad Cortafuego:** Todo módulo derivador o rejilla difusora hacia cabina habitable se acopla en la brida de salida (`Z = 600 mm`), **siempre aguas abajo (después) de la compuerta cortafuego (`Z = 500 mm`)**.
- **Normativos / Seguridad (`NASA-STD-6001` y `C-01`):** Materiales no combustibles dentro del canal (`Al 6061-T6`, `Inox 304/316`, `Viton`, cuarzo fundido); cero referencias a propulsores o motores cohete.
- **Ergonomía y Gestión Industrial (`ind`):** Puertos de mantenimiento accesibles sin desmontar la estructura completa (`ISPR` modular) y Lista de Materiales (**BOM**) numerada 1:1 con los tags de `EPLAN`.

### 2.4 Mapa Exacto de Agujeros, Juntas, Montaje del Cuarzo, Caja ESP32 y Uniones (Plano `plano_ducto_solidworks.svg`)

Referencia gráfica vectorial: [`docs/industrial/plano_ducto_solidworks.svg`](plano_ducto_solidworks.svg).

| Elemento / Perforación | Ubicación Exacta `(Z, X, Y)` | Dimensiones / Rosca | Junta / Fijación / Distancia |
| :--- | :--- | :--- | :--- |
| **Bridas de acoplamiento (`Entrada` / `Salida`)** | `Z = 0 mm` y `Z = 600 mm` | `310 × 310 mm` ext., `8 × Ø 6.5 mm` | Soldadura TIG al cuerpo + **8× pernos `M6 × 20`** + junta plana **`Viton® 2.0 mm`**. |
| **Anclajes estructurales a rack (`ISPR`)** | Base inferior `Z = 100` y `Z = 520 mm` | Escuadras en `U` (`40 × 40 × 4 mm`) | Remaches ciegos/pernos `M6` + **tacones antivibración de elastómero ignífugo**. |
| **Ventilador axial `24 VDC` + *Honeycomb*** | Entrada `Z = 12..60 mm` y `Z = 65..90 mm` | Marco `220 × 220 × 38 mm` / Panal `248 × 248 × 25 mm` | 4× pernos `M4` en marco adaptador; *honeycomb* retenido por guías en `L` remachadas. |
| **Sonda de flujo de aire (`0–60 cm/s`)** | Pared derecha `Z = 120 mm`, `Y = 0` | Barreno `Ø 16.5 mm` / Boss `M16` | Racor compresión con junta PTFE; cableado hacia caja `ESP32` (`~120 mm`). |
| **Mirilla de Cuarzo Fundido + Cámara `CNN` Externa** | Techo `Z = 240 mm`, `X = 0` | Calado libre `Ø 60 mm`; disco cuarzo **`Ø 70 × 6 mm`**; `6 × M4` en `PCD Ø 84 mm` | **Sándwich sin contacto metal-vidrio:** Marco soldado + **O-ring inferior `Viton` (`Ø 64 × 3 mm`)** + Cuarzo + **Junta superior `PTFE/Grafito 1.5 mm`** + Aro aluminio + 4 postes separadores (`45 mm`) sosteniendo la **cámara afuera**. |
| **Grupo 3 Sensores (`dT/dt`, `CO`, `< 0.1 µm`)** | Pared derecha `Z = 340 mm`, `Y = +45 / 0 / -45 mm` | `M12 × 1.5` (`Ø 12.5`), Brida `Ø 20.5` (`2 × M3`), `M12 × 1.5` | Racores soldados `TIG` con sellos `Viton`. |
| **Caja Electrónica `ESP32` + Placa Proteus** | Pared derecha exterior `Z = 240..370 mm` | Caja aluminio IP65 `130 × 90 × 55 mm` | **4× tuercas remachables (`Rivnuts M4`) + 4× separadores térmicos de `15 mm`**. Distancia cable analógico a sensores: **`80–130 mm` (`< 15 cm`)** vía prensacables `PG9`; salida troncal única `RS-485 + 24 VDC`. |
| **Boquilla Atomizadora `PFE`** | Techo `Z = 420 mm`, `X = 0` | Boss soldado `1/4" NPT` / `M14` inclinado **`30°` hacia `-Z`** | Arandela cobre/`Viton`; confinada aguas arriba de la compuerta. |
| **Compuerta Cortafuego + Actuador Externo** | Eje pasante `Z = 500 mm`, `Y = 0` (`X = ±125 mm`) | `2 × Ø 12.2 mm` + bujes bronce y retenes `Viton` | Hoja `Inox 304` sobre tope perimetral `10 × 10 mm` con `Viton`; actuador externo *spring-return* montado en pared izquierda con **4× pernos `M5`**. |

#### Criterio de Uniones Mecánicas
- **Soldadura TIG continua:** Cuerpo principal `250 × 250 mm`, bridas extremas, marco base de la mirilla y *bosses* roscados (`M12`, `30° PFE`) para estanqueidad total.
- **Pernos Inoxidables (`M4`/`M5`/`M6`):** Todo componente desmontable o calibrable (*Line Replaceable Unit*): unión entre módulos (`M6`), prensa de cuarzo (`M4`), caja `ESP32` (`M4`), actuador (`M5`) y ventilador (`M4`).
- **Remaches ciegos y *Rivnuts*:** Fijación de guías internas del *honeycomb*, escuadras inferiores de soporte al rack y tuercas remachables `M4` en chapa de `3 mm` para montar separadores sin necesitar acceso por detrás.

### 2.4 Qué Se Debe Esperar (Entregables)
1. Archivos nativos SolidWorks (`.SLDPRT`, `.SLDASM`) + exportación neutra `.STEP` (`AP214`) para apertura universal.
2. **Render / Captura 1 (`1920 × 1080` PNG):** Vista isométrica con corte de sección (*Section View*) mostrando flujo, muestra, sensores, compuerta y boquilla a `30°`.
3. **Render / Captura 2 (`1920 × 1080` PNG):** Vista explosionada con globos numerados y **BOM** (Lista de Materiales).
4. **Plano 2D (`PDF` / `PNG`):** Cotas principales (`250 × 250 mm`, `600 mm`, ángulo `30°`), masa total y cajetín de revisión `AERO-IGNIS SI`.

---

## 3. Detalle Profundo — `EXT-02`: Diagramas Eléctricos en EPLAN Electric P8 (Perfil A `meca`)

### 3.1 Propósito y Alcance
Documentar el respaldo eléctrico cableado (*Hardwired Fail-Safe Interlock*) que garantiza que, incluso si el microcontrolador se cuelga o se corta el enlace serial (`comm_ok = False`), el ducto se aísla físicamente sin depender del software.
- **Dentro del alcance:** Proyecto EPLAN de 3 a 4 páginas bajo estándar `IEC 60617` a `24 VDC` con lógica de disparo por desenergización (*de-energize to trip*), tabla de bornes y alineación exacta con `DeterministicFsmController` (`backend/duct_twin.py`).
- **Fuera del alcance:** Tableros de potencia trifásica de alta tensión (`480 VAC`), certificación formal de vuelo `NASA-STD-8739` o simulaciones transitorias SPICE dentro de EPLAN.

### 3.2 Cómo Realizarlo Hoja por Hoja
1. **Hoja 01 — Portada, Simbología y Leyenda de Tags:** Identificación del proyecto `AERO-IGNIS-ECAD-01`, norma `IEC 60617`, lista de referencias cruzadas (`QF1`, `K1-WD`, `KM-FAN`, `SOL-DMP`, `SOL-PFE`, `SQ-DMP-CLOSED`).
2. **Hoja 02 — Alimentación `24 VDC` y Cadena de Seguridad Cableada (`Interlock`):**
   - Línea superior `+24V_ESS` (bus esencial) y línea inferior `0V_GND`.
   - Interruptor magnetotérmico bipolar `QF1 (4 A)` para potencia de actuadores y fusible `F1 (1 A)` para lógica de control.
   - Pulsador físico de paro de emergencia con retención `S1-EMO` (contacto `NC`).
   - **Relé Watchdog de Seguridad `K1-WD`:** Bobina excitada únicamente mientras el microcontrolador envía tren de pulsos `WD_HEARTBEAT` (`comm_ok = True`) a través de etapa rectificadora/monoestable. Si se pierde la comunicación (`comm_ok = False`), `K1-WD` cae por gravedad/resorte magnético y abre sus contactos `NO` en serie con la habilitación de operación normal.
3. **Hoja 03 — Potencia de Actuadores y Enclavamientos Cruzados:**
   - **Ventilador HVAC (`M1-FAN` / `KM-FAN`):** Alimentado a través de contacto habilitador de `K1-WD` y relé de control FSM (`DO_FAN_EN`). Ante `CONTENCION` o `FALLA_SEGURA`, `KM-FAN` se desenergiza y detiene la convección forzada.
   - **Compuerta Cortafuego (`SOL-DMP`):** Solenoide de retención abierta con retorno mecánico por resorte (*Spring-Return*). Conectado en serie con contacto de `K1-WD` y contacto `NC` de disparo `DO_DAMPER_TRIP`. Al perder `24 VDC` o entrar en `CONTENCION` / `FALLA_SEGURA`, el resorte cierra la compuerta automáticamente. Diodo *flyback* `1N5819` / supresor TVS en paralelo con la bobina.
   - **Electroválvula de Niebla Fina `PFE` (`SOL-PFE`):** Enclavada **en serie eléctrica obligatoria** con el contacto `NO` del fin de carrera `SQ-DMP-CLOSED` (se cierra físicamente cuando la compuerta llega al 100% de cierre) y la señal `DO_PFE_FIRE`. Garantiza que el agente `PFE` no se disperse hacia un ducto abierto ni durante `FALLA_SEGURA` sin alarma confirmada.
4. **Hoja 04 — Tabla de Bornes (`-X1`, `-X2`) y Matriz Lógica Hardware vs. FSM:**

| Estado `DeterministicFsmController` | `K1-WD` (Watchdog) | `KM-FAN` (Ventilador) | `SOL-DMP` (Compuerta) | `SQ-DMP-CLOSED` | `SOL-PFE` (Niebla Fina) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`NORMAL`** | Energizado (`ON`) | `ON` (Flujo nominal) | Energizado (**Abierta**) | Abierto (`0`) | `OFF` |
| **`PRE_ALERTA`** | Energizado (`ON`) | `ON` (Vigilancia activa) | Energizado (**Abierta**) | Abierto (`0`) | `OFF` |
| **`CONTENCION`** | Energizado (`ON`) | **`OFF` (Corte flujo)** | Desenergizado (**Cerrada**) | Cerrado (`1`) | **`ON` (Descarga PFE)** |
| **`FALLA_SEGURA`** (`comm_ok=False`) | **Caído (`OFF`)** | **`OFF` (Corte hardware)** | **Desenergizado (Cerrada)** | Cerrado (`1`) | **`OFF` (Bloqueado)** |

### 3.3 Requisitos que Debe Cumplir
- **Principio Fail-Safe:** Todo corte de alimentación o ruptura de cableado hacia `SOL-DMP` o `K1-WD` debe provocar parada del ventilador y cierre mecánico de compuerta.
- **Protección EMC / Inductiva:** Diodos volante (*flyback*) en todas las bobinas `DC` (`KM-FAN`, `SOL-DMP`, `SOL-PFE`, `K1-WD`).
- **Trazabilidad:** Nomenclatura de etiquetas exactamente igual a los textos del panel Blueprint (`K1-WD`, `SOL-PFE`) y al contrato `DuctTwinSnapshot` (`fan_on`, `damper_closed`, `pfe_active`).

### 3.4 Qué Se Debe Esperar (Entregables)
1. Proyecto EPLAN (`.zw1` / `.elk`) y exportación multi-página en **PDF vectorial** (`eplan_interlock_24vdc.pdf`).
2. Capturas en alta resolución (`PNG 1920 × 1080`) de las hojas de potencia y cadena `K1-WD` / `SOL-PFE` para integrar en la pestaña `Blueprint` y en las slides del pitch.
3. Lista de bornes y cables (*Terminal Diagram* / *Wire List*) exportada desde EPLAN.

---

## 4. Detalle Profundo — `EXT-03`: Simulación Electrónica en Proteus ISIS (Perfil A `meca`)

### 4.1 Propósito y Alcance
Demostrar la etapa física de adquisición de sensores, filtrado analógico, disparo de actuadores y envío de telemetría serial verificada que alimentaría al módulo `SensorDecisionTreeModel` (`backend/duct_twin.py`).
- **Dentro del alcance:** Esquemático completo en Proteus ISIS con sensores simulados mediante fuentes/potenciómetros calibrados, acondicionamiento analógico, firmware en MCU (`STM32F103C8` o `ATmega328P` / Arduino Uno) con ciclo de `100 ms`, salida `WD_HEARTBEAT` hacia circuito Watchdog y verificación por `VIRTUAL TERMINAL` + `OSCILLOSCOPE`.
- **Fuera del alcance (`F-09 WON'T HAVE`):** Conectar Proteus en tiempo real mediante puerto `COMPIM` / USB-UART al navegador web del jurado (prohibido explícitamente en `SPEC.md` y `FURPS+ F-09` para garantizar demo pública HTTPS sin drivers locales).

### 4.2 Cómo Realizarlo Bloque por Bloque
1. **Bloque 1 — Los 4 Canales Analógicos (`ADC 0..3`) Alineados con `SensorTelemetryFrame`:**
   - **`CH0` — Gradiente Térmico ($\Delta T/\Delta t$, `-5 a +100 °C/s`):** Modelo de termopar Tipo K / puente `LM35`/`POT-HG` + amplificador diferencial `LM358` o `AD8495` + filtro pasa-bajos RC ($R=10\text{ k}\Omega, C=1.5\,\mu\text{F} \Rightarrow f_c \approx 10.6\text{ Hz}$) para eliminar ruido de conmutación.
   - **`CH1` — Monóxido de Carbono ($\text{CO}$, `0 a 5000 ppm`):** Emulación de celda electroquímica (`0.0–5.0 V` proporcional) con etapa seguidora de tensión y diodo de protección Schottky `BAT54S` al pin `ADC1`.
   - **`CH2` — Aerosol Submicrónico `< 0.1 µm` (`0 a 100%`, `Spinoff 9407`):** Fotodiodo + amplificador de transimpedancia (`TIA` con `LM358`) emulando dispersión óptica de partículas ultrafinas previas a la llama visible.
   - **`CH3` — Velocidad de Flujo de Aire (`0 a 60 cm/s`):** Puente de Wheatstone emulando anemómetro térmico calibrado a `0–5 V`.
2. **Bloque 2 — Microcontrolador y Firmware Determinista (`100 ms` / `10 Hz`):**
   - Leer los 4 canales cada `100 ms` por interrupción de Timer (cero `delay()` bloqueantes).
   - Aplicar filtro de media móvil (`N = 5` muestras) y calcular $\Delta T/\Delta t$ discreto entre muestras consecutivas.
   - Emitir señal cuadrada `WD_HEARTBEAT` (`10 Hz`) hacia un circuito detector de pulsos (`charge pump` + relé `K1-WD` de `EPLAN`); si el firmware se detiene, el relé cae en `< 300 ms`.
   - Construir trama UART a `115200 bps` con **checksum `CRC-8` (polinomio `0x07`)**:
     - Formato sugerido: `$IGNIS,<dTdt>,<CO>,<Aerosol>,<Flow>,<State>,<CRC8>\r\n`
3. **Bloque 3 — Etapas de Salida Aisladas (Optoacopladores + Relés/MOSFET):**
   - Tres salidas digitales (`FAN_EN`, `DAMPER_OPEN`, `PFE_FIRE`) manejadas mediante optoacopladores `PC817` + transistor `2N2222` / MOSFET `IRLZ44N` con LEDs indicadores y diodos `1N4007` sobre las cargas inductivas simuladas (`24 V`).
4. **Bloque 4 — Instrumentación Virtual de Prueba:**
   - Conectar `VIRTUAL TERMINAL` (`115200 8N1`) al pin `TX` del MCU para inspeccionar las tramas `CRC-8`.
   - Conectar `OSCILLOSCOPE` a `WD_HEARTBEAT` y al pin de disparo `PFE_FIRE`.
   - Opcional en captura: simular corte de pulso `WD_HEARTBEAT` con un interruptor de falla y mostrar en osciloscopio la transición inmediata a `FALLA_SEGURA`.

### 4.3 Requisitos que Debe Cumplir
- **Frecuencia de muestreo:** Periodo estricto de `100 ms` (`10 Hz`) coherente con el texto embebido en `frontend/index.html` (`Muestreo 100 ms · CRC-8 115200bps`).
- **Rangos de entrada idénticos a `SensorTelemetryFrame` (`backend/duct_twin.py`):**
  - $\Delta T/\Delta t \in [-5, 100]\,^\circ\text{C/s}$, $\text{CO} \in [0, 5000]\text{ ppm}$, Aerosol $\in [0, 100]\%$, Flujo $\in [0, 60]\text{ cm/s}$.
- **Integridad de trama:** Cada paquete serial incluye byte `CRC-8` calculado sobre los campos previos.

### 4.4 Qué Se Debe Esperar (Entregables)
1. Archivo esquemático Proteus (`.pdsprj`) + código fuente firmware en C/C++ (`.ino` / `main.c`) + binario compilado (`.hex`).
2. Captura de pantalla (`1920 × 1080` PNG) mostrando el circuito simulando en vivo con el `VIRTUAL TERMINAL` imprimiendo tramas `CRC-8` y el `OSCILLOSCOPE` mostrando el pulso `WD_HEARTBEAT`.
3. Prueba documentada de 2 escenarios: (a) *Llama Fría NTC* (sube aerosol `< 0.1 µm`, `dT/dt` bajo -> `PRE_ALERTA`), (b) *Falla de Watchdog* (caída de pulso -> `FALLA_SEGURA`).

---

## 5. Priorización MoSCoW Completa de Tareas Externas

| Prioridad MoSCoW | Tareas | Justificación Estratégica en Hackathon |
| :--- | :--- | :--- |
| **MUST HAVE** | `J-04` (Activación Render + UptimeRobot e incógnito), `J-05` (Video 1080p), `J-06` (Envío Space Apps) | Sin URL pública HTTPS ni video ni formulario enviado a tiempo, el proyecto queda descalificado aunque los CAD/ECAD sean perfectos. |
| **SHOULD HAVE** | `EXT-02` (**EPLAN `24 VDC` Fail-Safe**) | Respalda directamente la credibilidad de ingeniería de control (`F-04`) y el argumento diferenciador de *enclavamiento hardware independiente de la IA*. Es el diagrama más rápido y visualmente claro para el pitch técnico. |
| **COULD HAVE** | `EXT-01` (**SolidWorks CAD Ducto**), `EXT-03` (**Proteus ISIS**) | Refuerzan `F-08` (pestaña `Blueprint` y diapositiva de arquitectura física), elevando `Validity` y `Presentation` sin bloquear ningún criterio `MUST`. |
| **WON'T HAVE** | `F-09` (Enlace serial `COMPIM` en vivo, CFD químico 3D, certificación PCB multicapa) | Excluido intencionalmente para no introducir fallos en la PC del jurado ni consumir horas críticas antes del code freeze. |

**Orden recomendado de ejecución:** `J-04` (asegurar URL en vivo) $\rightarrow$ `EXT-02` (EPLAN `24 VDC`) $\rightarrow$ `EXT-01` (SolidWorks corte + BOM) $\rightarrow$ `EXT-03` (Proteus captura `CRC-8`) $\rightarrow$ `J-05` (grabar video) $\rightarrow$ `J-06` (enviar 2h antes).

---

## 6. Recursos, Páginas, Proyectos Similares y Diferenciación de `AERO-IGNIS SI`

### 6.1 Recursos y Librerías Gratuitas para Acelerar `SolidWorks`, `EPLAN` y `Proteus` (`$0 USD`)
- **SolidWorks (CAD 3D):**
  - **NASA 3D Resources** (`nasa3d.arc.nasa.gov`) y **NASA NTRS** (`ntrs.nasa.gov`): Envolventes `ISPR`, racks `CIR`/`MSG` y planos acotados reales del módulo `Saffire` (`53 × 90 × 133 cm`).
  - **GrabCAD Community Library** (`grabcad.com/library`): Modelos gratuitos `.SLDPRT` / `.STEP` de *"motorized fire damper"*, *"HVAC duct flange"*, *"axial fan 24V"* y *"ISPR rack"*.
  - **McMaster-Carr** (`mcmaster.com`): Descarga directa gratuita de archivos SolidWorks nativos (`.SLDPRT`) de tornillería `M6`, racores `M12`, sellos O-ring y boquillas atomizadoras industriales.
  - **Greenheck / Belimo CAD Libraries:** Bloques `.STEP` gratuitos de actuadores *spring-return* para compuertas cortafuego.
- **EPLAN Electric P8 (ECAD):**
  - **EPLAN Data Portal** (incluido con licencia educativa/estándar) y **TraceParts** (`traceparts.com`): Macros `IEC 60617` de relés de seguridad, contactores `24 VDC`, interruptores magnetotérmicos y borneras.
  - **Festo / Schneider Electric CAD & Macros:** Símbolos gratuitos de electroválvulas `24 VDC` y relés de control.
- **Proteus ISIS (Electrónica y Firmware):**
  - **SnapEDA / Ultra Librarian / ComponentSearchEngine:** Huellas y símbolos esquemáticos gratuitos importables a Proteus cuando un sensor (`AD8495`, `STM32`) no venga en librería base.
  - **Wokwi (`wokwi.com`)** como apoyo rápido gratuito para probar el firmware C/C++ del cálculo `CRC-8` y temporizador `100 ms` antes de compilar el `.hex` para Proteus.

### 6.2 Proyectos Similares y Cómo Se Diferencia `AERO-IGNIS SI`

| Categoría / Referente | Qué Hacen los Proyectos Similares | Cómo Se Diferencia `AERO-IGNIS SI` |
| :--- | :--- | :--- |
| **1. Hardware Científico NASA (`Saffire I–VI`, `BASS-II`, `CIR`/`MSG`)** | Plataformas experimentales pasivas o teleoperadas diseñadas para *registrar* propagación de llama en cintas y videos (11–255 GB) para análisis científico posterior. | No solo archiva ensayos: convierte las 24 investigaciones PSI en un **sistema predictivo de seguridad operativa en vivo** con `RandomForest/GBR`, sandbox *What-If* lunar (`34% O2 / 8.2 psi`) y controlador autónomo de ducto. |
| **2. Ganadores NASA Space Apps Previos (`Starflock` 2022, `PureFlow` 2025, `SpaceGenes+` 2025)** | Cada ganador destacó en **un solo eje**: `Starflock` en química de humo/aerosoles, `PureFlow` en diseño de hábitats, `SpaceGenes+` en metadatos OSDR/ISA-Tab. | **`AERO-IGNIS SI` integra los tres ejes más control hardware en una sola plataforma:** catálogo/ranking `TOPSIS + PCA + TextRank` de las 24 PSI, simulador físico ($\text{Da}, \text{Pe}$), Gemelo Digital `CNN ONNX + DecisionTree + FSM` y respaldo físico `SolidWorks + EPLAN + Proteus`. |
| **3. Proyectos Estudiantiles Típicos de Detección de Fuego (Arduino + MQ-2 + Proteus)** | Usan sensores domésticos en `1g`, lógica `if/else` simple sobre humo visible, sin respaldo eléctrico `Fail-Safe` y amarrados a puerto serial local. | Reemplaza reglas ingenuas por **física de microgravedad (`Gr -> 0`)**, detección de **llama fría invisible (`500–800 K`, `FLEX`)** y aerosol `< 0.1 µm` (`Spinoff 9407`), **histéresis anti-paradoja `BASS`**, **enclavamiento cableado EPLAN `K1-WD`** y entrega web pública 0-fricción (`$0 USD`, sin `COMPIM` local). |
| **4. Sistemas BMS / HVAC Industriales Terrestres (`NFPA 72` / `Belimo`)** | Diseñados para edificios en `1g` donde el humo caliente sube por convección natural al techo y los rociadores descargan agua masiva. | Adaptado a **cabinas presurizadas en `0g` / `0.16g`**: sensores en flujo forzado de ducto, exclusión de agentes tóxicos (`Halón`/`CO2` excesivo) en favor de **niebla fina `PFE (20–100 µm)`** e integración explícita con estándares `NASA-STD-6001` y Spinoffs terrestres (`9582, 9407, 9918`). |
