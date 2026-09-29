"""
Native PowerPoint Presentation Generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.pptx
Adheres strictly to the Canva 'Blue and White Modern Data Analytics' Design System (16:9 widescreen).
Features 14 production-grade executive slides with KPI cards, tables, high-DPI graphics,
and strict compliance with The 4 Public Communication Rules.
"""

import os
from pathlib import Path
from PIL import Image
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = Path(__file__).resolve().parent
SLIDE_ASSETS = BASE_DIR / "slide_assets"
OUTPUT_PPTX = BASE_DIR / "Assignment9_StrategicSynthesis.pptx"

# -------------------------------------------------------------
# Canva Template Design System: "Blue and White Modern Data Analytics"
# -------------------------------------------------------------
COLOR_PRIMARY_NAVY = RGBColor(41, 62, 156)    # #293E9C (Deep Royal Navy)
COLOR_ROYAL_BLUE   = RGBColor(58, 88, 228)    # #3A58E4 (Vibrant Royal Blue)
COLOR_MID_BLUE     = RGBColor(105, 132, 254)  # #6984FE (Mid Periwinkle Blue)
COLOR_SOFT_BLUE    = RGBColor(154, 173, 255)  # #9AADFF (Soft Cornflower Blue)
COLOR_ICE_TINT     = RGBColor(211, 223, 255)  # #D3DFFF (Ice Tint Accent)
COLOR_CANVAS_BG    = RGBColor(245, 247, 251)  # #F5F7FB (Tech Off-White Canvas)
COLOR_CARD_BG      = RGBColor(255, 255, 255)  # #FFFFFF (Pure White)
COLOR_CARD_BORDER  = RGBColor(220, 228, 245)  # #DCE4F5 (Subtle Border)
COLOR_TEXT_DARK    = RGBColor(29, 31, 38)     # #1D1F26 (Charcoal Slate)
COLOR_TEXT_MUTED   = RGBColor(100, 116, 145)  # #647491 (Muted Slate)
COLOR_RED          = RGBColor(220, 38, 38)    # #DC2626 (Alert Red)
COLOR_GREEN        = RGBColor(5, 150, 105)    # #059669 (Action Green)
COLOR_AMBER        = RGBColor(217, 119, 6)    # #D97706 (Warning Amber)
COLOR_TEAL         = RGBColor(13, 148, 136)   # #0D9488 (Teal Champion)

FONT_DISPLAY = "Trebuchet MS"  # Primary title font
FONT_BODY    = "Segoe UI"      # Body and metadata font


def set_slide_background(slide):
    """Fill slide with canvas off-white background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_CANVAS_BG
    bg.line.fill.background()
    return bg


def add_canva_header(slide, title_text, category_text, slide_num_str):
    """Add standard Canva top header with category chip, title, and page badge."""
    # 1. Top-Right Slide Number Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.133), Inches(0), Inches(1.2), Inches(0.82))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_PRIMARY_NAVY
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = slide_num_str
    p_b.font.name = FONT_DISPLAY
    p_b.font.size = Pt(24)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_CARD_BG
    p_b.alignment = PP_ALIGN.CENTER

    # 2. Vertical Accent Line
    line_v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.06), Inches(0.82))
    line_v.fill.solid()
    line_v.fill.fore_color.rgb = COLOR_ROYAL_BLUE
    line_v.line.fill.background()

    # 3. Header Title & Subtitle Box
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.38), Inches(10.8), Inches(0.92))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_sub = tf.paragraphs[0]
    p_sub.text = category_text.upper()
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_ROYAL_BLUE
    p_sub.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_DISPLAY
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_NAVY

    # Subtle horizontal line below header
    line_h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.012))
    line_h.fill.solid()
    line_h.fill.fore_color.rgb = COLOR_CARD_BORDER
    line_h.line.fill.background()


def add_canva_footer(slide, current_page, total_pages=14):
    """Add standard bottom footer bar."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(9.5), Inches(0.35))
    tf_l = tb_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "Data Science Alliance • Downtown San Diego Homeless Population Analysis • Sources: DSDP Field Counts & RTFH PIT"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9)
    p_l.font.color.rgb = COLOR_TEXT_MUTED

    tb_right = slide.shapes.add_textbox(Inches(10.5), Inches(6.98), Inches(2.033), Inches(0.35))
    tf_r = tb_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.text = f"Slide {current_page} of {total_pages}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_PRIMARY_NAVY


def add_canva_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Add styled rounded rectangle card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card


def add_image_fitted(slide, image_path, container_left, container_top, container_width, container_height):
    """Add an image fitted within container while preserving exact aspect ratio."""
    if not os.path.exists(image_path):
        tb = slide.shapes.add_textbox(container_left, container_top, container_width, container_height)
        tb.text_frame.text = f"Missing Image:\n{os.path.basename(image_path)}"
        return tb

    with Image.open(image_path) as img:
        img_w, img_h = img.size
    aspect = img_w / img_h
    cont_aspect = container_width / container_height
    if aspect > cont_aspect:
        target_w = container_width
        target_h = container_width / aspect
        offset_x = 0
        offset_y = (container_height - target_h) / 2
    else:
        target_h = container_height
        target_w = container_height * aspect
        offset_y = 0
        offset_x = (container_width - target_w) / 2
    return slide.shapes.add_picture(str(image_path), container_left + offset_x, container_top + offset_y, target_w, target_h)


def add_kpi_card(slide, left, top, width, height, value_str, label_str, subtext_str, accent_color=COLOR_PRIMARY_NAVY):
    """Add high-impact executive KPI badge card."""
    card = add_canva_card(slide, left, top, width, height, COLOR_CARD_BG, COLOR_CARD_BORDER)

    # Accent color bar on top
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.25))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_v = tf.paragraphs[0]
    p_v.text = value_str
    p_v.font.name = FONT_DISPLAY
    p_v.font.size = Pt(28)
    p_v.font.bold = True
    p_v.font.color.rgb = accent_color
    p_v.space_after = Pt(2)

    p_l = tf.add_paragraph()
    p_l.text = label_str.upper()
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9.5)
    p_l.font.bold = True
    p_l.font.color.rgb = COLOR_TEXT_DARK
    p_l.space_after = Pt(3)

    p_s = tf.add_paragraph()
    p_s.text = subtext_str
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(8.5)
    p_s.font.color.rgb = COLOR_TEXT_MUTED


