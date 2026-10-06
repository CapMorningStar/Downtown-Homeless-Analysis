import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# -------------------------------------------------------------
# Canva Template Design System: "Blue and White Modern Data Analytics" (EAG_ft-JLCA)
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
COLOR_RED          = RGBColor(220, 38, 38)    # #DC2626
COLOR_GREEN        = RGBColor(5, 150, 105)    # #059669
COLOR_AMBER        = RGBColor(217, 119, 6)    # #D97706

FONT_DISPLAY = "Trebuchet MS"  # Office fallback for Bricolage Grotesque
FONT_BODY    = "Segoe UI"      # Office fallback for Poppins

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_CANVAS_BG
    bg.line.fill.background()
    return bg

def add_canva_header(slide, title_text, category_text, slide_num_str):
    # 1. Top-Right Slide Number Badge (Flush at top-right)
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.133), Inches(0), Inches(1.2), Inches(0.85))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_PRIMARY_NAVY
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = slide_num_str
    p_b.font.name = FONT_DISPLAY
    p_b.font.size = Pt(26)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_CARD_BG
    p_b.alignment = PP_ALIGN.CENTER
    
    # 2. Vertical Accent Line
    line_v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.06), Inches(0.82))
    line_v.fill.solid()
    line_v.fill.fore_color.rgb = COLOR_ROYAL_BLUE
    line_v.line.fill.background()

    # 3. Header Title & Subtitle Box
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.38), Inches(10.8), Inches(0.95))
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
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_NAVY

    # Subtle horizontal line below header
    line_h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.012))
    line_h.fill.solid()
    line_h.fill.fore_color.rgb = COLOR_CARD_BORDER
    line_h.line.fill.background()

def add_canva_footer(slide, current_page, total_pages=8):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(9.5), Inches(0.35))
    tf_l = tb_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "Data Science Alliance • Downtown San Diego Homeless Population Analysis • Source: DSDP Monthly Counts (2017–2025)"
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
    return slide.shapes.add_picture(image_path, container_left + offset_x, container_top + offset_y, target_w, target_h)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# =============================================================
# SLIDE 1: TITLE SLIDE (Canva Style)
# =============================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Large Hero Card Container
hero = add_canva_card(s1, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7), bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

# Top Left Category Chip (Canva Pill)
chip = add_canva_card(s1, Inches(1.6), Inches(1.5), Inches(4.5), Inches(0.42), bg_color=COLOR_ICE_TINT, border_color=COLOR_SOFT_BLUE)
tb_chip = s1.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(4.5), Inches(0.42))
tf_c = tb_chip.text_frame
tf_c.margin_left = Inches(0.18); tf_c.margin_top = Inches(0.08)
p_c = tf_c.paragraphs[0]
p_c.text = "DATA SCIENCE ALLIANCE • TASK 2.3 CHECK-IN"
p_c.font.name = FONT_BODY
p_c.font.size = Pt(10)
p_c.font.bold = True
p_c.font.color.rgb = COLOR_PRIMARY_NAVY

# Title & Subtitle
tb_t = s1.shapes.add_textbox(Inches(1.6), Inches(2.2), Inches(10.0), Inches(2.2))
tf_t = tb_t.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
p_t1 = tf_t.paragraphs[0]
p_t1.text = "Downtown San Diego Unsheltered\nHomeless Population: EDA Findings"
p_t1.font.name = FONT_DISPLAY
p_t1.font.size = Pt(36)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_PRIMARY_NAVY
p_t1.space_after = Pt(14)

p_t2 = tf_t.add_paragraph()
p_t2.text = "Kyaw Soe Lwin | Data Science Alliance | 2017–2025"
p_t2.font.name = FONT_BODY
p_t2.font.size = Pt(17)
p_t2.font.bold = True
p_t2.font.color.rgb = COLOR_ROYAL_BLUE

# Horizontal divider rule
div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(4.7), Inches(10.0), Inches(0.015))
div1.fill.solid(); div1.fill.fore_color.rgb = COLOR_CARD_BORDER; div1.line.fill.background()

