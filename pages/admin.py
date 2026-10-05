"""
AutoElite — Admin Dashboard
Full dealership CRM: KPIs, analytics charts, inventory CRUD,
test drive management, enquiry tracking, user overview.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from components.ui import (
    _html, render_page_header, render_status_badge,
    render_success_toast, render_info_toast, render_confirm_box,
    render_empty_state, render_footer,
)
from utils.database import (
    get_all_vehicles, get_vehicle, add_vehicle, update_vehicle, delete_vehicle,
    get_all_users, get_vehicle_count, get_user_count,
    get_test_drives, get_test_drive_count, update_test_drive_status,
    get_enquiries, get_enquiry_count, update_enquiry_status,
    get_status_distribution, get_revenue_estimate, get_brands,
    _fmt_price,
)

# ── Chart theme helpers ────────────────────────────────────────────────────────
_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8A8A95", size=12),
    margin=dict(l=0, r=0, t=8, b=0),
    showlegend=False,
    xaxis=dict(
        gridcolor="rgba(42,42,53,0.6)",
        linecolor="rgba(42,42,53,0.6)",
        tickfont=dict(size=11, color="#8A8A95"),
    ),
    yaxis=dict(
        gridcolor="rgba(42,42,53,0.6)",
        linecolor="rgba(42,42,53,0.6)",
        tickfont=dict(size=11, color="#8A8A95"),
    ),
)
ACCENT = "#C8A84B"
MID    = "#3A3A45"


def _chart_cfg() -> dict:
    return {"displayModeBar": False, "responsive": True}


# ── Access guard ───────────────────────────────────────────────────────────────
def _require_admin() -> bool:
    role = st.session_state.get("user_role", "")
    if role != "admin":
        _html("""
        <div style="min-height:60vh;display:flex;align-items:center;
                    justify-content:center;padding:40px;text-align:center">
          <div>
            <div style="font-size:48px;color:var(--mid);margin-bottom:20px">
              <i class="ti ti-lock"></i>
            </div>
            <h2 style="font-family:'Playfair Display',serif;font-size:28px;
                       color:var(--white);margin-bottom:8px">Admin Access Required</h2>
            <p style="font-size:14px;color:var(--gray);margin-bottom:24px">
              Sign in with an admin account to access the dealership dashboard.
            </p>
            <a href="?page=dashboard"
               style="display:inline-flex;align-items:center;gap:8px;padding:12px 24px;
                      background:var(--accent);color:var(--black);border-radius:8px;
                      font-weight:600;font-size:14px;text-decoration:none">
              Sign In
            </a>
          </div>
        </div>""")
        return False
    return True


# ── KPI row ────────────────────────────────────────────────────────────────────
def _render_kpis() -> None:
    revenue    = get_revenue_estimate()
    v_count    = get_vehicle_count()
    u_count    = get_user_count()
    td_count   = get_test_drive_count()
    enq_count  = get_enquiry_count()

    _html('<div style="padding:28px 40px 0">')
    c1, c2, c3, c4, c5 = st.columns(5, gap="medium")

    kpis = [
        (c1, "Revenue",        f"₹{revenue/1_000_000:.1f}M", "+12.4% this month", True),
        (c2, "Vehicles",       str(v_count),                  "+3 this week",       True),
        (c3, "Customers",      str(u_count),                  "+28 this month",     True),
        (c4, "Test Drives",    str(td_count),                 "This year",          True),
        (c5, "Enquiries",      str(enq_count),                "-5 from last week",  False),
    ]
    for col, label, val, delta, pos in kpis:
        with col:
            delta_color = "#4CAF50" if pos else "#EF5350"
            delta_icon  = "ti-trending-up" if pos else "ti-trending-down"
            _html(f"""
            <div class="ae-kpi-card">
              <div class="ae-kpi-label">{label}</div>
              <div class="ae-kpi-val">{val}</div>
              <div style="font-size:11px;color:{delta_color};margin-top:4px">
                <i class="ti {delta_icon}" style="font-size:10px"></i> {delta}
              </div>
            </div>""")
    _html("</div>")


# ── Analytics charts ───────────────────────────────────────────────────────────
def _render_analytics() -> None:
    _html('<div style="padding:28px 40px 0">')
    _html('<div class="ae-eyebrow" style="margin-bottom:20px">Analytics Overview</div>')

    col_bar, col_pie, col_line = st.columns([2, 1, 2], gap="medium")

    # Monthly sales bar
    with col_bar:
        months = ["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]
        values = [42, 38, 55, 48, 62, 70, 58, 65, 72, 68, 80, 55]
        colors = [ACCENT if m == "Sep" else MID for m in months]

        fig = go.Figure(go.Bar(
            x=months, y=values,
            marker_color=colors,
            marker_line_width=0,
        ))
        fig.update_layout(
            **_CHART_LAYOUT,
            height=220,
            title_text="Monthly Enquiries (2026)",
            title_font=dict(size=12, color="#8A8A95"),
            title_x=0,
        )
        st.plotly_chart(fig, use_container_width=True, config=_chart_cfg())

    # Status donut
    with col_pie:
        dist   = get_status_distribution()
        labels = list(dist.keys())
        vals   = list(dist.values())
        colors_pie = {
            "Available":   ACCENT,
            "Reserved":    "#A0843A",
            "Sold":        "#D94040",
            "Coming Soon": MID,
        }
        fig = go.Figure(go.Pie(
            labels=labels, values=vals,
            hole=0.6,
            marker_colors=[colors_pie.get(l, MID) for l in labels],
            textinfo="none",
            hoverinfo="label+value+percent",
        ))
        fig.update_layout(
            **_CHART_LAYOUT,
            height=220,
            title_text="Vehicle Status",
            title_font=dict(size=12, color="#8A8A95"),
            title_x=0,
            showlegend=True,
            legend=dict(
                font=dict(size=10, color="#8A8A95"),
                orientation="v",
                x=1, y=0.5,
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config=_chart_cfg())

    # Revenue trend line
    with col_line:
        rev_months = ["Apr","May","Jun","Jul","Aug","Sep"]
        rev_vals   = [18.2, 20.1, 22.4, 21.8, 23.6, 24.8]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rev_months, y=rev_vals,
            mode="lines+markers",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(color=ACCENT, size=6),
            fill="tozeroy",
            fillcolor="rgba(200,168,75,0.08)",
        ))
        fig.update_layout(
            **_CHART_LAYOUT,
            height=220,
            title_text="Revenue Trend — ₹M",
            title_font=dict(size=12, color="#8A8A95"),
            title_x=0,
            yaxis=dict(**_CHART_LAYOUT["yaxis"], tickprefix="₹", ticksuffix="M"),
        )
        st.plotly_chart(fig, use_container_width=True, config=_chart_cfg())

    _html("</div>")


# ── Inventory tab ──────────────────────────────────────────────────────────────
def _render_inventory_tab() -> None:
    # Filters
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2], gap="small")
    with c1:
        search = st.text_input("Search inventory", placeholder="Brand, model, variant…",
                               key="adm_search", label_visibility="collapsed")
    with c2:
        status_f = st.selectbox("Status", ["All","Available","Reserved","Sold","Coming Soon"],
                                key="adm_status", label_visibility="collapsed")
    with c3:
        brand_f  = st.selectbox("Brand", ["All"] + get_brands(),
                                key="adm_brand", label_visibility="collapsed")
    with c4:
        sort_f   = st.selectbox("Sort", ["Default","Price ↑","Price ↓","Newest"],
                                key="adm_sort", label_visibility="collapsed")

    sort_map = {"Default":"default","Price ↑":"price_asc","Price ↓":"price_desc","Newest":"year_desc"}
    vehicles = get_all_vehicles(
        status_filter = "" if status_f == "All" else status_f,
        brand_filter  = "" if brand_f  == "All" else brand_f,
        sort          = sort_map[sort_f],
        search_term   = search,
    )

    _html(f'<div style="font-size:12px;color:var(--gray);margin:12px 0 14px">'
          f'{len(vehicles)} vehicle{"s" if len(vehicles)!=1 else ""} in inventory</div>')

    if not vehicles:
        render_empty_state("ti-inbox", "No vehicles match your filters", "")
        return

    # Table header
    _html("""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                  border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
      <thead>
        <tr>""")
    for h in ["", "Vehicle", "Brand", "Year", "Price", "Status", "Stock", "Actions"]:
        _html(f"""
          <th style="padding:12px 16px;text-align:left;font-size:10px;font-weight:600;
                     color:var(--gray);text-transform:uppercase;letter-spacing:1px;
                     background:var(--dark);border-bottom:1px solid var(--card-border)">
            {h}</th>""")
    _html("</tr></thead><tbody>")

    for v in vehicles:
        thumb = (
            f'<img src="{v["image_url"]}" style="width:60px;height:40px;'
            f'object-fit:cover;border-radius:6px;display:block" '
            f'onerror="this.style.display=\'none\'">'
            if v.get("image_url") else
            '<div style="width:60px;height:40px;background:var(--dark);border-radius:6px;'
            'display:flex;align-items:center;justify-content:center">'
            '<i class="ti ti-car" style="color:var(--mid)"></i></div>'
        )
        badge = render_status_badge(v["status"])
        _html(f"""
        <tr>
          <td style="padding:10px 16px;border-bottom:1px solid rgba(42,42,53,.5)">{thumb}</td>
          <td style="padding:10px 16px;font-size:13px;font-weight:500;color:var(--white);
                     border-bottom:1px solid rgba(42,42,53,.5)">
            {v['model']} {v['variant']}</td>
          <td style="padding:10px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{v['brand']}</td>
          <td style="padding:10px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{v['year']}</td>
          <td style="padding:10px 16px;font-size:13px;font-weight:600;color:var(--accent);
                     border-bottom:1px solid rgba(42,42,53,.5)">{_fmt_price(v['price'])}</td>
          <td style="padding:10px 16px;border-bottom:1px solid rgba(42,42,53,.5)">{badge}</td>
          <td style="padding:10px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{v.get('stock',1)}</td>
          <td style="padding:10px 16px;border-bottom:1px solid rgba(42,42,53,.5)">
            <div style="display:flex;gap:6px">
              <a href="?page=detail&vid={v['id']}" title="View"
                 style="display:inline-flex;align-items:center;justify-content:center;
                        width:30px;height:30px;border-radius:6px;border:1px solid var(--card-border);
                        color:var(--gray);text-decoration:none;font-size:14px">
                <i class="ti ti-eye"></i></a>
            </div>
          </td>
        </tr>""")

    _html("</tbody></table></div>")

    # Edit / Delete expanders
    st.write("")
    st.caption("Manage a specific vehicle:")
    sel_id = st.number_input("Vehicle ID to edit/delete", min_value=1, step=1,
                             key="adm_sel_id", label_visibility="collapsed",
                             placeholder="Enter vehicle ID")

    if sel_id:
        sv = get_vehicle(int(sel_id))
        if sv:
            with st.expander(f"Edit — {sv['brand']} {sv['model']} {sv['variant']}", expanded=False):
                with st.form(f"edit_form_{sel_id}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        new_price  = st.number_input("Price (₹)", value=sv["price"], step=10000)
                        new_km     = st.number_input("Km Driven", value=sv.get("km_driven",0), step=100)
                        new_stock  = st.number_input("Stock", value=sv.get("stock",1), min_value=0)
                    with ec2:
                        new_status = st.selectbox("Status",
                            ["Available","Reserved","Sold","Coming Soon"],
                            index=["Available","Reserved","Sold","Coming Soon"].index(sv["status"])
                                   if sv["status"] in ["Available","Reserved","Sold","Coming Soon"] else 0)
                        new_feat   = st.checkbox("Featured", value=bool(sv.get("featured")))
                        new_color  = st.text_input("Colour", value=sv.get("color",""))
                    new_desc = st.text_area("Description", value=sv.get("description",""), height=80)
                    new_img  = st.text_input("Image URL", value=sv.get("image_url",""))
                    saved = st.form_submit_button("Save Changes", use_container_width=True)
                    if saved:
                        update_vehicle(int(sel_id), {
                            "price":       new_price,
                            "km_driven":   new_km,
                            "stock":       new_stock,
                            "status":      new_status,
                            "featured":    int(new_feat),
                            "color":       new_color,
                            "description": new_desc,
                            "image_url":   new_img,
                        })
                        render_success_toast(
                            f"{sv['brand']} {sv['model']} updated successfully."
                        )
                        st.rerun()

            with st.expander(f"⚠ Delete — {sv['brand']} {sv['model']} {sv['variant']}", expanded=False):
                render_confirm_box(
                    f"Permanently remove <strong>{sv['brand']} {sv['model']} {sv['variant']} "
                    f"({sv['year']})</strong> from inventory? This cannot be undone."
                )
                col_cancel, col_delete = st.columns(2)
                with col_cancel:
                    if st.button("Cancel", key=f"cancel_del_{sel_id}", use_container_width=True):
                        st.rerun()
                with col_delete:
                    _html('<div class="btn-danger-wrap">')
                    if st.button("Yes, Delete Vehicle", key=f"confirm_del_{sel_id}",
                                 use_container_width=True):
                        delete_vehicle(int(sel_id))
                        render_success_toast("Vehicle removed from inventory.")
                        st.rerun()
                    _html("</div>")
        else:
            render_info_toast(f"No vehicle found with ID {int(sel_id)}.")


# ── Add vehicle tab ────────────────────────────────────────────────────────────
def _render_add_vehicle_tab() -> None:
    _html("""
    <div style="max-width:700px">
      <h3 style="font-size:20px;font-weight:600;color:var(--white);margin-bottom:24px">
        Add New Vehicle
      </h3>""")

    with st.form("add_vehicle_form"):
        _html('<div class="ae-form-divider">Vehicle Identity</div>')
        r1c1, r1c2, r1c3 = st.columns(3, gap="medium")
        with r1c1:
            av_brand   = st.text_input("Brand *", placeholder="BMW")
        with r1c2:
            av_model   = st.text_input("Model *", placeholder="3 Series")
        with r1c3:
            av_variant = st.text_input("Variant *", placeholder="330i M Sport")

        _html('<div class="ae-form-divider">Details</div>')
        r2c1, r2c2, r2c3, r2c4 = st.columns(4, gap="medium")
        with r2c1:
            av_year  = st.number_input("Year *", min_value=2010, max_value=2027,
                                       value=2025, step=1)
        with r2c2:
            av_price = st.number_input("Price (₹) *", min_value=100000,
                                       max_value=100000000, value=5000000, step=50000)
        with r2c3:
            av_fuel  = st.selectbox("Fuel *",
                ["Petrol","Diesel","Electric","Hybrid","CNG"])
        with r2c4:
            av_trans = st.selectbox("Transmission *",
                ["Automatic","Manual","CVT","DCT"])

        r3c1, r3c2, r3c3, r3c4 = st.columns(4, gap="medium")
        with r3c1:
            av_body    = st.selectbox("Body Type *",
                ["Sedan","SUV","Coupe","Convertible","Hatchback","Pickup","MPV"])
        with r3c2:
            av_mileage = st.number_input("Mileage (km/l)", min_value=0.0,
                                         max_value=50.0, value=14.0, step=0.1)
        with r3c3:
            av_km      = st.number_input("Km Driven", min_value=0,
                                         max_value=500000, value=0, step=500)
        with r3c4:
            av_stock   = st.number_input("Stock Units", min_value=0,
                                         max_value=50, value=1, step=1)

        _html('<div class="ae-form-divider">Specifications</div>')
        s1, s2, s3, s4 = st.columns(4, gap="medium")
        with s1:
            av_engine = st.text_input("Engine", placeholder="2.0L Turbo")
        with s2:
            av_power  = st.text_input("Power",  placeholder="258 HP")
        with s3:
            av_torque = st.text_input("Torque", placeholder="400 Nm")
        with s4:
            av_color  = st.text_input("Colour", placeholder="Alpine White")

        _html('<div class="ae-form-divider">Listing</div>')
        l1, l2, l3 = st.columns([2, 1, 1], gap="medium")
        with l1:
            av_image = st.text_input("Image URL", placeholder="https://…")
        with l2:
            av_status  = st.selectbox("Status", ["Available","Coming Soon","Reserved"])
        with l3:
            av_featured = st.checkbox("Mark as Featured")
        av_desc = st.text_area("Description", height=80,
                               placeholder="A brief description of the vehicle…")

        submitted = st.form_submit_button("Add to Inventory", use_container_width=True)

        if submitted:
            if not all([av_brand, av_model, av_variant, av_year, av_price]):
                st.error("Please fill in all required fields (marked with *).")
            else:
                new_id = add_vehicle({
                    "brand":        av_brand.strip(),
                    "model":        av_model.strip(),
                    "variant":      av_variant.strip(),
                    "year":         int(av_year),
                    "price":        int(av_price),
                    "fuel":         av_fuel,
                    "transmission": av_trans,
                    "body_type":    av_body,
                    "engine":       av_engine or "—",
                    "power":        av_power  or "—",
                    "torque":       av_torque or "—",
                    "mileage":      float(av_mileage) if av_mileage else None,
                    "km_driven":    int(av_km),
                    "color":        av_color  or "—",
                    "status":       av_status,
                    "featured":     av_featured,
                    "description":  av_desc,
                    "image_url":    av_image,
                    "stock":        int(av_stock),
                })
                render_success_toast(
                    f"{av_brand} {av_model} {av_variant} added to inventory (ID: {new_id})."
                )
                st.rerun()

    _html("</div>")


# ── Test drives tab ────────────────────────────────────────────────────────────
def _render_test_drives_tab() -> None:
    drives = get_test_drives()

    if not drives:
        render_empty_state("ti-calendar-off","No test drive bookings yet",
                           "Bookings will appear here once customers submit requests.")
        return

    _html(f'<div style="font-size:12px;color:var(--gray);margin-bottom:14px">'
          f'{len(drives)} booking{"s" if len(drives)!=1 else ""}</div>')

    _html("""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                  border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
      <thead><tr>""")
    for h in ["Vehicle","Customer","Phone","Date","Time","Status","Action"]:
        _html(f"""
        <th style="padding:12px 16px;text-align:left;font-size:10px;font-weight:600;
                   color:var(--gray);text-transform:uppercase;letter-spacing:1px;
                   background:var(--dark);border-bottom:1px solid var(--card-border)">{h}</th>""")
    _html("</tr></thead><tbody>")

    for d in drives:
        status_map = {
            "Pending":   "Reserved",
            "Confirmed": "Available",
            "Cancelled": "Sold",
            "Completed": "Coming Soon",
        }
        badge = render_status_badge(status_map.get(d["status"], "Reserved"))
        vehicle_str = f"{d.get('brand','')} {d.get('model','')}".strip()
        _html(f"""
        <tr>
          <td style="padding:12px 16px;font-size:13px;color:var(--white);font-weight:500;
                     border-bottom:1px solid rgba(42,42,53,.5)">{vehicle_str}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{d['name']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{d['phone']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{d['drive_date']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{d['time_slot']}</td>
          <td style="padding:12px 16px;border-bottom:1px solid rgba(42,42,53,.5)">{badge}</td>
          <td style="padding:12px 16px;border-bottom:1px solid rgba(42,42,53,.5)">
            <div style="display:flex;gap:6px">""")

        col_confirm, col_cancel = st.columns([1, 1])
        with col_confirm:
            if st.button("✓", key=f"td_confirm_{d['id']}", help="Mark Confirmed"):
                update_test_drive_status(d["id"], "Confirmed")
                st.rerun()
        with col_cancel:
            if st.button("✕", key=f"td_cancel_{d['id']}", help="Cancel"):
                update_test_drive_status(d["id"], "Cancelled")
                st.rerun()
        _html("</div></td></tr>")
    _html("</tbody></table></div>")


