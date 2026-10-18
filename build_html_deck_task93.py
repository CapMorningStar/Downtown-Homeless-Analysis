"""
Standalone HTML presentation deck generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.html
A responsive, self-contained 12-slide browser presentation styled in the Canva
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
    print(f"Generating Task 9.3 Companion HTML Presentation (12 Slides): {OUTPUT_HTML}...")

    img_trajectory = get_b64(SLIDE_ASSETS / "task93_trajectory_9year.png")
    img_forecast = get_b64(SLIDE_ASSETS / "task93_forecast_2026.png")
    img_regional = get_b64(SLIDE_ASSETS / "task93_regional_divergence.png")
    img_migration = get_b64(SLIDE_ASSETS / "task93_hotspot_migration.png")
    img_wedge = get_b64(SLIDE_ASSETS / "task93_footprint_wedge.png")
    img_seasonality = get_b64(SLIDE_ASSETS / "chart2_clean_hd.png")
    img_county_ols = get_b64(SLIDE_ASSETS / "task93_county_ols_intervals.png")

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
  .nav-btn:hover {{ background: #2643c9; }}

  .nav-indicator {{
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    padding: 0 10px;
  }}

  .deck-container {{
    display: flex;
    flex-direction: column;
    gap: 40px;
    width: 100%;
    max-width: 1240px;
  }}

  .slide {{
    width: 1240px;
    height: 700px;
    background: var(--bg-canvas);
    border-radius: 12px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
    position: relative;
    padding: 32px 48px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  .slide-badge {{
    position: absolute;
    top: 0;
    right: 48px;
    width: 80px;
    height: 60px;
    background: var(--navy-primary);
    color: #fff;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 24px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }}

  .slide-header {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-card);
  }}

  .accent-bar {{
    width: 5px;
    height: 48px;
    background: var(--royal-blue);
    border-radius: 3px;
    flex-shrink: 0;
  }}

  .header-text h3 {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--royal-blue);
    font-weight: 700;
    margin-bottom: 2px;
  }}

  .header-text h2 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--navy-primary);
    line-height: 1.2;
  }}

  .slide-body {{
    display: flex;
    gap: 20px;
    flex: 1;
    min-height: 0;
  }}

  .card {{
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 18px;
    display: flex;
    flex-direction: column;
  }}

  .callout-box {{
    background: var(--ice-tint);
    border: 1px solid var(--royal-blue);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
  }}

  .callout-title {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 11px;
    font-weight: 800;
    color: var(--navy-primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
  }}

  .callout-text {{
    font-size: 10.5px;
    font-weight: 600;
    color: var(--navy-primary);
    line-height: 1.35;
  }}

  .kpi-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 14px;
  }}

  .kpi-box {{
    flex: 1;
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
  }}

  .kpi-box.primary {{
    background: var(--navy-primary);
    border-color: var(--navy-primary);
  }}

  .kpi-box.primary .kpi-val, .kpi-box.primary .kpi-lbl {{ color: #fff; }}
  .kpi-box.primary .kpi-sub {{ color: var(--soft-blue); }}

  .kpi-val {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--navy-primary);
    line-height: 1.1;
  }}

  .kpi-lbl {{
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-dark);
    margin-top: 2px;
  }}

  .kpi-sub {{
    font-size: 8.5px;
    color: var(--text-muted);
    margin-top: 1px;
  }}

  .bullet-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .bullet-list li {{
    font-size: 10.5px;
    color: var(--text-dark);
    line-height: 1.35;
    position: relative;
    padding-left: 14px;
  }}

  .bullet-list li::before {{
    content: "•";
    color: var(--royal-blue);
    font-weight: bold;
    font-size: 14px;
    position: absolute;
    left: 0;
    top: -1px;
  }}

  .bullet-list strong {{
    color: var(--royal-blue);
    font-weight: 600;
  }}

  .hero-img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 6px;
  }}

  .slide-footer {{
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid var(--border-card);
    display: flex;
    justify-content: space-between;
    font-size: 9px;
    color: var(--text-muted);
  }}

  table.styled-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
  }}

  table.styled-table th {{
    background: var(--navy-primary);
    color: #fff;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
    font-family: 'Bricolage Grotesque', sans-serif;
  }}

  table.styled-table td {{
    padding: 7px 10px;
    border-bottom: 1px solid var(--border-card);
    color: var(--text-dark);
  }}

  table.styled-table tr:nth-child(even) {{
    background: var(--bg-canvas);
  }}

  .rule-badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    color: #fff;
    margin-right: 6px;
  }}
</style>
</head>
<body>

<div class="nav-bar">
  <button class="nav-btn" onclick="prevSlide()">◀ Previous</button>
  <div class="nav-indicator" id="slideIndicator">Slide 1 of 12</div>
  <button class="nav-btn" onclick="nextSlide()">Next ▶</button>
</div>

<div class="deck-container">

  <!-- SLIDE 1: TITLE SLIDE -->
  <div class="slide" id="slide-1">
    <div class="slide-badge">01</div>
    <div class="slide-body" style="align-items: center; justify-content: center;">
      <div class="card" style="width: 100%; height: 100%; padding: 45px 55px; justify-content: space-between;">
        <div>
          <div style="display:inline-block; background:var(--ice-tint); border:1px solid var(--soft-blue); padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700; color:var(--navy-primary); margin-bottom:18px;">
            DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS
          </div>
          <h1 style="font-family:'Bricolage Grotesque',sans-serif; font-size:36px; font-weight:800; color:var(--navy-primary); line-height:1.2; margin-bottom:10px;">
            Downtown San Diego Unsheltered<br>Homeless Population Analysis
          </h1>
          <p style="font-size:16px; font-weight:600; color:var(--royal-blue); margin-bottom:12px;">
            Longitudinal Modeling, Spatial Dynamics & Macro Policy Governance (2017–2025)
          </p>
          <p style="font-size:13px; color:var(--text-muted);">
            Kyaw Soe Lwin | Data Science Alliance Lead Project Deliverable
          </p>
        </div>
        <div style="border-top:1px solid var(--border-card); padding-top:20px; display:grid; grid-template-columns: repeat(3, 1fr); gap:20px;">
          <div>
            <div style="font-size:10px; font-weight:700; color:var(--royal-blue); text-transform:uppercase;">Longitudinal Scope</div>
            <div style="font-size:12px; color:var(--text-dark); margin-top:3px;">9 Years • 108 Months (2017–2025)<br>7 Downtown Neighborhoods</div>
          </div>
          <div>
            <div style="font-size:10px; font-weight:700; color:var(--royal-blue); text-transform:uppercase;">Dual Data Pipeline</div>
            <div style="font-size:12px; color:var(--text-dark); margin-top:3px;">DSDP Monthly Field Counts<br>+ RTFH Regional PIT Census</div>
          </div>
          <div>
            <div style="font-size:10px; font-weight:700; color:var(--royal-blue); text-transform:uppercase;">Production Deliverables</div>
            <div style="font-size:12px; color:var(--text-dark); margin-top:3px;">12-Slide Deck • 7-Tab Streamlit App<br>Strategic Action Roadmap (R1–R8)</div>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 01 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 2: MACRO TRAJECTORY -->
  <div class="slide" id="slide-2">
    <div class="slide-badge">02</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Longitudinal Epidemiology</h3>
        <h2>Macro Trajectory: Three Distinct Epochs Across 9 Years (2017–2025)</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val">529</div>
            <div class="kpi-lbl">Series Low</div>
            <div class="kpi-sub">March 2020 (COVID)</div>
          </div>
          <div class="kpi-box primary">
            <div class="kpi-val">2,103</div>
            <div class="kpi-lbl">Series Peak</div>
            <div class="kpi-sub">May 2023 (Crisis)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-val">851</div>
            <div class="kpi-lbl">Jan 2025 Count</div>
            <div class="kpi-sub">−59.5% from peak</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Downtown San Diego experienced 3 distinct epochs across 9 years—contraction, crisis peak, and policy stabilization—with 4 unpublished months in 2025.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>Epoch 1 (2017–2020):</strong> Baseline contraction from 882 to all-time series low of 529 in March 2020 during initial COVID de-densification.</li>
            <li><strong>Epoch 2 (2021–2023):</strong> Post-pandemic surge of +297%, peaking at 2,103 in May 2023 driven by evictions, inflation, and street encampments.</li>
            <li><strong>Epoch 3 (2024–2025):</strong> Enforcement stabilization; Jan 2025 count dropped to 851 (−59.5% from peak), ending Dec 2025 at 985.</li>
            <li><strong>2025 Data Notice:</strong> Jul, Aug, Oct, Nov unpublished by DSDP; handled with honest interpolation and explicit data gap indicators.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_trajectory}" class="hero-img" alt="9-Year Trajectory">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 02 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 3: ADMINISTRATIVE FOOTPRINT ARTIFACT -->
  <div class="slide" id="slide-3">
    <div class="slide-badge">03</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Spatial Measurement</h3>
        <h2>Measurement Validity: The 2022 Footprint Expansion Artifact</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val">+121</div>
            <div class="kpi-lbl">Added Blocks</div>
            <div class="kpi-sub">Oct 2022 (+46.4%)</div>
          </div>
          <div class="kpi-box" style="border-top:3px solid var(--amber-warn);">
            <div class="kpi-val" style="color:var(--amber-warn);">32.8%</div>
            <div class="kpi-lbl">Peak Wedge</div>
            <div class="kpi-sub">641 of 1,955 in Jan 2023</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-val" style="font-size:16px;">261 vs 382</div>
            <div class="kpi-lbl">Dual Metrics</div>
            <div class="kpi-sub">Core vs Expanded</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Over 32% of the apparent 2023 surge was an administrative measurement artifact caused by expanding the count perimeter by 121 blocks.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>Perimeter Expansion:</strong> In Oct 2022, DSDP expanded its counting footprint from 261 to 382 blocks (+46.4%), absorbing perimeter highway zones.</li>
            <li><strong>Wedge Quantification:</strong> In Jan 2023, the added 121 blocks contributed 641 of 1,955 total individuals (32.8% of the entire reported count).</li>
            <li><strong>Persistent Effect:</strong> Even in Jan 2025, the expansion wedge accounts for 84 of 847 spatial individuals (10.0% of total count).</li>
            <li><strong>Policy Directive (R3):</strong> City reporting must mandate dual-series metrics (Core 261 vs Expanded 382) to avoid false longitudinal claims.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_wedge}" class="hero-img" alt="Footprint Wedge">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 03 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 4: SEASONALITY QUANTIFIED -->
  <div class="slide" id="slide-4">
    <div class="slide-badge">04</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Temporal Decomposition</h3>
        <h2>Seasonality Quantified: Invariant Summer Peaks vs Policy Forces</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val">August</div>
            <div class="kpi-lbl">Seasonal Peak</div>
            <div class="kpi-sub">+9.4% above baseline</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-val">April</div>
            <div class="kpi-lbl">Seasonal Trough</div>
            <div class="kpi-sub">−10.8% below baseline</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-val" style="font-size:16px;">p = 0.995</div>
            <div class="kpi-lbl">Kruskal-Wallis</div>
            <div class="kpi-sub">H = 2.66 (Not sig.)</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Seasonal cycles peak in August (+9.4%) and trough in April (−10.8%), but non-parametric ANOVA (p=0.995) confirms policy regimes drive 90%+ of variance.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>Additive Seasonal Swing:</strong> STL decomposition reveals a consistent seasonal amplitude of ±110 individuals, peaking in warm summer months (July–August).</li>
            <li><strong>Statistical Significance:</strong> Kruskal-Wallis test across calendar months yields H = 2.66, p = 0.995 (11 d.f.), indicating seasonality is subordinate to macro trend.</li>
            <li><strong>Operational Implication:</strong> Seasonal changes require flexible shelter surge beds in summer, but cannot explain multi-year hundred-person swings.</li>
            <li><strong>Strategic Outreach Window:</strong> April spring trough represents the optimal intervention window before the annual summer influx begins.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_seasonality}" class="hero-img" alt="Seasonality Analysis">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 04 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 5: STRUCTURAL BREAK CHRONOLOGY -->
  <div class="slide" id="slide-5">
    <div class="slide-badge">05</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Policy Intervention Timeline</h3>
        <h2>Chronology of Policy Regimes & Structural Breaks (2017–2025)</h2>
      </div>
    </div>
    <div class="slide-body" style="flex-direction:column; gap:14px;">
      <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px;">
        <div class="card" style="border-top:4px solid var(--royal-blue);">
          <div style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--royal-blue); margin-bottom:2px;">
            REGIME 1: BASELINE & HEPATITIS A (2017–2019)
          </div>
          <div style="font-size:10px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">Sanitation infrastructure & initial shelter tents</div>
          <ul class="bullet-list">
            <li><strong>Hepatitis A Outbreak:</strong> Emergency street power-washing and 3 bridge shelters opened.</li>
            <li><strong>Count Trajectory:</strong> Gradual contraction from 882 to ~750 individuals.</li>
            <li><strong>Multiplier Change:</strong> Transitioned tent multiplier from 2.0 to 1.75 in April 2017.</li>
          </ul>
        </div>
        <div class="card" style="border-top:4px solid var(--teal-champ);">
          <div style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--teal-champ); margin-bottom:2px;">
            REGIME 2: COVID-19 EMERGENCY RESPONSE (2020)
          </div>
          <div style="font-size:10px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">Mass congregate sheltering & de-densification</div>
          <ul class="bullet-list">
            <li><strong>Operation Shelter to Home:</strong> Convention Center sheltered up to 1,300 people.</li>
            <li><strong>Series Low Reached:</strong> Street counts dropped to 529 in March 2020 trough.</li>
            <li><strong>HUD Waiver:</strong> HUD granted count waivers in 2021; unsheltered census suspended.</li>
          </ul>
        </div>
        <div class="card" style="border-top:4px solid var(--amber-warn);">
          <div style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--amber-warn); margin-bottom:2px;">
            REGIME 3: CRISIS REBOUND & SURGE (2021–2023)
          </div>
          <div style="font-size:10px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">Post-COVID economic shocks & perimeter expansion</div>
          <ul class="bullet-list">
            <li><strong>Convention Center Closes:</strong> People returned to streets as emergency beds ended.</li>
            <li><strong>Historical Peak:</strong> Count reached 2,103 in May 2023 (+297% from 2020 low).</li>
            <li><strong>Footprint Added:</strong> October 2022 added 121 blocks, adding 641 people in Jan 2023.</li>
          </ul>
        </div>
        <div class="card" style="border-top:4px solid var(--green-action);">
          <div style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--green-action); margin-bottom:2px;">
            REGIME 4: CAMPING ORDINANCE & STABILIZATION (2024–2025)
          </div>
          <div style="font-size:10px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">Enforcement, Safe Sleeping sites & displacement</div>
          <ul class="bullet-list">
            <li><strong>Unsafe Camping Ordinance:</strong> Enforced July 2023; sidewalk tents prohibited.</li>
            <li><strong>Downtown Drops:</strong> Counts fell to 851 in Jan 2025 and 985 in Dec 2025.</li>
            <li><strong>Regional Divergence:</strong> County unsheltered rose to 6,110 (2024); displacement reality.</li>
          </ul>
        </div>
      </div>
      <div class="callout-box" style="margin-bottom:0;">
        <div class="callout-title">Executive Insight</div>
        <div class="callout-text">Macro policy interventions create immediate spatial displacement rather than net exits from homelessness. Enforcement in one zone redistributes individuals across municipal borders.</div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 05 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 6: SPATIAL CONCENTRATION & 120M MIGRATION (MERGED) -->
  <div class="slide" id="slide-6">
    <div class="slide-badge">06</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Geospatial Clustering</h3>
        <h2>Spatial Concentration: 54% East Village Core & 120m SSE Migration</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val">54.0%</div>
            <div class="kpi-lbl">East Village Share</div>
            <div class="kpi-sub">Over half of downtown count</div>
          </div>
          <div class="kpi-box" style="border-top:3px solid var(--red-alert);">
            <div class="kpi-val" style="color:var(--red-alert);">120.4 m</div>
            <div class="kpi-lbl">Centroid Shift</div>
            <div class="kpi-sub">Bearing 160.1° SSE</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Downtown homelessness is hyper-concentrated in East Village (54%), with the cluster centroid migrating 120m SSE toward Imperial Ave due to sidewalk enforcement.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>Hyper-Concentration:</strong> East Village accounts for 54.0% of all downtown unsheltered individuals. City Center ranks second at ~18%.</li>
            <li><strong>120m Centroid Shift:</strong> Between 2018–2020 and 2022–2025, the weighted hotspot center shifted 120.4 meters SSE (160.1° bearing) toward Imperial Ave.</li>
            <li><strong>Top Persistent Hotspots:</strong> 100% of top 10 Getis-Ord Gi* clusters are in South East Village: 16th & Imperial (9/12 dates), I-5 SB & Imperial (8/12).</li>
            <li><strong>Outreach Focus (R1):</strong> Target mobile hygiene, medical vans, and outreach teams at 16th-17th & Imperial Ave corridor.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_migration}" class="hero-img" alt="Hotspot Migration">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 06 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 7: MACHINE LEARNING CV BENCHMARK -->
  <div class="slide" id="slide-7">
    <div class="slide-badge">07</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Predictive Intelligence</h3>
        <h2>Machine Learning: 5-Fold Cross-Validation Benchmark</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.4;">
        <h4 style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--navy-primary); margin-bottom:10px;">5-FOLD CROSS-VALIDATION ERROR COMPARISON</h4>
        <table class="styled-table">
          <thead>
            <tr>
              <th>Model Architecture</th>
              <th>1-Month MAPE</th>
              <th>3-Month MAPE</th>
              <th>6-Month MAPE</th>
              <th>12-Month CV MAPE</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>SARIMA (ACF/PACF Grid)</td>
              <td><strong>5.4% ± 4.1%</strong></td>
              <td>14.3% ± 10.3%</td>
              <td>24.7% ± 20.9%</td>
              <td>39.6% ± 35.5%</td>
            </tr>
            <tr>
              <td>Holt-Winters Exp Smooth</td>
              <td>13.0% ± 9.2%</td>
              <td>17.6% ± 10.4%</td>
              <td>25.2% ± 18.2%</td>
              <td>38.4% ± 28.5%</td>
            </tr>
            <tr style="background:#EFF6FF; font-weight:bold;">
              <td style="color:var(--royal-blue);">XGBoost (Champion)</td>
              <td style="color:var(--royal-blue);">14.0% ± 8.9%</td>
              <td style="color:var(--royal-blue);">19.9% ± 14.8%</td>
              <td style="color:var(--royal-blue);">26.7% ± 18.5%</td>
              <td style="color:var(--royal-blue);">38.3% ± 26.0%</td>
            </tr>
            <tr>
              <td>Naive Seasonal (t−12)</td>
              <td>39.5% ± 31.9%</td>
              <td>40.1% ± 31.3%</td>
              <td>48.5% ± 35.4%</td>
              <td>51.7% ± 24.5%</td>
            </tr>
            <tr>
              <td>Prophet (Changepoints)</td>
              <td>42.9% ± 26.0%</td>
              <td>42.7% ± 26.0%</td>
              <td>51.3% ± 31.9%</td>
              <td>64.2% ± 35.4%</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card" style="flex: 1;">
        <div class="callout-box">
          <div class="callout-title">Production Winner</div>
          <div class="callout-text">XGBoost is our champion production model with 38.3% 12-month CV MAPE and 8.5% 2025 hold-out error, outperforming Prophet by over 25 percentage points.</div>
        </div>
        <ul class="bullet-list">
          <li><strong>Short vs Long Horizons:</strong> SARIMA leads at 1-month (5.4% MAPE); XGBoost matches Holt-Winters at 12-months (38.3%) while exhibiting tighter variance.</li>
          <li><strong>Hold-Out Validation:</strong> On 2025 out-of-time hold-out months, XGBoost achieved 8.5% error, confirming robust generalization under policy shifts.</li>
          <li><strong>Prophet Vulnerability:</strong> Prophet failed severely (64.2% MAPE) because automated linear changepoints missed the steep post-ordinance drop.</li>
          <li><strong>Deployment Pipeline:</strong> XGBoost embedded into Tab 2 of Streamlit application with automatic quarterly retraining cues.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 07 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 8: 2026 FORWARD OUTLOOK -->
  <div class="slide" id="slide-8">
    <div class="slide-badge">08</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Prospective Forecasting</h3>
        <h2>2026 Forward Outlook: 12-Month Projections & Stress Scenarios</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val" style="font-size:17px;">816–896</div>
            <div class="kpi-lbl">Baseline Forecast</div>
            <div class="kpi-sub">Stable range through 2026</div>
          </div>
          <div class="kpi-box" style="border-top:3px solid var(--green-action);">
            <div class="kpi-val" style="color:var(--green-action);">~675</div>
            <div class="kpi-lbl">Optimistic</div>
            <div class="kpi-sub">−24% housing exits</div>
          </div>
          <div class="kpi-box" style="border-top:3px solid var(--red-alert);">
            <div class="kpi-val" style="color:var(--red-alert);">~1,123</div>
            <div class="kpi-lbl">Pessimistic</div>
            <div class="kpi-sub">+26% shelter cuts</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Baseline 2026 forecast projects Downtown unsheltered counts to remain range-bound at 816–896 individuals, but city leaders must budget for the 675–1,123 stress-test envelope.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>Stable Baseline:</strong> Under current enforcement, downtown counts remain flat at ~850 individuals throughout 2026 (Nov peak: 896; Dec M12: 888).</li>
            <li><strong>Stress-Test Envelope:</strong> Optimistic (~675, −24%) and Pessimistic (~1,123, +26%) scenarios model plausible policy and economic variations.</li>
            <li><strong>Uncertainty Bounds:</strong> 80% PI [660–1,116] and 95% PI [539–1,237] at M12 account for residual volatility and seasonal swings.</li>
            <li><strong>Budget Directive (R2):</strong> Municipal budgets must plan across the 675–1,123 envelope rather than relying on a single static number.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_forecast}" class="hero-img" alt="2026 Forecast">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 08 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 9: REGIONAL DIVERGENCE -->
  <div class="slide" id="slide-9">
    <div class="slide-badge">09</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Regional Policy Dynamics</h3>
        <h2>Regional Divergence: Downtown Drops vs Countywide Unsheltered Highs</h2>
      </div>
    </div>
    <div class="slide-body">
      <div style="flex: 1; display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-row">
          <div class="kpi-box primary">
            <div class="kpi-val">14.9%</div>
            <div class="kpi-lbl">Downtown Share</div>
            <div class="kpi-sub">Fell from 37.5% peak</div>
          </div>
          <div class="kpi-box" style="border-top:3px solid var(--red-alert);">
            <div class="kpi-val" style="color:var(--red-alert);">6,110</div>
            <div class="kpi-lbl">County High (2024)</div>
            <div class="kpi-sub">Record unsheltered PIT</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-val">5,714</div>
            <div class="kpi-lbl">County PIT (2025)</div>
            <div class="kpi-sub">High regional baseline</div>
          </div>
        </div>
        <div class="card" style="flex: 1;">
          <div class="callout-box">
            <div class="callout-title">Key Takeaway</div>
            <div class="callout-text">Downtown counts dropped 56%, but County unsheltered hit an all-time record of 6,110—proving Downtown enforcement displaced people into surrounding jurisdictions.</div>
          </div>
          <ul class="bullet-list">
            <li><strong>The Regional Paradox:</strong> Downtown Jan count plunged from 1,939 to 851 (−56%), yet countywide unsheltered homelessness reached historical record highs (6,110 in 2024, 5,714 in 2025).</li>
            <li><strong>Share Collapse:</strong> Downtown's share of county unsheltered collapsed from 37.5% in 2023 to 14.9% in 2025.</li>
            <li><strong>Displacement Dynamics:</strong> Sidewalk clearance displaced encampments along trolley corridors, canyon edges, and into neighbouring East/South County jurisdictions.</li>
            <li><strong>Evaluation Caveat:</strong> Macro divergence is proven by paired data; tracking individual migration requires unified HMIS data linkage (R5).</li>
          </ul>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_regional}" class="hero-img" alt="Regional Divergence">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 09 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 10: MACRO OLS MODEL & THE 4 RULES -->
  <div class="slide" id="slide-10">
    <div class="slide-badge">10</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Macro Econometrics & Governance</h3>
        <h2>Macro Econometric Model & The 4 Public Communication Rules</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1; border-top:4px solid var(--red-alert);">
        <h4 style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--red-alert); margin-bottom:10px;">
          THE 4 MANDATORY PUBLIC COMMUNICATION RULES
        </h4>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="background:var(--bg-canvas); border-left:3px solid var(--red-alert); padding:8px 10px; border-radius:4px;">
            <div style="font-size:11px; font-weight:700; color:var(--red-alert);">Rule 1: Eliminate False Precision</div>
            <div style="font-size:9.5px; color:var(--text-dark); margin-top:2px;">Never quote raw single points (e.g. '5,921'). Claiming exact single-person precision with n=8 data points destroys public credibility.</div>
          </div>
          <div style="background:var(--bg-canvas); border-left:3px solid var(--amber-warn); padding:8px 10px; border-radius:4px;">
            <div style="font-size:11px; font-weight:700; color:var(--amber-warn);">Rule 2: Mandate Rounding to 100</div>
            <div style="font-size:9.5px; color:var(--text-dark); margin-top:2px;">Always report headline estimates rounded to the nearest hundred: quote <strong>'about 5,900 individuals'</strong>.</div>
          </div>
          <div style="background:var(--bg-canvas); border-left:3px solid var(--green-action); padding:8px 10px; border-radius:4px;">
            <div style="font-size:11px; font-weight:700; color:var(--green-action);">Rule 3: Always State 95% Prediction Interval</div>
            <div style="font-size:9.5px; color:var(--text-dark); margin-top:2px;">Every point estimate must be paired with calibrated Student's t range: <strong>'5,900 [3,900 to 8,000]'</strong> (margin of error ±2,050 / ±35%).</div>
          </div>
          <div style="background:var(--bg-canvas); border-left:3px solid var(--royal-blue); padding:8px 10px; border-radius:4px;">
            <div style="font-size:11px; font-weight:700; color:var(--royal-blue);">Rule 4: Disclose Policy Regime Assumptions</div>
            <div style="font-size:9.5px; color:var(--text-dark); margin-top:2px;">State model assumptions: Y = 4,513 + 0.186X + 1,225*D_post. True fit is <strong>R² = 0.504</strong> (0.964 is ANOVA effect size η², not R²).</div>
          </div>
        </div>
      </div>
      <div class="card" style="flex: 1.4; display:flex; align-items:center; justify-content:center; padding:10px;">
        <img src="{img_county_ols}" class="hero-img" alt="Macro OLS & Intervals">
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 10 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 11: MUNICIPAL POLICY ROADMAP (R1–R8) -->
  <div class="slide" id="slide-11">
    <div class="slide-badge">11</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Strategic Recommendations</h3>
        <h2>Municipal Policy Action Roadmap: Recommendations (R1–R8)</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1; border-top: 4px solid var(--royal-blue);">
        <h4 style="color: var(--royal-blue); font-size:11.5px; font-family:'Bricolage Grotesque',sans-serif;">IMMEDIATE (0–3 MONTHS)</h4>
        <div style="font-size: 11px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Outreach, Standards & Boundaries</div>
        <ul class="bullet-list">
          <li><strong>R1. Persistent Hotspot Surge:</strong> Deploy mobile hygiene, medical vans, and outreach directly to 16th-17th & Imperial corridor.</li>
          <li><strong>R2. Mandate Range Planning:</strong> Enforce The 4 Communication Rules (5,900 [3,900–8,000]) across all municipal reports and budget allocations.</li>
          <li><strong>R3. Disclose Footprint Wedge:</strong> Require dual reporting (Core 261 vs Expanded 382 blocks) to maintain longitudinal data integrity.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--green-action);">
        <h4 style="color: var(--green-action); font-size:11.5px; font-family:'Bricolage Grotesque',sans-serif;">MEDIUM-TERM (6–12 MONTHS)</h4>
        <div style="font-size: 11px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">Data Rigor & Regional Audits</div>
        <ul class="bullet-list">
          <li><strong>R4. Component Sub-Totals:</strong> Restore separate tent, vehicle, and individual street count breakdowns in monthly DSDP reports.</li>
          <li><strong>R5. Displacement Tracking:</strong> Launch joint City-County surveillance along transit corridors, riverbeds, and unincorporated areas.</li>
          <li><strong>R6. Retrain OLS Estimators:</strong> Update regression coefficients with incoming 2026 RTFH Point-in-Time benchmark counts.</li>
          <li><strong>R7. Shelter Bed Integration:</strong> Incorporate real-time Housing Inventory Count (HIC) bed occupancy into monthly analytics.</li>
        </ul>
      </div>
      <div class="card" style="flex: 1; border-top: 4px solid var(--navy-primary);">
        <h4 style="color: var(--navy-primary); font-size:11.5px; font-family:'Bricolage Grotesque',sans-serif;">LONG-TERM (1–3 YEARS)</h4>
        <div style="font-size: 11px; font-weight:700; color:var(--text-dark); margin-bottom:8px;">System Digitization & Governance</div>
        <ul class="bullet-list">
          <li><strong>R8. Complete Map Digitization:</strong> Digitize remaining 78 historical block-level PDF tally maps (2017–2022) to establish block-level panel.</li>
          <li><strong>Unified Regional HMIS:</strong> Link City DSDP field counts with County Homeless Management Information System (HMIS) records.</li>
          <li><strong>True Regional Evaluation:</strong> Measure net permanent housing exits rather than local sidewalk clearance.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 11 of 12</strong></div>
    </div>
  </div>

  <!-- SLIDE 12: INTERACTIVE DASHBOARD & SYNTHESIS -->
  <div class="slide" id="slide-12">
    <div class="slide-badge">12</div>
    <div class="slide-header">
      <div class="accent-bar"></div>
      <div class="header-text">
        <h3>Operational Tool & Synthesis</h3>
        <h2>Interactive Decision-Support Tool & Executive Synthesis</h2>
      </div>
    </div>
    <div class="slide-body">
      <div class="card" style="flex: 1.1;">
        <h4 style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--navy-primary); margin-bottom:8px;">
          7 DECISION-SUPPORT MODULES (STREAMLIT APP)
        </h4>
        <ul class="bullet-list" style="gap:5px;">
          <li><strong>Tab 1: History:</strong> Multi-year trajectory with policy epoch overlays (2017–2025).</li>
          <li><strong>Tab 2: Forecast:</strong> XGBoost 12-month projections, 95% fans & scenario stress-testing.</li>
          <li><strong>Tab 3: Hotspots:</strong> Interactive Getis-Ord Gi* cluster maps and centroid migration vector.</li>
          <li><strong>Tab 4: Seasonality:</strong> STL decomposition with month-of-year seasonal indices.</li>
          <li><strong>Tab 5: Calculator:</strong> County macro estimator strictly enforcing The 4 Communication Rules.</li>
          <li><strong>Tab 6: Methods:</strong> Multiplier transparency, perimeter changes, and documentation.</li>
          <li><strong>Tab 7: Alerts:</strong> Anomaly surveillance matrix and CUSUM early-warning monitoring.</li>
        </ul>
        <div style="border-top:1px solid var(--border-card); margin-top:8px; padding-top:6px; font-size:9.5px; color:var(--text-muted);">
          <div>• <strong>Local Server:</strong> <code>http://localhost:8501</code> (Instant response)</div>
          <div>• <strong>Cloud URL:</strong> <code>https://downtown-sd-homelessness.streamlit.app</code></div>
          <div>• <strong>Test Suite:</strong> 46/46 unit tests passing • Sub-second <code>@st.cache_data</code></div>
        </div>
      </div>
      <div class="card" style="flex: 1.1;">
        <h4 style="font-family:'Bricolage Grotesque',sans-serif; font-size:12px; font-weight:800; color:var(--navy-primary); margin-bottom:8px;">
          EXECUTIVE SYNTHESIS & CORE TAKEAWAYS
        </h4>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="border-left:3px solid var(--royal-blue); padding-left:8px;">
            <div style="font-size:10.5px; font-weight:700; color:var(--royal-blue);">Pillar 1: Regional Displacement Reality</div>
            <div style="font-size:9.2px; color:var(--text-dark);">Downtown counts dropped to 851, but county unsheltered reached record highs (6,110). Enforcement redistributes individuals; reduction requires regional shelter and permanent housing capacity.</div>
          </div>
          <div style="border-left:3px solid var(--amber-warn); padding-left:8px;">
            <div style="font-size:10.5px; font-weight:700; color:var(--amber-warn);">Pillar 2: Honest Uncertainty Quantification</div>
            <div style="font-size:9.2px; color:var(--text-dark);">Point estimates without intervals mislead public officials. Mandating Rule 2 (5,900) and Rule 3 ([3,900 to 8,000]) protects municipal credibility and anchors realistic budgeting.</div>
          </div>
          <div style="border-left:3px solid var(--green-action); padding-left:8px;">
            <div style="font-size:10.5px; font-weight:700; color:var(--green-action);">Pillar 3: Unified Data Infrastructure</div>
            <div style="font-size:9.2px; color:var(--text-dark);">Measuring progress requires linking street counts with shelter bed inventories, component breakdowns, and HMIS tracking to measure human exits rather than block clearances.</div>
          </div>
        </div>
        <div class="callout-box" style="margin-top:10px; margin-bottom:0;">
          <div class="callout-title">Discussion & Q&A</div>
          <div class="callout-text">Executive presentation concluded. Ready for scenario walk-throughs, stakeholder questions, and live Streamlit dashboard demonstration.</div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div>Data Science Alliance • Downtown San Diego Homeless Population Analysis</div>
      <div><strong>Slide 12 of 12</strong></div>
    </div>
  </div>

</div>

<script>
  let currentSlide = 1;
  const totalSlides = 12;

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
