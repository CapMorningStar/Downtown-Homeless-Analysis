"""
Main Streamlit Application Entry Point and Interactive Router.
Downtown San Diego Homeless Population Analysis - Task 9.1
Author: Kyaw Soe Lwin (Data Science Alliance / UC San Diego)
"""

from pathlib import Path
import streamlit as st
from src.config import APP_TITLE, ORGANIZATION, AUTHORS
from src.data_loader import load_historical_data
from src.components.header import render_header
from src.components.tab1_historical import render_tab1
from src.components.tab2_forecast import render_tab2
from src.components.tab3_hotspots import render_tab3
from src.components.tab4_decomposition import render_tab4
from src.components.tab5_calculator import render_tab5
from src.components.tab6_about import render_tab6

# Set Page Config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject Custom CSS Stylesheet
css_path = Path(__file__).resolve().parent / "src" / "styles" / "custom.css"
if css_path.exists():
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    """Main application lifecycle and tab routing."""
    # Ingest Cached Baseline Data
    historical_df = load_historical_data()

    # Executive Header & KPI Ribbon
    render_header(historical_df)

    # 6 Core Functional Tabs (Task 9.1 Specifications)
    tabs = st.tabs(
        [
            "📈 1. Historical Trends",
            "🔮 2. 12-Month Forecast",
            "🗺️ 3. Hotspot Surveillance",
            "🔬 4. Neighborhood Deep-Dive",
            "🧮 5. County Estimation",
            "📖 6. Methodology & About",
        ]
    )

    with tabs[0]:
        render_tab1(historical_df)

    with tabs[1]:
        render_tab2()

    with tabs[2]:
        render_tab3()

    with tabs[3]:
        render_tab4(historical_df)

    with tabs[4]:
        render_tab5()

    with tabs[5]:
        render_tab6()

    # Footer
    st.markdown("---")
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        st.markdown(
            f"""
            <div style="font-size: 0.85rem; color: #64748B;">
                <strong>Downtown San Diego Homeless Population Analysis</strong> | Task 9.1 Interactive Dashboard<br>
                Published by <strong>{ORGANIZATION}</strong> in partnership with community researchers.<br>
                Data Sources: Downtown San Diego Partnership (DSDP) & Regional Task Force on Homelessness (RTFH).
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f_col2:
        st.markdown(
            """
            <div style="text-align: right; font-size: 0.82rem; color: #94A3B8;">
                Engine: Streamlit & Plotly & Folium | Python 3.11/3.13<br>
                Status: Production Ready | Seed 42 Deterministic
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
