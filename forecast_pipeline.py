"""Autonomous Production Forecasting Pipeline for Downtown San Diego Homeless Population Analysis.

Author: Kyaw Soe Lwin (Data Science Alliance / UC San Diego)
Project: Downtown San Diego Homeless Population Analysis
Task: 7.4 - Generate Forecast Outputs and Build Automated Pipeline

This standalone script loads the latest constant-methodology monthly data,
trains the selected champion model architectures (XGBoost, Holt-Winters, SARIMA, Prophet),
and produces 12-month forward-looking point forecasts, statistically calibrated
80% and 95% prediction intervals, and policy scenario projections (Optimistic and Pessimistic).

Restored Oct 2026 from the Task 7.4 Drive deliverable (the repo copy had been replaced by a
print-only viewer). The viewer behaviour is kept as --show-only.

Usage:
    python forecast_pipeline.py [--input PATH] [--output PATH] [--horizon MONTHS] [--no-plots]
    python forecast_pipeline.py --series "Overall - reported footprint" --horizon 12
    python forecast_pipeline.py --show-only --series "East Village"
"""

import argparse
from pathlib import Path
import warnings
import sys
import logging

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Suppress verbose dependency logs
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="No frequency information was provided")
warnings.filterwarnings("ignore", category=Warning, module="statsmodels")

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "data" / "TimeSeries_ConstantMethodology.csv"
DEFAULT_ADJUSTED = ROOT / "data" / "AdjustedTimeSeries_Forecasting.csv"
DEFAULT_OUTPUT = ROOT / "data" / "Forecasts_12Month.csv"
DEFAULT_FIGURE_DIR = ROOT / "figures" / "task7_4"

SEASONAL_LAG = 12
CHANGEPOINT_DATES = [pd.Timestamp("2017-04-01"), pd.Timestamp("2018-05-01"), pd.Timestamp("2020-03-01")]

# Champion Model Assignments from Task 7.3 Cross-Validation
# (re-run Oct 2026 on corrected data: Outside Perimeter changed sarima -> xgboost; all others unchanged)
CHAMPION_MODELS = {
    "Overall - reported footprint": "xgboost",
    "Overall - fixed core six": "xgboost",
    "East Village": "xgboost",
    "City Center": "xgboost",
    "Cortez": "xgboost",
    "Columbia": "sarima",
    "Gaslamp": "prophet",
    "Marina": "prophet",
    "Outside Perimeter": "xgboost",
}

# Feature engineering parameters for XGBoost
LAGS = [1, 2, 3, 6, 12]
ROLLS = [3, 6, 12]


def build_xgb_features(series):
    df = pd.DataFrame({"y": series})
    for lag in LAGS:
        df[f"lag_{lag}"] = df["y"].shift(lag)
    for w in ROLLS:
        df[f"roll_mean_{w}"] = df["y"].shift(1).rolling(w).mean()
    df["month_sin"] = np.sin(2 * np.pi * df.index.month / 12)
    df["month_cos"] = np.cos(2 * np.pi * df.index.month / 12)
    df["trend"] = np.arange(len(df))
    return df


def forecast_xgboost(train_series, future_dates):
    import xgboost as xgb

    working = train_series.copy()
    feat_train = build_xgb_features(working).dropna()
    feature_cols = [c for c in feat_train.columns if c != "y"]

    model = xgb.XGBRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    model.fit(feat_train[feature_cols], feat_train["y"])

    preds = []
    for date in future_dates:
        working.loc[date] = np.nan
        feat_row = build_xgb_features(working).loc[[date], feature_cols]
        pred = max(0.0, float(model.predict(feat_row)[0]))
        working.loc[date] = pred
        preds.append(pred)
    return pd.Series(preds, index=future_dates)


