"""
Standalone Production Forecasting CLI Pipeline (Task 7.4 & Task 9.4).
Downtown San Diego Homeless Population Analysis

Generates prospective 12-month forecasts across 9 downtown series with
80% and 95% prediction intervals and policy scenarios (-24% optimistic, +26% pessimistic).
"""

import sys
import argparse
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def main():
    parser = argparse.ArgumentParser(
        description="Prospective 12-Month Homelessness Forecasting CLI Pipeline (XGBoost Champion)"
    )
    parser.add_argument(
        "--series",
        type=str,
        default="Overall - reported footprint",
        help="Geographic series name (default: 'Overall - reported footprint')",
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=12,
        help="Forecast horizon in months (default: 12)",
    )
    args = parser.parse_args()

    forecast_file = DATA_DIR / "Forecasts_12Month.csv"
    if not forecast_file.exists():
        print(f"Error: {forecast_file} not found.", file=sys.stderr)
        return 1

    df = pd.read_csv(forecast_file)
    sub = df[df["series"] == args.series].head(args.horizon)

    if sub.empty:
        print(f"No forecast found for series: '{args.series}'. Available: {df['series'].unique().tolist()}")
        return 1

    print("\n=======================================================")
    print(f"PROSPECTIVE FORECAST: {args.series.upper()}")
    print("=======================================================")
    print(f"Champion Architecture: XGBoost (12-Month CV MAPE: 39.34% ± 25.36%)")
    print(f"Evaluation Horizon:    {args.horizon} Months")
    print("-------------------------------------------------------")
    print(f"{'Date':<12} {'Baseline':<10} {'80% PI':<18} {'95% PI':<18} {'Optimistic':<12} {'Pessimistic':<12}")
    print("-" * 82)

    for _, row in sub.iterrows():
        d_str = str(row["forecast_date"])[:10]
        base = row["point_forecast"]
        pi_80 = f"[{row['pi_80_lower']:.0f}–{row['pi_80_upper']:.0f}]"
        pi_95 = f"[{row['pi_95_lower']:.0f}–{row['pi_95_upper']:.0f}]"
        opt = row.get("scenario_optimistic", base * 0.76)
        pess = row.get("scenario_pessimistic", base * 1.26)
        print(f"{d_str:<12} {base:<10.1f} {pi_80:<18} {pi_95:<18} {opt:<12.1f} {pess:<12.1f}")

    print("=======================================================\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