# 3 Metadata blocks
meta_items = [
    ("Source Data", "Downtown San Diego Partnership (DSDP) Clean & Safe monthly counts"),
    ("Longitudinal Scope", "2017–2025 (8 full & partial calendar years, 7 downtown neighborhoods)"),
    ("Analysis Focus", "Overall trajectory, seasonality, COVID dip, methodology & spatial dynamics")
]
for idx, (m_label, m_val) in enumerate(meta_items):
    m_left = Inches(1.6 + idx * 3.4)
    tb_m = s1.shapes.add_textbox(m_left, Inches(4.9), Inches(3.1), Inches(1.3))
    tf_m = tb_m.text_frame; tf_m.word_wrap = True; tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
    p_ml = tf_m.paragraphs[0]; p_ml.text = m_label.upper(); p_ml.font.name = FONT_BODY; p_ml.font.size = Pt(9.5); p_ml.font.bold = True; p_ml.font.color.rgb = COLOR_ROYAL_BLUE; p_ml.space_after = Pt(2)
    p_mv = tf_m.add_paragraph(); p_mv.text = m_val; p_mv.font.name = FONT_BODY; p_mv.font.size = Pt(10.5); p_mv.font.color.rgb = COLOR_TEXT_DARK

add_canva_footer(s1, 1, 8)

# =============================================================
# SLIDE 2: OVERALL TREND
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_canva_header(s2, "Overall Longitudinal Trend: Three Distinct Phases (2017–2025)", "Longitudinal Analysis", "02")

# 3 Floating KPI Stat Cards (Canva Style)
kpis_s2 = [
    ("529", "Series Low", "March 2020 (COVID trough)", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
    ("2,103", "Series Peak", "May 2023 (Rebound peak)", COLOR_PRIMARY_NAVY, COLOR_CARD_BG, COLOR_SOFT_BLUE),
    ("156.4", "Grand Mean", "Per neighborhood-month", COLOR_CARD_BG, COLOR_PRIMARY_NAVY, COLOR_TEXT_MUTED)
]
for i, (val, lbl, sub, bg_col, txt_col, sub_col) in enumerate(kpis_s2):
    c_left = Inches(0.8 + i * 1.55)
    card_kpi = add_canva_card(s2, c_left, Inches(1.5), Inches(1.45), Inches(1.15), bg_color=bg_col, border_color=COLOR_CARD_BORDER if bg_col == COLOR_CARD_BG else None)
    tb_k = s2.shapes.add_textbox(c_left + Inches(0.08), Inches(1.58), Inches(1.3), Inches(1.0))
    tf_k = tb_k.text_frame; tf_k.word_wrap = True; tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    
    pk1 = tf_k.paragraphs[0]; pk1.text = val; pk1.font.name = FONT_DISPLAY; pk1.font.size = Pt(21); pk1.font.bold = True; pk1.font.color.rgb = txt_col
    pk2 = tf_k.add_paragraph(); pk2.text = lbl.upper(); pk2.font.name = FONT_BODY; pk2.font.size = Pt(8.5); pk2.font.bold = True; pk2.font.color.rgb = txt_col
    pk3 = tf_k.add_paragraph(); pk3.text = sub; pk3.font.name = FONT_BODY; pk3.font.size = Pt(7.5); pk3.font.color.rgb = sub_col

# Left Side Narrative Card: Three Phases
card_phases = add_canva_card(s2, Inches(0.8), Inches(3.0), Inches(4.9), Inches(3.75), bg_color=COLOR_CARD_BG)
tb_phases = s2.shapes.add_textbox(Inches(1.0), Inches(3.15), Inches(4.15), Inches(3.45))
tf_p = tb_phases.text_frame; tf_p.word_wrap = True; tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

p_h = tf_p.paragraphs[0]; p_h.text = "Trajectory Overview: Three Clear Phases"; p_h.font.name = FONT_DISPLAY; p_h.font.size = Pt(13); p_h.font.bold = True; p_h.font.color.rgb = COLOR_PRIMARY_NAVY; p_h.space_after = Pt(6)

phases_data = [
    ("2017–2020 Decline", "Annual average fell from 176.31 to 109.02 (~-38% cumulative drop). Year-over-year changes: -20.31% (2018), -3.87% (2019), and -19.29% (2020)."),
    ("2021–2023 Rebound & Peak", "Counts rebounded sharply: +25.85% (2021) and +57.55% (2022), reaching an annual average of 223.30 in 2023 — more than double the 2020 trough."),
    ("2024–2025 Pullback & Stabilization", "A steep -43.26% drop in 2024 brought the annual average down to 126.71; 2025 remained roughly flat (-2.56%) at 123.47.")
]
for p_title, p_desc in phases_data:
    p_t = tf_p.add_paragraph(); p_t.text = f"• {p_title}:"; p_t.font.name = FONT_BODY; p_t.font.size = Pt(10); p_t.font.bold = True; p_t.font.color.rgb = COLOR_ROYAL_BLUE
    p_d = tf_p.add_paragraph(); p_d.text = f"  {p_desc}"; p_d.font.name = FONT_BODY; p_d.font.size = Pt(9.2); p_d.font.color.rgb = COLOR_TEXT_DARK; p_d.space_after = Pt(5)

# Right: Chart Card Frame
chart_card_s2 = add_canva_card(s2, Inches(5.6), Inches(1.5), Inches(6.933), Inches(5.25), bg_color=COLOR_CARD_BG)
add_image_fitted(s2, "slide_assets/chart1_clean_hd.png", Inches(5.75), Inches(1.65), Inches(6.633), Inches(4.9))

add_canva_footer(s2, 2, 8)

# =============================================================
# SLIDE 3: SEASONALITY (QUANTIFIED)
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_canva_header(s3, "Calendar-Month Seasonality: Modest Variance vs. Annual Swings", "Seasonal Analysis", "03")

card_season = add_canva_card(s3, Inches(0.8), Inches(1.5), Inches(4.7), Inches(5.25), bg_color=COLOR_CARD_BG)
tb_s3 = s3.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(4.2), Inches(4.85))
tf_s3 = tb_s3.text_frame; tf_s3.word_wrap = True; tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0

