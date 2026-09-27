"""
Component 2: 12-Month Prospective Forecast View with Policy Scenarios and Uncertainty Envelopes.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import load_forecast_data, load_historical_data
from src.utils import calculate_scenario_forecast, format_count


def render_tab2():
    """Render Tab 2: 12-Month Prospective Forecast View."""
    st.markdown("### 🔮 12-Month Prospective Forecast Horizon (2026)")
    st.markdown(
        """
        Explore prospective 2026 unsheltered population projections produced by Assignment 7's 
        expanding-window walk-forward cross-validated machine learning and econometric champions. 
        Stress-test policy interventions under optimistic, status quo, and pessimistic scenarios.
        """
    )

    forecast_df = load_forecast_data()
    historical_df = load_historical_data()

    if forecast_df.empty:
        st.warning("Forecast dataset is currently unavailable.")
        return

    # Controls row
    c_col1, c_col2, c_col3 = st.columns([2, 1, 1])

    available_series = sorted(forecast_df["series"].unique().tolist()) if "series" in forecast_df.columns else ["Overall - reported footprint"]
    default_series = "Overall - reported footprint" if "Overall - reported footprint" in available_series else available_series[0]

    with c_col1:
        selected_series = st.selectbox(
            "Select Projection Series / Footprint:",
            options=available_series,
            index=available_series.index(default_series),
            help="Choose between headline downtown footprints and individual neighborhoods.",
        )

    with c_col2:
        model_family = st.selectbox(
            "Forecasting Model Architecture:",
            options=[
                "XGBoost Champion (CV MAPE: 39.3%)",
                "Holt-Winters Parametric (CV MAPE: 39.6%)",
                "SARIMA Seasonal Benchmark",
                "Prophet Additive GAM",
                "Naive Seasonal (t-12 Baseline)",
            ],
            index=0,
            help="XGBoost demonstrated superior multi-step cross-validation accuracy across 5 chronological folds.",
        )

    with c_col3:
        scenario_mode = st.radio(
            "Policy Scenario:",
            options=["Status Quo (Baseline)", "Optimistic (-24%)", "Pessimistic (+26%)", "Custom Stress-Test"],
            index=0,
            horizontal=False,
        )

    # Custom slider if selected
    custom_shift = 0.0
    if scenario_mode == "Custom Stress-Test":
        custom_shift = st.slider(
            "Month 12 Target Policy Shift (%):",
            min_value=-50,
            max_value=50,
            value=-15,
            step=5,
            format="%d%%",
            help="Simulate arbitrary policy interventions or macroeconomic supply shocks.",
        )

    # Uncertainty toggles
    u_col1, u_col2, _ = st.columns([1, 1, 2])
    with u_col1:
        show_pi_80 = st.checkbox("Show 80% Prediction Interval", value=True)
    with u_col2:
        show_pi_95 = st.checkbox("Show 95% Prediction Interval", value=True)

    # Filter forecast dataset for selected series
    series_col = "series" if "series" in forecast_df.columns else "series_name"
    f_sub = forecast_df[forecast_df[series_col] == selected_series].sort_values("forecast_date").copy()
    f_sub["forecast_date"] = pd.to_datetime(f_sub["forecast_date"])

    # Historical actuals tail (2024-2025)
    hist_tail = pd.DataFrame()
    if not historical_df.empty:
        h_area_match = historical_df[
            (historical_df["area"] == selected_series)
            & (historical_df["date"] >= "2024-01-01")
        ].sort_values("date")
        hist_tail = h_area_match

    # Plotly Figure
    fig = go.Figure()

    # 1. Historical Actuals Trace
    if not hist_tail.empty:
        fig.add_trace(
            go.Scatter(
                x=hist_tail["date"],
                y=hist_tail["total_count"],
                mode="lines+markers",
                name="Historical Actuals (2024–2025)",
                line=dict(color="#2563EB", width=2.5),
                marker=dict(size=5, color="#1D4ED8"),
                hovertemplate="<b>%{x|%b %Y} (Actual)</b><br>Count: <b>%{y:,.1f}</b><extra></extra>",
            )
        )

    # Calculate custom/active scenario line
    active_scenario_y = []
    for _, row in f_sub.iterrows():
        h = int(row.get("horizon", 1))
        pt = float(row["point_forecast"])
        if scenario_mode == "Status Quo (Baseline)":
            val = pt
        elif scenario_mode == "Optimistic (-24%)":
            val = row.get("scenario_optimistic", calculate_scenario_forecast(pt, h, 12, -0.24))
        elif scenario_mode == "Pessimistic (+26%)":
            val = row.get("scenario_pessimistic", calculate_scenario_forecast(pt, h, 12, 0.26))
        else:
            val = calculate_scenario_forecast(pt, h, 12, custom_shift / 100.0)
        active_scenario_y.append(val)

    # 2. Prediction Intervals (Shaded Envelopes)
    if show_pi_95 and "pi_95_upper" in f_sub.columns:
        fig.add_trace(
            go.Scatter(
                x=f_sub["forecast_date"].tolist() + f_sub["forecast_date"].tolist()[::-1],
                y=f_sub["pi_95_upper"].tolist() + f_sub["pi_95_lower"].tolist()[::-1],
                fill="toself",
                fillcolor="rgba(13, 148, 136, 0.12)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                name="95% Prediction Interval",
            )
        )

    if show_pi_80 and "pi_80_upper" in f_sub.columns:
        fig.add_trace(
            go.Scatter(
                x=f_sub["forecast_date"].tolist() + f_sub["forecast_date"].tolist()[::-1],
                y=f_sub["pi_80_upper"].tolist() + f_sub["pi_80_lower"].tolist()[::-1],
                fill="toself",
                fillcolor="rgba(13, 148, 136, 0.22)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                name="80% Prediction Interval",
            )
        )

    # 3. Baseline Point Forecast
    fig.add_trace(
        go.Scatter(
            x=f_sub["forecast_date"],
            y=f_sub["point_forecast"],
            mode="lines+markers",
            name="Baseline Champion Forecast",
            line=dict(color="#0D9488", width=3, dash="dash"),
            marker=dict(size=6, color="#0F766E"),
            hovertemplate="<b>%{x|%b %Y} (Baseline)</b><br>Forecast: <b>%{y:,.1f}</b><extra></extra>",
        )
    )

    # 4. Active Scenario Line (if not Baseline)
    if scenario_mode != "Status Quo (Baseline)":
        scen_color = "#16A34A" if "Optimistic" in scenario_mode or custom_shift < 0 else "#DC2626"
        fig.add_trace(
            go.Scatter(
                x=f_sub["forecast_date"],
                y=active_scenario_y,
                mode="lines+markers",
                name=f"Scenario: {scenario_mode}",
                line=dict(color=scen_color, width=3),
                marker=dict(size=6, color=scen_color),
                hovertemplate="<b>%{x|%b %Y} (Scenario)</b><br>Projected: <b>%{y:,.1f}</b><extra></extra>",
            )
        )

    # Vertical Forecast Horizon Boundary
    fig.add_vline(
        x="2026-01-01",
        line_width=1.5,
        line_dash="dot",
        line_color="#64748B",
    )
    fig.add_annotation(
        x="2026-01-01",
        y=1.02,
        yref="paper",
        text="<b>Forecast Horizon Start (2026)</b>",
        showarrow=False,
        font=dict(size=10, color="#475569"),
    )

    fig.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0),
        xaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="Unsheltered Population Estimate", showgrid=True, gridcolor="#F1F5F9"),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Forecast Metric Highlights
    m1_val = f_sub.iloc[0]["point_forecast"]
    m12_val = f_sub.iloc[-1]["point_forecast"]
    m12_scen = active_scenario_y[-1]

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Jan 2026 Baseline Projection", format_count(m1_val))
    with col_m2:
        st.metric("Dec 2026 Baseline Projection", format_count(m12_val), delta=f"{m12_val - m1_val:+.1f}")
    with col_m3:
        st.metric(f"Dec 2026 ({scenario_mode})", format_count(m12_scen), delta=f"{m12_scen - m12_val:+.1f}")

    # Model Evaluation Expander
    with st.expander("📊 View Model Cross-Validation Benchmarks (Task 7.3)"):
        st.markdown(
            """
            **5-Fold Walk-Forward Cross-Validation Performance:**
            Models were evaluated across 5 chronological expanding windows with zero data leakage.
            """
        )
        perf_data = [
            {"Model": "XGBoost Champion", "12-Mo CV MAPE": "39.34%", "12-Mo CV RMSE": "184.2", "Hold-Out Test MAPE": "38.48%", "Strengths": "Best non-linear adaptation to policy shifts"},
            {"Model": "Holt-Winters Exponential Smoothing", "12-Mo CV MAPE": "39.57%", "12-Mo CV RMSE": "188.5", "Hold-Out Test MAPE": "41.12%", "Strengths": "Stable parametric trend and variance anchor"},
            {"Model": "SARIMA (1,1,1)(1,0,1)[12]", "12-Mo CV MAPE": "43.12%", "12-Mo CV RMSE": "212.7", "Hold-Out Test MAPE": "44.20%", "Strengths": "Rigorous stationary differencing"},
            {"Model": "Prophet (Changepoints)", "12-Mo CV MAPE": "47.80%", "12-Mo CV RMSE": "245.1", "Hold-Out Test MAPE": "49.65%", "Strengths": "Calendar and holiday flexibility"},
            {"Model": "Naive Seasonal Baseline (t-12)", "12-Mo CV MAPE": "51.34%", "12-Mo CV RMSE": "278.9", "Hold-Out Test MAPE": "53.10%", "Strengths": "Simple heuristic comparison"},
        ]
        st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)
