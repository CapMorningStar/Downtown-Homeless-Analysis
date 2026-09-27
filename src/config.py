"""
Global configuration, theme palettes, date limits, and historical regime definitions.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"

# Application Metadata
APP_TITLE = "Downtown San Diego Homeless Population Analysis"
APP_SUBTITLE = "Longitudinal Modeling, Spatial Hotspots & Strategic Synthesis Dashboard"
ORGANIZATION = "Data Science Alliance"
AUTHORS = "Kyaw Soe Lwin & Adir Mancebo Jr."

# Geographic & Series Entities
NEIGHBORHOODS = [
    "Overall - reported footprint",
    "Overall - fixed core six",
    "East Village",
    "City Center",
    "Columbia",
    "Cortez",
    "Gaslamp",
    "Marina",
    "Outside Perimeter",
]

CORE_SIX_NEIGHBORHOODS = [
    "East Village",
    "City Center",
    "Columbia",
    "Cortez",
    "Gaslamp",
    "Marina",
]

DIGITIZED_COUNT_DATES = [
    "2018-01-24",
    "2018-06-27",
    "2018-12-19",
    "2019-01-30",
    "2020-01-31",
    "2021-02-25",
    "2022-01-27",
    "2022-03-01",  # Date anomaly noted in DSDP source maps
    "2023-01-31",
    "2024-01-25",
    "2025-01-31",
]

# Historical Multiplier Regimes
REGIME_EVENTS = [
    {
        "date": "2017-04-01",
        "label": "APR2017 Multipliers",
        "description": "Individual 1.0x, Tent 1.75x, Vehicle 1.66x",
        "color": "#D97706",
        "dash": "dot",
    },
    {
        "date": "2018-05-01",
        "label": "MAY2018 Multipliers",
        "description": "Vehicle multiplier increased to 2.03x",
        "color": "#D97706",
        "dash": "dash",
    },
    {
        "date": "2020-03-01",
        "label": "COVID-19 Emergency",
        "description": "Pandemic declaration; RTFH ceased multipliers for HUD PIT",
        "color": "#DC2626",
        "dash": "dashdot",
    },
    {
        "date": "2023-07-31",
        "label": "Unsafe Camping Ordinance",
        "description": "Enactment of City encampment ban across downtown rights-of-way",
        "color": "#7C3AED",
        "dash": "solid",
    },
]

# Thematic Color Palette (Executive Slate)
COLORS = {
    "primary": "#2563EB",         # Royal Blue
    "secondary": "#0D9488",       # Teal
    "background": "#F8FAFC",      # Slate 50
    "card": "#FFFFFF",            # Pure White
    "border": "#E2E8F0",          # Slate 200
    "text": "#0F172A",            # Slate 900
    "muted": "#64748B",           # Slate 500
    "success": "#16A34A",         # Emerald Green
    "warning": "#D97706",         # Amber
    "danger": "#DC2626",          # Crimson Red
    "purple": "#7C3AED",          # Ordinance Purple
}

# Getis-Ord Gi* Spatial Symbology Scale
HOTSPOT_PALETTE = {
    "99% Hotspot": "#B91C1C",     # Deep Red (z >= 2.576, p < 0.01)
    "95% Hotspot": "#EF4444",     # Red (z >= 1.960, p < 0.05)
    "90% Hotspot": "#F87171",     # Light Red (z >= 1.645, p < 0.10)
    "Not Significant": "#CBD5E1", # Neutral Grey
    "90% Coldspot": "#93C5FD",    # Light Blue (z <= -1.645, p < 0.10)
    "95% Coldspot": "#3B82F6",    # Blue (z <= -1.960, p < 0.05)
    "99% Coldspot": "#1D4ED8",    # Dark Blue (z <= -2.576, p < 0.01)
}

# Econometric Policy Regime Parameters (Assignment 8 Champion OLS)
# Model: Y = beta_0 + beta_1 * X + beta_2 * D_post
BETA_0 = 4513.26
BETA_1 = 0.1859
BETA_2 = 1225.04
STUDENT_T_CRITICAL_95 = 2.571     # df = 8 - 3 = 5, two-tailed alpha = 0.05
SIGMA_EPSILON = 799.20            # Residual standard error
X_BAR = 1245.50                   # Mean of historical downtown counts in paired sample
VAR_X = 184520.0                  # Variance of historical downtown counts in paired sample
MARGIN_OF_ERROR_APPROX = 2050     # Calibrated empirical margin of error (approx +/- 35%)
