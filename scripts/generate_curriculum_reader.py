#!/usr/bin/env python3
"""
Generate Study_Curriculum_Reader.html
A standalone, responsive, high-contrast executive frontend reader for the 
Downtown San Diego Homelessness 9-Day Study Curriculum and Defense Suite.
"""
import os
import shutil

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Downtown San Diego Homelessness — 9-Day Study Curriculum Reader</title>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(15, 23, 42, 0.75);
      --card-border: rgba(255, 255, 255, 0.1);
      --sidebar-bg: #0b1120;
      --sidebar-border: rgba(255, 255, 255, 0.08);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --cyan: #38bdf8;
      --cyan-dim: rgba(56, 189, 248, 0.15);
      --purple: #c084fc;
      --purple-dim: rgba(192, 132, 252, 0.15);
      --green: #34d399;
      --green-dim: rgba(52, 211, 153, 0.15);
      --amber: #fbbf24;
      --amber-dim: rgba(251, 191, 36, 0.15);
      --red: #f87171;
      --red-dim: rgba(248, 113, 113, 0.15);
      --blue: #60a5fa;
      --blue-dim: rgba(96, 165, 250, 0.15);
    }
    
    [data-theme="light"] {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --sidebar-bg: #f1f5f9;
      --sidebar-border: #cbd5e1;
      --text: #0f172a;
      --text-muted: #475569;
      --cyan: #0284c7;
      --cyan-dim: #e0f2fe;
      --purple: #7c3aed;
      --purple-dim: #f3e8ff;
      --green: #059669;
      --green-dim: #d1fae5;
      --amber: #d97706;
      --amber-dim: #fef3c7;
      --red: #dc2626;
      --red-dim: #fee2e2;
      --blue: #2563eb;
      --blue-dim: #dbeafe;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      display: flex;
      height: 100vh;
      overflow: hidden;
      transition: background 0.2s ease, color 0.2s ease;
    }

    /* Top Banner Bar */
    header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: var(--sidebar-bg);
      border-bottom: 1px solid var(--sidebar-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      font-size: 1.5em;
    }
    .brand-title {
      font-weight: 800;
      font-size: 1.05em;
      letter-spacing: -0.01em;
    }
    .brand-subtitle {
      font-size: 0.78em;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 0.82em;
      font-weight: 650;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
    }
    .btn-cyan { background: var(--cyan-dim); color: var(--cyan); border-color: var(--cyan); }
    .btn-cyan:hover { filter: brightness(1.15); transform: translateY(-1px); }
    .btn-green { background: var(--green-dim); color: var(--green); border-color: var(--green); }
    .btn-green:hover { filter: brightness(1.15); transform: translateY(-1px); }
    .btn-toggle {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 6px 10px;
    }

    /* Layout */
    .app-container {
      display: flex;
      width: 100%;
      height: calc(100vh - 60px);
      margin-top: 60px;
    }

    /* Sidebar Navigation */
    nav.sidebar {
      width: 320px;
      min-width: 320px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--sidebar-border);
      height: 100%;
      overflow-y: auto;
      padding: 16px 12px 60px 12px;
    }
    .nav-group-title {
      font-size: 0.72em;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      padding: 12px 12px 6px 12px;
    }
    .nav-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 3px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88em;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.12s ease;
      border-left: 3px solid transparent;
    }
    .nav-item:hover {
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
    }
    [data-theme="light"] .nav-item:hover {
      background: rgba(0, 0, 0, 0.05);
    }
    .nav-item.active {
      background: var(--cyan-dim);
      color: var(--cyan);
      border-left: 3px solid var(--cyan);
      font-weight: 750;
    }
    .badge {
      font-size: 0.72em;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
    }

    /* Main Content Area */
    main.content {
      flex: 1;
      height: 100%;
      overflow-y: auto;
      padding: 32px 48px 100px 48px;
      max-width: 1100px;
      margin: 0 auto;
    }

    .tab-pane {
      display: none;
      animation: fadeIn 0.18s ease-in;
    }
    .tab-pane.active {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Typography & Headers */
    .day-badge-header {
      font-size: 0.78em;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--cyan);
      margin-bottom: 6px;
    }
    h1.day-title {
      font-size: 2.2em;
      font-weight: 800;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }
    .day-subtitle {
      font-size: 1.05em;
      color: var(--text-muted);
      margin-bottom: 24px;
    }

    /* Cards & Boxes */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 22px;
      margin-bottom: 22px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    .card-cyan { border-left: 4px solid var(--cyan); }
    .card-purple { border-left: 4px solid var(--purple); }
    .card-amber { border-left: 4px solid var(--amber); }
    .card-green { border-left: 4px solid var(--green); }
    .card-red { border-left: 4px solid var(--red); }
    .card-blue { border-left: 4px solid var(--blue); }

    .card-title {
      font-size: 1.1em;
      font-weight: 800;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Stat Cards Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin: 20px 0;
    }
    .stat-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 18px;
    }
    .stat-label {
      font-size: 0.76em;
      text-transform: uppercase;
      font-weight: 800;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }
    .stat-value {
      font-size: 2.2em;
      font-weight: 800;
      margin-bottom: 4px;
    }
    .stat-subtext {
      font-size: 0.82em;
      color: var(--text-muted);
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      background: var(--card-bg);
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--card-border);
    }
    th, td {
      padding: 12px 16px;
      text-align: left;
      font-size: 0.9em;
      border-bottom: 1px solid var(--card-border);
    }
    th {
      background: rgba(255, 255, 255, 0.04);
      font-weight: 750;
      color: var(--text-muted);
      text-transform: uppercase;
      font-size: 0.76em;
      letter-spacing: 0.08em;
    }
    [data-theme="light"] th {
      background: rgba(0, 0, 0, 0.03);
    }
    tr:last-child td { border-bottom: none; }

    /* Lists */
    ol, ul {
      padding-left: 24px;
      margin: 12px 0;
    }
    li {
      margin-bottom: 10px;
      font-size: 0.95em;
      line-height: 1.65;
    }

    /* Foldable Quiz Items */
    .quiz-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      margin-bottom: 12px;
      overflow: hidden;
    }
    .quiz-header {
      padding: 14px 18px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.02);
    }
    .quiz-header:hover {
      background: rgba(255, 255, 255, 0.05);
    }
    .quiz-body {
      padding: 16px 18px;
      border-top: 1px solid var(--card-border);
      font-size: 0.92em;
      color: var(--text-muted);
      display: none;
      background: rgba(0, 0, 0, 0.15);
    }
    [data-theme="light"] .quiz-body {
      background: rgba(0, 0, 0, 0.02);
    }
    .quiz-body.show {
      display: block;
    }

    /* Images */
    .figure-container {
      margin: 20px 0;
      text-align: center;
    }
    .figure-img {
      max-width: 100%;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
    }

    /* Bottom Navigation Controls */
    .day-nav-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
    }
  </style>
