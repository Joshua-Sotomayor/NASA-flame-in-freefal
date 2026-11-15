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

  function escapeHtml(raw) {
    return String(raw)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function setRuntimeBadge(online) {
    apiOnline = online;
    const badge = document.getElementById("runtimeModeBadge");
    badge.textContent = online ? "Simulador Activo" : "Catálogo Local Autónomo";
    badge.className = "badge " + (online ? "badge-ok" : "badge-warn");
  }

  async function apiJson(url, options) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error("HTTP " + res.status);
    setRuntimeBadge(true);
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

  // --- MODULO 1: EXPLORADOR & MAPA DE SIMILITUD ---
  function renderClustersSvg(points) {
    const svg = document.getElementById("clustersSvg");
    const colors = ["#0B3B66", "#065F46", "#B43E18", "#6D28D9"];
    if (!points.length) {
      svg.innerHTML = "";
      return;
    }
    const xs = points.map((p) => p.x);
    const ys = points.map((p) => p.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs) || 1;
    const minY = Math.min(...ys), maxY = Math.max(...ys) || 1;

    const circles = points.map((pt) => {
      const nx = 45 + ((pt.x - minX) / Math.max(0.01, maxX - minX)) * 380;
      const ny = 195 - ((pt.y - minY) / Math.max(0.01, maxY - minY)) * 155;
      const fill = colors[pt.cluster_id % colors.length];
      return `<g><circle cx="${nx.toFixed(1)}" cy="${ny.toFixed(1)}" r="5.5" fill="${fill}" opacity="0.92" /><text x="${(nx + 8).toFixed(1)}" y="${(ny + 3).toFixed(1)}" fill="#18181B" font-size="8.5" font-family="monospace">${escapeHtml(pt.acronym)}</text></g>`;
    }).join("");

    svg.innerHTML = `<rect x="25" y="15" width="430" height="195" rx="2" fill="#FFFFFF" stroke="#94A3B8" /><line x1="25" y1="112" x2="455" y2="112" stroke="#E2E8F0" stroke-dasharray="4 3" /><line x1="240" y1="15" x2="240" y2="210" stroke="#E2E8F0" stroke-dasharray="4 3" />${circles}`;
  }

  async function runExplorerAndTopsis() {
    const wHab = Number(document.getElementById("wHabSlider").value);
    const wMod = Number(document.getElementById("wModSlider").value);
    const wSen = Number(document.getElementById("wSenSlider").value);
    document.getElementById("wHabVal").textContent = String(wHab);
    document.getElementById("wModVal").textContent = String(wMod);
    document.getElementById("wSenVal").textContent = String(wSen);

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
      renderExplorerOutput(filtered, data.clusters_2d, data.synthesis);
    } catch (_) {
      setRuntimeBadge(false);
      const total = Math.max(1, wHab + wMod + wSen);
      const scored = OFFLINE_PSI
        .filter((d) => !facility || d.facility === facility)
        .map((d, idx) => {
          const score = (
            d.criteria_scores.habitat * wHab +
            d.criteria_scores.modeling * wMod +
            ((d.criteria_scores.sensors + d.criteria_scores.spinoff) * 0.5) * wSen
          ) / total;
          return { ...d, rank: idx + 1, topsis_score: score };
        })
        .sort((a, b) => b.topsis_score - a.topsis_score)
        .map((d, i) => ({ ...d, rank: i + 1 }));

      const pts = scored.map((d, i) => ({
        psi_id: d.psi_id,
        acronym: d.acronym,
        x: Math.cos(i * 0.7) * 0.4,
        y: Math.sin(i * 0.9) * 0.35,
        cluster_id: i % 4
      }));
      const top = scored[0] || OFFLINE_PSI[0];
      renderExplorerOutput(scored, pts, {
        persona,
        bullets: [
          `${top.psi_id} (${top.acronym}, ${top.facility}) encabeza la prioridad según tus criterios (${top.doi}).`,
          `${top.earth_benefits}`,
          `Síntesis generada a partir del catálogo científico local validado.`
        ],
        cited_dois: [top.doi]
      });
    }
  }

  function renderExplorerOutput(ranked, clusters, synthesis) {
    document.getElementById("synthesisPersonaBadge").textContent = "Síntesis de Evidencia · " + synthesis.persona;
    document.getElementById("citedDoisLine").textContent = synthesis.cited_dois.join(" · ");
    document.getElementById("synthesisBullets").innerHTML = synthesis.bullets
      .map((b) => `<li>${escapeHtml(b)}</li>`)
      .join("");
    renderClustersSvg(clusters);
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

  // --- MODULO 2: INFLAMABILIDAD EN CABINA ---
  function renderFlammabilityContour(currentO2, currentFlow) {
    const svg = document.getElementById("flammabilityContourSvg");
    const oxToX = (o2) => 48 + ((Math.min(60, Math.max(14, o2)) - 14) / 46) * 405;
    const flToY = (fl) => 240 - (Math.min(60, Math.max(0, fl)) / 60) * 205;

    const px = oxToX(currentO2);
    const py = flToY(currentFlow);

    svg.innerHTML = `
      <rect x="48" y="35" width="405" height="205" fill="#FFFFFF" stroke="#94A3B8" />
      <line x1="48" y1="138" x2="453" y2="138" stroke="#E2E8F0" stroke-dasharray="4 3" />
      <line x1="250" y1="35" x2="250" y2="240" stroke="#E2E8F0" stroke-dasharray="4 3" />
      <rect x="48" y="218" width="140" height="22" fill="rgba(6, 95, 70, 0.14)" />
      <text x="118" y="232" text-anchor="middle" fill="#065F46" font-size="9" font-weight="bold" font-family="monospace">Extinción Radiativa</text>
      <polygon points="48,35 190,35 160,115 48,115" fill="rgba(11, 59, 102, 0.12)" />
      <text x="108" y="68" text-anchor="middle" fill="#0B3B66" font-size="9" font-weight="bold" font-family="monospace">Zona Soplado</text>
      <path d="M 188 238 C 195 160, 220 90, 290 42 L 453 42 L 453 240 Z" fill="rgba(153, 27, 27, 0.12)" stroke="#991B1B" stroke-width="1.6" />
      <text x="348" y="145" text-anchor="middle" fill="#991B1B" font-size="10" font-weight="bold" font-family="monospace">Propagación Sostenida</text>
      <circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="7.5" fill="#B43E18" stroke="#18181B" stroke-width="2" />
      <text x="250" y="268" text-anchor="middle" fill="#3F3F46" font-size="10" font-family="monospace">% O2 (14% a 60%+)</text>
      <text x="18" y="138" transform="rotate(-90 18 138)" text-anchor="middle" fill="#3F3F46" font-size="10" font-family="monospace">Flujo (cm/s)</text>
    `;
  }

  async function runFlammabilitySandbox() {
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

    renderFlammabilityContour(o2, flow);

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
      setRuntimeBadge(false);
      const mMap = { Algodon: 1.35, PMMA: 1.15, SIBAL: 1.05, Nomex: 0.42, Kapton: 0.35, PTFE: 0.25 };
      const flowEff = Math.max(0.3, flow + 12.0 * Math.pow(grav, 0.7));
      const pe = (flowEff * Math.max(0.3, thick)) / 1.8;
      const da = (0.45 * (mMap[mat] || 1) * Math.pow(o2 / 21, 2.1) * Math.pow(press / 14.7, 0.75)) / Math.max(0.35, flowEff * 0.08);
      const flamIdx = Math.pow(o2 / 21, 1.8) * (mMap[mat] || 1) * (fdir === "concurrent" ? 1.25 : 0.85) / (0.65 + 0.35 * thick);
      const extProb = 1 / (1 + Math.exp(3.4 * (flamIdx - 0.78)));
      const vf = Math.max(0.05, 2.4 * flamIdx * (1 + 0.025 * Math.min(flow, 30)));
      renderFlammabilityOutput({
        extinguished_prob: extProb,
        flame_spread_mm_s: vf,
        damkohler: da,
        peclet: pe,
        regime: flamIdx < 0.72 ? "Extinción Radiativa (Quenching)" : (o2 >= 32 ? "Propagación Acelerada" : "Propagación Estable 0g"),
        feature_importance: [
          { feature: "Concentración O2 (%)", importance: 0.41 },
          { feature: "Reactividad del Material", importance: 0.28 },
          { feature: "Velocidad de Flujo (cm/s)", importance: 0.16 },
          { feature: "Espesor de Muestra (cm)", importance: 0.15 }
        ]
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
      setRuntimeBadge(false);
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
    const svgInk = snap.fsm_state === "NORMAL" ? "#065F46" : snap.fsm_state === "PRE_ALERTA" ? "#78350F" : snap.fsm_state === "CONTENCION" ? "#991B1B" : "#7C280C";
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

  // --- MODULO 4: RIESGO FMEA Y TRANSFERENCIA TERRESTRE ---
  async function updateGovernance() {
    const mitigated = document.getElementById("fmeaMitigatedToggle").checked;
    const spinoffId = document.getElementById("spinoffSelect").value;
    const units = Number(document.getElementById("unitsSlider").value);
    document.getElementById("unitsVal").textContent = String(units);

    const suppKind = document.getElementById("suppScenarioSelect").value;
    const suppText = suppKind === "auto_oxidizing"
      ? "Protocolo recomendado: niebla fina PFE (20–100 micras). Cortar el aire no apaga reactivos LiClO4 auto-oxidantes."
      : suppKind === "laminar_diffusion"
      ? "Protocolo recomendado: supresión asistida por campo eléctrico (+/-10 kV ACME) sin consumir agente extintor."
      : "Protocolo recomendado: niebla fina PFE estándar de la Estación Espacial, segura cerca de paneles electrónicos.";
    document.getElementById("suppOutputBox").textContent = suppText;

    try {
      const data = await apiJson(`/api/v1/governance/fmea-and-spinoffs?mitigated=${mitigated}&spinoff_id=${encodeURIComponent(spinoffId)}&units=${units}`);
      document.getElementById("fmeaSummaryLine").textContent = `NPR Total: ${data.fmea_summary.total_active_npr} / ${data.fmea_summary.total_baseline_npr} (Reducción ${data.fmea_summary.average_npr_reduction_pct}%)`;
      document.getElementById("fmeaTableBody").innerHTML = data.fmea_rows.map((r) => `
        <tr>
          <td class="mono"><strong>${escapeHtml(r.mode_id)}</strong></td>
          <td><strong>${escapeHtml(r.subsystem)}</strong><br /><span>${escapeHtml(r.failure_mode)}</span></td>
          <td class="mono tabular"><strong>${r.active_npr}</strong> <small>(base ${r.baseline_npr})</small></td>
          <td>${escapeHtml(r.mitigation)}</td>
          <td class="mono">${escapeHtml(r.linked_psi)}</td>
        </tr>
      `).join("");
      const sp = data.spinoff_metrics;
      document.getElementById("spinWeightOut").textContent = sp.weight_saved_lb_total.toLocaleString() + " lb";
      document.getElementById("spinRiskOut").textContent = "-" + sp.risk_reduction_pct + "%";
      document.getElementById("spinPsiOut").textContent = sp.linked_psi;
      document.getElementById("spinoffDescBox").textContent = `${sp.origin_nasa}: ${sp.earth_impact}`;
    } catch (_) {
      setRuntimeBadge(false);
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
    ["psiFacilitySelect", "personaSelect", "wHabSlider", "wModSlider", "wSenSlider"].forEach((id) => {
      document.getElementById(id).addEventListener("change", runExplorerAndTopsis);
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

    ["o2Slider", "pressSlider", "flowSlider", "thickSlider", "gravSelect", "matSelect", "dirSelect"].forEach((id) => {
      document.getElementById(id).addEventListener("input", runFlammabilitySandbox);
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
      document.getElementById(id).addEventListener("input", updateGovernance);
    });

    const glossaryInput = document.getElementById("glossarySearchInput");
    if (glossaryInput) {
      glossaryInput.addEventListener("input", () => renderGlossary(glossaryInput.value));
    }

    document.addEventListener("keydown", (e) => {
      const tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "SELECT") return;
      const map = { "1": "explorer", "2": "sandbox", "3": "twin", "4": "governance", "5": "blueprint", "6": "museum" };
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
