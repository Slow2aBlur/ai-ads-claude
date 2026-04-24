#!/usr/bin/env python3
"""
AI Ads Strategy PDF Report Generator — AI Ads Claude Code Skills
Generates professional, client-ready PDF ad strategy reports with score gauges,
horizontal bar charts, audience personas, campaign structures, ad copy samples,
and budget/ROI projections.

Requires: reportlab (pip install reportlab)

Usage:
  python3 generate_ads_pdf.py                        # Demo mode
  python3 generate_ads_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_ads_pdf.py data.json               # From JSON
  python3 generate_ads_pdf.py data.json output.pdf    # From JSON with custom output
"""

import sys
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Daily Discounts brand
# ---------------------------------------------------------------------------
# All colours come from the DD brand style guide. Brand Teal is the primary
# colour used for headers, table header rows, and key callouts. Signal Orange
# is used sparingly for highlights and alerts only. Charcoal is used for body
# text (never pure black). See STYLE.md Section 14 for full visual rules.
COLORS = {
    "primary": HexColor("#119190"),        # Brand Teal — primary headers, CTAs
    "accent": HexColor("#f85c1a"),         # Signal Orange — sparingly, for alerts
    "highlight": HexColor("#f85c1a"),      # Signal Orange (same as accent)
    "success": HexColor("#13c177"),        # Success Green
    "warning": HexColor("#ffa577"),        # Light Orange — soft warnings
    "danger": HexColor("#e20000"),         # Error Red
    "light_bg": HexColor("#f5f5f5"),       # Mist Grey — section backgrounds
    "text": HexColor("#222c2f"),           # Charcoal — body text
    "text_light": HexColor("#64748b"),     # Muted helper text
    "border": HexColor("#e3e3e3"),         # Line Grey — table lines, dividers
    "white": white,
    "black": black,
}


def score_color(score):
    """Return color based on score value, using the DD palette."""
    if score >= 80:
        return COLORS["success"]       # Green — strong
    elif score >= 60:
        return COLORS["primary"]       # Teal — adequate/strong
    elif score >= 40:
        return COLORS["accent"]        # Orange — weak
    else:
        return COLORS["danger"]        # Red — critical


def score_grade(score):
    """Return letter grade from score."""
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 80:
        return "B+"
    elif score >= 75:
        return "B"
    elif score >= 70:
        return "B-"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "C-"
    elif score >= 50:
        return "D+"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "D-"
    else:
        return "F"