p_s3_h = tf_s3.paragraphs[0]; p_s3_h.text = "Quantifying Calendar Seasonality"; p_s3_h.font.name = FONT_DISPLAY; p_s3_h.font.size = Pt(13.5); p_s3_h.font.bold = True; p_s3_h.font.color.rgb = COLOR_PRIMARY_NAVY; p_s3_h.space_after = Pt(6)

# Pill takeaway (Canva callout style)
p_s3_callout = tf_s3.add_paragraph()
p_s3_callout.text = "Key Takeaway: Which YEAR a month falls in matters far more than which calendar month it is."
p_s3_callout.font.name = FONT_BODY; p_s3_callout.font.size = Pt(10.5); p_s3_callout.font.bold = True; p_s3_callout.font.color.rgb = COLOR_ROYAL_BLUE; p_s3_callout.space_after = Pt(8)

s3_bullets = [
    ("Modest Range of Deviation", "No single calendar month deviates by more than ~5% from the grand mean (156.44). The peak-to-trough spread is only ~8.1 percentage points."),
    ("Top 3 Highest Months", "Feb (+3.2%, 161.76), Aug (+3.1%, 161.61), and May (+2.6%, 160.93)."),
    ("Top 3 Lowest Months", "Mar (-5.2%, 148.67), Sep (-2.0%, 153.63), Nov (-2.1%, 153.43) [Apr: -2.1%, 153.53]."),
    ("Large Residual Variance", "Month-to-month standard deviations (187–216) dwarf monthly mean differences, confirming macro annual shocks overpower calendar cycles."),
    ("East Village Sub-Pattern", "East Village diverges from citywide rhythm: peaks in Jul–Aug (~601–604) and dips in spring (Mar–Apr, ~509).")
]
for b_head, b_txt in s3_bullets:
    p_bhead = tf_s3.add_paragraph(); p_bhead.text = f"• {b_head}:"; p_bhead.font.name = FONT_BODY; p_bhead.font.size = Pt(10); p_bhead.font.bold = True; p_bhead.font.color.rgb = COLOR_ROYAL_BLUE
    p_btxt = tf_s3.add_paragraph(); p_btxt.text = f"  {b_txt}"; p_btxt.font.name = FONT_BODY; p_btxt.font.size = Pt(9.2); p_btxt.font.color.rgb = COLOR_TEXT_DARK; p_btxt.space_after = Pt(5)

chart_card_s3 = add_canva_card(s3, Inches(5.75), Inches(1.5), Inches(6.783), Inches(5.25), bg_color=COLOR_CARD_BG)
add_image_fitted(s3, "slide_assets/chart2_clean_hd.png", Inches(5.95), Inches(1.7), Inches(6.383), Inches(4.9))

add_canva_footer(s3, 3, 8)

# =============================================================
# SLIDE 4: NEIGHBORHOOD RANKINGS
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_canva_header(s4, "Neighborhood Rankings: Volume Concentration vs. Growth Rates", "Spatial Dynamics", "04")

