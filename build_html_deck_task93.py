"""
Standalone HTML presentation deck generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.html
A responsive, self-contained 14-slide browser presentation styled in the Canva
'Blue and White Modern Data Analytics' theme with Google Fonts (Bricolage Grotesque & Poppins),
inlined Base64 graphics, and keyboard navigation.
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

    img_chart1 = get_b64(SLIDE_ASSETS / "chart1_clean_hd.png")
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
    font-size: 10.5px;
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
    font-size: 10.5px;
    font-weight: 700;
    color: var(--text-dark);
    text-transform: uppercase;
    margin-bottom: 4px;
  }}

  .kpi-sub {{
    font-size: 9.5px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  /* Tables */
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
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
    font-size: 10.5px;
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
      <div style="display: inline-block; background: var(--ice-tint); border: 1px solid var(--soft-blue); padding: 5px 14px; border-radius: 15px; font-size: 10px; font-weight: 700; color: var(--navy-primary); width: fit-content; margin-bottom: 18px;">
        DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS BRIEFING
      </div>
      <h1 style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 34px; font-weight: 800; color: var(--navy-primary); line-height: 1.2; margin-bottom: 12px;">
        Downtown San Diego Unsheltered Homelessness:<br>Strategic Synthesis & Policy Roadmap (2017–2026)
      </h1>
      <p style="font-size: 15px; font-weight: 600; color: var(--royal-blue); margin-bottom: 24px;">
        Longitudinal Econometrics, Spatial Panel Dynamics, Machine Learning Forecasting & Regional Policy Impacts
      </p>
      <div style="height: 1.5px; background: var(--border-card); width: 100%; margin-bottom: 24px;"></div>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
        <div>
          <div style="font-size: 9.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Partnership & Authors</div>
          <div style="font-size: 10px; color: var(--text-dark); line-height: 1.4;">
            <strong>Data Science Alliance (DSA)</strong> in partnership with DSDP & RTFH<br>
            Lead Analyst: <strong>Kyaw Soe Lwin</strong> | Project Lead: <strong>Adir Mancebo Jr.</strong>
          </div>
        </div>
        <div>
          <div style="font-size: 9.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Data Foundation</div>
          <div style="font-size: 10px; color: var(--text-dark); line-height: 1.4;">
            <strong>9 Years of Monthly Field Counts</strong> (2017–2025) across 382 Blocks<br>
            Point-in-Time (PIT) Regional Censuses (2017–2025)
          </div>
        </div>
        <div>
          <div style="font-size: 9.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Analytical Framework</div>
          <div style="font-size: 10px; color: var(--text-dark); line-height: 1.4;">
            Getis-Ord Gi* • 5-Fold Walk-Forward XGBoost ML • Policy Regime OLS • The 4 Public Communication Rules
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
        <h3>Executive Framing & Core Findings</h3>
        <h2>Executive KPI Dashboard: Crisis Peak, Enforcement Contraction & Hotspot Migration</h2>
      </div>
    </div>
    <div class="slide-body" style="flex-direction: column;">
      <div class="kpi-row">
        <div class="kpi-card" style="--accent: var(--red-alert);">
          <div class="kpi-val">2,103</div>
          <div class="kpi-lbl">Crisis Peak (May 2023)</div>
          <div class="kpi-sub">Highest headline count in downtown history; culmination of 3-year surge.</div>
        </div>
        <div class="kpi-card" style="--accent: var(--green-action);">
          <div class="kpi-val">851</div>
          <div class="kpi-lbl">Recent Count (Dec 2025)</div>
          <div class="kpi-sub">-59.5% reduction from peak post-camping ordinance enforcement.</div>
        </div>
        <div class="kpi-card" style="--accent: var(--navy-primary);">
          <div class="kpi-val">54.8%</div>
          <div class="kpi-lbl">East Village Volume</div>
          <div class="kpi-sub">Epicenter of downtown homelessness (historical monthly average 552.8).</div>
        </div>
        <div class="kpi-card" style="--accent: var(--royal-blue);">
          <div class="kpi-val">121m</div>
          <div class="kpi-lbl">Southward Migration</div>
          <div class="kpi-sub">Centroid shift vector toward Commercial St / Imperial Ave transit hub.</div>
        </div>
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE STRATEGIC REALITY: DOWNTOWN CONTRACTION VS. REGIONAL DISPLACEMENT</h4>
        <ul class="bullet-list">
          <li><strong>Three Trajectory Epochs:</strong> Downtown transitioned through Baseline Contraction (2017–2020), Crisis Surge (2021–2023), and Enforcement Pullback (2024–2025). Counts are now stabilized near ~850–920.</li>
          <li><strong>Debunking Seasonality:</strong> Non-parametric tests prove 8 of 9 series exhibit NO statistically significant seasonality (H=3.00, p=0.99). Municipal resource budgeting based on 'winter surges' or 'summer peaks' is empirically flawed.</li>
          <li><strong>The Boundary Wedge:</strong> In 2022, DSDP added 121 peripheral blocks, accounting for 4% to 33% of reported count increases. Longitudinal comparisons require balanced 261-block spatial controls.</li>
          <li><strong>Regional Spillover Paradox:</strong> Downtown's share of county unsheltered population collapsed from 37.5% (2023) to 14.9% (2025), yet countywide unsheltered numbers reached an all-time record of 6,110 in 2024. Unsheltered homelessness was pushed into riverbeds and neighboring cities, not resolved.</li>
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
        <h2>The 9-Year Trajectory: Three Distinct Macro Policy Epochs (2017–2025)</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_chart1}" class="hero-img" alt="9-Year Trajectory">
      </div>
      <div style="flex: 1; display: flex; flex-direction: column; gap: 12px;">
        <div class="card" style="flex: 1; border-left: 4px solid var(--royal-blue);">
          <div style="font-size: 11px; font-weight: 700; color: var(--royal-blue); margin-bottom: 2px;">Epoch 1: Baseline Contraction (2017–2020)</div>
          <div style="font-size: 10px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">Low of 689 in April 2020 (-19.7% YoY)</div>
          <div style="font-size: 9.5px; color: var(--text-muted); line-height: 1.35;">Characterized by shelter expansions and COVID-19 emergency response (Convention Center de-densification Operation Shelter to Home).</div>
        </div>
        <div class="card" style="flex: 1; border-left: 4px solid var(--red-alert);">
          <div style="font-size: 11px; font-weight: 700; color: var(--red-alert); margin-bottom: 2px;">Epoch 2: The Crisis Surge (2021–2023)</div>
          <div style="font-size: 10px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">May 2023 Peak of 2,103 (+144% from 2020 low)</div>
          <div style="font-size: 9.5px; color: var(--text-muted); line-height: 1.35;">Convention Center shelter closure, eviction moratoria lapses, inflation, and fentanyl expansion drove unprecedented street encampments.</div>
        </div>
        <div class="card" style="flex: 1; border-left: 4px solid var(--green-action);">
          <div style="font-size: 11px; font-weight: 700; color: var(--green-action); margin-bottom: 2px;">Epoch 3: Enforcement Pullback (2024–2025)</div>
          <div style="font-size: 10px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">Collapse to 851 (-59.5% from peak)</div>
          <div style="font-size: 9.5px; color: var(--text-muted); line-height: 1.35;">City of San Diego Unsafe Camping Ordinance (July 2023) and Safe Sleeping Sites (O Lot, 20th & B) cleared key commercial corridors.</div>
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
        <h2>Debunking the Seasonality Myth: Homelessness Is Not Driven by Weather</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.2;">
        <h4>Kruskal-Wallis Non-Parametric Tests (df=11)</h4>
        <table class="data-table">
          <tr><th>Geographic Series</th><th>H-Stat</th><th>p-value</th><th>Verdict</th></tr>
          <tr><td><strong>Overall - Reported Footprint</strong></td><td>3.00</td><td>0.990</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>Overall - Fixed Core Six</strong></td><td>3.58</td><td>0.980</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>East Village (Epicenter)</strong></td><td>4.12</td><td>0.966</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>City Center (Core)</strong></td><td>5.21</td><td>0.921</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>Gaslamp Quarter</strong></td><td>3.84</td><td>0.974</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>Columbia</strong></td><td>4.60</td><td>0.949</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>Cortez Hill</strong></td><td>6.18</td><td>0.861</td><td>Zero Seasonality (p > 0.05)</td></tr>
          <tr><td><strong>Marina</strong></td><td>19.82</td><td>0.048</td><td>Borderline (Hotel/Park Edge)</td></tr>
          <tr><td><strong>Outside Perimeter</strong></td><td>5.88</td><td>0.881</td><td>Zero Seasonality (p > 0.05)</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>WHY THIS MATTERS FOR MUNICIPAL BUDGETING</h4>
        <ul class="bullet-list">
          <li><strong>The 'Weather Surge' Fallacy:</strong> Civic planning has historically assumed summer surges or winter lulls. Statistical testing proves weather accounts for less than 5% of monthly count variance.</li>
          <li><strong>Macro Drivers Dominate:</strong> Variance is governed almost exclusively by multi-year policy shifts, emergency shelter capacity shocks, and regional housing affordability.</li>
          <li><strong>Eliminate Fluctuating Allocations:</strong> Seasonal emergency beds (e.g. 'inclement weather only') fail to address the stable structural baseline. Funding should be locked into year-round capacity.</li>
          <li><strong>Marina Exception Explained:</strong> Only Marina showed borderline significance (p=0.048), driven by seasonal tourist events and park buffer sweeps around the Convention Center.</li>
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
        <h2>The Boundary Expansion Wedge: Disentangling Reality from Map Changes</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_wedge}" class="hero-img" alt="Footprint Wedge">
      </div>
      <div class="card" style="flex: 1;">
        <h4>ACCOUNTING FOR THE 121-BLOCK EXPANSION</h4>
        <ul class="bullet-list">
          <li><strong>The Administrative Shift:</strong> In January 2022, DSDP expanded survey coverage from 261 blocks to 382 blocks by incorporating 121 peripheral blocks across Golden Hill (52), Barrio Logan (35), and Sherman Heights (34).</li>
          <li><strong>Quantifying the Wedge:</strong> Between 4.0% and 32.8% of reported post-2021 count increases were driven strictly by drawing a larger perimeter on the map. In January 2023, 641 of 1,955 reported individuals were in the expansion zone.</li>
          <li><strong>Underlying Crisis Remained Real:</strong> The balanced 261-block panel shows counts still surged +71% in 2022. The crisis was real, but naive unadjusted comparisons exaggerated growth by nearly a third.</li>
          <li><strong>Data Engineering Fix:</strong> Constructed <code>BlockPanel_Balanced_261.csv</code> to enforce strict longitudinal panel balance across all 12 digitized count dates (2018–2025).</li>
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
        <h2>Where Homelessness Concentrates: The East Village Epicenter</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.3;">
        <h4>Top Persistent Hotspots (Getis-Ord Gi*)</h4>
        <table class="data-table">
          <tr><th>Rank</th><th>Block Identifier</th><th>Area</th><th>Hotspot Dates</th><th>Rate</th><th>Transit Dist</th></tr>
          <tr><td><strong>#1</strong></td><td>16th St & Imperial Ave</td><td>South East Village</td><td>9 / 12 dates</td><td>75%</td><td>52 m</td></tr>
          <tr><td><strong>#2</strong></td><td>I-5 SB & Imperial Ave</td><td>South East Village</td><td>8 / 12 dates</td><td>67%</td><td>137 m</td></tr>
          <tr><td><strong>#3</strong></td><td>I-5 SB Off-Ramp Border</td><td>South East Village</td><td>6 / 12 dates</td><td>50%</td><td>204 m</td></tr>
          <tr><td><strong>#4</strong></td><td>I-5 SB On-Ramp Border</td><td>South East Village</td><td>4 / 12 dates</td><td>33%</td><td>154 m</td></tr>
          <tr><td><strong>#5</strong></td><td>17th St & Imperial Ave</td><td>South East Village</td><td>4 / 12 dates</td><td>33%</td><td>72 m</td></tr>
          <tr><td><strong>#6</strong></td><td>16th St & J St</td><td>South East Village</td><td>2 / 12 dates</td><td>17%</td><td>283 m</td></tr>
          <tr><td><strong>#7</strong></td><td>17th St & J St</td><td>South East Village</td><td>2 / 12 dates</td><td>17%</td><td>274 m</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE BUILT-ENVIRONMENT MAGNET</h4>
        <ul class="bullet-list">
          <li><strong>East Village Volume Dominance:</strong> Historically accounts for 54.8% of all downtown homelessness (mean 552.8 individuals). During crisis peaks, over 1,200 individuals sheltered here simultaneously.</li>
          <li><strong>100% of Top 10 in South East Village:</strong> Every single one of the top 10 persistent hotspot blocks is located south of Market Street in East Village, forming a permanent geographic cluster.</li>
          <li><strong>The Built Environment Triad:</strong> Hotspots do not occur at random; they are anchored by (1) Regional Transit Hubs (12th & Imperial Transit Center), (2) Intake Services (Father Joe's Villages, Neil Good Day Center), and (3) Caltrans freeway underpasses providing structural overhead shelter.</li>
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
        <h2>Geospatial Hotspot Dynamics: The 121-Meter Southward Displacement Vector</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_migration}" class="hero-img" alt="Centroid Migration">
      </div>
      <div class="card" style="flex: 1;">
        <h4>DRIVERS OF CLUSTER DISPLACEMENT</h4>
        <ul class="bullet-list">
          <li><strong>121-Meter Migration Vector:</strong> Between the Early Period (2018–2020) and the Recent Period (2022–2025), the count-weighted hotspot centroid migrated 121 meters south toward Commercial St and Imperial Ave.</li>
          <li><strong>Northern Right-of-Way Sweeps:</strong> Aggressive enforcement of sidewalk accessibility in commercial retail corridors (Gaslamp, Core/City Center, North East Village) pushed individuals southward.</li>
          <li><strong>Freeway & Industrial Buffer:</strong> Displaced encampments compressed into the industrial transition zone bordering Interstate 5 and the MTS rail yards, where enforcement was historically less continuous.</li>
          <li><strong>Service Gravity:</strong> Expanding safe sleeping and shelter intakes along 20th & B and Commercial Street acted as an institutional gravity well cementing the southward migration.</li>
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
        <h2>Multi-Model Machine Learning Benchmark: 5-Fold Walk-Forward Cross-Validation</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4;">
        <h4>5-Fold Walk-Forward CV Performance (96 Months, Zero Leakage)</h4>
        <table class="data-table">
          <tr><th>Model Architecture</th><th>1-Month MAPE</th><th>3-Month MAPE</th><th>6-Month MAPE</th><th>12-Month CV MAPE</th></tr>
          <tr style="background:#E6FFFA;"><td><strong>XGBoost (Champion)</strong></td><td>12.45% ± 5.8%</td><td>18.92% ± 8.4%</td><td>27.34% ± 12.6%</td><td><strong>39.34% ± 25.4%</strong></td></tr>
          <tr><td><strong>Holt-Winters Exp Smooth</strong></td><td>13.82% ± 6.2%</td><td>20.15% ± 9.1%</td><td>28.90% ± 13.8%</td><td>39.57% ± 27.6%</td></tr>
          <tr><td><strong>SARIMA (1,1,1)(0,0,0)</strong></td><td>14.10% ± 7.4%</td><td>21.50% ± 11.2%</td><td>30.45% ± 16.5%</td><td>40.10% ± 34.5%</td></tr>
          <tr><td><strong>Naive Seasonal (t-12)</strong></td><td>19.85% ± 9.5%</td><td>29.40% ± 14.2%</td><td>38.20% ± 18.9%</td><td>51.34% ± 24.5%</td></tr>
          <tr><td><strong>Prophet (Changepoints)</strong></td><td>22.30% ± 11.0%</td><td>33.15% ± 16.8%</td><td>45.80% ± 22.4%</td><td>63.81% ± 35.5%</td></tr>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <h4>CORE FORECASTING TAKEAWAYS</h4>
        <ul class="bullet-list">
          <li><strong>XGBoost Wins Citywide:</strong> Achieved lowest 12-month CV error (39.34%) and best 2025 hold-out performance (38.48%). Non-linear decision trees capture rapid velocity shifts without linear divergence.</li>
          <li><strong>Holt-Winters as Parametric Anchor:</strong> Holt-Winters achieved virtually tied accuracy (39.57%), serving as our secondary baseline to provide closed-form analytical prediction intervals.</li>
          <li><strong>Why Prophet Failed:</strong> Prophet's Bayesian changepoints overshot post-2023 counts by +63.8%, failing to adapt to the camping ordinance inflection. Fixed changepoint models should NOT be used for policy stress testing.</li>
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
        <h2>2026 Forward Outlook: Stress-Testing Three Strategic Policy Scenarios</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_forecast}" class="hero-img" alt="2026 Forecast">
      </div>
      <div class="card" style="flex: 1;">
        <h4>PROSPECTIVE 2026 SCENARIOS</h4>
        <ul class="bullet-list">
          <li><strong>Baseline (Status Quo):</strong> Monthly counts projected to remain range-bound between 850 and 920 individuals (Month 12: 890). Assumes current shelter turnover and enforcement levels.</li>
          <li><strong>Optimistic Scenario (-24% at M12):</strong> Accelerated Safe Sleeping Sites and 800 shelter beds drive downtown street counts down to ~670 individuals by December 2026.</li>
          <li><strong>Pessimistic Scenario (+26% at M12):</strong> Capacity exhaustion, shelter closures, and eviction spikes push counts back up to ~1,110 individuals by December 2026.</li>
          <li><strong>The Necessity of Uncertainty Bands:</strong> Point forecasts without prediction intervals mislead decision-makers. Planning must accommodate the calibrated 80% and 95% fan envelopes.</li>
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
        <h2>The Regional Displacement Paradox: Downtown Collapse vs. Countywide Record</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="{img_regional}" class="hero-img" alt="Regional Divergence">
      </div>
      <div class="card" style="flex: 1;">
        <h4>THE DISPLACEMENT REALITY</h4>
        <ul class="bullet-list">
          <li><strong>Downtown Share Collapsed:</strong> Downtown's share of countywide unsheltered homelessness plunged from 37.5% in January 2023 to 14.9% in January 2025.</li>
          <li><strong>Countywide Homelessness Hit Record:</strong> Simultaneously, the RTFH Point-in-Time count recorded an all-time countywide peak of 6,110 unsheltered individuals in 2024 (and 5,714 in 2025).</li>
          <li><strong>Displacement, Not Elimination:</strong> The Unsafe Camping Ordinance successfully reduced visible encampments in commercial corridors, but individuals were dispersed into riverbeds, freeway rights-of-way, and neighboring jurisdictions (El Cajon, Chula Vista, National City).</li>
          <li><strong>Regional Coordination Required:</strong> City-centric enforcement without countywide shelter capacity shifts the burden rather than solving the systemic crisis.</li>
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
        <h2>Countywide Macro Estimation Model & Mandatory Communication Rules</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1;">
        <h4>POLICY REGIME OLS CHAMPION MODEL</h4>
        <ul class="bullet-list">
          <li><strong>Constant-Ratio Assumption Rejected:</strong> One-Way ANOVA decisively rejects ratio stability across regimes: F = 66.51, p = 0.0002, eta^2 = 0.9638. A constant-ratio multiplier creates up to +96.2% error!</li>
          <li><strong>Econometric Equation:</strong><br>
            <code style="background:#EFF6FF; color:#1E40AF; padding:2px 6px; border-radius:4px; font-size:10px;">Y = 4,513.26 + 0.1859 * X + 1,225.04 * D_post</code><br>
            Where X = Downtown count, D_post = 1 under active Camping Ordinance enforcement.</li>
          <li><strong>Goodness-of-Fit:</strong> R^2 = 0.9638 | Adj R^2 = 0.9493 | LOOCV RMSE = 815.32 | Signed Bias = -0.34%.</li>
          <li><strong>Current County Estimate (Dec 2025):</strong><br>
            <strong>5,900 [95% PI: 3,900 to 8,000 individuals]</strong><br>
            Calibrated margin of error is ±2,050 individuals (±35%) using exact Student's t distribution (df=5).</li>
        </ul>
      </div>
      <div class="card" style="flex: 1.1; border-top: 4px solid var(--red-alert);">
        <h4 style="color: var(--red-alert);">THE 4 MANDATORY PUBLIC COMMUNICATION RULES</h4>
        <ul class="bullet-list">
          <li><strong>Rule 1: Prohibit Raw Single-Point Precision:</strong> Never publish uncalibrated single figures like '5,921'. False precision misleads the public and damages institutional credibility.</li>
          <li><strong>Rule 2: Mandate Rounding to Nearest 100:</strong> Always round estimated point totals to the nearest 100 individuals (e.g. mandate '5,900' instead of '5,921').</li>
          <li><strong>Rule 3: Always Publish Calibrated 95% Interval:</strong> Every headline figure MUST be accompanied by its calibrated Student's t prediction interval: <em>'5,900 [3,900 to 8,000]'</em>.</li>
          <li><strong>Rule 4: Mandatory Policy Regime Disclosure:</strong> Public statements must explicitly disclose that the +1,225 adjustment accounts for displacement following the July 2023 Camping Ordinance.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 11 of 14</strong></div>
    </div>
  </div>

  <!-- SLIDE 12: MUNICIPAL POLICY ROADMAP -->
  <div class="slide" id="slide-12">
    <div class="slide-badge">12</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Strategic Recommendations</h3>
        <h2>Municipal Policy Action Roadmap: 30-Day, 1-Year, and 3-Year Horizons</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1; border-top: 4px solid var(--royal-blue);">
        <h4 style="color: var(--royal-blue); font-size:12px;">IMMEDIATE ACTION (30–90 DAYS)</h4>
        <div style="font-size: 10px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">High-Frequency Outreach & Tool Deployment</div>
        <ul class="bullet-list">
          <li><strong>Mobile Sanitation:</strong> Deploy intensive hygiene and mobile restrooms directly to the top 10 persistent blocks (led by 16th & Imperial).</li>
          <li><strong>Dashboard Deployment:</strong> Provide City Council and County Supervisors with live dashboard access for real-time surveillance.</li>
          <li><strong>Target Metric:</strong> Zero unsheltered growth on top 5 hotspot blocks.</li>
          <li><strong>Lead:</strong> City Homelessness Strategies & DSDP.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--green-action);">
        <h4 style="color: var(--green-action); font-size:12px;">MEDIUM-TERM (6–12 MONTHS)</h4>
        <div style="font-size: 10px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Safe Sleeping & Regional Containment</div>
        <ul class="bullet-list">
          <li><strong>Scale Safe Sleeping:</strong> Expand Safe Sleeping Sites by 800 beds to capture the -24% optimistic scenario (~670 individuals).</li>
          <li><strong>Regional Taskforce:</strong> Establish joint intervention protocol with East & South County to intercept displaced encampments.</li>
          <li><strong>Target Metric:</strong> Sub-700 downtown count sustained 6+ months.</li>
          <li><strong>Lead:</strong> City of San Diego, RTFH, Caltrans.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--navy-primary);">
        <h4 style="color: var(--navy-primary); font-size:12px;">LONG-TERM (1–3 YEARS)</h4>
        <div style="font-size: 10px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">System Integration & Housing Exits</div>
        <ul class="bullet-list">
          <li><strong>Regional HMIS 2.0:</strong> Deploy integrated bed reservation system with real-time shelter vacancy tracking across all regional providers.</li>
          <li><strong>Permanent Housing:</strong> Fund 1,500 permanent supportive housing units with tenancy retention services.</li>
          <li><strong>Target Metric:</strong> 25%+ reduction in countywide unsheltered PIT.</li>
          <li><strong>Lead:</strong> County Health & Human Services, RTFH.</li>
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
        <h4>THE 6 SPECIALIZED DASHBOARD MODULES (TASK 9.1)</h4>
        <ul class="bullet-list">
          <li><strong>Tab 1: Historical Trends View:</strong> Longitudinal time series (2017–2025), dynamic multiplier regime markers, macro epoch shading, and component toggles (individuals, tents, vehicles).</li>
          <li><strong>Tab 2: 12-Month Forward Forecast:</strong> Prospective 2026 projections, model selectors (XGBoost champion, Holt-Winters, SARIMA, Prophet), shaded 80%/95% prediction fans, and scenario stress testing (-24% optimistic, +26% pessimistic).</li>
          <li><strong>Tab 3: Hotspot Surveillance Map:</strong> Folium interactive choropleth, 12 count dates selector, balanced 261 vs 382 footprint toggle, Getis-Ord Gi* classifications (90%, 95%, 99%), and centroid migration vector.</li>
          <li><strong>Tab 4: Neighborhood Decomposition:</strong> 4-pane STL decomposition (Trend, Seasonality, Residuals) and Kruskal-Wallis non-parametric significance displays.</li>
          <li><strong>Tab 5: County Estimation Calculator:</strong> Interactive Policy Regime OLS calculator strictly enforcing The 4 Public Communication Rules with Student's t prediction intervals.</li>
          <li><strong>Tab 6: Methodology & Governance:</strong> Comprehensive documentation of 4 multiplier schedules, 2022 footprint expansion (+121 blocks), and root causes for historical missing data.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1;">
        <h4>DEPLOYMENT & ACCESS INFO</h4>
        <ul class="bullet-list">
          <li><strong>Local Live URL:</strong> <code>http://localhost:8501</code> (Sub-2s load time)</li>
          <li><strong>Cloud Production URL:</strong> <code>https://downtown-sd-homelessness.streamlit.app</code></li>
          <li><strong>Automated Quality:</strong> 10 / 10 pytest unit tests passing with zero regressions.</li>
          <li><strong>Data Pipeline SLA:</strong> <code>@st.cache_data</code> provides microsecond cached lookups across all 6 tabs.</li>
          <li><strong>Target Users:</strong> City Council policy analysts, RTFH outreach coordinators, and DSDP operations directors.</li>
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
        <h2>Executive Synthesis, Data Governance & Partnership Next Steps</h2>
      </div>
    </div>
    <div class="slide-body" style="flex-direction: column; gap: 14px;">
      <div class="card" style="border-left: 5px solid var(--navy-primary);">
        <h4>1. EVIDENCE-BASED RESOURCE ALLOCATION</h4>
        <div style="font-size: 10.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">Move Beyond Seasonal Budgeting</div>
        <div style="font-size: 10px; color: var(--text-muted); line-height: 1.4;">
          Discontinue volatile seasonal budget adjustments. The empirical finding that 8 of 9 series exhibit zero seasonality mandates locking investments into permanent, year-round shelter capacity and focused sanitation on the top 10 persistent South East Village blocks.
        </div>
      </div>
      <div class="card" style="border-left: 5px solid var(--royal-blue);">
        <h4>2. REGIONAL ACCOUNTABILITY & SYSTEMS REFORM</h4>
        <div style="font-size: 10.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">Acknowledge the Regional Displacement Reality</div>
        <div style="font-size: 10px; color: var(--text-muted); line-height: 1.4;">
          Municipal enforcement in downtown corridors has displaced unsheltered individuals into surrounding municipalities and Caltrans corridors. Solving homelessness requires countywide inter-jurisdictional collaboration and real-time HMIS 2.0 bed allocation.
        </div>
      </div>
      <div class="card" style="border-left: 5px solid var(--green-action);">
        <h4>3. CONTINUOUS DATA GOVERNANCE & MACHINE LEARNING</h4>
        <div style="font-size: 10.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px;">Annual Retraining & Multi-Source Expansion</div>
        <div style="font-size: 10px; color: var(--text-muted); line-height: 1.4;">
          Retrain the Policy Regime OLS model annually upon RTFH January PIT release using the calibrated Student's t distribution. Transition to Assignment 10 to integrate NOAA weather, 311 service requests, and shelter census signals into an early warning system.
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
