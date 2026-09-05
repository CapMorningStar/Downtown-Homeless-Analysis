import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# -------------------------------------------------------------
# Color Palette (Tailwind / Modern Executive Theme)
# -------------------------------------------------------------
COLOR_BG_SLIDE = RGBColor(248, 250, 252)       # Slate 50
COLOR_CARD_BG = RGBColor(255, 255, 255)        # Pure White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200
COLOR_TITLE = RGBColor(15, 23, 42)             # Slate 900
COLOR_BODY = RGBColor(51, 65, 85)              # Slate 700
COLOR_MUTED = RGBColor(100, 116, 139)          # Slate 500
COLOR_PRIMARY_BLUE = RGBColor(37, 99, 235)     # Blue 600
COLOR_NAVY = RGBColor(30, 58, 138)             # Blue 900
COLOR_AMBER = RGBColor(217, 119, 6)            # Amber 600
COLOR_RED = RGBColor(220, 38, 38)              # Red 600
COLOR_GREEN = RGBColor(5, 150, 105)            # Emerald 600
COLOR_ACCENT_BG = RGBColor(239, 246, 255)      # Blue 50
COLOR_ACCENT_BORDER = RGBColor(191, 219, 254)  # Blue 200

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def set_slide_background(slide):
    # Add a full-screen background rectangle
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG_SLIDE
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_tracker="TASK 2.3 | EDA CHECK-IN"):
    # Header container
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Category Tracker
    p0 = tf.paragraphs[0]
    p0.text = category_tracker.upper()
    p0.font.name = "Calibri"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_PRIMARY_BLUE
    p0.space_after = Pt(2)
    
    # Title
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "Calibri"
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TITLE
    
    # Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

def add_footer(slide, current_page, total_pages=8):
    # Divider line above footer
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    # Left text
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(9.5), Inches(0.35))
    tf_left = tb_left.text_frame
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_l = tf_left.paragraphs[0]
    p_l.text = "Data Science Alliance • Downtown San Diego Homeless Population Analysis • Source: DSDP Monthly Counts (2017–2025)"
    p_l.font.name = "Calibri"
    p_l.font.size = Pt(9)
    p_l.font.color.rgb = COLOR_MUTED

    # Right text (Slide number)
    tb_right = slide.shapes.add_textbox(Inches(10.5), Inches(6.98), Inches(2.033), Inches(0.35))
    tf_right = tb_right.text_frame
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_r = tf_right.paragraphs[0]
    p_r.text = f"Slide {current_page} of {total_pages}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = "Calibri"
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
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
    # Calculate aspect-ratio fit
    with Image.open(image_path) as img:
        img_w, img_h = img.size
    
    aspect = img_w / img_h
    cont_aspect = container_width / container_height
    
    if aspect > cont_aspect:
        # Image is wider relative to container -> fit width
        target_w = container_width
        target_h = container_width / aspect
        offset_x = 0
        offset_y = (container_height - target_h) / 2
    else:
        # Image is taller -> fit height
        target_h = container_height
        target_w = container_height * aspect
        offset_y = 0
        offset_x = (container_width - target_w) / 2
        
    return slide.shapes.add_picture(
        image_path,
        container_left + offset_x,
        container_top + offset_y,
        target_w,
        target_h
    )

# -------------------------------------------------------------
# Presentation Initialization
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# =============================================================
# SLIDE 1: TITLE SLIDE
# =============================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Large hero container card
hero = add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

# Top badge
badge = add_card(s1, Inches(1.8), Inches(1.6), Inches(4.2), Inches(0.4), bg_color=COLOR_ACCENT_BG, border_color=COLOR_ACCENT_BORDER)
tb_badge = s1.shapes.add_textbox(Inches(1.8), Inches(1.6), Inches(4.2), Inches(0.4))
tf_b = tb_badge.text_frame
tf_b.margin_left = Inches(0.15)
tf_b.margin_top = Inches(0.08)
p_b = tf_b.paragraphs[0]
p_b.text = "DATA SCIENCE ALLIANCE • TASK 2.3 CHECK-IN"
p_b.font.name = "Calibri"
p_b.font.size = Pt(10.5)
p_b.font.bold = True
p_b.font.color.rgb = COLOR_PRIMARY_BLUE

# Title text box
tb_title = s1.shapes.add_textbox(Inches(1.8), Inches(2.2), Inches(9.7), Inches(2.2))
tf_t = tb_title.text_frame
tf_t.word_wrap = True
tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

p_t1 = tf_t.paragraphs[0]
p_t1.text = "Downtown San Diego Unsheltered\nHomeless Population: EDA Findings"
p_t1.font.name = "Calibri"
p_t1.font.size = Pt(34)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_TITLE
p_t1.space_after = Pt(14)