card_rank = add_canva_card(s4, Inches(0.8), Inches(1.5), Inches(4.7), Inches(5.25), bg_color=COLOR_CARD_BG)
tb_s4 = s4.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(4.2), Inches(4.85))
tf_s4 = tb_s4.text_frame; tf_s4.word_wrap = True; tf_s4.margin_left = tf_s4.margin_top = tf_s4.margin_right = tf_s4.margin_bottom = 0
p_s4_h = tf_s4.paragraphs[0]; p_s4_h.text = "Volume Scale vs. Growth Dynamic"; p_s4_h.font.name = FONT_DISPLAY; p_s4_h.font.size = Pt(13.5); p_s4_h.font.bold = True; p_s4_h.font.color.rgb = COLOR_PRIMARY_NAVY; p_s4_h.space_after = Pt(4)

p_s4_takeaway = tf_s4.add_paragraph(); p_s4_takeaway.text = "Core Insight: Growth is NOT concentrated in the largest neighborhood."
p_s4_takeaway.font.name = FONT_BODY; p_s4_takeaway.font.size = Pt(10.5); p_s4_takeaway.font.bold = True; p_s4_takeaway.font.color.rgb = COLOR_ROYAL_BLUE; p_s4_takeaway.space_after = Pt(6)

p_r1_h = tf_s4.add_paragraph(); p_r1_h.text = "• By Average Monthly Count (Magnitude):"; p_r1_h.font.name = FONT_BODY; p_r1_h.font.size = Pt(10); p_r1_h.font.bold = True; p_r1_h.font.color.rgb = COLOR_ROYAL_BLUE

rank_size_items = [
    "1. East Village: 552.04 (std 157.27 — highest volume & volatility)",
    "2. Outside Perimeter: 217.57 (partial coverage, 56 obs)",
    "3. City Center: 170.68 (std 52.95)",
    "4. Cortez: 59.62  |  5. Gaslamp: 48.17",
    "6. Columbia: 44.49  |  7. Marina: 30.75 (smallest, std 15.54)"
]
for rsi in rank_size_items:
    p_rsi = tf_s4.add_paragraph(); p_rsi.text = f"    {rsi}"; p_rsi.font.name = FONT_BODY; p_rsi.font.size = Pt(8.8); p_rsi.font.color.rgb = COLOR_TEXT_DARK

p_r2_h = tf_s4.add_paragraph(); p_r2_h.text = "• By Growth Rate (Mean YoY %, 2019+):"; p_r2_h.font.name = FONT_BODY; p_r2_h.font.size = Pt(10); p_r2_h.font.bold = True; p_r2_h.font.color.rgb = COLOR_ROYAL_BLUE; p_r2_h.space_before = Pt(4)

rank_growth_items = [
    "Fastest Growing: Outside Perimeter (+26.90%/yr), Cortez (+12.12%/yr), City Center (+5.19%/yr).",
    "Modest Core Growth: East Village grew slowly (+1.64%/yr) despite ~55% volume share.",
    "Shrinking Areas: Marina (-13.11%/yr) and Columbia (-4.28%/yr) had sustained drops."
]
for rgi in rank_growth_items:
    p_rgi = tf_s4.add_paragraph(); p_rgi.text = f"  - {rgi}"; p_rgi.font.name = FONT_BODY; p_rgi.font.size = Pt(8.8); p_rgi.font.color.rgb = COLOR_TEXT_DARK

p_r3_h = tf_s4.add_paragraph(); p_r3_h.text = "• Spatial Sub-Area Asymmetry:"; p_r3_h.font.name = FONT_BODY; p_r3_h.font.size = Pt(10); p_r3_h.font.bold = True; p_r3_h.font.color.rgb = COLOR_ROYAL_BLUE; p_r3_h.space_before = Pt(4)
p_r3_d = tf_s4.add_paragraph(); p_r3_d.text = "  North East & South East EV consistently outcount West sub-areas."; p_r3_d.font.name = FONT_BODY; p_r3_d.font.size = Pt(8.8); p_r3_d.font.color.rgb = COLOR_TEXT_DARK

chart_card_s4 = add_canva_card(s4, Inches(5.75), Inches(1.5), Inches(6.783), Inches(5.25), bg_color=COLOR_CARD_BG)
add_image_fitted(s4, "slide_assets/chart7_yoy_hd.png", Inches(5.95), Inches(1.7), Inches(6.383), Inches(4.9))