</head>
<body data-theme="dark">

  <!-- Top Header -->
  <header>
    <div class="brand">
      <span class="brand-logo">📊</span>
      <div>
        <div class="brand-title">Downtown San Diego Homelessness</div>
        <div class="brand-subtitle">Executive Study Curriculum & Defense Cockpit</div>
      </div>
    </div>
    <div class="header-actions">
      <a href="https://downtown-sd-homelessness.streamlit.app" target="_blank" class="btn btn-green">🖥️ Live Streamlit Dashboard</a>
      <a href="Assignment9_StrategicSynthesis.html" target="_blank" class="btn btn-cyan">📑 Presentation Deck</a>
      <button class="btn btn-toggle" onclick="toggleTheme()" title="Toggle Light/Dark Theme">🌗</button>
    </div>
  </header>

  <div class="app-container">
    <!-- Sidebar Navigation -->
    <nav class="sidebar">
      <div class="nav-group-title">Executive Command</div>
      <div class="nav-item active" onclick="showTab('tab-00')">
        <span>🎯 Command Center</span>
        <span class="badge" style="background:var(--cyan-dim); color:var(--cyan);">Overview</span>
      </div>

      <div class="nav-group-title">9-Day Study Curriculum</div>
      <div class="nav-item" onclick="showTab('tab-01')">
        <span>Day 01 · Executive Narrative</span>
        <span class="badge" style="background:var(--cyan-dim); color:var(--cyan);">Core</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-02')">
        <span>Day 02 · Data Forensics & QA</span>
        <span class="badge" style="background:var(--purple-dim); color:var(--purple);">QA</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-03')">
        <span>Day 03 · GIS & Balanced Panel</span>
        <span class="badge" style="background:var(--green-dim); color:var(--green);">GIS</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-04')">
        <span>Day 04 · Debunking Seasonality</span>
        <span class="badge" style="background:var(--amber-dim); color:var(--amber);">Econ</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-05')">
        <span>Day 05 · Breaks & 120m Shift</span>
        <span class="badge" style="background:var(--red-dim); color:var(--red);">Spatial</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-06')">
        <span>Day 06 · 12-Month ML Forecast</span>
        <span class="badge" style="background:var(--blue-dim); color:var(--blue);">ML</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-07')">
        <span>Day 07 · County Model & 4 Rules</span>
        <span class="badge" style="background:var(--green-dim); color:var(--green);">Policy</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-08')">
        <span>Day 08 · Multi-Source & ML Truths</span>
        <span class="badge" style="background:var(--red-dim); color:var(--red);">Ablation</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-09')">
        <span>Day 09 · Dual-Layer Surveillance</span>
        <span class="badge" style="background:var(--cyan-dim); color:var(--cyan);">Live</span>
      </div>

      <div class="nav-group-title">Presentation & Defense</div>
      <div class="nav-item" onclick="showTab('tab-script')">
        <span>🎙️ 14-Slide Speaker Script</span>
        <span class="badge" style="background:var(--purple-dim); color:var(--purple);">Speech</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-defense')">
        <span>⚔️ Defense Playbook (Top 10)</span>
        <span class="badge" style="background:var(--red-dim); color:var(--red);">Defense</span>
      </div>
      <div class="nav-item" onclick="showTab('tab-cheat')">
        <span>🧮 1-Page Battle Card</span>
        <span class="badge" style="background:var(--amber-dim); color:var(--amber);">Quick</span>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="content">

      <!-- TAB 00: COMMAND CENTER -->
      <section id="tab-00" class="tab-pane active">
        <div class="day-badge-header">🎯 EXECUTIVE SYNTHESIS COCKPIT</div>
        <h1 class="day-title">Downtown San Diego Homelessness Command Center</h1>
        <div class="day-subtitle">Lead Analyst: <strong>Kyaw Soe Lwin</strong> (@CapMorningStar) · Project Lead: <strong>Adir Mancebo Jr.</strong></div>

        <!-- 4 Stats -->
        <div class="stats-grid">
          <div class="stat-card" style="border-left: 4px solid var(--red);">
            <div class="stat-label">Historic Crisis Peak</div>
            <div class="stat-value" style="color:var(--red);">2,103</div>
            <div class="stat-subtext">May 2023 pre-ordinance record</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--green);">
            <div class="stat-label">Enforcement Contraction</div>
            <div class="stat-value" style="color:var(--green);">851</div>
            <div class="stat-subtext">-59.5% drop (Jan 2025 paired)</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--cyan);">
            <div class="stat-label">Centroid Migration</div>
            <div class="stat-value" style="color:var(--cyan);">120.4m</div>
            <div class="stat-subtext">Bearing 160.1° SSE to industrial buffer</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--amber);">
            <div class="stat-label">County Estimate</div>
            <div class="stat-value" style="color:var(--amber);">5,900</div>
            <div class="stat-subtext">95% Interval: [3,900 to 8,000]</div>
          </div>
        </div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">🛑 The 4 Mandatory Public Communication Rules</div>
          <ul>
            <li><strong>Rule 1 · No Raw Single-Point Precision:</strong> Never cite unrounded estimates like <em>"5,921"</em>. Single-point precision damages empirical credibility.</li>
            <li><strong>Rule 2 · Mandate Rounding to Nearest 100:</strong> Always report the headline total rounded to the nearest hundred: quote <strong>"about 5,900"</strong>.</li>
            <li><strong>Rule 3 · Always State 95% Prediction Interval:</strong> Always pair with the calibrated range: <strong>"5,900 [3,900 to 8,000]"</strong> (±2,050).</li>
            <li><strong>Rule 4 · Mandatory Policy Regime Disclosure:</strong> Explicitly state that the estimate structurally assumes post-July 2023 camping ordinance enforcement remains in place.</li>
          </ul>
        </div>

        <div class="card card-cyan">
          <div class="card-title" style="color:var(--cyan);">📚 9-Day Executive Learning Roadmap</div>
          <table>
            <thead>
              <tr><th>Day</th><th>Topic</th><th>Core Takeaway</th><th>Mental Model Analogy</th></tr>
            </thead>
            <tbody>
              <tr><td>Day 01</td><td>Executive Narrative</td><td>-59.5% downtown drop vs 6,110 county record</td><td>Draining the pond while the watershed floods</td></tr>
              <tr><td>Day 02</td><td>Data Forensics & QA</td><td>45-cell audit (97.8%), 2 archival fixes, multiplier impact</td><td>Changing the scale vs. true weight loss</td></tr>
              <tr><td>Day 03</td><td>GIS Grid & Balanced Panel</td><td>+121 blocks in 2022 accounted for ~1/3 of peak</td><td>Expanding the garden fence vs. fruit yield</td></tr>
              <tr><td>Day 04</td><td>Debunking Seasonality</td><td>Kruskal-Wallis H=2.66, p=0.995 (0 seasonality)</td><td>Surface ripples vs. macro tidal waves</td></tr>
              <tr><td>Day 05</td><td>Breaks & Centroid Shift</td><td>March 2020 break; 120.4m SSE southward drift</td><td>Thermal imaging & shifting fire perimeter</td></tr>
              <tr><td>Day 06</td><td>12-Month ML Forecasting</td><td>XGBoost vs Holt-Winters tie (~38% MAPE)</td><td>Short-term radar vs. 1-year almanac</td></tr>
              <tr><td>Day 07</td><td>County Policy Model</td><td>Policy Regime OLS (R²=0.504, 5,900 [3,900–8,000])</td><td>Estimating statewide harvest from one stall</td></tr>
              <tr><td>Day 08</td><td>Multi-Source & ML Truths</td><td>Lag-1 persistence beat complex ensemble (MAE 119.6 vs 248.0)</td><td>Intricate clockwork vs. simple hourglass</td></tr>
              <tr><td>Day 09</td><td>Dual-Layer Surveillance</td><td>Shewhart ±3σ + Tabular CUSUM (100% crisis detection)</td><td>Smoke detector & thermal sensor dual alarm</td></tr>
            </tbody>
          </table>
        </div>

        <div class="day-nav-footer">
          <div></div>
          <button class="btn btn-cyan" onclick="showTab('tab-01')">Start Day 01 →</button>
        </div>
      </section>

      <!-- TAB 01: DAY 01 -->
      <section id="tab-01" class="tab-pane">
        <div class="day-badge-header">📚 DAY 01 · 15-20 MIN</div>
        <h1 class="day-title">The Executive Narrative & The 4 Core Truths</h1>
        <div class="day-subtitle">Master the macro storyline, regional divergence, and The 4 Mandatory Public Communication Rules.</div>

        <div class="card card-cyan">
          <div class="card-title" style="color:var(--cyan);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>Historic Peak to Post-Ordinance Drop:</strong> In Downtown San Diego, the unsheltered population reached a historic peak of <strong>2,103</strong> in May 2023. Following the enforcement of the Camping Ordinance, the count dropped dramatically to <strong>851 (-59.5%)</strong> by January 2025.</li>
            <li><strong>Regional Divergence:</strong> Even though Downtown numbers plummeted, the annual Point-in-Time (PIT) census for the entire San Diego County surged to a record high of <strong>6,110</strong> in 2024.</li>
            <li><strong>Strategic Policy Insight:</strong> The spatial and time-series data strongly suggest that the decline in Downtown is not a true net reduction of homelessness. Instead, it represents <strong>Regional Displacement</strong>—populations relocating into riverbeds, canyons, and adjacent peripheral neighborhoods.</li>
          </ol>
        </div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">💡 Plain-Language Analogy: "Draining the Pond while the Watershed Floods"</div>
          <p>Think of Downtown San Diego as a small pond located in the middle of a massive river basin. The Camping Ordinance acted like a giant water pump, forcefully draining the water out of that specific pond (reducing the Downtown count to 851). However, the surrounding river basin is still actively flooding (with the countywide count surging to a record 6,110). Therefore, the data clearly proves that draining the pond didn't actually solve the flood—it simply pushed the water out into the surrounding floodplains. This is the essence of <strong>Regional Displacement</strong>.</p>
        </div>

        <div class="card card-amber">
          <div class="card-title" style="color:var(--amber);">📢 The 4 Mandatory Public Communication Rules</div>
          <ul>
            <li><strong>Rule 1 (No Raw Single-Point):</strong> Never cite unrounded point estimates (citing 5,921 is an empirical error).</li>
            <li><strong>Rule 2 (Round to Hundreds):</strong> Always report the county estimate rounded to the nearest hundred: <strong>5,900</strong>.</li>
            <li><strong>Rule 3 (Always State the Interval):</strong> Always pair with the 95% prediction interval: <strong>[3,900 to 8,000]</strong>.</li>
            <li><strong>Rule 4 (Policy Regime Caveat):</strong> Explicitly state that the model assumes the post-ordinance displacement regime continues.</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Why is it an empirical error to claim "Downtown counts fell to 851 in December 2025"?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> 851 is the January 2025 paired count used to match the annual RTFH Point-in-Time census. The latest published count in December 2025 was <strong>985.4</strong>. Mixing these dates damages technical credibility in front of Adir.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Does our data prove the July 2023 Camping Ordinance CAUSED the countywide surge?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> No! We prove empirical <em>macro divergence</em> and temporal correlation. Anonymous block headcounts cannot track individuals across jurisdictional boundaries. Always emphasize this distinction to display empirical humility.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-00')">← Command Center</button>
          <button class="btn btn-cyan" onclick="showTab('tab-02')">Next: Day 02 (Data Forensics) →</button>
        </div>
      </section>

      <!-- TAB 02: DAY 02 -->
      <section id="tab-02" class="tab-pane">
        <div class="day-badge-header">📚 DAY 02 · 15-20 MIN</div>
        <h1 class="day-title">Data Forensics, QA Audits & Multiplier Math</h1>
        <div class="day-subtitle">Understand the 45-cell audit, source error fixes, and why multiplier changes did not drive real trends.</div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>PDF Source Audit:</strong> A rigorous random audit of 45 data cells from original monthly PDF reports verified <strong>97.8% transcription accuracy</strong> (44 of 45 cells matched perfectly).</li>
            <li><strong>Correction of 2 Discovered Archival Errors:</strong> Identified and corrected two specific archival defects: a copy-paste error in 2019 East Village sub-quadrants (NE, NW, SE, SW data copied from 2020) and a February 2018 City Center typo (10 tents recorded instead of 100). *(Neither error impacted headline downtown totals).*</li>
            <li><strong>Minimal Impact of Multiplier Regimes:</strong> Recalibrating tent and vehicle multipliers across 4 historical regimes shifted counts by only <strong>-3.6% to +0.7%</strong>—proving mathematically that historical surges and contractions were driven by real physical conditions, not changes in counting methodology.</li>
          </ol>
        </div>

        <div class="card">
          <div class="card-title">The 4 Multiplier Regimes in History</div>
          <table>
            <thead>
              <tr><th>Regime Name</th><th>Active Period</th><th>Tent Multiplier</th><th>Vehicle Multiplier</th><th>Governance Reason</th></tr>
            </thead>
            <tbody>
              <tr><td><strong>PRE2017</strong></td><td>Jan 2017 – Mar 2017</td><td>2.00×</td><td>2.00×</td><td>Legacy DSDP field counting guidelines</td></tr>
              <tr><td><strong>APR2017</strong></td><td>Apr 2017 – Apr 2018</td><td>1.75×</td><td>1.66×</td><td>First empirical survey recalibration</td></tr>
              <tr><td><strong>MAY2018</strong></td><td>May 2018 – Dec 2019</td><td>1.75×</td><td>2.03×</td><td>Updated empirical occupancy field survey</td></tr>
              <tr><td><strong>POST2020</strong></td><td>Jan 2020 – Present</td><td>1.75×</td><td>2.03×</td><td>Current DSDP operational standard (HUD dropped to 1.0)</td></tr>
            </tbody>
          </table>
        </div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">💡 Plain-Language Analogy: "Changing the Scale vs. True Weight Loss"</div>
          <p>Imagine a merchant switches from an older mechanical weighing scale to a digital one. The new scale might read slightly higher or lower by a tiny fraction (<strong>-3.6% to +0.7%</strong> due to calibration). However, if the entire bag of grain suddenly loses <strong>over 20% of its volume</strong>, that depletion cannot be blamed on the scale calibration—grain is physically leaving the warehouse! In our analysis, on-the-ground fluctuations dwarfed multiplier adjustments by an order of magnitude.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Did the 2019 East Village quadrant copy-paste error distort neighborhood headline totals?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <strong>No.</strong> It only affected the internal sub-quadrant allocation (NE, NW, SE, SW) within East Village. The total neighborhood counts and headline downtown figures remained 100% accurate.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Why is the Constant-Methodology Hybrid series better than a purely data-derived adjustment?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> The Constant-Methodology Hybrid series exhibits a pre-2020 transition gap of only <strong>+0.10%</strong>, whereas a purely data-derived adjustment artificially inflates historical baseline counts by <strong>+5.1%</strong>, introducing severe distortions into long-term trend analysis.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-01')">← Day 01</button>
          <button class="btn btn-cyan" onclick="showTab('tab-03')">Next: Day 03 (GIS Grid) →</button>
        </div>
      </section>

      <!-- TAB 03: DAY 03 -->
      <section id="tab-03" class="tab-pane">
        <div class="day-badge-header">📚 DAY 03 · 15-20 MIN</div>
        <h1 class="day-title">GIS Block Grid, Footprint Expansion & Balanced Panels</h1>
        <div class="day-subtitle">Understand the 2022 boundary expansion (+121 blocks) and why the balanced 261-block panel is essential.</div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>The Boundary Expansion Distortion:</strong> In January 2022, DSDP expanded its monthly survey boundary from 261 blocks to 382 blocks (<strong>adding 121 peripheral blocks</strong> across Golden Hill, Barrio Logan, and Sherman Heights).</li>
            <li><strong>The "Wedge" Inflation Effect:</strong> At the May 2023 crisis peak, these 121 added peripheral blocks accounted for <strong>32.8% of the total downtown count (641 individuals)</strong>. Without isolating this boundary expansion, an analyst would falsely inflate the downtown core crisis by nearly one-third.</li>
            <li><strong>The Empirical Solution (Balanced 261-Block Panel):</strong> By isolating the consistent 261 core blocks across all years, we prove that homelessness still surged by <strong>+71%</strong> during that same period. This confirms that the crisis was authentically severe and not merely an administrative boundary artifact.</li>
          </ol>
        </div>

        <div class="figure-container">
          <img src="slide_assets/task93_footprint_wedge.png" alt="Footprint Wedge Chart" class="figure-img" onerror="this.style.display='none'">
        </div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">💡 Plain-Language Analogy: "Expanding the Garden Fence vs. Fruit Production"</div>
          <p>Imagine last year you harvested 100 apples from the trees inside your garden fence. This year, you expand your fence outward to enclose three neighboring vacant lots, and you harvest 200 apples. Did your apple trees suddenly become twice as productive, or did you simply expand your collection area? By counting apples from <strong>only the original trees inside the old fence line</strong> (our <strong>Balanced 261-Block Panel</strong>), we found an authentic <strong>+71% increase</strong> in the core. Therefore, both are true: the fence expansion added 32.8%, but the core still surged significantly.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: How much of the January 2023 count came from the 121 added blocks?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Exactly <strong>32.8% (640.6 individuals)</strong>. Failing to control for this boundary change leads analysts to overestimate the downtown core surge by roughly one-third.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Which dataset must be used for longitudinal block-level spatial comparisons?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <code>data/BlockPanel_Balanced_261.csv</code>. Never use the unadjusted 382-block pool for pre-2022 vs post-2022 block comparisons.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-02')">← Day 02</button>
          <button class="btn btn-cyan" onclick="showTab('tab-04')">Next: Day 04 (Seasonality) →</button>
        </div>
      </section>

      <!-- TAB 04: DAY 04 -->
      <section id="tab-04" class="tab-pane">
        <div class="day-badge-header">📚 DAY 04 · 15-20 MIN</div>
        <h1 class="day-title">Debunking Seasonality & Time-Series Stationarity</h1>
        <div class="day-subtitle">Prove that homelessness is governed by macro policy and economic shifts, not weather cycles.</div>

        <div class="card card-amber">
          <div class="card-title" style="color:var(--amber);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>The Conventional Myth:</strong> Public perception and conventional civic assumptions hold that cold winter weather pushes people indoors and mild summer weather increases unsheltered counts (weather-driven seasonality).</li>
            <li><strong>The Mathematical Refutation:</strong> Non-parametric Kruskal-Wallis tests (df = 11) prove that <strong>8 of the 9 downtown series show zero statistically significant seasonality</strong> (Overall Downtown: <strong>H = 2.66, p = 0.995</strong>). STL time-series decomposition confirmed a seasonal strength of only <strong>0.07</strong> (accounting for less than 5% of variance).</li>
            <li><strong>Strategic Policy Recommendation:</strong> Municipalities should discontinue seasonal surge budgeting and stop opening reactive winter-only shelters; funding must be redirected into continuous, year-round capacity.</li>
          </ol>
        </div>

        <div class="card">
          <div class="card-title">Kruskal-Wallis Non-Parametric Seasonality Results (df = 11)</div>
          <table>
            <thead>
              <tr><th>Series / Neighborhood</th><th>Test Statistic (H)</th><th>p-value</th><th>Significant Seasonality?</th><th>Operational Takeaway</th></tr>
            </thead>
            <tbody>
              <tr><td><strong>Overall Downtown Footprint</strong></td><td><strong>2.66</strong></td><td><strong>0.995</strong></td><td>❌ <strong>No (Zero Seasonality)</strong></td><td>Discontinue seasonal budget swings</td></tr>
              <tr><td><strong>East Village</strong></td><td>14.16</td><td>0.224</td><td>❌ <strong>No</strong></td><td>Permanent year-round beds needed</td></tr>
              <tr><td><strong>City Center (Core)</strong></td><td>4.86</td><td>0.938</td><td>❌ <strong>No</strong></td><td>Stable month-to-month patterns</td></tr>
              <tr><td><strong>Marina</strong></td><td>19.88</td><td><strong>0.047</strong></td><td>⚠️ <strong>Borderline</strong></td><td>Driven by Comic-Con / event sweeps</td></tr>
            </tbody>
          </table>
        </div>

        <div class="card card-amber">
          <div class="card-title" style="color:var(--amber);">💡 Plain-Language Analogy: "Surface Ripples vs. Macro Tidal Waves"</div>
          <p>Month-to-month weather changes are like tiny surface ripples on the water (seasonal strength of 0.07—virtually negligible). The forces that actually move the water level are deep tectonic tidal waves: COVID-19 emergency hotel sheltering, eviction moratorium rollbacks, and the July 2023 Unsafe Camping Ordinance. Worrying about seasonal winter shelter spikes while ignoring long-term policy shifts is like staring at 2-inch ripples while ignoring a 10-foot tidal surge.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Why did Marina show borderline seasonality (p = 0.047)?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Marina hosts the San Diego Convention Center. Every July, municipal sweeps clear the perimeter ahead of massive international events like <strong>San Diego Comic-Con</strong>. Parametric ANOVA is non-significant (p = 0.162). This is an artificial enforcement artifact, not organic weather migration.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: What was the result of stationarity testing (ADF & KPSS)?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Raw series levels were non-stationary across all 9 series. However, after taking the <strong>first difference (Δy_t = y_t - y_{t-1})</strong>, all 9 series achieved full stationarity, enabling valid ARIMA and econometric modeling.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-03')">← Day 03</button>
          <button class="btn btn-cyan" onclick="showTab('tab-05')">Next: Day 05 (Hotspots & Shift) →</button>
        </div>
      </section>

      <!-- TAB 05: DAY 05 -->
      <section id="tab-05" class="tab-pane">
        <div class="day-badge-header">📚 DAY 05 · 15-20 MIN</div>
        <h1 class="day-title">Structural Breaks, Policy Shifts & Spatial Hotspots</h1>
        <div class="day-subtitle">Understand the March 2020 COVID break, Getis-Ord Gi* clusters, and the 120.4m southward centroid shift.</div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>The COVID Structural Pivot (Chow Test):</strong> The onset of COVID-19 in March 2020 caused a statistically significant structural break (p &lt; 0.05) in 7 of the 8 analyzed time series. *(Crucial Defense Caveat: The July 2023 Camping Ordinance was not evaluated as a candidate break date in Task 4.3).*</li>
            <li><strong>The Persistent Hotspot Epicenter:</strong> Getis-Ord Gi* spatial analysis across 12 temporal benchmark dates identified <strong>16th St & Imperial Ave</strong> as the #1 persistent hotspot (active in 75% of periods). All top 10 persistent hotspots are concentrated in Southeast East Village.</li>
            <li><strong>The 120.4-Meter Southward Migration Vector:</strong> Comparing 2018–2020 to 2022–2025 reveals that the count-weighted centroid shifted <strong>120.4 meters bearing 160.1° South-South-East (SSE)</strong> away from the commercial core toward industrial and transit buffers.</li>
          </ol>
        </div>

        <div class="figure-container">
          <img src="slide_assets/task93_hotspot_migration.png" alt="Hotspot Migration Chart" class="figure-img" onerror="this.style.display='none'">
        </div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">💡 Plain-Language Analogy: "Thermal Imaging & Shifting Fire Perimeter"</div>
          <p>Hotspot spatial analysis (Getis-Ord Gi*) is like flying a drone with an infrared thermal camera over the city to detect the hottest heat signatures. The intersection of 16th & Imperial has consistently burned the hottest across nearly a decade. When we report that the centroid moved <strong>120.4 meters southward</strong>, it means the collective center of mass of that fire perimeter drifted toward the industrial rail corridor and freeway underpasses. It describes aggregate cluster migration, not personal GPS tracking of specific individuals.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Did Task 4.3 test a Chow structural break for the July 2023 Camping Ordinance?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <strong>NO!</strong> Task 4.3 only tested April 2017, May 2018, and March 2020. Never cite an invented F-statistic for July 2023. Transparently acknowledge: <em>"July 2023 was not tested under Task 4.3 Chow candidate dates; evaluating it formally is an immediate next step."</em>
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: What is the exact bearing and distance of the centroid shift?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Distance is <strong>120.4 meters</strong> bearing <strong>160.1° South-South-East (SSE)</strong>. It reflects the weighted center of gravity shifting away from Gaslamp and Core toward the industrial fringe.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-04')">← Day 04</button>
          <button class="btn btn-cyan" onclick="showTab('tab-06')">Next: Day 06 (ML Forecasting) →</button>
        </div>
      </section>

      <!-- TAB 06: DAY 06 -->
      <section id="tab-06" class="tab-pane">
        <div class="day-badge-header">📚 DAY 06 · 15-20 MIN</div>
        <h1 class="day-title">12-Month Predictive Modeling & Walk-Forward CV</h1>
        <div class="day-subtitle">Understand walk-forward validation, the XGBoost/Holt-Winters statistical tie, and prospective 2026 scenarios.</div>

        <div class="card card-blue">
          <div class="card-title" style="color:var(--blue);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>Leak-Free Walk-Forward Validation:</strong> To eliminate temporal data leakage, five competing model families were evaluated across 5 expanding-window folds.</li>
            <li><strong>The 12-Month Statistical Tie:</strong> At a 12-month horizon, XGBoost (<strong>38.3%</strong>), Holt-Winters (<strong>38.4%</strong>), and SARIMA (<strong>39.6%</strong>) are in a <strong>mathematical statistical tie</strong> given fold standard deviations of 26%–36%. XGBoost was selected as nominal champion because it achieved a superior fit on the 2025 hold-out evaluation (<strong>8.5% MAPE</strong>).</li>
            <li><strong>Prophet's Structural Failure:</strong> Meta's Prophet model suffered severe catastrophic overfitting (<strong>64.2% CV MAPE</strong>), assuming the historical upward climb would continue and failing to account for the abrupt enforcement cliff.</li>
          </ol>
        </div>

        <div class="figure-container">
          <img src="slide_assets/task93_forecast_2026.png" alt="2026 Forecast Scenarios" class="figure-img" onerror="this.style.display='none'">
        </div>

        <div class="card card-blue">
          <div class="card-title" style="color:var(--blue);">💡 Plain-Language Analogy: "Short-Term Radar vs. 1-Year Almanac"</div>
          <p>Predicting tomorrow's rainfall (<strong>short-term 1-month horizon</strong>) is highly accurate with specialized instruments (SARIMA achieves 5.4% MAPE). However, predicting precipitation a full year in advance (<strong>12-month horizon</strong>) carries immense macroeconomic noise. At that distance, an advanced AI algorithm (<strong>XGBoost</strong>) and a traditional classical trend line (<strong>Holt-Winters</strong>) reach a virtual statistical tie at ~38% error. Recognizing and admitting this tie to stakeholders demonstrates rigorous statistical honesty rather than blind algorithmic bias.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Can Kyaw claim XGBoost is statistically superior to Holt-Winters at 12 months?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <strong>NO!</strong> The fold standard deviations are 26–28 percentage points, making a 0.1% difference a statistical tie. XGBoost was chosen due to its lower numerical mean and superior 2025 hold-out performance (8.5%). Always transparently admit this tie.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Are the optimistic (-24%) and pessimistic (+26%) scenarios structural forecasts?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> No. They are fixed compound stress-test boundaries (-2.0% and +2.2% monthly) designed for municipal shelter capacity planning, not causal macroeconomic simulations.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-05')">← Day 05</button>
          <button class="btn btn-cyan" onclick="showTab('tab-07')">Next: Day 07 (County Model) →</button>
        </div>
      </section>

      <!-- TAB 07: DAY 07 -->
      <section id="tab-07" class="tab-pane">
        <div class="day-badge-header">📚 DAY 07 · 15-20 MIN</div>
        <h1 class="day-title">County Estimation, Policy Regimes & Public Communication</h1>
        <div class="day-subtitle">Master the Policy Regime OLS model (R²=0.504), the N=8 power caveat, and The 4 Mandatory Rules.</div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>Low Sample Size & Statistical Power (N=8):</strong> Because the HUD PIT count occurs only once annually in late January, only 8 paired observation years exist (2017–2025). This yields a statistical power of only <strong>~23%</strong>, demanding deep empirical caution.</li>
            <li><strong>Model Specification & True Fit:</strong> Using the Policy Regime OLS model (Y = 4,513.26 + 0.1859*X + 1,225.04*D_post), the true regression fit is <strong>R² = 0.504</strong> *(0.964 is the ANOVA effect size η², not regression R²)*. The calibrated 2025 county estimate is <strong>5,900 [3,900 to 8,000]</strong>.</li>
            <li><strong>The 4 Mandatory Public Communication Rules:</strong> Due to wide prediction intervals (±2,050), public reporting must strictly follow the 4 rules: no raw single-point precision, round to hundreds, always state the 95% interval, and disclose the policy regime caveat.</li>
          </ol>
        </div>

        <div class="figure-container">
          <img src="slide_assets/task93_regional_divergence.png" alt="Regional Divergence" class="figure-img" onerror="this.style.display='none'">
        </div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">💡 Plain-Language Analogy: "Estimating Statewide Harvest from One Market Stall"</div>
          <p>Estimating the entire countywide homeless population from Downtown counts is like trying to forecast total statewide crop production by observing transactions at a single downtown wholesale stall—with only 8 historical data points. Because you only have 8 years of data, claiming you know the exact county total down to a single person (<strong>"5,921 individuals"</strong>) is statistically irresponsible. A professional analyst reports an honest, rounded range: <strong>"about 5,900 individuals [between 3,900 and 8,000]"</strong>.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: What is the true R² of the County estimation regression model?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Exactly <strong>0.504</strong>. The number <strong>0.964</strong> is the η² effect size from the One-Way ANOVA test that proved the downtown-to-county ratio collapsed over time. Conflating these two numbers in front of Adir is a major statistical trap.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Why does changing downtown counts from 851 to 985 only shift the estimate by 25 people?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> The slope coefficient (β₁ = 0.1859) is very flat and statistically non-significant (p = 0.78). The model is anchored primarily by the baseline constant (4,513) and post-ordinance structural displacement term (+1,225).
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-06')">← Day 06</button>
          <button class="btn btn-cyan" onclick="showTab('tab-08')">Next: Day 08 (Multi-Source & ML) →</button>
        </div>
      </section>

      <!-- TAB 08: DAY 08 -->
      <section id="tab-08" class="tab-pane">
        <div class="day-badge-header">📚 DAY 08 · 15-20 MIN</div>
        <h1 class="day-title">Multi-Source Systems & ML Realities</h1>
        <div class="day-subtitle">Understand feature ablation, shelter placeholder caveats, and why simple lag-1 persistence beat the complex ensemble.</div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>Simple Persistence Outperformed Complex Ensembles:</strong> Despite engineering 68 external features across an advanced stacked ensemble (BSTS, MLP, LightGBM), the simple <strong>Lag-1 Naive Persistence baseline (y_t = y_{t-1}) decisively outperformed the machine learning ensemble</strong> (Lag-1 MAE <strong>119.6</strong> vs Ensemble MAE <strong>248.0</strong>).</li>
            <li><strong>Feature Ablation Findings:</strong> In small-sample regimes (N ≈ 90), adding voluminous external signals (weather, 311 service requests) actually degraded LightGBM accuracy by <strong>1.6%</strong>, injecting noise rather than predictive power.</li>
            <li><strong>Shelter Capacity Disclaimer:</strong> Shelter bed capacity figures were timeline-approximated operational placeholders, not official HUD/HIC administrative bed registries.</li>
          </ol>
        </div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">💡 Plain-Language Analogy: "Intricate Watch Movement vs. Simple Hourglass"</div>
          <p>We constructed a hyper-intricate machine with 68 gears and springs (our <strong>Stacked ML Ensemble</strong>) to predict next month's unsheltered numbers. Yet, a simple hourglass (<strong>Lag-1 baseline</strong>: <em>"next month will look almost exactly like this month"</em>) decisively beat the machine. In systems with heavy serial inertia (AR(1) > 0.85), forcing 68 noisy external variables into small sample sizes confuses the algorithm. Acknowledging this <strong>negative result</strong> demonstrates deep statistical maturity and intellectual honesty.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: Is the lag-1 baseline victory considered a failure of the machine learning work?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <strong>Absolutely not.</strong> High autoregressive persistence (AR(1) > 0.85) mathematically guarantees that persistence is near-optimal. Demonstrating this empirically and publishing the negative result proves academic rigor and scientific integrity over algorithmic vanity.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: What were the NNLS stacking weights for the ensemble?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> <strong>BSTS = 0.812</strong>, <strong>MLP = 0.188</strong>, and <strong>LightGBM = 0.000</strong>. LightGBM was completely zeroed out by Non-Negative Least Squares optimization.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-07')">← Day 07</button>
          <button class="btn btn-cyan" onclick="showTab('tab-09')">Next: Day 09 (Surveillance & Streamlit) →</button>
        </div>
      </section>

      <!-- TAB 09: DAY 09 -->
      <section id="tab-09" class="tab-pane">
        <div class="day-badge-header">📚 DAY 09 · 15-20 MIN</div>
        <h1 class="day-title">Dual-Layer Surveillance & Live Streamlit Dashboard</h1>
        <div class="day-subtitle">Understand statistical quality control (Shewhart + CUSUM), 46 passing tests, and interactive operational tooling.</div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">⚡ Frank & Direct Summary (Executive Talking Points)</div>
          <ol>
            <li><strong>Dual-Layer Anomaly Surveillance:</strong> Combines a <strong>Shewhart Control Chart (±3σ)</strong> for acute flash spikes with a <strong>Tabular CUSUM (k=0.5, h=4.0)</strong> algorithm to catch insidious, low-amplitude structural drift.</li>
            <li><strong>100% Historical Crisis Detection:</strong> Successfully flagged all 4 major historical crisis events in the 9-year record (<strong>Event-level sensitivity: 100%</strong>, False Positive Rate: 7.4%).</li>
            <li><strong>Production-Ready Live Dashboard:</strong> Built and deployed a full 7-tab Streamlit application passing all <strong>46 out of 46 automated unit tests</strong>, operating under a sub-2-second SLA.</li>
          </ol>
        </div>

        <div class="card card-green">
          <div class="card-title" style="color:var(--green);">💡 Plain-Language Analogy: "Dual Fire Alarms: Smoke Detector & Thermal Sensor"</div>
          <p>Our dual-layer surveillance is like protecting a building with two specialized alarms: 
          1) <strong>The Smoke Alarm (Shewhart ±3σ):</strong> Screams immediately if a sudden, massive explosion of smoke fills the room (an acute monthly flash surge). 
          2) <strong>The Thermal Sensor (Tabular CUSUM):</strong> Silently monitors for a slow, creeping temperature rise behind the drywall (a subtle month-after-month baseline creep). 
          By running both algorithms simultaneously, the city has early warning for both sudden emergency surges and gradual policy displacement.</p>
        </div>

        <div class="card">
          <div class="card-title">❓ Self-Test Knowledge Checkpoints</div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: What is the status of the automated unit test suite?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Exactly <strong>46 out of 46 Pytest unit tests pass</strong> with zero failures, covering mathematical models, data loaders, conformal thresholds, and anomaly alerting logic.
            </div>
          </div>
          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: What is the difference between event-level detection and month-level sensitivity?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body">
              <strong>Answer:</strong> Event-level is <strong>100%</strong> (all 4 distinct historical crisis periods were flagged at least once). Month-level sensitivity across all individual crisis months is <strong>45.8%</strong>, because alerts reset as new higher baselines are absorbed.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-08')">← Day 08</button>
          <button class="btn btn-cyan" onclick="showTab('tab-script')">Next: 14-Slide Speaker Script →</button>
        </div>
      </section>

      <!-- TAB SCRIPT: 14-SLIDE SPEAKER SCRIPT -->
      <section id="tab-script" class="tab-pane">
        <div class="day-badge-header">🎙️ PRESENTATION DELIVERY SUITE</div>
        <h1 class="day-title">14-Slide Executive Speaker Script</h1>
        <div class="day-subtitle">Minute-by-minute speaking script, click prompts, and delivery cues for your executive briefing with Adir Mancebo Jr.</div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">Slide 01: Title Slide & Governance (0:00 - 1:30)</div>
          <p><strong>Executive Mental Cue:</strong> <em>"Make direct eye contact and speak with calm authority. Ground the presentation immediately on 104 published counts and 382 GIS blocks—the most comprehensive longitudinal analysis ever conducted on this dataset."</em></p>
          <blockquote style="margin: 12px 0; padding: 12px; background: rgba(0,0,0,0.2); border-left: 3px solid var(--purple); font-style: italic;">
            "Good morning Adir and team. Today I present our comprehensive 9-year longitudinal synthesis of unsheltered homelessness in Downtown San Diego, covering 2017 through 2026. This analysis synthesizes 104 published field counts across 382 GIS blocks, combined with annual countywide PIT censuses. Our objective today is to cut through civic intuition using spatial econometrics, 5-fold cross-validation, and strict adherence to The 4 Public Communication Rules to deliver an evidence-based roadmap for municipal leadership."
          </blockquote>
        </div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">Slide 02: Executive KPI Dashboard (1:30 - 3:30) -- CORE HOOK</div>
          <p><strong>Executive Mental Cue:</strong> <em>"These 4 numbers are your primary rhetorical anchors (2,103 peak -> 851 contraction -> 54% East Village -> 120m shift). Emphasize clearly: downtown dropping by ~60% while the county surged to a record 6,110 is regional displacement, not resolution."</em></p>
          <blockquote style="margin: 12px 0; padding: 12px; background: rgba(0,0,0,0.2); border-left: 3px solid var(--purple); font-style: italic;">
            "The crisis in numbers: Downtown peaked at a historic 2,103 individuals in May 2023. Following the city's Unsafe Camping Ordinance, we observed a 59.5% net contraction, stabilizing around 851 individuals in early 2025.<br><br>
            However, we must frame this reality transparently: while downtown numbers contracted, the countywide unsheltered census reached a historic peak of 6,110. This macro decoupling proves that downtown clearing represents spatial displacement, not regional resolution.<br><br>
            Geographically, 54% of all downtown homelessness remains concentrated in East Village, and the center of gravity has migrated 120 meters southward toward the industrial buffer."
          </blockquote>
        </div>

        <div class="card card-purple">
          <div class="card-title" style="color:var(--purple);">Slide 04: Debunking the Seasonality Myth (5:30 - 7:30)</div>
          <blockquote style="margin: 12px 0; padding: 12px; background: rgba(0,0,0,0.2); border-left: 3px solid var(--purple); font-style: italic;">
            "Civic conventional wisdom assumes that homeless numbers surge in summer and drop in winter due to climate. The econometrics prove this is a myth.<br><br>
            Applying the non-parametric Kruskal-Wallis test across 108 months, 8 of 9 downtown series show zero statistically significant seasonality. Our overall footprint yields a p-value of 0.995.<br><br>
            Time-series decomposition confirms seasonal strength is under 0.07. Volatility is governed by multi-year policy decisions and shelter openings—not ambient temperature. Civic budgets must end seasonal fluctuations and fund year-round permanent shelter beds."
          </blockquote>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-09')">← Day 09</button>
          <button class="btn btn-cyan" onclick="showTab('tab-defense')">Next: Defense Playbook →</button>
        </div>
      </section>

      <!-- TAB DEFENSE: DEFENSE PLAYBOOK -->
      <section id="tab-defense" class="tab-pane">
        <div class="day-badge-header">⚔️ STAKEHOLDER DEFENSE PLAYBOOK</div>
        <h1 class="day-title">Top 10 Grilling Questions & Bulletproof Defenses</h1>
        <div class="day-subtitle">Exact mathematical proofs and empirical boundaries to defend your work against tough questions.</div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">🛡️ The Golden Rule of Defense</div>
          <p>Always lead with <strong>Empirical Humility</strong>. Never invent numbers. If sample size is small (N=8), declare it proudly and show how prediction intervals protect credibility.</p>
        </div>

        <div class="card">
          <div class="card-title">Top 5 Critical Questions & Answers</div>

          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q1: How can you claim 8 of 9 series have zero seasonality? (Kruskal-Wallis p=0.995)</span>
              <span>▼</span>
            </div>
            <div class="quiz-body show">
              <strong>Defense:</strong> Non-parametric one-way ANOVA across 108 months yields H = 2.66, p = 0.995. STL decomposition confirms seasonal strength is under 0.07 (&lt;5% of variance). Volatility is driven by multi-year policy decisions and shelter cycles, not ambient weather. Marina's borderline p=0.047 is driven by Comic-Con July sweeps, not organic weather migration.
            </div>
          </div>

          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q2: Does your analysis prove the Camping Ordinance CAUSED the countywide surge?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body show">
              <strong>Defense:</strong> We explicitly do <strong>not</strong> claim causal proof. We prove empirical <strong>macro divergence</strong>: downtown dropped by 59.5%, while countywide unsheltered numbers reached historic highs (6,110). Anonymous block headcounts cannot track individuals across jurisdictional boundaries without HMIS/biometric microdata.
            </div>
          </div>

          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q3: What is the true R² of the County estimation model? (0.504 vs 0.964 trap)</span>
              <span>▼</span>
            </div>
            <div class="quiz-body show">
              <strong>Defense:</strong> The true regression R² is <strong>0.504</strong> (Adjusted R² = 0.306). The number 0.964 is the η² effect size from the One-Way ANOVA test proving that the historical downtown-to-county ratio collapsed. Conflating these two numbers damages credibility.
            </div>
          </div>

          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q4: Did Task 4.3 test a Chow structural break for the July 2023 Camping Ordinance?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body show">
              <strong>Defense:</strong> <strong>NO!</strong> Task 4.3 strictly tested April 2017, May 2018, and March 2020. Never cite an invented F-statistic for July 2023. Transparently acknowledge: <em>"July 2023 was not tested under Task 4.3 Chow candidate dates; evaluating it formally is an immediate next step."</em>
            </div>
          </div>

          <div class="quiz-card">
            <div class="quiz-header" onclick="toggleQuiz(this)">
              <span>Q5: Why did the simple Lag-1 baseline beat the complex ML stacked ensemble?</span>
              <span>▼</span>
            </div>
            <div class="quiz-body show">
              <strong>Defense:</strong> High autoregressive persistence (AR(1) > 0.85) mathematically guarantees that persistence is near-optimal. In small-sample regimes (N ≈ 90), adding 68 external features introduces noise and causes models to hallucinate complexity. Reporting this negative result demonstrates scientific integrity over algorithmic vanity.
            </div>
          </div>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-script')">← Speaker Script</button>
          <button class="btn btn-cyan" onclick="showTab('tab-cheat')">Next: 1-Page Battle Card →</button>
        </div>
      </section>

      <!-- TAB CHEAT: 1-PAGE BATTLE CARD -->
      <section id="tab-cheat" class="tab-pane">
        <div class="day-badge-header">🧮 EXECUTIVE BATTLE CARD</div>
        <h1 class="day-title">The 4 Numbers & The 4 Rules (Split-Screen Card)</h1>
        <div class="day-subtitle">Keep this tab open or on a split screen during your presentation with Adir.</div>

        <div class="stats-grid">
          <div class="stat-card" style="border-left: 4px solid var(--red);">
            <div class="stat-label">1. Historic Crisis Peak</div>
            <div class="stat-value" style="color:var(--red);">2,103</div>
            <div class="stat-subtext">May 2023 monthly peak</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--green);">
            <div class="stat-label">2. Current Level</div>
            <div class="stat-value" style="color:var(--green);">851</div>
            <div class="stat-subtext">-59.5% drop (Dec: 985)</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--cyan);">
            <div class="stat-label">3. Hotspot Migration</div>
            <div class="stat-value" style="color:var(--cyan);">120.4m</div>
            <div class="stat-subtext">SSE 160.1° to industrial edge</div>
          </div>
          <div class="stat-card" style="border-left: 4px solid var(--amber);">
            <div class="stat-label">4. County Estimate</div>
            <div class="stat-value" style="color:var(--amber);">5,900</div>
            <div class="stat-subtext">[3,900 to 8,000] (±2,050)</div>
          </div>
        </div>

        <div class="card card-amber">
          <div class="card-title" style="color:var(--amber);">🛑 The 4 Mandatory Public Communication Rules</div>
          <ol>
            <li><strong>Rule 1 — Prohibit Raw Single-Point Precision:</strong> Never say <em>"5,921"</em>.</li>
            <li><strong>Rule 2 — Mandate Rounding to Nearest 100:</strong> Always quote <strong>"about 5,900"</strong>.</li>
            <li><strong>Rule 3 — Always State the 95% Prediction Interval:</strong> Always report <strong>"5,900 [3,900 to 8,000]"</strong>.</li>
            <li><strong>Rule 4 — Mandatory Policy Regime Disclosure:</strong> Disclose that the estimate assumes post-July 2023 camping ordinance enforcement remains in place.</li>
          </ol>
        </div>

        <div class="card card-red">
          <div class="card-title" style="color:var(--red);">⚠️ 5 Stakeholder Traps to Avoid (Kill-Sheet)</div>
          <table>
            <thead>
              <tr><th>❌ NEVER SAY</th><th>✅ ALWAYS SAY INSTEAD</th><th>WHY / EMPIRICAL REASON</th></tr>
            </thead>
            <tbody>
              <tr><td><em>"The County model R² is 0.964"</em></td><td><em>"The County model R² is <strong>0.504</strong>; 0.964 is the ANOVA η²"</em></td><td>Conflating regression fit with ratio collapse destroys credibility</td></tr>
              <tr><td><em>"Camping ordinance caused county surge"</em></td><td><em>"We prove <strong>macro divergence</strong>; block counts cannot prove causation"</em></td><td>No individual tracking microdata (Recommendation R5)</td></tr>
              <tr><td><em>"Chow test F-statistic for July 2023 was X"</em></td><td><em>"Task 4.3 did not evaluate July 2023 in its candidate battery"</em></td><td>Avoids citing unverified/hallucinated F-stats</td></tr>
              <tr><td><em>"Downtown count fell to 851 in Dec 2025"</em></td><td><em>"851 was <strong>Jan 2025</strong> paired count; Dec 2025 was <strong>985</strong>"</em></td><td>Prevents date confusion</td></tr>
              <tr><td><em>"XGBoost clearly beat Holt-Winters at 12M"</em></td><td><em>"At 12 months, XGBoost, HW, and SARIMA are in a <strong>statistical tie</strong>"</em></td><td>Fold SDs are 26–36 points</td></tr>
            </tbody>
          </table>
        </div>

        <div class="day-nav-footer">
          <button class="btn btn-toggle" onclick="showTab('tab-defense')">← Defense Playbook</button>
          <button class="btn btn-cyan" onclick="showTab('tab-00')">Return to Command Center 🎯</button>
        </div>
      </section>

    </main>
  </div>

  <script>
    function showTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      
      const targetPane = document.getElementById(tabId);
      if (targetPane) targetPane.classList.add('active');
      
      // Update sidebar active state
      const matchingNavItem = Array.from(document.querySelectorAll('.nav-item')).find(el => {
        return el.getAttribute('onclick') && el.getAttribute('onclick').includes(tabId);
      });
      if (matchingNavItem) matchingNavItem.classList.add('active');
      
      document.querySelector('main.content').scrollTop = 0;
    }

    function toggleQuiz(headerEl) {
      const body = headerEl.nextElementSibling;
      if (body) {
        body.classList.toggle('show');
      }
    }

    function toggleTheme() {
      const current = document.body.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', next);
    }

    // Keyboard navigation (Arrow Left / Right)
    const tabList = ['tab-00', 'tab-01', 'tab-02', 'tab-03', 'tab-04', 'tab-05', 'tab-06', 'tab-07', 'tab-08', 'tab-09', 'tab-script', 'tab-defense', 'tab-cheat'];
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      const currentActive = document.querySelector('.tab-pane.active');
      if (!currentActive) return;
      const currentId = currentActive.id;
      const currentIndex = tabList.indexOf(currentId);
      
      if (e.key === 'ArrowRight' || e.key === ']') {
        if (currentIndex < tabList.length - 1) {
          showTab(tabList[currentIndex + 1]);
        }
      } else if (e.key === 'ArrowLeft' || e.key === '[') {
        if (currentIndex > 0) {
          showTab(tabList[currentIndex - 1]);
        }
      }
    });
  </script>
</body>
</html>
"""

# 1. Write to repo root
target_repo = "/Users/kyawsoelwin/MSI/Downtownhomelessness/Study_Curriculum_Reader.html"
with open(target_repo, "w", encoding="utf-8") as f:
    f.write(html_content)

# 2. Copy to Obsidian Visual Assets
target_obsidian = "/Users/kyawsoelwin/Obsidian/DSA_Downtown_Homelessness/03 - 📊 Visual Assets & Slide Decks/Study_Curriculum_Reader.html"
shutil.copy2(target_repo, target_obsidian)

print("Successfully generated Study_Curriculum_Reader.html in:")
print("1.", target_repo)
print("2.", target_obsidian)
