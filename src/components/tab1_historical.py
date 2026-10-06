"""
Component 1: Historical Trends View with Methodology Change Markers and Multiplier Regimes.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.config import REGIME_EVENTS, COLORS, NEIGHBORHOODS
from src.data_loader import load_all_components_data


def render_tab1(historical_df: pd.DataFrame):
    """Render Tab 1: Historical Trends View."""
    st.markdown("### 📈 Longitudinal Unsheltered Population Trends (2017–2025)")
    st.markdown(
        """
        Analyze multi-year trends across Downtown San Diego. Filter by neighborhood, examine the impact 
        of multiplier schedule updates, and evaluate the sharp contraction following the July 2023 Unsafe Camping Ordinance.
        """
    )

    if historical_df.empty:
        st.warning("Historical dataset is currently unavailable.")
        return

    # Filter row
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])

    available_areas = sorted(historical_df["area"].unique().tolist())
    default_areas = (
        ["Overall - reported footprint"]
        if "Overall - reported footprint" in available_areas
        else available_areas[:1]
    )

    with f_col1:
        selected_areas = st.multiselect(
            "Select Reporting Footprint / Neighborhood(s):",
            options=available_areas,
            default=default_areas,
            help="Compare citywide aggregate footprints or individual neighborhoods.",
        )

    with f_col2:
        show_regimes = st.checkbox("Show Policy & Regime Markers", value=True)
        show_shaded_epochs = st.checkbox("Highlight Macro Epochs", value=True)

    with f_col3:
        breakdown_enabled = len(selected_areas) == 1 and not selected_areas[0].startswith("Overall")
        show_components = st.checkbox(
            "Show Component Breakdown",
            value=False,
            disabled=not breakdown_enabled,
            help="Break down into individuals, tents, and vehicles (available when a single neighborhood is selected).",
        )

    # Date Range Filter
    min_date = historical_df["date"].min().to_pydatetime()
    max_date = historical_df["date"].max().to_pydatetime()

    date_range = st.slider(
        "Date Range Filter:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY",
    )

    # Fallback to default if user cleared multiselect
    active_areas = selected_areas if selected_areas else default_areas

    # Filter dataset
    filtered_df = historical_df[
        (historical_df["area"].isin(active_areas))
        & (historical_df["date"] >= pd.Timestamp(date_range[0]))
        & (historical_df["date"] <= pd.Timestamp(date_range[1]))
    ].copy()

    # Build Interactive Plotly Figure
    fig = go.Figure()

    if show_components and breakdown_enabled:
        # Load component data for the single selected neighborhood
        comp_df = load_all_components_data()
        sub_comp = comp_df[
            (comp_df["area"] == active_areas[0])
            & (comp_df["component"].isin(["individual", "tent", "vehicle"]))
            & (comp_df["date"] >= pd.Timestamp(date_range[0]))
            & (comp_df["date"] <= pd.Timestamp(date_range[1]))
        ].sort_values("date")

        comp_colors = {"individual": "#2563EB", "tent": "#D97706", "vehicle": "#0D9488"}
        comp_names = {"individual": "Individuals (1.0x)", "tent": "Tents/Structures (1.75x)", "vehicle": "Vehicles (2.03x)"}

        for comp in ["individual", "tent", "vehicle"]:
            cd = sub_comp[sub_comp["component"] == comp]
            fig.add_trace(
                go.Bar(
                    x=cd["date"],
                    y=cd["total_count"],
                    name=comp_names.get(comp, comp.title()),
                    marker_color=comp_colors.get(comp, "#94A3B8"),
                )
            )
        fig.update_layout(barmode="stack")

    else:
        # Standard Multi-Line Comparison
        for area in active_areas:
            sub = filtered_df[filtered_df["area"] == area].sort_values("date")
            is_headline = "Overall" in area
            fig.add_trace(
                go.Scatter(
                    x=sub["date"],
                    y=sub["total_count"],
                    mode="lines+markers",
                    name=area,
                    line=dict(width=3 if is_headline else 2),
                    marker=dict(size=5),
                    hovertemplate="<b>%{x|%b %Y}</b><br>Area: "
                    + area
                    + "<br>Count: <b>%{y:,.1f}</b><extra></extra>",
                )
            )

    # Shaded Epochs
    if show_shaded_epochs:
        # COVID-19 Emergency
        fig.add_vrect(
            x0="2020-03-01",
            x1="2021-06-01",
            fillcolor="#FEE2E2",
            opacity=0.35,
            layer="below",
            line_width=0,
            annotation_text="COVID-19 Shelter Operation",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#991B1B"),
        )
        # Post-Camping Ordinance
        fig.add_vrect(
            x0="2023-07-31",
            x1=max_date.strftime("%Y-%m-%d"),
            fillcolor="#F3E8FF",
            opacity=0.35,
            layer="below",
            line_width=0,
            annotation_text="Camping Ordinance Enforcement",
            annotation_position="top right",
            annotation_font=dict(size=10, color="#6B21A8"),
        )

    # Vertical Policy Markers
    if show_regimes:
        for event in REGIME_EVENTS:
            evt_date = pd.Timestamp(event["date"])
            if date_range[0] <= evt_date <= date_range[1]:
                fig.add_vline(
                    x=event["date"],
                    line_width=1.5,
                    line_dash=event["dash"],
                    line_color=event["color"],
                )
                fig.add_annotation(
                    x=event["date"],
                    y=1.02,
                    yref="paper",
                    text=f"<b>{event['label']}</b>",
                    showarrow=False,
                    font=dict(size=9, color=event["color"]),
                    textangle=-45,
                )

    fig.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0),
        xaxis=dict(title="", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="Estimated Unsheltered Individuals", showgrid=True, gridcolor="#F1F5F9"),
        hovermode="x unified",
    )

    st.plotly_chart(fig, width="stretch")

    # Contextual Summary Callout
    st.markdown(
        """
        <div class="banner-info">
            <strong>Key Analytical Finding:</strong> 
            Downtown San Diego experienced an unprecedented apex in <strong>May 2023 (2,103 unsheltered individuals)</strong>. 
            Following the July 2023 enactment of the Unsafe Camping Ordinance, counts collapsed by <strong>43.5%</strong>. 
            However, cross-sectional evaluation against RTFH Point-in-Time counts reveals regional displacement into outlying municipalities rather than net exit from homelessness.
        </div>
        """,
        unsafe_allow_html=True,
    )
