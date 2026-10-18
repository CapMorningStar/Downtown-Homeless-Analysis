"""
Native PowerPoint Presentation Generator for Task 9.3: Strategic Recommendations & Slide Deck.
Downtown San Diego Homeless Population Analysis (Assignment 9)

Produces: Assignment9_StrategicSynthesis.pptx
Adheres strictly to the Canva 'Blue and White Modern Data Analytics' Design System (16:9 widescreen).
Features 12 production-grade executive slides with .callout speech hooks, KPI cards, tables,
high-DPI graphics, and strict compliance with The 4 Public Communication Rules and v3.0 Report outputs.
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

FONT_DISPLAY = "Trebuchet MS"  # Primary title font (Canva display alternative)
FONT_BODY    = "Segoe UI"      # Body and metadata font (Canva clean alternative)


def set_slide_background(slide):
    """Fill slide with canvas off-white background and attach smooth Fade slide transition."""
    from pptx.oxml import parse_xml
    transition_xml = parse_xml(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med" advClick="1">'
        '<p:fade thruBlk="0"/>'
        '</p:transition>'
    )
    slide._element.append(transition_xml)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_CANVAS_BG
    bg.line.fill.background()
    return bg


def add_canva_header(slide, title_text, category_text, slide_num_str):
    """Add standard Canva top header with category chip, title, and page badge."""
    # Top-right page badge
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

    # Vertical royal blue accent bar
    line_v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.06), Inches(0.82))
    line_v.fill.solid()
    line_v.fill.fore_color.rgb = COLOR_ROYAL_BLUE
    line_v.line.fill.background()

    # Category and title text
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.38), Inches(10.8), Inches(0.92))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_sub = tf.paragraphs[0]
    p_sub.text = category_text.upper()
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(11)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_ROYAL_BLUE
    p_sub.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_DISPLAY
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_NAVY

    # Horizontal divider rule
    line_h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.012))
    line_h.fill.solid()
    line_h.fill.fore_color.rgb = COLOR_CARD_BORDER
    line_h.line.fill.background()


def add_canva_footer(slide, current_page, total_pages=12):
    """Add standard bottom footer bar."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(9.5), Inches(0.35))
    tf_l = tb_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "Data Science Alliance • Downtown San Diego Homeless Population Analysis • Sources: DSDP Field Counts & RTFH PIT Census"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9)
    p_l.font.color.rgb = COLOR_TEXT_MUTED

    tb_right = slide.shapes.add_textbox(Inches(10.5), Inches(6.98), Inches(2.033), Inches(0.35))
    tf_r = tb_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.text = f"Slide {current_page:02d} of {total_pages:02d}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_PRIMARY_NAVY


def add_canva_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Add card container with rounded corners and clean borders."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    try:
        card.adjustments[0] = 0.025
    except Exception:
        pass
    return card


def add_callout_box(slide, left, top, width, height, title_text, body_text, bg_color=COLOR_ICE_TINT, border_color=COLOR_ROYAL_BLUE):
    """Add Ice-Blue callout speech hook box at top of narrative cards."""
    box = add_canva_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.08), width - Inches(0.24), height - Inches(0.16))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = title_text + " "
    r1.font.name = FONT_BODY
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_PRIMARY_NAVY
    r2 = p1.add_run()
    r2.text = body_text
    r2.font.name = FONT_BODY
    r2.font.size = Pt(10.0)
    r2.font.color.rgb = COLOR_TEXT_DARK
    return box


def add_image_fitted(slide, image_path, container_left, container_top, container_width, container_height):
    """Add high-DPI image fitted within bounding box preserving aspect ratio."""
    if not Path(image_path).exists():
        tb = slide.shapes.add_textbox(container_left, container_top, container_width, container_height)
        tb.text_frame.paragraphs[0].text = f"[Image Missing: {Path(image_path).name}]"
        return None

    with Image.open(image_path) as img:
        img_w, img_h = img.size
    aspect = img_w / img_h
    cont_aspect = container_width / container_height

    if aspect > cont_aspect:
        target_w = container_width
        target_h = container_width / aspect
        offset_x = Inches(0)
        offset_y = (container_height - target_h) / 2
    else:
        target_h = container_height
        target_w = container_height * aspect
        offset_y = Inches(0)
        offset_x = (container_width - target_w) / 2

    return slide.shapes.add_picture(
        str(image_path),
        container_left + offset_x,
        container_top + offset_y,
        target_w,
        target_h
    )


def add_formatted_table(slide, left, top, width, height, headers, rows, col_widths=None):
    """Add table styled with Canva colors."""
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height)
    table = table_shape.table

    if col_widths and len(col_widths) == len(headers):
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_NAVY
        tf = cell.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_BG
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if (row_idx % 2 == 0) else COLOR_CANVAS_BG
            tf = cell.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.text = str(cell_value)
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_DARK
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            if "Champion" in str(cell_value) or "XGBoost" in str(cell_value):
                p.font.bold = True
                p.font.color.rgb = COLOR_ROYAL_BLUE

    return table_shape