# ── Enquiries tab ──────────────────────────────────────────────────────────────
def _render_enquiries_tab() -> None:
    enqs = get_enquiries()

    if not enqs:
        render_empty_state("ti-inbox","No enquiries yet",
                           "Customer enquiries and quote requests will appear here.")
        return

    status_filter = st.selectbox("Filter by status",
                                 ["All","New","InProgress","Resolved","Closed"],
                                 key="enq_status_filter", label_visibility="collapsed")
    if status_filter != "All":
        enqs = [e for e in enqs if e["status"] == status_filter]

    _html(f'<div style="font-size:12px;color:var(--gray);margin-bottom:14px">'
          f'{len(enqs)} enquir{"ies" if len(enqs)!=1 else "y"}</div>')

    _html("""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                  border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
      <thead><tr>""")
    for h in ["Type","Name","Phone","Vehicle","Date","Status","Action"]:
        _html(f"""
        <th style="padding:12px 16px;text-align:left;font-size:10px;font-weight:600;
                   color:var(--gray);text-transform:uppercase;letter-spacing:1px;
                   background:var(--dark);border-bottom:1px solid var(--card-border)">{h}</th>""")
    _html("</tr></thead><tbody>")

    for e in enqs:
        status_display = {
            "New":        "Available",
            "InProgress": "Reserved",
            "Resolved":   "Coming Soon",
            "Closed":     "Sold",
        }
        badge = render_status_badge(status_display.get(e["status"], "Available"))
        vehicle_str = f"{e.get('brand','')} {e.get('model','')}".strip() or "General"
        _html(f"""
        <tr>
          <td style="padding:12px 16px;font-size:13px;color:var(--white);font-weight:500;
                     border-bottom:1px solid rgba(42,42,53,.5)">{e['type']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{e['name']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{e['phone']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{vehicle_str}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{e['created_at'][:10]}</td>
          <td style="padding:12px 16px;border-bottom:1px solid rgba(42,42,53,.5)">{badge}</td>
          <td style="padding:12px 16px;border-bottom:1px solid rgba(42,42,53,.5)">""")
        new_status = st.selectbox(
            f"status_{e['id']}",
            ["New","InProgress","Resolved","Closed"],
            index=["New","InProgress","Resolved","Closed"].index(
                e["status"] if e["status"] in ["New","InProgress","Resolved","Closed"] else "New"
            ),
            key=f"enq_sel_{e['id']}",
            label_visibility="collapsed",
        )
        if new_status != e["status"]:
            update_enquiry_status(e["id"], new_status)
            st.rerun()
        _html("</td></tr>")
    _html("</tbody></table></div>")


