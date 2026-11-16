(function () {
  "use strict";

  const PSI_PLAIN_GUIDE = {
    "PSI-98": "Primer gran incendio controlado en una nave Cygnus: midió cómo crece el fuego sobre telas con aire en movimiento.",
    "PSI-101": "Comparó 9 materiales reales de cabina para distinguir telas seguras (Nomex) frente a plásticos que propagan fuego.",
    "PSI-102": "Demostró cuánto se acelera un incendio a gran escala cuando los ventiladores suben su velocidad un 50%.",
    "PSI-103": "Evaluó detectores de humo en atmósferas con más oxígeno y menos presión usadas antes de caminatas espaciales.",
    "PSI-104": "Simuló el aire exacto de los hábitats lunares Artemis (34% oxígeno y 8.2 psi) en un incendio de escala real.",
    "PSI-105": "Midió gases tóxicos y ácidos invisibles (CO, HF, HCl) que quedan flotando en la cabina después del incendio.",
    "PSI-26": "Probó en la ISS que una brisa suave en el espacio hace arder sólidos con menos oxígeno del que necesitan en Tierra.",
    "PSI-25": "Más de 130 pruebas en cabina: definió el mapa maestro de cuándo la llama se apaga sola o avanza en plásticos y telas.",
    "PSI-146": "Estudió llamas esféricas limpias en microgravedad para diseñar quemadores y sensores con mínima emisión de hollín.",
    "PSI-147": "Midió el punto exacto en que una llama pierde su calor por radiación y se apaga sola cuando no hay gravedad.",
    "PSI-153": "Rastreó con láser cómo nace y desaparece el hollín flotante para calibrar alarmas ópticas de humo.",
    "PSI-154": "Demostró cómo empujar y apagar llamas usando campos eléctricos de alto voltaje sin mojar equipos electrónicos.",
    "PSI-132": "Replicó materiales sólidos usando quemadores porosos precisos para abaratar pruebas de inflamabilidad.",
    "PSI-138": "Estudió llamas frías invisibles en gases hasta 85% de oxígeno para evitar re-encendidos ocultos.",
    "PSI-24": "Descubrió llamas frías silenciosas (500–800 K) que siguen quemando vapores invisibles después de apagarse la luz.",
    "PSI-27": "Midió qué cantidad exacta de gases inertes (nitrógeno, CO2, helio) apaga tanto llamas calientes como frías.",
    "PSI-78": "Proyecto NASA-JAXA que midió cómo salta el fuego de una gota de combustible a otra sin gravedad.",
    "PSI-79": "Cooperación con Italia sobre mezclas líquidas para evitar micro-explosiones en sistemas cerrados.",
    "PSI-126": "Encontró la velocidad exacta de aire capaz de arrancar y apagar una llama por efecto de soplado.",
    "PSI-129": "Midió partículas de humo menores a 0.1 micras; base directa para detectores tempranos en hospitales y naves.",
    "PSI-107": "Observó cómo hierven y se evaporan películas finas de líquido sin gravedad para mejorar enfriamiento por niebla.",
    "PSI-108": "Estudió puntos calientes en líquidos y tuberías térmicas para proteger baterías y sistemas electrónicos.",
    "PSI-109": "Validó un túnel terrestre estrecho que imita la gravedad cero y reduce costos antes de lanzar experimentos.",
    "PSI-110": "Estudió la brasa lenta sin llama abierta en espumas de relleno para detectar incendios nocturnos antes del fuego."
  };

  const OFFLINE_PSI = [
    { psi_id: "PSI-98", acronym: "SAFFIRE-I", facility: "Cygnus", doi: "10.60555/psi-98", criteria_scores: { habitat: 0.95, modeling: 0.91, sensors: 0.86, spinoff: 0.84 }, earth_benefits: "Calibrar modelos de incendio en aeronaves y edificios presurizados." },
    { psi_id: "PSI-101", acronym: "SAFFIRE-II", facility: "Cygnus", doi: "10.60555/psi-101", criteria_scores: { habitat: 0.96, modeling: 0.89, sensors: 0.80, spinoff: 0.88 }, earth_benefits: "Seleccionar textiles retardantes seguros para transporte." },
    { psi_id: "PSI-102", acronym: "SAFFIRE-III", facility: "Cygnus", doi: "10.60555/psi-102", criteria_scores: { habitat: 0.93, modeling: 0.90, sensors: 0.82, spinoff: 0.85 }, earth_benefits: "Definir cortes de ventilación en túneles y centros de datos." },
    { psi_id: "PSI-103", acronym: "SAFFIRE-IV", facility: "Cygnus", doi: "10.60555/psi-103", criteria_scores: { habitat: 0.98, modeling: 0.88, sensors: 0.92, spinoff: 0.86 }, earth_benefits: "Optimizar detectores de humo en cámaras hiperbáricas." },
    { psi_id: "PSI-104", acronym: "SAFFIRE-V", facility: "Cygnus", doi: "10.60555/psi-104", criteria_scores: { habitat: 0.99, modeling: 0.91, sensors: 0.89, spinoff: 0.87 }, earth_benefits: "Refinar normas NFPA para atmósferas enriquecidas y minas." },
    { psi_id: "PSI-105", acronym: "SAFFIRE-VI", facility: "Cygnus", doi: "10.60555/psi-105", criteria_scores: { habitat: 0.97, modeling: 0.86, sensors: 0.96, spinoff: 0.92 }, earth_benefits: "Proteger cuadrillas contra gases ácidos HF/HCl y monóxido de carbono." },
    { psi_id: "PSI-25", acronym: "BASS-II", facility: "ISS-MSG", doi: "10.60555/psi-25", criteria_scores: { habitat: 0.94, modeling: 0.99, sensors: 0.81, spinoff: 0.85 }, earth_benefits: "Calibrar simuladores de propagación de fuego en edificios." },
    { psi_id: "PSI-24", acronym: "FLEX", facility: "ISS-CIR", doi: "10.60555/psi-24", criteria_scores: { habitat: 0.85, modeling: 0.96, sensors: 0.97, spinoff: 0.88 }, earth_benefits: "Prevenir re-igniciones silenciosas por llamas frías." },
    { psi_id: "PSI-129", acronym: "SPICE", facility: "ISS-MSG", doi: "10.60555/psi-129", criteria_scores: { habitat: 0.92, modeling: 0.84, sensors: 0.99, spinoff: 0.98 }, earth_benefits: "Calibrar detectores tempranos de aerosoles menores a 0.1 micras." },
    { psi_id: "PSI-110", acronym: "MSC", facility: "Otros", doi: "10.60555/psi-110", criteria_scores: { habitat: 0.95, modeling: 0.87, sensors: 0.97, spinoff: 0.95 }, earth_benefits: "Reducir muertes por combustión latente en espumas domésticas." }
  ];

  const FORENSIC_PRESETS = {
    apollo_1: { o2_pct: 100, pressure_psi: 16.7, flow_cm_s: 5, gravity_g: "1", material: "PTFE", thickness_mm: 2.0, flow_dir: "concurrent", note: "Apollo 1 (1967): 100% de oxígeno a 16.7 psi elevó la presión de cabina hasta 29 psi en 15 segundos. Dio origen a la norma NASA-STD-6001." },
    apollo_13: { o2_pct: 100, pressure_psi: 30.0, flow_cm_s: 2, gravity_g: "0", material: "PTFE", thickness_mm: 1.2, flow_dir: "opposed", note: "Apollo 13 (1970): El simulador llega hasta 30 psi en cabina; en el tanque criogénico original, el aislamiento PTFE superó 500 grados C." },
    mir_1997: { o2_pct: 21, pressure_psi: 14.7, flow_cm_s: 12, gravity_g: "0", material: "SIBAL", thickness_mm: 5.0, flow_dir: "concurrent", note: "Mir Kvant-1 (1997): Un cartucho químico Vika ardió 14 minutos liberando su propio oxígeno; exigió extinción directa." },
    lunar_artemis: { o2_pct: 34, pressure_psi: 8.2, flow_cm_s: 12, gravity_g: "0.16", material: "SIBAL", thickness_mm: 0.8, flow_dir: "concurrent", note: "Hábitat Lunar Artemis: Mezcla de 34% O2 a 8.2 psi evaluada experimentalmente en las campañas SAFFIRE-IV y SAFFIRE-V." }
  };

  const OFFICIAL_RESOURCES = [
    { tag: "Repositorio", title: "1. NASA PSI Combustion Repository", url: "https://psi.nasa.gov/physci/repo/search?q=combustion" },
    { tag: "Divulgación", title: "2. NASA Glenn Combustion Science", url: "https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/" },
    { tag: "Video NASA", title: "3. NASA ScienceCasts: ISS Combustion", url: "https://www.youtube.com/watch?v=W1oXykoz9zg" },
    { tag: "Guía Técnica", title: "4. Researcher's Guide to ISS Combustion", url: "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/" },
    { tag: "Caso Histórico", title: "5. Apollo 1 Historical Case Study", url: "https://sma.nasa.gov/sma-disciplines/accllp/apollo-1" },
    { tag: "Caso Histórico", title: "6. Apollo 13 Historical Case Study", url: "https://sma.nasa.gov/sma-disciplines/accllp/apollo-13" },
    { tag: "Caso Histórico", title: "7. Fire Aboard Space Station Mir", url: "https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/" },
    { tag: "Spinoff 9582", title: "8. Fireman's Air Tanks (COPV)", url: "https://spinoff.nasa.gov/node/9582" },
    { tag: "Spinoff 9407", title: "9. Incipient Fire Detector (Shuttle)", url: "https://spinoff.nasa.gov/node/9407" },
    { tag: "Spinoff 9918", title: "10. Fire Attire PBI & PFE Mist", url: "https://spinoff.nasa.gov/node/9918" }
  ];

  const SPINOFF_OFFLINE = {
    "9582": { name: "Fireman's Air Tanks (COPV)", weight: 13.0, risk: 40, psi: "PSI-104", origin: "Apollo PLSS (1976)", desc: "Cilindros compuestos de 4,500 psi reducen el peso del equipo autónomo de bomberos de 33 lb a 20 lb (-40%)." },
    "9407": { name: "Incipient Fire Detector", weight: 0.0, risk: 58, psi: "PSI-129", origin: "Transbordador Espacial (1978)", desc: "Distingue polvo ambiental frente a partículas ultrafinas de combustión menores a 0.1 micras antes de la llama abierta." },
    "9918": { name: "Fire Attire PBI / FIRES", weight: 11.5, risk: 35, psi: "PSI-101", origin: "Post-Apollo 1 (1977)", desc: "Trajes estructurales PBI y Nomex con más de 30% menos peso y alta resistencia térmica directa." },
    "PFE": { name: "ISS Fine Water Mist (PFE)", weight: 4.2, risk: 65, psi: "PSI-107", origin: "Supresión Limpia ISS", desc: "Microgotas de 20 a 100 micras seguras junto a paneles eléctricos, libres de residuos ácidos HF/HBr." }
  };

  const MUSEUM_EXHIBITS = [
    {
      img: "/assets/museum/flame_0g.jpg",
      badge: "Física Fundamental",
      title: "Llama Esférica Azul en Microgravedad",
      summary: "En la Tierra el aire caliente asciende y estira la flama en forma de lágrima. Sin flotabilidad térmica en órbita, los gases se mezclan lentamente por difusión y forman una esfera azul tenue.",
      atmosphere: "Aire de cabina normal (21% O2 · 14.7 psi · 0g)",
      phenomenon: "Baja luminosidad y combustión continua alimentada por difusión radial.",
      legacy: "Demostró que la detección en órbita necesita sensores de partículas y gas, no solo detectores visuales tradicionales.",
      caption: "Archivo NASA Glenn Research Center · Referencia 9902615"
    },
    {
      img: "/assets/museum/apollo_1_crew.jpg",
      badge: "Enero 1967 · Lección Histórica",
      title: "Apollo 1 y la Norma NASA-STD-6001",
      summary: "Un ensayo en tierra con 100% de oxígeno a 16.7 psi aceleró un incendio fatal dentro de la cápsula. El rediseño posterior prohibió esa atmósfera en plataforma e instauró pruebas estrictas para cada material.",
      atmosphere: "100% O2 puro · 16.7 psi · gravedad terrestre 1g",
      phenomenon: "Presurización súbita a 29 psi en 15 segundos sobre polímeros comunes.",
      legacy: "Fundó el estándar internacional NASA-STD-6001 para calificar plásticos, espumas, cables y telas aeroespaciales.",
      caption: "Tripulación Apollo 1 · Archivo Histórico NASA S66-30238"
    },
    {
      img: "/assets/museum/mir_station.jpg",
      badge: "Febrero 1997 · Órbita Terrestre",
      title: "Incendio en la Estación Espacial Mir",
      summary: "Un generador sólido de oxígeno en el módulo Kvant-1 entró en reacción térmica y liberó chorros incandescentes durante 14 minutos porque producía su propio oxidante químico.",
      atmosphere: "21% O2 · 14.7 psi · 0g (Módulo Kvant-1)",
      phenomenon: "Combustión auto-oxidante de perclorato de litio (LiClO4).",
      legacy: "Confirmó que apagar la ventilación no basta en reacciones auto-oxidantes y aceleró la adopción de niebla fina de agua en la ISS.",
      caption: "Estación Mir vista desde Discovery · NASA STS063-708-095"
    },
    {
      img: "/assets/museum/bass_ii_iss.jpg",
      badge: "2014 · ISS Expedition 40",
      title: "Campaña BASS-II: Sólidos en Caída Libre",
      summary: "Astronautas operaron muestras de acrílico PMMA, algodón y telas espaciales dentro de una caja sellada con ventilador regulable para medir velocidades reales de avance de llama.",
      atmosphere: "15% a 23% O2 · flujo forzado de 0 a 50 cm/s · 0g",
      phenomenon: "El flujo opuesto y el concurrente cambian drásticamente la longitud de llama.",
      legacy: "Aportó la base numérica principal para validar simuladores térmicos y reglas de corte rápido de aire.",
      caption: "Experimento BASS-II en la ISS · NASA ISS040E086481"
    },
    {
      img: "/assets/museum/saffire_cygnus.jpg",
      badge: "2016–2023 · Naves Cygnus",
      title: "Serie Saffire I–VI a Escala Real",
      summary: "Seis módulos instalados en naves de carga automáticas tras abandonar la ISS permitieron observar incendios de gran tamaño sin poner en riesgo a la tripulación.",
      atmosphere: "Hasta 34% O2 y 8.2 psi (equivalente a hábitat lunar)",
      phenomenon: "Propagación tridimensional y generación de gases ácidos con tejidos SIBAL.",
      legacy: "Validó directamente los límites de inflamabilidad para las futuras misiones lunares del programa Artemis.",
      caption: "Hardware experimental Saffire · NASA GRC-2014-C-02323"
    },
    {
      img: "/assets/museum/cir_rack_iss.jpg",
      badge: "2009–Actualidad · ISS Rack CIR",
      title: "Llamas Frías en el Rack CIR (FLEX)",
      summary: "Al estudiar combustión de gotas en microgravedad, investigadores notaron que varias muestras seguían reaccionando sin flama luminosa visible entre 500 y 800 K tras extinguirse.",
      atmosphere: "Mezclas nitrógeno-oxígeno y helio-oxígeno en cámara presurizada",
      phenomenon: "Oxidación en régimen de coeficiente térmico negativo (NTC) sin hollín.",
      legacy: "Impulsó el monitoreo combinado de aerosoles submicrónicos y monóxido de carbono para detectar fallas latentes.",
      caption: "Combustion Integrated Rack (CIR) · NASA GRC-2005-C-00892"
    }
  ];

  const GLOSSARY_TERMS = [
    { term: "Microgravedad (0g)", tag: "Física básica", def: "Estado de caída libre continua en órbita. Los objetos no pierden masa, pero desaparece la diferencia de peso entre aire frío denso y aire caliente liviano." },
    { term: "Convección natural vs. Difusión", tag: "Transporte de calor", def: "En la Tierra, la convección sube el humo y atrae oxígeno fresco desde abajo. En el espacio manda la difusión molecular, un movimiento mucho más lento." },
    { term: "Llama Esférica Azul", tag: "Régimen visual", def: "Forma característica de una flama tranquila en gravedad cero. Produce muy poco hollín amarillo y emite una luz azul tenue difícil de distinguir a simple vista." },
    { term: "Llama Fría (Cool Flame / NTC)", tag: "Combustión silenciosa", def: "Reacción química sin llama brillante que ocurre alrededor de 500 a 800 Kelvin. Libera humo invisible ultrafino y gases tóxicos antes de una posible re-ignición." },
    { term: "Número de Damköhler (Da)", tag: "Parámetro adimensional", def: "Relación entre la velocidad de reacción química del incendio y el tiempo de paso del flujo de aire. Valores altos indican combustión vigorosa difícil de apagar." },
    { term: "Número de Péclet (Pe)", tag: "Parámetro térmico", def: "Compara el transporte de calor arrastrado por la ventilación frente a la conducción térmica del material. Ayuda a definir cuándo el aire enfría o aviva la brasa." },
    { term: "Extinción por Radiación (Quenching)", tag: "Límite inferior", def: "Ocurre cuando la ventilación es casi nula en microgravedad: el calor escapa por radiación térmica y el dióxido de carbono propio termina ahogando la llama." },
    { term: "Extinción por Soplado (Blowoff)", tag: "Límite superior", def: "Si la corriente de aire supera la velocidad química con la que avanza la reacción, el flujo desprende el frente de llama y apaga la combustión local." },
    { term: "Combustión Latente (Smoldering)", tag: "Fase temprana", def: "Degradación térmica lenta y sin llama abierta en espumas o aislantes de cables. Produce partículas menores a 0.1 micras y monóxido de carbono medible minutos antes del fuego." },
    { term: "Norma NASA-STD-6001", tag: "Regulación espacial", def: "Estándar técnico que establece las pruebas obligatorias de propagación ascendente, toxicidad y desgasificación para aprobar materiales dentro de naves habitables." },
    { term: "Niebla Fina de Agua (PFE)", tag: "Supresión limpia", def: "Extintor portátil usado en la Estación Espacial Internacional que rocía gotas diminutas (20 a 100 micras). Enfría el fuego sin dejar residuos corrosivos sobre electrónica." },
    { term: "Índice NPR y Matriz FMEA", tag: "Gestión de riesgo", def: "Herramienta que multiplica Gravedad, Ocurrencia y Dificultad de Detección de cada falla (NPR) para priorizar barreras mecánicas y electrónicas antes de volar." }
  ];

  let apiOnline = false;
  let fsmLocalTicks = 0;
  let explorerDebounce = null;
  let sandboxDebounce = null;
  let lastRankedTopId = "PSI-104";

  function escapeHtml(raw) {
    return String(raw)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function apiJson(url, options) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error("HTTP " + res.status);
    apiOnline = true;
    return res.json();
  }

  function switchTab(tabId) {
    document.querySelectorAll('[role="tab"]').forEach((btn) => {
      btn.setAttribute("aria-selected", String(btn.dataset.tab === tabId));
    });
    document.querySelectorAll('[role="tabpanel"]').forEach((panel) => {
      panel.classList.toggle("is-active", panel.id === "panel-" + tabId);
    });
  }

  // --- MODULO 2: EXPLORADOR & MAPA DE SIMILITUD ---
  function renderClustersSvg(points, topPsiId) {
    const svg = document.getElementById("clustersSvg");
    const colors = ["#0B3D91", "#065F46", "#C82812", "#4B2E83"];
    if (!points.length) {
      svg.innerHTML = "";
      return;
    }
    const clamp = (val, lo, hi) => Math.min(hi, Math.max(lo, val));
    const xs = points.map((p) => p.x);
    const ys = points.map((p) => p.y);
    const padMinX = Math.min(...xs, -0.05) - 0.06;
    const padMaxX = Math.max(...xs, 0.05) + 0.06;
    const padMinY = Math.min(...ys, -0.05) - 0.06;
    const padMaxY = Math.max(...ys, 0.05) + 0.06;
    const spanX = Math.max(0.12, padMaxX - padMinX);
    const spanY = Math.max(0.12, padMaxY - padMinY);

    // Marco interno: x [42..524], y [22..266]. Zona activa de puntos: x [56..504], y [62..228]
    const toPlotX = (vx) => 56 + ((vx - padMinX) / spanX) * 448;
    const toPlotY = (vy) => 228 - ((vy - padMinY) / spanY) * 166;

    const hasZeroX = padMinX < 0 && padMaxX > 0;
    const hasZeroY = padMinY < 0 && padMaxY > 0;
    const axisX = clamp(hasZeroX ? toPlotX(0) : 283, 145, 410);
    const axisY = clamp(hasZeroY ? toPlotY(0) : 145, 74, 212);

    const coords = points.map((pt, idx) => ({
      pt,
      idx,
      nx: clamp(toPlotX(pt.x), 56, 504),
      ny: clamp(toPlotY(pt.y), 62, 226),
      isTop: pt.psi_id === topPsiId
    }));

    // Separacion deterministica leve si dos puntos caen casi encima
    for (let i = 0; i < coords.length; i += 1) {
      for (let j = i + 1; j < coords.length; j += 1) {
        const dx = coords[j].nx - coords[i].nx;
        const dy = coords[j].ny - coords[i].ny;
        const d = Math.hypot(dx, dy);
        if (d < 9) {
          const ang = (j * 2.1) % (Math.PI * 2);
          coords[j].nx = clamp(coords[j].nx + Math.cos(ang) * 8.2, 54, 506);
          coords[j].ny = clamp(coords[j].ny + Math.sin(ang) * 8.2, 60, 228);
        }
      }
    }

    const order = [...coords].sort((a, b) => (a.isTop === b.isTop ? a.ny - b.ny : a.isTop ? -1 : 1));
    // Pre-reservar cajas de las 4 cabeceras de cuadrante para evitar superposicion con etiquetas
    const placedBoxes = [
      { x1: 46, y1: 25, x2: 236, y2: 55 },
      { x1: 318, y1: 25, x2: 520, y2: 55 },
      { x1: 46, y1: 234, x2: 244, y2: 264 },
      { x1: 312, y1: 234, x2: 520, y2: 264 }
    ];
    const offsets = [
      [10, 3], [-1, 3], [0, -12], [0, 16],
      [12, -13], [-1, -13], [12, 18], [-1, 18],
      [24, -20], [24, 24], [-1, -22], [-1, 26],
      [0, -27], [0, 30], [34, -30], [34, 34],
      [-1, -32], [-1, 36], [44, -8], [-1, -8],
      [0, -40], [0, 42], [52, -24], [-1, 24]
    ];

    const placed = order.map((item) => {
      const label = item.pt.acronym || item.pt.psi_id;
      const w = Math.max(28, label.length * 5.25 + 6);
      let best = null;
      for (const [oxRaw, oy] of offsets) {
        const ox = oxRaw === -1 ? -w - 9 : oxRaw;
        const tx = clamp(item.nx + ox, 46, 518 - w);
        const ty = clamp(item.ny + oy, 64, 232);
        const box = { x1: tx - 2, y1: ty - 9, x2: tx + w, y2: ty + 2.5 };

        let hits = 0;
        for (const prev of placedBoxes) {
          if (box.x1 < prev.x2 && box.x2 > prev.x1 && box.y1 < prev.y2 && box.y2 > prev.y1) hits += 1;
        }
        let dotHits = 0;
        for (const d of coords) {
          const cx = clamp(d.nx, box.x1, box.x2);
          const cy = clamp(d.ny, box.y1, box.y2);
          if (Math.hypot(d.nx - cx, d.ny - cy) < 6.8) dotHits += 1;
        }
        const dist = Math.hypot((tx + w * 0.5) - item.nx, (ty - 3) - item.ny);
        const cost = hits * 12000 + dotHits * 1100 + dist;
        if (!best || cost < best.cost) best = { tx, ty, box, cost };
        if (hits === 0 && dotHits === 0 && dist < 24) break;
      }
      placedBoxes.push(best.box);
      return { ...item, label, w, tx: best.tx, ty: best.ty, box: best.box };
    });

    const quadrantBg = `
      <rect x="42" y="22" width="${(axisX - 42).toFixed(1)}" height="${(axisY - 22).toFixed(1)}" fill="rgba(200, 40, 18, 0.045)" />
      <rect x="${axisX.toFixed(1)}" y="22" width="${(524 - axisX).toFixed(1)}" height="${(axisY - 22).toFixed(1)}" fill="rgba(6, 95, 70, 0.045)" />
      <rect x="42" y="${axisY.toFixed(1)}" width="${(axisX - 42).toFixed(1)}" height="${(266 - axisY).toFixed(1)}" fill="rgba(11, 61, 145, 0.045)" />
      <rect x="${axisX.toFixed(1)}" y="${axisY.toFixed(1)}" width="${(524 - axisX).toFixed(1)}" height="${(266 - axisY).toFixed(1)}" fill="rgba(75, 46, 131, 0.045)" />
    `;

    const quadrantHeaders = `
      <g>
        <rect x="48" y="27" width="184" height="25" rx="3" fill="#FFEAE5" stroke="#C82812" stroke-width="0.9" />
        <text x="55" y="38" fill="#9E1C0B" font-size="8.2" font-weight="bold" font-family="monospace">I · GOTAS Y LLAMAS FRÍAS</text>
        <text x="55" y="48" fill="#1E2E4A" font-size="7.3" font-family="sans-serif">Líquidos y vapores silenciosos (CIR)</text>

        <rect x="326" y="27" width="192" height="25" rx="3" fill="#E6F6F0" stroke="#065F46" stroke-width="0.9" />
        <text x="511" y="38" text-anchor="end" fill="#065F46" font-size="8.2" font-weight="bold" font-family="monospace">II · INCENDIOS A GRAN ESCALA</text>
        <text x="511" y="48" text-anchor="end" fill="#1E2E4A" font-size="7.3" font-family="sans-serif">Cabinas Cygnus y atmósfera lunar</text>

        <rect x="48" y="236" width="192" height="25" rx="3" fill="#E0ECFF" stroke="#0B3D91" stroke-width="0.9" />
        <text x="55" y="247" fill="#0B3D91" font-size="8.2" font-weight="bold" font-family="monospace">III · GASES, HOLLÍN Y CAMPOS</text>
        <text x="55" y="257" fill="#1E2E4A" font-size="7.3" font-family="sans-serif">Química de flama, humo &lt;0.1 um y kV</text>

        <rect x="318" y="236" width="200" height="25" rx="3" fill="#F3E8FF" stroke="#4B2E83" stroke-width="0.9" />
        <text x="511" y="247" text-anchor="end" fill="#4B2E83" font-size="8.2" font-weight="bold" font-family="monospace">IV · SÓLIDOS Y BRASAS LENTAS</text>
        <text x="511" y="257" text-anchor="end" fill="#1E2E4A" font-size="7.3" font-family="sans-serif">Telas, acrílicos, cables y espumas</text>
      </g>
    `;

    const axisCaptions = `
      <text x="283" y="14" text-anchor="middle" fill="#0A1931" font-size="8.6" font-weight="bold" font-family="sans-serif">4 cuadrantes por tipo de combustible y escala de la nave espacial</text>
      <text x="48" y="282" text-anchor="start" fill="#1E2E4A" font-size="8" font-family="sans-serif">← Cámaras pequeñas en la ISS</text>
      <text x="283" y="282" text-anchor="middle" fill="#0B3D91" font-size="8" font-weight="bold" font-family="sans-serif">| Eje Horizontal: Escala del Ensayo |</text>
      <text x="518" y="282" text-anchor="end" fill="#1E2E4A" font-size="8" font-family="sans-serif">Naves completas Cygnus / Sólidos →</text>
      <text x="283" y="297" text-anchor="middle" fill="#415678" font-size="7.6" font-family="sans-serif">Cada punto representa un estudio oficial NASA; los puntos cercanos comparten objetivos, sensores y física.</text>
      <text x="16" y="144" transform="rotate(-90 16 144)" text-anchor="middle" fill="#1E2E4A" font-size="8" font-weight="bold" font-family="sans-serif">← Gases y Sólidos   |   Gotas y Escala Nave →</text>
    `;

    const leaders = placed.map((p) => {
      const ax = clamp(p.nx, p.box.x1, p.box.x2);
      const ay = clamp(p.ny, p.box.y1, p.box.y2);
      if (Math.hypot(ax - p.nx, ay - p.ny) <= 10.5) return "";
      return `<line x1="${p.nx.toFixed(1)}" y1="${p.ny.toFixed(1)}" x2="${ax.toFixed(1)}" y2="${ay.toFixed(1)}" stroke="#7E97B8" stroke-width="0.9" stroke-dasharray="2 1.5" />`;
    }).join("");

    const dots = placed.map((p) => {
      const fill = colors[p.pt.cluster_id % colors.length];
      const halo = p.isTop ? `<circle cx="${p.nx.toFixed(1)}" cy="${p.ny.toFixed(1)}" r="9.8" fill="none" stroke="#C82812" stroke-width="2.1" />` : "";
      const note = PSI_PLAIN_GUIDE[p.pt.psi_id] || "";
      return `<g>${halo}<circle cx="${p.nx.toFixed(1)}" cy="${p.ny.toFixed(1)}" r="5.5" fill="${fill}" stroke="#FFFFFF" stroke-width="1.3" opacity="0.96" /><title>${escapeHtml(p.pt.psi_id + " · " + p.label + ": " + note)}</title></g>`;
    }).join("");

    const labels = placed.map((p) => {
      const ink = p.isTop ? "#C82812" : "#1E2E4A";
      const weight = p.isTop ? "700" : "600";
      return `<g><rect x="${(p.tx - 1.5).toFixed(1)}" y="${(p.ty - 8.5).toFixed(1)}" width="${p.w.toFixed(1)}" height="11" rx="2" fill="rgba(255,255,255,0.9)" /><text x="${p.tx.toFixed(1)}" y="${p.ty.toFixed(1)}" fill="${ink}" font-size="8.2" font-weight="${weight}" font-family="monospace">${escapeHtml(p.label)}</text></g>`;
    }).join("");

    svg.innerHTML = `<rect x="42" y="22" width="482" height="244" rx="3" fill="#FFFFFF" stroke="#9EB4D4" stroke-width="1.2" />${quadrantBg}<line x1="42" y1="${axisY.toFixed(1)}" x2="524" y2="${axisY.toFixed(1)}" stroke="#9EB4D4" stroke-width="1.1" stroke-dasharray="5 3" /><line x1="${axisX.toFixed(1)}" y1="22" x2="${axisX.toFixed(1)}" y2="266" stroke="#9EB4D4" stroke-width="1.1" stroke-dasharray="5 3" />${quadrantHeaders}${leaders}${dots}${labels}${axisCaptions}`;
  }

  function refreshExplorerLabels() {
    document.getElementById("wHabVal").textContent = document.getElementById("wHabSlider").value;
    document.getElementById("wModVal").textContent = document.getElementById("wModSlider").value;
    document.getElementById("wSenVal").textContent = document.getElementById("wSenSlider").value;
  }

  function scheduleExplorerAndTopsis() {
    refreshExplorerLabels();
    clearTimeout(explorerDebounce);
    explorerDebounce = setTimeout(runExplorerAndTopsis, 110);
  }

  async function runExplorerAndTopsis() {
    refreshExplorerLabels();
    const wHab = Number(document.getElementById("wHabSlider").value);
    const wMod = Number(document.getElementById("wModSlider").value);
    const wSen = Number(document.getElementById("wSenSlider").value);

    const facility = document.getElementById("psiFacilitySelect").value;
    const persona = document.getElementById("personaSelect").value;
    const query = document.getElementById("psiQueryInput").value.trim().slice(0, 120);

    try {
      const data = await apiJson("/api/v1/psi/rank-and-interpret", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          weights: { habitat: wHab, modeling: wMod, sensors: wSen * 0.55, spinoff: wSen * 0.45 },
          persona,
          query
        })
      });
      const filtered = facility ? data.ranked.filter((r) => r.facility === facility) : data.ranked;
      renderExplorerOutput(filtered, data.clusters_2d, data.synthesis, { wHab, wMod, wSen });
    } catch (_) {
      apiOnline = false;
      const total = Math.max(1, wHab + wMod + wSen);
      const qTokens = query.toLowerCase().split(/\s+/).filter(Boolean);
      const scored = OFFLINE_PSI
        .filter((d) => !facility || d.facility === facility)
        .map((d, idx) => {
          const hay = `${d.psi_id} ${d.acronym} ${d.facility} ${d.earth_benefits}`.toLowerCase();
          const boost = qTokens.length ? qTokens.filter((t) => hay.includes(t)).length * 0.14 : 0;
          const score = (
            d.criteria_scores.habitat * wHab +
            d.criteria_scores.modeling * wMod +
            ((d.criteria_scores.sensors + d.criteria_scores.spinoff) * 0.5) * wSen
          ) / total + boost;
          return { ...d, rank: idx + 1, topsis_score: Math.min(0.999, score) };
        })
        .sort((a, b) => b.topsis_score - a.topsis_score)
        .map((d, i) => ({ ...d, rank: i + 1 }));

      const pts = scored.map((d, i) => ({
        psi_id: d.psi_id,
        acronym: d.acronym,
        x: Math.cos(i * 0.85) * (0.32 + (i % 3) * 0.14),
        y: Math.sin(i * 1.15) * (0.3 + ((i + 1) % 3) * 0.15),
        cluster_id: i % 4
      }));
      const top = scored[0] || OFFLINE_PSI[0];
      const peer = scored[1] || OFFLINE_PSI[1];
      renderExplorerOutput(scored, pts, {
        persona,
        bullets: [
          `Estudio líder #1 (${top.psi_id} · ${top.acronym}, ${top.facility}): encabeza tu prioridad actual (${top.doi}).`,
          `Aporte práctico: ${top.earth_benefits}`,
          `Campaña complementaria #2: ${peer.psi_id} (${peer.acronym}) aporta evidencia de soporte (${peer.doi}).`
        ],
        cited_dois: [top.doi, peer.doi]
      }, { wHab, wMod, wSen });
    }
  }

  function renderExplorerOutput(ranked, clusters, synthesis, weights) {
    const top = ranked[0];
    if (top) lastRankedTopId = top.psi_id;
    document.getElementById("synthesisPersonaBadge").textContent = "Síntesis de Evidencia · " + synthesis.persona;
    document.getElementById("citedDoisLine").textContent = synthesis.cited_dois.join(" · ");
    const explainer = document.getElementById("synthesisExplainer");
    if (explainer && top && weights) {
      explainer.textContent = `Resumen automático centrado en el puesto #1 de tu tabla (${top.psi_id} · ${top.acronym}) según tus pesos actuales (Hábitat ${weights.wHab}%, Modelado ${weights.wMod}%, Sensores ${weights.wSen}%).`;
    }
    document.getElementById("synthesisBullets").innerHTML = synthesis.bullets
      .map((b) => `<li>${escapeHtml(b)}</li>`)
      .join("");
    renderClustersSvg(clusters, lastRankedTopId);
    document.getElementById("psiRankBody").innerHTML = ranked.slice(0, 12).map((r) => {
      const importance = PSI_PLAIN_GUIDE[r.psi_id] || "Evidencia NASA de combustión en cabinas sin gravedad.";
      return `
      <tr>
        <td class="mono" data-label="Orden"><strong>#${r.rank}</strong></td>
        <td data-label="Estudio e Instalación">
          <strong>${escapeHtml(r.psi_id)} · ${escapeHtml(r.acronym)}</strong><br />
          <span class="badge badge-info" style="margin-top:4px;">${escapeHtml(r.facility)}</span>
        </td>
        <td data-label="Importancia">${escapeHtml(importance)}</td>
        <td class="mono tabular" data-label="Índice y DOI">
          <strong>${Number(r.topsis_score).toFixed(3)}</strong><br />
          <small>${escapeHtml(r.doi)}</small>
        </td>
      </tr>`;
    }).join("");
  }

  // --- MODULO 3: INFLAMABILIDAD EN CABINA ---
  function renderFlammabilityContour(params) {
    const svg = document.getElementById("flammabilityContourSvg");
    const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
    const { o2, flow, press, thick, grav, mat, fdir } = params;

    const sMin = Math.sqrt(14);
    const sMax = Math.sqrt(100);
    const oxToX = (pct) => 48 + ((Math.sqrt(clamp(pct, 14, 100)) - sMin) / (sMax - sMin)) * 405;
    const flToY = (fl) => 240 - (clamp(fl, 0, 60) / 60) * 205;

    const matEase = { Algodon: 1.35, PMMA: 1.15, SIBAL: 1.05, Nomex: 0.48, Kapton: 0.38, PTFE: 0.28 }[mat] || 1.0;
    const pressScale = Math.pow(14.7 / Math.max(5, press), 0.26);
    const thickScale = 1 + 0.16 * Math.log1p(Math.max(0.2, thick));
    const dirScale = fdir === "concurrent" ? 0.88 : 1.08;
    const gravScale = 1 - 0.12 * grav;

    const o2Loc = clamp(21.0 * Math.pow(1 / matEase, 0.42) * pressScale * thickScale * dirScale * gravScale, 15.2, 54.0);
    const quenchFlow = grav > 0.35 ? 1.2 : clamp(2.2 + 0.42 * thick - 0.05 * (press - 8.2) + (matEase < 0.6 ? 1.6 : 0), 1.2, 9.5);
    const yQuench = flToY(quenchFlow);

    const blowoffFactor = Math.max(0.45, Math.sqrt(press / 14.7) * Math.pow(matEase, 0.35) / thickScale);
    const curvePts = [];
    for (let fl = quenchFlow; fl <= 60; fl += 3) {
      const lowFlowPen = fl < 10 ? (10 - fl) * 0.22 : 0;
      const highFlowPen = fl > 16 ? (0.011 * Math.pow(fl - 16, 1.58)) / blowoffFactor : 0;
      const o2Bound = clamp(o2Loc + lowFlowPen + highFlowPen, 14.5, 96.0);
      curvePts.push(`${oxToX(o2Bound).toFixed(1)},${flToY(fl).toFixed(1)}`);
    }
    const lastO2Top = clamp(o2Loc + (0.011 * Math.pow(44, 1.58)) / blowoffFactor, 14.5, 96.0);
    curvePts.push(`${oxToX(lastO2Top).toFixed(1)},35`);

    const sustainedPath = `M ${curvePts.join(" L ")} L 453 35 L 453 240 L ${oxToX(o2Loc + 1.8).toFixed(1)} 240 Z`;
    const blowRightTopX = clamp(oxToX(lastO2Top) - 18, 120, 310);
    const blowMidX = clamp(oxToX(o2Loc) - 16, 95, 250);

    const px = oxToX(o2);
    const py = flToY(flow);
    const tagText = `${o2}% O2 · ${press.toFixed(1)} psi · ${thick.toFixed(1)} mm`;
    const tagW = tagText.length * 5.0 + 10;
    const tagX = clamp(px + (px > 315 ? -tagW - 11 : 11), 52, 449 - tagW);
    const tagY = clamp(py - 8, 40, 224);

    const ticks = [21, 34, 60].map((v) => {
      const tx = oxToX(v).toFixed(1);
      return `<line x1="${tx}" y1="35" x2="${tx}" y2="240" stroke="#DCE6F5" stroke-dasharray="3 3" /><text x="${tx}" y="254" text-anchor="middle" fill="#415678" font-size="8.5" font-family="monospace">${v}%</text>`;
    }).join("");

    svg.innerHTML = `
      <rect x="48" y="35" width="405" height="205" fill="#FFFFFF" stroke="#9EB4D4" />
      <line x1="48" y1="138" x2="453" y2="138" stroke="#DCE6F5" stroke-dasharray="4 3" />
      ${ticks}
      <text x="${oxToX(100).toFixed(1)}" y="254" text-anchor="end" fill="#415678" font-size="8.5" font-family="monospace">100%</text>
      <rect x="48" y="${yQuench.toFixed(1)}" width="165" height="${(240 - yQuench).toFixed(1)}" fill="rgba(6, 95, 70, 0.14)" />
      <text x="128" y="${Math.min(236, yQuench + 13).toFixed(1)}" text-anchor="middle" fill="#065F46" font-size="8.5" font-weight="bold" font-family="monospace">Extinción Radiativa</text>
      <polygon points="48,35 ${blowRightTopX.toFixed(1)},35 ${blowMidX.toFixed(1)},118 48,118" fill="rgba(11, 61, 145, 0.11)" />
      <text x="108" y="68" text-anchor="middle" fill="#0B3D91" font-size="9" font-weight="bold" font-family="monospace">Zona Soplado</text>
      <path d="${sustainedPath}" fill="rgba(200, 40, 18, 0.12)" stroke="#C82812" stroke-width="1.8" />
      <text x="${clamp((oxToX(o2Loc) + 453) * 0.52, 235, 385).toFixed(1)}" y="150" text-anchor="middle" fill="#9E1C0B" font-size="9.5" font-weight="bold" font-family="monospace">Propagación Sostenida</text>
      <circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="11" fill="rgba(200, 40, 18, 0.16)" />
      <circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="7" fill="#C82812" stroke="#FFFFFF" stroke-width="2" />
      <rect x="${tagX.toFixed(1)}" y="${(tagY - 10).toFixed(1)}" width="${tagW.toFixed(1)}" height="14" rx="2" fill="rgba(255,255,255,0.92)" stroke="#C5D3E8" />
      <text x="${(tagX + 5).toFixed(1)}" y="${tagY.toFixed(1)}" fill="#0A1931" font-size="8" font-weight="700" font-family="monospace">${escapeHtml(tagText)}</text>
      <text x="250" y="271" text-anchor="middle" fill="#1E2E4A" font-size="9.5" font-family="monospace">Oxígeno en Cabina (% O2)</text>
      <text x="18" y="138" transform="rotate(-90 18 138)" text-anchor="middle" fill="#1E2E4A" font-size="9.5" font-family="monospace">Flujo (cm/s)</text>
    `;
  }

  function readSandboxInputsAndPreview() {
    const o2 = Number(document.getElementById("o2Slider").value);
    const press = Number(document.getElementById("pressSlider").value);
    const flow = Number(document.getElementById("flowSlider").value);
    const thick = Number(document.getElementById("thickSlider").value);
    const grav = Number(document.getElementById("gravSelect").value);
    const mat = document.getElementById("matSelect").value;
    const fdir = document.getElementById("dirSelect").value;

    document.getElementById("o2Val").textContent = String(o2);
    document.getElementById("pressVal").textContent = press.toFixed(1);
    document.getElementById("flowVal").textContent = flow.toFixed(1);
    document.getElementById("thickVal").textContent = thick.toFixed(1);

    renderFlammabilityContour({ o2, flow, press, thick, grav, mat, fdir });
    return { o2, press, flow, thick, grav, mat, fdir };
  }

  function scheduleFlammabilitySandbox() {
    readSandboxInputsAndPreview();
    clearTimeout(sandboxDebounce);
    sandboxDebounce = setTimeout(runFlammabilitySandbox, 150);
  }

  async function runFlammabilitySandbox() {
    clearTimeout(sandboxDebounce);
    const { o2, press, flow, thick, grav, mat, fdir } = readSandboxInputsAndPreview();

    try {
      const pred = await apiJson("/api/v1/sandbox/predict-flammability", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          o2_pct: o2, pressure_psi: press, flow_cm_s: flow,
          gravity_g: grav, material: mat, thickness_mm: thick, flow_dir: fdir
        })
      });
      renderFlammabilityOutput(pred);
    } catch (_) {
      apiOnline = false;
      const mMap = { Algodon: 1.35, PMMA: 1.15, SIBAL: 1.05, Nomex: 0.42, Kapton: 0.35, PTFE: 0.25 };
      const flowEff = Math.max(0.3, flow + 12.0 * Math.pow(grav, 0.7));
      const pe = (flowEff * Math.max(0.3, thick)) / 1.8;
      const da = (0.45 * (mMap[mat] || 1) * Math.pow(o2 / 21, 2.1) * Math.pow(press / 14.7, 0.75)) / Math.max(0.35, flowEff * 0.08);
      const flamIdx = Math.pow(o2 / 21, 1.8) * (mMap[mat] || 1) * (fdir === "concurrent" ? 1.25 : 0.85) * Math.pow(press / 14.7, 0.35) / (0.65 + 0.35 * thick);
      const extProb = 1 / (1 + Math.exp(3.4 * (flamIdx - 0.78)));
      const vf = Math.max(0.05, 2.4 * flamIdx * (1 + 0.025 * Math.min(flow, 30)));
      const rawImp = [
        { feature: "Concentración O2 (%)", val: 0.34 + 0.14 * Math.min(1, Math.abs(o2 - 21) / 30) },
        { feature: "Reactividad del Material", val: 0.18 + 0.08 * (mMap[mat] || 1) },
        { feature: "Espesor de Muestra (mm)", val: 0.10 + 0.14 * Math.exp(-thick / 2.2) },
        { feature: "Velocidad de Flujo (cm/s)", val: 0.09 + 0.12 * Math.min(1, flow / 35) },
        { feature: "Presión de Cabina (psi)", val: 0.06 + 0.16 * Math.abs(press - 14.7) / 15.3 }
      ];
      const totImp = rawImp.reduce((acc, r) => acc + r.val, 0);
      const sortedImp = rawImp
        .map((r) => ({ feature: r.feature, importance: r.val / totImp }))
        .sort((a, b) => b.importance - a.importance);

      renderFlammabilityOutput({
        extinguished_prob: extProb,
        flame_spread_mm_s: vf,
        damkohler: da,
        peclet: pe,
        regime: flamIdx < 0.72 ? "Extinción Radiativa (Quenching)" : (o2 >= 32 ? "Propagación Acelerada" : "Propagación Estable 0g"),
        feature_importance: sortedImp
      });
    }
  }

  function renderFlammabilityOutput(pred) {
    document.getElementById("outExtProb").textContent = (pred.extinguished_prob * 100).toFixed(1) + "%";
    document.getElementById("outSpread").textContent = pred.flame_spread_mm_s.toFixed(2) + " mm/s";
    document.getElementById("outDa").textContent = pred.damkohler.toFixed(2);
    document.getElementById("outPe").textContent = pred.peclet.toFixed(2);
    const badge = document.getElementById("regimeBadge");
    badge.textContent = pred.regime;
    badge.className = "badge " + (pred.regime.includes("Extinción") ? "badge-ok" : "badge-danger");

    document.getElementById("featureImportanceBox").innerHTML = pred.feature_importance.slice(0, 5).map((item) => `
      <div class="bar-row">
        <span>${escapeHtml(item.feature)}</span>
        <div class="bar-track"><div class="bar-fill" style="--ratio:${Number(item.importance).toFixed(3)}"></div></div>
        <span class="mono tabular">${(item.importance * 100).toFixed(1)}%</span>
      </div>
    `).join("");
  }

  // --- MODULO 3: GEMELO DIGITAL DEL DUCTO ---
  function appendEventLog(msg) {
    const box = document.getElementById("twinEventLog");
    const ts = new Date().toLocaleTimeString();
    box.textContent = `[${ts}] ${msg}\n` + box.textContent;
  }

  async function stepDigitalTwin() {
    const preset = document.getElementById("twinPresetSelect").value;
    const commOk = document.getElementById("twinCommSelect").value === "true";
    const dt = Number(document.getElementById("dtSlider").value);
    const co = Number(document.getElementById("coSlider").value);
    const aer = Number(document.getElementById("aerSlider").value);
    const flow = Number(document.getElementById("ductFlowSlider").value);

    document.getElementById("dtVal").textContent = dt.toFixed(1);
    document.getElementById("coVal").textContent = String(co);
    document.getElementById("aerVal").textContent = String(aer);
    document.getElementById("ductFlowVal").textContent = String(flow);

    try {
      const snap = await apiJson("/api/v1/twin/step-fsm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          optical_preset: preset, delta_t_dt: dt, co_ppm: co,
          submicron_aerosol: aer, airflow_cm_s: flow, comm_ok: commOk
        })
      });
      renderTwinSnapshot(snap, preset);
    } catch (_) {
      apiOnline = false;
      let state = "NORMAL";
      if (!commOk) state = "FALLA_SEGURA";
      else if (dt >= 12 || co >= 150 || preset === "open_propagation") {
        fsmLocalTicks += 1;
        state = fsmLocalTicks >= 2 ? "CONTENCION" : "PRE_ALERTA";
      } else if (aer >= 18 || co >= 35 || preset === "cool_flame_ntc") {
        fsmLocalTicks = 1;
        state = "PRE_ALERTA";
      } else {
        fsmLocalTicks = 0;
      }
      const clsMap = { nominal: "Nominal", spherical_0g: "Llama Esférica Azul 0g", cool_flame_ntc: "Llama Fría NTC", open_propagation: "Propagación Abierta" };
      const idx = ["nominal", "spherical_0g", "cool_flame_ntc", "open_propagation"].indexOf(preset);
      const probs = [0.02, 0.02, 0.02, 0.02];
      probs[Math.max(0, idx)] = 0.94;
      renderTwinSnapshot({
        cnn_class: clsMap[preset] || "Nominal",
        cnn_probs: probs,
        tree_rule_path: `dT/dt (${dt.toFixed(1)} C/s) y partículas (${aer}%) -> ${state}`,
        fsm_state: state,
        fan_on: state === "NORMAL" || state === "PRE_ALERTA",
        damper_closed: state === "CONTENCION" || state === "FALLA_SEGURA",
        pfe_active: state === "CONTENCION"
      }, preset);
    }
  }

  function renderTwinSnapshot(snap, preset) {
    document.getElementById("twinCnnOut").textContent = snap.cnn_class;
    document.getElementById("twinFanOut").textContent = snap.fan_on ? "ACTIVA" : "APAGADA";
    document.getElementById("twinDamperOut").textContent = snap.damper_closed ? "Cerrada" : "Abierta";
    document.getElementById("twinPfeOut").textContent = snap.pfe_active ? "ACTIVO (Niebla)" : "En espera";
    document.getElementById("twinTreeRuleBox").textContent = snap.tree_rule_path;

    const fsmBadge = document.getElementById("fsmStateBadge");
    const svgLabel = document.getElementById("twinSvgFsmLabel");
    fsmBadge.textContent = "ESTADO: " + snap.fsm_state;
    svgLabel.textContent = snap.fsm_state;

    const clsColor = snap.fsm_state === "NORMAL" ? "badge-ok" : snap.fsm_state === "PRE_ALERTA" ? "badge-warn" : snap.fsm_state === "CONTENCION" ? "badge-danger" : "badge-cool";
    const svgInk = snap.fsm_state === "NORMAL" ? "#065F46" : snap.fsm_state === "PRE_ALERTA" ? "#78350F" : snap.fsm_state === "CONTENCION" ? "#991B1B" : "#0B3D91";
    fsmBadge.className = "badge " + clsColor;
    svgLabel.setAttribute("fill", svgInk);

    document.getElementById("twinFanRotor").setAttribute("class", snap.fan_on ? "fan-active" : "fan-stopped");
    document.getElementById("twinFlowGroup").setAttribute("class", snap.fan_on ? "flow-active" : "flow-stopped");
    document.getElementById("twinDamperRect").style.transform = snap.damper_closed ? "scaleY(1)" : "scaleY(0.14)";
    document.getElementById("twinMistGroup").style.display = snap.pfe_active ? "block" : "none";

    document.getElementById("twinFlame0g").style.display = preset === "spherical_0g" ? "block" : "none";
    document.getElementById("twinFlameCool").style.display = preset === "cool_flame_ntc" ? "block" : "none";
    document.getElementById("twinFlameOpen").style.display = preset === "open_propagation" ? "block" : "none";

    const labels = ["Nominal", "Esférica Azul 0g", "Llama Fría NTC", "Propagación Abierta"];
    document.getElementById("cnnProbsBox").innerHTML = snap.cnn_probs.map((p, i) => `
      <div class="bar-row">
        <span>${labels[i]}</span>
        <div class="bar-track"><div class="bar-fill" style="--ratio:${Number(p).toFixed(3)}"></div></div>
        <span class="mono tabular">${(p * 100).toFixed(1)}%</span>
      </div>
    `).join("");

    appendEventLog(`Estado=${snap.fsm_state} | Régimen=${snap.cnn_class} | Ventilación=${snap.fan_on ? "ON" : "OFF"} | Niebla=${snap.pfe_active ? "SI" : "NO"}`);
  }

  // --- MODULO 5: RIESGO FMEA Y TRANSFERENCIA TERRESTRE ---
  function humanizeFmeaText(raw) {
    return String(raw || "")
      .replace(/Enlace serial supervisor Python\s*<->\s*Controlador de ducto/gi, "Enlace serial estación <-> controlador de ducto")
      .replace(/supervisor Python/gi, "estación de monitoreo")
      .replace(/DeterministicFsmController/gi, "controlador automático de falla segura")
      .replace(/[a-z_]*cnn\s*\.?\s*onnx/gi, "modelo de visión óptica")
      .replace(/Arbol de decision tabular/gi, "reglas de decisión por sensores")
      .replace(/delta_t_dt/gi, "tasa térmica (dT/dt)")
      .replace(/corte hvac/gi, "corte de ventilación")
      .replace(/\(hardwired interlock\)/gi, "(enclavamiento eléctrico directo)")
      .replace(/\bFSM\b/g, "secuencia de emergencia");
  }

  const SUPPRESSION_PROTOCOLS = {
    auto_oxidizing: {
      agent: "Niebla fina PFE (20–100 micras)",
      cabin: "Mantener cabina presurizada y usar mascarillas O2",
      why: "Los cartuchos de LiClO4 liberan su propio oxígeno químico; el corte de aire o vacío no detiene la reacción."
    },
    laminar_diffusion: {
      agent: "Campo eléctrico ACME (+/-10 kV)",
      cabin: "Aislar ventilación puntual sin despresurizar",
      why: "Oscila y extingue flamas laminares sin descargar líquidos ni dañar tarjetas electrónicas cercanas."
    },
    habitable_general: {
      agent: "Niebla fina PFE estándar de la ISS",
      cabin: "Cerrar compuerta del ducto y detener ventilador",
      why: "Enfría el foco térmico con microgotas limpias evitando los gases corrosivos HF/HBr de halones antiguos."
    }
  };

  const FMEA_OFFLINE_ROWS = [
    { mode_id: "FM-01", subsystem: "Arnés eléctrico en cabina (>=30% O2)", failure_mode: "Pirólisis de aislamiento PTFE (>500 C)", baseline_npr: 350, active_npr: 32, mitigation: "Detección <0.1 um (Spinoff 9407) + corte eléctrico directo + PBI/Kapton", linked_psi: "PSI-129" },
    { mode_id: "FM-02", subsystem: "Ducto de ventilación en flujo bajo", failure_mode: "Ventilación estancada (<3 cm/s) con llama esférica", baseline_npr: 288, active_npr: 24, mitigation: "Histéresis temporal y cierre completo de compuerta en contención", linked_psi: "PSI-25" },
    { mode_id: "FM-03", subsystem: "Vapores orgánicos (FLEX / CFI-G)", failure_mode: "Llama fría NTC invisible (500–800 K)", baseline_npr: 405, active_npr: 28, mitigation: "Modelo de visión óptica en clase NTC y bloqueo de rearme automático", linked_psi: "PSI-24" },
    { mode_id: "FM-04", subsystem: "Espuma porosa en rack avio-electrónico", failure_mode: "Combustión latente sin llama visible", baseline_npr: 432, active_npr: 28, mitigation: "Reglas de decisión por CO, tasa térmica y aerosol submicrónico", linked_psi: "PSI-110" },
    { mode_id: "FM-05", subsystem: "Generador sólido de oxígeno (LiClO4)", failure_mode: "Reacción auto-oxidante tipo soplete", baseline_npr: 210, active_npr: 16, mitigation: "Supresión directa por niebla fina PFE + máscara de tripulación", linked_psi: "PSI-105" },
    { mode_id: "FM-06", subsystem: "Enlace serial estación <-> controlador", failure_mode: "Pérdida de comunicación UART / watchdog", baseline_npr: 216, active_npr: 6, mitigation: "Enclavamiento cableado de seguridad llevando el ducto a falla segura", linked_psi: "PSI-98" }
  ];

  function renderFmeaRows(rows, mitigated) {
    return rows.map((r) => `
      <tr>
        <td class="mono" data-label="Código"><strong>${escapeHtml(r.mode_id)}</strong></td>
        <td data-label="Subsistema y Fallo"><strong>${escapeHtml(humanizeFmeaText(r.subsystem))}</strong><br /><span>${escapeHtml(humanizeFmeaText(r.failure_mode))}</span></td>
        <td class="mono tabular" data-label="Índice NPR"><strong>${mitigated ? r.active_npr : r.baseline_npr}</strong> <small>(base ${r.baseline_npr})</small></td>
        <td data-label="Barrera de Mitigación">${escapeHtml(humanizeFmeaText(r.mitigation))}</td>
        <td class="mono" data-label="Estudio NASA">${escapeHtml(r.linked_psi)}</td>
      </tr>
    `).join("");
  }

  async function updateGovernance() {
    const mitigated = document.getElementById("fmeaMitigatedToggle").checked;
    const spinoffId = document.getElementById("spinoffSelect").value;
    const units = Number(document.getElementById("unitsSlider").value);
    document.getElementById("unitsVal").textContent = String(units);

    const suppKind = document.getElementById("suppScenarioSelect").value;
    const supp = SUPPRESSION_PROTOCOLS[suppKind] || SUPPRESSION_PROTOCOLS.habitable_general;
    document.getElementById("suppAgentOut").textContent = supp.agent;
    document.getElementById("suppCabinOut").textContent = supp.cabin;
    document.getElementById("suppWhyOut").textContent = supp.why;

    const baseOutEl = document.getElementById("fmeaBaseOut");
    const activeOutEl = document.getElementById("fmeaActiveOut");
    const dropOutEl = document.getElementById("fmeaDropOut");

    try {
      const data = await apiJson(`/api/v1/governance/fmea-and-spinoffs?mitigated=${mitigated}&spinoff_id=${encodeURIComponent(spinoffId)}&units=${units}`);
      const baseNpr = data.fmea_summary.total_baseline_npr;
      const activeNpr = data.fmea_summary.total_active_npr;
      const dropPct = data.fmea_summary.average_npr_reduction_pct;

      baseOutEl.textContent = `${baseNpr.toLocaleString()} NPR`;
      activeOutEl.textContent = `${activeNpr.toLocaleString()} NPR`;
      activeOutEl.style.color = mitigated ? "var(--accent-emerald)" : "var(--accent-crimson)";
      dropOutEl.textContent = mitigated ? `-${dropPct}%` : "0.0%";
      dropOutEl.style.color = mitigated ? "var(--accent-emerald)" : "var(--accent-amber)";

      document.getElementById("fmeaSummaryLine").textContent = mitigated
        ? "Barreras físicas y sensores activos en los 6 modos de fallo del ducto."
        : "Escenario sin barreras activas: representa el riesgo crudo antes de añadir sensores y compuerta.";

      document.getElementById("fmeaTableBody").innerHTML = renderFmeaRows(data.fmea_rows, true);
      const sp = data.spinoff_metrics;
      document.getElementById("spinWeightOut").textContent = sp.weight_saved_lb_total.toLocaleString() + " lb";
      document.getElementById("spinRiskOut").textContent = "-" + sp.risk_reduction_pct + "%";
      document.getElementById("spinPsiOut").textContent = sp.linked_psi;
      document.getElementById("spinoffDescBox").textContent = `${sp.origin_nasa}: ${sp.earth_impact}`;
    } catch (_) {
      apiOnline = false;
      baseOutEl.textContent = "1,901 NPR";
      activeOutEl.textContent = mitigated ? "134 NPR" : "1,901 NPR";
      activeOutEl.style.color = mitigated ? "var(--accent-emerald)" : "var(--accent-crimson)";
      dropOutEl.textContent = mitigated ? "-93.0%" : "0.0%";
      document.getElementById("fmeaSummaryLine").textContent = mitigated
        ? "Barreras de diseño activadas sobre el catálogo de riesgo local."
        : "Sin barreras activas: riesgo acumulado base sin compuerta ni sensores múltiples.";
      document.getElementById("fmeaTableBody").innerHTML = renderFmeaRows(FMEA_OFFLINE_ROWS, mitigated);
      const sp = SPINOFF_OFFLINE[spinoffId];
      document.getElementById("spinWeightOut").textContent = (sp.weight * units).toLocaleString() + " lb";
      document.getElementById("spinRiskOut").textContent = "-" + sp.risk + "%";
      document.getElementById("spinPsiOut").textContent = sp.psi;
      document.getElementById("spinoffDescBox").textContent = `${sp.origin}: ${sp.desc}`;
    }
  }

  // --- MODULO 5 Y 6: REFERENCIAS, MINI MUSEO VIRTUAL & GLOSARIO ---
  function renderOfficialResources() {
    document.getElementById("officialResourcesGrid").innerHTML = OFFICIAL_RESOURCES.map((r) => `
      <div class="resource-item">
        <a href="${escapeHtml(r.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.title)}</a>
        <span class="badge badge-info">${escapeHtml(r.tag)}</span>
      </div>
    `).join("");
  }

  function renderMuseum() {
    const gallery = document.getElementById("museumGallery");
    if (!gallery) return;
    gallery.innerHTML = MUSEUM_EXHIBITS.map((ex) => `
      <article class="museum-exhibit">
        <img class="museum-photo" src="${escapeHtml(ex.img)}" alt="${escapeHtml(ex.title)}" loading="lazy" />
        <div class="museum-head">
          <h3>${escapeHtml(ex.title)}</h3>
          <span class="badge badge-info">${escapeHtml(ex.badge)}</span>
        </div>
        <p class="museum-summary">${escapeHtml(ex.summary)}</p>
        <ul class="museum-facts">
          <li><strong>Atmósfera:</strong> ${escapeHtml(ex.atmosphere)}</li>
          <li><strong>Fenómeno:</strong> ${escapeHtml(ex.phenomenon)}</li>
          <li><strong>Legado:</strong> ${escapeHtml(ex.legacy)}</li>
        </ul>
        <span class="museum-caption">${escapeHtml(ex.caption)}</span>
      </article>
    `).join("");
  }

  function renderGlossary(filterText) {
    const grid = document.getElementById("glossaryGrid");
    if (!grid) return;
    const q = (filterText || "").trim().toLowerCase();
    const items = GLOSSARY_TERMS.filter((item) => {
      if (!q) return true;
      return (
        item.term.toLowerCase().includes(q) ||
        item.tag.toLowerCase().includes(q) ||
        item.def.toLowerCase().includes(q)
      );
    });
    if (!items.length) {
      grid.innerHTML = `<div class="glossary-entry"><p>No hay coincidencias para "${escapeHtml(q)}" en el glosario.</p></div>`;
      return;
    }
    grid.innerHTML = items.map((item) => `
      <article class="glossary-entry">
        <div class="glossary-term">
          <h4>${escapeHtml(item.term)}</h4>
          <span class="badge badge-cool">${escapeHtml(item.tag)}</span>
        </div>
        <p>${escapeHtml(item.def)}</p>
      </article>
    `).join("");
  }

  function wireEvents() {
    document.querySelectorAll('[role="tab"]').forEach((btn) => {
      btn.addEventListener("click", () => switchTab(btn.dataset.tab));
    });

    document.getElementById("runRankingBtn").addEventListener("click", runExplorerAndTopsis);
    ["psiFacilitySelect", "personaSelect", "psiQueryInput"].forEach((id) => {
      document.getElementById(id).addEventListener("change", runExplorerAndTopsis);
    });
    ["wHabSlider", "wModSlider", "wSenSlider"].forEach((id) => {
      const el = document.getElementById(id);
      el.addEventListener("input", scheduleExplorerAndTopsis);
      el.addEventListener("change", runExplorerAndTopsis);
    });

    document.querySelectorAll("[data-forensic]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const p = FORENSIC_PRESETS[btn.dataset.forensic];
        if (!p) return;
        document.getElementById("o2Slider").value = String(p.o2_pct);
        document.getElementById("pressSlider").value = String(p.pressure_psi);
        document.getElementById("flowSlider").value = String(p.flow_cm_s);
        document.getElementById("gravSelect").value = p.gravity_g;
        document.getElementById("matSelect").value = p.material;
        document.getElementById("thickSlider").value = String(p.thickness_mm);
        document.getElementById("dirSelect").value = p.flow_dir;
        document.getElementById("forensicNoteBox").textContent = p.note;
        runFlammabilitySandbox();
      });
    });

    ["o2Slider", "pressSlider", "flowSlider", "thickSlider"].forEach((id) => {
      const el = document.getElementById(id);
      el.addEventListener("input", scheduleFlammabilitySandbox);
      el.addEventListener("change", runFlammabilitySandbox);
    });
    ["gravSelect", "matSelect", "dirSelect"].forEach((id) => {
      document.getElementById(id).addEventListener("change", runFlammabilitySandbox);
    });

    document.getElementById("stepFsmBtn").addEventListener("click", stepDigitalTwin);
    document.getElementById("simCoolFlameBtn").addEventListener("click", () => {
      document.getElementById("twinPresetSelect").value = "cool_flame_ntc";
      document.getElementById("dtSlider").value = "2.5";
      document.getElementById("coSlider").value = "40";
      document.getElementById("aerSlider").value = "28";
      document.getElementById("twinCommSelect").value = "true";
      stepDigitalTwin();
    });
    document.getElementById("simFireBtn").addEventListener("click", () => {
      document.getElementById("twinPresetSelect").value = "open_propagation";
      document.getElementById("dtSlider").value = "22";
      document.getElementById("coSlider").value = "260";
      document.getElementById("aerSlider").value = "72";
      document.getElementById("twinCommSelect").value = "true";
      stepDigitalTwin();
    });
    document.getElementById("simNominalBtn").addEventListener("click", () => {
      document.getElementById("twinPresetSelect").value = "nominal";
      document.getElementById("dtSlider").value = "0.0";
      document.getElementById("coSlider").value = "3";
      document.getElementById("aerSlider").value = "2";
      document.getElementById("twinCommSelect").value = "true";
      stepDigitalTwin();
    });

    ["fmeaMitigatedToggle", "spinoffSelect", "unitsSlider", "suppScenarioSelect"].forEach((id) => {
      const el = document.getElementById(id);
      el.addEventListener("input", updateGovernance);
      el.addEventListener("change", updateGovernance);
    });

    const glossaryInput = document.getElementById("glossarySearchInput");
    if (glossaryInput) {
      glossaryInput.addEventListener("input", () => renderGlossary(glossaryInput.value));
    }

    initPrototypeHardwareAndLightbox();

    document.addEventListener("keydown", (e) => {
      const lightbox = document.getElementById("blueprintLightbox");
      if (lightbox && !lightbox.hidden) {
        if (e.key === "Escape") { closeLightbox(); return; }
        if (e.key === "ArrowLeft") { stepLightbox(-1); return; }
        if (e.key === "ArrowRight") { stepLightbox(1); return; }
      }
      const tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "SELECT") return;
      const map = { "1": "museum", "2": "explorer", "3": "sandbox", "4": "twin", "5": "governance", "6": "blueprint", "7": "models" };
      if (map[e.key]) switchTab(map[e.key]);
    });
  }

  // --- MODULO 6: VISOR LIGHTBOX DE PLANOS, ROTADOR 3D Y EMULADOR DE LOGICA HARDWARE ---
  const BLUEPRINT_SLIDES = [
    {
      category: "Electrónica · Vista 3D",
      categoryClass: "badge badge-ok",
      title: "Modelo 3D de la Tarjeta PCB de Control",
      src: "/assets/hardware/pcb_3d.png",
      downloadHref: "/api/v1/models/download/hw-pcb-3d-png",
      downloadLabel: "Descargar Render 3D (.png)",
      caption: "Vista tridimensional de la placa ensamblada: borneras de sensores (5V/SIG/GND), cuatro salidas de potencia 24 VDC con optoacopladores PC817 y MOSFETs IRLZ44N, reductor XL4015 con inductor toroidal y cabezales para ESP32.",
      is3d: false
    },
    {
      category: "Electrónica · Modelo .STEP",
      categoryClass: "badge badge-cool",
      title: "Visor 3D Interactivo del Archivo .STEP (PCB)",
      src: "",
      downloadHref: "/api/v1/models/download/hw-pcb-step",
      downloadLabel: "Descargar Modelo 3D (.step)",
      caption: "Sección independiente del modelo sólido tridimensional de la tarjeta electrónica de control. Arrastra para rotar 360° o usa la rueda del ratón para acercar los componentes y borneras.",
      is3d: true
    },
    {
      category: "Electrónica · Layout 2D",
      categoryClass: "badge badge-ok",
      title: "Layout de Pistas PCB (Centrado y Escala Real)",
      src: "/assets/hardware/pcb_layout.png",
      downloadHref: "/api/v1/models/download/hw-pcb-layout-png",
      downloadLabel: "Descargar Layout (.png)",
      caption: "Distribución de cobre, serigrafía y separación física entre la zona lógica de 5V/3.3V (izquierda), el regulador XL4015 con fusibles FU1/FU2 (arriba) y los cuatro canales aislados de potencia 24 VDC (derecha).",
      is3d: false
    },
    {
      category: "Electrónica · Esquemático",
      categoryClass: "badge badge-ok",
      title: "Esquema Electrónico Completo (ESP32 + XL4015 + PC817)",
      src: "/assets/hardware/esquema_control.png",
      downloadHref: "/api/v1/models/download/hw-esquema-pdf",
      downloadLabel: "Descargar Esquema (.pdf)",
      caption: "Circuito completo: fuente reductora 24V→5.1V/5A con protección crowbar 1N5339B+BT151, divisores 330 Ω/470 Ω en SP0..SP3, amplificador LMV358M para ventilador, 4 indicadores 2N7000 y 4 optoacopladores PC817 con diodos volante 1N5822.",
      is3d: false
    },
    {
      category: "Mecánica · SolidWorks",
      categoryClass: "badge badge-info",
      title: "Plano Mecánico SolidWorks · Ducto 250 × 250 × 600 mm",
      src: "/assets/hardware/plano_ducto_solidworks.svg",
      downloadHref: "/api/v1/models/download/hw-ducto-solidworks",
      downloadLabel: "Descargar Plano CAD (.svg)",
      caption: "Sección longitudinal acotada del ducto en aluminio 6061-T6: ventilador con panal laminar, mirilla de cuarzo Ø 60 mm para cámara superior, puerto de sensores, compuerta spring-return y boquilla atomizadora PFE a 30°.",
      is3d: false
    }
  ];

  const PROTO_EMULATOR_MODES = {
    normal: {
      badgeText: "Estado: NORMAL",
      badgeClass: "badge badge-ok",
      power: "24.0 V → 5.10 V (FU1 2A / FU2 5A OK)",
      sensor: "SP0..SP3: 0.35 V – 0.92 V → ESP32 ADC1 (Nominal)",
      fanPwm: "GPIO 22 (3.3 V · 40% PWM) → LMV358M 5.0 V · Flujo 20 cm/s",
      outputs: [
        { name: "J12 Ventilador", state: "ACTIVO", cls: "badge badge-ok" },
        { name: "J13 Compuerta", state: "ABIERTA (24V)", cls: "badge badge-info" },
        { name: "J14 Niebla PFE", state: "ESPERA", cls: "badge badge-cool" },
        { name: "J15 Reserva", state: "LIBRE", cls: "badge badge-cool" }
      ],
      leds: { green: true, yellow: false, white: true, red: false },
      summary: "Flujo laminar estable; el ESP32 lee los 4 divisores 330 Ω / 470 Ω cada 100 ms y mantiene el LED verde y blanco activos."
    },
    prealert: {
      badgeText: "Estado: PRE_ALERTA",
      badgeClass: "badge badge-warn",
      power: "24.0 V → 5.10 V (Consumo estable < 1.2 A)",
      sensor: "SP1 (CO) / SP2 (<0.1 um): 1.65 V – 2.15 V → Umbral preventivo",
      fanPwm: "GPIO 22 (3.3 V · 55% PWM) → LMV358M 5.0 V · Vigilancia activa",
      outputs: [
        { name: "J12 Ventilador", state: "VIGILANCIA", cls: "badge badge-warn" },
        { name: "J13 Compuerta", state: "ABIERTA (24V)", cls: "badge badge-info" },
        { name: "J14 Niebla PFE", state: "PRE-ARMADO", cls: "badge badge-warn" },
        { name: "J15 Reserva", state: "LIBRE", cls: "badge badge-cool" }
      ],
      leds: { green: false, yellow: true, white: true, red: false },
      summary: "Detección temprana de pirólisis o humo submicrónico (<0.1 um): el transistor Q1 (2N7000) enciende el piloto ámbar sin detener aún el ducto."
    },
    containment: {
      badgeText: "Estado: CONTENCION (PFE ACTIVO)",
      badgeClass: "badge badge-danger",
      power: "24.0 V → 5.10 V (Diodos 1N5822 absorben retorno inductivo)",
      sensor: "SP0 (dT/dt) / SP1 (CO): 2.40 V – 2.88 V → Disparo confirmado",
      fanPwm: "GPIO 22 (0% PWM · 0.0 V) → Ventilador detenido",
      outputs: [
        { name: "J12 Ventilador", state: "CORTE (0V)", cls: "badge badge-danger" },
        { name: "J13 Compuerta", state: "CERRADA (RESORTE)", cls: "badge badge-danger" },
        { name: "J14 Niebla PFE", state: "DISPARO ON (24V)", cls: "badge badge-ok" },
        { name: "J15 Reserva", state: "BALIZA AUX", cls: "badge badge-warn" }
      ],
      leds: { green: false, yellow: false, white: true, red: true },
      summary: "Canal 0 (Q2) corta ventilador, Canal 1 (Q6) desenergiza compuerta para cierre por resorte y Canal 2 (Q7) dispara la niebla fina PFE con LED rojo activo."
    },
    failsafe: {
      badgeText: "Estado: FALLA_SEGURA / PROTECCION",
      badgeClass: "badge badge-danger",
      power: "Crowbar 1N5339B + BT151 vigila sobretensión >5.6 V; FU1/FU2 listos",
      sensor: "Enlace perdido o lectura fuera de rango (<0.1 V / >2.94 V)",
      fanPwm: "GPIO 22 bloqueado a 0 V · Sin excitación de flujo",
      outputs: [
        { name: "J12 Ventilador", state: "BLOQUEADO OFF", cls: "badge badge-danger" },
        { name: "J13 Compuerta", state: "CERRADA SEGURA", cls: "badge badge-danger" },
        { name: "J14 Niebla PFE", state: "INHIBIDO", cls: "badge badge-cool" },
        { name: "J15 Reserva", state: "ALARMA FALLA", cls: "badge badge-danger" }
      ],
      leds: { green: false, yellow: true, white: false, red: true },
      summary: "Ante pérdida de comunicación o falla eléctrica, el módulo desenergiza ventilador y compuerta manteniendo el ducto físicamente aislado sin disparar agente innecesario."
    }
  };

  let activeLightboxIdx = 0;
  let pcb3dController = null;

  function renderLightboxSlide(idx) {
    const safeIdx = ((idx % BLUEPRINT_SLIDES.length) + BLUEPRINT_SLIDES.length) % BLUEPRINT_SLIDES.length;
    activeLightboxIdx = safeIdx;
    const slide = BLUEPRINT_SLIDES[safeIdx];

    const imgEl = document.getElementById("lightboxImg");
    const titleEl = document.getElementById("lightboxTitle");
    const counterEl = document.getElementById("lightboxCounter");
    const catBadgeEl = document.getElementById("lightboxCategoryBadge");
    const captionEl = document.getElementById("lightboxCaption");
    const dlEl = document.getElementById("lightboxDownloadLink");
    const wrap3d = document.getElementById("lightbox3dWrap");

    if (!imgEl || !titleEl) return;
    titleEl.textContent = slide.title;
    counterEl.textContent = `${safeIdx + 1} / ${BLUEPRINT_SLIDES.length}`;
    if (catBadgeEl) {
      catBadgeEl.textContent = slide.category;
      catBadgeEl.className = slide.categoryClass;
    }
    captionEl.textContent = slide.caption;
    dlEl.href = slide.downloadHref;
    dlEl.textContent = slide.downloadLabel;

    if (slide.is3d) {
      imgEl.hidden = true;
      imgEl.removeAttribute("src");
      wrap3d.hidden = false;
      if (pcb3dController) pcb3dController.activate();
    } else {
      wrap3d.hidden = true;
      if (pcb3dController) pcb3dController.deactivate();
      imgEl.src = slide.src;
      imgEl.alt = slide.title;
      imgEl.hidden = false;
    }

    document.querySelectorAll(".lightbox-thumb-btn").forEach((btn, i) => {
      btn.classList.toggle("is-active", i === safeIdx);
    });
  }

  function openLightbox(idx) {
    const modal = document.getElementById("blueprintLightbox");
    if (!modal) return;
    renderLightboxSlide(idx);
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    const closeBtn = document.getElementById("lightboxCloseBtn");
    if (closeBtn) closeBtn.focus();
  }

  function closeLightbox() {
    const modal = document.getElementById("blueprintLightbox");
    if (!modal) return;
    modal.hidden = true;
    document.body.style.overflow = "";
    if (pcb3dController) pcb3dController.deactivate();
  }

  function stepLightbox(delta) {
    renderLightboxSlide(activeLightboxIdx + delta);
  }

  function initPcb3dViewer() {
    const canvas = document.getElementById("pcb3dCanvas");
    if (!canvas || !canvas.getContext) return null;
    const ctx = canvas.getContext("2d");

    let yaw = -0.58;
    let pitch = 0.56;
    let zoom = 1.0;
    let dragging = false;
    let lastX = 0;
    let lastY = 0;
    let stlTriangles = null;
    let stlLoading = false;
    let isActive = false;

    // Modelo parametrico fiel a la PCB real (usado al instante y mientras/si carga malla STL)
    function buildPcbParts() {
      const parts = [];
      const addBox = (cx, cy, cz, sx, sy, sz, color) => {
        const hx = sx / 2, hy = sy / 2, hz = sz / 2;
        const v = [
          [cx - hx, cy - hy, cz - hz], [cx + hx, cy - hy, cz - hz],
          [cx + hx, cy + hy, cz - hz], [cx - hx, cy + hy, cz - hz],
          [cx - hx, cy - hy, cz + hz], [cx + hx, cy - hy, cz + hz],
          [cx + hx, cy + hy, cz + hz], [cx - hx, cy + hy, cz + hz]
        ];
        const faces = [
          [4, 5, 6, 7], [0, 3, 2, 1], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 4, 7, 3]
        ];
        faces.forEach((f) => parts.push({ pts: f.map((i) => v[i]), color }));
      };
      // Placa FR4 verde principal (140 x 110 x 2.2 mm escalado)
      addBox(0, 0, 0, 120, 96, 2.5, "#2E6F24");
      // Headers ESP32 (J2/J3) y bloque reserva izquierda
      addBox(-36, 22, 5.5, 4, 34, 8.5, "#1E293B");
      addBox(-18, 22, 5.5, 4, 34, 8.5, "#1E293B");
      addBox(-52, 18, 4.2, 4, 30, 5.5, "#0F172A");
      // Borneras de sensores (izquierda + abajo-izq)
      for (let i = 0; i < 3; i++) addBox(-52, -16 - i * 11, 5.8, 9, 9.5, 9, "#15803D");
      addBox(-40, -42, 5.8, 13, 9.5, 9, "#15803D");
      addBox(-24, -42, 5.8, 13, 9.5, 9, "#15803D");
      // 4 borneras indicadoras de estado (abajo centro) + 2N7000
      for (let i = 0; i < 4; i++) {
        addBox(-8 + i * 11, -42, 5.8, 9.5, 9.5, 9, "#15803D");
        addBox(-8 + i * 11, -31, 4.5, 4.5, 4, 6, "#1E293B");
      }
      // 4 etapas de potencia PC817 + IRLZ44N + borneras J12..J15 (derecha)
      for (let i = 0; i < 4; i++) {
        const y = 20 - i * 17;
        addBox(24, y, 3.6, 6.5, 6.5, 4.5, "#1E293B");
        addBox(36, y, 7.5, 5, 9.5, 12, "#334155");
        addBox(52, y, 5.8, 9.5, 9.5, 9, "#15803D");
      }
      // Etapa reductor XL4015 + toroide + portafusibles (arriba)
      addBox(8, 38, 8.0, 14, 6, 13, "#22C55E");
      addBox(-8, 37, 6.5, 16, 8, 10, "#1E293B");
      addBox(28, 37, 6.5, 16, 8, 10, "#1E293B");
      addBox(-16, 42, 5.8, 9, 8.5, 9, "#15803D");
      addBox(44, 42, 5.8, 9, 8.5, 9, "#15803D");
      // LMV358M etapa ventilador
      addBox(-34, -14, 3.0, 6, 6, 3.2, "#1E293B");
      return parts;
    }
    const fallbackFaces = buildPcbParts();

    function parseBinaryStl(buffer) {
      if (!buffer || buffer.byteLength < 84) return null;
      const view = new DataView(buffer);
      const count = view.getUint32(80, true);
      if (count === 0 || 84 + count * 50 > buffer.byteLength) return null;
      const step = Math.max(1, Math.floor(count / 8500));
      const tris = [];
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity, minZ = Infinity, maxZ = -Infinity;
      for (let i = 0; i < count; i += step) {
        const off = 84 + i * 50;
        const p = [];
        for (let k = 0; k < 3; k++) {
          const x = view.getFloat32(off + 12 + k * 12, true);
          const y = view.getFloat32(off + 16 + k * 12, true);
          const z = view.getFloat32(off + 20 + k * 12, true);
          if (x < minX) minX = x; if (x > maxX) maxX = x;
          if (y < minY) minY = y; if (y > maxY) maxY = y;
          if (z < minZ) minZ = z; if (z > maxZ) maxZ = z;
          p.push([x, y, z]);
        }
        const attr = view.getUint16(off + 48, true);
        let color = "#2E6F24";
        if (attr & 0x8000) {
          const r = Math.round(((attr >> 10) & 0x1F) * 255 / 31);
          const g = Math.round(((attr >> 5) & 0x1F) * 255 / 31);
          const b = Math.round((attr & 0x1F) * 255 / 31);
          color = "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");
        }
        tris.push({ p, color });
      }
      const cx = (minX + maxX) / 2, cy = (minY + maxY) / 2, cz = (minZ + maxZ) / 2;
      const span = Math.max(maxX - minX, maxY - minY, maxZ - minZ, 1e-3);
      const scale = 120 / span;
      return tris.map((t) => ({
        pts: t.p.map((v) => [(v[0] - cx) * scale, (v[1] - cy) * scale, (v[2] - cz) * scale]),
        color: t.color
      }));
    }

    function maybeLoadStl() {
      if (stlTriangles || stlLoading) return;
      stlLoading = true;
      fetch("/assets/hardware/pcb_3d_preview.stl")
        .then((res) => (res.ok ? res.arrayBuffer() : null))
        .then((buf) => {
          if (buf) {
            const parsed = parseBinaryStl(buf);
            if (parsed && parsed.length) stlTriangles = parsed;
          }
          render();
        })
        .catch(() => {});
    }

    function shadeColor(hex, factor) {
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      const f = Math.max(0.35, Math.min(1.18, factor));
      return `rgb(${Math.min(255, Math.round(r * f))}, ${Math.min(255, Math.round(g * f))}, ${Math.min(255, Math.round(b * f))})`;
    }

    function render() {
      if (!isActive) return;
      const w = canvas.width, h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = "#EDF2FA";
      ctx.fillRect(0, 0, w, h);

      const cosY = Math.cos(yaw), sinY = Math.sin(yaw);
      const cosP = Math.cos(pitch), sinP = Math.sin(pitch);
      const faces = stlTriangles || fallbackFaces;
      const projected = [];

      for (let i = 0; i < faces.length; i++) {
        const f = faces[i];
        const tPts = f.pts.map(([x, y, z]) => {
          const x1 = x * cosY - y * sinY;
          const y1 = x * sinY + y * cosY;
          const y2 = y1 * cosP - z * sinP;
          const z2 = y1 * sinP + z * cosP;
          return [x1, y2, z2];
        });
        const ax = tPts[1][0] - tPts[0][0], ay = tPts[1][1] - tPts[0][1], az = tPts[1][2] - tPts[0][2];
        const bx = tPts[2][0] - tPts[0][0], by = tPts[2][1] - tPts[0][1], bz = tPts[2][2] - tPts[0][2];
        const nx = ay * bz - az * by, ny = az * bx - ax * bz, nz = ax * by - ay * bx;
        const nLen = Math.hypot(nx, ny, nz) || 1;
        const light = 0.52 + 0.55 * Math.abs((nx * 0.3 + ny * 0.4 + nz * 0.86) / nLen);
        const depth = tPts.reduce((acc, p) => acc + p[2], 0) / tPts.length;
        const persp = 4.2 * zoom;
        const screen = tPts.map(([px, py, pz]) => {
          const k = persp / (1 + (420 - pz) * 0.0012);
          return [w / 2 + px * k, h / 2 - py * k * 0.92];
        });
        projected.push({ screen, depth, fill: shadeColor(f.color, light) });
      }

      projected.sort((a, b) => a.depth - b.depth);
      for (let i = 0; i < projected.length; i++) {
        const item = projected[i];
        ctx.beginPath();
        ctx.moveTo(item.screen[0][0], item.screen[0][1]);
        for (let k = 1; k < item.screen.length; k++) ctx.lineTo(item.screen[k][0], item.screen[k][1]);
        ctx.closePath();
        ctx.fillStyle = item.fill;
        ctx.fill();
        ctx.strokeStyle = stlTriangles ? item.fill : "rgba(10, 25, 49, 0.16)";
        ctx.lineWidth = stlTriangles ? 0.55 : 0.7;
        ctx.stroke();
      }
    }

    canvas.addEventListener("pointerdown", (e) => {
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!dragging) return;
      yaw += (e.clientX - lastX) * 0.012;
      pitch = Math.max(-1.35, Math.min(1.35, pitch + (e.clientY - lastY) * 0.012));
      lastX = e.clientX;
      lastY = e.clientY;
      render();
    });
    canvas.addEventListener("pointerup", () => { dragging = false; });
    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      zoom = Math.max(0.55, Math.min(2.1, zoom + (e.deltaY < 0 ? 0.1 : -0.1)));
      render();
    }, { passive: false });

    return {
      activate() {
        isActive = true;
        maybeLoadStl();
        render();
      },
      deactivate() { isActive = false; }
    };
  }

  function setProtoMode(modeKey) {
    const cfg = PROTO_EMULATOR_MODES[modeKey] || PROTO_EMULATOR_MODES.normal;
    const badge = document.getElementById("protoStageBadge");
    if (!badge) return;
    badge.textContent = cfg.badgeText;
    badge.className = cfg.badgeClass;
    document.getElementById("protoPowerOut").textContent = cfg.power;
    document.getElementById("protoSensorOut").textContent = cfg.sensor;
    document.getElementById("protoFanPwmOut").textContent = cfg.fanPwm;
    document.getElementById("protoSummaryText").textContent = cfg.summary;

    document.getElementById("protoOutputsList").innerHTML = cfg.outputs.map((o) =>
      `<li><strong>${escapeHtml(o.name)}:</strong> <span class="${escapeHtml(o.cls)}">${escapeHtml(o.state)}</span></li>`
    ).join("");

    document.querySelectorAll("#protoLedsRow .proto-led").forEach((el) => {
      const key = el.dataset.led;
      el.classList.toggle("is-on", Boolean(cfg.leds[key]));
    });
    document.querySelectorAll(".proto-sim-btn").forEach((btn) => {
      btn.classList.toggle("is-selected", btn.dataset.protoMode === modeKey);
    });
  }

  function initPrototypeHardwareAndLightbox() {
    pcb3dController = initPcb3dViewer();

    const thumbsEl = document.getElementById("lightboxThumbs");
    if (thumbsEl) {
      thumbsEl.innerHTML = BLUEPRINT_SLIDES.map((s, i) => `
        <button type="button" class="btn btn-sm lightbox-thumb-btn" data-thumb-idx="${i}">${escapeHtml(s.category.split("·")[1].trim())}</button>
      `).join("");
      thumbsEl.querySelectorAll("[data-thumb-idx]").forEach((btn) => {
        btn.addEventListener("click", () => {
          renderLightboxSlide(Number(btn.dataset.thumbIdx));
        });
      });
    }

    document.querySelectorAll("[data-lightbox-index]").forEach((el) => {
      el.addEventListener("click", () => openLightbox(Number(el.dataset.lightboxIndex)));
    });

    const closeBtn = document.getElementById("lightboxCloseBtn");
    const prevBtn = document.getElementById("lightboxPrevBtn");
    const nextBtn = document.getElementById("lightboxNextBtn");
    const backdrop = document.getElementById("blueprintLightbox");

    if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
    if (prevBtn) prevBtn.addEventListener("click", () => stepLightbox(-1));
    if (nextBtn) nextBtn.addEventListener("click", () => stepLightbox(1));
    if (backdrop) {
      backdrop.addEventListener("click", (e) => {
        if (e.target === backdrop) closeLightbox();
      });
    }

    document.querySelectorAll(".proto-sim-btn").forEach((btn) => {
      btn.addEventListener("click", () => setProtoMode(btn.dataset.protoMode));
    });
    setProtoMode("normal");
  }

  // --- FONDO ORBITAL MULTI-TRAYECTORIA EN BUCLE SOBRE TEMA CLARO ---
  function initOrbitalBackdrop() {
    const canvas = document.getElementById("orbitalBackdropCanvas");
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext("2d");
    const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let width = 0;
    let height = 0;
    let dpr = 1;
    let phase = 0;
    let rafId = null;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function drawOrbitAndCraft(cx, cy, rx, ry, rot, dash, strokeColor, craftColor, angle, label, withTail) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rot);

      ctx.setLineDash(dash);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.3;
      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
      ctx.stroke();

      if (withTail) {
        ctx.setLineDash([]);
        ctx.strokeStyle = craftColor;
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.ellipse(0, 0, rx, ry, 0, angle - 0.32, angle);
        ctx.stroke();
      }

      const sx = Math.cos(angle) * rx;
      const sy = Math.sin(angle) * ry;
      ctx.setLineDash([]);
      ctx.fillStyle = craftColor;
      ctx.beginPath();
      ctx.arc(sx, sy, 4.1, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.arc(sx, sy, 9.5, 0, Math.PI * 2);
      ctx.stroke();

      if (label && width >= 720) {
        ctx.rotate(-rot);
        const gx = sx * Math.cos(rot) - sy * Math.sin(rot);
        const gy = sx * Math.sin(rot) + sy * Math.cos(rot);
        ctx.font = "10px monospace";
        ctx.fillStyle = craftColor;
        ctx.fillText(label, gx + 12, gy + 3);
      }
      ctx.restore();
    }

    function drawFrame(t) {
      ctx.clearRect(0, 0, width, height);

      // Reticulas fiduciales tipo camara Apollo (Reseau)
      ctx.strokeStyle = "rgba(11, 61, 145, 0.13)";
      ctx.lineWidth = 1;
      const step = width < 680 ? 130 : 185;
      for (let x = 64; x < width - 32; x += step) {
        for (let y = 64; y < height - 32; y += step) {
          ctx.beginPath();
          ctx.moveTo(x - 5, y);
          ctx.lineTo(x + 5, y);
          ctx.moveTo(x, y - 5);
          ctx.lineTo(x, y + 5);
          ctx.stroke();
        }
      }

      const cx = width * 0.5;
      const cy = height * 0.47;
      const baseRx = Math.max(210, width * 0.45);
      const baseRy = Math.max(125, height * 0.27);

      // Anillo graduado central estilo telemetria espacial
      const ringR = Math.min(width, height) * 0.34;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.strokeStyle = "rgba(11, 61, 145, 0.08)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(0, 0, ringR, 0, Math.PI * 2);
      ctx.stroke();
      for (let deg = 0; deg < 360; deg += 30) {
        const rad = (deg * Math.PI) / 180 + t * 0.04;
        ctx.beginPath();
        ctx.moveTo(Math.cos(rad) * (ringR - 5), Math.sin(rad) * (ringR - 5));
        ctx.lineTo(Math.cos(rad) * (ringR + 5), Math.sin(rad) * (ringR + 5));
        ctx.stroke();
      }
      ctx.restore();

      // 6 orbitas con distintas inclinaciones, radios y naves animadas
      drawOrbitAndCraft(
        cx, cy, baseRx * 1.04, baseRy * 1.04, -0.22, [7, 6],
        "rgba(11, 61, 145, 0.17)", "rgba(11, 61, 145, 0.52)", t * 0.36,
        "ISS-0G // LEO 408 KM", true
      );
      drawOrbitAndCraft(
        cx, cy, baseRx * 0.82, baseRy * 0.90, 0.34, [4, 8],
        "rgba(200, 40, 18, 0.14)", "rgba(200, 40, 18, 0.48)", -t * 0.27 + 1.9,
        "CYGNUS // SAFFIRE", true
      );
      drawOrbitAndCraft(
        cx, cy, baseRx * 1.18, baseRy * 1.32, 0.12, [10, 8],
        "rgba(6, 95, 70, 0.13)", "rgba(6, 95, 70, 0.45)", t * 0.19 + 4.1,
        "ARTEMIS // TRANSITO LUNAR", true
      );
      drawOrbitAndCraft(
        cx, cy, baseRx * 0.62, baseRy * 1.24, -0.68, [3, 6],
        "rgba(65, 86, 120, 0.14)", "rgba(65, 86, 120, 0.44)", t * 0.44 + 0.7,
        "", false
      );
      drawOrbitAndCraft(
        width * 0.22, height * 0.26, Math.max(115, width * 0.16), Math.max(58, height * 0.11), 0.46, [5, 5],
        "rgba(120, 53, 15, 0.12)", "rgba(120, 53, 15, 0.42)", -t * 0.52 + 2.6,
        "", false
      );
      drawOrbitAndCraft(
        width * 0.80, height * 0.74, Math.max(125, width * 0.17), Math.max(62, height * 0.12), -0.35, [6, 5],
        "rgba(11, 61, 145, 0.13)", "rgba(200, 40, 18, 0.42)", t * 0.48 + 3.4,
        "", false
      );
    }

    function tick() {
      if (!document.hidden) {
        phase += 0.008;
        drawFrame(phase);
      }
      rafId = window.requestAnimationFrame(tick);
    }

    resize();
    window.addEventListener("resize", () => {
      resize();
      if (reducedMotion) drawFrame(0.6);
    });

    if (reducedMotion) {
      drawFrame(0.6);
    } else {
      rafId = window.requestAnimationFrame(tick);
    }
    return () => {
      if (rafId) window.cancelAnimationFrame(rafId);
    };
  }

  initOrbitalBackdrop();
  wireEvents();
  renderOfficialResources();
  renderMuseum();
  renderGlossary("");
  runExplorerAndTopsis();
  runFlammabilitySandbox();
  stepDigitalTwin();
  updateGovernance();
})();