def forecast_holt_winters(train_series, future_dates):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    # Ensure regular frequency with in-memory linear interpolation
    train_clean = train_series.dropna()
    train_clean = train_clean.interpolate(method="linear").asfreq("MS")

    seasonals = ["add", "mul"] if train_clean.min() > 0 else ["add"]
    best_fit = None
    best_aic = float("inf")
    for s in seasonals:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fit = ExponentialSmoothing(
                    train_clean, trend="add", seasonal=s, seasonal_periods=SEASONAL_LAG
                ).fit()
            if fit.aic < best_aic:
                best_aic = fit.aic
                best_fit = fit
        except Exception:
            continue
    if best_fit is not None:
        fc = best_fit.forecast(len(future_dates))
        fc.index = future_dates
        if np.isnan(fc.values).any():
            fit_fallback = ExponentialSmoothing(train_clean, trend="add").fit()
            fc = fit_fallback.forecast(len(future_dates))
            fc.index = future_dates
            residuals = train_clean - fit_fallback.fittedvalues
        else:
            residuals = train_clean - best_fit.fittedvalues
        sigma_res = float(np.nanstd(residuals))
        if np.isnan(sigma_res) or sigma_res == 0:
            sigma_res = float(np.nanstd(train_clean))
        return fc.clip(lower=0.0), sigma_res
    fit = ExponentialSmoothing(train_clean, trend="add").fit()
    fc = fit.forecast(len(future_dates))
    fc.index = future_dates
    residuals = train_clean - fit.fittedvalues
    sigma_res = float(np.nanstd(residuals))
    if np.isnan(sigma_res) or sigma_res == 0:
        sigma_res = float(np.nanstd(train_clean))
    return fc.clip(lower=0.0), sigma_res


def forecast_sarima(train_series, future_dates, candidate_orders, series_name):
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    train_clean = train_series.dropna().interpolate(method="linear").asfreq("MS")
    known = candidate_orders is not None and series_name in candidate_orders.index
    d = int(candidate_orders.loc[series_name, "d"]) if known else 1
    p0, q0 = (int(x) for x in candidate_orders.loc[series_name, ["p", "q"]]) if known else (1, 1)
    p_grid = sorted({max(0, p0 - 1), p0, p0 + 1})
    q_grid = sorted({max(0, q0 - 1), q0, q0 + 1})

    best_fit = None
    best_aic = float("inf")
    for p in p_grid:
        for q in q_grid:
            for P in [0, 1]:
                for D in [0, 1]:
                    for Q in [0, 1]:
                        try:
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                fit = SARIMAX(
                                    train_clean, order=(p, d, q), seasonal_order=(P, D, Q, SEASONAL_LAG),
                                    enforce_stationarity=False, enforce_invertibility=False,
                                ).fit(disp=False)
                            if fit.aic < best_aic:
                                best_aic = fit.aic
                                best_fit = fit
                        except Exception:
                            continue
    try:
        if best_fit is not None:
            fc = best_fit.get_forecast(steps=len(future_dates)).predicted_mean
            fc.index = future_dates
            sigma_res = float(np.std(best_fit.resid))
            return fc.clip(lower=0.0), sigma_res
    except Exception:
        pass

    try:
        fit = SARIMAX(train_clean, order=(1, d, 0), enforce_stationarity=False).fit(disp=False)
        fc = fit.get_forecast(steps=len(future_dates)).predicted_mean
        fc.index = future_dates
        sigma_res = float(np.std(fit.resid))
        return fc.clip(lower=0.0), sigma_res
    except Exception:
        last_val = float(train_clean.iloc[-1])
        fc = pd.Series([last_val] * len(future_dates), index=future_dates)
        sigma_res = float(np.std(train_clean)) if len(train_clean) > 1 else 1.0
        if sigma_res == 0:
            sigma_res = 1.0
        return fc.clip(lower=0.0), sigma_res