def draw_score_gauge(score, size=120):
    """Create a circular score gauge drawing."""
    d = Drawing(size + 20, size + 20)

    cx = size / 2 + 10
    cy = size / 2 + 10

    # Background circle
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["border"], strokeWidth=2))

    # Score arc (colored ring)
    color = score_color(score)
    inner_r = size / 2 - 8
    d.add(Circle(cx, cy, inner_r,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, inner_r - 12,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score text
    d.add(String(cx, cy - 4, str(int(score)),
                 fontSize=28, fillColor=COLORS["primary"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # "/ 100" label
    d.add(String(cx, cy - 20, "/ 100",
                 fontSize=9, fillColor=COLORS["text_light"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=180):
    """Create horizontal bar charts for category scores."""
    d = Drawing(width, height)

    bar_height = 20
    gap = 10
    max_bar_width = width - 190
    start_y = height - 25
    label_x = 5
    bar_x = 165

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        # Category label
        d.add(String(label_x, y + 5, cat[:25],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        # Score bar
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        # Score label
        d.add(String(bar_x + max_bar_width + 10, y + 5, f"{int(score)}/100",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


# ---------------------------------------------------------------------------
# Custom styles
# ---------------------------------------------------------------------------
def get_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    custom = {
        "title": ParagraphStyle(
            "AdsTitle", parent=styles["Title"],
            fontSize=32, textColor=COLORS["primary"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=38
        ),
        "subtitle": ParagraphStyle(
            "AdsSubtitle", parent=styles["Normal"],
            fontSize=14, textColor=COLORS["text_light"],
            spaceAfter=6, fontName="Helvetica"
        ),
        "heading": ParagraphStyle(
            "AdsHeading", parent=styles["Heading1"],
            fontSize=20, textColor=COLORS["primary"],
            spaceBefore=16, spaceAfter=10,
            fontName="Helvetica-Bold"
        ),
        "subheading": ParagraphStyle(
            "AdsSubheading", parent=styles["Heading2"],
            fontSize=14, textColor=COLORS["accent"],
            spaceBefore=12, spaceAfter=6,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "AdsBody", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14
        ),
        "body_small": ParagraphStyle(
            "AdsBodySmall", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=11
        ),
        "footer": ParagraphStyle(
            "AdsFooter", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text_light"],
            fontName="Helvetica"
        ),
        "grade_large": ParagraphStyle(
            "AdsGrade", parent=styles["Title"],
            fontSize=18, textColor=COLORS["primary"],
            spaceAfter=6, fontName="Helvetica-Bold",
            alignment=1
        ),
    }
    return custom


# ---------------------------------------------------------------------------
# Table style helper
# ---------------------------------------------------------------------------
def standard_table_style(extra=None):
    """Return a standard table style with optional extras."""
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["primary"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    """Generate a professional ads strategy PDF report."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    S = get_styles()
    elements = []

    company = data.get("company_name", data.get("url", "Company"))
    date_str = data.get("date", datetime.now().strftime("%d/%m/%Y"))
    overall_score = data.get("overall_score", 0)
    grade = score_grade(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 1.2 * inch))
    elements.append(Paragraph("Advertising Strategy Report", S["title"]))
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(company, ParagraphStyle(
        "CompanyName", parent=S["subtitle"], fontSize=18,
        textColor=COLORS["accent"], spaceAfter=4
    )))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Report date: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 50))

    # Score gauge
    gauge = draw_score_gauge(overall_score, size=120)
    elements.append(gauge)
    elements.append(Spacer(1, 40))

    # Grade
    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Ad Readiness Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))

    elements.append(Spacer(1, 30))

    # Executive summary
    exec_summary = data.get("executive_summary",
        "This report covers the business's readiness to spend on paid advertising. "
        "It looks at five areas: how well the audience is understood, the quality of "
        "the ad copy and creative, how the campaigns are structured, the competitive "
        "position, and how efficiently the budget is being spent. Each area is scored "
        "and the report sets out what to do next."
    )
    elements.append(Paragraph(exec_summary, S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 2 — SCORE DASHBOARD
    # =====================================================================
    elements.append(Paragraph("Score Dashboard", S["heading"]))
    elements.append(Spacer(1, 6))

    categories = data.get("categories", {})
    default_cats = {
        "Audience Clarity": {"score": 72, "weight": "25%"},
        "Creative Quality": {"score": 65, "weight": "20%"},
        "Funnel Architecture": {"score": 58, "weight": "20%"},
        "Competitive Position": {"score": 70, "weight": "15%"},
        "Budget Efficiency": {"score": 62, "weight": "20%"},
    }
    if not categories:
        categories = default_cats

    cat_names = list(categories.keys())
    cat_scores = [categories[c].get("score", 50) if isinstance(categories[c], dict)
                  else categories[c] for c in cat_names]

    # Bar chart
    chart = create_bar_chart(cat_names, cat_scores)
    elements.append(chart)
    elements.append(Spacer(1, 16))

    # Score breakdown table
    score_data = [["Category", "Score", "Weight", "Rating"]]
    for name, score in zip(cat_names, cat_scores):
        weight = categories[name].get("weight", "--") if isinstance(categories[name], dict) else "--"
        # Five-band rating scale matching STYLE.md
        if score >= 90:
            status = "Excellent"
        elif score >= 75:
            status = "Strong"
        elif score >= 60:
            status = "Adequate"
        elif score >= 40:
            status = "Weak"
        else:
            status = "Critical"
        score_data.append([name, f"{int(score)}/100", weight, status])

    score_table = Table(score_data, colWidths=[160, 80, 60, 100])
    score_style_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    # Color-code status column
    for i, score in enumerate(cat_scores, 1):
        color = score_color(score)
        score_style_extra.append(("TEXTCOLOR", (3, i), (3, i), color))
        score_style_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    score_table.setStyle(standard_table_style(score_style_extra))
    elements.append(score_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 3 — GLOSSARY
    # =====================================================================
    # Every strategy report must include a glossary near the front. STYLE.md
    # Section 5 makes this mandatory. Explains every acronym the reader might
    # meet in the rest of the report.
    elements.append(Paragraph("Glossary", S["heading"]))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "Plain-English explanations of the terms used in this report. "
        "Skim it now and come back to it whenever a term trips you up.",
        S["body"]
    ))
    elements.append(Spacer(1, 10))

    glossary = data.get("glossary", [
        ("ROAS (Return on Ad Spend)", "What you get back in sales for every rand spent on ads. A 4x ROAS means you spent R1.00 and earned R4.00."),
        ("CPA (Cost Per Acquisition)", "What it costs in ads to win one paying customer."),
        ("AOV (Average Order Value)", "The average basket size across the shop."),
        ("LTV (Lifetime Value)", "What a customer is worth across all their purchases, not just the first."),
        ("CPM", "Cost Per 1,000 Impressions. What it costs to show the ad to 1,000 people."),
        ("CTR (Click Through Rate)", "The percentage of people who see the ad and click it."),
        ("Funnel (TOFU / MOFU / BOFU)", "The path a shopper takes from never hearing of you to buying. Top (strangers), Middle (browsing), Bottom (ready to buy)."),
        ("Retargeting", "Ads shown to people who already visited the site."),
        ("Prospecting", "Ads shown to people who have never seen the brand before."),
        ("Lookalike audience", "An audience Facebook or Google builds for you, based on your existing buyers."),
        ("Performance Max (PMax)", "Google campaign that runs across Search, Shopping, YouTube and Gmail, automated."),
        ("UGC", "User Generated Content. Content that looks like a customer made it, not a brand."),
        ("Pixel / Conversions API (CAPI)", "Tracking code on the site. CAPI (server-side) is more accurate than the old browser pixel."),
        ("BFCM", "Black Friday and Cyber Monday."),
        ("BNPL", "Buy Now Pay Later (PayJustNow, PayFlex, Mobicred, Payshap)."),
    ])

    gloss_data = [["Term", "What it means"]]
    for term, meaning in glossary:
        gloss_data.append([
            Paragraph(term, S["body_small"]),
            Paragraph(meaning, S["body_small"]),
        ])

    gloss_table = Table(gloss_data, colWidths=[140, 360])
    gloss_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(gloss_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — AUDIENCE PERSONAS
    # =====================================================================
    elements.append(Paragraph("Audience Analysis", S["heading"]))
    elements.append(Spacer(1, 6))

    personas = data.get("personas", [])
    if not personas:
        personas = [
            {
                "name": "Startup Sarah",
                "demographics": "28-35, Female, Urban, $75K-$120K income",
                "platforms": "Instagram, LinkedIn, YouTube",
                "targeting": "Interest: SaaS, Startup, Entrepreneurship. Lookalike: Website visitors"
            },
            {
                "name": "Enterprise Eric",
                "demographics": "40-55, Male, Suburban, $150K+ income",
                "platforms": "LinkedIn, Google Search, YouTube",
                "targeting": "Job Title: VP/Director/C-Suite. Industry: Technology, Finance"
            },
            {
                "name": "Freelancer Fiona",
                "demographics": "25-38, Any gender, Urban/Remote, $45K-$80K income",
                "platforms": "Instagram, TikTok, Facebook Groups",
                "targeting": "Interest: Freelancing, Side Hustle, Productivity tools"
            },
        ]

    persona_data = [["Persona", "Demographics", "Platforms", "Targeting Parameters"]]
    for p in personas:
        persona_data.append([
            Paragraph(p.get("name", ""), S["body_small"]),
            Paragraph(p.get("demographics", ""), S["body_small"]),
            Paragraph(p.get("platforms", ""), S["body_small"]),
            Paragraph(p.get("targeting", ""), S["body_small"]),
        ])

    persona_table = Table(persona_data, colWidths=[90, 120, 100, 160])
    persona_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(persona_table)

    # Targeting recommendations
    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Targeting recommendations", S["subheading"]))
    recs = data.get("targeting_recommendations", [
        "Start with Lookalike audiences based on existing customers or email lists",
        "Layer interest-based targeting with demographic filters for precision",
        "Use retargeting pools segmented by funnel stage (visited vs. engaged vs. converted)",
        "Test broad vs. narrow audiences — let platform algorithms optimize delivery",
    ])
    for i, rec in enumerate(recs, 1):
        elements.append(Paragraph(f"{i}. {rec}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — CAMPAIGN ARCHITECTURE (renamed from Campaign Structure)
    # =====================================================================
    elements.append(Paragraph("Campaign Architecture", S["heading"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "How the ad plan moves a shopper from first contact to purchase, "
        "then back again for a second order. The budget is split across four "
        "stages based on how far along the buying journey each audience is.",
        S["body"]
    ))
    elements.append(Spacer(1, 10))

    funnel_stages = data.get("funnel_stages", [])
    if not funnel_stages:
        funnel_stages = [
            {
                "stage": "Top (TOFU)",
                "objective": "Awareness. Reach strangers who have never heard of the brand.",
                "budget_pct": "25%",
                "platforms": "Meta, YouTube, TikTok",
                "ad_types": "Video, carousel, story ads",
                "kpis": "Cost per 1,000 impressions, video view rate, reach"
            },
            {
                "stage": "Middle (MOFU)",
                "objective": "Consideration. People who know the brand but have not bought yet.",
                "budget_pct": "28%",
                "platforms": "Meta, Google, LinkedIn",
                "ad_types": "Lead forms, content ads, landing-page traffic",
                "kpis": "Cost per click, click-through rate, cost per lead"
            },
            {
                "stage": "Bottom (BOFU)",
                "objective": "Conversion. Close the sale for people ready to buy.",
                "budget_pct": "22%",
                "platforms": "Google Search, Meta, LinkedIn",
                "ad_types": "Search ads, dynamic product ads, testimonial ads",
                "kpis": "Cost per acquisition, return on ad spend, conversion rate"
            },
            {
                "stage": "Retargeting",
                "objective": "Recovery and loyalty. Bring back recent visitors and keep existing customers warm.",
                "budget_pct": "25%",
                "platforms": "Meta, Google Display, YouTube",
                "ad_types": "Dynamic retargeting, cart-abandonment, win-back",
                "kpis": "Return on ad spend, frequency, cost per acquisition"
            },
        ]

    funnel_data = [["Funnel Stage", "Objective", "Budget", "Platforms", "Ad Types", "KPIs"]]
    for stage in funnel_stages:
        funnel_data.append([
            Paragraph(stage.get("stage", ""), S["body_small"]),
            Paragraph(stage.get("objective", ""), S["body_small"]),
            stage.get("budget_pct", ""),
            Paragraph(stage.get("platforms", ""), S["body_small"]),
            Paragraph(stage.get("ad_types", ""), S["body_small"]),
            Paragraph(stage.get("kpis", ""), S["body_small"]),
        ])

    funnel_table = Table(funnel_data, colWidths=[80, 90, 50, 80, 90, 80])
    funnel_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    elements.append(funnel_table)

    # Budget allocation summary
    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Budget flow", S["subheading"]))
    elements.append(Paragraph(
        "Top (25%) reaches strangers with high-reach formats. "
        "Middle (28%) warms up people who know the brand but have not bought. "
        "Bottom (22%) closes sales with high-intent targeting. "
        "Retargeting (25%) brings back visitors and keeps customers loyal. "
        "Fifty percent of the budget sits in Middle and Bottom combined, where the return is strongest.",
        S["body"]
    ))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — CREATIVE DIRECTION (renamed from Ad Copy Samples)
    # =====================================================================
    elements.append(Paragraph("Creative Direction", S["heading"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Sample ad copy across the priority platforms. A hook is the first line "
        "of the ad. If it does not stop the scroll, nothing else matters.",
        S["body"]
    ))
    elements.append(Spacer(1, 10))

    ad_samples = data.get("ad_samples", [])
    if not ad_samples:
        ad_samples = [
            {
                "platform": "Meta (Facebook)",
                "headline": "Stop Wasting Ad Spend",
                "primary_text": "87% of small businesses lose money on ads because they skip strategy. Get a free AI-powered ad audit and find out where your budget is leaking.",
                "cta": "Get Free Audit"
            },
            {
                "platform": "Google Search",
                "headline": "AI Ad Strategy Tool | Free Audit",
                "primary_text": "See exactly where your ad budget is going wrong. AI-powered analysis across 5 dimensions. Results in 60 seconds.",
                "cta": "Start Free Audit"
            },
            {
                "platform": "LinkedIn",
                "headline": "Your Competitors Are Outspending You",
                "primary_text": "We analyzed 1,000+ ad accounts. The top performers all share 5 traits. Find out if your campaigns measure up with our free Ad Readiness Score.",
                "cta": "Get Your Score"
            },
            {
                "platform": "Instagram Story",
                "headline": "Is Your Ad Budget Working?",
                "primary_text": "Swipe up to get your free Ad Readiness Score. AI analyzes your audience, creative, funnel, and budget in under 60 seconds.",
                "cta": "Swipe Up"
            },
            {
                "platform": "YouTube Pre-Roll",
                "headline": "The #1 Reason Ads Fail",
                "primary_text": "It's not your budget. It's not your creative. It's your targeting. Watch how AI fixes ad targeting in 60 seconds.",
                "cta": "Learn More"
            },
            {
                "platform": "TikTok",
                "headline": "POV: Your ads finally work",
                "primary_text": "I ran this AI tool on my ad account and it found $2,300/mo in wasted spend. Here's exactly what it flagged.",
                "cta": "Try It Free"
            },
        ]

    ad_data = [["Platform", "Headline", "Primary Text", "CTA"]]
    for ad in ad_samples:
        ad_data.append([
            Paragraph(ad.get("platform", ""), S["body_small"]),
            Paragraph(ad.get("headline", ""), S["body_small"]),
            Paragraph(ad.get("primary_text", ""), S["body_small"]),
            Paragraph(ad.get("cta", ""), S["body_small"]),
        ])

    ad_table = Table(ad_data, colWidths=[80, 100, 200, 70])
    ad_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(ad_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 7 — BUDGET AND RETURN ON INVESTMENT
    # =====================================================================
    elements.append(Paragraph("Budget and Return on Investment", S["heading"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Profitability depends on repeat custom, the email and WhatsApp list, "
        "and Black Friday — not on cheaper clicks. The retention infrastructure "
        "is where the economics actually work.",
        S["body"]
    ))
    elements.append(Spacer(1, 10))

    # Budget allocation table (pie chart data as table)
    elements.append(Paragraph("Budget allocation by platform", S["subheading"]))

    budget_alloc = data.get("budget_allocation", [])
    if not budget_alloc:
        budget_alloc = [
            {"platform": "Meta (Facebook/Instagram)", "allocation": "35%", "monthly": "$1,750"},
            {"platform": "Google Ads (Search + Display)", "allocation": "30%", "monthly": "$1,500"},
            {"platform": "YouTube Ads", "allocation": "15%", "monthly": "$750"},
            {"platform": "LinkedIn Ads", "allocation": "10%", "monthly": "$500"},
            {"platform": "TikTok Ads", "allocation": "5%", "monthly": "$250"},
            {"platform": "Pinterest Ads", "allocation": "5%", "monthly": "$250"},
        ]

    alloc_data = [["Platform", "Allocation", "Monthly Budget"]]
    for item in budget_alloc:
        alloc_data.append([
            item.get("platform", ""),
            item.get("allocation", ""),
            item.get("monthly", ""),
        ])

    alloc_table = Table(alloc_data, colWidths=[220, 100, 120])
    alloc_table.setStyle(standard_table_style([
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(alloc_table)

    elements.append(Spacer(1, 20))

    # Projected metrics
    elements.append(Paragraph("Projected monthly metrics", S["subheading"]))

    projections = data.get("projections", {})
    if not projections:
        projections = {
            "total_budget": "R100,000.00 per month",
            "impressions": "250,000 to 400,000",
            "clicks": "3,500 to 6,000",
            "ctr": "1.4% to 1.8%",
            "conversions": "85 to 150",
            "cpa": "R500.00 to R750.00",
            "roas": "3.8x to 4.2x",
            "revenue_estimate": "R380,000.00 to R420,000.00",
        }

    proj_data = [["Metric", "Projected range"]]
    metric_labels = {
        "total_budget": "Total monthly budget",
        "impressions": "Impressions (ad views)",
        "clicks": "Clicks",
        "ctr": "Click-through rate",
        "conversions": "Conversions (purchases)",
        "cpa": "Cost per new customer",
        "roas": "Return on ad spend",
        "revenue_estimate": "Estimated revenue",
    }
    for key, label in metric_labels.items():
        value = projections.get(key, "--")
        proj_data.append([label, value])

    proj_table = Table(proj_data, colWidths=[240, 200])
    proj_style_extra = [("ALIGN", (1, 0), (1, -1), "CENTER")]
    # Highlight ROAS row
    roas_row = list(metric_labels.keys()).index("roas") + 1
    proj_style_extra.append(("TEXTCOLOR", (1, roas_row), (1, roas_row), COLORS["success"]))
    proj_style_extra.append(("FONTNAME", (1, roas_row), (1, roas_row), "Helvetica-Bold"))
    # Highlight revenue row
    rev_row = list(metric_labels.keys()).index("revenue_estimate") + 1
    proj_style_extra.append(("TEXTCOLOR", (1, rev_row), (1, rev_row), COLORS["success"]))
    proj_style_extra.append(("FONTNAME", (1, rev_row), (1, rev_row), "Helvetica-Bold"))
    proj_table.setStyle(standard_table_style(proj_style_extra))
    elements.append(proj_table)

    elements.append(Spacer(1, 24))

    # Footer
    elements.append(Paragraph(
        "Daily Discounts Advertising Strategy Report",
        S["footer"]
    ))

    # Build PDF
    doc.build(elements)
    return output_path


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def get_demo_data():
    """Return sample data for demo mode. Daily Discounts-style SA e-commerce."""
    return {
        "company_name": "Daily Discounts",
        "url": "https://dailydiscounts.co.za",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "overall_score": 78,
        "executive_summary": (
            "Daily Discounts should start spending R100,000.00 a month on ads, but the "
            "business cannot lean on the word 'discounts' to sell. The actual savings "
            "sit between 2% and 14%, which is not deep enough to pull in the flash-deal "
            "crowd. What the business offers is trusted brand names, free delivery, a "
            "one-year warranty, and a real human to talk to when something goes wrong. "
            "That is the story the ads must tell. A well-run programme should return "
            "R3.80 to R4.20 in sales per R1.00 of ad spend within 90 days."
        ),
        "categories": {
            "Audience clarity": {"score": 82, "weight": "25%"},
            "Creative quality": {"score": 87, "weight": "20%"},
            "Campaign architecture": {"score": 94, "weight": "20%"},
            "Competitive position": {"score": 52, "weight": "15%"},
            "Budget efficiency": {"score": 68, "weight": "20%"},
        },
        "personas": [
            {
                "name": "Thandi",
                "demographics": "34 to 48, 70% female, household income R18,000.00 to R35,000.00, metros plus smaller towns",
                "platforms": "Facebook 60%, Google Shopping 30%, TikTok 10%",
                "targeting": "Interest: home appliances, bargain hunters, mid-tier brands. Lookalike from customer list."
            },
            {
                "name": "Johan",
                "demographics": "35 to 65, 65% male, household income R25,000.00 to R80,000.00, national with smaller-town skew",
                "platforms": "Google Search 50%, Facebook 40%, TikTok 10%",
                "targeting": "Keywords: inverter, generator, load-shedding backup. Bid-up during Stage 4+."
            },
            {
                "name": "Megan",
                "demographics": "30 to 50, 60% female, household income R60,000.00 to R150,000.00, Sandton, Constantia, Umhlanga",
                "platforms": "Facebook and Instagram 60%, Google PMax 30%, Pinterest 10%",
                "targeting": "Interest: home decor, kitchen appliances, premium brands. Lookalike from high-AOV buyers."
            },
        ],
        "targeting_recommendations": [
            "Start with Lookalike audiences built from the existing customer list",
            "Layer interest targeting with demographic filters for precision",
            "Use retargeting segmented by funnel stage: visited, engaged, cart-added, purchased",
            "Test broad versus narrow audiences and let the platforms optimise delivery",
        ],
        "funnel_stages": [
            {
                "stage": "Top (TOFU)",
                "objective": "Awareness. Reach strangers who have never heard of the brand.",
                "budget_pct": "25%",
                "platforms": "Meta, YouTube, TikTok",
                "ad_types": "Video, carousel, story ads",
                "kpis": "Cost per 1,000 impressions, video view rate, reach"
            },
            {
                "stage": "Middle (MOFU)",
                "objective": "Consideration. People who know the brand but have not bought yet.",
                "budget_pct": "28%",
                "platforms": "Meta, Google, LinkedIn",
                "ad_types": "Lead forms, content ads, landing-page traffic",
                "kpis": "Cost per click, click-through rate, cost per lead"
            },
            {
                "stage": "Bottom (BOFU)",
                "objective": "Conversion. Close the sale for people ready to buy.",
                "budget_pct": "22%",
                "platforms": "Google Search, Meta",
                "ad_types": "Search ads, dynamic product ads, testimonial ads",
                "kpis": "Cost per acquisition, return on ad spend, conversion rate"
            },
            {
                "stage": "Retargeting",
                "objective": "Recovery and loyalty. Bring back recent visitors.",
                "budget_pct": "25%",
                "platforms": "Meta, Google Display, YouTube",
                "ad_types": "Dynamic retargeting, cart-abandonment, win-back",
                "kpis": "Return on ad spend, frequency, cost per acquisition"
            },
        ],
        "ad_samples": [
            {
                "platform": "Meta (Facebook)",
                "headline": "Still paying Takealot prices in 2026?",
                "primary_text": "The same Bosch, Defy and Midea appliances you know, 14% cheaper. Free delivery. One-year warranty.",
                "cta": "Shop Now"
            },
            {
                "platform": "Google Search",
                "headline": "Buy fridge online SA",
                "primary_text": "Trusted brands at everyday savings. Free delivery across South Africa. One-year warranty.",
                "cta": "View Deals"
            },
            {
                "platform": "Instagram Reels",
                "headline": "Load-shedding broke your kettle?",
                "primary_text": "Replace it for under R500.00. Free delivery. Trusted brands only.",
                "cta": "Shop Kettles"
            },
            {
                "platform": "Instagram Story",
                "headline": "Fridge died?",
                "primary_text": "You have got 24 hours before the meat spoils. Same-day delivery in Gauteng, next-day nationally.",
                "cta": "Browse Fridges"
            },
            {
                "platform": "YouTube Pre-Roll",
                "headline": "The appliance brands Makro sells, 14% cheaper.",
                "primary_text": "Same Bosch. Same Defy. Same Midea. Better price. Question the markup.",
                "cta": "Learn More"
            },
            {
                "platform": "TikTok",
                "headline": "POV: Your 55-inch TV came on budget",
                "primary_text": "Only 8 Telefunken 55s left at last month's price. Gone Friday. Free delivery.",
                "cta": "Grab Yours"
            },
        ],
        "budget_allocation": [
            {"platform": "Google (Shopping + Performance Max + Search)", "allocation": "65%", "monthly": "R65,000.00"},
            {"platform": "Facebook / Instagram (Advantage+, retargeting, prospecting)", "allocation": "25%", "monthly": "R25,000.00"},
            {"platform": "TikTok (creator-led tests)", "allocation": "10%", "monthly": "R10,000.00"},
        ],
        "projections": {
            "total_budget": "R100,000.00 per month",
            "impressions": "1,200,000 to 1,800,000",
            "clicks": "18,000 to 26,000",
            "ctr": "1.4% to 1.8%",
            "conversions": "130 to 200",
            "cpa": "R500.00 to R750.00",
            "roas": "3.8x to 4.2x",
            "revenue_estimate": "R380,000.00 to R420,000.00",
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        # Demo mode
        data = get_demo_data()
        output = "ADS-STRATEGY-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    # JSON input mode
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "ADS-STRATEGY-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
