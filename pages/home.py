"""
AutoElite — Home Page
Hero → Search → Featured → Why AutoElite → Popular → Services → CTA → Footer
"""

import streamlit as st
from components.ui import (
    _html, render_section_header, render_vehicle_grid,
    render_why_card, render_service_card, render_footer,
)
from utils.database import (
    get_featured_vehicles, get_popular_vehicles, get_brands, get_body_types,
)


def render_hero() -> None:
    _html("""
    <div class="ae-hero">
      <div class="ae-hero-bg"></div>
      <!-- decorative rings -->
      <svg style="position:absolute;right:0;top:50%;transform:translateY(-50%);
                  width:520px;height:520px;opacity:.12;pointer-events:none"
           viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg">
        <circle cx="260" cy="260" r="240" fill="none" stroke="#C8A84B" stroke-width="1"/>
        <circle cx="260" cy="260" r="180" fill="none" stroke="#C8A84B" stroke-width="1"/>
        <circle cx="260" cy="260" r="120" fill="none" stroke="#C8A84B" stroke-width="1"/>
        <circle cx="260" cy="260" r="60"  fill="none" stroke="#C8A84B" stroke-width="1"/>
      </svg>
      <!-- Car SVG illustration -->
      <svg style="position:absolute;right:40px;top:50%;transform:translateY(-50%);
                  width:560px;height:320px;opacity:.82;pointer-events:none;
                  filter:drop-shadow(0 20px 60px rgba(200,168,75,.18))"
           viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="hbg" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#2A2A35"/><stop offset="100%" stop-color="#1A1A1F"/>
          </linearGradient>
          <radialGradient id="hwg">
            <stop offset="30%" stop-color="#3A3A45"/><stop offset="100%" stop-color="#1A1A1F"/>
          </radialGradient>
        </defs>
        <ellipse cx="300" cy="285" rx="280" ry="8" fill="#0A0A0B" opacity=".8"/>
        <path d="M60,190 L80,155 L120,130 L200,115 L280,110 L370,115 L430,130 L460,155 L520,175 L530,190 L530,220 L60,220 Z"
              fill="url(#hbg)" stroke="#C8A84B" stroke-width="1.5" stroke-opacity=".6"/>
        <path d="M140,155 L165,125 L220,112 L310,108 L380,112 L420,130 L430,155 Z"
              fill="#22222A" stroke="#C8A84B" stroke-width="1" stroke-opacity=".4"/>
        <path d="M160,150 L178,128 L225,116 L225,150 Z" fill="#0D1A2E" opacity=".9"/>
        <path d="M232,116 L310,113 L310,150 L232,150 Z" fill="#0D1A2E" opacity=".9"/>
        <path d="M317,114 L375,117 L415,135 L415,150 L317,150 Z" fill="#0D1A2E" opacity=".9"/>
        <path d="M80,178 L510,178" stroke="#C8A84B" stroke-width="1.5" opacity=".5"/>
        <ellipse cx="510" cy="170" rx="16" ry="8" fill="#F5E6B8" opacity=".9"/>
        <ellipse cx="510" cy="170" rx="10" ry="5" fill="#fff" opacity=".6"/>
        <rect x="68" y="162" width="20" height="10" rx="3" fill="#D94040" opacity=".8"/>
        <circle cx="155" cy="220" r="38" fill="url(#hwg)" stroke="#C8A84B" stroke-width="1.5" stroke-opacity=".5"/>
        <circle cx="155" cy="220" r="22" fill="none" stroke="#C8A84B" stroke-width="1" stroke-opacity=".6"/>
        <circle cx="155" cy="220" r="8"  fill="#C8A84B" opacity=".7"/>
        <circle cx="415" cy="220" r="38" fill="url(#hwg)" stroke="#C8A84B" stroke-width="1.5" stroke-opacity=".5"/>
        <circle cx="415" cy="220" r="22" fill="none" stroke="#C8A84B" stroke-width="1" stroke-opacity=".6"/>
        <circle cx="415" cy="220" r="8"  fill="#C8A84B" opacity=".7"/>
        <g stroke="#C8A84B" stroke-width="1" opacity=".5">
          <line x1="155" y1="198" x2="155" y2="242"/>
          <line x1="133" y1="220" x2="177" y2="220"/>
          <line x1="140" y1="205" x2="170" y2="235"/>
          <line x1="170" y1="205" x2="140" y2="235"/>
          <line x1="415" y1="198" x2="415" y2="242"/>
          <line x1="393" y1="220" x2="437" y2="220"/>
          <line x1="400" y1="205" x2="430" y2="235"/>
          <line x1="430" y1="205" x2="400" y2="235"/>
        </g>
        <rect x="60" y="218" width="470" height="8" rx="3" fill="#1A1A1F"/>
        <path d="M505,155 L530,150 L535,165 L505,165 Z"
              fill="#22222A" stroke="#C8A84B" stroke-width=".8" stroke-opacity=".4"/>
      </svg>
      <!-- Text content -->
      <div style="position:relative;z-index:2;max-width:580px">
        <div class="ae-hero-eyebrow">Premium Automotive Collection</div>
        <h1 class="ae-hero-title">
          Find Your<br>Next <em>Signature</em><br>Drive
        </h1>
        <p class="ae-hero-sub">
          Exceptional vehicles meticulously selected for those who refuse to compromise.
        </p>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a href="?page=cars"
             style="display:inline-flex;align-items:center;gap:8px;padding:14px 30px;
                    background:var(--accent);color:var(--black);border-radius:8px;
                    font-weight:600;font-size:14px;text-decoration:none;transition:.2s">
            <i class="ti ti-car"></i> Explore Vehicles
          </a>
          <a href="?page=services"
             style="display:inline-flex;align-items:center;gap:8px;padding:13px 28px;
                    background:transparent;color:var(--white);border-radius:8px;
                    border:1px solid rgba(255,255,255,.2);font-weight:500;font-size:14px;
                    text-decoration:none;transition:.2s">
            <i class="ti ti-key"></i> Book Test Drive
          </a>
        </div>
      </div>
    </div>""")


