import os, base64

def get_b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img_c27 = get_b64("slide_assets/chart1_clean_hd.png")
img_c30 = get_b64("slide_assets/chart2_clean_hd.png")
img_c33 = get_b64("slide_assets/chart7_yoy_hd.png")
img_c48 = get_b64("slide_assets/chart8_clean_hd.png")
img_c51 = get_b64("slide_assets/chart9_clean_hd.png")

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Downtown San Diego Homeless Population Analysis - EDA Findings (Canva Theme)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Poppins:wght@400;500;600;700&display=swap');

  :root {
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
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Poppins', sans-serif;
    background-color: #0c101d;
    color: var(--text-dark);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
  }
  .slide-container {
    display: flex;
    flex-direction: column;
    gap: 40px;
    width: 100%;
    max-width: 1200px;
  }
  .slide {
    width: 1200px;
    height: 675px;
    background: var(--bg-canvas);
    border-radius: 12px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.35);
    position: relative;
    padding: 35px 50px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .slide-badge {
    position: absolute;
    top: 0;
    right: 50px;
    width: 100px;
    height: 75px;
    background: var(--navy-primary);
    color: #fff;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 28px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  }
  .header-zone {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    border-bottom: 1px solid var(--border-card);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  .accent-bar {
    width: 5px;
    height: 65px;
    background: var(--royal-blue);
    border-radius: 3px;
    flex-shrink: 0;
  }
  .header-content h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--navy-primary);
    line-height: 1.15;
  }
  .header-content .subtitle {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--royal-blue);
    margin-bottom: 3px;
  }
  .footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 38px;
    border-top: 1px solid var(--border-card);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 50px;
    font-size: 11px;
    color: var(--text-muted);
    background: var(--bg-canvas);
  }
  .content-2col {
    display: grid;
    grid-template-columns: 4.8fr 7.2fr;
    gap: 20px;
    flex: 1;
    height: calc(100% - 95px);
  }
  .card {
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(41, 62, 156, 0.04);
  }
  .chart-card {
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 1px 4px rgba(41, 62, 156, 0.04);
  }
  .chart-card img {
    max-width: 100%;
    max-height: 410px;
    object-fit: contain;
  }
  .chart-caption {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 8px;
    text-align: center;
  }
  .kpi-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 12px;
  }
  .kpi-card {
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 10px 12px;
  }
  .kpi-card.hero {
    background: linear-gradient(135deg, var(--navy-primary) 0%, var(--royal-blue) 100%);
    color: #fff;
    border: none;
  }
  .kpi-val {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 22px;
    font-weight: 700;
  }
  .kpi-lbl {
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .kpi-sub { font-size: 8.5px; opacity: 0.85; }
  .bullet-item { margin-bottom: 8px; font-size: 12px; line-height: 1.45; }
  .bullet-title { font-weight: 700; color: var(--navy-primary); }
  .callout {
    background: var(--ice-tint);
    border-left: 3px solid var(--royal-blue);
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    color: var(--navy-primary);
    margin-bottom: 10px;
  }
  .grid-2x2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 16px;
    flex: 1;
    height: calc(100% - 95px);
  }
  .h-card {
    background: var(--bg-white);
    border: 1px solid var(--border-card);
    border-radius: 8px;
    padding: 16px;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .h-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; }
  .h-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--navy-primary);
    margin-bottom: 2px;
  }
  .h-sub { font-size: 9.5px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 5px; }
  .h-desc { font-size: 11.5px; line-height: 1.4; color: var(--text-dark); margin-bottom: 6px; }
  .h-action { font-size: 10.5px; font-weight: 600; color: var(--navy-primary); }
