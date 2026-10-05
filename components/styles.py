"""
AutoElite — Centralized Style System
All CSS variables, component styles, and layout rules live here.
Import get_css() in app.py and inject once with st.markdown().
"""

# ── Brand tokens ──────────────────────────────────────────────────────────────
COLORS = {
    "black":        "#0A0A0B",
    "charcoal":     "#1A1A1F",
    "dark":         "#22222A",
    "mid":          "#3A3A45",
    "gray":         "#8A8A95",
    "light":        "#C8C8D0",
    "fog":          "#E8E8F0",
    "white":        "#FAFAFA",
    "accent":       "#C8A84B",   # signature gold
    "accent_dim":   "#A0843A",
    "accent_light": "#F5E6B8",
    "danger":       "#D94040",
    "success":      "#2E7D52",
    "card_bg":      "#1E1E26",
    "card_border":  "#2A2A35",
}


def get_css() -> str:
    """Return the complete AutoElite CSS string."""
    return f"""
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css');

/* ── CSS Reset & Root ────────────────────────────────────────────────── */
:root {{
    --black:        {COLORS["black"]};
    --charcoal:     {COLORS["charcoal"]};
    --dark:         {COLORS["dark"]};
    --mid:          {COLORS["mid"]};
    --gray:         {COLORS["gray"]};
    --light:        {COLORS["light"]};
    --fog:          {COLORS["fog"]};
    --white:        {COLORS["white"]};
    --accent:       {COLORS["accent"]};
    --accent-dim:   {COLORS["accent_dim"]};
    --accent-light: {COLORS["accent_light"]};
    --danger:       {COLORS["danger"]};
    --success:      {COLORS["success"]};
    --card-bg:      {COLORS["card_bg"]};
    --card-border:  {COLORS["card_border"]};
    --radius:       12px;
    --radius-lg:    16px;
    --radius-sm:    8px;
}}

/* ── Streamlit Shell Overrides ────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: var(--black) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--white) !important;
}}

/* Hide Streamlit default branding */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

/* Remove default padding */
[data-testid="stAppViewContainer"] > .main {{
    padding: 0 !important;
}}
.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: var(--charcoal) !important;
    border-right: 1px solid var(--card-border) !important;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {{
    color: var(--gray) !important;
    font-size: 13px !important;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] label,
[data-testid="stSidebar"] [data-testid="stSlider"] label {{
    color: var(--gray) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Selectbox / Input */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input,
[data-testid="stNumberInput"] > div > div > input,
[data-testid="stTextArea"] > div > div > textarea,
[data-testid="stDateInput"] > div > div > input {{
    background: var(--dark) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}}
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stTextInput"] > div > div:focus-within {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,168,75,.15) !important;
}}

/* Slider */
[data-testid="stSlider"] > div > div > div > div {{
    background: var(--accent) !important;
}}
[data-testid="stSlider"] .st-bx {{
    background: var(--mid) !important;
}}

/* Buttons */
.stButton > button {{
    background: var(--accent) !important;
    color: var(--black) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{
    background: var(--accent-dim) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(200,168,75,.25) !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* Ghost button variant — wrap in <div class="btn-ghost-wrap"> */
.btn-ghost-wrap .stButton > button {{
    background: transparent !important;
    color: var(--light) !important;
    border: 1px solid var(--card-border) !important;
}}
.btn-ghost-wrap .stButton > button:hover {{
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: transparent !important;
    box-shadow: none !important;
}}

/* Danger button */
.btn-danger-wrap .stButton > button {{
    background: rgba(217,64,64,.1) !important;
    color: var(--danger) !important;
    border: 1px solid rgba(217,64,64,.25) !important;
}}
.btn-danger-wrap .stButton > button:hover {{
    background: rgba(217,64,64,.2) !important;
    box-shadow: none !important;
    transform: none !important;
}}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid var(--card-border) !important;
    gap: 0 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important;
    color: var(--gray) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
    background: transparent !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background: var(--accent) !important;
    height: 2px !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-border"] {{
    background: var(--card-border) !important;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: var(--radius) !important;
    padding: 20px 24px !important;
}}
[data-testid="stMetricLabel"] {{
    color: var(--gray) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-weight: 500 !important;
}}
[data-testid="stMetricValue"] {{
    color: var(--accent) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 12px !important;
}}

/* Expander */
[data-testid="stExpander"] {{
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: var(--radius) !important;
}}
[data-testid="stExpander"] summary {{
    color: var(--light) !important;
    font-weight: 500 !important;
}}

/* Divider */
hr {{
    border-color: var(--card-border) !important;
    margin: 24px 0 !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--black); }}
::-webkit-scrollbar-thumb {{ background: var(--mid); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--gray); }}

/* ── AutoElite Custom Components ──────────────────────────────────────── */

/* Navigation bar */
.ae-nav {{
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(10,10,11,0.94);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(200,168,75,0.15);
    padding: 0 40px;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 32px;
}}
.ae-logo {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--white);
    letter-spacing: 0.5px;
    text-decoration: none;
    flex-shrink: 0;
}}
.ae-logo span {{ color: var(--accent); }}
.ae-nav-links {{
    display: flex;
    gap: 4px;
    flex: 1;
    align-items: center;
}}
.ae-nav-link {{
    background: none;
    border: none;
    color: var(--gray);
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.3px;
    font-family: 'Inter', sans-serif;
    text-decoration: none;
}}
.ae-nav-link:hover {{ color: var(--white); background: rgba(255,255,255,0.06); }}
.ae-nav-link.active {{ color: var(--accent); }}

/* Hero section */
.ae-hero {{
    min-height: 540px;
    background: linear-gradient(135deg, #0A0A0B 0%, #1A1A1F 50%, #0D0D12 100%);
    display: flex;
    align-items: center;
    padding: 60px 60px;
    position: relative;
    overflow: hidden;
}}
.ae-hero-bg {{
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 70% 50%, rgba(200,168,75,0.12) 0%, transparent 65%);
    pointer-events: none;
}}
.ae-hero-eyebrow {{
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 20px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}}
.ae-hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: 58px;
    line-height: 1.08;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 20px;
}}
.ae-hero-title em {{
    font-style: normal;
    color: var(--accent);
}}
.ae-hero-sub {{
    font-size: 17px;
    color: var(--gray);
    line-height: 1.6;
    max-width: 440px;
    font-weight: 300;
    margin-bottom: 36px;
}}

/* Section */
.ae-section {{
    padding: 64px 40px;
}}
.ae-section-dark {{
    background: var(--charcoal);
}}
.ae-eyebrow {{
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    margin-bottom: 8px;
}}
.ae-section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 10px;
    line-height: 1.2;
}}
.ae-section-sub {{
    font-size: 15px;
    color: var(--gray);
    line-height: 1.6;
    max-width: 500px;
}}
.ae-page-header {{
    padding: 40px 40px 0;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 40px;
    padding-bottom: 32px;
}}
.ae-page-title {{
    font-family: 'Playfair Display', serif;
    font-size: 40px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 6px;
}}
.ae-page-sub {{
    font-size: 15px;
    color: var(--gray);
}}

/* Vehicle card */
.ae-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all 0.25s ease;
    height: 100%;
}}
.ae-card:hover {{
    border-color: rgba(200,168,75,0.35);
    transform: translateY(-3px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}}
.ae-card-img {{
    width: 100%;
    aspect-ratio: 16/9;
    object-fit: cover;
    display: block;
    background: var(--dark);
}}
.ae-card-img-placeholder {{
    width: 100%;
    aspect-ratio: 16/9;
    background: linear-gradient(135deg, var(--dark), var(--charcoal));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    color: var(--mid);
}}
.ae-card-body {{
    padding: 20px;
}}
.ae-card-brand {{
    font-size: 11px;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 4px;
}}
.ae-card-name {{
    font-size: 17px;
    font-weight: 600;
    color: var(--white);
    margin-bottom: 10px;
    line-height: 1.2;
}}
.ae-card-meta {{
    display: flex;
    gap: 14px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}}
.ae-card-meta-item {{
    font-size: 12px;
    color: var(--gray);
    display: flex;
    align-items: center;
    gap: 4px;
}}
.ae-card-price {{
    font-size: 22px;
    font-weight: 700;
    color: var(--accent);
    font-family: 'Playfair Display', serif;
    margin-bottom: 4px;
}}
.ae-card-emi {{
    font-size: 11px;
    color: var(--gray);
    margin-bottom: 16px;
}}

/* Status badge */
.ae-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.ae-badge-available {{
    background: rgba(46,125,82,0.15);
    color: #4CAF50;
    border: 1px solid rgba(46,125,82,0.25);
}}
.ae-badge-reserved {{
    background: rgba(200,168,75,0.12);
    color: var(--accent);
    border: 1px solid rgba(200,168,75,0.2);
}}
.ae-badge-sold {{
    background: rgba(217,64,64,0.12);
    color: #EF5350;
    border: 1px solid rgba(217,64,64,0.2);
}}
.ae-badge-coming {{
    background: rgba(138,138,149,0.12);
    color: var(--gray);
    border: 1px solid rgba(138,138,149,0.2);
}}
.ae-badge-new {{
    background: rgba(200,168,75,0.9);
    color: var(--black);
    font-weight: 700;
}}

/* Why / Feature cards */
.ae-why-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 28px 24px;
    transition: border-color 0.2s;
    height: 100%;
}}
.ae-why-card:hover {{
    border-color: rgba(200,168,75,0.25);
}}
.ae-why-icon {{
    font-size: 28px;
    color: var(--accent);
    margin-bottom: 14px;
}}
.ae-why-num {{
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
    margin-bottom: 14px;
}}
.ae-why-title {{
    font-size: 16px;
    font-weight: 600;
    color: var(--white);
    margin-bottom: 8px;
}}
.ae-why-text {{
    font-size: 13px;
    color: var(--gray);
    line-height: 1.6;
}}

/* Service card */
.ae-svc-card {{
    background: var(--card-bg);
    border: 1px solid rgba(200,168,75,0.15);
    border-radius: var(--radius);
    padding: 28px 24px;
    transition: all 0.2s;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}
.ae-svc-card:hover {{
    border-color: rgba(200,168,75,0.3);
    transform: translateY(-2px);
}}
.ae-svc-icon {{
    font-size: 32px;
    color: var(--accent);
}}
.ae-svc-title {{
    font-size: 17px;
    font-weight: 600;
    color: var(--white);
}}
.ae-svc-text {{
    font-size: 13px;
    color: var(--gray);
    line-height: 1.6;
    flex: 1;
}}

/* Spec card */
.ae-spec-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
}}
.ae-spec-icon {{
    font-size: 24px;
    color: var(--accent);
    margin-bottom: 8px;
}}
.ae-spec-label {{
    font-size: 10px;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
    font-weight: 500;
}}
.ae-spec-val {{
    font-size: 16px;
    font-weight: 600;
    color: var(--white);
}}

/* KPI / Dashboard cards */
.ae-kpi-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 24px;
}}
.ae-kpi-label {{
    font-size: 11px;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
    margin-bottom: 8px;
}}
.ae-kpi-val {{
    font-size: 32px;
    font-weight: 700;
    color: var(--white);
    font-family: 'Playfair Display', serif;
    margin-bottom: 4px;
}}
.ae-kpi-delta-pos {{
    font-size: 12px;
    color: #4CAF50;
}}
.ae-kpi-delta-neg {{
    font-size: 12px;
    color: #EF5350;
}}

/* Search panel */
.ae-search-panel {{
    background: var(--charcoal);
    border: 1px solid rgba(200,168,75,0.2);
    border-radius: var(--radius-lg);
    padding: 28px 32px;
    margin: -28px 40px 0;
    position: relative;
    z-index: 10;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}

/* Finance panel */
.ae-finance-panel {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    padding: 32px;
}}
.ae-emi-display {{
    text-align: center;
    padding: 28px;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 24px;
}}
.ae-emi-label {{
    font-size: 11px;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}
.ae-emi-amount {{
    font-size: 48px;
    font-weight: 700;
    color: var(--accent);
    font-family: 'Playfair Display', serif;
}}
.ae-emi-period {{
    font-size: 14px;
    color: var(--gray);
    margin-top: 4px;
}}
.ae-breakdown-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(42,42,53,0.5);
    font-size: 14px;
}}
.ae-breakdown-row:last-child {{
    border-bottom: none;
    padding-top: 14px;
    font-weight: 600;
}}
.ae-breakdown-label {{ color: var(--gray); }}
.ae-breakdown-val {{ color: var(--white); font-weight: 600; }}
.ae-finance-note {{
    font-size: 11px;
    color: var(--mid);
    text-align: center;
    margin-top: 16px;
    font-style: italic;
}}

/* Booking step */
.ae-step {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 20px 24px;
    display: flex;
    gap: 18px;
    align-items: flex-start;
}}
.ae-step-active {{
    border-color: rgba(200,168,75,0.4);
    background: rgba(200,168,75,0.04);
}}
.ae-step-done {{
    border-color: rgba(46,125,82,0.3);
    background: rgba(46,125,82,0.04);
}}
.ae-step-num {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: 2px solid var(--mid);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: var(--gray);
    flex-shrink: 0;
    font-family: 'Inter', sans-serif;
}}
.ae-step-title {{
    font-size: 15px;
    font-weight: 600;
    color: var(--white);
    margin-bottom: 4px;
}}
.ae-step-text {{
    font-size: 13px;
    color: var(--gray);
    line-height: 1.5;
}}

/* Compare table */
.ae-compare-table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--card-bg);
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--card-border);
}}
.ae-compare-table th {{
    padding: 16px 20px;
    text-align: left;
    font-size: 12px;
    font-weight: 600;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--card-border);
    background: var(--dark);
    font-family: 'Inter', sans-serif;
}}
.ae-compare-table td {{
    padding: 13px 20px;
    font-size: 14px;
    color: var(--light);
    border-bottom: 1px solid rgba(42,42,53,0.5);
    font-family: 'Inter', sans-serif;
}}
.ae-compare-table td:first-child {{
    color: var(--gray);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}}
.ae-compare-table tr:last-child td {{ border-bottom: none; }}
.ae-compare-table tr:hover td {{ background: rgba(255,255,255,0.02); }}
.ae-compare-best {{
    color: var(--accent) !important;
    font-weight: 700 !important;
}}

/* Admin table */
.ae-admin-table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    overflow: hidden;
    font-family: 'Inter', sans-serif;
}}
.ae-admin-table th {{
    padding: 14px 20px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--card-border);
    background: var(--dark);
}}
.ae-admin-table td {{
    padding: 14px 20px;
    font-size: 13px;
    color: var(--light);
    border-bottom: 1px solid rgba(42,42,53,0.5);
    vertical-align: middle;
}}
.ae-admin-table tr:last-child td {{ border-bottom: none; }}
.ae-admin-table tr:hover td {{ background: rgba(255,255,255,0.02); }}

/* Empty state */
.ae-empty {{
    text-align: center;
    padding: 80px 40px;
}}
.ae-empty-icon {{ font-size: 56px; color: var(--mid); margin-bottom: 20px; }}
.ae-empty-title {{
    font-size: 20px;
    font-weight: 600;
    color: var(--light);
    margin-bottom: 8px;
}}
.ae-empty-text {{
    font-size: 14px;
    color: var(--gray);
    max-width: 320px;
    margin: 0 auto 24px;
    line-height: 1.6;
}}

/* Toast / success message */
.ae-toast {{
    background: var(--charcoal);
    border: 1px solid var(--card-border);
    border-radius: var(--radius);
    padding: 14px 18px;
    font-size: 13px;
    color: var(--white);
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
}}
.ae-toast-success {{ border-color: rgba(46,125,82,0.3); }}
.ae-toast-info    {{ border-color: rgba(200,168,75,0.3); }}

/* Form divider */
.ae-form-divider {{
    font-size: 11px;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(200,168,75,0.15);
    margin: 24px 0 16px;
    font-family: 'Inter', sans-serif;
}}

/* Detail hero */
.ae-detail-brand {{
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 6px;
}}
.ae-detail-name {{
    font-family: 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 700;
    color: var(--white);
    line-height: 1.1;
    margin-bottom: 6px;
}}
.ae-detail-variant {{
    font-size: 18px;
    color: var(--gray);
    font-weight: 300;
    margin-bottom: 18px;
}}
.ae-detail-price {{
    font-size: 34px;
    font-weight: 700;
    color: var(--accent);
    font-family: 'Playfair Display', serif;
    margin-bottom: 6px;
}}
.ae-detail-meta {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--card-border);
}}
.ae-detail-meta-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--gray);
}}

/* CTA banner */
.ae-cta {{
    background: linear-gradient(135deg, var(--charcoal), var(--dark));
    border-top: 1px solid var(--card-border);
    border-bottom: 1px solid var(--card-border);
    padding: 80px 40px;
    text-align: center;
}}
.ae-cta-title {{
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 12px;
}}
.ae-cta-sub {{
    font-size: 16px;
    color: var(--gray);
    margin-bottom: 32px;
}}

/* Footer */
.ae-footer {{
    background: var(--charcoal);
    border-top: 1px solid var(--card-border);
    padding: 48px 40px 24px;
}}
.ae-footer-logo {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 6px;
}}
.ae-footer-logo span {{ color: var(--accent); }}
.ae-footer-col-title {{
    font-size: 11px;
    font-weight: 600;
    color: var(--white);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    font-family: 'Inter', sans-serif;
}}
.ae-footer-link {{
    font-size: 13px;
    color: var(--gray);
    cursor: pointer;
    transition: color 0.15s;
    display: block;
    margin-bottom: 10px;
    text-decoration: none;
    font-family: 'Inter', sans-serif;
}}
.ae-footer-link:hover {{ color: var(--accent); }}
.ae-footer-bottom {{
    border-top: 1px solid var(--card-border);
    padding-top: 20px;
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.ae-footer-copy {{
    font-size: 12px;
    color: var(--mid);
}}

/* Admin bar */
.ae-admin-bar {{
    background: var(--charcoal);
    border-bottom: 1px solid var(--card-border);
    padding: 12px 40px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.ae-admin-tag {{
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    background: rgba(200,168,75,0.1);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(200,168,75,0.2);
}}
.ae-confirm-box {{
    background: rgba(217,64,64,0.06);
    border: 1px solid rgba(217,64,64,0.2);
    border-radius: var(--radius-sm);
    padding: 16px;
    margin-bottom: 16px;
    font-size: 14px;
    color: var(--light);
    line-height: 1.6;
}}

/* Inline info box */
.ae-info-box {{
    background: rgba(200,168,75,0.06);
    border: 1px solid rgba(200,168,75,0.2);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    font-size: 13px;
    color: var(--light);
    line-height: 1.6;
}}

/* ── Responsive / Mobile ─────────────────────────────────────────────── */
@media (max-width: 900px) {{
    /* Streamlit's horizontal column groups */
    [data-testid="stHorizontalBlock"] {{
        grid-template-columns: 1fr !important;
        flex-wrap: wrap !important;
        gap: 1rem !important;
    }}

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }}

    .block-container {{
        width: 100% !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}

    /* Keep Streamlit sidebar usable on tablets/phones */
    [data-testid="stSidebar"] {{
        min-width: min(86vw, 320px) !important;
        max-width: min(86vw, 320px) !important;
    }}

    /* Navigation */
    .ae-nav {{
        height: auto !important;
        min-height: 60px !important;
        padding: 10px 16px !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
        align-items: center !important;
    }}

    .ae-logo {{
        font-size: 20px !important;
        margin-right: auto !important;
    }}

    .ae-nav > div:last-child {{
        margin-left: 0 !important;
        flex-shrink: 0 !important;
    }}

    .ae-nav-links {{
        order: 3 !important;
        flex: 0 0 100% !important;
        width: 100% !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        scrollbar-width: none !important;
        padding-bottom: 2px !important;
        gap: 2px !important;
    }}

    .ae-nav-links::-webkit-scrollbar {{
        display: none !important;
    }}

    .ae-nav-link {{
        display: inline-flex !important;
        flex: 0 0 auto !important;
        font-size: 12px !important;
        padding: 7px 10px !important;
    }}

    /* Hero */
    .ae-hero {{
        min-height: 500px !important;
        padding: 48px 22px 40px !important;
        align-items: flex-start !important;
    }}

    .ae-hero > div[style*="max-width:580px"] {{
        max-width: 100% !important;
        width: 100% !important;
    }}

    .ae-hero-title {{
        font-size: clamp(34px, 8vw, 46px) !important;
        line-height: 1.08 !important;
    }}

    .ae-hero-sub {{
        font-size: 15px !important;
        max-width: 100% !important;
        margin-bottom: 26px !important;
    }}

    .ae-hero svg[style*="width:520px"],
    .ae-hero svg[style*="width:560px"] {{
        width: 420px !important;
        max-width: 90vw !important;
        height: auto !important;
        opacity: .18 !important;
        right: -90px !important;
        top: auto !important;
        bottom: 0 !important;
        transform: none !important;
    }}

    .ae-hero svg[style*="width:520px"] {{
        right: -70px !important;
        bottom: -40px !important;
    }}

    .ae-hero-eyebrow {{
        font-size: 9px !important;
        letter-spacing: 2px !important;
    }}

    /* Common page spacing */
    .ae-section {{
        padding: 42px 18px !important;
    }}

    .ae-page-header {{
        padding: 28px 18px 22px !important;
        margin-bottom: 26px !important;
    }}

    .ae-page-title {{
        font-size: clamp(30px, 8vw, 40px) !important;
    }}

    .ae-section-title {{
        font-size: clamp(28px, 7vw, 36px) !important;
    }}

    /* Catch common inline 40px page wrappers */
    div[style*="padding:0 40px"],
    div[style*="padding:0 40px 64px"],
    div[style*="padding:0 40px 32px"] {{
        padding-left: 18px !important;
        padding-right: 18px !important;
    }}

    div[style*="padding:40px 40px"] {{
        padding-left: 18px !important;
        padding-right: 18px !important;
    }}

    /* Search / finance / cards */
    .ae-search-panel {{
        margin: -18px 14px 0 !important;
        padding: 20px 16px !important;
    }}

    .ae-finance-panel {{
        padding: 22px 18px !important;
    }}

    .ae-card-body {{
        padding: 17px !important;
    }}

    .ae-card-name {{
        font-size: 16px !important;
    }}

    .ae-card-price {{
        font-size: 20px !important;
    }}

    .ae-kpi-card {{
        padding: 18px !important;
    }}

    .ae-kpi-val {{
        font-size: 28px !important;
    }}

    .ae-why-card,
    .ae-svc-card {{
        padding: 22px 18px !important;
    }}

    .ae-spec-card {{
        padding: 16px 12px !important;
    }}

    /* Details */
    .ae-detail-name {{
        font-size: clamp(30px, 8vw, 38px) !important;
    }}

    .ae-detail-variant {{
        font-size: 16px !important;
    }}

    .ae-detail-price {{
        font-size: 30px !important;
    }}

    .ae-detail-meta {{
        gap: 10px !important;
    }}

    /* Booking / compare / data tables */
    .ae-step {{
        padding: 17px 16px !important;
        gap: 12px !important;
    }}

    .ae-compare-table,
    .ae-admin-table {{
        min-width: 620px !important;
    }}

    /* Make HTML tables scroll instead of crushing columns */
    div[style*="overflow-x:auto"] {{
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }}

    /* Plotly charts should fit the viewport */
    [data-testid="stPlotlyChart"] {{
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }}

    /* Tabs scroll horizontally */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        overflow-x: auto !important;
        scrollbar-width: none !important;
        white-space: nowrap !important;
    }}

    [data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
    }}

    [data-testid="stTabs"] [data-baseweb="tab"] {{
        flex: 0 0 auto !important;
        padding: 9px 13px !important;
        font-size: 12px !important;
    }}

    /* Inputs and buttons */
    .stButton > button {{
        min-height: 44px !important;
        width: 100% !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] input {{
        font-size: 16px !important; /* prevents iOS zoom */
    }}

    /* CTA and footer */
    .ae-cta {{
        padding: 52px 18px !important;
    }}

    .ae-cta-title {{
        font-size: clamp(30px, 8vw, 42px) !important;
    }}

    .ae-cta-sub {{
        font-size: 14px !important;
    }}

    .ae-footer {{
        padding: 36px 18px 20px !important;
    }}

    .ae-footer-bottom {{
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 10px !important;
    }}

    .ae-empty {{
        padding: 55px 18px !important;
    }}
}}

@media (max-width: 480px) {{
    .ae-nav {{
        padding: 9px 12px !important;
    }}

    .ae-logo {{
        font-size: 18px !important;
    }}

    .ae-hero {{
        min-height: 470px !important;
        padding: 38px 18px 34px !important;
    }}

    .ae-hero-title {{
        font-size: 34px !important;
    }}

    .ae-hero svg[style*="width:560px"] {{
        width: 340px !important;
        right: -100px !important;
        bottom: 4px !important;
    }}

    .ae-hero svg[style*="width:520px"] {{
        width: 300px !important;
        right: -65px !important;
        bottom: -25px !important;
    }}

    .ae-section {{
        padding: 34px 14px !important;
    }}

    .ae-page-header {{
        padding-left: 14px !important;
        padding-right: 14px !important;
    }}

    div[style*="padding:0 40px"],
    div[style*="padding:0 40px 64px"],
    div[style*="padding:0 40px 32px"],
    div[style*="padding:40px 40px"] {{
        padding-left: 14px !important;
        padding-right: 14px !important;
    }}

    .ae-search-panel {{
        margin-left: 10px !important;
        margin-right: 10px !important;
        padding: 17px 14px !important;
    }}

    .ae-detail-name {{
        font-size: 29px !important;
    }}

    .ae-detail-price {{
        font-size: 27px !important;
    }}

    .ae-emi-amount {{
        font-size: 38px !important;
    }}

    .ae-badge {{
        font-size: 9px !important;
        padding: 4px 8px !important;
    }}

    /* Prevent long vehicle names/URLs from forcing horizontal overflow */
    .ae-card-name,
    .ae-card-brand,
    .ae-card-meta,
    .ae-page-title,
    .ae-section-title,
    .ae-detail-name,
    .ae-detail-variant {{
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }}

    img,
    video,
    iframe {{
        max-width: 100% !important;
    }}
}}

/* Utility classes */
.text-accent  {{ color: var(--accent) !important; }}
.text-gray    {{ color: var(--gray) !important; }}
.text-white   {{ color: var(--white) !important; }}
.text-danger  {{ color: var(--danger) !important; }}
.text-success {{ color: #4CAF50 !important; }}
.font-serif   {{ font-family: 'Playfair Display', serif !important; }}
.fw-600       {{ font-weight: 600 !important; }}
.fw-700       {{ font-weight: 700 !important; }}
.mt-0         {{ margin-top: 0 !important; }}
.mb-0         {{ margin-bottom: 0 !important; }}
</style>
"""
