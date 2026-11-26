(() => {
  "use strict";

  const I18N = {
    de: {
      "nav.overview": "Übersicht",
      "nav.sensors": "Temperaturen",
      "nav.hardware": "Hardware",
      "nav.storage": "Speicher & Netz",
      "nav.processes": "Prozesse",
      "hero.uptime": "Laufzeit",
      "hero.load": "Load Avg",
      "hero.ip": "IP-Adresse",
      "kpi.cpu": "Prozessor",
      "kpi.memory": "Arbeitsspeicher",
      "kpi.temp": "Temperatur",
      "kpi.io": "Netzwerk & I/O",
      "kpi.net_rx": "Download",
      "kpi.net_tx": "Upload",
      "kpi.disk_r": "Disk Lesen",
      "kpi.disk_w": "Disk Schreiben",
      "chart.cpu_mem_title": "Auslastungsverlauf",
      "chart.cpu_mem_desc": "Echtzeit-Verlauf von Prozessor und Arbeitsspeicher",
      "chart.temp_title": "Temperaturverlauf",
      "chart.temp_desc": "Primärer Prozessor-Sensor in °C",
      "chart.net_title": "Netzwerk-Durchsatz",
      "chart.net_desc": "Eingehender (RX) und ausgehender (TX) Datenverkehr",
      "chart.disk_title": "Festplatten-I/O",
      "chart.disk_desc": "Lese- und Schreibdurchsatz aller Blockgeräte",
      "tab.temp": "Temperatur",
      "tab.net": "Netzwerk",
      "tab.disk": "Disk I/O",
      "sensors.title": "Temperaturen & Kühlung",
      "sensors.desc": "Alle erkannten Hardware-Sensoren via lm-sensors, sysfs und GPU-Treiber",
      "sensors.fans": "Lüfter",
      "sensors.power": "Leistung",
      "cpu.cores_title": "Prozessorkerne",
      "hw.title": "Verbaute Hardware & System",
      "hw.desc": "Erkannte Komponenten, Mainboard und Betriebssystem",
      "hw.refresh": "Neu einlesen",
      "storage.title": "Speicher & Dateisysteme",
      "storage.desc": "Eingehängte Partitionen und freier Platz",
      "net.title": "Netzwerk-Schnittstellen",
      "net.desc": "Adapter, IP-Adressen und aktueller Durchsatz",
      "net.show_virtual": "Virtuelle",
      "proc.title": "Aktive Prozesse",
      "proc.desc": "Sortierbare Übersicht nach CPU-Last und Arbeitsspeicher",
      "proc.name": "Prozess",
      "proc.user": "Benutzer",
      "proc.state": "Status",
      "proc.mem": "RAM",
      "proc.placeholder": "Prozess oder Benutzer suchen…",
      "conn.live": "Live",
      "conn.reconnecting": "Verbindet…",
      "conn.offline": "Offline",
      "hw.cpu": "Prozessor",
      "hw.cores": "Kerne / Threads",
      "hw.freq": "Taktbereich",
      "hw.cache": "Cache",
      "hw.ram": "Arbeitsspeicher",
      "hw.gpu": "Grafikkarte",
      "hw.board": "System / Mainboard",
      "hw.bios": "BIOS / Firmware",
      "hw.os": "Betriebssystem",
      "hw.kernel": "Kernel / Arch",
      "hw.disks": "Laufwerke",
      "hw.none": "Nicht erkannt",
      "hw.baremetal": "Bare-Metal",
      "sensor.all": "Alle",
      "sensor.none_title": "Keine physischen Temperatursensoren erkannt",
      "sensor.none_vm": "Dieses System läuft in einer virtualisierten Umgebung (Hypervisor / Container), die keine Hardware-Sensoren durchreicht. Auf einem physischen Linux-Server erscheinen CPU-, NVMe-, GPU- und Mainboard-Temperaturen hier automatisch.",
      "sensor.none_install": "lm-sensors ist noch nicht eingerichtet. Führe das Installationsskript aus mit",
      "chart.no_temp": "Keine Temperaturdaten verfügbar",
      "chart.collecting": "Sammle Messwerte…",
      "updated": "Aktualisiert",
      "tasks": "Tasks",
      "free": "frei",
      "max_label": "Max",
      "crit_label": "Krit",
      "no_sensors_short": "Kein Sensor",
    },
    en: {
      "nav.overview": "Overview",
      "nav.sensors": "Thermal",
      "nav.hardware": "Hardware",
      "nav.storage": "Storage & Net",
      "nav.processes": "Processes",
      "hero.uptime": "Uptime",
      "hero.load": "Load Avg",
      "hero.ip": "IP Address",
      "kpi.cpu": "Processor",
      "kpi.memory": "Memory",
      "kpi.temp": "Temperature",
      "kpi.io": "Network & I/O",
      "kpi.net_rx": "Download",
      "kpi.net_tx": "Upload",
      "kpi.disk_r": "Disk Read",
      "kpi.disk_w": "Disk Write",
      "chart.cpu_mem_title": "Utilization History",
      "chart.cpu_mem_desc": "Real-time processor and memory utilization",
      "chart.temp_title": "Temperature History",
      "chart.temp_desc": "Primary processor sensor in °C",
      "chart.net_title": "Network Throughput",
      "chart.net_desc": "Incoming (RX) and outgoing (TX) bandwidth",
      "chart.disk_title": "Disk I/O",
      "chart.disk_desc": "Aggregate read and write throughput across block devices",
      "tab.temp": "Thermal",
      "tab.net": "Network",
      "tab.disk": "Disk I/O",
      "sensors.title": "Temperatures & Cooling",
      "sensors.desc": "Hardware telemetry via lm-sensors, sysfs, and GPU drivers",
      "sensors.fans": "Fans",
      "sensors.power": "Power",
      "cpu.cores_title": "Processor Cores",
      "hw.title": "System & Hardware",
      "hw.desc": "Detected components, motherboard, and OS environment",
      "hw.refresh": "Refresh",
      "storage.title": "Storage & Filesystems",
      "storage.desc": "Mounted partitions and available capacity",
      "net.title": "Network Interfaces",
      "net.desc": "Adapters, IP addresses, and live throughput",
      "net.show_virtual": "Virtual",
      "proc.title": "Active Processes",
      "proc.desc": "Sortable breakdown by CPU load and memory usage",
      "proc.name": "Process",
      "proc.user": "User",
      "proc.state": "State",
      "proc.mem": "Memory",
      "proc.placeholder": "Search process or user…",
      "conn.live": "Live",
      "conn.reconnecting": "Reconnecting…",
      "conn.offline": "Offline",
      "hw.cpu": "Processor",
      "hw.cores": "Cores / Threads",
      "hw.freq": "Clock Range",
      "hw.cache": "Cache",
      "hw.ram": "Memory",
      "hw.gpu": "Graphics",
      "hw.board": "System / Board",
      "hw.bios": "BIOS / Firmware",
      "hw.os": "Operating System",
      "hw.kernel": "Kernel / Arch",
      "hw.disks": "Drives",
      "hw.none": "Not detected",
      "hw.baremetal": "Bare Metal",
      "sensor.all": "All",
      "sensor.none_title": "No physical temperature sensors detected",
      "sensor.none_vm": "This host runs inside a virtualized environment (hypervisor or container) that does not expose physical thermal sensors. On bare-metal Linux servers, CPU, NVMe, GPU, and motherboard temperatures appear here automatically.",
      "sensor.none_install": "lm-sensors is not configured yet. Run the install script with",
      "chart.no_temp": "No temperature readings available",
      "chart.collecting": "Collecting samples…",
      "updated": "Updated",
      "tasks": "tasks",
      "free": "free",
      "max_label": "High",
      "crit_label": "Crit",
      "no_sensors_short": "No sensor",
    },
  };

  const state = {
    lang: localStorage.getItem("serverstats-lang") || "de",
    hardware: null,
    latest: null,
    history: [],
    interval: 2,
    secondaryTab: "temp",
    sensorCategory: "ALL",
    showVirtualNet: false,
    procSearch: "",
    procSortKey: "cpu_pct",
    procSortAsc: false,
    sse: null,
    pollTimer: null,
  };

  const $ = (id) => document.getElementById(id);
  const t = (key) => (I18N[state.lang] && I18N[state.lang][key]) || I18N.de[key] || key;

  function esc(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function fmtBytes(bytes, decimals = 1) {
    if (!Number.isFinite(bytes) || bytes <= 0) return "0 B";
    const units = ["B", "KB", "MB", "GB", "TB", "PB"];
    const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
    const val = bytes / Math.pow(1024, i);
    const d = i === 0 ? 0 : val >= 100 ? 0 : decimals;
    return `${val.toFixed(d)} ${units[i]}`;
  }

  function fmtRate(bps) {
    if (!Number.isFinite(bps) || bps <= 0) return "0 B/s";
    return `${fmtBytes(bps)}/s`;
  }

  function fmtFreq(mhz) {
    if (!Number.isFinite(mhz) || mhz <= 0) return "—";
    if (mhz >= 1000) return `${(mhz / 1000).toFixed(2)} GHz`;
    return `${Math.round(mhz)} MHz`;
  }

  function fmtUptime(sec) {
    if (!Number.isFinite(sec) || sec < 0) return "—";
    const d = Math.floor(sec / 86400);
    const h = Math.floor((sec % 86400) / 3600);
    const m = Math.floor((sec % 3600) / 60);
    if (d > 0) return `${d}d ${h}h ${m}m`;
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m ${Math.floor(sec % 60)}s`;
  }

  function fmtTime(ts) {
    const d = new Date(ts * 1000);
    return d.toLocaleTimeString(state.lang === "de" ? "de-DE" : "en-GB", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }

  function tempLevel(tempC, highC, critC) {
    const crit = critC || 90;
    const high = highC || 75;
    if (tempC >= crit - 5) return "crit";
    if (tempC >= high - 5) return "warn";
    return "ok";
  }

  // Smooth monotone cubic bezier SVG path builder
  function smoothPath(pts) {
    if (pts.length < 2) return "";
    if (pts.length === 2) {
      return `M ${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)} L ${pts[1][0].toFixed(1)},${pts[1][1].toFixed(1)}`;
    }
    let d = `M ${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[Math.max(0, i - 1)];
      const p1 = pts[i];
      const p2 = pts[i + 1];
      const p3 = pts[Math.min(pts.length - 1, i + 2)];
      const cp1x = p1[0] + (p2[0] - p0[0]) / 6;
      const cp1y = p1[1] + (p2[1] - p0[1]) / 6;
      const cp2x = p2[0] - (p3[0] - p1[0]) / 6;
      const cp2y = p2[1] - (p3[1] - p1[1]) / 6;
      d += ` C ${cp1x.toFixed(1)},${cp1y.toFixed(1)} ${cp2x.toFixed(1)},${cp2y.toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
    }
    return d;
  }

  function applyTranslations() {
    document.documentElement.lang = state.lang;
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.getAttribute("data-i18n");
      if (k) el.textContent = t(k);
    });
    const search = $("proc-search");
    if (search) search.placeholder = t("proc.placeholder");
    $("lang-toggle").textContent = state.lang.toUpperCase();
    updateSecondaryChartHeader();
    if (state.hardware) renderHardware();
    if (state.latest) renderLive(state.latest);
  }

  function updateSecondaryChartHeader() {
    const titleEl = $("secondary-chart-title");
    const descEl = $("secondary-chart-desc");
    if (state.secondaryTab === "temp") {
      titleEl.textContent = t("chart.temp_title");
      descEl.textContent = t("chart.temp_desc");
    } else if (state.secondaryTab === "net") {
      titleEl.textContent = t("chart.net_title");
      descEl.textContent = t("chart.net_desc");
    } else {
      titleEl.textContent = t("chart.disk_title");
      descEl.textContent = t("chart.disk_desc");
    }
  }

  function setConnectionStatus(status) {
    const dot = $("conn-dot");
    const label = $("conn-label");
    dot.className = "status-dot" + (status === "live" ? "" : ` ${status}`);
    if (status === "live") {
      label.textContent = `${t("conn.live")} · ${state.interval}s`;
    } else if (status === "reconnecting") {
      label.textContent = t("conn.reconnecting");
    } else {
      label.textContent = t("conn.offline");
    }
  }

  // -------------------------------------------------------------------------
  // Hardware Rendering
  // -------------------------------------------------------------------------

  function renderHardware() {
    const hw = state.hardware;
    if (!hw) return;

    const hostname = hw.hostname || "Linux Server";
    const osName = hw.os?.name || "Linux";
    const cpu = hw.cpu || {};
    const mem = hw.memory || {};

    $("hdr-hostname").textContent = hostname;
    $("hdr-os").textContent = osName;
    $("hero-hostname").textContent = hostname;
    document.title = `${hostname} — ServerStats`;
    $("footer-host").textContent = `${hostname} · ${osName}`;
    $("hero-ip").textContent = hw.primary_ip || "—";

    const coreCountLabel = cpu.physical_cores && cpu.physical_cores !== cpu.logical_cores
      ? `${cpu.physical_cores}C / ${cpu.logical_cores}T`
      : `${cpu.logical_cores} ${state.lang === "de" ? "Kerne" : "Cores"}`;

    $("hero-specs").textContent = [
      cpu.model,
      coreCountLabel,
      `${fmtBytes(mem.total_bytes || 0, 1)} RAM`,
      `${osName} · Kernel ${hw.kernel}`,
    ].filter(Boolean).join("  ·  ");

    $("cpu-model-subtitle").textContent = cpu.model || "—";
    $("cpu-cores-badge").textContent = coreCountLabel;

    let freqStr = "—";
    if (cpu.min_mhz && cpu.max_mhz) {
      freqStr = `${fmtFreq(cpu.min_mhz)} – ${fmtFreq(cpu.max_mhz)}`;
    } else if (cpu.max_mhz) {
      freqStr = `bis ${fmtFreq(cpu.max_mhz)}`;
    }

    const cacheEntries = Object.entries(cpu.caches || {});
    const cacheStr = cacheEntries.length ? cacheEntries.map(([k, v]) => `${k} ${v}`).join(" · ") : null;

    const memExtra = [mem.type, mem.speed, mem.modules ? `${mem.modules} Slots` : null].filter(Boolean).join(" · ");
    const memStr = fmtBytes(mem.total_bytes || 0, 1) + (memExtra ? ` (${memExtra})` : "");

    const gpuList = hw.gpus || [];
    const gpuHtml = gpuList.length
      ? gpuList
          .map((g) => {
            const sub = [
              g.vram_mb ? `${Math.round((g.vram_mb / 1024) * 10) / 10} GB VRAM` : null,
              g.driver ? `Driver ${g.driver}` : null,
            ].filter(Boolean).join(" · ");
            return `<div>${esc(g.name)}${sub ? `<span class="spec-sub mono">${esc(sub)}</span>` : ""}</div>`;
          })
          .join("")
      : `<span style="color:var(--ink-muted)">${esc(t("hw.none"))}</span>`;

    const board = hw.board || {};
    const boardText = [board.system, board.board].filter(Boolean).join(" · ") || null;

    const disks = hw.disks || [];
    const disksHtml = disks.length
      ? disks
          .map((d) => `<div>${esc(d.model)} <span class="mono" style="color:var(--ink-2)">(${esc(d.media)} · ${fmtBytes(d.size_bytes, 0)})</span></div>`)
          .join("")
      : null;

    const virtStr = cpu.hypervisor ? `${hw.architecture} · ${cpu.hypervisor}` : `${hw.architecture} · ${t("hw.baremetal")}`;

    const rows = [
      [t("hw.cpu"), `<span class="mono">${esc(cpu.model || "—")}</span>`],
      [t("hw.cores"), `<span class="mono">${esc(coreCountLabel)}${cpu.sockets > 1 ? ` · ${cpu.sockets} Sockets` : ""}</span>`],
      freqStr !== "—" ? [t("hw.freq"), `<span class="mono">${esc(freqStr)}</span>`] : null,
      cacheStr ? [t("hw.cache"), `<span class="mono">${esc(cacheStr)}</span>`] : null,
      [t("hw.ram"), `<span class="mono">${esc(memStr)}</span>`],
      [t("hw.gpu"), gpuHtml],
      boardText ? [t("hw.board"), esc(boardText)] : null,
      board.bios ? [t("hw.bios"), `<span class="mono">${esc(board.bios)}</span>`] : null,
      [t("hw.os"), esc(osName)],
      [t("hw.kernel"), `<span class="mono">${esc(hw.kernel)} · ${esc(virtStr)}</span>`],
      disksHtml ? [t("hw.disks"), disksHtml] : null,
    ].filter(Boolean);

    $("hw-spec-list").innerHTML = rows
      .map(([k, v]) => `<div class="spec-row"><dt>${esc(k)}</dt><dd>${v}</dd></div>`)
      .join("");
  }

  // -------------------------------------------------------------------------
  // Smooth SVG Sparklines & Interactive Charts
  // -------------------------------------------------------------------------

  function renderSparkline(containerId, values, color, minVal = 0, maxVal = 100) {
    const el = $(containerId);
    if (!el) return;
    const valid = values.filter((v) => v !== null && v !== undefined && Number.isFinite(v));
    if (valid.length < 2) {
      el.innerHTML = "";
      return;
    }
    const slice = valid.slice(-32);
    const w = 104;
    const h = 36;
    const padX = 2;
    const padY = 4;
    const hi = maxVal === "auto" ? Math.max(...slice, 1) * 1.15 : maxVal;
    const lo = minVal === "auto" ? Math.min(...slice) * 0.9 : minVal;
    const span = Math.max(hi - lo, 0.001);

    const pts = slice.map((v, i) => [
      padX + (i / (slice.length - 1)) * (w - padX * 2),
      h - padY - ((Math.max(lo, Math.min(hi, v)) - lo) / span) * (h - padY * 2),
    ]);

    const line = smoothPath(pts);
    const area = `${line} L ${pts[pts.length - 1][0].toFixed(1)},${h} L ${pts[0][0].toFixed(1)},${h} Z`;
    const gradId = `sg-${containerId}`;

    el.innerHTML = `
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <defs>
          <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="${color}" stop-opacity="0.22"></stop>
            <stop offset="100%" stop-color="${color}" stop-opacity="0.0"></stop>
          </linearGradient>
        </defs>
        <path d="${area}" fill="url(#${gradId})"></path>
        <path d="${line}" fill="none" stroke="${color}" stroke-width="1.8" stroke-linecap="round"></path>
      </svg>`;
  }

  function renderLineChart(containerId, config) {
    const container = $(containerId);
    if (!container) return;

    const points = state.history.slice(-90);
    const { series, fixedMax, yFormat, emptyText } = config;

    const hasAnyValue = points.length >= 2 && series.some((s) => points.some((p) => Number.isFinite(p[s.key])));
    if (!hasAnyValue) {
      container.innerHTML = `<div class="chart-empty">${esc(emptyText || t("chart.collecting"))}</div>`;
      return;
    }

    const rect = container.getBoundingClientRect();
    const width = Math.max(320, Math.round(rect.width || 560));
    const height = 224;
    const padL = 48;
    const padR = 14;
    const padT = 14;
    const padB = 26;
    const plotW = width - padL - padR;
    const plotH = height - padT - padB;

    let maxVal = fixedMax || 0;
    if (!fixedMax) {
      for (const s of series) {
        for (const p of points) {
          if (Number.isFinite(p[s.key]) && p[s.key] > maxVal) maxVal = p[s.key];
        }
      }
      maxVal = maxVal <= 0 ? 10 : maxVal * 1.2;
    }
    const minVal = 0;
    const span = Math.max(maxVal - minVal, 1);

    const xOf = (i) => padL + (i / (points.length - 1)) * plotW;
    const yOf = (v) => padT + plotH - ((Math.max(minVal, Math.min(maxVal, v)) - minVal) / span) * plotH;

    let defsSvg = "";
    let gridSvg = "";
    for (let i = 0; i <= 4; i++) {
      const val = minVal + (span * i) / 4;
      const y = yOf(val);
      gridSvg += `<line x1="${padL}" y1="${y.toFixed(1)}" x2="${width - padR}" y2="${y.toFixed(1)}" stroke="var(--border)" stroke-width="1" ${i > 0 ? 'stroke-dasharray="3,4"' : ""} />`;
      gridSvg += `<text x="${padL - 10}" y="${(y + 3.5).toFixed(1)}" text-anchor="end" font-size="11" fill="var(--ink-muted)" font-family="var(--font-mono)">${esc(yFormat(val))}</text>`;
    }

    const xIndices = [0, Math.floor((points.length - 1) / 2), points.length - 1];
    let xSvg = "";
    const usedX = new Set();
    for (const idx of xIndices) {
      if (usedX.has(idx) || !points[idx]) continue;
      usedX.add(idx);
      const x = xOf(idx);
      const anchor = idx === 0 ? "start" : idx === points.length - 1 ? "end" : "middle";
      xSvg += `<text x="${x.toFixed(1)}" y="${height - 5}" text-anchor="${anchor}" font-size="11" fill="var(--ink-muted)" font-family="var(--font-mono)">${esc(fmtTime(points[idx].ts))}</text>`;
    }

    let seriesSvg = "";
    let markersSvg = "";
    series.forEach((s, sIdx) => {
      const gradId = `cg-${containerId}-${sIdx}`;
      defsSvg += `
        <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="${s.color}" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="${s.color}" stop-opacity="0.0"></stop>
        </linearGradient>`;

      const segs = [];
      let current = [];
      points.forEach((p, idx) => {
        const v = p[s.key];
        if (Number.isFinite(v)) {
          current.push([xOf(idx), yOf(v)]);
        } else if (current.length) {
          segs.push(current);
          current = [];
        }
      });
      if (current.length) segs.push(current);

      for (const seg of segs) {
        if (seg.length < 2) continue;
        const path = smoothPath(seg);
        if (s.fill) {
          const area = `${path} L ${seg[seg.length - 1][0].toFixed(1)},${(padT + plotH).toFixed(1)} L ${seg[0][0].toFixed(1)},${(padT + plotH).toFixed(1)} Z`;
          seriesSvg += `<path d="${area}" fill="url(#${gradId})" />`;
        }
        seriesSvg += `<path d="${path}" fill="none" stroke="${s.color}" stroke-width="2" stroke-linecap="round" />`;
      }
      markersSvg += `<circle class="hover-dot" data-sidx="${sIdx}" r="4" fill="${s.color}" stroke="var(--bg-card)" stroke-width="2" visibility="hidden" />`;
    });

    container.innerHTML = `
      <svg viewBox="0 0 ${width} ${height}">
        <defs>${defsSvg}</defs>
        ${gridSvg}
        ${seriesSvg}
        <line class="crosshair" x1="0" y1="${padT}" x2="0" y2="${padT + plotH}" stroke="var(--border-strong)" stroke-width="1" visibility="hidden" />
        ${markersSvg}
        ${xSvg}
        <rect class="hover-zone" x="${padL}" y="${padT}" width="${plotW}" height="${plotH}" fill="transparent" />
      </svg>`;

    const svg = container.querySelector("svg");
    const zone = container.querySelector(".hover-zone");
    const crosshair = container.querySelector(".crosshair");
    const dots = container.querySelectorAll(".hover-dot");
    const tooltip = $("chart-tooltip");

    zone.addEventListener("mousemove", (ev) => {
      const srect = svg.getBoundingClientRect();
      const relX = ((ev.clientX - srect.left) / srect.width) * width;
      const ratio = Math.max(0, Math.min(1, (relX - padL) / plotW));
      const idx = Math.round(ratio * (points.length - 1));
      const pt = points[idx];
      if (!pt) return;

      const cx = xOf(idx);
      crosshair.setAttribute("x1", cx.toFixed(1));
      crosshair.setAttribute("x2", cx.toFixed(1));
      crosshair.setAttribute("visibility", "visible");

      series.forEach((s, sIdx) => {
        const dot = dots[sIdx];
        if (!dot) return;
        if (Number.isFinite(pt[s.key])) {
          dot.setAttribute("cx", cx.toFixed(1));
          dot.setAttribute("cy", yOf(pt[s.key]).toFixed(1));
          dot.setAttribute("visibility", "visible");
        } else {
          dot.setAttribute("visibility", "hidden");
        }
      });

      const rowsHtml = series
        .map((s) => {
          const val = Number.isFinite(pt[s.key]) ? s.format(pt[s.key]) : "—";
          return `<div class="tt-row"><span class="tt-key"><i class="dot" style="background:${s.color}"></i>${esc(s.label)}</span><strong>${esc(val)}</strong></div>`;
        })
        .join("");

      tooltip.innerHTML = `<div class="tt-time">${esc(fmtTime(pt.ts))}</div>${rowsHtml}`;
      tooltip.hidden = false;

      const ttW = tooltip.offsetWidth || 160;
      const ttH = tooltip.offsetHeight || 72;
      let left = ev.clientX + 16;
      let top = ev.clientY - ttH - 12;
      if (left + ttW > window.innerWidth - 10) left = ev.clientX - ttW - 16;
      if (top < 10) top = ev.clientY + 16;
      tooltip.style.left = `${left}px`;
      tooltip.style.top = `${top}px`;
    });

    zone.addEventListener("mouseleave", () => {
      crosshair.setAttribute("visibility", "hidden");
      dots.forEach((d) => d.setAttribute("visibility", "hidden"));
      tooltip.hidden = true;
    });
  }

  function renderCharts() {
    renderLineChart("chart-cpu-mem", {
      fixedMax: 100,
      yFormat: (v) => `${Math.round(v)}%`,
      series: [
        { key: "cpu", label: "CPU", color: "var(--cpu)", fill: true, format: (v) => `${v.toFixed(1)}%` },
        { key: "mem", label: "RAM", color: "var(--mem)", fill: false, format: (v) => `${v.toFixed(1)}%` },
      ],
    });

    if (state.secondaryTab === "temp") {
      renderLineChart("chart-secondary", {
        fixedMax: 100,
        yFormat: (v) => `${Math.round(v)}°C`,
        emptyText: t("chart.no_temp"),
        series: [
          { key: "temp", label: "CPU", color: "var(--warn)", fill: true, format: (v) => `${v.toFixed(1)} °C` },
        ],
      });
    } else if (state.secondaryTab === "net") {
      renderLineChart("chart-secondary", {
        fixedMax: null,
        yFormat: (v) => fmtRate(v),
        series: [
          { key: "net_rx", label: "RX", color: "var(--cpu)", fill: true, format: (v) => fmtRate(v) },
          { key: "net_tx", label: "TX", color: "var(--mem)", fill: false, format: (v) => fmtRate(v) },
        ],
      });
    } else {
      renderLineChart("chart-secondary", {
        fixedMax: null,
        yFormat: (v) => fmtRate(v),
        series: [
          { key: "disk_r", label: "Read", color: "var(--cpu)", fill: true, format: (v) => fmtRate(v) },
          { key: "disk_w", label: "Write", color: "var(--sys)", fill: false, format: (v) => fmtRate(v) },
        ],
      });
    }
  }

  // -------------------------------------------------------------------------
  // Live Telemetry Rendering
  // -------------------------------------------------------------------------

  function renderLive(snap) {
    if (!snap) return;

    const cpu = snap.cpu;
    const mem = snap.memory;
    const temps = snap.temperatures;
    const net = snap.network;

    $("hero-uptime").textContent = fmtUptime(snap.uptime_seconds);
    $("hero-load").textContent = `${cpu.load.load1.toFixed(2)} · ${cpu.load.load5.toFixed(2)} · ${cpu.load.load15.toFixed(2)}`;
    $("footer-updated").textContent = `${t("updated")}: ${fmtTime(snap.timestamp)}`;

    // 1. KPI CPU
    $("kpi-cpu-val").textContent = cpu.usage_pct.toFixed(1);
    $("kpi-cpu-freq").textContent = fmtFreq(cpu.freq_mhz);
    $("bar-cpu-user").style.width = `${Math.min(100, cpu.user_pct)}%`;
    $("bar-cpu-sys").style.width = `${Math.min(100, cpu.system_pct)}%`;
    $("bar-cpu-io").style.width = `${Math.min(100, cpu.iowait_pct)}%`;
    $("kpi-cpu-breakdown").textContent = `User ${cpu.user_pct.toFixed(0)}% · Sys ${cpu.system_pct.toFixed(0)}%`;
    $("kpi-cpu-tasks").textContent = `${cpu.load.tasks_total} ${t("tasks")}`;
    $("leg-cpu").textContent = `${cpu.usage_pct.toFixed(1)}%`;

    // 2. KPI RAM
    $("kpi-mem-val").textContent = mem.used_pct.toFixed(1);
    $("kpi-mem-total").textContent = fmtBytes(mem.total_bytes, 1);
    const cachedPct = mem.total_bytes > 0 ? ((mem.cached_bytes + mem.buffers_bytes) / mem.total_bytes) * 100 : 0;
    $("bar-mem-used").style.width = `${Math.min(100, mem.used_pct)}%`;
    $("bar-mem-cached").style.width = `${Math.min(Math.max(0, 100 - mem.used_pct), cachedPct)}%`;
    $("kpi-mem-detail").textContent = `${fmtBytes(mem.used_bytes, 1)} / ${fmtBytes(mem.total_bytes, 1)}`;
    $("kpi-swap-detail").textContent = mem.swap_total_bytes > 0
      ? `Swap ${fmtBytes(mem.swap_used_bytes, 1)}`
      : "Swap —";
    $("leg-mem").textContent = `${mem.used_pct.toFixed(1)}%`;

    // 3. KPI Temp
    const primary = temps.cpu_primary || temps.hottest;
    const tempWrap = $("kpi-temp-wrap");
    const tempBar = $("bar-temp");
    if (primary) {
      const lvl = tempLevel(primary.current_c, primary.high_c, primary.crit_c);
      $("kpi-temp-val").textContent = primary.current_c.toFixed(1);
      $("kpi-temp-unit").textContent = "°C";
      tempWrap.className = "kpi-figure mono" + (lvl === "ok" ? "" : ` temp-${lvl}`);
      const maxScale = primary.crit_c || 100;
      tempBar.style.width = `${Math.max(5, Math.min(100, (primary.current_c / maxScale) * 100))}%`;
      tempBar.className = `progress-fill fill-${lvl}`;
      $("kpi-temp-source").textContent = primary.chip || "Sensor";
      $("kpi-temp-label").textContent = primary.label;
      if (temps.fans && temps.fans.length) {
        $("kpi-temp-extra").textContent = `${temps.fans[0].rpm} RPM`;
      } else if (primary.crit_c) {
        $("kpi-temp-extra").textContent = `${t("crit_label")} ${primary.crit_c.toFixed(0)}°C`;
      } else {
        $("kpi-temp-extra").textContent = `${temps.sensors.length} Sensoren`;
      }
    } else {
      $("kpi-temp-val").textContent = "—";
      $("kpi-temp-unit").textContent = "";
      tempWrap.className = "kpi-figure mono";
      tempBar.style.width = "0%";
      tempBar.className = "progress-fill fill-ok";
      $("kpi-temp-source").textContent = t("no_sensors_short");
      $("kpi-temp-label").textContent = state.hardware?.cpu?.hypervisor ? `${state.hardware.cpu.hypervisor} VM` : "lm-sensors";
      $("kpi-temp-extra").textContent = "—";
    }

    // 4. KPI Network & Disk I/O
    const primaryIface = net.interfaces.find((i) => !i.is_virtual && i.operstate === "UP") || net.interfaces[0];
    $("kpi-net-iface").textContent = primaryIface ? primaryIface.name : "—";
    $("kpi-net-rx").textContent = fmtRate(net.rx_bps);
    $("kpi-net-tx").textContent = fmtRate(net.tx_bps);
    $("kpi-disk-r").textContent = fmtRate(snap.disk_io.read_bps);
    $("kpi-disk-w").textContent = fmtRate(snap.disk_io.write_bps);
    $("kpi-net-speed").textContent = primaryIface?.speed_mbps ? `${primaryIface.speed_mbps} Mbit/s` : primaryIface?.operstate || "—";
    $("kpi-net-total").textContent = primaryIface
      ? `↓ ${fmtBytes(primaryIface.rx_total_bytes, 1)} · ↑ ${fmtBytes(primaryIface.tx_total_bytes, 1)}`
      : "—";

    // Sparklines & Charts
    renderSparkline("spark-cpu", state.history.map((p) => p.cpu), "var(--cpu)", 0, 100);
    renderSparkline("spark-mem", state.history.map((p) => p.mem), "var(--mem)", 0, 100);
    renderSparkline("spark-temp", state.history.map((p) => p.temp), "var(--warn)", 20, 100);
    renderCharts();

    // Detail Sections
    renderSensors(temps);
    renderCores(cpu);
    renderGpuLive(temps.gpu_live || []);
    renderFilesystems(snap.filesystems || []);
    renderNetwork(net.interfaces || []);
    renderProcesses(snap.processes || []);
  }

  function renderSensors(temps) {
    const sensors = temps.sensors || [];
    const fans = temps.fans || [];
    const power = temps.power || [];
    const tabsEl = $("sensor-category-tabs");
    const contentEl = $("sensors-content");

    if (!sensors.length) {
      tabsEl.innerHTML = "";
      const isVm = Boolean(state.hardware?.cpu?.hypervisor);
      const hint = isVm || temps.lm_sensors_installed
        ? `<p>${esc(t("sensor.none_vm"))}</p>`
        : `<p>${esc(t("sensor.none_install"))} <code>sudo ./install.sh</code></p>`;
      contentEl.innerHTML = `
        <div class="sensor-empty">
          <strong>${esc(t("sensor.none_title"))}</strong>
          ${hint}
        </div>`;
    } else {
      const categories = ["ALL", ...Array.from(new Set(sensors.map((s) => s.category)))];
      if (!categories.includes(state.sensorCategory)) state.sensorCategory = "ALL";

      tabsEl.innerHTML = categories
        .map((cat) => {
          const label = cat === "ALL" ? `${t("sensor.all")} (${sensors.length})` : cat;
          const active = cat === state.sensorCategory ? "active" : "";
          return `<button type="button" class="filter-chip ${active}" data-cat="${esc(cat)}">${esc(label)}</button>`;
        })
        .join("");

      const filtered = state.sensorCategory === "ALL"
        ? sensors
        : sensors.filter((s) => s.category === state.sensorCategory);

      contentEl.innerHTML = `<div class="sensor-grid">${filtered
        .map((s) => {
          const lvl = tempLevel(s.current_c, s.high_c, s.crit_c);
          const maxScale = s.crit_c || 100;
          const pct = Math.max(4, Math.min(100, (s.current_c / maxScale) * 100));
          const bounds = [
            s.high_c ? `${t("max_label")} ${s.high_c.toFixed(0)}°` : null,
            s.crit_c ? `${t("crit_label")} ${s.crit_c.toFixed(0)}°` : null,
          ].filter(Boolean).join(" · ");
          return `
            <div class="sensor-tile">
              <div class="sensor-top">
                <span class="sensor-name" title="${esc(s.label)}">${esc(s.label)}</span>
                <span class="sensor-temp mono ${lvl}">${s.current_c.toFixed(1)} °C</span>
              </div>
              <div class="sensor-bar">
                <div class="sensor-bar-fill ${lvl}" style="width:${pct}%"></div>
              </div>
              <div class="sensor-foot mono">
                <span>${esc(s.chip)} · ${esc(s.category)}</span>
                <span>${esc(bounds || "—")}</span>
              </div>
            </div>`;
        })
        .join("")}</div>`;
    }

    const auxRow = $("aux-sensors-row");
    const fansBlock = $("fans-block");
    const powerBlock = $("power-block");

    if (!fans.length && !power.length) {
      auxRow.hidden = true;
      return;
    }

    auxRow.hidden = false;
    fansBlock.hidden = !fans.length;
    powerBlock.hidden = !power.length;

    if (fans.length) {
      $("fans-list").innerHTML = fans
        .map((f) => `<div class="aux-pill"><span class="aux-pill-k">${esc(f.label)}</span><span class="aux-pill-v mono">${f.rpm} RPM</span></div>`)
        .join("");
    }
    if (power.length) {
      $("power-list").innerHTML = power
        .map((p) => `<div class="aux-pill"><span class="aux-pill-k">${esc(p.label)}</span><span class="aux-pill-v mono">${p.watts.toFixed(1)} W</span></div>`)
        .join("");
    }
  }

  function renderCores(cpu) {
    const cores = cpu.cores || [];
    $("cores-grid").innerHTML = cores
      .map((c) => {
        const cls = c.usage_pct >= 88 ? "crit" : c.usage_pct >= 68 ? "warn" : "";
        return `
          <div class="core-tile">
            <div class="core-head mono">
              <span class="core-id">Core ${c.id}</span>
              <span class="core-val">${c.usage_pct.toFixed(0)}%</span>
            </div>
            <div class="core-track">
              <div class="core-fill ${cls}" style="width:${Math.min(100, c.usage_pct)}%"></div>
            </div>
            <div class="core-freq mono">${fmtFreq(c.freq_mhz)}</div>
          </div>`;
      })
      .join("");
  }

  function renderGpuLive(gpuLive) {
    const wrap = $("gpu-live-wrap");
    if (!gpuLive.length) {
      wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    wrap.innerHTML = gpuLive
      .map((g) => {
        const parts = [
          Number.isFinite(g.util_pct) ? `${g.util_pct.toFixed(0)}% GPU` : null,
          Number.isFinite(g.vram_used_mb) && Number.isFinite(g.vram_total_mb)
            ? `${(g.vram_used_mb / 1024).toFixed(1)} / ${(g.vram_total_mb / 1024).toFixed(1)} GB VRAM`
            : null,
          Number.isFinite(g.temp_c) ? `${g.temp_c.toFixed(0)} °C` : null,
          Number.isFinite(g.power_w) ? `${g.power_w.toFixed(0)} W` : null,
        ].filter(Boolean);
        return `
          <div class="gpu-live-row">
            <strong>${esc(g.name)}</strong>
            <span class="mono" style="color:var(--ink-2)">${parts.join(" · ")}</span>
          </div>`;
      })
      .join("");
  }

  function renderFilesystems(filesystems) {
    const totalBytes = filesystems.reduce((acc, f) => acc + (f.total_bytes || 0), 0);
    const usedBytes = filesystems.reduce((acc, f) => acc + (f.used_bytes || 0), 0);
    $("storage-summary").textContent = `${fmtBytes(usedBytes, 1)} / ${fmtBytes(totalBytes, 1)}`;

    $("fs-list").innerHTML = filesystems
      .map((f) => {
        const fillCls = f.used_pct >= 90 ? "fill-crit" : f.used_pct >= 75 ? "fill-warn" : "fill-cpu";
        return `
          <div class="fs-item">
            <div class="fs-top">
              <div>
                <span class="fs-mount mono">${esc(f.mount)}</span>
                <span class="fs-type mono">${esc(f.fstype)}</span>
              </div>
              <span class="fs-pct mono">${f.used_pct.toFixed(1)}%</span>
            </div>
            <div class="progress-rail">
              <div class="progress-fill ${fillCls}" style="width:${Math.min(100, f.used_pct)}%"></div>
            </div>
            <div class="fs-foot mono">
              <span>${esc(f.device)}</span>
              <span>${fmtBytes(f.used_bytes, 1)} / ${fmtBytes(f.total_bytes, 1)} (${fmtBytes(f.available_bytes, 1)} ${esc(t("free"))})</span>
            </div>
          </div>`;
      })
      .join("");
  }

  function renderNetwork(interfaces) {
    const list = state.showVirtualNet ? interfaces : interfaces.filter((i) => !i.is_virtual);
    const shown = list.length ? list : interfaces;

    $("net-list").innerHTML = shown
      .map((i) => {
        const ips = [...(i.ipv4 || []), ...(i.ipv6 || []).slice(0, 1)];
        const isUp = i.operstate === "UP";
        const speed = i.speed_mbps ? `${i.speed_mbps} Mbit/s` : i.mac || "";
        return `
          <div class="net-item">
            <div class="net-top">
              <div class="net-name-group">
                <span class="net-name mono">${esc(i.name)}</span>
                <span class="state-badge ${isUp ? "up" : ""}">${esc(i.operstate)}</span>
              </div>
              <div class="net-rates mono">
                <span>↓ ${fmtRate(i.rx_bps)}</span>
                <span>↑ ${fmtRate(i.tx_bps)}</span>
              </div>
            </div>
            <div class="net-foot mono">
              <span>${ips.length ? esc(ips.join(" · ")) : "—"}</span>
              <span>${speed ? `${esc(speed)} · ` : ""}Σ ${fmtBytes(i.rx_total_bytes + i.tx_total_bytes, 1)}</span>
            </div>
          </div>`;
      })
      .join("");
  }

  function renderProcesses(processes) {
    const q = state.procSearch.trim().toLowerCase();
    let list = q
      ? processes.filter((p) => p.name.toLowerCase().includes(q) || p.user.toLowerCase().includes(q) || String(p.pid).includes(q))
      : processes.slice();

    const key = state.procSortKey;
    const dir = state.procSortAsc ? 1 : -1;
    list.sort((a, b) => {
      const av = a[key];
      const bv = b[key];
      if (typeof av === "string") return av.localeCompare(bv) * dir;
      return ((av || 0) - (bv || 0)) * dir;
    });

    $("proc-tbody").innerHTML = list
      .slice(0, 18)
      .map((p) => {
        const cpuBarW = Math.min(100, p.cpu_pct);
        const memBarW = Math.min(100, p.mem_pct * 2);
        return `
          <tr>
            <td class="num mono" style="color:var(--ink-muted)">${p.pid}</td>
            <td class="proc-name mono">${esc(p.name)}</td>
            <td class="mono" style="color:var(--ink-2)">${esc(p.user)}</td>
            <td class="mono" style="color:var(--ink-muted)">${esc(p.state)}</td>
            <td class="num mono">
              <span class="proc-metric-cell">
                <span class="proc-mini-bar"><span class="proc-mini-fill" style="width:${cpuBarW}%"></span></span>
                <span>${p.cpu_pct.toFixed(1)}%</span>
              </span>
            </td>
            <td class="num mono">${fmtBytes(p.mem_bytes, 1)}</td>
            <td class="num mono">
              <span class="proc-metric-cell">
                <span class="proc-mini-bar"><span class="proc-mini-fill" style="width:${memBarW}%;background:var(--mem)"></span></span>
                <span>${p.mem_pct.toFixed(1)}%</span>
              </span>
            </td>
          </tr>`;
      })
      .join("");
  }

  // -------------------------------------------------------------------------
  // Data Fetching & SSE Live Stream
  // -------------------------------------------------------------------------

  function pushHistoryPoint(snap) {
    const cpuTemp = snap.temperatures?.cpu_primary?.current_c ?? snap.temperatures?.hottest?.current_c ?? null;
    const pt = {
      ts: snap.timestamp,
      cpu: snap.cpu.usage_pct,
      mem: snap.memory.used_pct,
      temp: cpuTemp,
      net_rx: snap.network.rx_bps,
      net_tx: snap.network.tx_bps,
      disk_r: snap.disk_io.read_bps,
      disk_w: snap.disk_io.write_bps,
    };
    const last = state.history[state.history.length - 1];
    if (!last || Math.abs(pt.ts - last.ts) > 0.4) {
      state.history.push(pt);
      if (state.history.length > 300) state.history.shift();
    }
  }

  async function fetchHardware(force = false) {
    try {
      const res = await fetch(force ? "/api/system?refresh=1" : "/api/system");
      if (!res.ok) return;
      state.hardware = await res.json();
      renderHardware();
    } catch (_) {}
  }

  async function fetchHistory() {
    try {
      const res = await fetch("/api/history");
      if (!res.ok) return;
      const data = await res.json();
      if (data.interval) state.interval = data.interval;
      if (Array.isArray(data.points)) state.history = data.points;
    } catch (_) {}
  }

  function startStream() {
    if (state.sse) {
      state.sse.close();
      state.sse = null;
    }
    if (state.pollTimer) {
      clearInterval(state.pollTimer);
      state.pollTimer = null;
    }

    if (typeof EventSource !== "undefined") {
      const es = new EventSource("/api/stream");
      state.sse = es;
      es.addEventListener("open", () => setConnectionStatus("live"));
      es.addEventListener("stats", (ev) => {
        try {
          const snap = JSON.parse(ev.data);
          state.latest = snap;
          pushHistoryPoint(snap);
          setConnectionStatus("live");
          renderLive(snap);
        } catch (_) {}
      });
      es.addEventListener("error", () => setConnectionStatus("reconnecting"));
    } else {
      const poll = async () => {
        try {
          const res = await fetch("/api/stats");
          if (!res.ok) throw new Error();
          const snap = await res.json();
          state.latest = snap;
          pushHistoryPoint(snap);
          setConnectionStatus("live");
          renderLive(snap);
        } catch (_) {
          setConnectionStatus("offline");
        }
      };
      poll();
      state.pollTimer = setInterval(poll, state.interval * 1000);
    }
  }

  function bindEvents() {
    $("theme-toggle").addEventListener("click", () => {
      const cur = document.documentElement.getAttribute("data-theme") || "light";
      const next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("serverstats-theme", next);
    });

    $("lang-toggle").addEventListener("click", () => {
      state.lang = state.lang === "de" ? "en" : "de";
      localStorage.setItem("serverstats-lang", state.lang);
      applyTranslations();
    });

    $("refresh-hw-btn").addEventListener("click", () => fetchHardware(true));

    document.querySelectorAll(".seg-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".seg-btn").forEach((b) => {
          b.classList.remove("active");
          b.setAttribute("aria-selected", "false");
        });
        btn.classList.add("active");
        btn.setAttribute("aria-selected", "true");
        state.secondaryTab = btn.getAttribute("data-chart") || "temp";
        updateSecondaryChartHeader();
        renderCharts();
      });
    });

    $("sensor-category-tabs").addEventListener("click", (ev) => {
      const btn = ev.target.closest(".filter-chip");
      if (!btn) return;
      state.sensorCategory = btn.getAttribute("data-cat") || "ALL";
      if (state.latest) renderSensors(state.latest.temperatures);
    });

    $("toggle-virtual-net").addEventListener("change", (ev) => {
      state.showVirtualNet = Boolean(ev.target.checked);
      if (state.latest) renderNetwork(state.latest.network.interfaces || []);
    });

    $("proc-search").addEventListener("input", (ev) => {
      state.procSearch = ev.target.value || "";
      if (state.latest) renderProcesses(state.latest.processes || []);
    });

    document.querySelectorAll(".proc-table th.sortable").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.getAttribute("data-sort");
        if (!key) return;
        if (state.procSortKey === key) {
          state.procSortAsc = !state.procSortAsc;
        } else {
          state.procSortKey = key;
          state.procSortAsc = key === "name" || key === "user" || key === "pid";
        }
        document.querySelectorAll(".proc-table th.sortable").forEach((h) => h.classList.remove("active-sort", "asc"));
        th.classList.add("active-sort");
        if (state.procSortAsc) th.classList.add("asc");
        if (state.latest) renderProcesses(state.latest.processes || []);
      });
    });

    let resizeTimer;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(renderCharts, 120);
    });
  }

  async function init() {
    bindEvents();
    applyTranslations();
    await Promise.all([fetchHardware(), fetchHistory()]);
    startStream();
  }

  init();
})();