</style>
</head>
<body>
<div class="slide-container">
"""

slides_part1 = f"""
  <!-- SLIDE 1: TITLE SLIDE (Canva Style) -->
  <div class="slide" id="slide-1">
    <div style="background: var(--bg-white); border: 1px solid var(--border-card); border-radius: 12px; padding: 45px 55px; height: calc(100% - 40px); display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="display: inline-block; background: var(--ice-tint); border: 1px solid var(--soft-blue); color: var(--navy-primary); font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 9999px; margin-bottom: 25px;">
          DATA SCIENCE ALLIANCE • TASK 2.3 CHECK-IN
        </div>
        <h1 style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 38px; color: var(--navy-primary); font-weight: 800; line-height: 1.2; margin-bottom: 16px;">
          Downtown San Diego Unsheltered<br>Homeless Population: EDA Findings
        </h1>
        <div style="font-size: 19px; font-weight: 700; color: var(--royal-blue); margin-bottom: 30px;">
          Kyaw Soe Lwin | Data Science Alliance | 2017–2025
        </div>
      </div>
      <div style="border-top: 1px solid var(--border-card); padding-top: 25px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div>
          <div style="font-size: 10px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Source Data</div>
          <div style="font-size: 12px; color: var(--text-dark);">Downtown San Diego Partnership (DSDP) Clean & Safe monthly counts</div>
        </div>
        <div>
          <div style="font-size: 10px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Longitudinal Scope</div>
          <div style="font-size: 12px; color: var(--text-dark);">2017–2025 (8 full & partial calendar years, 7 downtown neighborhoods)</div>
        </div>
        <div>
          <div style="font-size: 10px; font-weight: 700; color: var(--royal-blue); text-transform: uppercase; margin-bottom: 4px;">Analysis Focus</div>
          <div style="font-size: 12px; color: var(--text-dark);">Overall trajectory, seasonality, COVID dip, methodology & spatial dynamics</div>
        </div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 1 of 8</span>
    </div>
  </div>

  <!-- SLIDE 2: OVERALL TREND -->
  <div class="slide" id="slide-2">
    <div class="slide-badge">02</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Longitudinal Analysis</div>
        <h1>Overall Longitudinal Trend: Three Distinct Phases (2017–2025)</h1>
      </div>
    </div>
    <div class="content-2col">
      <div style="display: flex; flex-direction: column;">
        <div class="kpi-row">
          <div class="kpi-card hero"><div class="kpi-val">529</div><div class="kpi-lbl">Series Low</div><div class="kpi-sub">March 2020</div></div>
          <div class="kpi-card hero"><div class="kpi-val">2,103</div><div class="kpi-lbl">Series Peak</div><div class="kpi-sub">May 2023</div></div>
          <div class="kpi-card"><div class="kpi-val" style="color: var(--navy-primary);">156.8</div><div class="kpi-lbl" style="color: var(--navy-primary);">Grand Mean</div><div class="kpi-sub" style="color: var(--text-muted);">Per neigh-mo</div></div>
        </div>
        <div class="card" style="flex: 1;">
          <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 10px;">Trajectory Overview: Three Clear Phases</div>
          <div class="bullet-item">
            <span class="bullet-title">• 2017–2020 Decline:</span>
            Annual average fell from 176.31 to 109.02 (~-38% cumulative drop). YoY changes: -18.98% (2018), -4.94% (2019), and -19.71% (2020).
          </div>
          <div class="bullet-item">
            <span class="bullet-title">• 2021–2023 Rebound & Peak:</span>
            Counts rebounded sharply: +25.85% (2021) and +57.63% (2022), reaching an annual average of 223.98 in 2023 — more than double the 2020 trough.
          </div>
          <div class="bullet-item">
            <span class="bullet-title">• 2024–2025 Pullback & Stabilization:</span>
            A steep -43.52% drop in 2024 brought the annual average down to 126.50; 2025 remained roughly flat (-2.94%) at 122.78.
          </div>
        </div>
      </div>
      <div class="chart-card">
        <img src="{img_c27}" alt="Chart 1: Overall Time Series">
        <div class="chart-caption">Chart 1 (EDA Notebook): Citywide monthly total unsheltered count with methodology regime boundaries.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 2 of 8</span>
    </div>
  </div>

  <!-- SLIDE 3: SEASONALITY -->
  <div class="slide" id="slide-3">
    <div class="slide-badge">03</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Seasonal Analysis</div>
        <h1>Calendar-Month Seasonality: Modest Variance vs. Annual Swings</h1>
      </div>
    </div>
    <div class="content-2col">
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 8px;">Quantifying Calendar Seasonality</div>
        <div class="callout">Key Takeaway: Which YEAR a month falls in matters far more than which calendar month it is.</div>
        <div class="bullet-item"><span class="bullet-title">• Modest Range of Deviation:</span> No single calendar month deviates by more than ~5% from the grand mean (156.78). Peak-to-trough spread is only ~8.4 percentage points.</div>
        <div class="bullet-item"><span class="bullet-title">• Top 3 Highest Months:</span> Feb (+3.2%, 161.76), Aug (+3.1%, 161.61), and May (+2.6%, 160.93).</div>
        <div class="bullet-item"><span class="bullet-title">• Top 3 Lowest Months:</span> Mar (-5.2%, 148.67), Sep (-2.0%, 153.63), Nov (-2.1%, 153.43) [Apr: -2.1%, 153.53].</div>
        <div class="bullet-item"><span class="bullet-title">• Large Residual Variance:</span> Month-to-month standard deviations (187–216) dwarf monthly mean differences, confirming macro annual shocks overpower calendar cycles.</div>
        <div class="bullet-item"><span class="bullet-title">• East Village Sub-Pattern:</span> East Village diverges from citywide rhythm: peaks in Jul–Aug (~601–604) and dips in spring (Mar–Apr, ~509).</div>
      </div>
      <div class="chart-card">
        <img src="{img_c30}" alt="Chart 2: Seasonal Pattern">
        <div class="chart-caption">Chart 2 (EDA Notebook): Average monthly count by calendar month across all years with std error bars.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 3 of 8</span>
    </div>
  </div>

  <!-- SLIDE 4: NEIGHBORHOOD RANKINGS -->
  <div class="slide" id="slide-4">
    <div class="slide-badge">04</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Spatial Dynamics</div>
        <h1>Neighborhood Rankings: Volume Concentration vs. Growth Rates</h1>
      </div>
    </div>
    <div class="content-2col">
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 6px;">Volume Scale vs. Growth Dynamic</div>
        <div class="callout">Core Insight: Growth is NOT concentrated in the largest neighborhood.</div>
        <div class="bullet-item">
          <span class="bullet-title">• By Average Monthly Count (Magnitude):</span><br>
          &nbsp;&nbsp;1. East Village: 552.77 (std 157.09 — highest volume & volatility)<br>
          &nbsp;&nbsp;2. Outside Perimeter: 217.57 (partial coverage, 56 obs)<br>
          &nbsp;&nbsp;3. City Center: 171.81 (std 54.80)<br>
          &nbsp;&nbsp;4. Cortez: 59.52 | 5. Gaslamp: 48.43 | 6. Columbia: 44.49 | 7. Marina: 30.94
        </div>
        <div class="bullet-item">
          <span class="bullet-title">• By Growth Rate (Mean YoY %, 2019+):</span><br>
          &nbsp;&nbsp;- Fastest Growing: Outside Perimeter (+26.90%/yr), Cortez (+11.96%/yr), City Center (+3.94%/yr).<br>
          &nbsp;&nbsp;- Modest Core Growth: East Village (+1.64%/yr) grew slowly despite ~55% total volume.<br>
          &nbsp;&nbsp;- Shrinking Areas: Marina (-12.76%/yr) and Columbia (-4.28%/yr) declined.
        </div>
        <div class="bullet-item">
          <span class="bullet-title">• Spatial Sub-Area Asymmetry:</span><br>
          &nbsp;&nbsp;Within East Village, North East & South East EV consistently outcount West sub-areas.
        </div>
      </div>
      <div class="chart-card">
        <img src="{img_c33}" alt="Chart 3: Stacked Area">
        <div class="chart-caption">Chart 3 (EDA Notebook): Neighborhood composition stacked area over time (2017–2025).</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 4 of 8</span>
    </div>
  </div>
