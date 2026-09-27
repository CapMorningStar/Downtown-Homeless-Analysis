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

    tab_prov, tab_mult, tab_footprint, tab_caveats = st.tabs(
        [
            "1. Data Sources & Provenance",
            "2. The 4 Multiplier Regimes",
            "3. 2022 Footprint Expansion",
            "4. Policy Caveats & Data Quality",
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
            * **Expansion in January 2022:** DSDP added **121 additional blocks** covering adjacent peripheral areas:
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
               * While downtown counts dropped precipitously by **-43.5%**, regional RTFH counts proved that **countywide unsheltered homelessness reached an all-time record of 6,110 in 2024**.
               * **Analytical Rule:** A downtown reduction does not equal regional resolution; it reflects localized spatial displacement into canyons, riverbeds, and adjacent cities (El Cajon, Escondido, Chula Vista).

            2. **Resolution of 134 Null Values (Task 1.1 Data Quality Audit):**
               * **116 nulls in 2025:** Genuine reporting lag (unreleased monthly count packets for July, August, October, and November 2025).
               * **18 nulls in November 2018:** The published DSDP PDF included the headline total count table but omitted the detailed component breakout table.
               * All nulls have been mathematically cataloged and accounted for without distorting time-series models.
            """
        )
