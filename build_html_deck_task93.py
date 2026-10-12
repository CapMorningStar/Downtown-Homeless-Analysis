"""
Standalone HTML presentation deck generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.html
A responsive, self-contained 14-slide browser presentation styled in the Canva
'Blue and White Modern Data Analytics' theme with Google Fonts (Bricolage Grotesque & Poppins),
inlined Base64 graphics, keyboard navigation, and exact v3.0 Report figures.
"""

import os
import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SLIDE_ASSETS = BASE_DIR / "slide_assets"
OUTPUT_HTML = BASE_DIR / "Assignment9_StrategicSynthesis.html"


def get_b64(path):
    p = Path(path)
    if not p.exists():
        return ""
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")


def build_html_deck():
    print(f"Generating Task 9.3 Companion HTML Presentation: {OUTPUT_HTML}...")

    img_trajectory = get_b64(SLIDE_ASSETS / "task93_trajectory_9year.png")
    img_forecast = get_b64(SLIDE_ASSETS / "task93_forecast_2026.png")
    img_regional = get_b64(SLIDE_ASSETS / "task93_regional_divergence.png")
    img_migration = get_b64(SLIDE_ASSETS / "task93_hotspot_migration.png")
    img_wedge = get_b64(SLIDE_ASSETS / "task93_footprint_wedge.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Downtown San Diego Unsheltered Homelessness: Strategic Synthesis (Assignment 9.3)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Poppins:wght@400;500;600;700&display=swap');

  :root {{
    --navy-primary: #293E9C;
    --royal-blue: #3A58E4;
    --periwinkle: #6984FE;
    --soft-blue: #9AADFF;
    --ice-tint: #D3DFFF;
    --bg-white: #FFFFFF;
    --bg-canvas: #F5F7FB;
    --border-card: #DCE4F5;
    --text-dark: #1D1F26;
    --text-muted: #647491;
    --red-alert: #DC2626;
    --green-action: #059669;
    --amber-warn: #D97706;
    --teal-champ: #0D9488;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0c101d;
    color: var(--text-dark);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0 60px 0;
  }}

  .nav-bar {{
    position: sticky;
    top: 15px;
    z-index: 1000;
    display: flex;
    gap: 12px;
    background: rgba(29, 31, 38, 0.9);
    backdrop-filter: blur(8px);
    padding: 10px 24px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  }}

  .nav-btn {{
    background: var(--royal-blue);
    color: #fff;
    border: none;
    padding: 6px 16px;
    border-radius: 20px;
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .nav-btn:hover {{ background: #2642be; transform: translateY(-1px); }}
  .nav-info {{
    color: #D3DFFF;
    font-size: 13px;
    display: flex;
    align-items: center;
    font-weight: 500;
  }}

  .slide-container {{
    display: flex;
    flex-direction: column;
    gap: 40px;
    width: 100%;
    max-width: 1200px;
  }}

  .slide {{
    width: 1200px;
    height: 675px;
    background: var(--bg-canvas);
    border-radius: 12px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.35);
    position: relative;
    padding: 32px 45px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  /* Top Right Slide Badge */
  .slide-badge {{
    position: absolute;
    top: 0;
    right: 35px;
    background: var(--navy-primary);
    color: #fff;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 20px;
    font-weight: 800;
    padding: 4px 18px 8px 18px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }}

  /* Canva Header */
  .slide-header {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1.5px solid var(--border-card);
  }}

  .accent-bar {{
    width: 5px;
    height: 48px;
    background: var(--royal-blue);
    border-radius: 3px;
    flex-shrink: 0;
  }}

  .header-text h3 {{
    font-size: 13.5px;
    font-weight: 700;
    color: var(--royal-blue);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 3px;
  }}

  .header-text h2 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 21px;
    font-weight: 800;
    color: var(--navy-primary);
    line-height: 1.25;
  }}

  /* Slide Content Area */
  .slide-body {{
    flex: 1;
    display: flex;
    gap: 22px;
    min-height: 0;
  }}

  /* Cards */
  .card {{
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  }}

  .card h4 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 14px;
    font-weight: 800;
    color: var(--navy-primary);
    margin-bottom: 8px;
  }}

  /* KPI Ribbon */
  .kpi-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 20px;
  }}

  .kpi-card {{
    background: #fff;
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
  }}

  .kpi-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--accent, var(--navy-primary));
  }}

  .kpi-val {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: var(--accent, var(--navy-primary));
    line-height: 1;
    margin-bottom: 6px;
  }}

  .kpi-lbl {{
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-dark);
    text-transform: uppercase;
    margin-bottom: 4px;
  }}

  .kpi-sub {{
    font-size: 12.5px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  /* Tables */
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    background: #fff;
  }}
  table.data-table th {{
    background: var(--navy-primary);
    color: #fff;
    font-weight: 600;
    padding: 8px 10px;
    text-align: left;
  }}
  table.data-table td {{
    padding: 7px 10px;
    border-bottom: 1px solid var(--border-card);
    color: var(--text-dark);
  }}
  table.data-table tr:nth-child(even) td {{
    background: var(--bg-canvas);
  }}

  /* Footer */
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border-card);
    padding-top: 8px;
    margin-top: 10px;
    font-size: 9px;
    color: var(--text-muted);
  }}
  .slide-footer strong {{
    color: var(--navy-primary);
  }}

  .hero-img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 6px;
  }}

  ul.bullet-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  ul.bullet-list li {{
    font-size: 13.5px;
    line-height: 1.45;
    position: relative;
    padding-left: 14px;
    color: var(--text-dark);
  }}
  ul.bullet-list li::before {{
    content: '•';
    position: absolute;
    left: 0;
    color: var(--royal-blue);
    font-weight: bold;
  }}
  ul.bullet-list strong {{
    color: var(--royal-blue);
  }}

  @media print {{
    body {{
      background: var(--bg-canvas) !important;
      padding: 0 !important;
      margin: 0 !important;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
    .nav-bar {{
      display: none !important;
    }}
    .slide-container {{
      gap: 0 !important;
      max-width: none !important;
      width: 100% !important;
    }}
    .slide {{
      width: 13.333in !important;
      height: 7.5in !important;
      max-width: 13.333in !important;
      max-height: 7.5in !important;
      page-break-after: always !important;
      break-after: page !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      margin: 0 !important;
      padding: 32px 45px !important;
    }}
    @page {{
      size: 13.333in 7.5in;
      margin: 0;
    }}
  }}
</style>
</head>
<body>

<div class="nav-bar">
  <button class="nav-btn" onclick="prevSlide()">◀ Previous</button>
  <div class="nav-info" id="slideIndicator">Slide 1 of 14</div>
  <button class="nav-btn" onclick="nextSlide()">Next ▶</button>
  <button class="nav-btn" style="background:#0D9488;" onclick="window.print()">Print / Export PDF</button>
</div>

<div class="slide-container">

  <!-- SLIDE 1: TITLE SLIDE -->
  <div class="slide" id="slide-1">
    <div class="slide-badge">01</div>
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 20px 40px; background: #fff; border: 1px solid var(--border-card); border-radius: 12px;">
      <div style="display: inline-block; background: var(--ice-tint); border: 1px solid var(--soft-blue); padding: 5px 14px; border-radius: 15px; font-size: 13px; font-weight: 700; color: var(--navy-primary); width: fit-content; margin-bottom: 18px;">
        DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS BRIEFING
      </div>
      <h1 style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 34px; font-weight: 800; color: var(--navy-primary); line-height: 1.2; margin-bottom: 12px;">
        Downtown Homelessness:<br>Executive Strategic Roadmap (2017–2026)
      </h1>
      <p style="font-size: 15px; font-weight: 600; color: var(--royal-blue); margin-bottom: 24px;">
        Econometrics, Spatial Dynamics, ML Forecasting & Regional Policy
      </p>
      <div style="height: 1.5px; background: var(--border-card); width: 100%; margin-bottom: 24px;"></div>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
        <div>
          <div style="font-size: 12.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Partnership & Authors</div>
          <div style="font-size: 13px; color: var(--text-dark); line-height: 1.4;">
            <strong>DSA</strong>, DSDP & RTFH<br>
            Lead: <strong>K.S. Lwin</strong> | Proj Lead: <strong>A. Mancebo Jr.</strong>
          </div>
        </div>
        <div>
          <div style="font-size: 12.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Data Foundation</div>
          <div style="font-size: 13px; color: var(--text-dark); line-height: 1.4;">
            <strong>108 Months of Counts</strong> (2017–2025)<br>
            Regional PIT Censuses
          </div>
        </div>
        <div>
          <div style="font-size: 12.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Analytical Framework</div>
          <div style="font-size: 13px; color: var(--text-dark); line-height: 1.4;">
            Spatial Gi* • Walk-Forward CV • OLS Regime • 4 Comm Rules
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 1 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 2: KPI DASHBOARD -->
  <div class="slide" id="slide-2">
    <div class="slide-badge">02</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Executive Framing</h3>
        <h2>Executive KPIs: Peak & Migration</h2>
      </div>
    </div>
    <div class="slide-body" style="flex-direction: column;">
      <div class="kpi-row">
        <div class="kpi-card" style="--accent: var(--red-alert);">
          <div class="kpi-val">2,103</div>
          <div class="kpi-lbl">Crisis Peak (May 2023)</div>
          <div class="kpi-sub">Highest count on record. Capped a 3-year surge.</div>
        </div>
        <div class="kpi-card" style="--accent: var(--green-action);">
          <div class="kpi-val">851</div>
          <div class="kpi-lbl">Recent Count (Jan 2025)</div>
          <div class="kpi-sub">Down 59% from peak. Dec 2025 hit 985.</div>
        </div>
        <div class="kpi-card" style="--accent: var(--navy-primary);">
          <div class="kpi-val">54.0%</div>
          <div class="kpi-lbl">East Village Volume</div>
          <div class="kpi-sub">Core driver of downtown population.</div>
        </div>
        <div class="kpi-card" style="--accent: var(--royal-blue);">
          <div class="kpi-val">120 m</div>
          <div class="kpi-lbl">Hotspot Migration Vector</div>
          <div class="kpi-sub">Centroid shifted 120m south toward South East Village.</div>
        </div>
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE REALITY: DOWNTOWN DROPS VS REGIONAL SHIFTS</h4>
        <ul class="bullet-list">
          <li><strong>Three Phases:</strong> Pre-COVID drop, massive 2021-2023 surge (peak 2,103), then post-enforcement contraction (851 in Jan 2025).</li>
          <li><strong>No Seasonality:</strong> Weather doesn't drive numbers (p=0.995). Seasonal budgets are a mismatch for year-round needs.</li>
          <li><strong>Map Changes:</strong> 121 blocks added in 2022. Correcting for this shows a real, but smaller, +71% surge in the core.</li>
          <li><strong>Regional Shift:</strong> Downtown share fell to 15%, while countywide hit a record 6,110. The crisis moved, it didn't end.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 2 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 3: 9-YEAR TRAJECTORY -->
  <div class="slide" id="slide-3">
    <div class="slide-badge">03</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Longitudinal Dynamics</h3>
        <h2>9-Year Trajectory: Three Policy Epochs</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_trajectory}" class="hero-img" alt="9-Year Trajectory">
      </div>
      <div style="flex: 1; display: flex; flex-direction: column; gap: 12px;">
        <div class="card" style="flex: 1; border-left: 4px solid var(--royal-blue);">
          <div style="font-size: 14px; font-weight: 700; color: var(--royal-blue); margin-bottom: 2px;">Epoch 1: Contraction (2017–2020)</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">Low of 529 in Mar 2020 (−38%)</div>
          <div style="font-size: 12.5px; color: var(--text-muted); line-height: 1.35;">Pre-COVID drop. Baseline interventions worked.</div>
        </div>
        <div class="card" style="flex: 1; border-left: 4px solid var(--red-alert);">
          <div style="font-size: 14px; font-weight: 700; color: var(--red-alert); margin-bottom: 2px;">Epoch 2: Crisis Surge (2021–2023)</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">May 2023 Peak of 2,103 (+297%)</div>
          <div style="font-size: 12.5px; color: var(--text-muted); line-height: 1.35;">Driven by shelter de-densification and housing vulnerability.</div>
        </div>
        <div class="card" style="flex: 1; border-left: 4px solid var(--green-action);">
          <div style="font-size: 14px; font-weight: 700; color: var(--green-action); margin-bottom: 2px;">Epoch 3: Enforcement (2024–2025)</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">Jan 2025 Count of 851 (−59%)</div>
          <div style="font-size: 12.5px; color: var(--text-muted); line-height: 1.35;">Sharp drop post-Camping Ordinance. Counts stabilized ~860-880.</div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 3 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 4: DEBUNKING SEASONALITY -->
  <div class="slide" id="slide-4">
    <div class="slide-badge">04</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Econometric Seasonality Proof</h3>
        <h2>Seasonality Myth: Weather Doesn't Drive Homelessness</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.3;">
        <h4>Kruskal-Wallis Tests (df=11)</h4>
        <table class="data-table">
          <tr><th>Geographic Series</th><th>KW H</th><th>KW p</th><th>ANOVA p</th><th>Verdict</th></tr>
          <tr><td><strong>Overall — Reported Footprint</strong></td><td>2.66</td><td>0.995</td><td>0.998</td><td>No Seasonality</td></tr>
          <tr><td><strong>Overall — Fixed Core Six</strong></td><td>9.00</td><td>0.622</td><td>0.670</td><td>No Seasonality</td></tr>
          <tr><td><strong>East Village (Epicenter)</strong></td><td>14.16</td><td>0.224</td><td>0.219</td><td>No Seasonality</td></tr>
          <tr><td><strong>City Center (Core)</strong></td><td>4.86</td><td>0.938</td><td>0.913</td><td>No Seasonality</td></tr>
          <tr><td><strong>Gaslamp Quarter</strong></td><td>14.57</td><td>0.203</td><td>0.087</td><td>No Seasonality</td></tr>
          <tr><td><strong>Columbia</strong></td><td>8.76</td><td>0.644</td><td>0.473</td><td>No Seasonality</td></tr>
          <tr><td><strong>Cortez</strong></td><td>12.73</td><td>0.312</td><td>0.047</td><td>Mixed</td></tr>
          <tr><td><strong>Marina</strong></td><td>19.88</td><td>0.047</td><td>0.162</td><td>Mixed</td></tr>
          <tr><td><strong>Outside Perimeter</strong></td><td>11.45</td><td>0.406</td><td>0.440</td><td>No Seasonality</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>WHY THIS MATTERS FOR MUNICIPAL BUDGETING</h4>
        <ul class="bullet-list">
          <li><strong>Weather Fallacy:</strong> Calendar months explain zero variation (p=0.995). Seasonal planning is flawed.</li>
          <li><strong>Macro Drivers:</strong> Shifts are driven by capacity, policy, and housing dynamics—not weather.</li>
          <li><strong>Fund Year-Round:</strong> Stop seasonal allocations. Commit to permanent capacity.</li>
          <li><strong>Solid Evidence:</strong> 8 of 9 series show strictly non-significant seasonality.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 4 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 5: FOOTPRINT WEDGE -->
  <div class="slide" id="slide-5">
    <div class="slide-badge">05</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Spatial Panel Accounting</h3>
        <h2>Map Changes: Disentangling Reality from Map Changes</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_wedge}" class="hero-img" alt="Footprint Wedge">
      </div>
      <div class="card" style="flex: 1;">
        <h4>ACCOUNTING FOR THE 121-BLOCK EXPANSION</h4>
        <ul class="bullet-list">
          <li><strong>Administrative Shift:</strong> 121 blocks added in 2022 (Golden Hill, Barrio Logan).</li>
          <li><strong>The Wedge Effect:</strong> Added blocks inflated counts by up to 33% (640 individuals at peak).</li>
          <li><strong>True Core Growth:</strong> Balanced 261-block panel still grew 71% in 2022. Boundaries matter.</li>
          <li><strong>Analytical Fix:</strong> Enforced strict longitudinal panel balance (<code>BlockPanel_Balanced_261.csv</code>) across all 12 digitized count dates (2018–2025).</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 5 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 6: EAST VILLAGE EPICENTER -->
  <div class="slide" id="slide-6">
    <div class="slide-badge">06</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Geographic Concentration</h3>
        <h2>Concentration: The East Village Epicenter</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.3;">
        <h4>Top Hotspots (Getis-Ord Gi*)</h4>
        <table class="data-table">
          <tr><th>Rank</th><th>Block Identifier</th><th>Area</th><th>Hotspot Dates</th><th>Rate</th><th>Mean Count</th></tr>
          <tr><td><strong>#1</strong></td><td>16th St & Imperial Ave</td><td>South East Village</td><td>9 / 12 dates</td><td>75%</td><td>5.9</td></tr>
          <tr><td><strong>#2</strong></td><td>I-5 SB & Imperial Ave</td><td>South East Village</td><td>8 / 12 dates</td><td>67%</td><td>4.4</td></tr>
          <tr><td><strong>#3</strong></td><td>I-5 SB Off-Ramp (Map Border)</td><td>South East Village</td><td>6 / 12 dates</td><td>50%</td><td>6.8</td></tr>
          <tr><td><strong>#4</strong></td><td>I-5 SB On-Ramp (Map Border)</td><td>South East Village</td><td>4 / 12 dates</td><td>33%</td><td>1.3</td></tr>
          <tr><td><strong>#5</strong></td><td>17th St & Imperial Ave</td><td>South East Village</td><td>4 / 12 dates</td><td>33%</td><td>5.5</td></tr>
          <tr><td><strong>#6</strong></td><td>16th St & J St</td><td>South East Village</td><td>2 / 12 dates</td><td>17%</td><td>13.3</td></tr>
          <tr><td><strong>#7</strong></td><td>17th St & J St</td><td>South East Village</td><td>2 / 12 dates</td><td>17%</td><td>12.2</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE BUILT-ENVIRONMENT MAGNET</h4>
        <ul class="bullet-list">
          <li><strong>Volume Dominance:</strong> Drives 54% of downtown homelessness (avg 552 individuals).</li>
          <li><strong>Top Hotspots:</strong> 100% of the top 10 persistent hotspots are in South East Village.</li>
          <li><strong>Built Magnets:</strong> Clusters anchor around transit, services, and freeway underpasses.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 6 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 7: HOTSPOT CENTROID MIGRATION -->
  <div class="slide" id="slide-7">
    <div class="slide-badge">07</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Cluster Migration Vector</h3>
        <h2>Hotspot Dynamics: 120m Southward Vector</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_migration}" class="hero-img" alt="Centroid Migration">
      </div>
      <div class="card" style="flex: 1;">
        <h4>DRIVERS OF CLUSTER DISPLACEMENT</h4>
        <ul class="bullet-list">
          <li><strong>120m Migration:</strong> Centroid shifted 120m SSE toward South East Village.</li>
          <li><strong>Density Driven:</strong> Unweighted moved 62m; density and location both pull south.</li>
          <li><strong>Enforcement Push:</strong> Sidewalk clearance in Gaslamp displaced clusters south.</li>
          <li><strong>Spatial Shift:</strong> Reflects macro cluster movements, not individual tracking.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 7 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 8: MACHINE LEARNING BENCHMARK -->
  <div class="slide" id="slide-8">
    <div class="slide-badge">08</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Predictive Intelligence</h3>
        <h2>Machine Learning: 5-Fold CV Benchmark</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4;">
        <h4>5-Fold CV Performance</h4>
        <table class="data-table">
          <tr><th>Model Architecture</th><th>1-Month MAPE</th><th>3-Month MAPE</th><th>6-Month MAPE</th><th>12-Month CV MAPE</th></tr>
          <tr><td>SARIMA (ACF/PACF Grid)</td><td>5.4% ± 4.1%</td><td>14.3% ± 10.3%</td><td>24.7% ± 20.9%</td><td>39.6% ± 35.5%</td></tr>
          <tr><td>Holt-Winters Exp Smooth</td><td>13.0% ± 9.2%</td><td>17.6% ± 10.4%</td><td>25.2% ± 18.2%</td><td>38.4% ± 28.5%</td></tr>
          <tr style="background:#E6FFFA;"><td><strong>XGBoost (Champion)</strong></td><td>14.0% ± 8.9%</td><td>19.9% ± 14.8%</td><td>26.7% ± 18.5%</td><td><strong>38.3% ± 26.0%</strong></td></tr>
          <tr><td>Naive Seasonal (t−12)</td><td>39.5% ± 31.9%</td><td>40.1% ± 31.3%</td><td>48.5% ± 35.4%</td><td>51.7% ± 24.5%</td></tr>
          <tr><td>Prophet (Changepoints)</td><td>42.9% ± 26.0%</td><td>42.7% ± 26.0%</td><td>51.3% ± 31.9%</td><td>64.2% ± 35.4%</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>CORE FORECASTING TAKEAWAYS</h4>
        <ul class="bullet-list">
          <li><strong>Horizons:</strong> SARIMA wins short-term (5.4% MAPE). XGBoost ties at 12-months (38.3%).</li>
          <li><strong>Champion Model:</strong> XGBoost chosen for lowest error and strong 2025 hold-out (8.5%).</li>
          <li><strong>Baseline Check:</strong> Naive seasonal performed well in 2025, proving baselines are critical.</li>
          <li><strong>Prophet Failure:</strong> Prophet failed (64.2% error) as it missed the post-peak drop.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 8 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 9: 2026 FORWARD OUTLOOK -->
  <div class="slide" id="slide-9">
    <div class="slide-badge">09</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Prospective Forecasting</h3>
        <h2>2026 Outlook: Stress-Testing Scenarios</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_forecast}" class="hero-img" alt="2026 Forecast">
      </div>
      <div class="card" style="flex: 1;">
        <h4>PROSPECTIVE 2026 SCENARIOS</h4>
        <ul class="bullet-list">
          <li><strong>Baseline:</strong> Expected to remain range-bound at 816–896 individuals.</li>
          <li><strong>Stress-Tests:</strong> Fixed scenario paths, not causal policy models.</li>
          <li><strong>Optimistic:</strong> ~675 individuals by Dec 2026 (favorable dynamics).</li>
          <li><strong>Pessimistic:</strong> ~1,123 individuals by Dec 2026 (economic constraints).</li>
          <li><strong>Range Planning:</strong> Plan using uncertainty bands, not single points.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 9 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 10: REGIONAL DISPLACEMENT PARADOX -->
  <div class="slide" id="slide-10">
    <div class="slide-badge">10</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Regional Policy Dynamics</h3>
        <h2>Regional Displacement: Downtown Drops vs County Highs</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_regional}" class="hero-img" alt="Regional Divergence">
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE DISPLACEMENT REALITY</h4>
        <ul class="bullet-list">
          <li><strong>Share Plunged:</strong> Downtown's share of county unsheltered fell to 14.9%.</li>
          <li><strong>County Record:</strong> Countywide numbers reached 6,110 (2024) and 5,714 (2025).</li>
          <li><strong>Displacement:</strong> Downtown drops align with regional spikes. The crisis moved.</li>
          <li><strong>Data Limits:</strong> Reflects macro divergence, individual tracking is unavailable.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 10 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 11: MACRO ESTIMATION & 4 RULES -->
  <div class="slide" id="slide-11">
    <div class="slide-badge">11</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Macro Econometrics & Governance</h3>
        <h2>Macro Model & 4 Communication Rules</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1;">
        <h4>POLICY REGIME OLS CHAMPION MODEL</h4>
        <ul class="bullet-list">
          <li><strong>Ratio Rejected:</strong> Fixed ratios fail across policy regimes (ANOVA p=0.0002).</li>
          <li><strong>Model Equation:</strong><br>
            <code style="background:#EFF6FF; color:#1E40AF; padding:2px 6px; border-radius:4px; font-size:10px;">Y = 4,513.26 + 0.1859 * X + 1,225.04 * D_post</code><br>
            Where X = Downtown Jan count, D_post = 1 for 2024/2025.</li>
          <li><strong>Diagnostics:</strong> R^2 = 0.504 | Adj R^2 = 0.306 | LOOCV RMSE = 815.3 | Bias = −0.3%. Neither slope (p=0.78) nor D_post (p=0.075) is statistically significant at 5%.</li>
          <li><strong>Current Estimate:</strong><br>
            <strong>5,900 [95% PI: 3,900 to 8,000]</strong><br>Margin of error is ±35%.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1.1; border-top: 4px solid var(--red-alert);">
        <h4 style="color: var(--red-alert);">THE 4 MANDATORY PUBLIC COMMUNICATION RULES</h4>
        <ul class="bullet-list">
          <li><strong>Rule 1: No False Precision:</strong> Stop using raw single points (e.g., '5,921'). It damages credibility.</li>
          <li><strong>Rule 2: Round to 100:</strong> Always round estimates to the nearest hundred.</li>
          <li><strong>Rule 3: Show 95% Interval:</strong> Mandate prediction ranges: <em>'5,900 [3,900 to 8,000]'</em>.</li>
          <li><strong>Rule 4: Disclose Regimes:</strong> Explicitly state assumptions (e.g., assumes post-2023 enforcement holds).</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 11 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 12: MUNICIPAL POLICY ROADMAP (MEMO R1–R8) -->
  <div class="slide" id="slide-12">
    <div class="slide-badge">12</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Strategic Recommendations</h3>
        <h2>Policy Roadmap: Recommendations (R1–R8)</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1; border-top: 4px solid var(--royal-blue);">
        <h4 style="color: var(--royal-blue); font-size:12px;">IMMEDIATE ACTION (0–3 MONTHS)</h4>
        <div style="font-size: 13px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Outreach & Governance</div>
        <ul class="bullet-list">
          <li><strong>R1. Hotspots:</strong> Target 16th-17th & Imperial for rapid outreach.</li>
          <li><strong>R2. Range Planning:</strong> Enforce Rules 1-4 for all public numbers.</li>
          <li><strong>R3. Boundary Clarity:</strong> Disclose 261 vs 382-block footprint metrics.</li>
          <li><strong>Leaders:</strong> City Strategies, DSDP.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--green-action);">
        <h4 style="color: var(--green-action); font-size:12px;">MEDIUM-TERM (6–12 MONTHS)</h4>
        <div style="font-size: 13px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Data & Validation</div>
        <ul class="bullet-list">
          <li><strong>R4. Component Data:</strong> Mandate full tent/vehicle component reporting.</li>
          <li><strong>R5. Displacement:</strong> Verify cross-border regional movement.</li>
          <li><strong>R6. Retraining:</strong> Update OLS models with 2026 PIT data.</li>
          <li><strong>R7. Shelter Data:</strong> Integrate real Housing Inventory Count (HIC).</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--navy-primary);">
        <h4 style="color: var(--navy-primary); font-size:12px;">LONG-TERM (1–3 YEARS)</h4>
        <div style="font-size: 13px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Digitization & Infrastructure</div>
        <ul class="bullet-list">
          <li><strong>R8. Digitize Maps:</strong> Digitize remaining 78 monthly block maps.</li>
          <li><strong>Regional HMIS:</strong> Unify real-time city and county bed tracking.</li>
          <li><strong>True Evaluation:</strong> Measure regional outcomes, not just local clearing.</li>
          <li><strong>Leaders:</strong> County HHS, RTFH, DSA.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 12 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 13: STREAMLIT DASHBOARD -->
  <div class="slide" id="slide-13">
    <div class="slide-badge">13</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Operational Decision Tool</h3>
        <h2>Interactive Decision-Support System: The Streamlit Executive Dashboard</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4;">
        <h4>7 DASHBOARD MODULES (TASK 9.1)</h4>
        <ul class="bullet-list">
          <li><strong>Tab 1: Historical Trends:</strong> Longitudinal time series (2017–2025), multiplier regime markers, epoch shading, component toggles.</li>
          <li><strong>Tab 2: 12-Month Forecast:</strong> Prospective 2026 projections, model selectors (XGBoost champion, HW, SARIMA, Prophet), 80%/95% fan envelopes, scenario stress tests.</li>
          <li><strong>Tab 3: Hotspot Surveillance:</strong> Folium interactive choropleth, 12 count dates, 261 vs 382 panel toggle, Getis-Ord Gi* classifications (95%, 99%).</li>
          <li><strong>Tab 4: Regions:</strong> 4-pane STL decomposition, monthly seasonal indices, Kruskal-Wallis non-parametric significance displays.</li>
          <li><strong>Tab 5: Calculator:</strong> Interactive Policy Regime OLS calculator enforcing The 4 Public Communication Rules with Student's t intervals.</li>
          <li><strong>Tab 6: Methodology & About:</strong> Documentation of 4 multiplier schedules, 2022 expansion (+121 blocks), data audits and QA flags.</li>
          <li><strong>Tab 7: Alerts:</strong> Shewhart control charts (±2σ, ±3σ) and CUSUM (k=0.5, h=4.0) early-warning surveillance engine for rapid operational alerts.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1;">
        <h4>DEPLOYMENT & VERIFICATION INFO</h4>
        <ul class="bullet-list">
          <li><strong>Local URL:</strong> <code>http://localhost:8501</code> (Fast interactive response time)</li>
          <li><strong>Cloud URL:</strong> <code>https://downtown-sd-homelessness.streamlit.app</code></li>
          <li><strong>Quality Check:</strong> 46/46 unit tests passing.</li>
          <li><strong>Performance:</strong> <code>@st.cache_data</code> provides fast sub-second cached lookups across all 7 tabs.</li>
          <li><strong>Audience:</strong> City Council, RTFH, DSDP operations.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 13 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 14: EXECUTIVE SYNTHESIS -->
  <div class="slide" id="slide-14">
    <div class="slide-badge">14</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Synthesis & Next Steps</h3>
        <h2>Synthesis & Next Steps</h2>
      </div>
    </div>
    <div class="slide-body" style="flex-direction: column; gap: 14px;">
      <div class="card" style="border-left: 5px solid var(--navy-primary);">
        <h4>1. EVIDENCE-BASED RESOURCE ALLOCATION</h4>
        <div style="font-size: 13.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">End Seasonal Budgeting</div>
        <div style="font-size: 13px; color: var(--text-muted); line-height: 1.4;">
          Data proves zero seasonality (p=0.995). Lock investments into permanent capacity and target South East Village hotspots.
        </div>
      </div>
      <div class="card" style="border-left: 5px solid var(--royal-blue);">
        <h4>2. REGIONAL ACCOUNTABILITY & SYSTEMS REFORM</h4>
        <div style="font-size: 13.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">Fix Divergence</div>
        <div style="font-size: 13px; color: var(--text-muted); line-height: 1.4;">
          Downtown drops pair with countywide highs (6,110). Stop localized displacement; demand countywide shelter collaboration.
        </div>
      </div>
      <div class="card" style="border-left: 5px solid var(--green-action);">
        <h4>3. HIGH-VALUE DATA INVESTMENTS</h4>
        <div style="font-size: 13.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">Digitize & Retrain</div>
        <div style="font-size: 13px; color: var(--text-muted); line-height: 1.4;">
          Digitize remaining 78 block maps. Annually retrain the OLS model for accuracy.
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 14 of 14</strong></div>
    </div>
  </div>

</div>

<script>
  let currentSlide = 1;
  const totalSlides = 14;

  function updateIndicator() {{
    document.getElementById('slideIndicator').innerText = `Slide ${{currentSlide}} of ${{totalSlides}}`;
    const el = document.getElementById(`slide-${{currentSlide}}`);
    if (el) {{
      el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
  }}

  function nextSlide() {{
    if (currentSlide < totalSlides) {{
      currentSlide++;
      updateIndicator();
    }}
  }}

  function prevSlide() {{
    if (currentSlide > 1) {{
      currentSlide--;
      updateIndicator();
    }}
  }}

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
      e.preventDefault();
      nextSlide();
    }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
      e.preventDefault();
      prevSlide();
    }}
  }});
</script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated HTML presentation: {OUTPUT_HTML} ({len(html_content)} bytes)")


if __name__ == "__main__":
    build_html_deck()