def render_search_panel() -> None:
    brands     = ["All Brands"] + get_brands()
    body_types = ["All Types", "Sedan", "SUV", "Coupe", "Convertible", "Hatchback", "Pickup"]
    budgets    = {
        "Any Budget": 0,
        "Under ₹20L": 2_000_000,
        "Under ₹50L": 5_000_000,
        "Under ₹1 Cr": 10_000_000,
        "₹1 Cr+":     999_999_999,
    }
    fuels = ["All Fuels", "Petrol", "Diesel", "Electric", "Hybrid"]

    _html('<div class="ae-search-panel">')
    _html('<div class="ae-eyebrow" style="margin-bottom:18px">Find your perfect vehicle</div>')

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
    with c1:
        brand = st.selectbox("Brand", brands, label_visibility="collapsed",
                             key="hs_brand", placeholder="Brand")
        st.caption("Brand")
    with c2:
        body = st.selectbox("Body Type", body_types, label_visibility="collapsed",
                            key="hs_body", placeholder="Body Type")
        st.caption("Body Type")
    with c3:
        budget_label = st.selectbox("Budget", list(budgets.keys()),
                                    label_visibility="collapsed",
                                    key="hs_budget", placeholder="Budget")
        st.caption("Budget")
    with c4:
        fuel = st.selectbox("Fuel", fuels, label_visibility="collapsed",
                            key="hs_fuel", placeholder="Fuel")
        st.caption("Fuel")
    with c5:
        st.write("")
        search = st.button("Search", key="hs_search", use_container_width=True)

    _html("</div>")

    if search:
        params = {}
        if brand != "All Brands":
            params["brand"] = brand
        if body != "All Types":
            params["body"] = body
        if budget_label != "Any Budget":
            params["budget"] = budgets[budget_label]
        if fuel != "All Fuels":
            params["fuel"] = fuel
        # Store in session and redirect to cars page
        st.session_state["search_filters"] = params
        st.query_params["page"] = "cars"
        st.rerun()