add_canva_footer(s4, 4, 8)

# =============================================================
# SLIDE 5: COVID-19 PERIOD IMPACT
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_canva_header(s5, "COVID-19 Period Impact: Temporary Suppression & Sharp Rebound", "Pandemic Impact", "05")

card_covid = add_canva_card(s5, Inches(0.8), Inches(1.5), Inches(4.7), Inches(5.25), bg_color=COLOR_CARD_BG)
tb_s5 = s5.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(4.2), Inches(4.85))
tf_s5 = tb_s5.text_frame; tf_s5.word_wrap = True; tf_s5.margin_left = tf_s5.margin_top = tf_s5.margin_right = tf_s5.margin_bottom = 0
p_s5_h = tf_s5.paragraphs[0]; p_s5_h.text = "Pandemic Shock & Rebound Profile"; p_s5_h.font.name = FONT_DISPLAY; p_s5_h.font.size = Pt(13.5); p_s5_h.font.bold = True; p_s5_h.font.color.rgb = COLOR_PRIMARY_NAVY; p_s5_h.space_after = Pt(5)

p_s5_sub = tf_s5.add_paragraph(); p_s5_sub.text = "Finding: Pandemic programs suppressed visible street counts without a lasting reduction in demand."
p_s5_sub.font.name = FONT_BODY; p_s5_sub.font.size = Pt(10.5); p_s5_sub.font.bold = True; p_s5_sub.font.color.rgb = COLOR_ROYAL_BLUE; p_s5_sub.space_after = Pt(8)

covid_points = [
    ("Series All-Time Low (March 2020)", "Citywide unsheltered total hit its series low of 529 in March 2020 at the onset of initial COVID shelter-in-place orders."),
    ("2020 Annual Trough (~20% Reduction)", "2020 annual average (654.1) dropped ~20% below the 2019 pre-COVID baseline (810.43), reflecting -19.29% YoY contraction."),
    ("Full Recovery by 2021", "Counts recovered to an annual average of 960.37 in 2021 (+46.82% YoY, citywide-total basis), climbing above pre-COVID baseline levels prior to the 2022–2023 surge."),
    ("Operational & Policy Mechanisms", "Emergency indoor shelter placements (Convention Center Operation Shelter to Home), eviction moratoria, and curtailed street sweeps temporarily reduced visible unsheltered numbers; demobilization preceded the 2022–2023 peak.")
]
for c_head, c_txt in covid_points:
    p_ch = tf_s5.add_paragraph(); p_ch.text = f"• {c_head}:"; p_ch.font.name = FONT_BODY; p_ch.font.size = Pt(10); p_ch.font.bold = True; p_ch.font.color.rgb = COLOR_ROYAL_BLUE
    p_ct = tf_s5.add_paragraph(); p_ct.text = f"  {c_txt}"; p_ct.font.name = FONT_BODY; p_ct.font.size = Pt(9.2); p_ct.font.color.rgb = COLOR_TEXT_DARK; p_ct.space_after = Pt(6)

chart_card_s5 = add_canva_card(s5, Inches(5.75), Inches(1.5), Inches(6.783), Inches(5.25), bg_color=COLOR_CARD_BG)
add_image_fitted(s5, "slide_assets/chart8_clean_hd.png", Inches(5.95), Inches(1.7), Inches(6.383), Inches(4.9))

add_canva_footer(s5, 5, 8)

# =============================================================
# SLIDE 6: METHODOLOGY CHANGE EFFECTS
# =============================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_canva_header(s6, "Methodology Regimes: Quantifying the Raw vs. Adjusted Count Gap", "Data Governance", "06")

card_meth = add_canva_card(s6, Inches(0.8), Inches(1.5), Inches(4.7), Inches(5.25), bg_color=COLOR_CARD_BG)
tb_s6 = s6.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(4.2), Inches(4.85))
tf_s6 = tb_s6.text_frame; tf_s6.word_wrap = True; tf_s6.margin_left = tf_s6.margin_top = tf_s6.margin_right = tf_s6.margin_bottom = 0
p_s6_h = tf_s6.paragraphs[0]; p_s6_h.text = "Evaluation of Multiplier Regimes"; p_s6_h.font.name = FONT_DISPLAY; p_s6_h.font.size = Pt(13.5); p_s6_h.font.bold = True; p_s6_h.font.color.rgb = COLOR_PRIMARY_NAVY; p_s6_h.space_after = Pt(5)