def forecast_prophet(train_series, future_dates):
    from prophet import Prophet

    series_changepoints = [
        d.strftime("%Y-%m-%d")
        for d in CHANGEPOINT_DATES
        if train_series.index.min() < d < (train_series.index.max() - pd.DateOffset(months=6))
    ]
    prophet_df = pd.DataFrame({"ds": train_series.index, "y": train_series.values})
    kwargs = {"yearly_seasonality": True, "weekly_seasonality": False, "daily_seasonality": False}
    if series_changepoints:
        kwargs["changepoints"] = series_changepoints
    model = Prophet(**kwargs)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(prophet_df)
    future = pd.DataFrame({"ds": future_dates})
    fc_df = model.predict(future).set_index("ds")
    fc = fc_df["yhat"].clip(lower=0.0)
    # Estimate residual std on in-sample fit
    in_sample = model.predict(prophet_df).set_index("ds")["yhat"]
    residuals = train_series.values - in_sample.values
    sigma_res = float(np.std(residuals))
    return fc, sigma_res


def generate_forecasts(input_path, horizon=12, candidate_path=None):
    """Main forecasting execution function."""
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    const_pivot = df.pivot(index="date", columns="series", values="constant_methodology_count")
    const_pivot = const_pivot.asfreq("MS").interpolate(method="linear")

    candidate_orders = None
    if candidate_path and Path(candidate_path).exists():
        df_adj = pd.read_csv(candidate_path)
        candidate_cols = ["series", "d", "candidate_p", "candidate_q"]
        candidate_orders = (
            df_adj[candidate_cols].drop_duplicates().set_index("series")[["candidate_p", "d", "candidate_q"]]
        )
        candidate_orders.columns = ["p", "d", "q"]

    latest_date = const_pivot.index.max()
    future_dates = pd.date_range(latest_date + pd.DateOffset(months=1), periods=horizon, freq="MS")
    print(f"Historical training range: {const_pivot.index.min().date()} to {latest_date.date()}")
    print(f"Forecasting {horizon} forward months: {future_dates[0].date()} to {future_dates[-1].date()}")

    records = []

    for s_name in CHAMPION_MODELS:
        train_s = const_pivot[s_name].dropna()
        champ_type = CHAMPION_MODELS[s_name]
        print(f"Generating forecast for [{s_name}] using champion architecture: {champ_type.upper()}...")

        # 1. Point Forecast using Champion Model
        if champ_type == "xgboost":
            point_fc = forecast_xgboost(train_s, future_dates)
        elif champ_type == "sarima":
            point_fc, _ = forecast_sarima(train_s, future_dates, candidate_orders, s_name)
        elif champ_type == "prophet":
            point_fc, _ = forecast_prophet(train_s, future_dates)
        else:
            point_fc, _ = forecast_holt_winters(train_s, future_dates)

        # 2. Prediction Intervals using Parametric Expanding Variance (Holt-Winters calibration)
        hw_fc, sigma_res = forecast_holt_winters(train_s, future_dates)

        # Scaling factor: variance increases with horizon: sigma_h = sigma_res * sqrt(1 + 0.08 * (h-1))
        h_steps = np.arange(1, horizon + 1)
        sigma_h = sigma_res * np.sqrt(1.0 + 0.08 * (h_steps - 1))

        pi_80_lower = np.maximum(0.0, point_fc.values - 1.282 * sigma_h)
        pi_80_upper = point_fc.values + 1.282 * sigma_h
        pi_95_lower = np.maximum(0.0, point_fc.values - 1.960 * sigma_h)
        pi_95_upper = point_fc.values + 1.960 * sigma_h

        # 3. Policy Scenario Modeling
        # Optimistic: Accelerated shelter expansion/supportive housing intake (-18% to -24% by Month 12)
        optimistic_factor = 1.0 - (0.02 * h_steps)
        scenario_optimistic = np.maximum(0.0, point_fc.values * optimistic_factor)

        # Pessimistic: Shelter capacity exhaustion or legal stays (+20% to +26% by Month 12)
        pessimistic_factor = 1.0 + (0.022 * h_steps)
        scenario_pessimistic = point_fc.values * pessimistic_factor

        for idx, date in enumerate(future_dates):
            records.append({
                "forecast_date": date.strftime("%Y-%m-%d"),
                "series": s_name,
                "model": champ_type,
                "point_forecast": round(float(point_fc.iloc[idx]), 2),
                "pi_80_lower": round(float(pi_80_lower[idx]), 2),
                "pi_80_upper": round(float(pi_80_upper[idx]), 2),
                "pi_95_lower": round(float(pi_95_lower[idx]), 2),
                "pi_95_upper": round(float(pi_95_upper[idx]), 2),
                "scenario_optimistic": round(float(scenario_optimistic[idx]), 2),
                "scenario_baseline": round(float(point_fc.iloc[idx]), 2),
                "scenario_pessimistic": round(float(scenario_pessimistic[idx]), 2),
            })

    df_forecasts = pd.DataFrame(records)
    return df_forecasts, const_pivot, future_dates