p_t2 = tf_t.add_paragraph()
p_t2.text = "Kyaw Soe Lwin | Data Science Alliance | 2017–2025"
p_t2.font.name = "Calibri"
p_t2.font.size = Pt(18)
p_t2.font.color.rgb = COLOR_NAVY
p_t2.font.bold = True

# Divider inside hero
div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.8), Inches(4.6), Inches(9.7), Inches(0.015))
div1.fill.solid()
div1.fill.fore_color.rgb = COLOR_CARD_BORDER
div1.line.fill.background()

# Key metadata row (3 quick info blocks)
meta_items = [
    ("Source Data", "Downtown San Diego Partnership (DSDP) Clean & Safe monthly counts"),
    ("Longitudinal Scope", "2017–2025 (8 full & partial calendar years, 7 downtown neighborhoods)"),
    ("Analysis Purpose", "Baseline trends, seasonal variance, COVID-19 dip, & methodology impacts")
]
for idx, (m_label, m_val) in enumerate(meta_items):
    m_left = Inches(1.8 + idx * 3.3)
    tb_m = s1.shapes.add_textbox(m_left, Inches(4.8), Inches(3.0), Inches(1.2))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
    
    p_ml = tf_m.paragraphs[0]
    p_ml.text = m_label.upper()
    p_ml.font.name = "Calibri"
    p_ml.font.size = Pt(9.5)
    p_ml.font.bold = True
    p_ml.font.color.rgb = COLOR_MUTED
    p_ml.space_after = Pt(2)
    
    p_mv = tf_m.add_paragraph()
    p_mv.text = m_val
    p_mv.font.name = "Calibri"
    p_mv.font.size = Pt(11)
    p_mv.font.color.rgb = COLOR_BODY

# Footer
add_footer(s1, 1, 8)


# =============================================================
# SLIDE 2: OVERALL TREND
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "Overall Longitudinal Trend & Three Distinct Phases (2017–2025)")

# Left side: Metrics & 3 Phases
# KPI Stat chips row
kpis_s2 = [
    ("529", "Series Low", "March 2020 (COVID trough)", COLOR_RED),
    ("2,103", "Series Peak", "May 2023 (Rebound high)", COLOR_NAVY),
    ("156.8", "Grand Mean", "Per neighborhood-mo", COLOR_BODY)
]
for i, (val, lbl, sub, col) in enumerate(kpis_s2):
    c_left = Inches(0.8 + i * 1.55)
    add_card(s2, c_left, Inches(1.55), Inches(1.45), Inches(1.05), bg_color=COLOR_CARD_BG)
    tb_k = s2.shapes.add_textbox(c_left + Inches(0.08), Inches(1.6), Inches(1.3), Inches(0.95))
    tf_k = tb_k.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    
    pk1 = tf_k.paragraphs[0]
    pk1.text = val
    pk1.font.name = "Calibri"
    pk1.font.size = Pt(19)
    pk1.font.bold = True
    pk1.font.color.rgb = col
    
    pk2 = tf_k.add_paragraph()
    pk2.text = lbl.upper()
    pk2.font.name = "Calibri"
    pk2.font.size = Pt(8.5)
    pk2.font.bold = True
    pk2.font.color.rgb = COLOR_TITLE
    
    pk3 = tf_k.add_paragraph()
    pk3.text = sub
    pk3.font.name = "Calibri"
    pk3.font.size = Pt(7.5)
    pk3.font.color.rgb = COLOR_MUTED

# Left Text Card: Three Phases
card_phases = add_card(s2, Inches(0.8), Inches(2.75), Inches(4.55), Inches(3.95), bg_color=COLOR_CARD_BG)
tb_phases = s2.shapes.add_textbox(Inches(1.0), Inches(2.9), Inches(4.15), Inches(3.65))
tf_p = tb_phases.text_frame
tf_p.word_wrap = True
tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

p_h = tf_p.paragraphs[0]
p_h.text = "Trajectory Overview: Three Clear Phases"
p_h.font.name = "Calibri"
p_h.font.size = Pt(13.5)
p_h.font.bold = True
p_h.font.color.rgb = COLOR_TITLE
p_h.space_after = Pt(8)

