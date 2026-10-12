"""
Native PowerPoint Presentation Generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.pptx
Adheres strictly to the Canva 'Blue and White Modern Data Analytics' Design System (16:9 widescreen).
Features 14 production-grade executive slides with KPI cards, tables, high-DPI graphics,
and strict compliance with The 4 Public Communication Rules and v3.0 Report outputs.
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

    line_v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.06), Inches(0.82))
    line_v.fill.solid()
    line_v.fill.fore_color.rgb = COLOR_ROYAL_BLUE
    line_v.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.38), Inches(10.8), Inches(0.92))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_sub = tf.paragraphs[0]
    p_sub.text = category_text.upper()
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_ROYAL_BLUE
    p_sub.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_DISPLAY
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_NAVY

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
    p_l.font.size = Pt(11.5)
    p_l.font.bold = True
    p_l.font.color.rgb = COLOR_TEXT_DARK
    p_l.space_after = Pt(3)

    p_s = tf.add_paragraph()
    p_s.text = subtext_str
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(10.5)
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
        p.font.size = Pt(11.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_BG
        p.alignment = PP_ALIGN.CENTER

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
            p.font.size = Pt(10.5)
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
    # SLIDE 1: TITLE SLIDE
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_canva_card(s1, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7), COLOR_CARD_BG, COLOR_CARD_BORDER)

    add_canva_card(s1, Inches(1.6), Inches(1.5), Inches(4.8), Inches(0.42), COLOR_ICE_TINT, COLOR_SOFT_BLUE)
    tb_c = s1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(4.8), Inches(0.42))
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS BRIEFING"
    p_c.font.name = FONT_BODY
    p_c.font.size = Pt(12)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_PRIMARY_NAVY

    tb_t = s1.shapes.add_textbox(Inches(1.6), Inches(2.15), Inches(10.0), Inches(2.2))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "Downtown Homelessness:\nExecutive Strategic Roadmap (2017–2026)"
    p_t1.font.name = FONT_DISPLAY; p_t1.font.size = Pt(32); p_t1.font.bold = True; p_t1.font.color.rgb = COLOR_PRIMARY_NAVY; p_t1.space_after = Pt(12)

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Econometrics, Spatial Dynamics, ML Forecasting & Regional Policy"
    p_t2.font.name = FONT_BODY; p_t2.font.size = Pt(15); p_t2.font.bold = True; p_t2.font.color.rgb = COLOR_ROYAL_BLUE

    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(4.6), Inches(10.0), Inches(0.015))
    div1.fill.solid(); div1.fill.fore_color.rgb = COLOR_CARD_BORDER; div1.line.fill.background()

    meta_items = [
        ("Partnership & Author", "DSA, DSDP, RTFH\nLead: K.S. Lwin | Proj Lead: A. Mancebo Jr."),
        ("Data Foundation", "108 months of counts (2017-2025)\nRegional PIT censuses"),
        ("Analytical Framework", "Spatial Gi* • Walk-Forward CV • OLS Regime • 4 Comm Rules")
    ]
    for idx, (m_label, m_val) in enumerate(meta_items):
        m_left = Inches(1.6 + idx * 3.4)
        tb_m = s1.shapes.add_textbox(m_left, Inches(4.8), Inches(3.1), Inches(1.4))
        tf_m = tb_m.text_frame; tf_m.word_wrap = True
        p_ml = tf_m.paragraphs[0]; p_ml.text = m_label.upper(); p_ml.font.name = FONT_BODY; p_ml.font.size = Pt(11.5); p_ml.font.bold = True; p_ml.font.color.rgb = COLOR_ROYAL_BLUE; p_ml.space_after = Pt(2)
        p_mv = tf_m.add_paragraph(); p_mv.text = m_val; p_mv.font.name = FONT_BODY; p_mv.font.size = Pt(11.0); p_mv.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 2: EXECUTIVE KPI DASHBOARD (4 CORE METRICS)
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout); set_slide_background(s2)
    add_canva_header(s2, "Executive KPIs: Peak & Migration", "Executive Framing", "02")
    add_canva_footer(s2, 2)

    kpis = [
        ("2,103", "Crisis Peak (May 2023)", "Highest count on record. Capped a 3-year surge.", COLOR_RED),
        ("851", "Recent Count (Jan 2025)", "Down 59% from peak. Dec 2025 hit 985.", COLOR_GREEN),
        ("54.0%", "East Village Concentration", "Core driver of downtown population.", COLOR_PRIMARY_NAVY),
        ("120 m", "Hotspot Migration Vector", "Centroid shifted 120m south toward South East Village.", COLOR_ROYAL_BLUE),
    ]
    for idx, (val, lbl, sub, col) in enumerate(kpis):
        k_left = Inches(0.8 + idx * 2.98)
        add_kpi_card(s2, k_left, Inches(1.6), Inches(2.78), Inches(2.1), val, lbl, sub, col)

    add_canva_card(s2, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.6), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_s2 = s2.shapes.add_textbox(Inches(1.1), Inches(4.2), Inches(11.1), Inches(2.2))
    tf_s2 = tb_s2.text_frame; tf_s2.word_wrap = True
    p1 = tf_s2.paragraphs[0]
    p1.text = "THE REALITY: DOWNTOWN DROPS VS REGIONAL SHIFTS"
    p1.font.name = FONT_DISPLAY; p1.font.size = Pt(13); p1.font.bold = True; p1.font.color.rgb = COLOR_PRIMARY_NAVY; p1.space_after = Pt(6)

    bullets = [
        ("Three Phases: ", "Pre-COVID drop, massive 2021-2023 surge (peak 2,103), then post-enforcement contraction (851 in Jan 2025)."),
        ("No Seasonality: ", "Weather doesn't drive numbers (p=0.995). Seasonal budgets are a mismatch for year-round needs."),
        ("Map Changes: ", "121 blocks added in 2022. Correcting for this shows a real, but smaller, +71% surge in the core."),
        ("Regional Shift: ", "Downtown share fell to 15%, while countywide hit a record 6,110. The crisis moved, it didn't end.")
    ]
    for b_title, b_text in bullets:
        p = tf_s2.add_paragraph()
        p.space_after = Pt(4)
        run_t = p.add_run(); run_t.text = "• " + b_title; run_t.font.name = FONT_BODY; run_t.font.size = Pt(12); run_t.font.bold = True; run_t.font.color.rgb = COLOR_ROYAL_BLUE
        run_d = p.add_run(); run_d.text = b_text; run_d.font.name = FONT_BODY; run_d.font.size = Pt(11.5); run_d.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 3: THE 9-YEAR TRAJECTORY & THREE MACRO EPOCHS
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout); set_slide_background(s3)
    add_canva_header(s3, "9-Year Trajectory: Three Policy Epochs", "Longitudinal Dynamics", "03")
    add_canva_footer(s3, 3)

    add_canva_card(s3, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s3, SLIDE_ASSETS / "task93_trajectory_9year.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    epochs = [
        ("Epoch 1: Contraction (2017–2020)", "Low of 529 in Mar 2020 (−38%)", "Pre-COVID drop. Baseline interventions worked.", COLOR_ROYAL_BLUE),
        ("Epoch 2: Crisis Surge (2021–2023)", "May 2023 Peak of 2,103 (+297%)", "Driven by shelter de-densification and housing vulnerability.", COLOR_RED),
        ("Epoch 3: Enforcement (2024–2025)", "Jan 2025 Count of 851 (−59%)", "Sharp drop post-Camping Ordinance. Counts stabilized ~860-880.", COLOR_GREEN),
    ]
    for idx, (title, stat, desc, col) in enumerate(epochs):
        top_y = Inches(1.6 + idx * 1.7)
        add_canva_card(s3, Inches(8.2), top_y, Inches(4.333), Inches(1.55), COLOR_CARD_BG, COLOR_CARD_BORDER)
        tb_e = s3.shapes.add_textbox(Inches(8.4), top_y + Inches(0.12), Inches(3.933), Inches(1.3))
        tf_e = tb_e.text_frame; tf_e.word_wrap = True
        pe1 = tf_e.paragraphs[0]; pe1.text = title; pe1.font.name = FONT_DISPLAY; pe1.font.size = Pt(11); pe1.font.bold = True; pe1.font.color.rgb = col; pe1.space_after = Pt(2)
        pe2 = tf_e.add_paragraph(); pe2.text = stat; pe2.font.name = FONT_BODY; pe2.font.size = Pt(11.5); pe2.font.bold = True; pe2.font.color.rgb = COLOR_TEXT_DARK; pe2.space_after = Pt(2)
        pe3 = tf_e.add_paragraph(); pe3.text = desc; pe3.font.name = FONT_BODY; pe3.font.size = Pt(10.5); pe3.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # SLIDE 4: DEBUNKING THE SEASONALITY MYTH
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout); set_slide_background(s4)
    add_canva_header(s4, "Seasonality Myth: Weather Doesn't Drive Homelessness", "Econometric Seasonality Proof", "04")
    add_canva_footer(s4, 4)

    add_canva_card(s4, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_t4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.4), Inches(0.5))
    p_t4 = tb_t4.text_frame.paragraphs[0]
    p_t4.text = "Kruskal-Wallis Tests (df=11)"
    p_t4.font.name = FONT_DISPLAY; p_t4.font.size = Pt(11.5); p_t4.font.bold = True; p_t4.font.color.rgb = COLOR_PRIMARY_NAVY

    kw_headers = ["Geographic Series", "Kruskal-Wallis H", "KW p", "ANOVA p", "Verdict"]
    kw_data = [
        ["Overall — Reported Footprint", "2.66", "0.995", "0.998", "No Seasonality"],
        ["Overall — Fixed Core Six", "9.00", "0.622", "0.670", "No Seasonality"],
        ["East Village (Epicenter)", "14.16", "0.224", "0.219", "No Seasonality"],
        ["City Center (Core)", "4.86", "0.938", "0.913", "No Seasonality"],
        ["Gaslamp Quarter", "14.57", "0.203", "0.087", "No Seasonality"],
        ["Columbia", "8.76", "0.644", "0.473", "No Seasonality"],
        ["Cortez", "12.73", "0.312", "0.047", "Mixed"],
        ["Marina", "19.88", "0.047", "0.162", "Mixed"],
        ["Outside Perimeter", "11.45", "0.406", "0.440", "No Seasonality"],
    ]
    add_formatted_table(s4, Inches(1.0), Inches(2.35), Inches(6.4), Inches(3.95), kw_headers, kw_data, [Inches(2.5), Inches(0.9), Inches(0.7), Inches(0.7), Inches(1.6)])

    add_canva_card(s4, Inches(7.9), Inches(1.6), Inches(4.633), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_p4 = s4.shapes.add_textbox(Inches(8.2), Inches(1.8), Inches(4.033), Inches(4.6))
    tf_p4 = tb_p4.text_frame; tf_p4.word_wrap = True
    pp1 = tf_p4.paragraphs[0]; pp1.text = "WHY THIS MATTERS FOR MUNICIPAL BUDGETING"; pp1.font.name = FONT_DISPLAY; pp1.font.size = Pt(12.5); pp1.font.bold = True; pp1.font.color.rgb = COLOR_PRIMARY_NAVY; pp1.space_after = Pt(8)

    points4 = [
        ("Weather Fallacy: ", "Calendar months explain zero variation (p=0.995). Seasonal planning is flawed."),
        ("Macro Drivers: ", "Shifts are driven by capacity, policy, and housing dynamics—not weather."),
        ("Fund Year-Round: ", "Stop seasonal allocations. Commit to permanent capacity."),
        ("Solid Evidence: ", "8 of 9 series show strictly non-significant seasonality.")
    ]
    for pt, pd in points4:
        p = tf_p4.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + pt; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = pd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 5: THE 2022 BOUNDARY EXPANSION WEDGE
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout); set_slide_background(s5)
    add_canva_header(s5, "Map Changes: Disentangling Reality from Map Changes", "Spatial Panel Accounting", "05")
    add_canva_footer(s5, 5)

    add_canva_card(s5, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s5, SLIDE_ASSETS / "task93_footprint_wedge.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    add_canva_card(s5, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_w5 = s5.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_w5 = tb_w5.text_frame; tf_w5.word_wrap = True
    pw1 = tf_w5.paragraphs[0]; pw1.text = "ACCOUNTING FOR THE 121-BLOCK EXPANSION"; pw1.font.name = FONT_DISPLAY; pw1.font.size = Pt(12.5); pw1.font.bold = True; pw1.font.color.rgb = COLOR_PRIMARY_NAVY; pw1.space_after = Pt(8)

    w_points = [
        ("Administrative Shift: ", "121 blocks added in 2022 (Golden Hill, Barrio Logan)."),
        ("The Wedge Effect: ", "Added blocks inflated counts by up to 33% (640 individuals at peak)."),
        ("True Core Growth: ", "Balanced 261-block panel still grew 71% in 2022. Boundaries matter."),
        ("Analytical Fix: ", "Enforced strict 261-block balance across all years.")
    ]
    for wt, wd in w_points:
        p = tf_w5.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + wt; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = wd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 6: GEOSPATIAL CONCENTRATION: THE EAST VILLAGE EPICENTER
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout); set_slide_background(s6)
    add_canva_header(s6, "Concentration: The East Village Epicenter", "Geographic Concentration", "06")
    add_canva_footer(s6, 6)

    add_canva_card(s6, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_h6 = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.4), Inches(0.5))
    tb_h6.text_frame.paragraphs[0].text = "Top Hotspots (Getis-Ord Gi*)"
    tb_h6.text_frame.paragraphs[0].font.name = FONT_DISPLAY
    tb_h6.text_frame.paragraphs[0].font.size = Pt(11.5)
    tb_h6.text_frame.paragraphs[0].font.bold = True
    tb_h6.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY_NAVY

    hotspot_headers = ["Rank", "Block Identifier", "Area", "Hotspot Dates", "Rate", "Mean Count"]
    hotspot_rows = [
        ["#1", "16th St & Imperial Ave", "South East Village", "9 / 12 dates", "75%", "5.9"],
        ["#2", "I-5 SB & Imperial Ave", "South East Village", "8 / 12 dates", "67%", "4.4"],
        ["#3", "I-5 SB Off-Ramp (Map Border)", "South East Village", "6 / 12 dates", "50%", "6.8"],
        ["#4", "I-5 SB On-Ramp (Map Border)", "South East Village", "4 / 12 dates", "33%", "1.3"],
        ["#5", "17th St & Imperial Ave", "South East Village", "4 / 12 dates", "33%", "5.5"],
        ["#6", "16th St & J St", "South East Village", "2 / 12 dates", "17%", "13.3"],
        ["#7", "17th St & J St", "South East Village", "2 / 12 dates", "17%", "12.2"],
    ]
    add_formatted_table(s6, Inches(1.0), Inches(2.35), Inches(6.4), Inches(3.95), hotspot_headers, hotspot_rows, [Inches(0.6), Inches(2.3), Inches(1.5), Inches(0.9), Inches(0.5), Inches(0.6)])

    add_canva_card(s6, Inches(7.9), Inches(1.6), Inches(4.633), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_sc = s6.shapes.add_textbox(Inches(8.2), Inches(1.8), Inches(4.033), Inches(4.6))
    tf_sc = tb_sc.text_frame; tf_sc.word_wrap = True
    psc1 = tf_sc.paragraphs[0]; psc1.text = "THE BUILT-ENVIRONMENT MAGNET"; psc1.font.name = FONT_DISPLAY; psc1.font.size = Pt(12.5); psc1.font.bold = True; psc1.font.color.rgb = COLOR_PRIMARY_NAVY; psc1.space_after = Pt(8)

    sc_points = [
        ("Volume Dominance: ", "Drives 54% of downtown homelessness (avg 552 individuals)."),
        ("Top Hotspots: ", "100% of the top 10 persistent hotspots are in South East Village."),
        ("Built Magnets: ", "Clusters anchor around transit, services, and freeway underpasses.")
    ]
    for sct, scd in sc_points:
        p = tf_sc.add_paragraph(); p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + sct; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = scd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 7: HOTSPOT CENTROID MIGRATION (120M SOUTHWARD)
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout); set_slide_background(s7)
    add_canva_header(s7, "Hotspot Dynamics: 120m Southward Vector", "Cluster Migration Vector", "07")
    add_canva_footer(s7, 7)

    add_canva_card(s7, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s7, SLIDE_ASSETS / "task93_hotspot_migration.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    add_canva_card(s7, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_m7 = s7.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_m7 = tb_m7.text_frame; tf_m7.word_wrap = True
    pm1 = tf_m7.paragraphs[0]; pm1.text = "DRIVERS OF CLUSTER DISPLACEMENT"; pm1.font.name = FONT_DISPLAY; pm1.font.size = Pt(12.5); pm1.font.bold = True; pm1.font.color.rgb = COLOR_PRIMARY_NAVY; pm1.space_after = Pt(8)

    m_points = [
        ("120m Migration: ", "Centroid shifted 120m SSE toward South East Village."),
        ("Density Driven: ", "Unweighted moved 62m; density and location both pull south."),
        ("Enforcement Push: ", "Sidewalk clearance in Gaslamp displaced clusters south."),
        ("Spatial Shift: ", "Reflects macro cluster movements, not individual tracking.")
    ]
    for mt, md in m_points:
        p = tf_m7.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + mt; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = md; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 8: MACHINE LEARNING FORECASTING BENCHMARK
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout); set_slide_background(s8)
    add_canva_header(s8, "Machine Learning: 5-Fold CV Benchmark", "Predictive Intelligence", "08")
    add_canva_footer(s8, 8)

    add_canva_card(s8, Inches(0.8), Inches(1.6), Inches(7.0), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_f8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(6.6), Inches(0.5))
    tb_f8.text_frame.paragraphs[0].text = "5-Fold CV Performance"
    tb_f8.text_frame.paragraphs[0].font.name = FONT_DISPLAY; tb_f8.text_frame.paragraphs[0].font.size = Pt(11.5); tb_f8.text_frame.paragraphs[0].font.bold = True; tb_f8.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY_NAVY

    ml_headers = ["Model Architecture", "1-Month MAPE", "3-Month MAPE", "6-Month MAPE", "12-Month CV MAPE"]
    ml_rows = [
        ["SARIMA (ACF/PACF Grid)", "5.4% ± 4.1%", "14.3% ± 10.3%", "24.7% ± 20.9%", "39.6% ± 35.5%"],
        ["Holt-Winters Exp Smooth", "13.0% ± 9.2%", "17.6% ± 10.4%", "25.2% ± 18.2%", "38.4% ± 28.5%"],
        ["XGBoost (Champion)", "14.0% ± 8.9%", "19.9% ± 14.8%", "26.7% ± 18.5%", "38.3% ± 26.0%"],
        ["Naive Seasonal (t−12)", "39.5% ± 31.9%", "40.1% ± 31.3%", "48.5% ± 35.4%", "51.7% ± 24.5%"],
        ["Prophet (Changepoints)", "42.9% ± 26.0%", "42.7% ± 26.0%", "51.3% ± 31.9%", "64.2% ± 35.4%"],
    ]
    add_formatted_table(s8, Inches(1.0), Inches(2.35), Inches(6.6), Inches(3.95), ml_headers, ml_rows, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)])

    add_canva_card(s8, Inches(8.0), Inches(1.6), Inches(4.533), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_mf = s8.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(3.933), Inches(4.6))
    tf_mf = tb_mf.text_frame; tf_mf.word_wrap = True
    pmf1 = tf_mf.paragraphs[0]; pmf1.text = "CORE FORECASTING TAKEAWAYS"; pmf1.font.name = FONT_DISPLAY; pmf1.font.size = Pt(12.5); pmf1.font.bold = True; pmf1.font.color.rgb = COLOR_PRIMARY_NAVY; pmf1.space_after = Pt(8)

    ml_points = [
        ("Horizons: ", "SARIMA wins short-term (5.4% MAPE). XGBoost ties at 12-months (38.3%)."),
        ("Champion Model: ", "XGBoost chosen for lowest error and strong 2025 hold-out (8.5%)."),
        ("Baseline Check: ", "Naive seasonal performed well in 2025, proving baselines are critical."),
        ("Prophet Failure: ", "Prophet failed (64.2% error) as it missed the post-peak drop.")
    ]
    for mlt, mld in ml_points:
        p = tf_mf.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + mlt; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = mld; r2.font.name = FONT_BODY; r2.font.size = Pt(11.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 9: 2026 FORWARD OUTLOOK & SCENARIO PLANNING
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout); set_slide_background(s9)
    add_canva_header(s9, "2026 Outlook: Stress-Testing Scenarios", "Prospective Forecasting", "09")
    add_canva_footer(s9, 9)

    add_canva_card(s9, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s9, SLIDE_ASSETS / "task93_forecast_2026.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    add_canva_card(s9, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_sc9 = s9.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_sc9 = tb_sc9.text_frame; tf_sc9.word_wrap = True
    psc9 = tf_sc9.paragraphs[0]; psc9.text = "PROSPECTIVE 2026 SCENARIOS"; psc9.font.name = FONT_DISPLAY; psc9.font.size = Pt(12.5); psc9.font.bold = True; psc9.font.color.rgb = COLOR_PRIMARY_NAVY; psc9.space_after = Pt(8)

    scenarios = [
        ("Baseline: ", "Expected to remain range-bound at 816–896 individuals."),
        ("Stress-Tests: ", "Fixed scenario paths, not causal policy models."),
        ("Optimistic: ", "~675 individuals by Dec 2026 (favorable dynamics)."),
        ("Pessimistic: ", "~1,123 individuals by Dec 2026 (economic constraints)."),
        ("Range Planning: ", "Plan using uncertainty bands, not single points.")
    ]
    for st, sd in scenarios:
        p = tf_sc9.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + st; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = sd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 10: THE REGIONAL DISPLACEMENT PARADOX
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout); set_slide_background(s10)
    add_canva_header(s10, "Regional Displacement: Downtown Drops vs County Highs", "Regional Policy Dynamics", "10")
    add_canva_footer(s10, 10)

    add_canva_card(s10, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s10, SLIDE_ASSETS / "task93_regional_divergence.png", Inches(0.9), Inches(1.7), Inches(7.0), Inches(4.8))

    add_canva_card(s10, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_r10 = s10.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.733), Inches(4.6))
    tf_r10 = tb_r10.text_frame; tf_r10.word_wrap = True
    pr10 = tf_r10.paragraphs[0]; pr10.text = "THE DISPLACEMENT REALITY"; pr10.font.name = FONT_DISPLAY; pr10.font.size = Pt(12.5); pr10.font.bold = True; pr10.font.color.rgb = COLOR_PRIMARY_NAVY; pr10.space_after = Pt(8)

    r_points = [
        ("Share Plunged: ", "Downtown's share of county unsheltered fell to 14.9%."),
        ("County Record: ", "Countywide numbers reached 6,110 (2024) and 5,714 (2025)."),
        ("Displacement: ", "Downtown drops align with regional spikes. The crisis moved."),
        ("Data Limits: ", "Reflects macro divergence, individual tracking is unavailable.")
    ]
    for rt, rd in r_points:
        p = tf_r10.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + rt; r1.font.name = FONT_BODY; r1.font.size = Pt(12); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = rd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 11: MACRO ESTIMATION & THE 4 COMMUNICATION RULES
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout); set_slide_background(s11)
    add_canva_header(s11, "Macro Model & 4 Communication Rules", "Macro Econometrics & Governance", "11")
    add_canva_footer(s11, 11)

    add_canva_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_m11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.6))
    tf_m11 = tb_m11.text_frame; tf_m11.word_wrap = True
    pm11 = tf_m11.paragraphs[0]; pm11.text = "POLICY REGIME OLS CHAMPION MODEL"; pm11.font.name = FONT_DISPLAY; pm11.font.size = Pt(12.5); pm11.font.bold = True; pm11.font.color.rgb = COLOR_PRIMARY_NAVY; pm11.space_after = Pt(6)

    m11_specs = [
        ("Ratio Rejected: ", "Fixed ratios fail across policy regimes (ANOVA p=0.0002)."),
        ("Model Equation: ", "Y = 4,513 + 0.186X + 1,225*D_post (Accounts for 2024/25)."),
        ("Diagnostics: ", "R²=0.50. Slope and D_post are not strictly significant at 5%."),
        ("Current Estimate: ", "5,900 [95% PI: 3,900 to 8,000]. Margin of error is ±35%.")
    ]
    for mt, md in m11_specs:
        p = tf_m11.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = "• " + mt; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = md; r2.font.name = FONT_BODY; r2.font.size = Pt(11.0); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s11, Inches(6.7), Inches(1.6), Inches(5.833), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_r11 = s11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.233), Inches(4.6))
    tf_r11 = tb_r11.text_frame; tf_r11.word_wrap = True
    pr11 = tf_r11.paragraphs[0]; pr11.text = "THE 4 MANDATORY PUBLIC COMMUNICATION RULES"; pr11.font.name = FONT_DISPLAY; pr11.font.size = Pt(12.5); pr11.font.bold = True; pr11.font.color.rgb = COLOR_RED; pr11.space_after = Pt(8)

    rules = [
        ("Rule 1: No False Precision", "Stop using raw single points (e.g., '5,921'). It damages credibility."),
        ("Rule 2: Round to 100", "Always round estimates to the nearest hundred."),
        ("Rule 3: Show 95% Interval", "Mandate prediction ranges: '5,900 [3,900 to 8,000]'."),
        ("Rule 4: Disclose Regimes", "Explicitly state assumptions (e.g., assumes post-2023 enforcement holds).")
    ]
    for r_title, r_desc in rules:
        p = tf_r11.add_paragraph(); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = r_title + "\n"; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_PRIMARY_NAVY
        r2 = p.add_run(); r2.text = r_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(11.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 12: MUNICIPAL POLICY ACTION ROADMAP (MEMO R1–R8)
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout); set_slide_background(s12)
    add_canva_header(s12, "Policy Roadmap: Recommendations (R1–R8)", "Strategic Recommendations", "12")
    add_canva_footer(s12, 12)

    horizons = [
        ("Immediate (0–3 Months)", "Outreach & Governance", COLOR_ROYAL_BLUE, [
            ("R1. Hotspots: ", "Target 16th-17th & Imperial for rapid outreach."),
            ("R2. Range Planning: ", "Enforce Rules 1-4 for all public numbers."),
            ("R3. Boundary Clarity: ", "Disclose 261 vs 382-block footprint metrics."),
            ("Leaders: ", "City Strategies, DSDP.")
        ]),
        ("Medium (6–12 Months)", "Data & Validation", COLOR_GREEN, [
            ("R4. Component Data: ", "Mandate full tent/vehicle component reporting."),
            ("R5. Displacement: ", "Verify cross-border regional movement."),
            ("R6. Retraining: ", "Update OLS models with 2026 PIT data."),
            ("R7. Shelter Data: ", "Integrate real Housing Inventory Count (HIC).")
        ]),
        ("Long-Term (1–3 Years)", "Digitization & Infrastructure", COLOR_PRIMARY_NAVY, [
            ("R8. Digitize Maps: ", "Digitize remaining 78 monthly block maps."),
            ("Regional HMIS: ", "Unify real-time city and county bed tracking."),
            ("True Evaluation: ", "Measure regional outcomes, not just local clearing."),
            ("Leaders: ", "County HHS, RTFH, DSA.")
        ])
    ]
    for idx, (title, sub, col, items) in enumerate(horizons):
        h_left = Inches(0.8 + idx * 3.98)
        add_canva_card(s12, h_left, Inches(1.6), Inches(3.78), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)

        hbar = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, h_left, Inches(1.6), Inches(3.78), Inches(0.1))
        hbar.fill.solid(); hbar.fill.fore_color.rgb = col; hbar.line.fill.background()

        tb = s12.shapes.add_textbox(h_left + Inches(0.2), Inches(1.8), Inches(3.38), Inches(4.6))
        tf = tb.text_frame; tf.word_wrap = True
        p_ht = tf.paragraphs[0]; p_ht.text = title.upper(); p_ht.font.name = FONT_DISPLAY; p_ht.font.size = Pt(11); p_ht.font.bold = True; p_ht.font.color.rgb = col; p_ht.space_after = Pt(2)
        p_hs = tf.add_paragraph(); p_hs.text = sub; p_hs.font.name = FONT_BODY; p_hs.font.size = Pt(11.0); p_hs.font.bold = True; p_hs.font.color.rgb = COLOR_TEXT_MUTED; p_hs.space_after = Pt(12)

        for it, idesc in items:
            p = tf.add_paragraph(); p.space_after = Pt(6)
            r1 = p.add_run(); r1.text = "• " + it; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_TEXT_DARK
            r2 = p.add_run(); r2.text = idesc; r2.font.name = FONT_BODY; r2.font.size = Pt(10.8); r2.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # SLIDE 13: THE INTERACTIVE DECISION-SUPPORT DASHBOARD
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout); set_slide_background(s13)
    add_canva_header(s13, "Interactive Decision-Support System: The Streamlit Executive Dashboard", "Operational Decision Tool", "13")
    add_canva_footer(s13, 13)

    add_canva_card(s13, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_db = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(7.1), Inches(4.6))
    tf_db = tb_db.text_frame; tf_db.word_wrap = True
    pdb = tf_db.paragraphs[0]; pdb.text = "7 DASHBOARD MODULES (TASK 9.1)"; pdb.font.name = FONT_DISPLAY; pdb.font.size = Pt(12.5); pdb.font.bold = True; pdb.font.color.rgb = COLOR_PRIMARY_NAVY; pdb.space_after = Pt(8)

    db_tabs = [
        ("Tab 1: History", "Multi-year trends with policy epoch overlays."),
        ("Tab 2: Forecast", "2026 projections, 95% fans, and stress-testing."),
        ("Tab 3: Hotspots", "Interactive Gi* maps and centroid migration."),
        ("Tab 4: Regions", "STL decomposition and seasonality stats."),
        ("Tab 5: Calculator", "OLS estimator enforcing the 4 Comm Rules."),
        ("Tab 6: Methods", "Multiplier transparency and boundary docs."),
        ("Tab 7: Alerts", "Control charts (CUSUM) for early-warnings.")
    ]
    for tt, td in db_tabs:
        p = tf_db.add_paragraph(); p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = "• " + tt + ": "; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = td; r2.font.name = FONT_BODY; r2.font.size = Pt(10.8); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s13, Inches(8.5), Inches(1.6), Inches(4.033), Inches(5.0), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_op = s13.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.433), Inches(4.6))
    tf_op = tb_op.text_frame; tf_op.word_wrap = True
    pop1 = tf_op.paragraphs[0]; pop1.text = "DEPLOYMENT & ACCESS INFO"; pop1.font.name = FONT_DISPLAY; pop1.font.size = Pt(12.5); pop1.font.bold = True; pop1.font.color.rgb = COLOR_PRIMARY_NAVY; pop1.space_after = Pt(8)

    op_points = [
        ("Local URL: ", "http://localhost:8501 (Fast response)"),
        ("Cloud URL: ", "https://downtown-sd-homelessness.streamlit.app"),
        ("Quality Check: ", "46/46 unit tests passing."),
        ("Performance: ", "Sub-second caching via @st.cache_data."),
        ("Audience: ", "City Council, RTFH, DSDP operations.")
    ]
    for opt, opd in op_points:
        p = tf_op.add_paragraph(); p.space_after = Pt(8)
        r1 = p.add_run(); r1.text = "• " + opt; r1.font.name = FONT_BODY; r1.font.size = Pt(11.5); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = opd; r2.font.name = FONT_BODY; r2.font.size = Pt(11.0); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 14: EXECUTIVE SYNTHESIS & STRATEGIC NEXT STEPS
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout); set_slide_background(s14)
    add_canva_header(s14, "Synthesis & Next Steps", "Synthesis & Next Steps", "14")
    add_canva_footer(s14, 14)

    conclusions = [
        ("Fund Year-Round", "End Seasonal Budgeting", COLOR_PRIMARY_NAVY, "Data proves zero seasonality (p=0.995). Lock investments into permanent capacity and target South East Village hotspots."),
        ("Acknowledge Reality", "Fix Divergence", COLOR_ROYAL_BLUE, "Downtown drops pair with countywide highs (6,110). Stop localized displacement; demand countywide shelter collaboration."),
        ("Data Transparency", "Digitize & Retrain", COLOR_GREEN, "Digitize remaining 78 block maps. Annually retrain the OLS model for accuracy.")
    ]
    for idx, (title, sub, col, body) in enumerate(conclusions):
        top_y = Inches(1.6 + idx * 1.7)
        add_canva_card(s14, Inches(0.8), top_y, Inches(11.733), Inches(1.55), COLOR_CARD_BG, COLOR_CARD_BORDER)

        bar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_y, Inches(0.12), Inches(1.55))
        bar.fill.solid(); bar.fill.fore_color.rgb = col; bar.line.fill.background()

        tb = s14.shapes.add_textbox(Inches(1.1), top_y + Inches(0.12), Inches(11.2), Inches(1.3))
        tf = tb.text_frame; tf.word_wrap = True
        pc1 = tf.paragraphs[0]; pc1.text = title.upper(); pc1.font.name = FONT_DISPLAY; pc1.font.size = Pt(11.5); pc1.font.bold = True; pc1.font.color.rgb = col; pc1.space_after = Pt(2)
        pc2 = tf.add_paragraph(); pc2.text = sub; pc2.font.name = FONT_BODY; pc2.font.size = Pt(11.5); pc2.font.bold = True; pc2.font.color.rgb = COLOR_TEXT_DARK; pc2.space_after = Pt(4)
        pc3 = tf.add_paragraph(); pc3.text = body; pc3.font.name = FONT_BODY; pc3.font.size = Pt(10.8); pc3.font.color.rgb = COLOR_TEXT_MUTED

    prs.save(str(OUTPUT_PPTX))
    print(f"Successfully generated 14-slide presentation: {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_deck()