p_s6_sub = tf_s6.add_paragraph(); p_s6_sub.text = "Conclusion: Multipliers add only a small gap (within ±2/month on average) and do not distort longitudinal trends."
p_s6_sub.font.name = FONT_BODY; p_s6_sub.font.size = Pt(10.5); p_s6_sub.font.bold = True; p_s6_sub.font.color.rgb = COLOR_ROYAL_BLUE; p_s6_sub.space_after = Pt(8)

p_m1_h = tf_s6.add_paragraph(); p_m1_h.text = "• Four Historical Regimes:"; p_m1_h.font.name = FONT_BODY; p_m1_h.font.size = Pt(10); p_m1_h.font.bold = True; p_m1_h.font.color.rgb = COLOR_ROYAL_BLUE
regimes_list = [
    "PRE2017 (Jan–Mar 2017): Direct visual count, no component breakout.",
    "APR2017 (Apr 2017–Apr 2018): Vehicle multiplier set to 1.66×.",
    "MAY2018 (May 2018–Dec 2019): Vehicle multiplier increased to 2.03×.",
    "POST2020 (Jan 2020–present): 2.03× retained by DSDP for continuity."
]
for reg in regimes_list:
    p_reg = tf_s6.add_paragraph(); p_reg.text = f"  - {reg}"; p_reg.font.name = FONT_BODY; p_reg.font.size = Pt(8.8); p_reg.font.color.rgb = COLOR_TEXT_DARK

meth_other = [
    ("Gap Is Small in Every Year", "Gap (total_count - raw_count) averages within ±2/month each year: DSDP published totals already include the multipliers. The earlier Feb 2018 spike (+156.61) was a data-entry error (100 tents instead of 10), corrected against the source map in Oct 2026."),
    ("Remaining Outliers Are Source Conflicts", "The largest remaining single-month gaps (Apr 2020 +19.7, Feb 2023 -12.5) are months where DSDP map pages and its summary table disagree; listed in MasterCounts_QA_Flags.csv."),
    ("Pre-2018 Constraint", "Because component breakouts began in Jan 2018, raw and adjusted totals are identical across all of 2017 (gap = 0).")
]
for mo_head, mo_txt in meth_other:
    p_moh = tf_s6.add_paragraph(); p_moh.text = f"• {mo_head}:"; p_moh.font.name = FONT_BODY; p_moh.font.size = Pt(10); p_moh.font.bold = True; p_moh.font.color.rgb = COLOR_ROYAL_BLUE; p_moh.space_before = Pt(3)
    p_mot = tf_s6.add_paragraph(); p_mot.text = f"  {mo_txt}"; p_mot.font.name = FONT_BODY; p_mot.font.size = Pt(8.8); p_mot.font.color.rgb = COLOR_TEXT_DARK

chart_card_s6 = add_canva_card(s6, Inches(5.75), Inches(1.5), Inches(6.783), Inches(5.25), bg_color=COLOR_CARD_BG)
add_image_fitted(s6, "slide_assets/chart9_clean_hd.png", Inches(5.95), Inches(1.7), Inches(6.383), Inches(4.9))

add_canva_footer(s6, 6, 8)

# =============================================================
# SLIDE 7: HYPOTHESES FOR FURTHER ANALYSIS (Canva 4-Card Grid)
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_canva_header(s7, "Hypotheses for Further Analysis: Focus Areas for Later Tasks", "Research Directions", "07")