phases_data = [
    ("Phase 1: 2017–2020 Decline", 
     "Annual avg fell from 176.31 to 109.02 (~-38% cumulative reduction). YoY drops: -18.98% (2018), -4.94% (2019), and -19.71% (2020)."),
    ("Phase 2: 2021–2023 Rebound & Peak", 
     "Sharp reversal: +25.85% (2021) and +57.63% (2022). Rose to annual avg of 223.98 in 2023 (>2x the 2020 trough), setting all-time highs."),
    ("Phase 3: 2024–2025 Pullback & Stabilization", 
     "Steep -43.52% contraction in 2024 brought annual avg down to 126.50; 2025 remained roughly flat at 122.78 (-2.94% YoY).")
]

for p_title, p_desc in phases_data:
    p_t = tf_p.add_paragraph()
    p_t.text = f"• {p_title}: "
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(10.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY
    
    p_d = tf_p.add_paragraph()
    p_d.text = f"  {p_desc}"
    p_d.font.name = "Calibri"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_BODY
    p_d.space_after = Pt(6)

# Right: Chart Card
chart_card_s2 = add_card(s2, Inches(5.6), Inches(1.55), Inches(6.933), Inches(5.15), bg_color=COLOR_CARD_BG)
add_image_fitted(s2, "slide_assets/cell_27.png", Inches(5.75), Inches(1.7), Inches(6.633), Inches(4.5))

# Chart footnote
tb_cf2 = s2.shapes.add_textbox(Inches(5.75), Inches(6.3), Inches(6.633), Inches(0.3))
tf_cf2 = tb_cf2.text_frame
tf_cf2.margin_left = tf_cf2.margin_top = tf_cf2.margin_right = tf_cf2.margin_bottom = 0
p_cf2 = tf_cf2.paragraphs[0]
p_cf2.text = "Chart 1 (EDA Notebook): Sum of neighborhood monthly total_count with methodology regime markers."
p_cf2.font.name = "Calibri"
p_cf2.font.size = Pt(8.5)
p_cf2.font.color.rgb = COLOR_MUTED

add_footer(s2, 2, 8)


# =============================================================
# SLIDE 3: SEASONALITY (QUANTIFIED)
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "Calendar-Month Seasonality: Modest Effect vs. Multi-Year Swings")

# Left Column: Findings Card
card_season = add_card(s3, Inches(0.8), Inches(1.55), Inches(4.7), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s3 = s3.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(4.2), Inches(4.75))
tf_s3 = tb_s3.text_frame
tf_s3.word_wrap = True
tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0

p_s3_h = tf_s3.paragraphs[0]
p_s3_h.text = "Quantifying the Calendar Effect"
p_s3_h.font.name = "Calibri"
p_s3_h.font.size = Pt(14)
p_s3_h.font.bold = True
p_s3_h.font.color.rgb = COLOR_TITLE
p_s3_h.space_after = Pt(8)

p_s3_callout = tf_s3.add_paragraph()
p_s3_callout.text = "Key Takeaway: Which YEAR a month falls in matters far more than which calendar month it is."
p_s3_callout.font.name = "Calibri"
p_s3_callout.font.size = Pt(11)
p_s3_callout.font.bold = True
p_s3_callout.font.color.rgb = COLOR_PRIMARY_BLUE
p_s3_callout.space_after = Pt(10)

s3_bullets = [
    ("Modest Monthly Deviation", 
     "No single calendar month deviates by more than ~5% from the grand mean (156.78). Peak-to-trough spread is only 8.4 percentage points."),
    ("Top 3 Highest Months", 
     "Feb (+3.2%, avg 161.76), Aug (+3.1%, avg 161.61), May (+2.6%, avg 160.93)."),
    ("Top 3 Lowest Months", 
     "Mar (-5.2%, avg 148.67), Sep (-2.0%, avg 153.63), Nov (-2.1%, avg 153.43) [Apr: -2.1%, avg 153.53]."),
    ("High Standard Deviation", 
     "Month-to-month std ranges from 187 to 216 — substantially wider than the monthly mean differences, demonstrating year effects dominate."),
    ("East Village Exception", 
     "East Village exhibits its own local pattern: peaks in Jul–Aug (~601–604) and dips in spring (Mar–Apr, ~509), diverging from citywide trends.")
]

for b_head, b_txt in s3_bullets:
    p_bhead = tf_s3.add_paragraph()
    p_bhead.text = f"• {b_head}: "
    p_bhead.font.name = "Calibri"
    p_bhead.font.size = Pt(10.5)
    p_bhead.font.bold = True
    p_bhead.font.color.rgb = COLOR_NAVY
    
    p_btxt = tf_s3.add_paragraph()
    p_btxt.text = f"  {b_txt}"
    p_btxt.font.name = "Calibri"
    p_btxt.font.size = Pt(9.5)
    p_btxt.font.color.rgb = COLOR_BODY
    p_btxt.space_after = Pt(5)

