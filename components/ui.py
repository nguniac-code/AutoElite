"""
AutoElite — Reusable UI Components
Each function renders one self-contained HTML block via st.markdown().
Pages import from here — no raw HTML strings scattered across page files.
"""

import streamlit as st
from utils.database import _fmt_price


# ── Utility ───────────────────────────────────────────────────────────────────
def _html(content: str, unsafe: bool = True) -> None:
    st.markdown(content, unsafe_allow_html=unsafe)


def calc_emi(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0 or principal <= 0:
        return principal / n if n else 0
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


# ── Navigation ────────────────────────────────────────────────────────────────
def render_navbar(active: str = "Home", fav_count: int = 0) -> None:
    pages = ["Home", "Cars", "Compare", "Financing", "Services", "About"]
    links_html = "".join(
        f'<a class="ae-nav-link {"active" if p == active else ""}" '
        f'href="?page={p.lower()}">{p}</a>'
        for p in pages
    )
    fav_badge = (
        f'<span style="position:absolute;top:4px;right:4px;background:var(--accent);'
        f'color:var(--black);font-size:9px;font-weight:700;width:14px;height:14px;'
        f'border-radius:50%;display:flex;align-items:center;justify-content:center">'
        f'{fav_count}</span>'
        if fav_count > 0 else ""
    )
    _html(f"""
    <nav class="ae-nav">
      <a class="ae-logo" href="?page=home">AUTO<span>ELITE</span></a>
      <div class="ae-nav-links">{links_html}</div>
      <div style="display:flex;align-items:center;gap:6px;margin-left:auto">
        <a href="?page=favorites" style="position:relative;display:inline-flex;
           align-items:center;justify-content:center;width:36px;height:36px;
           border-radius:8px;color:var(--gray);transition:.2s;text-decoration:none"
           title="Saved vehicles">
          <i class="ti ti-heart" style="font-size:20px"></i>{fav_badge}
        </a>
        <a href="?page=dashboard" style="display:inline-flex;align-items:center;
           justify-content:center;width:36px;height:36px;border-radius:8px;
           color:var(--gray);text-decoration:none" title="My account">
          <i class="ti ti-user" style="font-size:20px"></i>
        </a>
      </div>
    </nav>""")


# ── Page header ───────────────────────────────────────────────────────────────
def render_page_header(eyebrow: str, title: str, subtitle: str = "") -> None:
    sub_html = f'<p class="ae-page-sub">{subtitle}</p>' if subtitle else ""
    _html(f"""
    <div class="ae-page-header">
      <div class="ae-eyebrow">{eyebrow}</div>
      <h1 class="ae-page-title">{title}</h1>
      {sub_html}
    </div>""")


# ── Section header ────────────────────────────────────────────────────────────
def render_section_header(eyebrow: str, title: str, subtitle: str = "") -> None:
    sub_html = f'<p class="ae-section-sub">{subtitle}</p>' if subtitle else ""
    _html(f"""
    <div style="margin-bottom:36px">
      <div class="ae-eyebrow">{eyebrow}</div>
      <h2 class="ae-section-title">{title}</h2>
      {sub_html}
    </div>""")


# ── Status badge ──────────────────────────────────────────────────────────────
_STATUS_CLASS = {
    "Available":   "ae-badge-available",
    "Reserved":    "ae-badge-reserved",
    "Sold":        "ae-badge-sold",
    "Coming Soon": "ae-badge-coming",
}
_STATUS_DOT = {
    "Available":   "●",
    "Reserved":    "◆",
    "Sold":        "✕",
    "Coming Soon": "○",
}


def render_status_badge(status: str) -> str:
    cls  = _STATUS_CLASS.get(status, "ae-badge-coming")
    dot  = _STATUS_DOT.get(status, "○")
    return f'<span class="ae-badge {cls}">{dot} {status}</span>'


# ── Vehicle card ──────────────────────────────────────────────────────────────
def render_vehicle_card(v: dict, show_compare_btn: bool = True,
                        is_favourite: bool = False,
                        in_compare: bool = False) -> str:
    price     = _fmt_price(v["price"])
    emi       = int(calc_emi(v["price"] * 0.8, 8.5, 5))
    emi_fmt   = f"₹{emi:,}"
    badge_html = render_status_badge(v["status"])
    fav_icon  = "ti-heart-filled" if is_favourite else "ti-heart"
    fav_style = "color:var(--accent)" if is_favourite else ""
    img_html  = (
        f'<img class="ae-card-img" src="{v["image_url"]}" '
        f'alt="{v["brand"]} {v["model"]}" '
        f'onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'">'
        f'<div class="ae-card-img-placeholder" style="display:none">'
        f'<i class="ti ti-car"></i></div>'
        if v.get("image_url")
        else '<div class="ae-card-img-placeholder"><i class="ti ti-car"></i></div>'
    )
    featured_tag = (
        '<span class="ae-badge ae-badge-new" '
        'style="position:absolute;top:12px;left:12px">Featured</span>'
        if v.get("featured") else ""
    )
    compare_btn = (
        f'<a href="?page=cars&action=compare&vid={v["id"]}" '
        f'style="flex:1;display:inline-flex;align-items:center;justify-content:center;'
        f'gap:6px;padding:8px 12px;border-radius:8px;font-size:12px;font-weight:500;'
        f'text-decoration:none;border:1px solid {"rgba(200,168,75,.4)" if in_compare else "var(--card-border)"};'
        f'color:{"var(--accent)" if in_compare else "var(--gray)"};transition:.2s">'
        f'<i class="ti {"ti-check" if in_compare else "ti-scale"}"></i>'
        f'{"Added" if in_compare else "Compare"}</a>'
        if show_compare_btn else ""
    )
    return f"""
    <div class="ae-card">
      <div style="position:relative">
        {img_html}
        {featured_tag}
        <a href="?page=cars&action=fav&vid={v['id']}"
           style="position:absolute;top:12px;right:12px;background:rgba(10,10,11,.7);
                  border:1px solid rgba(255,255,255,.1);border-radius:50%;width:36px;
                  height:36px;display:flex;align-items:center;justify-content:center;
                  text-decoration:none;{fav_style}">
          <i class="ti {fav_icon}" style="font-size:16px"></i>
        </a>
      </div>
      <div class="ae-card-body">
        <div class="ae-card-brand">{v['brand']}</div>
        <div class="ae-card-name">{v['model']} {v['variant']}</div>
        <div class="ae-card-meta">
          <span class="ae-card-meta-item">
            <i class="ti ti-calendar" style="font-size:12px"></i>{v['year']}
          </span>
          <span class="ae-card-meta-item">
            <i class="ti ti-droplet" style="font-size:12px"></i>{v['fuel']}
          </span>
          <span class="ae-card-meta-item">
            <i class="ti ti-settings-2" style="font-size:12px"></i>{v['transmission']}
          </span>
        </div>
        <div style="margin-bottom:12px">{badge_html}</div>
        <div class="ae-card-price">{price}</div>
        <div class="ae-card-emi">EMI from {emi_fmt}/mo</div>
        <div style="display:flex;gap:8px;margin-top:14px">
          {compare_btn}
          <a href="?page=detail&vid={v['id']}"
             style="flex:1;display:inline-flex;align-items:center;justify-content:center;
                    gap:6px;padding:8px 12px;border-radius:8px;font-size:12px;font-weight:600;
                    background:var(--accent);color:var(--black);text-decoration:none;transition:.2s">
            View <i class="ti ti-arrow-right"></i>
          </a>
        </div>
      </div>
    </div>"""


def render_vehicle_grid(vehicles: list[dict],
                        favourites: set = None,
                        compare_ids: set = None,
                        cols: int = 3) -> None:
    favourites  = favourites  or set()
    compare_ids = compare_ids or set()
    if not vehicles:
        render_empty_state(
            icon="ti-car-off",
            title="No vehicles found",
            text="Try adjusting your filters to see more results.",
        )
        return
    col_size = 12 // cols
    cards_html = "".join(
        f'<div style="flex:0 0 calc({100/cols}% - 16px);min-width:260px">'
        f'{render_vehicle_card(v, is_favourite=v["id"] in favourites, in_compare=v["id"] in compare_ids)}'
        f'</div>'
        for v in vehicles
    )
    _html(f"""
    <div style="display:flex;flex-wrap:wrap;gap:20px">
      {cards_html}
    </div>""")


# ── Spec card ─────────────────────────────────────────────────────────────────
def render_specification(icon: str, label: str, value: str) -> str:
    return f"""
    <div class="ae-spec-card">
      <div class="ae-spec-icon"><i class="ti {icon}"></i></div>
      <div class="ae-spec-label">{label}</div>
      <div class="ae-spec-val">{value or '—'}</div>
    </div>"""


# ── Why card ──────────────────────────────────────────────────────────────────
def render_why_card(num: str, icon: str, title: str, text: str) -> str:
    return f"""
    <div class="ae-why-card">
      <div class="ae-why-num">{num}</div>
      <div class="ae-why-icon"><i class="ti {icon}"></i></div>
      <div class="ae-why-title">{title}</div>
      <p class="ae-why-text">{text}</p>
    </div>"""


# ── Service card ──────────────────────────────────────────────────────────────
def render_service_card(icon: str, title: str, text: str,
                        btn_label: str, btn_href: str) -> str:
    return f"""
    <div class="ae-svc-card">
      <div class="ae-svc-icon"><i class="ti {icon}"></i></div>
      <div class="ae-svc-title">{title}</div>
      <p class="ae-svc-text">{text}</p>
      <a href="{btn_href}"
         style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;
                border-radius:8px;font-size:12px;font-weight:500;text-decoration:none;
                border:1px solid var(--card-border);color:var(--gray);transition:.2s;
                margin-top:auto">
        {btn_label} <i class="ti ti-arrow-right"></i>
      </a>
    </div>"""


# ── Stat / KPI card ───────────────────────────────────────────────────────────
def render_stat_card(label: str, value: str, delta: str = "",
                     delta_positive: bool = True) -> None:
    delta_col = "text-success" if delta_positive else "text-danger"
    delta_icon = "ti-trending-up" if delta_positive else "ti-trending-down"
    delta_html = (
        f'<div class="ae-kpi-delta-{"pos" if delta_positive else "neg"}">'
        f'<i class="ti {delta_icon}" style="font-size:11px"></i> {delta}</div>'
        if delta else ""
    )
    _html(f"""
    <div class="ae-kpi-card">
      <div class="ae-kpi-label">{label}</div>
      <div class="ae-kpi-val">{value}</div>
      {delta_html}
    </div>""")


# ── Booking step ──────────────────────────────────────────────────────────────
def render_booking_step(num: str, title: str, text: str,
                        state: str = "pending") -> None:
    """state: 'pending' | 'active' | 'done'"""
    extra_cls = {"active": "ae-step-active", "done": "ae-step-done"}.get(state, "")
    num_content = '<i class="ti ti-check" style="font-size:13px"></i>' if state == "done" else num
    num_color = (
        "border-color:var(--success);color:var(--success);background:rgba(46,125,82,.1)"
        if state == "done"
        else "border-color:var(--accent);color:var(--accent);background:rgba(200,168,75,.1)"
        if state == "active"
        else ""
    )
    _html(f"""
    <div class="ae-step {extra_cls}">
      <div class="ae-step-num" style="{num_color}">{num_content}</div>
      <div>
        <div class="ae-step-title">{title}</div>
        <div class="ae-step-text">{text}</div>
      </div>
    </div>""")


# ── Empty state ───────────────────────────────────────────────────────────────
def render_empty_state(icon: str, title: str, text: str,
                       btn_label: str = "", btn_href: str = "") -> None:
    btn_html = (
        f'<a href="{btn_href}" style="display:inline-flex;align-items:center;gap:8px;'
        f'padding:12px 24px;background:var(--accent);color:var(--black);border-radius:8px;'
        f'text-decoration:none;font-weight:600;font-size:14px">{btn_label}</a>'
        if btn_label else ""
    )
    _html(f"""
    <div class="ae-empty">
      <div class="ae-empty-icon"><i class="ti {icon}"></i></div>
      <div class="ae-empty-title">{title}</div>
      <p class="ae-empty-text">{text}</p>
      {btn_html}
    </div>""")


# ── Info / alert boxes ────────────────────────────────────────────────────────
def render_info_box(text: str) -> None:
    _html(f'<div class="ae-info-box">{text}</div>')


def render_confirm_box(text: str) -> None:
    _html(f'<div class="ae-confirm-box">{text}</div>')


def render_success_toast(text: str) -> None:
    _html(f"""
    <div class="ae-toast ae-toast-success">
      <i class="ti ti-circle-check" style="color:#4CAF50;font-size:18px"></i>
      <span>{text}</span>
    </div>""")


def render_info_toast(text: str) -> None:
    _html(f"""
    <div class="ae-toast ae-toast-info">
      <i class="ti ti-info-circle" style="color:var(--accent);font-size:18px"></i>
      <span>{text}</span>
    </div>""")


# ── Form divider ──────────────────────────────────────────────────────────────
def render_form_divider(label: str) -> None:
    _html(f'<div class="ae-form-divider">{label}</div>')


# ── Footer ────────────────────────────────────────────────────────────────────
def render_footer() -> None:
    _html("""
    <div class="ae-footer">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;margin-bottom:40px;flex-wrap:wrap">
        <div>
          <div class="ae-footer-logo">AUTO<span>ELITE</span></div>
          <p style="font-size:13px;color:var(--gray);margin:6px 0 12px;font-style:italic">
            Drive Your Ambition.
          </p>
          <p style="font-size:12px;color:var(--mid);line-height:1.6;max-width:240px">
            India's premium automotive retail experience.
            Quality vehicles. Exceptional service.
          </p>
        </div>
        <div>
          <div class="ae-footer-col-title">Vehicles</div>
          <a class="ae-footer-link" href="?page=cars">Browse Cars</a>
          <a class="ae-footer-link" href="?page=cars">New Arrivals</a>
          <a class="ae-footer-link" href="?page=cars">Featured</a>
          <a class="ae-footer-link" href="?page=compare">Compare</a>
        </div>
        <div>
          <div class="ae-footer-col-title">Services</div>
          <a class="ae-footer-link" href="?page=financing">Financing</a>
          <a class="ae-footer-link" href="?page=services">Test Drive</a>
          <a class="ae-footer-link" href="?page=services">Trade-In</a>
          <a class="ae-footer-link" href="?page=services">Insurance</a>
        </div>
        <div>
          <div class="ae-footer-col-title">Company</div>
          <a class="ae-footer-link" href="?page=about">About Us</a>
          <a class="ae-footer-link" href="?page=about">Contact</a>
          <a class="ae-footer-link" href="#">Privacy Policy</a>
          <a class="ae-footer-link" href="#">Terms of Use</a>
        </div>
      </div>
      <div class="ae-footer-bottom">
        <span class="ae-footer-copy">
          © 2026 AutoElite. All rights reserved.
          Prices shown are indicative only.
        </span>
        <div style="display:flex;gap:10px">
          <a href="#" style="color:var(--gray);font-size:18px;text-decoration:none">
            <i class="ti ti-brand-instagram"></i></a>
          <a href="#" style="color:var(--gray);font-size:18px;text-decoration:none">
            <i class="ti ti-brand-twitter"></i></a>
          <a href="#" style="color:var(--gray);font-size:18px;text-decoration:none">
            <i class="ti ti-brand-linkedin"></i></a>
        </div>
      </div>
    </div>""")