"""

slides_part2 = f"""
  <!-- SLIDE 5: COVID-19 PERIOD IMPACT -->
  <div class="slide" id="slide-5">
    <div class="slide-badge">05</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Pandemic Impact</div>
        <h1>COVID-19 Period Impact: Temporary Suppression & Sharp Rebound</h1>
      </div>
    </div>
    <div class="content-2col">
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 6px;">Pandemic Shock & Rebound Profile</div>
        <div class="callout">Finding: Pandemic programs suppressed visible street counts without a lasting reduction in demand.</div>
        <div class="bullet-item"><span class="bullet-title">• Series All-Time Low (March 2020):</span> Citywide unsheltered total hit its series low of 529 in March 2020 at the onset of initial COVID shelter-in-place orders.</div>
        <div class="bullet-item"><span class="bullet-title">• 2020 Annual Trough (~20% Reduction):</span> 2020 annual average (654.1) dropped ~20% below the 2019 pre-COVID baseline (814.72), reflecting -19.71% YoY contraction.</div>
        <div class="bullet-item"><span class="bullet-title">• Full Recovery by 2021:</span> Counts recovered to an annual average of 960.37 in 2021 (+25.85% YoY), climbing above pre-COVID baseline levels prior to the 2022–2023 surge.</div>
        <div class="bullet-item"><span class="bullet-title">• Operational & Policy Mechanisms:</span> Emergency indoor shelter placements (Convention Center Operation Shelter to Home), eviction moratoria, and curtailed street sweeps temporarily reduced visible unsheltered numbers; demobilization preceded the 2022–2023 peak.</div>
      </div>
      <div class="chart-card">
        <img src="{img_c48}" alt="Chart 8: COVID Period">
        <div class="chart-caption">Chart 8 (EDA Notebook): Overall monthly count trajectory (2019–2022) with shaded COVID-19 period.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 5 of 8</span>
    </div>
  </div>

  <!-- SLIDE 6: METHODOLOGY REGIMES -->
  <div class="slide" id="slide-6">
    <div class="slide-badge">06</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Data Governance</div>
        <h1>Methodology Regimes: Quantifying the Raw vs. Adjusted Count Gap</h1>
      </div>
    </div>
    <div class="content-2col">
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 6px;">Evaluation of Multiplier Regimes</div>
        <div class="callout">Conclusion: Multipliers produce a proportional gap without distorting longitudinal trendlines.</div>
        <div class="bullet-item">
          <span class="bullet-title">• Four Historical Regimes:</span><br>
          &nbsp;&nbsp;- PRE2017 (Jan–Mar 2017): Direct visual count, no component breakout.<br>
          &nbsp;&nbsp;- APR2017 (Apr 2017–Apr 2018): Vehicle multiplier set to 1.66×.<br>
          &nbsp;&nbsp;- MAY2018 (May 2018–Dec 2019): Vehicle multiplier increased to 2.03×.<br>
          &nbsp;&nbsp;- POST2020 (Jan 2020–present): 2.03× retained by DSDP for continuity.
        </div>
        <div class="bullet-item"><span class="bullet-title">• 2018 Volatility & Source Discrepancy:</span> Gap (total_count - raw_count) peaked in 2018 (avg +13.5/mo, spiking to +156.61 in Feb 2018). Audit logged Feb 2018 spike as partly a source-PDF addition error (+30 discrepancy), not purely multiplier mechanics.</div>
        <div class="bullet-item"><span class="bullet-title">• 2019+ Gap Stabilization:</span> From 2019 onward, monthly gap stabilized to near-zero (roughly ±1 to ±5/month), well within expected rounding tolerance (±2).</div>
        <div class="bullet-item"><span class="bullet-title">• Pre-2018 Constraint:</span> Because component breakouts began in Jan 2018, raw and adjusted totals are identical across all of 2017 (gap = 0).</div>
      </div>
      <div class="chart-card">
        <img src="{img_c51}" alt="Chart 9: Adjustment Gap">
        <div class="chart-caption">Chart 9 (EDA Notebook): Monthly adjustment gap (Adjusted Total - Raw Observed Count) across regimes.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 6 of 8</span>
    </div>
  </div>

  <!-- SLIDE 7: HYPOTHESES -->
  <div class="slide" id="slide-7">
    <div class="slide-badge">07</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Research Directions</div>
        <h1>Hypotheses for Further Analysis: Focus Areas for Later Tasks</h1>
      </div>
    </div>
    <div class="grid-2x2">
      <div class="h-card">
        <div class="h-bar" style="background: var(--royal-blue);"></div>
        <div>
          <div class="h-title">H1: Policy & Enforcement Driver of 2022–2023 Peak</div>
          <div class="h-sub">Synchronized Citywide Surge</div>
          <div class="h-desc">The +57.63% (2022) surge hit nearly every neighborhood simultaneously (Cortez +129%, Outside Perimeter +87%, East Village +50%). This synchronized timing points to systemic citywide drivers (eviction moratorium expirations, shelter demobilizations, or sweep shifts) rather than local dynamics.</div>
        </div>
        <div class="h-action">• Test: Correlate monthly counts against RTFH policy timelines, shelter census, and 311 encampment dispatch logs.</div>
      </div>
      <div class="h-card">
        <div class="h-bar" style="background: var(--navy-primary);"></div>
        <div>
          <div class="h-title">H2: East Village Asymmetry Reflects Built Environment</div>
          <div class="h-sub">East vs. West Infrastructure Divide</div>
          <div class="h-desc">East Village sub-areas show persistent asymmetry: North East and South East EV consistently outcount North West and South West EV across 2018–2025. This concentration indicates infrastructure and zoning drivers.</div>
        </div>
        <div class="h-action">• Test: Spatial autocorrelation (Moran's I / Getis-Ord Gi* in Assignment 5) against transit hubs, shelter proximity, and zoning.</div>
      </div>
      <div class="h-card">
        <div class="h-bar" style="background: var(--periwinkle);"></div>
        <div>
          <div class="h-title">H3: 2024 Pullback (-43.52%) May Be a Reporting Artifact</div>
          <div class="h-sub">Rapid Single-Year Drop Scrutiny</div>
          <div class="h-desc">A steep -43.52% drop in a single year immediately after the historical peak warrants verification against external benchmarks before reading it as a true population drop. Count area or staffing changes may be confounders.</div>
        </div>
        <div class="h-action">• Test: Benchmark against independent RTFH Point-in-Time (PIT) counts and audit 2024 DSDP canvassing operations.</div>
      </div>
      <div class="h-card">
        <div class="h-bar" style="background: var(--soft-blue);"></div>
        <div>
          <div class="h-title">H4: Neighborhood Growth Inversely Related to Area Size</div>
          <div class="h-sub">Peripheral Displacement Dynamics</div>
          <div class="h-desc">Mid-sized areas grow fastest (Outside Perimeter +26.90%, Cortez +11.96%, City Center +3.94%), while East Village grows slowly (+1.64%) and Marina shrinks (-12.76%). Enforcement in core areas may displace individuals to borders.</div>
        </div>
        <div class="h-action">• Test: Perform spatial adjacency and boundary-flow analysis in Assignment 5 to evaluate displacement effects.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 7 of 8</span>
    </div>
  </div>

  <!-- SLIDE 8: DATA LIMITATIONS & NEXT STEPS -->
  <div class="slide" id="slide-8">
    <div class="slide-badge">08</div>
    <div class="header-zone">
      <div class="accent-bar"></div>
      <div class="header-content">
        <div class="subtitle">Project Roadmap</div>
        <h1>Data Limitations, Governance Caveats & Roadmap Ahead</h1>
      </div>
    </div>
    <div class="content-2col" style="grid-template-columns: 1fr 1fr;">
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 10px;">Identified Data Limitations & Biases</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--red-alert);">• Incomplete 2025 Series (Reporting Lag):</span> 28 nulls in total_count (Jul, Aug, Oct, Nov 2025 across all 7 neighborhoods) represent unreleased counts, not data errors. All 2025 annual figures must be treated as partial-year.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--red-alert);">• Outside Perimeter Partial History:</span> Outside Perimeter contains only 56 observations (canvassing began ~2022). Its reported +26.90%/yr growth rate is the least statistically reliable neighborhood figure.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--red-alert);">• Pre-2018 Lack of Component Breakouts:</span> Component-level counts (tents, vehicles) are unavailable before Jan 2018. Raw and adjusted totals are identical for all of 2017, precluding early multiplier analysis.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--red-alert);">• Documented Source-PDF Addition Errors:</span> Task 1.1's 45-cell audit found a 97.56% fidelity rate against source PDFs, noting known errors (Feb 2018 +30 PDF addition bug, 2019 EV sub-area duplication, Apr 2025 discrepancy).</div>
      </div>
      <div class="card" style="display: flex; flex-direction: column;">
        <div style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 14px; font-weight: 700; color: var(--navy-primary); margin-bottom: 10px;">Roadmap Ahead: Assignment 3 Integration</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--green-action);">• Immediate Deliverable: Assignment 3:</span> Block-Level Validation & Spatial Integration — moving from macro neighborhood aggregates to granular micro-data across 500+ individual block parcels.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--green-action);">• Granular Block-Level Mapping:</span> Audit street-level counts, reconcile boundary discrepancies, and align block records with GIS city parcel boundaries.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--green-action);">• Spatial Autocorrelation Modeling:</span> Execute Global Moran's I and Local Getis-Ord Gi* hot-spot detection in Assignment 5 to quantify spatial clustering around transit nodes and service hubs.</div>
        <div class="bullet-item"><span class="bullet-title" style="color: var(--green-action);">• Cross-Dataset Validation & Benchmarking:</span> Cross-reference DSDP monthly counts with regional RTFH annual Point-in-Time (PIT) benchmarks and City of San Diego 311 service call logs.</div>
      </div>
    </div>
    <div class="footer">
      <span>Data Science Alliance • Downtown San Diego Homeless Population Analysis</span>
      <span>Slide 8 of 8</span>
    </div>
  </div>

</div>
</body>
</html>
"""

with open("EDA_Presentation.html", "w", encoding="utf-8") as f:
    f.write(html_head + slides_part1 + slides_part2)

print("SUCCESS: Updated EDA_Presentation.html with Canva theme")
print("File size:", os.path.getsize("EDA_Presentation.html"), "bytes")

with open(os.path.join(r"D:\Projects\Downtown-Homeless-Analysis", "EDA_Presentation.html"), "w", encoding="utf-8") as f:
    f.write(html_head + slides_part1 + slides_part2 + "</div>\n</body>\n</html>")
print("Saved EDA_Presentation.html successfully")