# Right: Chart Card (Chart 2)
chart_card_s3 = add_card(s3, Inches(5.75), Inches(1.55), Inches(6.783), Inches(5.15), bg_color=COLOR_CARD_BG)
add_image_fitted(s3, "slide_assets/cell_30.png", Inches(5.95), Inches(1.75), Inches(6.383), Inches(4.45))

tb_cf3 = s3.shapes.add_textbox(Inches(5.95), Inches(6.3), Inches(6.383), Inches(0.3))
tf_cf3 = tb_cf3.text_frame
tf_cf3.margin_left = tf_cf3.margin_top = tf_cf3.margin_right = tf_cf3.margin_bottom = 0
p_cf3 = tf_cf3.paragraphs[0]
p_cf3.text = "Chart 2 (EDA Notebook): Average monthly count by calendar month (with std error bars) across 2017–2025."
p_cf3.font.name = "Calibri"
p_cf3.font.size = Pt(8.5)
p_cf3.font.color.rgb = COLOR_MUTED

add_footer(s3, 3, 8)


# =============================================================
# SLIDE 4: NEIGHBORHOOD RANKINGS
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Neighborhood Breakdown: High Concentration vs. Peripheral Growth")

# Left Column: Size vs Growth Card
card_rank = add_card(s4, Inches(0.8), Inches(1.55), Inches(4.7), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s4 = s4.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(4.2), Inches(4.75))
tf_s4 = tb_s4.text_frame
tf_s4.word_wrap = True
tf_s4.margin_left = tf_s4.margin_top = tf_s4.margin_right = tf_s4.margin_bottom = 0

p_s4_h = tf_s4.paragraphs[0]
p_s4_h.text = "Volume Scale vs. Growth Dynamic"
p_s4_h.font.name = "Calibri"
p_s4_h.font.size = Pt(14)
p_s4_h.font.bold = True
p_s4_h.font.color.rgb = COLOR_TITLE
p_s4_h.space_after = Pt(6)

p_s4_takeaway = tf_s4.add_paragraph()
p_s4_takeaway.text = "Critical Finding: Growth is NOT concentrated in the largest neighborhood."
p_s4_takeaway.font.name = "Calibri"
p_s4_takeaway.font.size = Pt(11)
p_s4_takeaway.font.bold = True
p_s4_takeaway.font.color.rgb = COLOR_PRIMARY_BLUE
p_s4_takeaway.space_after = Pt(8)

rank_bullets = [
    ("By Average Monthly Count (Magnitude)",
     "1. East Village: 552.77 (std 157.1 — largest & most volatile)\n"
     "2. Outside Perimeter: 217.57 (partial series, 56 obs)\n"
     "3. City Center: 171.81\n"
     "4. Cortez: 59.52  |  5. Gaslamp: 48.43\n"
     "6. Columbia: 44.49  |  7. Marina: 30.94 (smallest, std 15.8)"),
    ("By Growth Rate (Mean YoY %, 2019+)",
     "• Fastest Growing: Outside Perimeter (+26.90%/yr), Cortez (+11.96%/yr), City Center (+3.94%/yr).\n"
     "• Modest Core Growth: East Village grew only +1.64%/yr despite comprising ~55% of the total volume.\n"
     "• Shrinking Areas: Columbia (-4.28%/yr) and Marina (-12.76%/yr) experienced steady net reductions."),
    ("Sub-Area Dynamics",
     "Within East Village, North East & South East EV consistently outcount western sectors, indicating eastern spatial clustering.")
]

for r_head, r_txt in rank_bullets:
    p_rh = tf_s4.add_paragraph()
    p_rh.text = f"• {r_head}"
    p_rh.font.name = "Calibri"
    p_rh.font.size = Pt(10.5)
    p_rh.font.bold = True
    p_rh.font.color.rgb = COLOR_NAVY
    
    p_rt = tf_s4.add_paragraph()
    p_rt.text = f"  {r_txt}"
    p_rt.font.name = "Calibri"
    p_rt.font.size = Pt(9.2)
    p_rt.font.color.rgb = COLOR_BODY
    p_rt.space_after = Pt(6)

# Right: Chart Card (Chart 3 Stacked Area)
chart_card_s4 = add_card(s4, Inches(5.75), Inches(1.55), Inches(6.783), Inches(5.15), bg_color=COLOR_CARD_BG)
add_image_fitted(s4, "slide_assets/cell_33.png", Inches(5.95), Inches(1.75), Inches(6.383), Inches(4.45))