# ── Users tab ──────────────────────────────────────────────────────────────────
def _render_users_tab() -> None:
    users = get_all_users()

    _html(f'<div style="font-size:12px;color:var(--gray);margin-bottom:14px">'
          f'{len(users)} registered user{"s" if len(users)!=1 else ""}</div>')

    _html("""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                  border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
      <thead><tr>""")
    for h in ["ID","Name","Email","Phone","Role","Joined"]:
        _html(f"""
        <th style="padding:12px 16px;text-align:left;font-size:10px;font-weight:600;
                   color:var(--gray);text-transform:uppercase;letter-spacing:1px;
                   background:var(--dark);border-bottom:1px solid var(--card-border)">{h}</th>""")
    _html("</tr></thead><tbody>")

    for u in users:
        role_color = "var(--accent)" if u["role"] == "admin" else "var(--gray)"
        _html(f"""
        <tr>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{u['id']}</td>
          <td style="padding:12px 16px;font-size:13px;font-weight:500;color:var(--white);
                     border-bottom:1px solid rgba(42,42,53,.5)">{u['name']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--light);
                     border-bottom:1px solid rgba(42,42,53,.5)">{u['email']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{u.get('phone','—')}</td>
          <td style="padding:12px 16px;font-size:12px;font-weight:600;
                     color:{role_color};text-transform:uppercase;letter-spacing:.5px;
                     border-bottom:1px solid rgba(42,42,53,.5)">{u['role']}</td>
          <td style="padding:12px 16px;font-size:13px;color:var(--gray);
                     border-bottom:1px solid rgba(42,42,53,.5)">{u['created_at'][:10]}</td>
        </tr>""")
    _html("</tbody></table></div>")