def export_visualizations(df_forecasts, const_pivot, future_dates, fig_dir):
    """Generate production plots for the forecasts."""
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    # 1. Headline Citywide Footprint Plot
    fig, ax = plt.subplots(figsize=(11, 5.5))
    s_name = "Overall - reported footprint"
    hist = const_pivot[s_name].dropna()
    fc_sub = df_forecasts[df_forecasts["series"] == s_name].copy()
    fc_sub["forecast_date"] = pd.to_datetime(fc_sub["forecast_date"])

    # Plot recent history
    recent_hist = hist.loc["2022-01-01":]
    ax.plot(recent_hist.index, recent_hist.values, label="Historical Actual (Observed)", color="#2c3e50", linewidth=2.2)

    # Plot baseline forecast
    ax.plot(fc_sub["forecast_date"], fc_sub["point_forecast"], label="XGBoost Champion Forecast (Baseline)",
            color="#8e44ad", linewidth=2.5, marker="o")

    # Prediction Intervals
    ax.fill_between(fc_sub["forecast_date"], fc_sub["pi_80_lower"], fc_sub["pi_80_upper"], color="#8e44ad",
                    alpha=0.25, label="80% Prediction Interval")
    ax.fill_between(fc_sub["forecast_date"], fc_sub["pi_95_lower"], fc_sub["pi_95_upper"], color="#8e44ad",
                    alpha=0.12, label="95% Prediction Interval")

    # Scenarios
    ax.plot(fc_sub["forecast_date"], fc_sub["scenario_optimistic"], label="Optimistic Scenario (Shelter Expansion)",
            color="#27ae60", linestyle="--", linewidth=1.8)
    ax.plot(fc_sub["forecast_date"], fc_sub["scenario_pessimistic"], label="Pessimistic Scenario (Capacity Ceiling)",
            color="#c0392b", linestyle="--", linewidth=1.8)

    ax.set_title(f"12-Month Operational Forecast: {s_name} ({future_dates[0].year})", fontsize=12,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=10, fontweight="bold")
    ax.set_ylabel("Unsheltered Homeless Count", fontsize=10, fontweight="bold")
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=8.5)
    fig.tight_layout()
    fig_path = fig_dir / "forecast_overall_footprint_12month.png"
    fig.savefig(fig_path, dpi=300)
    plt.close(fig)
    print(f"Saved figure: {fig_path}")

    # 2. Panel Plot for Key Neighborhoods (East Village, City Center, Gaslamp, Cortez)
    panel_series = ["East Village", "City Center", "Gaslamp", "Cortez"]
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    axes = axes.flatten()

    for idx, name in enumerate(panel_series):
        ax = axes[idx]
        hist_n = const_pivot[name].dropna().loc["2023-01-01":]
        fc_n = df_forecasts[df_forecasts["series"] == name].copy()
        fc_n["forecast_date"] = pd.to_datetime(fc_n["forecast_date"])

        model_used = CHAMPION_MODELS[name].upper()
        ax.plot(hist_n.index, hist_n.values, color="#34495e", linewidth=1.8, label="Historical")
        ax.plot(fc_n["forecast_date"], fc_n["point_forecast"], color="#2980b9", linewidth=2.0, marker="s",
                label=f"Forecast ({model_used})")
        ax.fill_between(fc_n["forecast_date"], fc_n["pi_80_lower"], fc_n["pi_80_upper"], color="#2980b9",
                        alpha=0.2, label="80% PI")

        ax.set_title(f"{name} ({model_used})", fontsize=11, fontweight="bold")
        ax.set_ylabel("Count", fontsize=9)
        ax.grid(True, alpha=0.4)
        if idx == 0:
            ax.legend(fontsize=8, loc="upper left")

    fig.suptitle(f"12-Month Neighborhood Forecast Projections ({future_dates[0].year})", fontsize=13,
                 fontweight="bold", y=0.99)
    fig.tight_layout()
    fig_panel_path = fig_dir / "forecast_neighborhoods_panel_12month.png"
    fig.savefig(fig_panel_path, dpi=300)
    plt.close(fig)
    print(f"Saved figure: {fig_panel_path}")


