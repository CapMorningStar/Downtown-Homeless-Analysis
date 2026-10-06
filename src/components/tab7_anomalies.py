"""
Tab 7: Anomaly Surveillance & Automated Alert Management Component
Interactive Quality Control Dashboard, CUSUM drift monitors, and Alert Review Form.
Downtown San Diego Homeless Population Analysis - Task 10.4
"""

from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from anomaly_detection.pipeline import AnomalySurveillancePipeline
from anomaly_detection.alerting import AlertEngine, AlertSeverity, AlertStatus


def render_tab7():
    """Renders Tab 7: Anomaly Surveillance & Alert Management."""
    st.markdown("### 🚨 Anomaly Surveillance & Automated Alert Management")
    st.markdown(
        """
        Continuous statistical quality control (Shewhart $\\mu \\pm 2\\sigma / 3\\sigma$, Tabular CUSUM) 
        and multivariate model-based outlier detection (Isolation Forest & Conformal Residual Bounds).
        """
    )

    # Sidebar / Parameter Expander
    with st.expander("⚙️ Anomaly Detection & Sensitivity Controls", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            win = st.slider("Rolling Window (Months)", min_value=6, max_value=24, value=12, step=1)
        with c2:
            warn_sig = st.slider("Warning Limit (σ)", min_value=1.5, max_value=2.5, value=2.0, step=0.1)
        with c3:
            crit_sig = st.slider("Action Limit (σ)", min_value=2.5, max_value=4.0, value=3.0, step=0.1)
        with c4:
            cusum_h = st.slider("CUSUM Threshold (h)", min_value=2.5, max_value=6.0, value=4.0, step=0.5)

    # Initialize Pipeline
    pipeline = AnomalySurveillancePipeline()
    pipeline.shewhart.window = win
    pipeline.shewhart.warning_sigma = warn_sig
    pipeline.shewhart.critical_sigma = crit_sig
    pipeline.cusum.window = win
    pipeline.cusum.threshold_h = cusum_h

    classified_df, event_df, summary = pipeline.run_surveillance()
    alert_engine = pipeline.alert_engine
    alerts = alert_engine.load_alerts_store()

    # Top KPI Ribbon
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Monitored Months", f"{summary['total_months']} M")
    with k2:
        st.metric("Total Anomalies", f"{summary['total_anomalies_detected']}")
    with k3:
        st.metric("Count Spikes / Drops", f"{summary['count_spikes']} / {summary['count_drops']}")
    with k4:
        st.metric("Spatial / QA Shifts", f"{summary['spatial_shifts']} / {summary['data_quality_issues']}")
    with k5:
        crit_count = sum(1 for a in alerts if a.get("severity") == "CRITICAL" and a.get("status") == "NEW")
        st.metric("Unreviewed Critical", f"{crit_count}", delta=f"{len(alerts)} total", delta_color="inverse")

    st.markdown("---")

    # Plotly Interactive Control Chart & CUSUM Subplot
    st.markdown("#### 1. Statistical Quality Control Chart & Drift Accumulators")

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.7, 0.3],
        subplot_titles=("Shewhart Control Chart with ±2σ and ±3σ Action Bands", "Tabular CUSUM Drift Accumulators (S⁺ & S⁻)"),
    )

    dates = pd.to_datetime(classified_df["date"])
    y = classified_df["value"]
    cl = classified_df["center_line"]
    ucl_w = classified_df["ucl_warning"]
    lcl_w = classified_df["lcl_warning"]
    ucl_c = classified_df["ucl_critical"]
    lcl_c = classified_df["lcl_critical"]

    # Critical Band (Red)
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=ucl_c,
            mode="lines",
            line=dict(color="rgba(239, 68, 68, 0.3)", width=0),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=lcl_c,
            mode="lines",
            line=dict(color="rgba(239, 68, 68, 0.3)", width=0),
            fill="tonexty",
            fillcolor="rgba(254, 226, 226, 0.45)",
            name="±3σ Action Limit",
        ),
        row=1,
        col=1,
    )

    # Warning Band (Yellow)
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=ucl_w,
            mode="lines",
            line=dict(color="rgba(245, 158, 11, 0.3)", width=0),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=lcl_w,
            mode="lines",
            line=dict(color="rgba(245, 158, 11, 0.3)", width=0),
            fill="tonexty",
            fillcolor="rgba(254, 243, 199, 0.65)",
            name="±2σ Warning Limit",
        ),
        row=1,
        col=1,
    )

    # Center Line & Historical Series
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=cl,
            mode="lines",
            line=dict(color="#2563EB", width=2, dash="dash"),
            name="12M Rolling Mean",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=y,
            mode="lines+markers",
            line=dict(color="#0F172A", width=2.2),
            marker=dict(size=4.5),
            name="Monthly Count (Adjusted)",
        ),
        row=1,
        col=1,
    )

    # Highlight Anomalies
    type_styles = {
        "Count Spike": {"color": "#DC2626", "symbol": "triangle-up", "size": 11},
        "Count Drop": {"color": "#2563EB", "symbol": "triangle-down", "size": 11},
        "Spatial Shift": {"color": "#D97706", "symbol": "square", "size": 10},
        "Potential Data Quality Issue": {"color": "#9333EA", "symbol": "diamond", "size": 10},
    }

    for typ, style in type_styles.items():
        subset = classified_df[classified_df["is_classified_anomaly"] & (classified_df["anomaly_typology"] == typ)]
        if not subset.empty:
            fig.add_trace(
                go.Scatter(
                    x=pd.to_datetime(subset["date"]),
                    y=subset["value"],
                    mode="markers",
                    marker=dict(color=style["color"], symbol=style["symbol"], size=style["size"], line=dict(color="#0F172A", width=1.2)),
                    name=f"Anomaly: {typ}",
                    text=subset["anomaly_description"],
                    hovertemplate="<b>%{x|%b %Y}</b><br>Count: %{y:,.0f}<br>%{text}<extra></extra>",
                ),
                row=1,
                col=1,
            )

    # Panel 2: CUSUM Drift
    s_pos = classified_df["cusum_s_pos"]
    s_neg = classified_df["cusum_s_neg"]

    fig.add_trace(
        go.Bar(
            x=dates,
            y=s_pos,
            marker_color="#DC2626",
            opacity=0.75,
            name="CUSUM S⁺ (Surge)",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=dates,
            y=-s_neg,
            marker_color="#2563EB",
            opacity=0.75,
            name="CUSUM S⁻ (Drop)",
        ),
        row=2,
        col=1,
    )
    fig.add_hline(y=cusum_h, line_dash="dash", line_color="#991B1B", row=2, col=1)
    fig.add_hline(y=-cusum_h, line_dash="dash", line_color="#1E40AF", row=2, col=1)

    fig.update_layout(
        height=680,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("---")

    # Alert Review and Management Panel
    st.markdown("#### 2. Alert Management & Incident Review Panel")

    filter_c1, filter_c2 = st.columns([1, 1])
    with filter_c1:
        status_filter = st.selectbox("Filter by Status", ["ALL", "NEW", "REVIEWED", "DISMISSED"], index=0)
    with filter_c2:
        severity_filter = st.selectbox("Filter by Severity", ["ALL", "CRITICAL", "WARNING", "INFO"], index=0)

    alerts_df = pd.DataFrame(alerts) if alerts else pd.DataFrame()

    if not alerts_df.empty:
        filtered = alerts_df.copy()
        if status_filter != "ALL":
            filtered = filtered[filtered["status"] == status_filter]
        if severity_filter != "ALL":
            filtered = filtered[filtered["severity"] == severity_filter]

        display_cols = ["alert_id", "month_date", "classification", "severity", "metric_value", "baseline_center_line", "status", "reviewer", "reviewer_notes"]
        present_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[present_cols].sort_values("month_date", ascending=False), width="stretch", height=280)

        # Interactive Review Action
        st.markdown("##### 📝 Review and Action Alert")
        unreviewed = [a["alert_id"] for a in alerts if a.get("status") in ["NEW", "REVIEWED"]]

        if unreviewed:
            r_col1, r_col2, r_col3 = st.columns([2, 2, 1])
            with r_col1:
                selected_alert_id = st.selectbox("Select Alert to Resolve", unreviewed)
            with r_col2:
                reviewer_name = st.text_input("Reviewer Name", value="Kyaw Soe Lwin (Lead Analyst)")
            with r_col3:
                new_status = st.selectbox("Updated Status", ["REVIEWED", "DISMISSED"], index=0)

            resolution_notes = st.text_area(
                "Resolution / Operational Action Notes",
                placeholder="Document operational investigation findings (e.g., confirmed field displacement to Chula Vista; emergency beds added)...",
            )

            if st.button("💾 Submit Alert Review", type="primary"):
                if resolution_notes.strip():
                    alert_engine.mark_as_reviewed(selected_alert_id, reviewer_name, resolution_notes, new_status=new_status)
                    st.success(f"✓ Alert {selected_alert_id} successfully updated to '{new_status}'!")
                    st.rerun()
                else:
                    st.warning("Please provide resolution notes before submitting review.")
        else:
            st.info("✓ All alerts have been reviewed and archived.")
    else:
        st.info("No active alerts detected in the surveillance matrix.")