# ── Main admin page ────────────────────────────────────────────────────────────
def render_admin_page() -> None:
    if not _require_admin():
        return

    today = datetime.now().strftime("%A, %d %B %Y")

    # Admin top bar
    _html(f"""
    <div class="ae-admin-bar">
      <span class="ae-admin-tag">Admin</span>
      <span style="font-size:15px;font-weight:600;color:var(--white)">
        Dealership Overview
      </span>
      <span style="font-size:12px;color:var(--gray);margin-left:auto">{today}</span>
      <a href="?page=dashboard"
         style="display:inline-flex;align-items:center;gap:6px;padding:7px 14px;
                border-radius:6px;border:1px solid var(--card-border);color:var(--gray);
                font-size:12px;text-decoration:none;margin-left:12px">
        <i class="ti ti-user"></i> My Account
      </a>
    </div>""")

    _render_kpis()
    _render_analytics()

    # Main tabs
    _html('<div style="padding:28px 40px 64px">')
    tab_inv, tab_add, tab_td, tab_enq, tab_users = st.tabs([
        "Inventory", "Add Vehicle", "Test Drives", "Enquiries", "Users"
    ])

    with tab_inv:
        _render_inventory_tab()

    with tab_add:
        _render_add_vehicle_tab()

    with tab_td:
        _render_test_drives_tab()

    with tab_enq:
        _render_enquiries_tab()

    with tab_users:
        _render_users_tab()

    _html("</div>")
    render_footer()
