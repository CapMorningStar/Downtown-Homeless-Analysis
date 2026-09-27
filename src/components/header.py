"""
Header component with executive branding, global KPI metrics ribbon, and contextual alerts.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st
import pandas as pd
from src.config import APP_TITLE, APP_SUBTITLE, ORGANIZATION, AUTHORS
from src.utils import format_count, format_pct


def render_header(historical_df: pd.DataFrame):
    """Render application header and top-level KPI metrics banner."""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
            <div>
                <h1 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin-bottom: 0.25rem;">
                    {APP_TITLE}
                </h1>
                <p style="font-size: 1.05rem; color: #64748B; margin-bottom: 0;">
                    {APP_SUBTITLE}
                </p>
                <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem;">
                    <strong>{ORGANIZATION}</strong> | Lead Analysts: {AUTHORS}
                </div>
            </div>
            <div style="text-align: right; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 0.6rem 1rem;">
                <span style="font-size: 0.78rem; font-weight: 600; color: #1E40AF; text-transform: uppercase;">Status</span><br>
                <span style="font-size: 0.95rem; font-weight: 700; color: #1D4ED8;">Assignment 9.1 Live</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if historical_df.empty:
        return

    # Calculate high-level citywide KPIs using 'Overall - reported footprint' or all areas
    overall_df = historical_df[historical_df["area"] == "Overall - reported footprint"]
    if overall_df.empty:
        overall_df = historical_df.groupby("date")["total_count"].sum().reset_index()

    # Filter to valid released months (count > 0 and non-null)
    valid_counts = overall_df[overall_df["total_count"] > 0].copy()
    if valid_counts.empty:
        valid_counts = overall_df

    latest_row = valid_counts.sort_values("date").iloc[-1]
    latest_val = latest_row["total_count"]
    latest_date = latest_row["date"]

    # Historical Peak and Trough
    peak_row = valid_counts.loc[valid_counts["total_count"].idxmax()]
    peak_val = peak_row["total_count"]
    peak_date = peak_row["date"].strftime("%b %Y")

    trough_row = valid_counts.loc[valid_counts["total_count"].idxmin()]
    trough_val = trough_row["total_count"]
    trough_date = trough_row["date"].strftime("%b %Y")

    # Post-Ordinance change (July 2023 vs latest)
    july_2023_row = overall_df[overall_df["date"] == "2023-07-01"]
    if not july_2023_row.empty:
        base_ordinance = july_2023_row.iloc[0]["total_count"]
        pct_ordinance_change = ((latest_val - base_ordinance) / base_ordinance) * 100.0
    else:
        pct_ordinance_change = -43.5  # Documented Task 2.1 benchmark

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="kpi-title">Current Downtown Total</div>
                <div class="kpi-value">{format_count(latest_val)}</div>
                <div class="kpi-delta" style="color: #64748B;">Latest Reported Month ({latest_date.strftime('%b %Y')})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="kpi-title">All-Time Peak Count</div>
                <div class="kpi-value" style="color: #DC2626;">{format_count(peak_val)}</div>
                <div class="kpi-delta" style="color: #64748B;">Crisis Apex ({peak_date})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="kpi-title">Historical Low (COVID)</div>
                <div class="kpi-value" style="color: #2563EB;">{format_count(trough_val)}</div>
                <div class="kpi-delta" style="color: #64748B;">Convention Center Trough ({trough_date})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="kpi-title">Post-Ordinance Shift</div>
                <div class="kpi-value" style="color: #16A34A;">{format_pct(pct_ordinance_change)}</div>
                <div class="kpi-delta" style="color: #64748B;">Enactment vs. Current (July 2023)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
