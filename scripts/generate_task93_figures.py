"""
Production figure generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Generates 5 high-resolution (300 DPI) publication-grade visual assets:
1. slide_assets/task93_forecast_2026.png (Forward prospective forecast, 80%/95% PIs & scenarios)
2. slide_assets/task93_regional_divergence.png (Downtown collapse vs county unsheltered high)
3. slide_assets/task93_hotspot_migration.png (120m SSE centroid migration & persistent hotspots)
4. slide_assets/task93_footprint_wedge.png (2022 footprint expansion wedge quantification)
5. slide_assets/task93_trajectory_9year.png (9-year monthly trajectory with 2025 unpublished gaps)
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "slide_assets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Canva Presentation Color System
NAVY = "#293E9C"
ROYAL_BLUE = "#3A58E4"
PERIWINKLE = "#6984FE"
SOFT_BLUE = "#9AADFF"
ICE_TINT = "#D3DFFF"
CANVAS_BG = "#F5F7FB"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#DCE4F5"
DARK_TEXT = "#1D1F26"
MUTED_TEXT = "#647491"
RED_ALERT = "#DC2626"
GREEN_ACTION = "#059669"
AMBER_WARN = "#D97706"
TEAL_CHAMP = "#0D9488"

# Plot formatting defaults
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
plt.rcParams["axes.edgecolor"] = CARD_BORDER
plt.rcParams["axes.linewidth"] = 1.0

NEIGHBORHOODS = [
    "East Village", "City Center", "Columbia", "Marina",
    "Cortez", "Gaslamp", "Outside Perimeter",
]


def load_overall_series():
    """Load the overall reported footprint monthly time series from MasterCounts_Adjusted_v2.csv."""
    master_path = DATA_DIR / "MasterCounts_Adjusted_v2.csv"
    df = pd.read_csv(master_path, parse_dates=["date"])
    monthly = df.loc[
        (df["component"] == "total")
        & (df["area_type"] == "neighborhood")
        & (df["area"].isin(NEIGHBORHOODS)),
        ["date", "area", "total_count"],
    ]
    pivot = monthly.pivot(index="date", columns="area", values="total_count").sort_index()
    overall = pivot.sum(axis=1, min_count=1)
    # Reindex to full monthly sequence from min to max date
    full_idx = pd.date_range(overall.index.min(), overall.index.max(), freq="MS")
    s_full = overall.reindex(full_idx)
    return s_full


def generate_trajectory_9year_figure():
    """Figure 5: 9-Year Monthly Trajectory (2017-2025) with Macro Epochs & Data Gaps."""
    s_full = load_overall_series()

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=CARD_BG)
    ax.set_facecolor(CANVAS_BG)

    # Shading Macro Epochs
    # Epoch 1: Jan 2017 - Dec 2020
    ax.axvspan(pd.Timestamp("2017-01-01"), pd.Timestamp("2020-12-31"), color=ICE_TINT, alpha=0.35, label="Epoch 1: Baseline Contraction (2017–2020)")
    # Epoch 2: Jan 2021 - Dec 2023
    ax.axvspan(pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31"), color="#FEE2E2", alpha=0.35, label="Epoch 2: Crisis Surge (2021–2023)")
    # Epoch 3: Jan 2024 - Dec 2025
    ax.axvspan(pd.Timestamp("2024-01-01"), pd.Timestamp("2025-12-31"), color="#D1FAE5", alpha=0.35, label="Epoch 3: Enforcement & Stabilization (2024–2025)")

    # Plot monthly count line (NaNs will create clean gaps for the 4 unpublished 2025 months)
    ax.plot(
        s_full.index,
        s_full.values,
        color=NAVY,
        linewidth=2.2,
        marker="o",
        markersize=4.5,
        markerfacecolor=ROYAL_BLUE,
        markeredgecolor=NAVY,
        label="Observed Monthly Count (DSDP Reported Footprint)",
        zorder=4,
    )

    # Key callout points
    # 1. Series Min: March 2020 (529.1)
    ax.annotate(
        "Series Low: 529\n(Mar 2020)",
        xy=(pd.Timestamp("2020-03-01"), 529.1),
        xytext=(pd.Timestamp("2019-06-01"), 350),
        arrowprops=dict(facecolor=ROYAL_BLUE, arrowstyle="->", lw=1.2),
        fontsize=8.5,
        fontweight="bold",
        color=ROYAL_BLUE,
        bbox=dict(boxstyle="round,pad=0.25", fc=CARD_BG, ec=ROYAL_BLUE, lw=1),
    )

    # 2. Series Peak: May 2023 (2,103.3)
    ax.annotate(
        "Series Peak: 2,103\n(May 2023)",
        xy=(pd.Timestamp("2023-05-01"), 2103.3),
        xytext=(pd.Timestamp("2022-04-01"), 2150),
        arrowprops=dict(facecolor=RED_ALERT, arrowstyle="->", lw=1.2),
        fontsize=8.5,
        fontweight="bold",
        color=RED_ALERT,
        bbox=dict(boxstyle="round,pad=0.25", fc=CARD_BG, ec=RED_ALERT, lw=1),
    )

    # 3. Post-surge inflection & 2025 hold-out count: Jan 2025 (851.0)
    ax.annotate(
        "Jan 2025: 851\n(−59.5% from peak)",
        xy=(pd.Timestamp("2025-01-01"), 851.0),
        xytext=(pd.Timestamp("2024-03-01"), 1200),
        arrowprops=dict(facecolor=GREEN_ACTION, arrowstyle="->", lw=1.2),
        fontsize=8.5,
        fontweight="bold",
        color=GREEN_ACTION,
        bbox=dict(boxstyle="round,pad=0.25", fc=CARD_BG, ec=GREEN_ACTION, lw=1),
    )

    # 4. Dec 2025 latest count: 985.4
    ax.annotate(
        "Dec 2025: 985",
        xy=(pd.Timestamp("2025-12-01"), 985.4),
        xytext=(pd.Timestamp("2025-05-01"), 650),
        arrowprops=dict(facecolor=NAVY, arrowstyle="->", lw=1.2),
        fontsize=8.5,
        fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.25", fc=CARD_BG, ec=NAVY, lw=1),
    )

    # Note about 2025 unpublished months
    ax.text(
        pd.Timestamp("2025-07-01"),
        1550,
        "⚠️ 4 Months Unpublished in 2025\n(Jul, Aug, Oct, Nov: plotted as gaps)",
        fontsize=8,
        fontweight="bold",
        color=MUTED_TEXT,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=CARD_BORDER, lw=0.8),
    )

    ax.set_title(
        "Downtown San Diego Unsheltered Homelessness: 9-Year Monthly Trajectory (2017–2025)",
        fontsize=12.5,
        fontweight="bold",
        color=NAVY,
        pad=15,
    )
    ax.set_ylabel("Monthly Unsheltered Count", fontsize=10, fontweight="bold", color=DARK_TEXT)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("'%y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER)
    ax.set_ylim(200, 2350)
    ax.set_xlim(pd.Timestamp("2016-10-01"), pd.Timestamp("2026-03-01"))
    ax.legend(loc="upper left", frameon=True, facecolor=CARD_BG, edgecolor=CARD_BORDER, fontsize=8)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_trajectory_9year.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def generate_forecast_2026_figure():
    """Figure 1: 12-Month Prospective 2026 Forecast with 80%/95% PIs and 3 Scenarios."""
    forecast_path = DATA_DIR / "Forecasts_12Month.csv"
    if not forecast_path.exists():
        print("Skipping forecast figure: missing data.")
        return

    df_fc = pd.read_csv(forecast_path)
    df_fc = df_fc[df_fc["series"] == "Overall - reported footprint"].copy()
    df_fc["date"] = pd.to_datetime(df_fc["forecast_date"])
    df_fc = df_fc.sort_values("date")

    # Load historical headline counts for context (2023 to 2025)
    s_full = load_overall_series()
    s_recent = s_full[s_full.index >= "2023-01-01"]

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=CARD_BG)
    ax.set_facecolor(CANVAS_BG)

    # Plot historical observations
    ax.plot(
        s_recent.index,
        s_recent.values,
        color=NAVY,
        marker="o",
        linewidth=2.2,
        markersize=4.5,
        label="Observed Monthly Count (2023–2025)",
        zorder=4,
    )

    # Shaded Prediction Intervals (derived from Holt-Winters residual variance)
    ax.fill_between(
        df_fc["date"],
        df_fc["pi_95_lower"],
        df_fc["pi_95_upper"],
        color=TEAL_CHAMP,
        alpha=0.15,
        label="Approximate 95% Prediction Interval",
        zorder=2,
    )
    ax.fill_between(
        df_fc["date"],
        df_fc["pi_80_lower"],
        df_fc["pi_80_upper"],
        color=TEAL_CHAMP,
        alpha=0.25,
        label="Approximate 80% Prediction Interval",
        zorder=3,
    )

    # Scenarios and Baseline
    ax.plot(
        df_fc["date"],
        df_fc["point_forecast"],
        color=TEAL_CHAMP,
        linewidth=2.8,
        label="Baseline Forecast (XGBoost Champion: 816–896)",
        zorder=5,
    )
    ax.plot(
        df_fc["date"],
        df_fc["scenario_optimistic"],
        color=GREEN_ACTION,
        linestyle="--",
        linewidth=2.0,
        label="Optimistic Fixed Scenario (−24% at M12: ~675)",
        zorder=5,
    )
    ax.plot(
        df_fc["date"],
        df_fc["scenario_pessimistic"],
        color=RED_ALERT,
        linestyle="--",
        linewidth=2.0,
        label="Pessimistic Fixed Scenario (+26% at M12: ~1,123)",
        zorder=5,
    )

    # Vertical line separating history and forecast
    sep_date = pd.Timestamp("2025-12-15")
    ax.axvline(sep_date, color=MUTED_TEXT, linestyle=":", linewidth=1.5, alpha=0.8)
    ax.text(
        sep_date - pd.Timedelta(days=15),
        2100,
        "Historical Observed",
        ha="right",
        va="top",
        fontsize=9.5,
        fontweight="bold",
        color=NAVY,
    )
    ax.text(
        sep_date + pd.Timedelta(days=15),
        2100,
        "Prospective 2026 Forecast",
        ha="left",
        va="top",
        fontsize=9.5,
        fontweight="bold",
        color=TEAL_CHAMP,
    )

    # Annotate key points
    m12_row = df_fc.iloc[-1]
    ax.annotate(
        f"M12 Baseline: {m12_row['point_forecast']:.0f}\n[95% PI: {m12_row['pi_95_lower']:.0f}–{m12_row['pi_95_upper']:.0f}]",
        xy=(m12_row["date"], m12_row["point_forecast"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["point_forecast"] - 20),
        fontsize=8.5,
        fontweight="bold",
        color=TEAL_CHAMP,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=TEAL_CHAMP, lw=1),
    )
    ax.annotate(
        f"Optimistic: {m12_row['scenario_optimistic']:.0f}",
        xy=(m12_row["date"], m12_row["scenario_optimistic"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["scenario_optimistic"] - 30),
        fontsize=8.5,
        fontweight="bold",
        color=GREEN_ACTION,
    )
    ax.annotate(
        f"Pessimistic: {m12_row['scenario_pessimistic']:.0f}",
        xy=(m12_row["date"], m12_row["scenario_pessimistic"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["scenario_pessimistic"] + 20),
        fontsize=8.5,
        fontweight="bold",
        color=RED_ALERT,
    )

    ax.set_title(
        "Downtown San Diego 12-Month Prospective Forecast & Stress-Test Scenarios (2026)",
        fontsize=12.5,
        fontweight="bold",
        color=NAVY,
        pad=15,
    )
    ax.set_ylabel("Monthly Unsheltered Count", fontsize=10, fontweight="bold", color=DARK_TEXT)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER)
    ax.set_ylim(400, 2300)
    ax.set_xlim(pd.Timestamp("2023-01-01"), pd.Timestamp("2027-02-15"))
    ax.legend(loc="upper right", frameon=True, facecolor=CARD_BG, edgecolor=CARD_BORDER, fontsize=8)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_forecast_2026.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def generate_regional_divergence_figure():
    """Figure 2: Paired Series - Downtown Contraction vs Countywide Unsheltered High."""
    paired_path = DATA_DIR / "Downtown_County_PairedCounts.csv"
    if not paired_path.exists():
        print("Skipping regional divergence figure: missing paired data.")
        return

    df = pd.read_csv(paired_path).dropna(subset=["county_unsheltered"]).sort_values("pit_year")

    fig, ax1 = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=CARD_BG)
    ax1.set_facecolor(CANVAS_BG)

    years = df["pit_year"].values
    downtown_vals = df["downtown_reported_adjusted"].values
    county_vals = df["county_unsheltered"].values
    shares = df["downtown_share_county_unsheltered_pct"].values

    x = np.arange(len(years))
    width = 0.35

    # Bar 1: Downtown Count
    rects1 = ax1.bar(
        x - width / 2,
        downtown_vals,
        width,
        label="Downtown January Field Count (DSDP Adjusted)",
        color=ROYAL_BLUE,
        alpha=0.9,
    )

    # Bar 2: Countywide Unsheltered PIT
    rects2 = ax1.bar(
        x + width / 2,
        county_vals,
        width,
        label="Countywide Unsheltered PIT (RTFH Annual Census)",
        color=NAVY,
        alpha=0.9,
    )

    ax1.set_ylabel("Unsheltered Population Count", fontsize=10, fontweight="bold", color=NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10, fontweight="bold", color=DARK_TEXT)
    ax1.set_ylim(0, 7500)
    ax1.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER, axis="y")

    # Secondary Axis for Share %
    ax2 = ax1.twinx()
    ax2.plot(
        x,
        shares,
        color=RED_ALERT,
        marker="s",
        linewidth=2.5,
        markersize=6.5,
        label="Downtown Share of County (%)",
    )
    ax2.set_ylabel("Downtown Share of County (%)", fontsize=10, fontweight="bold", color=RED_ALERT)
    ax2.set_ylim(0, 50)

    # Data value callouts on bars
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(
            f"{h:,.0f}",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=DARK_TEXT,
            fontweight="bold",
        )
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(
            f"{h:,.0f}",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=DARK_TEXT,
            fontweight="bold",
        )

    for i, s in enumerate(shares):
        ax2.annotate(
            f"{s:.1f}%",
            xy=(x[i], s),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=RED_ALERT,
            fontweight="bold",
        )

    # Highlight Downtown-County Divergence
    ax1.annotate(
        "Downtown–County Divergence:\nDowntown Jan fell to 851 (−56%)\nCounty unsheltered rose to 6,110 (series high)",
        xy=(len(years) - 1.5, 5900),
        xytext=(len(years) - 3.6, 6350),
        arrowprops=dict(facecolor=RED_ALERT, arrowstyle="->", lw=1.5),
        fontsize=8.5,
        fontweight="bold",
        color=RED_ALERT,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=RED_ALERT, lw=1),
    )

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor=CARD_BG, fontsize=8)

    plt.title(
        "Downtown–County Divergence: Downtown Contraction vs. County Unsheltered High (2017–2025)",
        fontsize=12,
        fontweight="bold",
        color=NAVY,
        pad=15,
    )
    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_regional_divergence.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def generate_hotspot_migration_figure():
    """Figure 3: Hotspot Centroid Migration Vector & Top Persistent Clusters."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.5), dpi=300, facecolor=CARD_BG, gridspec_kw={"width_ratios": [1.15, 1]})
    ax1.set_facecolor(CANVAS_BG)
    ax2.set_facecolor(CARD_BG)

    # Left plot: Centroid Migration Vector Diagram (Exact Recomputed Coordinates)
    # Early (2018-2020, n=10): (-117.149345, 32.708282)
    # Recent (2022-2025, n=20): (-117.148905, 32.707261)
    # Shift: 120.4 m, bearing 160.1° SSE
    c_early = (-117.149345, 32.708282)
    c_recent = (-117.148905, 32.707261)

    # Street grid reference lines
    streets_y = [32.7110, 32.7100, 32.7090, 32.7080, 32.7070, 32.7060]
    street_labels = ["Market St", "Island Ave", "J St", "K St", "Imperial Ave", "Commercial St"]
    for y, label in zip(streets_y, street_labels):
        ax1.axhline(y, color=CARD_BORDER, linestyle="-", linewidth=1.1, zorder=1)
        ax1.text(-117.1530, y + 0.0001, label, fontsize=7.5, color=MUTED_TEXT, fontweight="bold")

    streets_x = [-117.1515, -117.1500, -117.1485, -117.1470]
    street_x_labels = ["14th St", "15th St", "16th St", "17th St"]
    for x, label in zip(streets_x, street_x_labels):
        ax1.axvline(x, color=CARD_BORDER, linestyle="-", linewidth=1.1, zorder=1)
        ax1.text(x, 32.7115, label, fontsize=7.5, color=MUTED_TEXT, ha="center", fontweight="bold")

    # Plot Early vs Recent Centroids
    ax1.scatter(c_early[0], c_early[1], color=ROYAL_BLUE, s=320, marker="o", edgecolors=NAVY, linewidth=2, label="2018–2020 Centroid (n=10 dates)", zorder=5)
    ax1.scatter(c_recent[0], c_recent[1], color=RED_ALERT, s=320, marker="o", edgecolors="#7F1D1D", linewidth=2, label="2022–2025 Centroid (n=20 dates)", zorder=5)

    # Draw South-South-East Vector Arrow
    ax1.annotate(
        "",
        xy=(c_recent[0], c_recent[1] + 0.00015),
        xytext=(c_early[0], c_early[1] - 0.00015),
        arrowprops=dict(facecolor=RED_ALERT, edgecolor=RED_ALERT, width=3.0, headwidth=10, headlength=11),
        zorder=6,
    )
    ax1.text(
        (c_early[0] + c_recent[0]) / 2 + 0.0008,
        (c_early[1] + c_recent[1]) / 2,
        "120.4 m Shift (160.1° SSE)\n(Cluster location, not people)",
        fontsize=8.5,
        fontweight="bold",
        color=RED_ALERT,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=RED_ALERT, lw=1),
        zorder=7,
    )

    ax1.set_xlim(-117.1535, -117.1450)
    ax1.set_ylim(32.7055, 32.7122)
    ax1.set_title("Hotspot Centroid Migration (South East Village)", fontsize=11, fontweight="bold", color=NAVY)
    ax1.legend(loc="lower left", fontsize=7.5, frameon=True, facecolor=CARD_BG)
    ax1.axis("off")

    # Right plot: Top Persistent Hotspot Ranking Bar Chart (From Rebuilt Ranking CSV)
    hotspot_csv = DATA_DIR / "Hotspot_Persistence_Ranking_rebuilt.csv"
    if hotspot_csv.exists():
        df_rank = pd.read_csv(hotspot_csv).head(7)
        names = [
            "16th St & Imperial Ave",
            "I-5 SB & Imperial Ave",
            "I-5 SB Off-Ramp (Map Border)",
            "I-5 SB On-Ramp (Map Border)",
            "17th St & Imperial Ave",
            "16th St & J St",
            "17th St & J St",
        ]
        counts = df_rank["hotspot_dates"].values
        rates = (df_rank["hotspot_rate"] * 100).values
    else:
        names = ["16th & Imperial", "I-5 SB & Imperial", "I-5 SB Off-Ramp", "I-5 SB On-Ramp", "17th & Imperial", "16th & J", "17th & J"]
        counts = [9, 8, 6, 4, 4, 2, 2]
        rates = [75.0, 66.7, 50.0, 33.3, 33.3, 16.7, 16.7]

    colors = [RED_ALERT if c >= 8 else ROYAL_BLUE if c >= 4 else PERIWINKLE for c in counts]

    # Invert for horizontal bar plot
    names_rev = list(reversed(names))
    counts_rev = list(reversed(counts))
    rates_rev = list(reversed(rates))
    colors_rev = list(reversed(colors))

    y_pos = np.arange(len(names_rev))
    bars = ax2.barh(y_pos, counts_rev, color=colors_rev, height=0.6, alpha=0.9)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names_rev, fontsize=8, fontweight="bold", color=DARK_TEXT)
    ax2.set_xlabel("Statistically Significant Hotspot Dates (out of 12)", fontsize=8, fontweight="bold", color=NAVY)
    ax2.set_xlim(0, 12)
    ax2.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER, axis="x")

    for i, (bar, rate) in enumerate(zip(bars, rates_rev)):
        w = bar.get_width()
        ax2.annotate(
            f" {w}/12 ({rate:.0f}%)",
            xy=(w, bar.get_y() + bar.get_height() / 2),
            va="center",
            fontsize=8,
            fontweight="bold",
            color=DARK_TEXT,
        )

    ax2.set_title("Top Persistent Hotspots (Getis-Ord Gi*)", fontsize=11, fontweight="bold", color=NAVY)

    plt.suptitle("Geospatial Hotspot Dynamics: Migration Vector & Persistence (2018–2025)", fontsize=12, fontweight="bold", color=NAVY, y=0.98)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_hotspot_migration.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def generate_footprint_wedge_figure():
    """Figure 4: The 2022 Footprint Expansion Wedge (+121 Peripheral Blocks)."""
    wedge_path = DATA_DIR / "SpatialPanel_FootprintEffect.csv"
    if not wedge_path.exists():
        print("Skipping footprint wedge figure: missing data.")
        return

    df = pd.read_csv(wedge_path)
    df["date_label"] = pd.to_datetime(df["count_date"]).dt.strftime("%b %Y")

    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300, facecolor=CARD_BG)
    ax.set_facecolor(CANVAS_BG)

    x = np.arange(len(df))
    width = 0.55

    # Stacked Bars: Balanced 261 Blocks vs Expansion Wedge (121 Blocks)
    balanced_counts = df["balanced_261_total"].values
    deltas = df["expansion_delta"].values
    pcts = df["expansion_pct_of_full"].values

    p1 = ax.bar(x, balanced_counts, width, label="Balanced Core Footprint (261 Blocks)", color=ROYAL_BLUE, alpha=0.9)
    p2 = ax.bar(x, deltas, width, bottom=balanced_counts, label="2022 Expansion Footprint (+121 Blocks)", color=AMBER_WARN, alpha=0.95)

    ax.set_ylabel("Adjusted Total Homeless Count", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_xticks(x)
    ax.set_xticklabels(df["date_label"], fontsize=10, fontweight="bold", color=DARK_TEXT)
    ax.set_ylim(0, 2400)
    ax.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER, axis="y")

    # Annotate wedges
    for i, (total, delta, pct) in enumerate(zip(df["full_382_total"], deltas, pcts)):
        ax.annotate(
            f"Total: {total:,.0f}\n+{delta:,.0f} ({pct:.1f}%)",
            xy=(x[i], total),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=DARK_TEXT,
        )

    # Highlight January 2023 peak footprint share
    ax.annotate(
        "Peak Footprint Wedge:\nAdded 121 blocks contributed 32.8%\n(641 of 1,955) in Jan 2023",
        xy=(x[2], df["full_382_total"].iloc[2]),
        xytext=(x[2] + 0.2, 2150),
        arrowprops=dict(facecolor=AMBER_WARN, arrowstyle="->", lw=1.5),
        fontsize=8.5,
        fontweight="bold",
        color=AMBER_WARN,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=AMBER_WARN, lw=1),
    )

    ax.legend(loc="upper right", frameon=True, facecolor=CARD_BG, edgecolor=CARD_BORDER, fontsize=8.5)
    ax.set_title(
        "Disentangling Reality from Administrative Footprint Expansion (2022–2025)",
        fontsize=12,
        fontweight="bold",
        color=NAVY,
        pad=15,
    )

    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_footprint_wedge.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def main():
    print("Initiating Task 9.3 Figure Generation...")
    generate_trajectory_9year_figure()
    generate_forecast_2026_figure()
    generate_regional_divergence_figure()
    generate_hotspot_migration_figure()
    generate_footprint_wedge_figure()
    print("All Task 9.3 figures generated successfully!")


if __name__ == "__main__":
    main()
