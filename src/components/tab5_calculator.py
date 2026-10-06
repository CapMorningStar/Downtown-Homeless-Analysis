"""
Component 5: County-Level Estimation Calculator, Policy Regime OLS, and Governance Charter.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.utils import calculate_county_estimate, format_count
from src.data_loader import load_paired_county_data, load_forecast_data


def render_tab5():
    """Render Tab 5: County Estimation Calculator & Governance Charter."""
    st.markdown("### 🧮 Countywide Unsheltered Estimation Calculator & Governance Charter")
    st.markdown(
        """
        Translate monthly Downtown San Diego count observations into estimated San Diego County 
        unsheltered totals between annual Point-in-Time censuses. Governed by the validated **Policy Regime 
        OLS Model** from Assignment 8 and the **4 Mandatory Public Communication Rules**.
        """
    )

    # Statutory Governance Banner
    st.markdown(
        """
        <div class="banner-danger">
            <strong>⚠️ MANDATORY GOVERNANCE NOTICE (Task 8.4 Public Charter):</strong><br>
            This estimation tool is authorized <em>exclusively for interim directional tracking and macro capacity stress-testing</em>. 
            It is <strong>STRICTLY PROHIBITED</strong> for official HUD Continuum of Care submissions, statutory formula allocations, 
            or micro-regional sub-allocations. Single-point precision must never be communicated publicly.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input Layout
    in_col1, in_col2 = st.columns([1.5, 1])

    with in_col1:
        st.markdown("#### 1. Input Downtown Count Parameter")
        
        # Presets
        preset_cols = st.columns(4)
        preset_val = 985.38  # Default Dec 2025 baseline

        with preset_cols[0]:
            if st.button("📍 Dec 2025 (985)", help="Latest empirical monthly count"):
                st.session_state["downtown_input"] = 985.38
        with preset_cols[1]:
            fc = load_forecast_data()
            fc_col = "series" if "series" in fc.columns else "series_name"
            fc = fc[fc[fc_col] == "Overall - reported footprint"].sort_values("forecast_date") if not fc.empty else fc
            fc_val = float(fc["point_forecast"].iloc[0]) if len(fc) else 985.38
            fc_label = pd.Timestamp(fc["forecast_date"].iloc[0]).strftime("%b %Y") if len(fc) else "Forecast"
            if st.button(f"🔮 {fc_label} ({fc_val:,.0f})", help="Task 7.4 champion forecast, first forecast month"):
                st.session_state["downtown_input"] = round(fc_val, 2)
        with preset_cols[2]:
            if st.button("🔥 Peak Crisis (2,103)", help="Historical May 2023 maximum"):
                st.session_state["downtown_input"] = 2103.00
        with preset_cols[3]:
            if st.button("🧊 COVID Low (529)", help="March 2020 series low (COVID-19 onset)"):
                st.session_state["downtown_input"] = 529.09

        current_input = st.session_state.get("downtown_input", preset_val)

        dt_count = st.number_input(
            "Downtown Unsheltered Count (X):",
            min_value=100.0,
            max_value=3500.0,
            value=float(current_input),
            step=10.0,
            help="Enter any observed or hypothetical monthly count for Downtown San Diego.",
        )

        post_ordinance = st.toggle(
            "Active Unsafe Camping Ordinance Enforcement (Post-July 2023 Regime)",
            value=True,
            help="Accounts for the structural +1,225.04 countywide shift caused by encampment displacement out of downtown corridors.",
        )

    # Calculate Estimates
    calc_res = calculate_county_estimate(dt_count, post_ordinance=post_ordinance)

    with in_col2:
        st.markdown("#### 2. Calibrated Countywide Estimate")
        
        st.markdown(
            f"""
            <div class="dashboard-card" style="border: 2px solid #2563EB; background: #F8FAFC;">
                <div class="kpi-title">Calibrated Point & 95% Interval</div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #1E40AF; margin: 0.4rem 0;">
                    {calc_res['public_display_text']}
                </div>
                <div style="font-size: 0.82rem; color: #475569; border-top: 1px solid #CBD5E1; padding-top: 0.4rem; margin-top: 0.5rem;">
                    <strong>Enforced Public Disclosure:</strong><br>
                    • Rounded to nearest 100 individuals (Rule 2)<br>
                    • Exact Student's t 95% Prediction Interval [L to U] (Rule 3)<br>
                    • Margin of Error: <strong>±{calc_res['margin_of_error']:,.0f} individuals (±35%)</strong><br>
                    • <em>{calc_res['policy_context']}</em> (Rule 4)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # The 4 Public Communication Rules Callout
    st.markdown("#### 📋 The 4 Public Communication Rules Checklist")
    rule_c1, rule_c2, rule_c3, rule_c4 = st.columns(4)

    with rule_c1:
        st.markdown(
            f"""
            <div class="dashboard-card" style="padding: 0.8rem; border-top: 3px solid #DC2626;">
                <b style="color: #991B1B;">Rule 1: No Single Precision</b><br>
                <span style="font-size: 0.82rem; color: #475569;">
                    Raw estimate <del>{calc_res['raw_point_estimate']:,.0f}</del> is strictly prohibited from public press releases.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rule_c2:
        st.markdown(
            f"""
            <div class="dashboard-card" style="padding: 0.8rem; border-top: 3px solid #2563EB;">
                <b style="color: #1E40AF;">Rule 2: Round to 100s</b><br>
                <span style="font-size: 0.82rem; color: #475569;">
                    Mandatory reported point estimate: <strong>{calc_res['rounded_point_estimate']:,}</strong>.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rule_c3:
        st.markdown(
            f"""
            <div class="dashboard-card" style="padding: 0.8rem; border-top: 3px solid #0D9488;">
                <b style="color: #0F766E;">Rule 3: Calibrated Range</b><br>
                <span style="font-size: 0.82rem; color: #475569;">
                    Always state the full range: <strong>[{calc_res['rounded_lower_95']:,} to {calc_res['rounded_upper_95']:,}]</strong>.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rule_c4:
        st.markdown(
            f"""
            <div class="dashboard-card" style="padding: 0.8rem; border-top: 3px solid #7C3AED;">
                <b style="color: #6B21A8;">Rule 4: State Regime</b><br>
                <span style="font-size: 0.82rem; color: #475569;">
                    Must disclose enforcement status (Post-July 2023 Camping Ordinance active).
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Longitudinal Ratio Fragility Context
    with st.expander("📊 Why Simple Ratio Multipliers Failed (ANOVA Proof: F=66.51, p=0.0002)"):
        st.markdown(
            """
            Prior to Assignment 8, stakeholders commonly assumed that Downtown represents a fixed percentage (~20%) 
            of County homelessness. **Task 8.2 decisively rejected the constant-ratio hypothesis via One-Way ANOVA 
            (F=66.51, p=0.0002, η²=0.9638)**. The ratio fractured across three distinct policy regimes:
            """
        )
        paired_df = load_paired_county_data()
        if not paired_df.empty:
            # Ratio comparison chart
            fig_ratio = go.Figure()
            fig_ratio.add_trace(
                go.Bar(
                    x=paired_df["year"],
                    y=paired_df["share_of_county"],
                    name="Downtown Share of County Unsheltered (%)",
                    marker_color=["#2563EB" if y < 2022 else "#DC2626" if y in [2022, 2023] else "#7C3AED" for y in paired_df["year"]],
                    text=[f"{v:.1f}%" if pd.notnull(v) else "N/A" for v in paired_df["share_of_county"]],
                    textposition="outside",
                )
            )
            fig_ratio.update_layout(
                template="plotly_white",
                height=320,
                margin=dict(l=40, r=40, t=30, b=30),
                yaxis=dict(title="Downtown Share (%)", range=[0, 45], showgrid=True, gridcolor="#F1F5F9"),
                xaxis=dict(title="Annual PIT Census Year", tickmode="linear"),
            )
            st.plotly_chart(fig_ratio, width="stretch")

            st.markdown(
                """
                * **Baseline Epoch (2017–2020):** 17.9% average share (stable urban core).
                * **Peak Crisis Epoch (2022–2023):** 36.3% peak concentration (homelessness concentrated in downtown).
                * **Post-Ordinance Epoch (2024–2025):** 15.8% collapse (encampments pushed out of downtown into riverbeds and neighboring cities while county totals reached record highs).
                """
            )