def add_formatted_table(slide, left, top, width, height, headers, rows_data, col_widths=None):
    """Render a clean presentation table with header styling."""
    num_rows = len(rows_data) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    tbl = table_shape.table

    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            tbl.columns[idx].width = w

    # Style Headers
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_NAVY
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.06)
        p = tf.paragraphs[0]
        p.text = h
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_BG
        p.alignment = PP_ALIGN.CENTER

    # Style Data Rows
    for r_idx, row in enumerate(rows_data):
        bg = COLOR_CARD_BG if r_idx % 2 == 0 else COLOR_CANVAS_BG
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.06)
            p = tf.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_TEXT_DARK
            if c_idx == 0:
                p.font.bold = True
                p.alignment = PP_ALIGN.LEFT
            else:
                p.alignment = PP_ALIGN.CENTER

    return table_shape


def build_deck():
    print(f"Building Task 9.3 Presentation: {OUTPUT_PPTX}...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =============================================================
    # SLIDE 1: TITLE SLIDE (Canva Style)
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_canva_card(s1, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7), COLOR_CARD_BG, COLOR_CARD_BORDER)

    # Top Category Chip
    add_canva_card(s1, Inches(1.6), Inches(1.5), Inches(4.8), Inches(0.42), COLOR_ICE_TINT, COLOR_SOFT_BLUE)
    tb_c = s1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(4.8), Inches(0.42))
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS BRIEFING"
    p_c.font.name = FONT_BODY
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_PRIMARY_NAVY

    # Title & Subtitle
    tb_t = s1.shapes.add_textbox(Inches(1.6), Inches(2.15), Inches(10.0), Inches(2.2))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "Downtown San Diego Unsheltered Homelessness:\nStrategic Synthesis & Policy Roadmap (2017–2026)"
    p_t1.font.name = FONT_DISPLAY; p_t1.font.size = Pt(32); p_t1.font.bold = True; p_t1.font.color.rgb = COLOR_PRIMARY_NAVY; p_t1.space_after = Pt(12)

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Longitudinal Econometrics, Spatial Panel Dynamics, Machine Learning Forecasting & Regional Policy Impacts"
    p_t2.font.name = FONT_BODY; p_t2.font.size = Pt(15); p_t2.font.bold = True; p_t2.font.color.rgb = COLOR_ROYAL_BLUE

    # Divider Rule
    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(4.6), Inches(10.0), Inches(0.015))
    div1.fill.solid(); div1.fill.fore_color.rgb = COLOR_CARD_BORDER; div1.line.fill.background()

    # 3 Metadata blocks
    meta_items = [
        ("Partnership & Author", "Data Science Alliance (DSA) in partnership with DSDP and RTFH\nLead Analyst: Kyaw Soe Lwin | Project Lead: Adir Mancebo Jr."),
        ("Data Foundation", "9 Years of Monthly Field Counts (2017–2025) across 382 Blocks\nPoint-in-Time (PIT) Regional Censuses (2017–2025)"),
        ("Analytical Framework", "Spatial Getis-Ord Gi* • 5-Fold Walk-Forward XGBoost ML • Policy Regime OLS • 4 Public Communication Rules")
    ]
    for idx, (m_label, m_val) in enumerate(meta_items):
        m_left = Inches(1.6 + idx * 3.4)
        tb_m = s1.shapes.add_textbox(m_left, Inches(4.8), Inches(3.1), Inches(1.4))
        tf_m = tb_m.text_frame; tf_m.word_wrap = True
        p_ml = tf_m.paragraphs[0]; p_ml.text = m_label.upper(); p_ml.font.name = FONT_BODY; p_ml.font.size = Pt(9.5); p_ml.font.bold = True; p_ml.font.color.rgb = COLOR_ROYAL_BLUE; p_ml.space_after = Pt(2)
        p_mv = tf_m.add_paragraph(); p_mv.text = m_val; p_mv.font.name = FONT_BODY; p_mv.font.size = Pt(9.0); p_mv.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 2: EXECUTIVE KPI DASHBOARD (4 CORE METRICS)
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout); set_slide_background(s2)
    add_canva_header(s2, "Executive KPI Dashboard: Crisis Peak, Enforcement Contraction & Hotspot Migration", "Executive Framing & Core Findings", "02")
    add_canva_footer(s2, 2)

    # 4 KPI Cards
    kpis = [
        ("2,103", "Crisis Peak (May 2023)", "Highest headline count in downtown history; culmination of 3-year surge.", COLOR_RED),
        ("851", "Recent Count (Dec 2025)", "-59.5% reduction from peak post-camping ordinance enforcement.", COLOR_GREEN),
        ("54.8%", "East Village Concentration", "Epicenter of downtown homelessness (historical monthly average 552.8).", COLOR_PRIMARY_NAVY),
        ("121m", "Southward Centroid Shift", "Hotspot migration vector toward Commercial St / Imperial Ave transit hub.", COLOR_ROYAL_BLUE),
    ]
    for idx, (val, lbl, sub, col) in enumerate(kpis):
        k_left = Inches(0.8 + idx * 2.98)
        add_kpi_card(s2, k_left, Inches(1.6), Inches(2.78), Inches(2.1), val, lbl, sub, col)

    # Lower Synthesis Card
    add_canva_card(s2, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.6), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_s2 = s2.shapes.add_textbox(Inches(1.1), Inches(4.2), Inches(11.1), Inches(2.2))
    tf_s2 = tb_s2.text_frame; tf_s2.word_wrap = True
    p1 = tf_s2.paragraphs[0]
    p1.text = "THE STRATEGIC REALITY: DOWNTOWN CONTRACTION VS. REGIONAL DISPLACEMENT"
    p1.font.name = FONT_DISPLAY; p1.font.size = Pt(13); p1.font.bold = True; p1.font.color.rgb = COLOR_PRIMARY_NAVY; p1.space_after = Pt(6)

    bullets = [
        ("Three Trajectory Epochs: ", "Downtown transitioned through Baseline Contraction (2017–2020), Crisis Surge (2021–2023), and Enforcement Pullback (2024–2025). Current counts have stabilized near ~850–920."),
        ("Debunking Seasonality: ", "Non-parametric tests prove 8 of 9 downtown series have NO statistically significant seasonality (H=3.00, p=0.99). Resource budgeting based on 'winter surges' or 'summer peaks' is empirically flawed."),
        ("The Boundary Wedge: ", "In 2022, DSDP added 121 peripheral blocks, accounting for 4% to 33% of reported count increases. Longitudinal comparisons require balanced 261-block spatial controls."),
        ("Regional Spillover Paradox: ", "Downtown's share of county unsheltered population collapsed from 37.5% (2023) to 14.9% (2025), yet countywide unsheltered numbers reached an all-time record of 6,110 in 2024. Unsheltered homelessness was pushed into riverbeds and neighboring cities, not resolved.")
    ]
    for b_title, b_text in bullets:
        p = tf_s2.add_paragraph()
        p.space_after = Pt(4)
        run_t = p.add_run(); run_t.text = "• " + b_title; run_t.font.name = FONT_BODY; run_t.font.size = Pt(10); run_t.font.bold = True; run_t.font.color.rgb = COLOR_ROYAL_BLUE
        run_d = p.add_run(); run_d.text = b_text; run_d.font.name = FONT_BODY; run_d.font.size = Pt(9.5); run_d.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 3: THE 9-YEAR TRAJECTORY & THREE MACRO EPOCHS
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout); set_slide_background(s3)
    add_canva_header(s3, "The 9-Year Trajectory: Three Distinct Macro Policy Epochs (2017–2025)", "Longitudinal Dynamics", "03")
    add_canva_footer(s3, 3)

    # Left Image Container
    add_canva_card(s3, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s3, SLIDE_ASSETS / "chart1_clean_hd.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    # Right Column: 3 Epoch Cards
    epochs = [
        ("Epoch 1: Baseline Contraction (2017–2020)", "Low of 689 in April 2020 (-19.7% YoY)", "Characterized by shelter expansions and COVID-19 emergency response (Convention Center de-densification Operation Shelter to Home).", COLOR_ROYAL_BLUE),
        ("Epoch 2: The Crisis Surge (2021–2023)", "May 2023 Peak of 2,103 (+144% from 2020 low)", "Convention Center shelter closure, eviction moratoria lapses, inflation, and fentanyl expansion drove unprecedented street encampments.", COLOR_RED),
        ("Epoch 3: Enforcement Pullback (2024–2025)", "Collapse to 851 (-59.5% from peak)", "City of San Diego Unsafe Camping Ordinance (July 2023) and Safe Sleeping Sites (O Lot, 20th & B) cleared key commercial corridors.", COLOR_GREEN),
    ]
    for idx, (title, stat, desc, col) in enumerate(epochs):
        top_y = Inches(1.6 + idx * 1.7)
        add_canva_card(s3, Inches(8.2), top_y, Inches(4.333), Inches(1.55), COLOR_CARD_BG, COLOR_CARD_BORDER)
        tb_e = s3.shapes.add_textbox(Inches(8.4), top_y + Inches(0.12), Inches(3.933), Inches(1.3))
        tf_e = tb_e.text_frame; tf_e.word_wrap = True
        pe1 = tf_e.paragraphs[0]; pe1.text = title; pe1.font.name = FONT_DISPLAY; pe1.font.size = Pt(11); pe1.font.bold = True; pe1.font.color.rgb = col; pe1.space_after = Pt(2)
        pe2 = tf_e.add_paragraph(); pe2.text = stat; pe2.font.name = FONT_BODY; pe2.font.size = Pt(9.5); pe2.font.bold = True; pe2.font.color.rgb = COLOR_TEXT_DARK; pe2.space_after = Pt(2)
        pe3 = tf_e.add_paragraph(); pe3.text = desc; pe3.font.name = FONT_BODY; pe3.font.size = Pt(8.5); pe3.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # SLIDE 4: DEBUNKING THE SEASONALITY MYTH
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout); set_slide_background(s4)
    add_canva_header(s4, "Debunking the Seasonality Myth: Homelessness Is Not Driven by Weather", "Econometric Seasonality Proof", "04")
    add_canva_footer(s4, 4)

    # Left Container: Kruskal-Wallis Table
    add_canva_card(s4, Inches(0.8), Inches(1.6), Inches(6.5), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_t4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.1), Inches(0.6))
    p_t4 = tb_t4.text_frame.paragraphs[0]
    p_t4.text = "Kruskal-Wallis Non-Parametric Seasonality Tests (12 Months, df=11)"
    p_t4.font.name = FONT_DISPLAY; p_t4.font.size = Pt(11.5); p_t4.font.bold = True; p_t4.font.color.rgb = COLOR_PRIMARY_NAVY

    kw_headers = ["Geographic Series", "H-Stat", "p-value", "Seasonality Verdict"]
    kw_data = [
        ["Overall - Reported Footprint", "3.00", "0.990", "Zero Seasonality (p > 0.05)"],
        ["Overall - Fixed Core Six", "3.58", "0.980", "Zero Seasonality (p > 0.05)"],
        ["East Village (Epicenter)", "4.12", "0.966", "Zero Seasonality (p > 0.05)"],
        ["City Center (Core)", "5.21", "0.921", "Zero Seasonality (p > 0.05)"],
        ["Gaslamp Quarter", "3.84", "0.974", "Zero Seasonality (p > 0.05)"],
        ["Columbia", "4.60", "0.949", "Zero Seasonality (p > 0.05)"],
        ["Cortez Hill", "6.18", "0.861", "Zero Seasonality (p > 0.05)"],
        ["Marina", "19.82", "0.048", "Borderline (Hotel/Park Edge)"],
        ["Outside Perimeter", "5.88", "0.881", "Zero Seasonality (p > 0.05)"],
    ]
    add_formatted_table(s4, Inches(1.0), Inches(2.4), Inches(6.1), Inches(3.9), kw_headers, kw_data, [Inches(2.5), Inches(1.0), Inches(1.0), Inches(1.6)])

    # Right Container: Policy Implications
    add_canva_card(s4, Inches(7.6), Inches(1.6), Inches(4.933), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_p4 = s4.shapes.add_textbox(Inches(7.9), Inches(1.8), Inches(4.333), Inches(4.6))
    tf_p4 = tb_p4.text_frame; tf_p4.word_wrap = True
    pp1 = tf_p4.paragraphs[0]; pp1.text = "WHY THIS MATTERS FOR MUNICIPAL BUDGETING"; pp1.font.name = FONT_DISPLAY; pp1.font.size = Pt(12.5); pp1.font.bold = True; pp1.font.color.rgb = COLOR_PRIMARY_NAVY; pp1.space_after = Pt(8)

    points4 = [
        ("The 'Weather Surge' Fallacy: ", "Civic planning has historically assumed summer surges or winter lulls. STL decomposition and non-parametric testing prove weather accounts for less than 5% of monthly count variance."),
        ("Macro Drivers Dominate: ", "Month-to-month variance is governed almost exclusively by multi-year policy shifts, emergency shelter capacity expansions/closures, and macroeconomic housing stress."),
        ("Eliminate Fluctuating Allocations: ", "Seasonal emergency shelter beds (e.g. 'inclement weather only') fail to address the stable structural baseline. Funding should be locked into permanent year-round operating capacity."),
        ("Marina Exception Explained: ", "Only Marina showed borderline significance (p=0.048), driven by seasonal tourist events and park buffer sweeps around the Convention Center.")
    ]
    for pt, pd in points4:
        p = tf_p4.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + pt; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = pd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 5: THE 2022 BOUNDARY EXPANSION WEDGE
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout); set_slide_background(s5)
    add_canva_header(s5, "The Boundary Expansion Wedge: Disentangling Reality from Map Changes", "Spatial Panel Accounting", "05")
    add_canva_footer(s5, 5)

    # Left Container: Footprint Wedge Image
    add_canva_card(s5, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s5, SLIDE_ASSETS / "task93_footprint_wedge.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    # Right Container: Analytical Callout
    add_canva_card(s5, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_w5 = s5.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_w5 = tb_w5.text_frame; tf_w5.word_wrap = True
    pw1 = tf_w5.paragraphs[0]; pw1.text = "ACCOUNTING FOR THE 121-BLOCK EXPANSION"; pw1.font.name = FONT_DISPLAY; pw1.font.size = Pt(12.5); pw1.font.bold = True; pw1.font.color.rgb = COLOR_PRIMARY_NAVY; pw1.space_after = Pt(8)

    w_points = [
        ("The Administrative Shift: ", "In January 2022, DSDP expanded survey coverage from 261 blocks to 382 blocks by incorporating 121 peripheral blocks across Golden Hill (52), Barrio Logan (35), and Sherman Heights (34)."),
        ("Quantifying the Wedge: ", "Between 4.0% and 32.8% of reported post-2021 count increases were driven strictly by drawing a larger perimeter on the map. In January 2023, 641 of 1,955 reported individuals were in the expansion zone."),
        ("Underlying Crisis Remained Real: ", "The balanced 261-block panel shows counts still surged +71% in 2022. The crisis was real, but naive unadjusted comparisons exaggerated growth by nearly a third."),
        ("Data Engineering Fix: ", "Constructed BlockPanel_Balanced_261.csv to enforce strict longitudinal panel balance across all 12 digitized count dates (2018–2025).")
    ]
    for wt, wd in w_points:
        p = tf_w5.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + wt; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = wd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 6: GEOSPATIAL CONCENTRATION: THE EAST VILLAGE EPICENTER
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout); set_slide_background(s6)
    add_canva_header(s6, "Where Homelessness Concentrates: The East Village Epicenter", "Geographic Concentration", "06")
    add_canva_footer(s6, 6)

    # Left Container: Top Hotspot Blocks Table
    add_canva_card(s6, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_h6 = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.4), Inches(0.5))
    tb_h6.text_frame.paragraphs[0].text = "Top Persistent Hotspot Blocks in Downtown San Diego (Getis-Ord Gi*)"
    tb_h6.text_frame.paragraphs[0].font.name = FONT_DISPLAY
    tb_h6.text_frame.paragraphs[0].font.size = Pt(11.5)
    tb_h6.text_frame.paragraphs[0].font.bold = True
    tb_h6.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY_NAVY

    hotspot_headers = ["Rank", "Block Identifier", "Area", "Hotspot Dates", "Rate", "Transit Dist"]
    hotspot_rows = [
        ["#1", "16th St & Imperial Ave", "South East Village", "9 / 12 dates", "75%", "52 m"],
        ["#2", "I-5 SB & Imperial Ave", "South East Village", "8 / 12 dates", "67%", "137 m"],
        ["#3", "I-5 SB Off-Ramp Border", "South East Village", "6 / 12 dates", "50%", "204 m"],
        ["#4", "I-5 SB On-Ramp Border", "South East Village", "4 / 12 dates", "33%", "154 m"],
        ["#5", "17th St & Imperial Ave", "South East Village", "4 / 12 dates", "33%", "72 m"],
        ["#6", "16th St & J St", "South East Village", "2 / 12 dates", "17%", "283 m"],
        ["#7", "17th St & J St", "South East Village", "2 / 12 dates", "17%", "274 m"],
    ]
    add_formatted_table(s6, Inches(1.0), Inches(2.35), Inches(6.4), Inches(3.9), hotspot_headers, hotspot_rows, [Inches(0.6), Inches(2.2), Inches(1.5), Inches(1.0), Inches(0.5), Inches(0.6)])

    # Right Container: Spatial Context
    add_canva_card(s6, Inches(7.9), Inches(1.6), Inches(4.633), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_sc = s6.shapes.add_textbox(Inches(8.2), Inches(1.8), Inches(4.033), Inches(4.6))
    tf_sc = tb_sc.text_frame; tf_sc.word_wrap = True
    psc1 = tf_sc.paragraphs[0]; psc1.text = "THE BUILT-ENVIRONMENT MAGNET"; psc1.font.name = FONT_DISPLAY; psc1.font.size = Pt(12.5); psc1.font.bold = True; psc1.font.color.rgb = COLOR_PRIMARY_NAVY; psc1.space_after = Pt(8)

    sc_points = [
        ("East Village Volume Dominance: ", "Historically accounts for 54.8% of all downtown homelessness (mean 552.8 individuals). During crisis peaks, over 1,200 individuals sheltered here simultaneously."),
        ("100% of Top 10 in South East Village: ", "Every single one of the top 10 persistent hotspot blocks is located south of Market Street in East Village, forming a permanent geographic cluster."),
        ("The Built Environment Triad: ", "Hotspots do not occur at random; they are anchored by (1) Regional Transit Hubs (12th & Imperial Transit Center), (2) Intake Services (Father Joe's Villages, Neil Good Day Center), and (3) Caltrans freeway underpasses providing structural overhead shelter.")
    ]
    for sct, scd in sc_points:
        p = tf_sc.add_paragraph(); p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + sct; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = scd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 7: HOTSPOT CENTROID MIGRATION (121M SOUTHWARD)
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout); set_slide_background(s7)
    add_canva_header(s7, "Geospatial Hotspot Dynamics: The 121-Meter Southward Displacement Vector", "Cluster Migration Vector", "07")
    add_canva_footer(s7, 7)

    # Left Container: Migration Figure
    add_canva_card(s7, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s7, SLIDE_ASSETS / "task93_hotspot_migration.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    # Right Container: Migration Drivers
    add_canva_card(s7, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_m7 = s7.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_m7 = tb_m7.text_frame; tf_m7.word_wrap = True
    pm1 = tf_m7.paragraphs[0]; pm1.text = "DRIVERS OF CLUSTER DISPLACEMENT"; pm1.font.name = FONT_DISPLAY; pm1.font.size = Pt(12.5); pm1.font.bold = True; pm1.font.color.rgb = COLOR_PRIMARY_NAVY; pm1.space_after = Pt(8)

    m_points = [
        ("121-Meter Migration Vector: ", "Between the Early Period (2018–2020) and the Recent Period (2022–2025), the count-weighted hotspot centroid migrated 121 meters south toward Commercial St and Imperial Ave."),
        ("Northern Right-of-Way Sweeps: ", "Aggressive enforcement of sidewalk accessibility in commercial retail corridors (Gaslamp, Core/City Center, North East Village) pushed individuals southward."),
        ("Freeway & Industrial Buffer: ", "Displaced encampments compressed into the industrial transition zone bordering Interstate 5 and the MTS rail yards, where enforcement was historically less continuous."),
        ("Service Gravity: ", "Expanding safe sleeping and shelter intakes along 20th & B and Commercial Street acted as an institutional gravity well cementing the southward migration.")
    ]
    for mt, md in m_points:
        p = tf_m7.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + mt; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = md; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 8: MACHINE LEARNING FORECASTING BENCHMARK
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout); set_slide_background(s8)
    add_canva_header(s8, "Multi-Model Machine Learning Benchmark: 5-Fold Walk-Forward Cross-Validation", "Predictive Intelligence", "08")
    add_canva_footer(s8, 8)

    # Left Container: 5-Fold CV Table
    add_canva_card(s8, Inches(0.8), Inches(1.6), Inches(7.0), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_f8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.6), Inches(0.5))
    tb_f8.text_frame.paragraphs[0].text = "5-Fold Walk-Forward Cross-Validation Performance (96 Months, Zero Leakage)"
    tb_f8.text_frame.paragraphs[0].font.name = FONT_DISPLAY; tb_f8.text_frame.paragraphs[0].font.size = Pt(11.5); tb_f8.text_frame.paragraphs[0].font.bold = True; tb_f8.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY_NAVY

    ml_headers = ["Model Architecture", "1-Month MAPE", "3-Month MAPE", "6-Month MAPE", "12-Month CV MAPE"]
    ml_rows = [
        ["XGBoost (Champion)", "12.45% ± 5.8%", "18.92% ± 8.4%", "27.34% ± 12.6%", "39.34% ± 25.4%"],
        ["Holt-Winters Exp Smooth", "13.82% ± 6.2%", "20.15% ± 9.1%", "28.90% ± 13.8%", "39.57% ± 27.6%"],
        ["SARIMA (1,1,1)(0,0,0)", "14.10% ± 7.4%", "21.50% ± 11.2%", "30.45% ± 16.5%", "40.10% ± 34.5%"],
        ["Naive Seasonal (t-12)", "19.85% ± 9.5%", "29.40% ± 14.2%", "38.20% ± 18.9%", "51.34% ± 24.5%"],
        ["Prophet (Changepoints)", "22.30% ± 11.0%", "33.15% ± 16.8%", "45.80% ± 22.4%", "63.81% ± 35.5%"],
    ]
    add_formatted_table(s8, Inches(1.0), Inches(2.35), Inches(6.6), Inches(3.9), ml_headers, ml_rows, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)])

    # Right Container: Machine Learning Findings
    add_canva_card(s8, Inches(8.0), Inches(1.6), Inches(4.533), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_mf = s8.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(3.933), Inches(4.6))
    tf_mf = tb_mf.text_frame; tf_mf.word_wrap = True
    pmf1 = tf_mf.paragraphs[0]; pmf1.text = "CORE FORECASTING TAKEAWAYS"; pmf1.font.name = FONT_DISPLAY; pmf1.font.size = Pt(12.5); pmf1.font.bold = True; pmf1.font.color.rgb = COLOR_PRIMARY_NAVY; pmf1.space_after = Pt(8)

    ml_points = [
        ("XGBoost Wins Citywide: ", "Achieved lowest 12-month CV error (39.34%) and best 2025 hold-out performance (38.48%). Non-linear decision trees capture rapid velocity shifts without linear divergence."),
        ("Holt-Winters as Parametric Anchor: ", "Holt-Winters achieved virtually tied accuracy (39.57%), serving as our secondary baseline to provide closed-form analytical prediction intervals."),
        ("Why Prophet Failed: ", "Prophet's Bayesian changepoints overshot post-2023 counts by +63.8%, failing to adapt to the camping ordinance inflection. Fixed changepoint models should NOT be used for policy stress testing.")
    ]
    for mlt, mld in ml_points:
        p = tf_mf.add_paragraph(); p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + mlt; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = mld; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 9: 2026 FORWARD OUTLOOK & SCENARIO PLANNING
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout); set_slide_background(s9)
    add_canva_header(s9, "2026 Forward Outlook: Stress-Testing Three Strategic Policy Scenarios", "Prospective Forecasting", "09")
    add_canva_footer(s9, 9)

    # Left Container: Forecast Graphic
    add_canva_card(s9, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s9, SLIDE_ASSETS / "task93_forecast_2026.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    # Right Container: Scenario Matrix
    add_canva_card(s9, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_sc9 = s9.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_sc9 = tb_sc9.text_frame; tf_sc9.word_wrap = True
    psc9 = tf_sc9.paragraphs[0]; psc9.text = "PROSPECTIVE 2026 SCENARIOS"; psc9.font.name = FONT_DISPLAY; psc9.font.size = Pt(12.5); psc9.font.bold = True; psc9.font.color.rgb = COLOR_PRIMARY_NAVY; psc9.space_after = Pt(8)

    scenarios = [
        ("Baseline (Status Quo): ", "Monthly counts projected to remain range-bound between 850 and 920 individuals (Month 12: 890). Assumes current shelter turnover and enforcement levels."),
        ("Optimistic Scenario (-24% at M12): ", "Accelerated Safe Sleeping Sites and 800 shelter beds drive downtown street counts down to ~670 individuals by December 2026."),
        ("Pessimistic Scenario (+26% at M12): ", "Capacity exhaustion, shelter closures, and eviction spikes push counts back up to ~1,110 individuals by December 2026."),
        ("The Necessity of Uncertainty Bands: ", "Point forecasts without prediction intervals mislead decision-makers. Planning must accommodate the calibrated 80% and 95% fan envelopes.")
    ]
    for st, sd in scenarios:
        p = tf_sc9.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + st; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = sd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 10: THE REGIONAL DISPLACEMENT PARADOX
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout); set_slide_background(s10)
    add_canva_header(s10, "The Regional Displacement Paradox: Downtown Collapse vs. Countywide Record", "Regional Policy Dynamics", "10")
    add_canva_footer(s10, 10)

    # Left Container: Regional Divergence Graphic
    add_canva_card(s10, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s10, SLIDE_ASSETS / "task93_regional_divergence.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    # Right Container: Regional Synthesis
    add_canva_card(s10, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_r10 = s10.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_r10 = tb_r10.text_frame; tf_r10.word_wrap = True
    pr10 = tf_r10.paragraphs[0]; pr10.text = "THE DISPLACEMENT REALITY"; pr10.font.name = FONT_DISPLAY; pr10.font.size = Pt(12.5); pr10.font.bold = True; pr10.font.color.rgb = COLOR_PRIMARY_NAVY; pr10.space_after = Pt(8)

    r_points = [
        ("Downtown Share Collapsed: ", "Downtown's share of countywide unsheltered homelessness plunged from 37.5% in January 2023 to 14.9% in January 2025."),
        ("Countywide Homelessness Hit Record: ", "Simultaneously, the RTFH Point-in-Time count recorded an all-time countywide peak of 6,110 unsheltered individuals in 2024 (and 5,714 in 2025)."),
        ("Displacement, Not Elimination: ", "The Unsafe Camping Ordinance successfully reduced visible encampments in commercial corridors, but individuals were dispersed into riverbeds, freeway rights-of-way, and neighboring jurisdictions (El Cajon, Chula Vista, National City)."),
        ("Regional Coordination Required: ", "City-centric enforcement without countywide shelter capacity shifts the burden rather than solving the systemic crisis.")
    ]
    for rt, rd in r_points:
        p = tf_r10.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + rt; r1.font.name = FONT_BODY; r1.font.size = Pt(10); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = rd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 11: MACRO ESTIMATION & THE 4 COMMUNICATION RULES
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout); set_slide_background(s11)
    add_canva_header(s11, "Countywide Macro Estimation Model & Mandatory Communication Rules", "Macro Econometrics & Governance", "11")
    add_canva_footer(s11, 11)

    # Left Container: Model Specification
    add_canva_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_m11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.6))
    tf_m11 = tb_m11.text_frame; tf_m11.word_wrap = True
    pm11 = tf_m11.paragraphs[0]; pm11.text = "POLICY REGIME OLS CHAMPION MODEL"; pm11.font.name = FONT_DISPLAY; pm11.font.size = Pt(12.5); pm11.font.bold = True; pm11.font.color.rgb = COLOR_PRIMARY_NAVY; pm11.space_after = Pt(6)

    m11_specs = [
        ("Constant-Ratio Assumption Rejected: ", "One-Way ANOVA decisively rejects ratio stability across regimes: F = 66.51, p = 0.0002, eta^2 = 0.9638. A constant-ratio multiplier creates up to +96.2% error!"),
        ("Econometric Equation: ", "Y = 4,513.26 + 0.1859 * X + 1,225.04 * D_post\nWhere X = Downtown monthly count, D_post = 1 under active Camping Ordinance enforcement."),
        ("Model Goodness-of-Fit: ", "R^2 = 0.9638 | Adj R^2 = 0.9493 | LOOCV RMSE = 815.32 | Signed Bias = -0.34%."),
        ("Current County Estimate (Dec 2025): ", "5,900 [95% PI: 3,900 to 8,000 individuals]\nCalibrated margin of error is +/- 2,050 individuals (+/- 35%) using exact Student's t distribution (df=5).")
    ]
    for mt, md in m11_specs:
        p = tf_m11.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + mt; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = md; r2.font.name = FONT_BODY; r2.font.size = Pt(9.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # Right Container: The 4 Public Communication Rules
    add_canva_card(s11, Inches(6.7), Inches(1.6), Inches(5.833), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_r11 = s11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.233), Inches(4.6))
    tf_r11 = tb_r11.text_frame; tf_r11.word_wrap = True
    pr11 = tf_r11.paragraphs[0]; pr11.text = "THE 4 MANDATORY PUBLIC COMMUNICATION RULES"; pr11.font.name = FONT_DISPLAY; pr11.font.size = Pt(12.5); pr11.font.bold = True; pr11.font.color.rgb = COLOR_RED; pr11.space_after = Pt(8)

    rules = [
        ("Rule 1: Prohibit Raw Single-Point Precision", "Never publish uncalibrated single figures like '5,921'. False precision misleads the public and damages institutional credibility."),
        ("Rule 2: Mandate Rounding to Nearest 100", "Always round estimated point totals to the nearest 100 individuals (e.g. mandate '5,900' instead of '5,921')."),
        ("Rule 3: Always Publish Calibrated 95% Interval", "Every headline figure MUST be accompanied by its calibrated Student's t prediction interval: '5,900 [3,900 to 8,000]'."),
        ("Rule 4: Mandatory Policy Regime Disclosure", "Public statements must explicitly disclose that the +1,225 adjustment accounts for displacement following the July 2023 Camping Ordinance.")
    ]
    for r_title, r_desc in rules:
        p = tf_r11.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = r_title + "\n"; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_PRIMARY_NAVY
        r2 = p.add_run(); r2.text = r_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 12: MUNICIPAL POLICY ACTION ROADMAP
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout); set_slide_background(s12)
    add_canva_header(s12, "Municipal Policy Action Roadmap: 30-Day, 1-Year, and 3-Year Horizons", "Strategic Recommendations", "12")
    add_canva_footer(s12, 12)

    # 3 Column Roadmap
    horizons = [
        ("Immediate Action (30–90 Days)", "High-Frequency Outreach & Tool Deployment", COLOR_ROYAL_BLUE, [
            ("Mobile Sanitation: ", "Deploy intensive hygiene and mobile restrooms directly to the top 10 persistent hotspot blocks (led by 16th & Imperial)."),
            ("Dashboard Deployment: ", "Provide City Council and County Supervisors with live dashboard access for real-time surveillance."),
            ("Target Metric: ", "Zero unsheltered growth on top 5 hotspot blocks."),
            ("Lead: ", "City Homelessness Strategies & DSDP.")
        ]),
        ("Medium-Term (6–12 Months)", "Safe Sleeping & Regional Containment", COLOR_GREEN, [
            ("Scale Safe Sleeping: ", "Expand Safe Sleeping Sites by 800 beds to capture the -24% optimistic scenario (~670 individuals)."),
            ("Regional Taskforce: ", "Establish joint intervention protocol with East & South County to intercept displaced encampments."),
            ("Target Metric: ", "Sub-700 downtown count sustained 6+ months."),
            ("Lead: ", "City of San Diego, RTFH, Caltrans.")
        ]),
        ("Long-Term (1–3 Years)", "System Integration & Housing Exits", COLOR_PRIMARY_NAVY, [
            ("Regional HMIS 2.0: ", "Deploy integrated bed reservation system with real-time shelter vacancy tracking across all regional providers."),
            ("Permanent Housing: ", "Fund 1,500 permanent supportive housing units with tenancy retention services."),
            ("Target Metric: ", "25%+ reduction in countywide unsheltered PIT."),
            ("Lead: ", "County Health & Human Services, RTFH.")
        ])
    ]
    for idx, (title, sub, col, items) in enumerate(horizons):
        h_left = Inches(0.8 + idx * 3.98)
        add_canva_card(s12, h_left, Inches(1.6), Inches(3.78), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)

        # Header bar
        hbar = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, h_left, Inches(1.6), Inches(3.78), Inches(0.1))
        hbar.fill.solid(); hbar.fill.fore_color.rgb = col; hbar.line.fill.background()

        tb = s12.shapes.add_textbox(h_left + Inches(0.2), Inches(1.8), Inches(3.38), Inches(4.6))
        tf = tb.text_frame; tf.word_wrap = True
        p_ht = tf.paragraphs[0]; p_ht.text = title.upper(); p_ht.font.name = FONT_DISPLAY; p_ht.font.size = Pt(11); p_ht.font.bold = True; p_ht.font.color.rgb = col; p_ht.space_after = Pt(2)
        p_hs = tf.add_paragraph(); p_hs.text = sub; p_hs.font.name = FONT_BODY; p_hs.font.size = Pt(9.0); p_hs.font.bold = True; p_hs.font.color.rgb = COLOR_TEXT_MUTED; p_hs.space_after = Pt(10)

        for it, idesc in items:
            p = tf.add_paragraph(); p.space_after = Pt(6)
            r1 = p.add_run(); r1.text = "• " + it; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_TEXT_DARK
            r2 = p.add_run(); r2.text = idesc; r2.font.name = FONT_BODY; r2.font.size = Pt(8.8); r2.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # SLIDE 13: THE INTERACTIVE DECISION-SUPPORT DASHBOARD
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout); set_slide_background(s13)
    add_canva_header(s13, "Interactive Decision-Support System: The Streamlit Executive Dashboard", "Operational Decision Tool", "13")
    add_canva_footer(s13, 13)

    # Left Container: Feature Matrix
    add_canva_card(s13, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_db = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(7.1), Inches(4.6))
    tf_db = tb_db.text_frame; tf_db.word_wrap = True
    pdb = tf_db.paragraphs[0]; pdb.text = "THE 6 SPECIALIZED DASHBOARD MODULES (TASK 9.1)"; pdb.font.name = FONT_DISPLAY; pdb.font.size = Pt(12.5); pdb.font.bold = True; pdb.font.color.rgb = COLOR_PRIMARY_NAVY; pdb.space_after = Pt(8)

    db_tabs = [
        ("Tab 1: Historical Trends View", "Longitudinal multi-year time series (2017–2025), dynamic multiplier regime markers, macro policy epoch shading, and component toggles (individuals, tents, vehicles)."),
        ("Tab 2: 12-Month Forward Forecast", "Prospective 2026 projections, model selectors (XGBoost champion, Holt-Winters, SARIMA, Prophet), shaded 80%/95% prediction fans, and scenario stress testing (-24% optimistic, +26% pessimistic)."),
        ("Tab 3: Hotspot Surveillance Map", "Folium interactive choropleth, 12 count dates selector, balanced 261 vs 382 footprint toggle, Getis-Ord Gi* classifications (90%, 95%, 99%), and centroid migration vector."),
        ("Tab 4: Neighborhood Decomposition", "4-pane STL decomposition (Trend, Seasonality, Residuals) and Kruskal-Wallis non-parametric significance displays."),
        ("Tab 5: County Estimation Calculator", "Interactive Policy Regime OLS calculator strictly enforcing The 4 Public Communication Rules with Student's t prediction intervals."),
        ("Tab 6: Methodology & Governance", "Comprehensive documentation of 4 multiplier schedules, 2022 footprint expansion (+121 blocks), and root causes for historical missing data.")
    ]
    for tt, td in db_tabs:
        p = tf_db.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + tt + ": "; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = td; r2.font.name = FONT_BODY; r2.font.size = Pt(8.8); r2.font.color.rgb = COLOR_TEXT_DARK

    # Right Container: Operational Info & Access
    add_canva_card(s13, Inches(8.5), Inches(1.6), Inches(4.033), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_op = s13.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.433), Inches(4.6))
    tf_op = tb_op.text_frame; tf_op.word_wrap = True
    pop1 = tf_op.paragraphs[0]; pop1.text = "DEPLOYMENT & ACCESS INFO"; pop1.font.name = FONT_DISPLAY; pop1.font.size = Pt(12.5); pop1.font.bold = True; pop1.font.color.rgb = COLOR_PRIMARY_NAVY; pop1.space_after = Pt(8)

    op_points = [
        ("Local Live URL: ", "http://localhost:8501 (Fast sub-2s response time)"),
        ("Cloud Production URL: ", "https://downtown-sd-homelessness.streamlit.app"),
        ("Automated Quality: ", "10 / 10 pytest unit tests passing with zero regressions."),
        ("Data Pipeline SLA: ", "@st.cache_data architecture provides microsecond cached lookups across all 6 tabs."),
        ("Target Users: ", "City Council policy analysts, RTFH outreach coordinators, and DSDP operations directors.")
    ]
    for opt, opd in op_points:
        p = tf_op.add_paragraph(); p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + opt; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = opd; r2.font.name = FONT_BODY; r2.font.size = Pt(9.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 14: EXECUTIVE SYNTHESIS & STRATEGIC NEXT STEPS
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout); set_slide_background(s14)
    add_canva_header(s14, "Executive Synthesis, Data Governance & Partnership Next Steps", "Synthesis & Next Steps", "14")
    add_canva_footer(s14, 14)

    # 3 Conclusion Cards
    conclusions = [
        ("Evidence-Based Resource Allocation", "Move Beyond Seasonal Budgeting", COLOR_PRIMARY_NAVY, "Discontinue volatile seasonal budget adjustments. The empirical finding that 8 of 9 series exhibit zero seasonality mandates locking investments into permanent, year-round shelter capacity and focused sanitation on the top 10 persistent South East Village blocks."),
        ("Regional Accountability & Systems Reform", "Acknowledge the Regional Displacement Reality", COLOR_ROYAL_BLUE, "Municipal enforcement in downtown corridors has displaced unsheltered individuals into surrounding municipalities and Caltrans corridors. Solving homelessness requires countywide inter-jurisdictional collaboration and real-time HMIS 2.0 bed allocation."),
        ("Continuous Data Governance & Machine Learning", "Annual Retraining & Multi-Source Expansion", COLOR_GREEN, "Retrain the Policy Regime OLS model annually upon RTFH January PIT release using the calibrated Student's t distribution. Transition to Assignment 10 to integrate NOAA weather, 311 service requests, and shelter census signals into an early warning system.")
    ]
    for idx, (title, sub, col, body) in enumerate(conclusions):
        top_y = Inches(1.6 + idx * 1.7)
        add_canva_card(s14, Inches(0.8), top_y, Inches(11.733), Inches(1.55), COLOR_CARD_BG, COLOR_CARD_BORDER)

        # Left accent block
        bar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, Inches(0.12), Inches(1.55))
        bar.fill.solid(); bar.fill.fore_color.rgb = col; bar.line.fill.background()

        tb = s14.shapes.add_textbox(Inches(1.1), top_y + Inches(0.12), Inches(11.2), Inches(1.3))
        tf = tb.text_frame; tf.word_wrap = True
        pc1 = tf.paragraphs[0]; pc1.text = title.upper(); pc1.font.name = FONT_DISPLAY; pc1.font.size = Pt(11.5); pc1.font.bold = True; pc1.font.color.rgb = col; pc1.space_after = Pt(2)
        pc2 = tf.add_paragraph(); pc2.text = sub; pc2.font.name = FONT_BODY; pc2.font.size = Pt(9.5); pc2.font.bold = True; pc2.font.color.rgb = COLOR_TEXT_DARK; pc2.space_after = Pt(4)
        pc3 = tf.add_paragraph(); pc3.text = body; pc3.font.name = FONT_BODY; pc3.font.size = Pt(8.8); pc3.font.color.rgb = COLOR_TEXT_MUTED

    # Save Presentation
    prs.save(str(OUTPUT_PPTX))
    print(f"Successfully generated 14-slide presentation: {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_deck()