def render_why_section() -> None:
    _html('<div class="ae-section ae-section-dark">')
    render_section_header(
        "Our Promise", "Why AutoElite?",
        "Every vehicle, every price, every process — held to a higher standard."
    )
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("01", "ti-shield-check", "Verified Vehicles",
         "Every vehicle undergoes a comprehensive 120-point quality inspection before listing."),
        ("02", "ti-tag", "Transparent Pricing",
         "No hidden charges, no confusing add-ons. What you see is exactly what you pay."),
        ("03", "ti-headset", "Personalized Assistance",
         "Our automotive specialists help you find the vehicle that fits your life perfectly."),
        ("04", "ti-rocket", "Seamless Experience",
         "From discovery to delivery — a streamlined journey designed around your convenience."),
    ]
    for col, (num, icon, title, text) in zip([c1, c2, c3, c4], cards):
        with col:
            _html(render_why_card(num, icon, title, text))
    _html("</div>")


def render_services_strip() -> None:
    _html('<div class="ae-section ae-section-dark">')
    render_section_header("What We Offer", "Our Services")
    c1, c2, c3, c4 = st.columns(4)
    svcs = [
        ("ti-credit-card", "Financing",
         "Flexible EMI plans from 7.9% p.a. Quick approvals, minimal paperwork.",
         "Calculate EMI", "?page=financing"),
        ("ti-key", "Test Drive",
         "Experience the car before you decide. Book at your nearest showroom.",
         "Book a Slot", "?page=services"),
        ("ti-refresh", "Trade-In",
         "Turn your current vehicle into value toward your next AutoElite purchase.",
         "Get Valuation", "?page=services"),
        ("ti-shield", "Insurance",
         "Comprehensive coverage from trusted partners. Protection that travels with you.",
         "Learn More", "?page=services"),
    ]
    for col, (icon, title, text, btn, href) in zip([c1, c2, c3, c4], svcs):
        with col:
            _html(render_service_card(icon, title, text, btn, href))
    _html("</div>")


def render_cta() -> None:
    _html("""
    <div class="ae-cta">
      <div class="ae-eyebrow" style="text-align:center;margin-bottom:12px">Start Your Journey</div>
      <h2 class="ae-cta-title">Ready to Find Your Next Car?</h2>
      <p class="ae-cta-sub">Your next journey starts here. Browse our curated collection today.</p>
      <a href="?page=cars"
         style="display:inline-flex;align-items:center;gap:8px;padding:15px 36px;
                background:var(--accent);color:var(--black);border-radius:8px;
                font-weight:700;font-size:15px;text-decoration:none;transition:.2s">
        <i class="ti ti-car"></i> Explore Vehicles
      </a>
    </div>""")


def render_home() -> None:
    render_hero()
    render_search_panel()

    # Featured
    _html('<div class="ae-section">')
    _html("""
    <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:36px">
      <div>
        <div class="ae-eyebrow">Curated Selection</div>
        <h2 class="ae-section-title">Featured Collection</h2>
        <p class="ae-section-sub">Vehicles selected for those who expect something extraordinary.</p>
      </div>
      <a href="?page=cars"
         style="display:inline-flex;align-items:center;gap:6px;padding:9px 18px;
                border-radius:8px;border:1px solid var(--card-border);color:var(--gray);
                font-size:13px;text-decoration:none;flex-shrink:0;align-self:flex-end">
        View all <i class="ti ti-arrow-right"></i>
      </a>
    </div>""")

    favs = set(st.session_state.get("favourites", []))
    compare = set(st.session_state.get("compare_ids", []))

    featured = get_featured_vehicles(4)
    render_vehicle_grid(featured, favourites=favs, compare_ids=compare, cols=4)
    _html("</div>")

    render_why_section()

    # Popular
    _html('<div class="ae-section">')
    _html("""
    <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:36px">
      <div>
        <div class="ae-eyebrow">Most Viewed</div>
        <h2 class="ae-section-title">Popular Right Now</h2>
      </div>
      <a href="?page=cars"
         style="display:inline-flex;align-items:center;gap:6px;padding:9px 18px;
                border-radius:8px;border:1px solid var(--card-border);color:var(--gray);
                font-size:13px;text-decoration:none;flex-shrink:0;align-self:flex-end">
        View all <i class="ti ti-arrow-right"></i>
      </a>
    </div>""")
    popular = get_popular_vehicles(4)
    render_vehicle_grid(popular, favourites=favs, compare_ids=compare, cols=4)
    _html("</div>")

    render_services_strip()
    render_cta()
    render_footer()