tb_cf4 = s4.shapes.add_textbox(Inches(5.95), Inches(6.3), Inches(6.383), Inches(0.3))
tf_cf4 = tb_cf4.text_frame
tf_cf4.margin_left = tf_cf4.margin_top = tf_cf4.margin_right = tf_cf4.margin_bottom = 0
p_cf4 = tf_cf4.paragraphs[0]
p_cf4.text = "Chart 3 (EDA Notebook): Neighborhood composition stacked area over time (2017–2025)."
p_cf4.font.name = "Calibri"
p_cf4.font.size = Pt(8.5)
p_cf4.font.color.rgb = COLOR_MUTED

add_footer(s4, 4, 8)


# =============================================================
# SLIDE 5: COVID-19 PERIOD IMPACT
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "COVID-19 Period Impact: Temporary Suppression & Swift Rebound")

# Left Column: Findings Card
card_covid = add_card(s5, Inches(0.8), Inches(1.55), Inches(4.7), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s5 = s5.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(4.2), Inches(4.75))
tf_s5 = tb_s5.text_frame
tf_s5.word_wrap = True
tf_s5.margin_left = tf_s5.margin_top = tf_s5.margin_right = tf_s5.margin_bottom = 0

p_s5_h = tf_s5.paragraphs[0]
p_s5_h.text = "Pandemic Shock & Recovery Profile"
p_s5_h.font.name = "Calibri"
p_s5_h.font.size = Pt(14)
p_s5_h.font.bold = True
p_s5_h.font.color.rgb = COLOR_TITLE
p_s5_h.space_after = Pt(6)

p_s5_sub = tf_s5.add_paragraph()
p_s5_sub.text = "Observation: Pandemic interventions suppressed visible unsheltered counts without reducing underlying demand."
p_s5_sub.font.name = "Calibri"
p_s5_sub.font.size = Pt(10.5)
p_s5_sub.font.bold = True
p_s5_sub.font.color.rgb = COLOR_PRIMARY_BLUE
p_s5_sub.space_after = Pt(8)

covid_points = [
    ("Series All-Time Low (March 2020)", 
     "Citywide unsheltered count fell to 529 in March 2020 at the onset of initial COVID lockdown measures."),
    ("2020 Annual Trough (~20% Reduction)", 
     "2020 annual average count was 654.1, sitting ~20% below the 2019 pre-COVID baseline (814.72). Year-over-year contraction was -19.71%."),
    ("Rapid 2021 Recovery", 
     "Counts rebounded to an annual average of 960.37 in 2021 (+25.85% YoY), surpassing pre-COVID baselines prior to the larger 2022 climb."),
    ("Key Operational Drivers", 
     "Temporary emergency shelters (e.g. San Diego Convention Center 'Operation Shelter to Home'), eviction moratoria, and curtailed street sweeps suppressed street presence. Once demobilized, counts quickly escalated.")
]

for c_head, c_txt in covid_points:
    p_ch = tf_s5.add_paragraph()
    p_ch.text = f"• {c_head}: "
    p_ch.font.name = "Calibri"
    p_ch.font.size = Pt(10.5)
    p_ch.font.bold = True
    p_ch.font.color.rgb = COLOR_NAVY
    
    p_ct = tf_s5.add_paragraph()
    p_ct.text = f"  {c_txt}"
    p_ct.font.name = "Calibri"
    p_ct.font.size = Pt(9.5)
    p_ct.font.color.rgb = COLOR_BODY
    p_ct.space_after = Pt(6)

# Right: Chart Card (Chart 8 COVID Period)
chart_card_s5 = add_card(s5, Inches(5.75), Inches(1.55), Inches(6.783), Inches(5.15), bg_color=COLOR_CARD_BG)
add_image_fitted(s5, "slide_assets/cell_48.png", Inches(5.95), Inches(1.75), Inches(6.383), Inches(4.45))

tb_cf5 = s5.shapes.add_textbox(Inches(5.95), Inches(6.3), Inches(6.383), Inches(0.3))
tf_cf5 = tb_cf5.text_frame
tf_cf5.margin_left = tf_cf5.margin_top = tf_cf5.margin_right = tf_cf5.margin_bottom = 0
p_cf5 = tf_cf5.paragraphs[0]
p_cf5.text = "Chart 8 (EDA Notebook): Monthly count trajectory (2019–2022) with shaded COVID-19 period (Mar 2020 – Dec 2021)."
p_cf5.font.name = "Calibri"
p_cf5.font.size = Pt(8.5)
p_cf5.font.color.rgb = COLOR_MUTED

add_footer(s5, 5, 8)


# =============================================================
# SLIDE 6: METHODOLOGY CHANGE EFFECTS
# =============================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Methodology Regimes: Quantifying the Raw vs. Adjusted Adjustment Gap")