hypotheses = [
    ("H1: Policy & Enforcement Driver of 2022–2023 Peak",
     "Synchronized Citywide Surge",
     "The +57.55% (2022) surge hit nearly every neighborhood simultaneously (Cortez +132%, Outside Perimeter +87%, East Village +50%). This synchronized timing points to systemic citywide drivers (eviction moratorium expirations, shelter demobilizations, or sweep shifts) rather than local dynamics.",
     "Test: Correlate monthly counts against RTFH policy timelines, shelter census, and 311 encampment dispatch logs.",
     COLOR_ROYAL_BLUE),
    
    ("H2: East Village Asymmetry Reflects Built Environment",
     "East vs. West Infrastructure Divide",
     "East Village sub-areas show persistent asymmetry: North East and South East EV consistently outcount North West and South West EV across 2018–2025. This concentration indicates infrastructure and zoning drivers.",
     "Test: Spatial autocorrelation (Moran's I / Getis-Ord Gi* in Assignment 5) against transit hubs, shelter proximity, and zoning.",
     COLOR_PRIMARY_NAVY),
     
    ("H3: 2024 Pullback (-43.26%) May Be a Reporting Artifact",
     "Rapid Single-Year Drop Scrutiny",
     "A steep -43.26% drop in a single year immediately after the historical peak warrants verification against external benchmarks before reading it as a true population drop. Count area or staffing changes may be confounders.",
     "Test: Benchmark against independent RTFH Point-in-Time (PIT) counts and audit 2024 DSDP canvassing operations.",
     COLOR_MID_BLUE),
     
    ("H4: Neighborhood Growth Inversely Related to Area Size",
     "Peripheral Displacement Dynamics",
     "Mid-sized areas grow fastest (Outside Perimeter +26.90%, Cortez +12.12%, City Center +5.19%), while East Village grows slowly (+1.75%) and Marina shrinks (-13.11%). Enforcement in core areas may displace individuals to borders.",
     "Test: Perform spatial adjacency and boundary-flow analysis in Assignment 5 to evaluate displacement effects.",
     COLOR_SOFT_BLUE)
]

for idx, (h_title, h_sub, h_desc, h_action, h_color) in enumerate(hypotheses):
    row = idx // 2
    col = idx % 2
    c_left = Inches(0.8 + col * 5.95)
    c_top = Inches(1.55 + row * 2.35)
    c_w = Inches(5.783)
    c_h = Inches(2.05)
    add_canva_card(s7, c_left, c_top, c_w, c_h, bg_color=COLOR_CARD_BG)
    top_bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.02), c_top + Inches(0.02), c_w - Inches(0.04), Inches(0.06))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = h_color; top_bar.line.fill.background()
    tb_h = s7.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.18), c_w - Inches(0.4), c_h - Inches(0.3))
    tf_h = tb_h.text_frame; tf_h.word_wrap = True; tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    p_ht = tf_h.paragraphs[0]; p_ht.text = h_title; p_ht.font.name = FONT_DISPLAY; p_ht.font.size = Pt(11.5); p_ht.font.bold = True; p_ht.font.color.rgb = COLOR_PRIMARY_NAVY; p_ht.space_after = Pt(2)
    p_hs = tf_h.add_paragraph(); p_hs.text = h_sub.upper(); p_hs.font.name = FONT_BODY; p_hs.font.size = Pt(8.5); p_hs.font.bold = True; p_hs.font.color.rgb = COLOR_ROYAL_BLUE; p_hs.space_after = Pt(4)
    p_hd = tf_h.add_paragraph(); p_hd.text = h_desc; p_hd.font.name = FONT_BODY; p_hd.font.size = Pt(9.2); p_hd.font.color.rgb = COLOR_TEXT_DARK; p_hd.space_after = Pt(4)
    p_ha = tf_h.add_paragraph(); p_ha.text = f"• {h_action}"; p_ha.font.name = FONT_BODY; p_ha.font.size = Pt(9); p_ha.font.bold = True; p_ha.font.color.rgb = COLOR_PRIMARY_NAVY

add_canva_footer(s7, 7, 8)

# =============================================================
# SLIDE 8: DATA LIMITATIONS & NEXT STEPS
# =============================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_canva_header(s8, "Data Limitations, Governance Caveats & Roadmap Ahead", "Project Roadmap", "08")

card_lim = add_canva_card(s8, Inches(0.8), Inches(2.4), Inches(5.75), Inches(3.55), bg_color=COLOR_CARD_BG)
tb_s8_l = s8.shapes.add_textbox(Inches(1.05), Inches(2.6), Inches(5.25), Inches(3.15))
tf_s8_l = tb_s8_l.text_frame; tf_s8_l.word_wrap = True; tf_s8_l.margin_left = tf_s8_l.margin_top = tf_s8_l.margin_right = tf_s8_l.margin_bottom = 0
p_s8_lh = tf_s8_l.paragraphs[0]; p_s8_lh.text = "Identified Data Limitations & Biases"; p_s8_lh.font.name = FONT_DISPLAY; p_s8_lh.font.size = Pt(13.5); p_s8_lh.font.bold = True; p_s8_lh.font.color.rgb = COLOR_PRIMARY_NAVY; p_s8_lh.space_after = Pt(6)