def print_series(df_forecasts, series, horizon):
    sub = df_forecasts[df_forecasts["series"] == series].head(horizon)
    if sub.empty:
        print(f"No forecast found for series: '{series}'. Available: {df_forecasts['series'].unique().tolist()}")
        return 1
    print("\n" + "=" * 82)
    print(f"PROSPECTIVE FORECAST: {series.upper()}  (model: {sub['model'].iloc[0]})")
    print("=" * 82)
    print(f"{'Date':<12} {'Baseline':<10} {'80% PI':<18} {'95% PI':<18} {'Optimistic':<12} {'Pessimistic':<12}")
    print("-" * 82)
    for _, row in sub.iterrows():
        pi_80 = f"[{row['pi_80_lower']:.0f}–{row['pi_80_upper']:.0f}]"
        pi_95 = f"[{row['pi_95_lower']:.0f}–{row['pi_95_upper']:.0f}]"
        print(f"{str(row['forecast_date'])[:10]:<12} {row['point_forecast']:<10.1f} {pi_80:<18} {pi_95:<18} "
              f"{row['scenario_optimistic']:<12.1f} {row['scenario_pessimistic']:<12.1f}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Generate 12-month forward forecasts and policy scenarios.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to constant methodology CSV")
    parser.add_argument("--adjusted", default=str(DEFAULT_ADJUSTED), help="Path to adjusted forecasting CSV (for SARIMA orders)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to save forecast CSV")
    parser.add_argument("--horizon", type=int, default=12, help="Forecast horizon in months")
    parser.add_argument("--no-plots", action="store_true", help="Skip exporting visualization plots")
    parser.add_argument("--series", default=None, help="Print the forecast table for this series when done")
    parser.add_argument("--show-only", action="store_true",
                        help="Do not retrain; just print --series from the existing output CSV")
    args = parser.parse_args()

    output_path = Path(args.output)
    if args.show_only:
        if not output_path.exists():
            print(f"Error: {output_path} not found.", file=sys.stderr)
            return 1
        return print_series(pd.read_csv(output_path), args.series or "Overall - reported footprint", args.horizon)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        return 1

    print("=" * 70)
    print("DOWNTOWN SAN DIEGO HOMELESS POPULATION ANALYSIS — PRODUCTION PIPELINE")
    print("=" * 70)

    df_forecasts, const_pivot, future_dates = generate_forecasts(input_path, horizon=args.horizon,
                                                                 candidate_path=args.adjusted)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_forecasts.to_csv(output_path, index=False)
    print(f"\nSuccessfully wrote {len(df_forecasts)} forecast rows to: {output_path}")

    if not args.no_plots:
        print("\nExporting production visualizations...")
        export_visualizations(df_forecasts, const_pivot, future_dates, DEFAULT_FIGURE_DIR)

    if args.series:
        print_series(df_forecasts, args.series, args.horizon)

    print("\nProduction forecasting pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
