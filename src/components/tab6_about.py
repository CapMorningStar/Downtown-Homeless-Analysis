"""
Component 6: Methodology, Data Governance, Provenance, and Footprint Expansion Documentation.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import streamlit as st


def render_tab6():
    """Render Tab 6: Methodology & About Page."""
    st.markdown("### 📖 Methodology, Data Governance & Architectural Footprint")
    st.markdown(
        """
        Comprehensive documentation of data sources, multiplier regimes, econometric adjustment 
        methodologies, spatial boundary expansions, and analytical caveats governing this study.
        """
    )

    tab_prov, tab_mult, tab_footprint, tab_caveats, tab_roadmap = st.tabs(
        [
            "1. Data Sources & Provenance",
            "2. The 4 Multiplier Regimes",
            "3. 2022 Footprint Expansion",
            "4. Policy Caveats & Data Quality",
            "5. Strategic Roadmap (R1–R8)",
        ]
    )

    with tab_prov:
        st.markdown("#### Primary Data Sources & Provenance")
        st.markdown(
            """
            This longitudinal study synthesizes two distinct public interest homelessness data sources:

            1. **Downtown San Diego Partnership (DSDP) Clean & Safe Program:**
               * **Frequency:** Monthly field counts (conducted in the pre-dawn hours, typically between 3:00 AM and 6:00 AM on the last Wednesday or Thursday of each month).
               * **Coverage:** Downtown San Diego core corridors (East Village, City Center, Columbia, Cortez, Gaslamp, Marina, and Outside Perimeter).
               * **Scope:** Captures visible unsheltered individuals, tents/structures, and occupied vehicles.
               * **Timeline:** Empirical monthly counts span **January 2017 to the present** (`2017-01-01` to `2025-12-01`).
               * *(Correction: Early project documentation informally referenced 2012; Task 1.1 empirical audits confirmed that digitized, verifiable monthly count data begins in January 2017).*

            2. **Regional Task Force on Homelessness (RTFH) Continuum of Care (CA-601):**
               * **Frequency:** Annual federally mandated Point-in-Time (PIT) Census ("WeAllCount") conducted on a single night in late January.
               * **Coverage:** Entire County of San Diego, encompassing all 18 incorporated municipalities and unincorporated county territory.
               * **Scope:** Captures both sheltered individuals (in emergency shelters and transitional housing) and unsheltered street populations.
            """
        )

    with tab_mult:
        st.markdown("#### The 4 Historical Multiplier Regimes & 2020 Divergence")
        st.markdown(
            """
            DSDP applies mathematical multipliers to estimate the number of people occupying observed tents and vehicles. 
            Over the 9-year study window, four distinct multiplier regimes governed the published numbers:
            """
        )

        regime_table = [
            {"Regime": "1. PRE2017 (Prior to Apr 2017)", "Individual": "1.0x", "Tent / Structure": "2.00x", "Vehicle": "2.00x", "Context": "Early operational formula; simple doubling heuristic."},
            {"Regime": "2. APR2017 (Apr 2017 – Apr 2018)", "Individual": "1.0x", "Tent / Structure": "1.75x", "Vehicle": "1.66x", "Context": "Adopted based on RTFH demographic survey samples."},
            {"Regime": "3. MAY2018 (May 2018 – Dec 2019)", "Individual": "1.0x", "Tent / Structure": "1.75x", "Vehicle": "2.03x", "Context": "Updated vehicle multiplier based on 2018 PIT count survey data."},
            {"Regime": "4. POST2020 (Jan 2020 – Present)", "Individual": "1.0x", "Tent / Structure": "1.75x (DSDP) / 1.0x (HUD)", "Vehicle": "2.03x (DSDP) / 1.0x (HUD)", "Context": "Critical divergence: RTFH eliminated multipliers to meet HUD national PIT guidelines; DSDP maintained multipliers for operational continuity."},
        ]
        st.table(regime_table)

        st.markdown(
            """
            <div class="banner-info">
                <strong>Constant-Methodology Harmonization (Assignment 6):</strong><br>
                Because multiplier changes create artificial baseline steps, Assignment 6 constructed the 
                <strong>Constant-Methodology Hybrid Series</strong> (<code>TimeSeries_ConstantMethodology.csv</code>). 
                This series rescales pre-2020 data onto the POST2020 standard using exact per-row component breakdowns for 2018+ 
                and theoretical weight conversions for 2017, providing an uninterrupted, apples-to-apples basis for econometric forecasting.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_footprint:
        st.markdown("#### The 2022 Footprint Expansion: From 261 to 382 Blocks")
        st.markdown(
            """
            A critical spatial discovery was made during **Assignment 3 (Block-Level Validation)**:

            * **Historical Footprint (2018–2021):** DSDP mapped and counted **261 downtown blocks** concentrated strictly within the core 6 neighborhoods.
            * **Expansion in 2022:** DSDP added **121 additional blocks** covering adjacent peripheral areas:
              * *Golden Hill*
              * *Barrio Logan*
              * *Sherman Heights*
              *(Grouped analytically as "Outside Perimeter").*
            * **Methodological Impact:** Task 3.3 proved that **4% to 33% of the post-2021 increase in total downtown counts was purely an artifact of expanded geographic surveillance**, not an increase in street homelessness within the original core.
            * **Longitudinal Modeling Rule:** All valid cross-time comparisons and hotspot migration analyses must use the **Balanced 261-Block Panel** (`BlockPanel_Balanced_261.csv`) to prevent artificial footprint bias.
            """
        )

    with tab_caveats:
        st.markdown("#### Policy Caveats & Data Quality Log")
        st.markdown(
            """
            1. **July 2023 City of San Diego Unsafe Camping Ordinance:**
               * The ordinance banned tent encampments on public sidewalks when shelter beds are available, and banned tents at all times within two blocks of schools, shelters, and transit hubs.
               * While downtown counts dropped by **-36.7%** through December 2025 (a cumulative **-53.2%** drop from the May 2023 crisis apex), regional RTFH counts proved that **countywide unsheltered homelessness reached an all-time record of 6,110 in 2024**.
               * **Analytical Rule:** A downtown reduction does not equal regional resolution; it reflects localized spatial displacement into adjacent municipalities, riverbeds, and unincorporated areas.
               * *(🚨 Methodological Safeguard: Macro divergence is empirically proven; individual migration destinations require longitudinal HMIS tracking to confirm).*

            2. **Resolution of 134 Null Values (Task 1.1 Data Quality Audit):**
               * **116 nulls in 2025:** Genuine reporting lag (unreleased monthly count packets for July, August, October, and November 2025).
               * **18 nulls in November 2018:** The published DSDP PDF included the headline total count table but omitted the detailed component breakout table.
               * All nulls have been mathematically cataloged and accounted for without distorting time-series models.
            """
        )

    with tab_roadmap:
        st.markdown("#### 🎯 Municipal Policy Action Roadmap (Recommendations R1–R8)")
        st.markdown(
            """
            Derived from Task 9.3 Strategic Synthesis and presented on Slide 11, these eight actionable 
            recommendations bridge spatial-temporal modeling into evidence-based municipal governance:
            """
        )

        r_col1, r_col2, r_col3 = st.columns(3)

        with r_col1:
            st.markdown(
                """
                <div class="dashboard-card" style="border-top: 4px solid #EF4444; height: 100%;">
                    <div style="font-weight: 700; color: #B91C1C; font-size: 0.95rem;">⚡ Immediate Horizon (0–3 Months)</div>
                    <ul style="font-size: 0.84rem; color: #334155; padding-left: 1.1rem; margin-top: 0.5rem; line-height: 1.45;">
                        <li><strong>R1 (Hotspot Surge Capacity):</strong> Deploy mobile hygiene, medical vans, and peer navigators directly to the 5 persistent hotspot blocks (capturing 10.0% of downtown within 0.1 sq mi).</li>
                        <li><strong>R2 (The 4 Public Rules):</strong> Cease single-number press releases. Report rounded point estimates (5,900) + calibrated 95% intervals ([3,900 to 8,000]) with policy disclosures.</li>
                        <li><strong>R3 (Footprint Wedge Disclosure):</strong> Concurrently release both 261-block core and 382-block expanded totals to prevent misleading spatial artifacts.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r_col2:
            st.markdown(
                """
                <div class="dashboard-card" style="border-top: 4px solid #D97706; height: 100%;">
                    <div style="font-weight: 700; color: #B45309; font-size: 0.95rem;">🌱 Medium-Term Horizon (6–12 Months)</div>
                    <ul style="font-size: 0.84rem; color: #334155; padding-left: 1.1rem; margin-top: 0.5rem; line-height: 1.45;">
                        <li><strong>R4 (Component Sub-Totals):</strong> Mandate separate reporting of individuals, tents, and vehicles to isolate vehicular living and multiplier volatility.</li>
                        <li><strong>R5 (Cross-Border Tracking):</strong> Coordinate regional perimeter monitoring across Barrio Logan and transit hubs to track displacement vectors.</li>
                        <li><strong>R6 (Annual OLS Calibration):</strong> Re-estimate the countywide regression model each May following RTFH PIT Census releases.</li>
                        <li><strong>R7 (Live Bed Occupancy):</strong> Integrate DSDP outreach teams with real-time Housing Inventory Count (HIC) shelter bed vacancy feeds.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r_col3:
            st.markdown(
                """
                <div class="dashboard-card" style="border-top: 4px solid #10B981; height: 100%;">
                    <div style="font-weight: 700; color: #047857; font-size: 0.95rem;">🏛️ Long-Term Horizon (1–3 Years)</div>
                    <ul style="font-size: 0.84rem; color: #334155; padding-left: 1.1rem; margin-top: 0.5rem; line-height: 1.45;">
                        <li><strong>R8 (Unified Regional HMIS & Digitization):</strong> Complete digitization of historical field maps and unify monthly geospatial block observations with countywide Homeless Management Information System (HMIS) tracking.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
