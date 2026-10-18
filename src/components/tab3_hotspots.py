"""
Component 3: Geospatial Hotspot Surveillance Map (Getis-Ord Gi*) and Cluster Migration.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from src.config import DIGITIZED_COUNT_DATES, HOTSPOT_PALETTE
from src.data_loader import load_hotspot_rankings, load_geojson_grid, load_hotspot_classifications


def render_tab3():
    """Render Tab 3: Geospatial Hotspot Surveillance Map."""
    st.markdown("### 🗺️ Block-Level Hotspot Surveillance & Spatial Clustering")
    st.markdown(
        """
        Identify statistically significant spatial clustering using Queen-contiguity **Getis-Ord $G_i^*$** 
        hotspot analysis across 12 digitized field count dates. Inspect local cluster migration 
        and distance to essential transit and outreach service hubs.
        """
    )

    h_col1, h_col2, h_col3 = st.columns([1.5, 1.2, 1.3])

    with h_col1:
        selected_date = st.selectbox(
            "Select Digitized Count Date:",
            options=DIGITIZED_COUNT_DATES,
            index=len(DIGITIZED_COUNT_DATES) - 1,
            help="Select one of the 12 digitized source map count dates (2018–2025).",
        )

    with h_col2:
        footprint_mode = st.radio(
            "Spatial Panel Scope:",
            options=["Balanced Panel (261 Blocks)", "Full Footprint (382 Blocks)"],
            index=0,
            help="Balanced panel ensures strict longitudinal validity. 382-block footprint includes Outside Perimeter (available 2022+).",
        )

    with h_col3:
        sig_filter = st.multiselect(
            "Filter Significance:",
            options=list(HOTSPOT_PALETTE.keys()),
            default=["99% Hotspot", "95% Hotspot"],
            help="Strict statistical significance tiers: 95% and 99% (Task 5.2). 90% tier available for exploratory review.",
        )

    # Date anomaly notice for March 2022
    if selected_date == "2022-03-01":
        st.markdown(
            """
            <div class="banner-warning">
                <strong>⚠️ Source Data Audit Note (March 2022):</strong> 
                Task 3.1 & 3.4 audits identified inconsistent handwritten dates in DSDP field scans for this month. 
                Spatial results are retained for documentation completeness but should be interpreted with caution.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Load Base Block Polygons & Date-Specific Hotspot Classifications
    grid_gdf = load_geojson_grid()
    hc_gdf = load_hotspot_classifications()

    # Map Creation (Centered on Downtown San Diego: 32.7125, -117.1520)
    m = folium.Map(
        location=[32.7125, -117.1520],
        zoom_start=15,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # Add Persistent Hotspot Key Markers
    top_persistent = load_hotspot_rankings()
    
    # Merge exact centroid coordinates from grid_gdf if present
    if grid_gdf is not None:
        plot_rankings = top_persistent.merge(grid_gdf[["block_id", "lat", "lon"]], on="block_id", how="left")
    else:
        plot_rankings = top_persistent.copy()

    for _, row in plot_rankings.head(5).iterrows():
        lat = row["lat"] if "lat" in row and pd.notnull(row["lat"]) else 32.7082 + (row["rank"] * 0.001)
        lon = row["lon"] if "lon" in row and pd.notnull(row["lon"]) else -117.1485 - (row["rank"] * 0.0005)
        
        popup_html = f"""
        <div style="font-family: sans-serif; font-size: 12px; width: 220px;">
            <b style="color: #B91C1C;">Rank #{row['rank']}: {row['block_id']}</b><br>
            <hr style="margin: 4px 0;">
            <b>Neighborhood:</b> {row['neighborhood']}<br>
            <b>Hotspot Frequency:</b> {row['hotspot_dates']}/12 dates ({row['hotspot_rate']*100:.0f}%)<br>
            <b>Nearest Service:</b> {row['nearest_service_m']} m<br>
            <b>Nearest Transit:</b> {row['nearest_transit_m']} m
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=10 - row["rank"],
            color="#991B1B",
            weight=2,
            fill=True,
            fill_color="#EF4444",
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Persistent Rank #{row['rank']}: {row['block_id']} ({row['hotspot_dates']}/12 dates)",
        ).add_to(m)

    # Add GeoJSON boundary polygons dynamically styled by selected_date, footprint_mode, and sig_filter
    if grid_gdf is not None:
        display_gdf = grid_gdf.copy()
        tier_map = {
            "hotspot_99": "99% Hotspot",
            "hotspot_95": "95% Hotspot",
            "hotspot_90": "90% Hotspot",
            "not_significant": "Not Significant",
            "coldspot_90": "90% Coldspot",
            "coldspot_95": "95% Coldspot",
            "coldspot_99": "99% Coldspot",
        }
        if hc_gdf is not None and not hc_gdf.empty:
            balanced_ids = set(hc_gdf["block_id"].unique())
            date_sub = hc_gdf[hc_gdf["date_str"] == selected_date][
                ["block_id", "adjusted_count", "gi_star_z", "p_sim", "classification"]
            ].copy()
            display_gdf = display_gdf.merge(date_sub, on="block_id", how="left")
            if footprint_mode == "Balanced Panel (261 Blocks)":
                display_gdf = display_gdf[display_gdf["block_id"].isin(balanced_ids)].copy()
        else:
            display_gdf["adjusted_count"] = 0.0
            display_gdf["gi_star_z"] = 0.0
            display_gdf["classification"] = "not_significant"

        display_gdf["tier_label"] = display_gdf["classification"].map(tier_map).fillna("Not Significant")
        display_gdf["count_str"] = display_gdf["adjusted_count"].fillna(0.0).map(lambda v: f"{v:.1f}")
        display_gdf["z_str"] = display_gdf["gi_star_z"].fillna(0.0).map(lambda v: f"{v:+.2f}")

        def style_fn(feature):
            props = feature.get("properties", {})
            tier = props.get("tier_label", "Not Significant")
            if tier in sig_filter and tier == "99% Hotspot":
                return {
                    "fillColor": "#B91C1C",
                    "color": "#7F1D1D",
                    "weight": 2.6,
                    "fillOpacity": 0.52,
                }
            if tier in sig_filter and tier == "95% Hotspot":
                return {
                    "fillColor": "#EF4444",
                    "color": "#991B1B",
                    "weight": 2.2,
                    "fillOpacity": 0.38,
                }
            if tier in sig_filter and tier != "Not Significant":
                return {
                    "fillColor": HOTSPOT_PALETTE.get(tier, "#3B82F6"),
                    "color": "#1E40AF",
                    "weight": 1.8,
                    "fillOpacity": 0.30,
                }
            return {
                "fillColor": "#3B82F6",
                "color": "#64748B",
                "weight": 0.9,
                "fillOpacity": 0.14 if "Not Significant" in sig_filter else 0.05,
            }

        folium.GeoJson(
            display_gdf[["block_id", "neighborhood", "count_str", "z_str", "tier_label", "geometry"]].to_json(),
            name="Downtown Block Grid",
            style_function=style_fn,
            tooltip=folium.GeoJsonTooltip(
                fields=["block_id", "neighborhood", "count_str", "z_str", "tier_label"],
                aliases=["Block ID:", "Area:", f"Adjusted Count ({selected_date}):", "Getis-Ord Gi* Z:", "Status:"],
            ),
        ).add_to(m)

    # Render Folium Map in Streamlit
    st_folium(m, use_container_width=True, height=520, returned_objects=[])

    # Supporting Analysis Modules
    sub_col1, sub_col2 = st.columns([1.4, 1])

    with sub_col1:
        st.markdown("#### 🏆 Top Persistent Hotspot Blocks (2018–2025)")
        st.markdown(
            "Blocks that remained statistically significant hotspots across the highest proportion of count dates:"
        )
        st.dataframe(
            top_persistent.head(10)[
                ["rank", "block_id", "neighborhood", "hotspot_dates", "hotspot_rate", "nearest_service_m", "nearest_transit_m"]
            ].rename(
                columns={
                    "rank": "Rank",
                    "block_id": "Block ID",
                    "neighborhood": "Area",
                    "hotspot_dates": "Hotspot Dates",
                    "hotspot_rate": "Persistence Rate",
                    "nearest_service_m": "Nearest Service (m)",
                    "nearest_transit_m": "Nearest Transit (m)",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    with sub_col2:
        st.markdown("#### 🧭 Cluster Centroid Migration")
        st.markdown(
            f"""
            <div class="dashboard-card" style="border-left: 4px solid #0D9488;">
                <div class="kpi-title">Southward Displacement</div>
                <div class="kpi-value" style="font-size: 1.6rem; color: #0D9488;">120.4 Meters SSE (160.1°)</div>
                <p style="font-size: 0.88rem; color: #475569; margin-top: 0.5rem; line-height: 1.4;">
                    Between the <strong>Early Period (2018–2020)</strong> and the <strong>Recent Period (2022–2025)</strong>, 
                    the adjusted-count-weighted hotspot centroid shifted <strong>120.4 meters SSE (160.1° bearing)</strong> toward the Commercial St / Imperial Ave corridor in South East Village.
                </p>
                <div style="font-size: 0.82rem; color: #64748B;">
                    <strong>Driver:</strong> Concentrated spatial displacement along commercial and transit corridors (12th & Imperial Trolley) following municipal sidewalk camping enforcement.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
