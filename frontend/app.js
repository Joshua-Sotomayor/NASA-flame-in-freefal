(function () {
  "use strict";

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
    const minX = Math.min(...xs), spanX = Math.max(0.05, Math.max(...xs) - minX);
    const minY = Math.min(...ys), spanY = Math.max(0.05, Math.max(...ys) - minY);

    const coords = points.map((pt, idx) => {
      const baseNx = 56 + ((pt.x - minX) / spanX) * 336;
      const baseNy = 194 - ((pt.y - minY) / spanY) * 158;
      return { pt, idx, nx: baseNx, ny: baseNy, isTop: pt.psi_id === topPsiId };
    });

    // Separacion deterministica leve si dos puntos caen casi encima
    for (let i = 0; i < coords.length; i += 1) {
      for (let j = i + 1; j < coords.length; j += 1) {
        const dx = coords[j].nx - coords[i].nx;
        const dy = coords[j].ny - coords[i].ny;
        const d = Math.hypot(dx, dy);
        if (d < 8) {
          const ang = (j * 2.1) % (Math.PI * 2);
          coords[j].nx = clamp(coords[j].nx + Math.cos(ang) * 7.5, 42, 412);
          coords[j].ny = clamp(coords[j].ny + Math.sin(ang) * 7.5, 28, 200);
        }
      }
    }

    const order = [...coords].sort((a, b) => (a.isTop === b.isTop ? a.ny - b.ny : a.isTop ? -1 : 1));
    const placedBoxes = [];
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
      const w = Math.max(28, label.length * 5.15 + 6);
      const h = 11.5;
      let best = null;
      for (const [oxRaw, oy] of offsets) {
        const ox = oxRaw === -1 ? -w - 9 : oxRaw;
        const tx = clamp(item.nx + ox, 30, 448 - w);
        const ty = clamp(item.ny + oy, 25, 206);
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
      return { ...item, label, w, h, tx: best.tx, ty: best.ty, box: best.box };
    });

    const leaders = placed.map((p) => {
      const ax = clamp(p.nx, p.box.x1, p.box.x2);
      const ay = clamp(p.ny, p.box.y1, p.box.y2);
      if (Math.hypot(ax - p.nx, ay - p.ny) <= 10.5) return "";
      return `<line x1="${p.nx.toFixed(1)}" y1="${p.ny.toFixed(1)}" x2="${ax.toFixed(1)}" y2="${ay.toFixed(1)}" stroke="#7E97B8" stroke-width="0.9" stroke-dasharray="2 1.5" />`;
    }).join("");

    const dots = placed.map((p) => {
      const fill = colors[p.pt.cluster_id % colors.length];
      const halo = p.isTop ? `<circle cx="${p.nx.toFixed(1)}" cy="${p.ny.toFixed(1)}" r="9.5" fill="none" stroke="#C82812" stroke-width="2" />` : "";
      return `<g>${halo}<circle cx="${p.nx.toFixed(1)}" cy="${p.ny.toFixed(1)}" r="5.3" fill="${fill}" stroke="#FFFFFF" stroke-width="1.2" opacity="0.96" /><title>${escapeHtml(p.pt.psi_id + " · " + p.label)}</title></g>`;
    }).join("");

    const labels = placed.map((p) => {
      const ink = p.isTop ? "#0B3D91" : "#1E2E4A";
      const weight = p.isTop ? "700" : "500";
      return `<g><rect x="${(p.tx - 1.5).toFixed(1)}" y="${(p.ty - 8.5).toFixed(1)}" width="${p.w.toFixed(1)}" height="11" rx="2" fill="rgba(255,255,255,0.88)" /><text x="${p.tx.toFixed(1)}" y="${p.ty.toFixed(1)}" fill="${ink}" font-size="8.3" font-weight="${weight}" font-family="monospace">${escapeHtml(p.label)}</text></g>`;
    }).join("");

    svg.innerHTML = `<rect x="24" y="14" width="432" height="198" rx="2" fill="#FFFFFF" stroke="#C5D3E8" /><line x1="24" y1="113" x2="456" y2="113" stroke="#DCE6F5" stroke-dasharray="4 3" /><line x1="240" y1="14" x2="240" y2="212" stroke="#DCE6F5" stroke-dasharray="4 3" />${leaders}${dots}${labels}`;
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
    document.getElementById("psiRankBody").innerHTML = ranked.slice(0, 12).map((r) => `
      <tr>
        <td class="mono"><strong>#${r.rank}</strong></td>
        <td><strong>${escapeHtml(r.psi_id)}</strong> · ${escapeHtml(r.acronym)}</td>
        <td><span class="badge badge-info">${escapeHtml(r.facility)}</span></td>
        <td class="mono tabular">${Number(r.topsis_score).toFixed(3)}</td>
        <td class="mono">${escapeHtml(r.doi)}</td>
      </tr>
    `).join("");
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

      document.getElementById("fmeaTableBody").innerHTML = data.fmea_rows.map((r) => `
        <tr>
          <td class="mono"><strong>${escapeHtml(r.mode_id)}</strong></td>
          <td><strong>${escapeHtml(humanizeFmeaText(r.subsystem))}</strong><br /><span>${escapeHtml(humanizeFmeaText(r.failure_mode))}</span></td>
          <td class="mono tabular"><strong>${r.active_npr}</strong> <small>(base ${r.baseline_npr})</small></td>
          <td>${escapeHtml(humanizeFmeaText(r.mitigation))}</td>
          <td class="mono">${escapeHtml(r.linked_psi)}</td>
        </tr>
      `).join("");
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

    document.addEventListener("keydown", (e) => {
      const tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "SELECT") return;
      const map = { "1": "museum", "2": "explorer", "3": "sandbox", "4": "twin", "5": "governance", "6": "blueprint" };
      if (map[e.key]) switchTab(map[e.key]);
    });
  }

  wireEvents();
  renderOfficialResources();
  renderMuseum();
  renderGlossary("");
  runExplorerAndTopsis();
  runFlammabilitySandbox();
  stepDigitalTwin();
  updateGovernance();
})();