limitations = [
    ("Incomplete 2025 Series (Reporting Lag)", "28 nulls in total_count (Jul, Aug, Oct, Nov 2025 across all 7 neighborhoods) represent unreleased counts, not data errors. All 2025 annual figures must be treated as partial-year."),
    ("Outside Perimeter Partial History", "Outside Perimeter contains only 56 observations (canvassing began ~2022). Its reported +26.90%/yr growth rate is the least statistically reliable neighborhood figure."),
    ("Pre-2018 Lack of Component Breakouts", "Component-level counts (tents, vehicles) are unavailable before Jan 2018. Raw and adjusted totals are identical for all of 2017, precluding early multiplier analysis."),
    ("Documented Source-PDF Addition Errors", "Task 1.1's 45-cell audit found a 97.56% fidelity rate against source PDFs, noting known errors (Feb 2018 +30 PDF addition bug, 2019 EV sub-area duplication, Apr 2025 discrepancy).")
]
for l_head, l_desc in limitations:
    p_lh = tf_s8_l.add_paragraph(); p_lh.text = f"• {l_head}:"; p_lh.font.name = FONT_BODY; p_lh.font.size = Pt(10); p_lh.font.bold = True; p_lh.font.color.rgb = COLOR_RED
    p_ld = tf_s8_l.add_paragraph(); p_ld.text = f"  {l_desc}"; p_ld.font.name = FONT_BODY; p_ld.font.size = Pt(9.2); p_ld.font.color.rgb = COLOR_TEXT_DARK; p_ld.space_after = Pt(5)

card_nxt = add_canva_card(s8, Inches(6.783), Inches(2.4), Inches(5.75), Inches(3.55), bg_color=COLOR_CARD_BG)
tb_s8_r = s8.shapes.add_textbox(Inches(7.033), Inches(2.6), Inches(5.25), Inches(3.15))
tf_s8_r = tb_s8_r.text_frame; tf_s8_r.word_wrap = True; tf_s8_r.margin_left = tf_s8_r.margin_top = tf_s8_r.margin_right = tf_s8_r.margin_bottom = 0
p_s8_rh = tf_s8_r.paragraphs[0]; p_s8_rh.text = "Roadmap Ahead: Assignment 3 Integration"; p_s8_rh.font.name = FONT_DISPLAY; p_s8_rh.font.size = Pt(13.5); p_s8_rh.font.bold = True; p_s8_rh.font.color.rgb = COLOR_PRIMARY_NAVY; p_s8_rh.space_after = Pt(6)

next_steps = [
    ("Immediate Deliverable: Assignment 3", "Block-Level Validation & Spatial Integration — moving from macro neighborhood aggregates to granular micro-data across 500+ individual block parcels."),
    ("Granular Block-Level Mapping", "Audit street-level counts, reconcile boundary discrepancies, and align block records with GIS city parcel boundaries."),
    ("Spatial Autocorrelation Modeling", "Execute Global Moran's I and Local Getis-Ord Gi* hot-spot detection in Assignment 5 to quantify spatial clustering around transit nodes and service hubs."),
    ("Cross-Dataset Validation & Benchmarking", "Cross-reference DSDP monthly counts with regional RTFH annual Point-in-Time (PIT) benchmarks and City of San Diego 311 service call logs.")
]
for n_head, n_desc in next_steps:
    p_nh = tf_s8_r.add_paragraph(); p_nh.text = f"• {n_head}:"; p_nh.font.name = FONT_BODY; p_nh.font.size = Pt(10); p_nh.font.bold = True; p_nh.font.color.rgb = COLOR_GREEN
    p_nd = tf_s8_r.add_paragraph(); p_nd.text = f"  {n_desc}"; p_nd.font.name = FONT_BODY; p_nd.font.size = Pt(9.2); p_nd.font.color.rgb = COLOR_TEXT_DARK; p_nd.space_after = Pt(5)

add_canva_footer(s8, 8, 8)

try:
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EDA_Presentation.pptx")
    prs.save(output_path)
    print(f"SUCCESS: Saved Canva-themed presentation to {output_path}")
except PermissionError:
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EDA_Presentation_v2.pptx")
    prs.save(output_path)
    print(f"SUCCESS (Fallback): Saved Canva-themed presentation to {output_path} (EDA_Presentation.pptx was locked)")