# Left Column: Methodology Details
card_meth = add_card(s6, Inches(0.8), Inches(1.55), Inches(4.7), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s6 = s6.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(4.2), Inches(4.75))
tf_s6 = tb_s6.text_frame
tf_s6.word_wrap = True
tf_s6.margin_left = tf_s6.margin_top = tf_s6.margin_right = tf_s6.margin_bottom = 0

p_s6_h = tf_s6.paragraphs[0]
p_s6_h.text = "Evaluation of Adjustment Multipliers"
p_s6_h.font.name = "Calibri"
p_s6_h.font.size = Pt(14)
p_s6_h.font.bold = True
p_s6_h.font.color.rgb = COLOR_TITLE
p_s6_h.space_after = Pt(6)

p_s6_sub = tf_s6.add_paragraph()
p_s6_sub.text = "Conclusion: Multiplier adjustments produce a real but proportional gap; they do not distort longitudinal trends."
p_s6_sub.font.name = "Calibri"
p_s6_sub.font.size = Pt(10.5)
p_s6_sub.font.bold = True
p_s6_sub.font.color.rgb = COLOR_PRIMARY_BLUE
p_s6_sub.space_after = Pt(8)

meth_bullets = [
    ("Four Governance Regimes",
     "• PRE2017 (Jan–Mar 2017): Direct visual count, no component breakout.\n"
     "• APR2017 (Apr 2017–Apr 2018): Vehicle multiplier set to 1.66×.\n"
     "• MAY2018 (May 2018–Dec 2019): Vehicle multiplier raised to 2.03×.\n"
     "• POST2020 (Jan 2020–present): 2.03× retained by DSDP for continuity."),
    ("2018 Volatility & Source Bug",
     "Gap (total_count - raw_count) peaked in 2018 (avg +13.5/mo, spiking to +156.61 in Feb 2018). Audit confirmed Feb 2018 spike is partly an unadjusted source-PDF addition error (+30 discrepancy), not purely the multiplier."),
    ("2019+ Gap Stabilization",
     "From 2019 onward, monthly gap stabilized to near-zero (roughly ±1 to ±5), remaining well within the ±2 rounding tolerance."),
    ("Pre-2018 Constraint",
     "Because component breakouts began in Jan 2018, raw and adjusted totals are identical across all of 2017 (gap = 0).")
]

for m_head, m_txt in meth_bullets:
    p_mh = tf_s6.add_paragraph()
    p_mh.text = f"• {m_head}"
    p_mh.font.name = "Calibri"
    p_mh.font.size = Pt(10.5)
    p_mh.font.bold = True
    p_mh.font.color.rgb = COLOR_NAVY
    
    p_mt = tf_s6.add_paragraph()
    p_mt.text = f"  {m_txt}"
    p_mt.font.name = "Calibri"
    p_mt.font.size = Pt(9.2)
    p_mt.font.color.rgb = COLOR_BODY
    p_mt.space_after = Pt(5)

# Right: Chart Card (Chart 9 Adjustment Gap)
chart_card_s6 = add_card(s6, Inches(5.75), Inches(1.55), Inches(6.783), Inches(5.15), bg_color=COLOR_CARD_BG)
add_image_fitted(s6, "slide_assets/cell_51.png", Inches(5.95), Inches(1.75), Inches(6.383), Inches(4.45))

tb_cf6 = s6.shapes.add_textbox(Inches(5.95), Inches(6.3), Inches(6.383), Inches(0.3))
tf_cf6 = tb_cf6.text_frame
tf_cf6.margin_left = tf_cf6.margin_top = tf_cf6.margin_right = tf_cf6.margin_bottom = 0
p_cf6 = tf_cf6.paragraphs[0]
p_cf6.text = "Chart 9 (EDA Notebook): Citywide monthly adjustment gap (Adjusted Total – Raw Observed Count) across regimes."
p_cf6.font.name = "Calibri"
p_cf6.font.size = Pt(8.5)
p_cf6.font.color.rgb = COLOR_MUTED

add_footer(s6, 6, 8)


# =============================================================
# SLIDE 7: HYPOTHESES FOR FURTHER ANALYSIS
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Research Hypotheses for Downstream Spatial & Policy Analysis")

