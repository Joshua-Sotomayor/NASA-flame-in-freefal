(function () {
  "use strict";

  const OFFLINE_PSI = [
    { psi_id: "PSI-98", acronym: "SAFFIRE-I", facility: "Cygnus", doi: "10.60555/psi-98", criteria_scores: { habitat: 0.95, modeling: 0.91, sensors: 0.86, spinoff: 0.84 }, earth_benefits: "Calibrar modelos de incendio en aeronaves y edificios presurizados." },
    { psi_id: "PSI-101", acronym: "SAFFIRE-II", facility: "Cygnus", doi: "10.60555/psi-101", criteria_scores: { habitat: 0.96, modeling: 0.89, sensors: 0.80, spinoff: 0.88 }, earth_benefits: "Seleccionar textiles retardantes seguros para transporte." },
    { psi_id: "PSI-102", acronym: "SAFFIRE-III", facility: "Cygnus", doi: "10.60555/psi-102", criteria_scores: { habitat: 0.93, modeling: 0.90, sensors: 0.82, spinoff: 0.85 }, earth_benefits: "Definir cortes HVAC en tuneles y centros de datos." },
    { psi_id: "PSI-103", acronym: "SAFFIRE-IV", facility: "Cygnus", doi: "10.60555/psi-103", criteria_scores: { habitat: 0.98, modeling: 0.88, sensors: 0.92, spinoff: 0.86 }, earth_benefits: "Optimizar detectores de humo en camaras hiperbaricas." },
    { psi_id: "PSI-104", acronym: "SAFFIRE-V", facility: "Cygnus", doi: "10.60555/psi-104", criteria_scores: { habitat: 0.99, modeling: 0.91, sensors: 0.89, spinoff: 0.87 }, earth_benefits: "Refinar normas NFPA para atmosferas enriquecidas y minas." },
    { psi_id: "PSI-105", acronym: "SAFFIRE-VI", facility: "Cygnus", doi: "10.60555/psi-105", criteria_scores: { habitat: 0.97, modeling: 0.86, sensors: 0.96, spinoff: 0.92 }, earth_benefits: "Proteger cuadrillas contra gases acidos HF/HCl y CO." },
    { psi_id: "PSI-25", acronym: "BASS-II", facility: "ISS-MSG", doi: "10.60555/psi-25", criteria_scores: { habitat: 0.94, modeling: 0.99, sensors: 0.81, spinoff: 0.85 }, earth_benefits: "Calibrar simuladores FDS de seguridad en edificios." },
    { psi_id: "PSI-24", acronym: "FLEX", facility: "ISS-CIR", doi: "10.60555/psi-24", criteria_scores: { habitat: 0.85, modeling: 0.96, sensors: 0.97, spinoff: 0.88 }, earth_benefits: "Prevenir re-igniciones silenciosas por llamas frias NTC." },
    { psi_id: "PSI-129", acronym: "SPICE", facility: "ISS-MSG", doi: "10.60555/psi-129", criteria_scores: { habitat: 0.92, modeling: 0.84, sensors: 0.99, spinoff: 0.98 }, earth_benefits: "Calibrar detectores tempranos de aerosoles <0.1 um." },
    { psi_id: "PSI-110", acronym: "MSC", facility: "Otros", doi: "10.60555/psi-110", criteria_scores: { habitat: 0.95, modeling: 0.87, sensors: 0.97, spinoff: 0.95 }, earth_benefits: "Reducir muertes por combustion latente de espumas." }
  ];

  const FORENSIC_PRESETS = {
    apollo_1: { o2_pct: 100, pressure_psi: 16.7, flow_cm_s: 5, gravity_g: "1", material: "PTFE", thickness_mm: 2.0, flow_dir: "concurrent", note: "Apollo 1 (1967): 100% O2 a 16.7 psi escalo a 29 psi en 15 s. Origino NASA-STD-6001." },
    apollo_13: { o2_pct: 100, pressure_psi: 30.0, flow_cm_s: 2, gravity_g: "0", material: "PTFE", thickness_mm: 1.2, flow_dir: "opposed", note: "Apollo 13 (1970): Simulador capado a 30 psi (tanque real a ~1,000 psi con PTFE >500 C)." },
    mir_1997: { o2_pct: 21, pressure_psi: 14.7, flow_cm_s: 12, gravity_g: "0", material: "SIBAL", thickness_mm: 5.0, flow_dir: "concurrent", note: "Mir Kvant-1 (1997): Cartucho Vika LiClO4 auto-oxidante de 14 min; exige niebla PFE." },
    lunar_artemis: { o2_pct: 34, pressure_psi: 8.2, flow_cm_s: 12, gravity_g: "0.16", material: "SIBAL", thickness_mm: 0.8, flow_dir: "concurrent", note: "Habitat Lunar Artemis: 34% O2 y 8.2 psi validado en SAFFIRE-IV y SAFFIRE-V." }
  };

  const OFFICIAL_RESOURCES = [
    { tag: "Dataset", title: "1. NASA PSI Combustion Repository", url: "https://psi.nasa.gov/physci/repo/search?q=combustion" },
    { tag: "Ciencia", title: "2. NASA Glenn Combustion Science", url: "https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/" },
    { tag: "Video", title: "3. NASA ScienceCasts: ISS Combustion", url: "https://www.youtube.com/watch?v=W1oXykoz9zg" },
    { tag: "Guia", title: "4. Researcher's Guide to ISS Combustion", url: "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/" },
    { tag: "Forense", title: "5. Apollo 1 Historical Case Study", url: "https://sma.nasa.gov/sma-disciplines/accllp/apollo-1" },
    { tag: "Forense", title: "6. Apollo 13 Historical Case Study", url: "https://sma.nasa.gov/sma-disciplines/accllp/apollo-13" },
    { tag: "Forense", title: "7. Fire Aboard Space Station Mir", url: "https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/" },
    { tag: "Spinoff 9582", title: "8. Fireman's Air Tanks (COPV)", url: "https://spinoff.nasa.gov/node/9582" },
    { tag: "Spinoff 9407", title: "9. Incipient Fire Detector (Shuttle)", url: "https://spinoff.nasa.gov/node/9407" },
    { tag: "Spinoff 9918", title: "10. Fire Attire PBI & PFE Mist", url: "https://spinoff.nasa.gov/node/9918" }
  ];

  const SPINOFF_OFFLINE = {
    "9582": { name: "Fireman's Air Tanks (COPV)", weight: 13.0, risk: 40, psi: "PSI-104", origin: "Apollo PLSS (1976)", desc: "Cilindros de 4,500 psi reducen el peso del equipo SCBA de 33 lb a 20 lb (-40%)." },
    "9407": { name: "Incipient Fire Detector", weight: 0.0, risk: 58, psi: "PSI-129", origin: "Space Shuttle (1978)", desc: "Discrimina polvo flotante frente a aerosoles submicronicos <0.1 um antes de llama abierta." },
    "9918": { name: "Fire Attire PBI / FIRES", weight: 11.5, risk: 35, psi: "PSI-101", origin: "Post-Apollo 1 (1977)", desc: "Trajes estructurales PBI + Nomex con >30% menos peso y alta estabilidad termica." },
    "PFE": { name: "ISS Fine Water Mist (PFE)", weight: 4.2, risk: 65, psi: "PSI-107", origin: "ISS Supresion Limpia", desc: "Microgotas Sauter 20-100 um seguras para avionica sin residuos corrosivos HF/HBr." }
  };

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
    badge.textContent = online ? "API FastAPI En Vivo" : "Modo Offline Determinista";
    badge.className = "badge mono " + (online ? "badge-ok" : "badge-warn");
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

  function toggleTheme() {
    const root = document.documentElement;
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
  }

  // --- MODULO 1: TOPSIS + PCA 2D ---
  function renderClustersSvg(points) {
    const svg = document.getElementById("clustersSvg");
    const colors = ["#38bdf8", "#10b981", "#f59e0b", "#818cf8"];
    if (!points.length) {
      svg.innerHTML = "";
      return;
    }
    const xs = points.map((p) => p.x);
    const ys = points.map((p) => p.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs) || 1;
    const minY = Math.min(...ys), maxY = Math.max(...ys) || 1;

    const circles = points.map((pt) => {
      const nx = 45 + ((pt.x - minX) / Math.max(0.01, maxX - minX)) * 390;
      const ny = 195 - ((pt.y - minY) / Math.max(0.01, maxY - minY)) * 160;
      const fill = colors[pt.cluster_id % colors.length];
      return `<g><circle cx="${nx.toFixed(1)}" cy="${ny.toFixed(1)}" r="6" fill="${fill}" opacity="0.88" /><text x="${(nx + 8).toFixed(1)}" y="${(ny + 3).toFixed(1)}" fill="#cbd5e1" font-size="8.5" font-family="monospace">${escapeHtml(pt.acronym)}</text></g>`;
    }).join("");

    svg.innerHTML = `<rect x="25" y="15" width="430" height="195" rx="6" fill="none" stroke="rgba(148,163,184,0.2)" />${circles}`;
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
          `${top.psi_id} (${top.acronym}, ${top.facility}) lidera segun ponderacion actual (${top.doi}).`,
          `${top.earth_benefits}`,
          `Consulta ejecutada en modo offline determinista sobre catalogo local.`
        ],
        cited_dois: [top.doi]
      });
    }
  }

  function renderExplorerOutput(ranked, clusters, synthesis) {
    document.getElementById("synthesisPersonaBadge").textContent = "Síntesis Determinista · " + synthesis.persona;
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

  // --- MODULO 2: SIMULADOR & CONTORNO EN VIVO (M-09) ---
  function renderFlammabilityContour(currentO2, currentFlow) {
    const svg = document.getElementById("flammabilityContourSvg");
    const oxToX = (o2) => 48 + ((Math.min(60, Math.max(14, o2)) - 14) / 46) * 405;
    const flToY = (fl) => 240 - (Math.min(60, Math.max(0, fl)) / 60) * 205;

    const px = oxToX(currentO2);
    const py = flToY(currentFlow);

    svg.innerHTML = `
      <rect x="48" y="35" width="405" height="205" fill="#0b1220" stroke="#475569" />
      <rect x="48" y="218" width="140" height="22" fill="rgba(16,185,129,0.22)" />
      <text x="118" y="232" text-anchor="middle" fill="#34d399" font-size="9" font-family="monospace">Quenching Radiativo</text>
      <polygon points="48,35 190,35 160,115 48,115" fill="rgba(56,189,248,0.16)" />
      <text x="108" y="68" text-anchor="middle" fill="#7dd3fc" font-size="9" font-family="monospace">Zona Blowoff</text>
      <path d="M 188 238 C 195 160, 220 90, 290 42 L 453 42 L 453 240 Z" fill="rgba(239,68,68,0.16)" stroke="#ef4444" stroke-width="1.5" />
      <text x="348" y="145" text-anchor="middle" fill="#fca5a5" font-size="10" font-family="monospace">Zona Propagacion Sostenida</text>
      <circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="2" />
      <text x="250" y="268" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">% O2 (14% a 60%+)</text>
      <text x="18" y="138" transform="rotate(-90 18 138)" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">Flujo (cm/s)</text>
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
          { feature: "Concentracion O2 (%)", importance: 0.41 },
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
    badge.className = "badge mono " + (pred.regime.includes("Extinción") ? "badge-ok" : "badge-danger");

    document.getElementById("featureImportanceBox").innerHTML = pred.feature_importance.slice(0, 5).map((item) => `
      <div class="bar-row">
        <span>${escapeHtml(item.feature)}</span>
        <div class="bar-track"><div class="bar-fill" style="--ratio:${Number(item.importance).toFixed(3)}"></div></div>
        <span class="mono tabular">${(item.importance * 100).toFixed(1)}%</span>
      </div>
    `).join("");
  }

  // --- MODULO 3: GEMELO DIGITAL SVG & FSM (M-06) ---
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
      const clsMap = { nominal: "Nominal", spherical_0g: "Llama Esferica Azul 0g", cool_flame_ntc: "Llama Fria NTC", open_propagation: "Propagacion Abierta" };
      const idx = ["nominal", "spherical_0g", "cool_flame_ntc", "open_propagation"].indexOf(preset);
      const probs = [0.02, 0.02, 0.02, 0.02];
      probs[Math.max(0, idx)] = 0.94;
      renderTwinSnapshot({
        cnn_class: clsMap[preset] || "Nominal",
        cnn_probs: probs,
        tree_rule_path: `dT/dt (${dt.toFixed(1)}) & aerosol (${aer}) -> ${state}`,
        fsm_state: state,
        fan_on: state === "NORMAL" || state === "PRE_ALERTA",
        damper_closed: state === "CONTENCION" || state === "FALLA_SEGURA",
        pfe_active: state === "CONTENCION"
      }, preset);
    }
  }

  function renderTwinSnapshot(snap, preset) {
    document.getElementById("twinCnnOut").textContent = snap.cnn_class;
    document.getElementById("twinFanOut").textContent = snap.fan_on ? "ON" : "OFF";
    document.getElementById("twinDamperOut").textContent = snap.damper_closed ? "Cerrada" : "Abierta";
    document.getElementById("twinPfeOut").textContent = snap.pfe_active ? "ACTIVO (Niebla)" : "Standby";
    document.getElementById("twinTreeRuleBox").textContent = snap.tree_rule_path;

    const fsmBadge = document.getElementById("fsmStateBadge");
    const svgLabel = document.getElementById("twinSvgFsmLabel");
    fsmBadge.textContent = "FSM: " + snap.fsm_state;
    svgLabel.textContent = snap.fsm_state;

    const clsColor = snap.fsm_state === "NORMAL" ? "badge-ok" : snap.fsm_state === "PRE_ALERTA" ? "badge-warn" : snap.fsm_state === "CONTENCION" ? "badge-danger" : "badge-cool";
    fsmBadge.className = "badge mono " + clsColor;

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

    appendEventLog(`FSM=${snap.fsm_state} | CNN=${snap.cnn_class} | Fan=${snap.fan_on} | PFE=${snap.pfe_active}`);
  }

  // --- MODULO 4: FMEA & SPINOFFS ---
  async function updateGovernance() {
    const mitigated = document.getElementById("fmeaMitigatedToggle").checked;
    const spinoffId = document.getElementById("spinoffSelect").value;
    const units = Number(document.getElementById("unitsSlider").value);
    document.getElementById("unitsVal").textContent = String(units);

    const suppKind = document.getElementById("suppScenarioSelect").value;
    const suppText = suppKind === "auto_oxidizing"
      ? "Protocolo Recomendado: PFE (Niebla 20-100 um). Cortar HVAC no apaga reacciones LiClO4."
      : suppKind === "laminar_diffusion"
      ? "Protocolo Recomendado: E-FIELD (+/-10 kV ACME PSI-154) sin consumir fluidos ECLSS."
      : "Protocolo Recomendado: PFE estandar ISS seguro para avionica y libre de HF.";
    document.getElementById("suppOutputBox").textContent = suppText;

    try {
      const data = await apiJson(`/api/v1/governance/fmea-and-spinoffs?mitigated=${mitigated}&spinoff_id=${encodeURIComponent(spinoffId)}&units=${units}`);
      document.getElementById("fmeaSummaryLine").textContent = `NPR Total: ${data.fmea_summary.total_active_npr} / ${data.fmea_summary.total_baseline_npr} (Reduccion ${data.fmea_summary.average_npr_reduction_pct}%)`;
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

  function renderOfficialResources() {
    document.getElementById("officialResourcesGrid").innerHTML = OFFICIAL_RESOURCES.map((r) => `
      <div class="panel" style="background:var(--bg-elevated); padding:10px 12px;">
        <span class="badge badge-info">${escapeHtml(r.tag)}</span>
        <div style="margin-top:6px; font-weight:600;"><a href="${escapeHtml(r.url)}" target="_blank" rel="noopener noreferrer" style="color:var(--text-primary);">${escapeHtml(r.title)}</a></div>
      </div>
    `).join("");
  }

  function wireEvents() {
    document.querySelectorAll('[role="tab"]').forEach((btn) => {
      btn.addEventListener("click", () => switchTab(btn.dataset.tab));
    });
    document.getElementById("themeBtn").addEventListener("click", toggleTheme);

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

    document.addEventListener("keydown", (e) => {
      const tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "SELECT") return;
      const map = { "1": "explorer", "2": "sandbox", "3": "twin", "4": "governance", "5": "blueprint" };
      if (map[e.key]) switchTab(map[e.key]);
      else if (e.key.toLowerCase() === "t") toggleTheme();
    });
  }

  wireEvents();
  renderOfficialResources();
  runExplorerAndTopsis();
  runFlammabilitySandbox();
  stepDigitalTwin();
  updateGovernance();
})();
