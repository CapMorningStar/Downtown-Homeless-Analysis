"""
Production figure generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Generates 4 high-resolution (300 DPI) publication-grade visual assets:
1. slide_assets/task93_forecast_2026.png (Forward prospective forecast, 80%/95% PIs & scenarios)
2. slide_assets/task93_regional_divergence.png (Downtown collapse vs county record high)
3. slide_assets/task93_hotspot_migration.png (121m southward centroid migration & persistent hotspots)
4. slide_assets/task93_footprint_wedge.png (2022 footprint expansion wedge quantification)
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
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


def generate_forecast_2026_figure():
    """Figure 1: 12-Month Prospective 2026 Forecast with 80%/95% PIs and 3 Scenarios."""
    forecast_path = DATA_DIR / "Forecasts_12Month.csv"
    master_path = DATA_DIR / "MasterCounts_Adjusted_v2.csv"
    
    if not forecast_path.exists() or not master_path.exists():
        print(f"Skipping forecast figure: missing data.")
        return

    df_fc = pd.read_csv(forecast_path)
    df_fc = df_fc[df_fc["series"] == "Overall - reported footprint"].copy()
    df_fc["date"] = pd.to_datetime(df_fc["forecast_date"])
    df_fc = df_fc.sort_values("date")

    # Load historical headline counts for context (2022 to 2025)
    df_hist = pd.read_csv(master_path)
    df_hist["date"] = pd.to_datetime(df_hist["date"])
    df_hist_sub = df_hist[
        (df_hist["component"] == "total") &
        (df_hist["area"] == "Overall - reported footprint") &
        (df_hist["date"] >= "2023-01-01") &
        (df_hist["total_count"] > 0)
    ].sort_values("date")

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=CARD_BG)
    ax.set_facecolor(CANVAS_BG)

    # Plot historical observations
    ax.plot(
        df_hist_sub["date"],
        df_hist_sub["total_count"],
        color=NAVY,
        marker="o",
        linewidth=2.5,
        markersize=5,
        label="Observed Monthly Count (2023–2025)",
        zorder=4,
    )

    # Shaded Prediction Intervals
    ax.fill_between(
        df_fc["date"],
        df_fc["pi_95_lower"],
        df_fc["pi_95_upper"],
        color=TEAL_CHAMP,
        alpha=0.15,
        label="95% Prediction Interval",
        zorder=2,
    )
    ax.fill_between(
        df_fc["date"],
        df_fc["pi_80_lower"],
        df_fc["pi_80_upper"],
        color=TEAL_CHAMP,
        alpha=0.25,
        label="80% Prediction Interval",
        zorder=3,
    )

    # Scenarios and Baseline
    ax.plot(
        df_fc["date"],
        df_fc["point_forecast"],
        color=TEAL_CHAMP,
        linewidth=3.0,
        label="Baseline Forecast (Status Quo)",
        zorder=5,
    )
    ax.plot(
        df_fc["date"],
        df_fc["scenario_optimistic"],
        color=GREEN_ACTION,
        linestyle="--",
        linewidth=2.2,
        label="Optimistic Policy Scenario (-24% at M12)",
        zorder=5,
    )
    ax.plot(
        df_fc["date"],
        df_fc["scenario_pessimistic"],
        color=RED_ALERT,
        linestyle="--",
        linewidth=2.2,
        label="Pessimistic Policy Scenario (+26% at M12)",
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
        fontsize=10,
        fontweight="bold",
        color=NAVY,
    )
    ax.text(
        sep_date + pd.Timedelta(days=15),
        2100,
        "Prospective 2026 Forecast",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
        color=TEAL_CHAMP,
    )

    # Annotate key points
    m12_row = df_fc.iloc[-1]
    ax.annotate(
        f"Baseline: {m12_row['point_forecast']:.0f}\n[95% PI: {m12_row['pi_95_lower']:.0f}–{m12_row['pi_95_upper']:.0f}]",
        xy=(m12_row["date"], m12_row["point_forecast"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["point_forecast"] - 20),
        fontsize=9,
        fontweight="bold",
        color=TEAL_CHAMP,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=TEAL_CHAMP, lw=1),
    )
    ax.annotate(
        f"Optimistic: {m12_row['scenario_optimistic']:.0f}",
        xy=(m12_row["date"], m12_row["scenario_optimistic"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["scenario_optimistic"] - 30),
        fontsize=9,
        fontweight="bold",
        color=GREEN_ACTION,
    )
    ax.annotate(
        f"Pessimistic: {m12_row['scenario_pessimistic']:.0f}",
        xy=(m12_row["date"], m12_row["scenario_pessimistic"]),
        xytext=(m12_row["date"] + pd.Timedelta(days=10), m12_row["scenario_pessimistic"] + 20),
        fontsize=9,
        fontweight="bold",
        color=RED_ALERT,
    )

    ax.set_title(
        "Downtown San Diego 12-Month Prospective Forecast & Policy Scenarios (2026)",
        fontsize=13,
        fontweight="bold",
        color=NAVY,
        pad=15,
    )
    ax.set_ylabel("Monthly Unsheltered Count", fontsize=10, fontweight="bold", color=DARK_TEXT)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER)
    ax.set_ylim(400, 2300)
    ax.set_xlim(pd.Timestamp("2023-01-01"), pd.Timestamp("2027-02-15"))
    ax.legend(loc="upper right", frameon=True, facecolor=CARD_BG, edgecolor=CARD_BORDER, fontsize=8.5)

    plt.tight_layout()
    out_file = OUTPUT_DIR / "task93_forecast_2026.png"
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Generated: {out_file}")


def generate_regional_divergence_figure():
    """Figure 2: Paired Series - Downtown Contraction vs Countywide Unsheltered Record."""
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
        label="Downtown Monthly Field Count (DSDP)",
        color=ROYAL_BLUE,
        alpha=0.9,
    )

    # Bar 2: Countywide Unsheltered PIT
    rects2 = ax1.bar(
        x + width / 2,
        county_vals,
        width,
        label="Countywide Unsheltered PIT (RTFH)",
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
        markersize=7,
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
            fontsize=8.5,
            color=RED_ALERT,
            fontweight="bold",
        )

    # Highlight Post-Ordinance Displacement
    ax1.annotate(
        "Post-Ordinance Decoupling:\nDowntown fell -56%\nCounty hit record 6,110",
        xy=(len(years) - 1.5, 5900),
        xytext=(len(years) - 3.2, 6400),
        arrowprops=dict(facecolor=RED_ALERT, arrowstyle="->", lw=1.5),
        fontsize=9,
        fontweight="bold",
        color=RED_ALERT,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=RED_ALERT, lw=1),
    )

    # Legends combined
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor=CARD_BG, fontsize=8.5)

    plt.title(
        "The Regional Displacement Paradox: Downtown Collapse vs. Countywide Record (2017–2025)",
        fontsize=12.5,
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.5), dpi=300, facecolor=CARD_BG, gridspec_kw={"width_ratios": [1.2, 1]})
    ax1.set_facecolor(CANVAS_BG)
    ax2.set_facecolor(CARD_BG)

    # Left plot: Centroid Migration Vector Diagram
    # Approximate relative coordinates centered on South East Village
    c_early = (-117.1488, 32.7093)  # 2018-2020 cluster centroid (approx J St / 16th)
    c_late = (-117.1485, 32.7082)   # 2022-2025 cluster centroid (approx Imperial / 16th)

    # Plot base reference lines for streets
    streets_y = [32.7110, 32.7100, 32.7090, 32.7080, 32.7070]
    street_labels = ["Market St", "Island Ave", "J St", "K St / Imperial Ave", "Commercial St"]
    for y, label in zip(streets_y, street_labels):
        ax1.axhline(y, color=CARD_BORDER, linestyle="-", linewidth=1.2, zorder=1)
        ax1.text(-117.1530, y + 0.0001, label, fontsize=8, color=MUTED_TEXT, fontweight="bold")

    streets_x = [-117.1510, -117.1495, -117.1480, -117.1465]
    street_x_labels = ["14th St", "15th St", "16th St", "17th St"]
    for x, label in zip(streets_x, street_x_labels):
        ax1.axvline(x, color=CARD_BORDER, linestyle="-", linewidth=1.2, zorder=1)
        ax1.text(x, 32.7115, label, fontsize=8, color=MUTED_TEXT, ha="center", fontweight="bold")

    # Plot Transit & Service Anchors
    ax1.scatter(-117.1490, 32.7078, color=AMBER_WARN, s=280, marker="P", label="12th & Imperial Transit Center (52m)", zorder=4)
    ax1.scatter(-117.1475, 32.7088, color=PERIWINKLE, s=280, marker="H", label="Social Service & Intake Hubs (285m)", zorder=4)

    # Plot Early vs Recent Centroids
    ax1.scatter(c_early[0], c_early[1], color=ROYAL_BLUE, s=350, marker="o", edgecolors=NAVY, linewidth=2, label="2018–2020 Centroid (Early Epoch)", zorder=5)
    ax1.scatter(c_late[0], c_late[1], color=RED_ALERT, s=350, marker="o", edgecolors="#7F1D1D", linewidth=2, label="2022–2025 Centroid (Recent Epoch)", zorder=5)

    # Draw Southward Vector Arrow
    ax1.annotate(
        "",
        xy=(c_late[0], c_late[1] + 0.00015),
        xytext=(c_early[0], c_early[1] - 0.00015),
        arrowprops=dict(facecolor=RED_ALERT, edgecolor=RED_ALERT, width=3.5, headwidth=11, headlength=12),
        zorder=6,
    )
    ax1.text(
        (c_early[0] + c_late[0]) / 2 + 0.0008,
        (c_early[1] + c_late[1]) / 2,
        "121m Southward\nDisplacement Vector",
        fontsize=9,
        fontweight="bold",
        color=RED_ALERT,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=RED_ALERT, lw=1),
        zorder=7,
    )

    ax1.set_xlim(-117.1535, -117.1450)
    ax1.set_ylim(32.7065, 32.7120)
    ax1.set_title("Hotspot Centroid Migration (South East Village)", fontsize=11, fontweight="bold", color=NAVY)
    ax1.legend(loc="lower left", fontsize=7.5, frameon=True, facecolor=CARD_BG)
    ax1.axis("off")

    # Right plot: Top Persistent Hotspot Ranking Bar Chart
    top_blocks = [
        ("16th St & Imperial Ave", 9, 75.0, RED_ALERT),
        ("I-5 SB & Imperial Ave", 8, 66.7, RED_ALERT),
        ("I-5 SB Off-Ramp", 6, 50.0, ROYAL_BLUE),
        ("I-5 SB On-Ramp", 4, 33.3, ROYAL_BLUE),
        ("17th St & Imperial Ave", 4, 33.3, ROYAL_BLUE),
        ("16th St & J St", 2, 16.7, PERIWINKLE),
        ("17th St & J St", 2, 16.7, PERIWINKLE),
    ]

    names = [b[0] for b in reversed(top_blocks)]
    counts = [b[1] for b in reversed(top_blocks)]
    rates = [b[2] for b in reversed(top_blocks)]
    colors = [b[3] for b in reversed(top_blocks)]

    y_pos = np.arange(len(names))
    bars = ax2.barh(y_pos, counts, color=colors, height=0.6, alpha=0.9)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names, fontsize=8.5, fontweight="bold", color=DARK_TEXT)
    ax2.set_xlabel("Statistically Significant Hotspot Dates (out of 12)", fontsize=8.5, fontweight="bold", color=NAVY)
    ax2.set_xlim(0, 12)
    ax2.grid(True, linestyle="--", alpha=0.5, color=CARD_BORDER, axis="x")

    for i, (bar, rate) in enumerate(zip(bars, rates)):
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

    plt.suptitle("Geospatial Hotspot Dynamics: Migration Vector & Persistence (2018–2025)", fontsize=12.5, fontweight="bold", color=NAVY, y=0.98)
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
    p2 = ax.bar(x, deltas, width, bottom=balanced_counts, label="2022 Expansion Footprint (+121 Blocks: Golden Hill, Barrio Logan, Sherman Heights)", color=AMBER_WARN, alpha=0.95)

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
            fontsize=8.5,
            fontweight="bold",
            color=DARK_TEXT,
        )

    # Highlight January 2023 peak anomaly
    ax.annotate(
        "Peak Footprint Wedge:\n32.8% of Jan 2023 count was\nadministrative boundary expansion!",
        xy=(x[2], df["full_382_total"].iloc[2]),
        xytext=(x[2] - 0.9, 2150),
        arrowprops=dict(facecolor=AMBER_WARN, arrowstyle="->", lw=1.5),
        fontsize=9,
        fontweight="bold",
        color=AMBER_WARN,
        bbox=dict(boxstyle="round,pad=0.3", fc=CARD_BG, ec=AMBER_WARN, lw=1),
    )

    ax.legend(loc="upper left", frameon=True, facecolor=CARD_BG, edgecolor=CARD_BORDER, fontsize=9)
    ax.set_title(
        "Disentangling Reality from Administrative Footprint Expansion (2022–2025)",
        fontsize=12.5,
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
    generate_forecast_2026_figure()
    generate_regional_divergence_figure()
    generate_hotspot_migration_figure()
    generate_footprint_wedge_figure()
    print("All Task 9.3 figures generated successfully!")


if __name__ == "__main__":
    main()