# 2x2 Grid Layout for Hypotheses
hypotheses = [
    ("H1: Policy & Enforcement Driver of 2022–2023 Peak",
     "Synchronized Citywide Surge",
     "The +57.63% (2022) surge hit nearly every neighborhood simultaneously (Cortez +129%, Outside Perimeter +87%, East Village +50%). This broad synchronization suggests a systemic citywide driver (e.g., pandemic shelter demobilization, eviction moratorium expirations, or regional enforcement shifts) rather than localized dynamics.",
     "Next step: Cross-reference monthly counts against RTFH policy timelines and 311 encampment dispatch logs.",
     COLOR_PRIMARY_BLUE),
    
    ("H2: East Village Asymmetry Reflects Built Environment",
     "East vs. West Infrastructure Divide",
     "East Village sub-areas show consistent divergence: North East and South East EV consistently outcount North West and South West EV across 2018–2025. This asymmetry likely reflects infrastructure factors rather than random density.",
     "Next step: Test spatial clustering (Moran's I / Getis-Ord Gi* in Assignment 5) against shelter locations, trolley transit lines, and zoning.",
     COLOR_NAVY),
     
    ("H3: 2024 Pullback (-43.52%) May Be a Reporting Artifact",
     "Rapid Single-Year Drop Scrutiny",
     "A single-year drop of -43.52% immediately following the historical peak warrants rigorous verification before concluding an actual population reduction occurred. Operational count changes may be an unobserved confounder.",
     "Next step: Benchmark against independent RTFH Point-in-Time (PIT) counts and audit 2024 DSDP canvassing methodology/staffing changes.",
     COLOR_AMBER),
     
    ("H4: Neighborhood Growth Inversely Related to Area Size",
     "Peripheral Displacement & Spillover",
     "The fastest-growing areas (Outside Perimeter +26.90%, Cortez +11.96%, City Center +3.94%) are mid-sized, while East Village grows slowly (+1.64%) and Marina shrinks (-12.76%). Enforcement in core zones may be displacing people to peripheral blocks.",
     "Next step: Conduct spatial adjacency matrix analysis in Assignment 5 to model perimeter spillover dynamics.",
     COLOR_GREEN)
]

for idx, (h_title, h_sub, h_desc, h_action, h_color) in enumerate(hypotheses):
    row = idx // 2
    col = idx % 2
    
    c_left = Inches(0.8 + col * 5.95)
    c_top = Inches(1.55 + row * 2.6)
    c_w = Inches(5.783)
    c_h = Inches(2.45)
    
    # Card container
    add_card(s7, c_left, c_top, c_w, c_h, bg_color=COLOR_CARD_BG)
    
    # Colored top accent bar
    top_bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.02), c_top + Inches(0.02), c_w - Inches(0.04), Inches(0.06))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = h_color
    top_bar.line.fill.background()
    
    tb_h = s7.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.18), c_w - Inches(0.4), c_h - Inches(0.3))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
    
    # Title
    p_ht = tf_h.paragraphs[0]
    p_ht.text = h_title
    p_ht.font.name = "Calibri"
    p_ht.font.size = Pt(11.5)
    p_ht.font.bold = True
    p_ht.font.color.rgb = h_color
    p_ht.space_after = Pt(2)
    
    # Sub
    p_hs = tf_h.add_paragraph()
    p_hs.text = h_sub.upper()
    p_hs.font.name = "Calibri"
    p_hs.font.size = Pt(8.5)
    p_hs.font.bold = True
    p_hs.font.color.rgb = COLOR_MUTED
    p_hs.space_after = Pt(4)
    
    # Desc
    p_hd = tf_h.add_paragraph()
    p_hd.text = h_desc
    p_hd.font.name = "Calibri"
    p_hd.font.size = Pt(9.5)
    p_hd.font.color.rgb = COLOR_BODY
    p_hd.space_after = Pt(5)
    
    # Action / Next step
    p_ha = tf_h.add_paragraph()
    p_ha.text = f"• {h_action}"
    p_ha.font.name = "Calibri"
    p_ha.font.size = Pt(9)
    p_ha.font.bold = True
    p_ha.font.color.rgb = COLOR_NAVY

add_footer(s7, 7, 8)


# =============================================================
# SLIDE 8: DATA LIMITATIONS & NEXT STEPS
# =============================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "Data Limitations, Governance Caveats & Roadmap Ahead")

# Left Column: Data Limitations Card (Width: 5.75 in)
card_lim = add_card(s8, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s8_l = s8.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(5.25), Inches(4.75))
tf_s8_l = tb_s8_l.text_frame
tf_s8_l.word_wrap = True
tf_s8_l.margin_left = tf_s8_l.margin_top = tf_s8_l.margin_right = tf_s8_l.margin_bottom = 0

p_s8_lh = tf_s8_l.paragraphs[0]
p_s8_lh.text = "Identified Data Limitations & Biases"
p_s8_lh.font.name = "Calibri"
p_s8_lh.font.size = Pt(14)
p_s8_lh.font.bold = True
p_s8_lh.font.color.rgb = COLOR_TITLE
p_s8_lh.space_after = Pt(8)