def build_deck():
    print(f"Initializing Presentation Builder: 12-Slide Executive Architecture...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =============================================================
    # SLIDE 1: TITLE SLIDE (Canva Executive Hero Style)
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    hero = add_canva_card(s1, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7), COLOR_CARD_BG, COLOR_CARD_BORDER)

    chip = add_canva_card(s1, Inches(1.6), Inches(1.4), Inches(4.8), Inches(0.42), COLOR_ICE_TINT, COLOR_SOFT_BLUE)
    tb_chip = s1.shapes.add_textbox(Inches(1.6), Inches(1.4), Inches(4.8), Inches(0.42))
    tf_c = tb_chip.text_frame; tf_c.margin_left = Inches(0.18); tf_c.margin_top = Inches(0.08)
    p_c = tf_c.paragraphs[0]; p_c.text = "DATA SCIENCE ALLIANCE • EXECUTIVE SYNTHESIS"; p_c.font.name = FONT_BODY; p_c.font.size = Pt(10.5); p_c.font.bold = True; p_c.font.color.rgb = COLOR_PRIMARY_NAVY

    tb_t = s1.shapes.add_textbox(Inches(1.6), Inches(2.05), Inches(10.0), Inches(2.3))
    tf_t = tb_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t1 = tf_t.paragraphs[0]; p_t1.text = "Downtown San Diego Unsheltered\nHomeless Population Analysis"; p_t1.font.name = FONT_DISPLAY; p_t1.font.size = Pt(34); p_t1.font.bold = True; p_t1.font.color.rgb = COLOR_PRIMARY_NAVY; p_t1.space_after = Pt(8)
    p_t2 = tf_t.add_paragraph(); p_t2.text = "Longitudinal Modeling, Spatial Dynamics & Macro Policy Governance (2017–2025)"; p_t2.font.name = FONT_BODY; p_t2.font.size = Pt(15); p_t2.font.bold = True; p_t2.font.color.rgb = COLOR_ROYAL_BLUE; p_t2.space_after = Pt(10)
    p_t3 = tf_t.add_paragraph(); p_t3.text = "Kyaw Soe Lwin | Data Science Alliance Lead Project Deliverable"; p_t3.font.name = FONT_BODY; p_t3.font.size = Pt(13); p_t3.font.color.rgb = COLOR_TEXT_MUTED

    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(4.7), Inches(10.0), Inches(0.015))
    div1.fill.solid(); div1.fill.fore_color.rgb = COLOR_CARD_BORDER; div1.line.fill.background()

    meta_items = [
        ("Longitudinal Scope", "9 Years • 108 Months (2017–2025)\n7 Downtown Neighborhoods Analyzed"),
        ("Dual Data Pipeline", "DSDP Clean & Safe Field Counts\n+ RTFH Countywide PIT Census"),
        ("Production Deliverables", "12-Slide Deck • 7-Tab Streamlit App\nStrategic Action Roadmap (R1–R8)")
    ]
    for idx, (m_label, m_val) in enumerate(meta_items):
        m_left = Inches(1.6 + idx * 3.4)
        tb_m = s1.shapes.add_textbox(m_left, Inches(4.9), Inches(3.1), Inches(1.3))
        tf_m = tb_m.text_frame; tf_m.word_wrap = True; tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
        p_ml = tf_m.paragraphs[0]; p_ml.text = m_label.upper(); p_ml.font.name = FONT_BODY; p_ml.font.size = Pt(9.5); p_ml.font.bold = True; p_ml.font.color.rgb = COLOR_ROYAL_BLUE; p_ml.space_after = Pt(2)
        p_mv = tf_m.add_paragraph(); p_mv.text = m_val; p_mv.font.name = FONT_BODY; p_mv.font.size = Pt(10.5); p_mv.font.color.rgb = COLOR_TEXT_DARK

    add_canva_footer(s1, 1, 12)

    # =============================================================
    # SLIDE 2: MACRO TRAJECTORY: 3 DISTINCT EPOCHS (2017–2025)
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout); set_slide_background(s2)
    add_canva_header(s2, "Macro Trajectory: Three Distinct Epochs Across 9 Years (2017–2025)", "Longitudinal Epidemiology", "02")
    add_canva_footer(s2, 2, 12)

    # 3 Floating KPI cards on top-left
    kpis_s2 = [
        ("529", "Series Low", "March 2020 (COVID trough)", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("2,103", "Series Peak", "May 2023 (Crisis peak)", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("851", "Jan 2025 Count", "−59.5% from peak (Stabilization)", COLOR_CARD_BG, COLOR_PRIMARY_NAVY, COLOR_TEXT_MUTED)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s2):
        c_left = Inches(0.8 + i * 1.55)
        add_canva_card(s2, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s2.shapes.add_textbox(c_left + Inches(0.08), Inches(1.56), Inches(1.3), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(20); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.0); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    # Left Narrative Card with Ice-Blue Speech Hook Callout Box
    add_canva_card(s2, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s2, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Downtown San Diego experienced 3 distinct epochs across 9 years—contraction, crisis peak, and policy stabilization—with 4 unpublished months in 2025.")

    tb_p2 = s2.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p2 = tb_p2.text_frame; tf_p2.word_wrap = True; tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0
    p2_bullets = [
        ("Epoch 1 (2017–2020): ", "Baseline contraction from 882 to all-time series low of 529 in March 2020 during initial COVID de-densification."),
        ("Epoch 2 (2021–2023): ", "Post-pandemic surge of +297%, peaking at 2,103 in May 2023 driven by evictions, inflation, and street encampments."),
        ("Epoch 3 (2024–2025): ", "Enforcement stabilization; Jan 2025 count dropped to 851 (−59.5% from peak), ending Dec 2025 at 985."),
        ("2025 Data Notice: ", "Jul, Aug, Oct, Nov unpublished by DSDP; handled with honest interpolation and explicit data gap indicators.")
    ]
    for b_title, b_desc in p2_bullets:
        p = tf_p2.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    # Right Chart Frame
    add_canva_card(s2, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s2, SLIDE_ASSETS / "task93_trajectory_9year.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 3: ADMINISTRATIVE FOOTPRINT ARTIFACT (+121 BLOCKS)
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout); set_slide_background(s3)
    add_canva_header(s3, "Measurement Validity: The 2022 Footprint Expansion Artifact", "Spatial Measurement", "03")
    add_canva_footer(s3, 3, 12)

    kpis_s3 = [
        ("+121", "Added Blocks", "October 2022 expansion (+46.4%)", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("32.8%", "Peak Wedge Share", "Jan 2023 (641 of 1,955 count)", COLOR_AMBER, COLOR_CARD_BG, COLOR_ICE_TINT),
        ("261 vs 382", "Dual Metrics", "Core vs Expanded boundary reporting", COLOR_CARD_BG, COLOR_PRIMARY_NAVY, COLOR_TEXT_MUTED)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s3):
        c_left = Inches(0.8 + i * 1.55)
        add_canva_card(s3, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s3.shapes.add_textbox(c_left + Inches(0.08), Inches(1.56), Inches(1.3), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(19); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.0); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    add_canva_card(s3, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s3, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Over 32% of the apparent 2023 surge was an administrative measurement artifact caused by expanding the count perimeter by 121 blocks.")

    tb_p3 = s3.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p3 = tb_p3.text_frame; tf_p3.word_wrap = True; tf_p3.margin_left = tf_p3.margin_top = tf_p3.margin_right = tf_p3.margin_bottom = 0
    p3_bullets = [
        ("Perimeter Expansion: ", "In Oct 2022, DSDP expanded its counting footprint from 261 to 382 blocks (+46.4%), absorbing perimeter highway zones."),
        ("Wedge Quantification: ", "In Jan 2023, the added 121 blocks contributed 641 of 1,955 total individuals (32.8% of the entire reported count)."),
        ("Persistent Effect: ", "Even in Jan 2025, the expansion wedge accounts for 84 of 847 spatial individuals (10.0% of total count)."),
        ("Policy Directive (R3): ", "City reporting must mandate dual-series metrics (Core 261 vs Expanded 382) to avoid false longitudinal claims.")
    ]
    for b_title, b_desc in p3_bullets:
        p = tf_p3.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s3, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s3, SLIDE_ASSETS / "task93_footprint_wedge.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 4: SEASONALITY QUANTIFIED (STL DECOMPOSITION)
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout); set_slide_background(s4)
    add_canva_header(s4, "Seasonality Quantified: Invariant Summer Peaks vs Policy Forces", "Temporal Decomposition", "04")
    add_canva_footer(s4, 4, 12)

    kpis_s4 = [
        ("August", "Seasonal Peak", "+9.4% above annual baseline", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("April", "Seasonal Trough", "−10.8% below annual baseline", COLOR_ROYAL_BLUE, COLOR_CARD_BG, COLOR_ICE_TINT),
        ("p = 0.995", "Kruskal-Wallis", "H = 2.66 (Not significant)", COLOR_CARD_BG, COLOR_PRIMARY_NAVY, COLOR_TEXT_MUTED)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s4):
        c_left = Inches(0.8 + i * 1.55)
        add_canva_card(s4, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s4.shapes.add_textbox(c_left + Inches(0.08), Inches(1.56), Inches(1.3), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(19); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.0); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    add_canva_card(s4, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s4, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Seasonal cycles peak in August (+9.4%) and trough in April (−10.8%), but non-parametric ANOVA (p=0.995) confirms policy regimes drive 90%+ of variance.")

    tb_p4 = s4.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p4 = tb_p4.text_frame; tf_p4.word_wrap = True; tf_p4.margin_left = tf_p4.margin_top = tf_p4.margin_right = tf_p4.margin_bottom = 0
    p4_bullets = [
        ("Additive Seasonal Swing: ", "STL decomposition reveals a consistent seasonal amplitude of ±110 individuals, peaking in warm summer months (July–August)."),
        ("Statistical Significance: ", "Kruskal-Wallis test across calendar months yields H = 2.66, p = 0.995 (11 d.f.), indicating seasonality is subordinate to macro trend."),
        ("Operational Implication: ", "Seasonal changes require flexible shelter surge beds in summer, but cannot explain multi-year hundred-person swings."),
        ("Strategic Outreach Window: ", "April spring trough represents the optimal intervention window before the annual summer influx begins.")
    ]
    for b_title, b_desc in p4_bullets:
        p = tf_p4.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s4, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s4, SLIDE_ASSETS / "chart2_clean_hd.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 5: STRUCTURAL BREAK CHRONOLOGY (4 REGIMES)
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout); set_slide_background(s5)
    add_canva_header(s5, "Chronology of Policy Regimes & Structural Breaks (2017–2025)", "Policy Intervention Timeline", "05")
    add_canva_footer(s5, 5, 12)

    # 4 Horizontal Policy Regime Cards (2x2 Grid)
    regimes = [
        ("REGIME 1: BASELINE & HEPATITIS A (2017–2019)",
         "Sanitation infrastructure & initial shelter tents",
         COLOR_ROYAL_BLUE,
         [("Hepatitis A Outbreak: ", "Emergency street power-washing and 3 bridge shelters opened."),
          ("Count Trajectory: ", "Gradual contraction from 882 to ~750 individuals."),
          ("Multiplier Change: ", "Transitioned tent multiplier from 2.0 to 1.75 in April 2017.")]),
        ("REGIME 2: COVID-19 EMERGENCY RESPONSE (2020)",
         "Mass congregate sheltering & de-densification",
         COLOR_TEAL,
         [("Operation Shelter to Home: ", "Convention Center sheltered up to 1,300 people."),
          ("Series Low Reached: ", "Street counts dropped to 529 in March 2020 trough."),
          ("HUD Waiver: ", "HUD granted count waivers in 2021; unsheltered census suspended.")]),
        ("REGIME 3: CRISIS REBOUND & SURGE (2021–2023)",
         "Post-COVID economic shocks & perimeter expansion",
         COLOR_AMBER,
         [("Convention Center Closes: ", "People returned to streets as emergency beds ended."),
          ("Historical Peak: ", "Count reached 2,103 in May 2023 (+297% from 2020 low)."),
          ("Footprint Added: ", "October 2022 added 121 blocks, adding 641 people in Jan 2023.")]),
        ("REGIME 4: CAMPING ORDINANCE & STABILIZATION (2024–2025)",
         "Enforcement, Safe Sleeping sites & displacement",
         COLOR_GREEN,
         [("Unsafe Camping Ordinance: ", "Enforced July 2023; sidewalk tents prohibited."),
          ("Downtown Drops: ", "Counts fell to 851 in Jan 2025 and 985 in Dec 2025."),
          ("Regional Divergence: ", "County unsheltered rose to 6,110 (2024); displacement reality.")])
    ]

    card_positions = [
        (Inches(0.8), Inches(1.5), Inches(5.7), Inches(2.4)),
        (Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.4)),
        (Inches(0.8), Inches(4.05), Inches(5.7), Inches(2.2)),
        (Inches(6.8), Inches(4.05), Inches(5.7), Inches(2.2))
    ]

    for idx, (title, sub, col, items) in enumerate(regimes):
        c_left, c_top, c_w, c_h = card_positions[idx]
        add_canva_card(s5, c_left, c_top, c_w, c_h, COLOR_CARD_BG, COLOR_CARD_BORDER)

        top_strip = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.08))
        top_strip.fill.solid(); top_strip.fill.fore_color.rgb = col; top_strip.line.fill.background()

        tb = s5.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.12), c_w - Inches(0.4), c_h - Inches(0.2))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]; p1.text = title; p1.font.name = FONT_DISPLAY; p1.font.size = Pt(10.5); p1.font.bold = True; p1.font.color.rgb = col
        p2 = tf.add_paragraph(); p2.text = sub; p2.font.name = FONT_BODY; p2.font.size = Pt(9.0); p2.font.bold = True; p2.font.color.rgb = COLOR_TEXT_MUTED; p2.space_after = Pt(4)

        for it, idesc in items:
            p = tf.add_paragraph(); p.space_after = Pt(2)
            r1 = p.add_run(); r1.text = "• " + it; r1.font.name = FONT_BODY; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = COLOR_TEXT_DARK
            r2 = p.add_run(); r2.text = idesc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.0); r2.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Synthesis Callout Box
    add_callout_box(s5, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.50), "Executive Insight:",
                    "Macro policy interventions create immediate spatial displacement rather than net exits from homelessness. Enforcement in one zone redistributes individuals across municipal borders.",
                    COLOR_ICE_TINT, COLOR_ROYAL_BLUE)

    # =============================================================
    # SLIDE 6: SPATIAL CONCENTRATION & 120M HOTSPOT MIGRATION (MERGED)
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout); set_slide_background(s6)
    add_canva_header(s6, "Spatial Concentration: 54% East Village Core & 120m SSE Migration", "Geospatial Clustering", "06")
    add_canva_footer(s6, 6, 12)

    # 2 Floating KPI cards on top-left
    kpis_s6 = [
        ("54.0%", "East Village Share", "Consistently hosts over half of downtown total", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("120.4 m", "Centroid Migration", "Bearing 160.1° SSE toward Imperial Ave corridor", COLOR_RED, COLOR_CARD_BG, COLOR_ICE_TINT)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s6):
        c_left = Inches(0.8 + i * 2.35)
        add_canva_card(s6, c_left, Inches(1.5), Inches(2.25), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s6.shapes.add_textbox(c_left + Inches(0.12), Inches(1.56), Inches(2.0), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(20); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.2); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    add_canva_card(s6, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s6, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Downtown homelessness is hyper-concentrated in East Village (54%), with the cluster centroid migrating 120m SSE toward Imperial Ave due to sidewalk enforcement.")

    tb_p6 = s6.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p6 = tb_p6.text_frame; tf_p6.word_wrap = True; tf_p6.margin_left = tf_p6.margin_top = tf_p6.margin_right = tf_p6.margin_bottom = 0
    p6_bullets = [
        ("Hyper-Concentration: ", "East Village accounts for 54.0% of all downtown unsheltered individuals. City Center ranks second at ~18%."),
        ("120m Centroid Shift: ", "Between 2018–2020 and 2022–2025, the weighted hotspot center shifted 120.4 meters SSE (160.1° bearing) toward Imperial Ave."),
        ("Top Persistent Hotspots: ", "100% of top 10 Getis-Ord Gi* clusters are in South East Village: 16th & Imperial (9/12 dates), I-5 SB & Imperial (8/12)."),
        ("Outreach Focus (R1): ", "Target mobile hygiene, medical vans, and outreach teams at 16th-17th & Imperial Ave corridor.")
    ]
    for b_title, b_desc in p6_bullets:
        p = tf_p6.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s6, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s6, SLIDE_ASSETS / "task93_hotspot_migration.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 7: MACHINE LEARNING 5-FOLD CV BENCHMARK
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout); set_slide_background(s7)
    add_canva_header(s7, "Machine Learning: 5-Fold Cross-Validation Benchmark", "Predictive Intelligence", "07")
    add_canva_footer(s7, 7, 12)

    # Left: Full Table Card
    add_canva_card(s7, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_t7 = s7.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(6.6), Inches(0.45))
    tb_t7.text_frame.paragraphs[0].text = "5-FOLD CROSS-VALIDATION ERROR COMPARISON"
    tb_t7.text_frame.paragraphs[0].font.name = FONT_DISPLAY; tb_t7.text_frame.paragraphs[0].font.size = Pt(11.5); tb_t7.text_frame.paragraphs[0].font.bold = True; tb_t7.text_frame.paragraphs[0].font.color.rgb = COLOR_PRIMARY_NAVY

    ml_headers = ["Model Architecture", "1-Month MAPE", "3-Month MAPE", "6-Month MAPE", "12-Month CV MAPE"]
    ml_rows = [
        ["SARIMA (ACF/PACF Grid)", "5.4% ± 4.1%", "14.3% ± 10.3%", "24.7% ± 20.9%", "39.6% ± 35.5%"],
        ["Holt-Winters Exp Smooth", "13.0% ± 9.2%", "17.6% ± 10.4%", "25.2% ± 18.2%", "38.4% ± 28.5%"],
        ["XGBoost (Champion)", "14.0% ± 8.9%", "19.9% ± 14.8%", "26.7% ± 18.5%", "38.3% ± 26.0%"],
        ["Naive Seasonal (t−12)", "39.5% ± 31.9%", "40.1% ± 31.3%", "48.5% ± 35.4%", "51.7% ± 24.5%"],
        ["Prophet (Changepoints)", "42.9% ± 26.0%", "42.7% ± 26.0%", "51.3% ± 31.9%", "64.2% ± 35.4%"],
    ]
    add_formatted_table(s7, Inches(1.0), Inches(2.2), Inches(6.6), Inches(4.3), ml_headers, ml_rows,
                        [Inches(1.8), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)])

    # Right: Champion Model & Policy Takeaway Card
    add_canva_card(s7, Inches(8.0), Inches(1.5), Inches(4.533), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s7, Inches(8.2), Inches(1.7), Inches(4.133), Inches(1.15), "Production Winner:",
                    "XGBoost is our champion production model with 38.3% 12-month CV MAPE and 8.5% 2025 hold-out error, outperforming Prophet by over 25 percentage points.")

    tb_r7 = s7.shapes.add_textbox(Inches(8.2), Inches(3.0), Inches(4.133), Inches(3.5))
    tf_r7 = tb_r7.text_frame; tf_r7.word_wrap = True; tf_r7.margin_left = tf_r7.margin_top = tf_r7.margin_right = tf_r7.margin_bottom = 0
    p7_bullets = [
        ("Short vs Long Horizons: ", "SARIMA leads at 1-month (5.4% MAPE); XGBoost matches Holt-Winters at 12-months (38.3%) while exhibiting tighter variance."),
        ("Hold-Out Validation: ", "On 2025 out-of-time hold-out months, XGBoost achieved 8.5% error, confirming robust generalization under policy shifts."),
        ("Prophet Vulnerability: ", "Prophet failed severely (64.2% MAPE) because automated linear changepoints missed the steep post-ordinance drop."),
        ("Deployment Pipeline: ", "XGBoost embedded into Tab 2 of Streamlit application with automatic quarterly retraining cues.")
    ]
    for b_title, b_desc in p7_bullets:
        p = tf_r7.add_paragraph(); p.space_after = Pt(5)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(10.0); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_TEXT_DARK

    # =============================================================
    # SLIDE 8: 2026 PROSPECTIVE OUTLOOK & STRESS SCENARIOS
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout); set_slide_background(s8)
    add_canva_header(s8, "2026 Forward Outlook: 12-Month Projections & Stress Scenarios", "Prospective Forecasting", "08")
    add_canva_footer(s8, 8, 12)

    kpis_s8 = [
        ("816–896", "Baseline Forecast", "Expected monthly range throughout 2026", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("~675", "Optimistic Scenario", "−24% under accelerated housing exits", COLOR_GREEN, COLOR_CARD_BG, COLOR_ICE_TINT),
        ("~1,123", "Pessimistic Scenario", "+26% under shelter capacity contraction", COLOR_RED, COLOR_CARD_BG, COLOR_ICE_TINT)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s8):
        c_left = Inches(0.8 + i * 1.55)
        add_canva_card(s8, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s8.shapes.add_textbox(c_left + Inches(0.08), Inches(1.56), Inches(1.3), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(18); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.0); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    add_canva_card(s8, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s8, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Baseline 2026 forecast projects Downtown unsheltered counts to remain range-bound at 816–896 individuals, but city leaders must budget for the 675–1,123 stress-test envelope.")

    tb_p8 = s8.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p8 = tb_p8.text_frame; tf_p8.word_wrap = True; tf_p8.margin_left = tf_p8.margin_top = tf_p8.margin_right = tf_p8.margin_bottom = 0
    p8_bullets = [
        ("Stable Baseline: ", "Under current enforcement, downtown counts remain flat at ~850 individuals throughout 2026 (Nov peak: 896; Dec M12: 888)."),
        ("Stress-Test Envelope: ", "Optimistic (~675, −24%) and Pessimistic (~1,123, +26%) scenarios model plausible policy and economic variations."),
        ("Uncertainty Bounds: ", "80% PI [660–1,116] and 95% PI [539–1,237] at M12 account for residual volatility and seasonal swings."),
        ("Budget Directive (R2): ", "Municipal budgets must plan across the 675–1,123 envelope rather than relying on a single static number.")
    ]
    for b_title, b_desc in p8_bullets:
        p = tf_p8.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s8, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s8, SLIDE_ASSETS / "task93_forecast_2026.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 9: REGIONAL DIVERGENCE & THE DISPLACEMENT PARADOX
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout); set_slide_background(s9)
    add_canva_header(s9, "Regional Divergence: Downtown Drops vs Countywide Unsheltered Highs", "Regional Policy Dynamics", "09")
    add_canva_footer(s9, 9, 12)

    kpis_s9 = [
        ("14.9%", "Downtown Share", "Fell from 37.5% peak in 2023", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
        ("6,110", "County Peak (2024)", "All-time series record unsheltered count", COLOR_RED, COLOR_CARD_BG, COLOR_ICE_TINT),
        ("5,714", "County PIT (2025)", "High regional baseline remains", COLOR_CARD_BG, COLOR_PRIMARY_NAVY, COLOR_TEXT_MUTED)
    ]
    for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s9):
        c_left = Inches(0.8 + i * 1.55)
        add_canva_card(s9, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_col, COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
        tb_k = s9.shapes.add_textbox(c_left + Inches(0.08), Inches(1.56), Inches(1.3), Inches(1.0))
        tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(19); pk1.font.bold = True; pk1.font.color.rgb = txt_col
        pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.0); pk2.font.bold = True; pk2.font.color.rgb = txt_col
        pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.2); pk3.font.color.rgb = sub_col

    add_canva_card(s9, Inches(0.8), Inches(2.8), Inches(4.6), Inches(3.95), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_callout_box(s9, Inches(0.95), Inches(2.95), Inches(4.3), Inches(0.95), "Key Takeaway:",
                    "Downtown counts dropped 56%, but County unsheltered hit an all-time record of 6,110—proving Downtown enforcement displaced people into surrounding jurisdictions.")

    tb_p9 = s9.shapes.add_textbox(Inches(0.95), Inches(4.05), Inches(4.3), Inches(2.6))
    tf_p9 = tb_p9.text_frame; tf_p9.word_wrap = True; tf_p9.margin_left = tf_p9.margin_top = tf_p9.margin_right = tf_p9.margin_bottom = 0
    p9_bullets = [
        ("The Regional Paradox: ", "Downtown Jan count plunged from 1,939 to 851 (−56%), yet countywide unsheltered homelessness reached historical record highs (6,110 in 2024, 5,714 in 2025)."),
        ("Share Collapse: ", "Downtown's share of county unsheltered collapsed from 37.5% in 2023 to 14.9% in 2025."),
        ("Displacement Dynamics: ", "Sidewalk clearance displaced encampments along trolley corridors, canyon edges, and into neighbouring East/South County jurisdictions."),
        ("Evaluation Caveat: ", "Macro divergence is proven by paired data; tracking individual migration requires unified HMIS data linkage (R5).")
    ]
    for b_title, b_desc in p9_bullets:
        p = tf_p9.add_paragraph(); p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = b_desc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_DARK

    add_canva_card(s9, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s9, SLIDE_ASSETS / "task93_regional_divergence.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.95))

    # =============================================================
    # SLIDE 10: MACRO OLS MODEL & THE 4 PUBLIC COMMUNICATION RULES
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout); set_slide_background(s10)
    add_canva_header(s10, "Macro Econometric Model & The 4 Public Communication Rules", "Macro Econometrics & Governance", "10")
    add_canva_footer(s10, 10, 12)

    # Left: The 4 Rules Stacked Cards Container
    add_canva_card(s10, Inches(0.8), Inches(1.5), Inches(4.8), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_rules_h = s10.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(4.4), Inches(0.4))
    tb_rules_h.text_frame.paragraphs[0].text = "THE 4 MANDATORY PUBLIC COMMUNICATION RULES"
    tb_rules_h.text_frame.paragraphs[0].font.name = FONT_DISPLAY; tb_rules_h.text_frame.paragraphs[0].font.size = Pt(11); tb_rules_h.text_frame.paragraphs[0].font.bold = True; tb_rules_h.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    rule_items = [
        ("Rule 1: Eliminate False Precision", "Never quote raw single points (e.g. '5,921'). Claiming exact single-person precision with n=8 data points destroys public credibility.", COLOR_RED),
        ("Rule 2: Mandate Rounding to 100", "Always report headline estimates rounded to the nearest hundred: quote 'about 5,900 individuals'.", COLOR_AMBER),
        ("Rule 3: Always State 95% Interval", "Every point estimate must be paired with calibrated Student's t range: '5,900 [3,900 to 8,000]' (margin of error ±2,050 / ±35%).", COLOR_GREEN),
        ("Rule 4: Disclose Policy Regime", "State model assumptions: Y = 4,513 + 0.186X + 1,225*D_post. True fit is R² = 0.504 (0.964 is ANOVA effect size η², not R²).", COLOR_ROYAL_BLUE)
    ]

    for idx, (rt, rd, col) in enumerate(rule_items):
        r_top = Inches(2.1 + idx * 1.12)
        add_canva_card(s10, Inches(1.0), r_top, Inches(4.4), Inches(1.02), COLOR_CANVAS_BG, COLOR_CARD_BORDER)
        badge = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), r_top, Inches(0.08), Inches(1.02))
        badge.fill.solid(); badge.fill.fore_color.rgb = col; badge.line.fill.background()

        tb = s10.shapes.add_textbox(Inches(1.18), r_top + Inches(0.06), Inches(4.15), Inches(0.9))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p1 = tf.paragraphs[0]; p1.text = rt; p1.font.name = FONT_DISPLAY; p1.font.size = Pt(10.0); p1.font.bold = True; p1.font.color.rgb = col; p1.space_after = Pt(2)
        p2 = tf.add_paragraph(); p2.text = rd; p2.font.name = FONT_BODY; p2.font.size = Pt(8.8); p2.font.color.rgb = COLOR_TEXT_DARK

    # Right: High-Resolution 2-Panel OLS Figure
    add_canva_card(s10, Inches(5.8), Inches(1.5), Inches(6.733), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    add_image_fitted(s10, SLIDE_ASSETS / "task93_county_ols_intervals.png", Inches(5.95), Inches(1.65), Inches(6.433), Inches(4.95))

    # =============================================================
    # SLIDE 11: MUNICIPAL POLICY ACTION ROADMAP (R1–R8)
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout); set_slide_background(s11)
    add_canva_header(s11, "Municipal Policy Action Roadmap: Recommendations (R1–R8)", "Strategic Recommendations", "11")
    add_canva_footer(s11, 11, 12)

    horizons = [
        ("Immediate (0–3 Months)", "Outreach, Standards & Boundaries", COLOR_ROYAL_BLUE, [
            ("R1. Persistent Hotspot Surge: ", "Deploy mobile hygiene, medical vans, and outreach directly to 16th-17th & Imperial corridor."),
            ("R2. Mandate Range Planning: ", "Enforce The 4 Communication Rules (5,900 [3,900–8,000]) across all municipal reports and budget allocations."),
            ("R3. Disclose Footprint Wedge: ", "Require dual reporting (Core 261 vs Expanded 382 blocks) to maintain longitudinal data integrity.")
        ]),
        ("Medium-Term (6–12 Months)", "Data Rigor & Regional Audits", COLOR_GREEN, [
            ("R4. Component Sub-Totals: ", "Restore separate tent, vehicle, and individual street count breakdowns in monthly DSDP reports."),
            ("R5. Displacement Tracking: ", "Launch joint City-County surveillance along transit corridors, riverbeds, and unincorporated areas."),
            ("R6. Retrain OLS Estimators: ", "Update regression coefficients with incoming 2026 RTFH Point-in-Time benchmark counts."),
            ("R7. Shelter Bed Integration: ", "Incorporate real-time Housing Inventory Count (HIC) bed occupancy into monthly analytics.")
        ]),
        ("Long-Term (1–3 Years)", "System Digitization & Governance", COLOR_PRIMARY_NAVY, [
            ("R8. Complete Map Digitization: ", "Digitize remaining 78 historical block-level PDF tally maps (2017–2022) to establish block-level panel."),
            ("Unified Regional HMIS: ", "Link City DSDP field counts with County Homeless Management Information System (HMIS) records."),
            ("True Regional Evaluation: ", "Measure net permanent housing exits rather than local sidewalk clearance.")
        ])
    ]

    for idx, (title, sub, col, items) in enumerate(horizons):
        h_left = Inches(0.8 + idx * 3.98)
        add_canva_card(s11, h_left, Inches(1.5), Inches(3.78), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)

        hbar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, h_left, Inches(1.5), Inches(3.78), Inches(0.1))
        hbar.fill.solid(); hbar.fill.fore_color.rgb = col; hbar.line.fill.background()

        tb = s11.shapes.add_textbox(h_left + Inches(0.2), Inches(1.75), Inches(3.38), Inches(4.8))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_ht = tf.paragraphs[0]; p_ht.text = title.upper(); p_ht.font.name = FONT_DISPLAY; p_ht.font.size = Pt(11); p_ht.font.bold = True; p_ht.font.color.rgb = col; p_ht.space_after = Pt(2)
        p_hs = tf.add_paragraph(); p_hs.text = sub; p_hs.font.name = FONT_BODY; p_hs.font.size = Pt(9.5); p_hs.font.bold = True; p_hs.font.color.rgb = COLOR_TEXT_MUTED; p_hs.space_after = Pt(10)

        for it, idesc in items:
            p = tf.add_paragraph(); p.space_after = Pt(6)
            r1 = p.add_run(); r1.text = "• " + it; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_TEXT_DARK
            r2 = p.add_run(); r2.text = idesc; r2.font.name = FONT_BODY; r2.font.size = Pt(9.2); r2.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # SLIDE 12: INTERACTIVE DECISION SUPPORT & STRATEGIC SYNTHESIS (MERGED)
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout); set_slide_background(s12)
    add_canva_header(s12, "Interactive Decision-Support Tool & Executive Synthesis", "Operational Tool & Synthesis", "12")
    add_canva_footer(s12, 12, 12)

    # Left: 7-Tab Streamlit Dashboard Architecture Card
    add_canva_card(s12, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_db = s12.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf_db = tb_db.text_frame; tf_db.word_wrap = True; tf_db.margin_left = tf_db.margin_top = tf_db.margin_right = tf_db.margin_bottom = 0

    pdb = tf_db.paragraphs[0]; pdb.text = "7 DECISION-SUPPORT MODULES (STREAMLIT APP)"; pdb.font.name = FONT_DISPLAY; pdb.font.size = Pt(12); pdb.font.bold = True; pdb.font.color.rgb = COLOR_PRIMARY_NAVY; pdb.space_after = Pt(8)

    db_tabs = [
        ("Tab 1: History", "Multi-year trajectory with policy epoch overlays (2017–2025)."),
        ("Tab 2: Forecast", "XGBoost 12-month projections, 95% fans & scenario stress-testing."),
        ("Tab 3: Hotspots", "Interactive Getis-Ord Gi* cluster maps and centroid migration vector."),
        ("Tab 4: Seasonality", "STL decomposition with month-of-year seasonal indices."),
        ("Tab 5: Calculator", "County macro estimator strictly enforcing The 4 Communication Rules."),
        ("Tab 6: Methods", "Multiplier transparency, perimeter changes, and documentation."),
        ("Tab 7: Alerts", "Anomaly surveillance matrix and CUSUM early-warning monitoring.")
    ]
    for tt, td in db_tabs:
        p = tf_db.add_paragraph(); p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = "• " + tt + ": "; r1.font.name = FONT_BODY; r1.font.size = Pt(9.8); r1.font.bold = True; r1.font.color.rgb = COLOR_ROYAL_BLUE
        r2 = p.add_run(); r2.text = td; r2.font.name = FONT_BODY; r2.font.size = Pt(9.0); r2.font.color.rgb = COLOR_TEXT_DARK

    p_dep = tf_db.add_paragraph(); p_dep.space_before = Pt(8); p_dep.text = "DEPLOYMENT ACCESS & SYSTEM HEALTH"; p_dep.font.name = FONT_DISPLAY; p_dep.font.size = Pt(10.5); p_dep.font.bold = True; p_dep.font.color.rgb = COLOR_GREEN
    p_d1 = tf_db.add_paragraph(); p_d1.text = "• Local Server: http://localhost:8501 (Instant response)"; p_d1.font.name = FONT_BODY; p_d1.font.size = Pt(9.0); p_d1.font.color.rgb = COLOR_TEXT_DARK
    p_d2 = tf_db.add_paragraph(); p_d2.text = "• Cloud URL: https://downtown-sd-homelessness.streamlit.app"; p_d2.font.name = FONT_BODY; p_d2.font.size = Pt(9.0); p_d2.font.color.rgb = COLOR_TEXT_DARK
    p_d3 = tf_db.add_paragraph(); p_d3.text = "• Test Suite: 46/46 unit tests passing • Sub-second @st.cache_data"; p_d3.font.name = FONT_BODY; p_d3.font.size = Pt(9.0); p_d3.font.color.rgb = COLOR_TEXT_MUTED

    # Right: 3 Synthesis Pillars & Live Demo Cue Card
    add_canva_card(s12, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.25), COLOR_CARD_BG, COLOR_CARD_BORDER)
    tb_syn = s12.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.8))
    tf_syn = tb_syn.text_frame; tf_syn.word_wrap = True; tf_syn.margin_left = tf_syn.margin_top = tf_syn.margin_right = tf_syn.margin_bottom = 0

    psyn = tf_syn.paragraphs[0]; psyn.text = "EXECUTIVE SYNTHESIS & CORE TAKEAWAYS"; psyn.font.name = FONT_DISPLAY; psyn.font.size = Pt(12); psyn.font.bold = True; psyn.font.color.rgb = COLOR_PRIMARY_NAVY; psyn.space_after = Pt(8)

    pillars = [
        ("Pillar 1: Regional Displacement Reality", "Downtown counts dropped to 851, but county unsheltered reached record highs (6,110). Enforcement redistributes individuals; genuine reduction requires regional shelter and permanent supportive housing capacity.", COLOR_ROYAL_BLUE),
        ("Pillar 2: Honest Uncertainty Quantification", "Point estimates without intervals mislead public officials. Mandating Rule 2 (5,900) and Rule 3 ([3,900 to 8,000]) protects municipal credibility and anchors realistic budgeting.", COLOR_AMBER),
        ("Pillar 3: Unified Data Infrastructure", "Measuring progress requires linking street counts with shelter bed inventories, component breakdowns, and HMIS tracking to measure human exits rather than block clearances.", COLOR_GREEN)
    ]

    for pt, pd, pcol in pillars:
        p_t = tf_syn.add_paragraph(); p_t.space_before = Pt(4); p_t.text = pt; p_t.font.name = FONT_DISPLAY; p_t.font.size = Pt(10.5); p_t.font.bold = True; p_t.font.color.rgb = pcol
        p_d = tf_syn.add_paragraph(); p_d.text = pd; p_d.font.name = FONT_BODY; p_d.font.size = Pt(9.2); p_d.font.color.rgb = COLOR_TEXT_DARK

    # Bottom Live Demo Banner Box
    add_callout_box(s12, Inches(7.0), Inches(5.95), Inches(5.333), Inches(0.65), "Discussion & Q&A:",
                    "Executive presentation concluded. Ready for scenario walk-throughs, stakeholder questions, and live Streamlit dashboard demonstration.",
                    COLOR_ICE_TINT, COLOR_ROYAL_BLUE)

    prs.save(str(OUTPUT_PPTX))
    print(f"✅ Generated 12-Slide Native Presentation: {OUTPUT_PPTX} ({OUTPUT_PPTX.stat().st_size / 1024:,.1f} KB)")


if __name__ == "__main__":
    build_deck()