limitations = [
    ("Incomplete 2025 Late-Year Data",
     "28 null values exist in total_count (Jul, Aug, Oct, Nov 2025 across all 7 neighborhoods). These represent unreleased counts (reporting lag) rather than data corruption. 2025 annual figures must be treated as partial-year."),
    ("Outside Perimeter Partial History",
     "Only 56 observations exist for Outside Perimeter (canvassing initiated ~2022). Its reported +26.90%/yr growth rate is the least statistically reliable metric in the neighborhood rankings."),
    ("Pre-2018 Lack of Component Breakouts",
     "Breakouts for tents, hand-built structures, and vehicles are unavailable prior to Jan 2018. Raw and adjusted totals are identical for all of 2017, precluding early multiplier analysis."),
    ("Documented Source-PDF Addition Errors",
     "Task 1.1's 45-cell audit verified a 97.56% fidelity rate against source PDFs, noting known errors (Feb 2018 +30 PDF addition bug, 2019 EV sub-area duplication, Apr 2025 discrepancy).")
]

for l_head, l_desc in limitations:
    p_lh = tf_s8_l.add_paragraph()
    p_lh.text = f"• {l_head}: "
    p_lh.font.name = "Calibri"
    p_lh.font.size = Pt(10.5)
    p_lh.font.bold = True
    p_lh.font.color.rgb = COLOR_RED
    
    p_ld = tf_s8_l.add_paragraph()
    p_ld.text = f"  {l_desc}"
    p_ld.font.name = "Calibri"
    p_ld.font.size = Pt(9.5)
    p_ld.font.color.rgb = COLOR_BODY
    p_ld.space_after = Pt(6)

# Right Column: Next Steps Card (Width: 5.75 in)
card_nxt = add_card(s8, Inches(6.783), Inches(1.55), Inches(5.75), Inches(5.15), bg_color=COLOR_CARD_BG)
tb_s8_r = s8.shapes.add_textbox(Inches(7.033), Inches(1.75), Inches(5.25), Inches(4.75))
tf_s8_r = tb_s8_r.text_frame
tf_s8_r.word_wrap = True
tf_s8_r.margin_left = tf_s8_r.margin_top = tf_s8_r.margin_right = tf_s8_r.margin_bottom = 0

p_s8_rh = tf_s8_r.paragraphs[0]
p_s8_rh.text = "Roadmap Ahead: Assignment 3 Integration"
p_s8_rh.font.name = "Calibri"
p_s8_rh.font.size = Pt(14)
p_s8_rh.font.bold = True
p_s8_rh.font.color.rgb = COLOR_TITLE
p_s8_rh.space_after = Pt(8)

next_steps = [
    ("Immediate Deliverable: Assignment 3",
     "Block-Level Validation & Spatial Integration — transitioning from macro neighborhood aggregates to granular spatial micro-data."),
    ("Granular Block-Level Mapping",
     "Validate street-level counts across 500+ individual block parcels; reconcile bounding street definitions against GIS city shapefiles."),
    ("Spatial Autocorrelation Modeling",
     "Apply Global Moran's I and Local Getis-Ord Gi* hot-spot detection to evaluate whether unsheltered presence clusters around specific transit/shelter nodes."),
    ("Cross-Dataset Validation & Benchmarking",
     "Link monthly DSDP counts with regional RTFH annual Point-in-Time counts and City of San Diego 311 service request dispatches.")
]

for n_head, n_desc in next_steps:
    p_nh = tf_s8_r.add_paragraph()
    p_nh.text = f"• {n_head}: "
    p_nh.font.name = "Calibri"
    p_nh.font.size = Pt(10.5)
    p_nh.font.bold = True
    p_nh.font.color.rgb = COLOR_GREEN
    
    p_nd = tf_s8_r.add_paragraph()
    p_nd.text = f"  {n_desc}"
    p_nd.font.name = "Calibri"
    p_nd.font.size = Pt(9.5)
    p_nd.font.color.rgb = COLOR_BODY
    p_nd.space_after = Pt(6)

add_footer(s8, 8, 8)

# -------------------------------------------------------------
# Save Presentation
# -------------------------------------------------------------
output_path = os.path.join(r"D:\Projects\Downtown-Homeless-Analysis", "EDA_Presentation.pptx")
prs.save(output_path)
print(f"Presentation successfully saved to: {output_path}")
print(f"Slide count: {len(prs.slides)}")
print(f"File size: {os.path.getsize(output_path)} bytes")
