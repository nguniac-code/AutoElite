"""
AutoElite — Cars Listing & Vehicle Detail Pages
"""

import streamlit as st
from components.ui import (
    _html, render_page_header, render_vehicle_grid, render_empty_state,
    render_status_badge, render_specification, render_success_toast,
    render_info_toast, render_footer, calc_emi,
)
from utils.database import (
    get_all_vehicles, get_vehicle, get_brands, get_body_types,
    toggle_favourite, is_favourite, create_enquiry, book_test_drive,
    _fmt_price,
)


# ── Cars listing ──────────────────────────────────────────────────────────────
def render_cars_page() -> None:
    render_page_header(
        "Our Inventory", "Vehicle Collection",
        "Browse our complete selection of premium, verified vehicles.",
    )

    # Sidebar filters
    with st.sidebar:
        _html("""
        <div style="padding:16px 0 8px">
          <div class="ae-eyebrow" style="margin-bottom:12px">Filter Vehicles</div>
        </div>""")

        # Pre-fill from search panel
        sf = st.session_state.pop("search_filters", {})

        brands = ["All Brands"] + get_brands()
        default_brand = brands.index(sf["brand"]) if sf.get("brand") in brands else 0
        brand = st.selectbox("Brand", brands, index=default_brand, key="cf_brand")

        fuels = ["All Fuels", "Petrol", "Diesel", "Electric", "Hybrid"]
        fuel = st.selectbox("Fuel Type", fuels, key="cf_fuel")

        bodies = ["All Types"] + get_body_types()
        default_body = bodies.index(sf["body"]) if sf.get("body") in bodies else 0
        body = st.selectbox("Body Type", bodies, index=default_body, key="cf_body")

        statuses = ["All Status", "Available", "Reserved", "Coming Soon", "Sold"]
        status = st.selectbox("Status", statuses, key="cf_status")

        sort_opts = {
            "Default":            "default",
            "Price: Low → High":  "price_asc",
            "Price: High → Low":  "price_desc",
            "Newest First":       "year_desc",
        }
        sort_label = st.selectbox("Sort By", list(sort_opts.keys()), key="cf_sort")

        search_term = st.text_input("Search", placeholder="Brand, model, keyword…",
                                    key="cf_search")

        budget_max = sf.get("budget", 0)
        if budget_max:
            _html(f'<div class="ae-info-box" style="margin-top:8px">'
                  f'Budget filter active: up to {_fmt_price(budget_max)}</div>')

        st.divider()
        if st.button("Clear Filters", use_container_width=True, key="cf_clear"):
            for k in ["cf_brand","cf_fuel","cf_body","cf_status","cf_sort","cf_search"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # Apply filters
    vehicles = get_all_vehicles(
        status_filter  = "" if status  == "All Status"  else status,
        brand_filter   = "" if brand   == "All Brands"  else brand,
        fuel_filter    = "" if fuel    == "All Fuels"   else fuel,
        body_filter    = "" if body    == "All Types"   else body,
        sort           = sort_opts[sort_label],
        budget_max     = budget_max,
        search_term    = search_term,
    )

    # Top bar
    favs    = set(st.session_state.get("favourites", []))
    compare = set(st.session_state.get("compare_ids", []))

    _html(f"""
    <div style="padding:0 40px 20px;display:flex;align-items:center;
                justify-content:space-between">
      <span style="font-size:13px;color:var(--gray)">
        {len(vehicles)} vehicle{'s' if len(vehicles)!=1 else ''} found
      </span>
    </div>""")

    _html('<div style="padding:0 40px 64px">')
    render_vehicle_grid(vehicles, favourites=favs, compare_ids=compare, cols=3)
    _html("</div>")

    render_footer()


# ── Vehicle detail ────────────────────────────────────────────────────────────
def render_detail_page(vehicle_id: int) -> None:
    v = get_vehicle(vehicle_id)
    if not v:
        render_empty_state(
            "ti-alert-circle",
            "Vehicle not found",
            "This vehicle may no longer be available. Browse our full collection.",
            "Browse Vehicles", "?page=cars",
        )
        return

    user_id = st.session_state.get("user_id", 0)
    favs    = set(st.session_state.get("favourites", []))
    compare = set(st.session_state.get("compare_ids", []))
    fav     = vehicle_id in favs

    # ── Action buttons ──
    _html(f'<div style="padding:20px 40px 0">')
    _html('<a href="?page=cars" style="display:inline-flex;align-items:center;gap:6px;'
          'color:var(--gray);text-decoration:none;font-size:13px;margin-bottom:16px">'
          '<i class="ti ti-arrow-left"></i> Back to results</a>')
    _html("</div>")

    # ── Hero section ──
    img_html = (
        f'<img src="{v["image_url"]}" alt="{v["brand"]} {v["model"]}"'
        f' style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:16px;display:block"'
        f' onerror="this.style.display=\'none\'">'
        if v.get("image_url") else
        '<div style="width:100%;aspect-ratio:16/9;background:var(--dark);'
        'border-radius:16px;display:flex;align-items:center;justify-content:center">'
        '<i class="ti ti-car" style="font-size:64px;color:var(--mid)"></i></div>'
    )
    price   = _fmt_price(v["price"])
    emi_val = int(calc_emi(v["price"] * 0.8, 8.5, 5))
    emi_fmt = f"₹{emi_val:,}"
    badge   = render_status_badge(v["status"])
    km      = f'{v["km_driven"]:,} km' if v.get("km_driven") else "0 km"
    fav_style = "background:rgba(200,168,75,.12);border-color:rgba(200,168,75,.4);color:var(--accent)" if fav else "background:transparent;border-color:var(--card-border);color:var(--gray)"
    in_cmp = vehicle_id in compare
    cmp_style = "background:rgba(200,168,75,.08);border-color:rgba(200,168,75,.3);color:var(--accent)" if in_cmp else "background:transparent;border-color:var(--card-border);color:var(--gray)"

    _html(f"""
    <div style="background:var(--charcoal);border-bottom:1px solid var(--card-border);
                padding:32px 40px 40px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">
        <div>{img_html}</div>
        <div>
          <div class="ae-detail-brand">{v['brand']}</div>
          <h1 class="ae-detail-name">{v['model']}</h1>
          <div class="ae-detail-variant">{v['variant']}</div>
          <div class="ae-detail-price">{price}</div>
          <div style="font-size:13px;color:var(--gray);margin-bottom:20px">
            EMI from {emi_fmt}/month ·
            <a href="?page=financing" style="color:var(--accent);text-decoration:none">
              Calculate EMI
            </a>
          </div>
          <div class="ae-detail-meta">
            <span class="ae-detail-meta-item">
              <i class="ti ti-calendar"></i>{v['year']}
            </span>
            <span class="ae-detail-meta-item">
              <i class="ti ti-droplet"></i>{v['fuel']}
            </span>
            <span class="ae-detail-meta-item">
              <i class="ti ti-settings-2"></i>{v['transmission']}
            </span>
            <span class="ae-detail-meta-item">
              <i class="ti ti-road"></i>{km}
            </span>
            {'<span class="ae-detail-meta-item"><i class="ti ti-palette"></i>' + v['color'] + '</span>' if v.get('color') else ''}
          </div>
          <div style="margin-bottom:24px">{badge}</div>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <a href="?page=detail&vid={v['id']}&action=testdrive"
               style="display:inline-flex;align-items:center;gap:7px;padding:13px 22px;
                      background:var(--accent);color:var(--black);border-radius:8px;
                      font-weight:600;font-size:14px;text-decoration:none">
              <i class="ti ti-key"></i> Book Test Drive
            </a>
            <a href="?page=detail&vid={v['id']}&action=quote"
               style="display:inline-flex;align-items:center;gap:7px;padding:12px 20px;
                      background:transparent;color:var(--white);border-radius:8px;
                      border:1px solid rgba(255,255,255,.2);font-weight:500;
                      font-size:14px;text-decoration:none">
              <i class="ti ti-file-text"></i> Request Quote
            </a>
            <a href="?page=detail&vid={v['id']}&action=fav"
               style="display:inline-flex;align-items:center;gap:7px;padding:12px 18px;
                      border-radius:8px;border:1px solid;font-size:13px;font-weight:500;
                      text-decoration:none;{fav_style}">
              <i class="ti {'ti-heart-filled' if fav else 'ti-heart'}"></i>
              {'Saved' if fav else 'Save'}
            </a>
            <a href="?page=detail&vid={v['id']}&action=compare"
               style="display:inline-flex;align-items:center;gap:7px;padding:12px 18px;
                      border-radius:8px;border:1px solid;font-size:13px;font-weight:500;
                      text-decoration:none;{cmp_style}">
              <i class="ti {'ti-check' if in_cmp else 'ti-scale'}"></i>
              {'In Compare' if in_cmp else 'Compare'}
            </a>
          </div>
        </div>
      </div>
    </div>""")

    # ── Handle inline actions ──
    action = st.query_params.get("action", "")

    if action == "fav":
        if user_id:
            added = toggle_favourite(user_id, vehicle_id)
            if added:
                st.session_state.setdefault("favourites", [])
                if vehicle_id not in st.session_state["favourites"]:
                    st.session_state["favourites"].append(vehicle_id)
                render_success_toast(f"{v['brand']} {v['model']} added to saved vehicles.")
            else:
                if vehicle_id in st.session_state.get("favourites", []):
                    st.session_state["favourites"].remove(vehicle_id)
                render_info_toast(f"{v['brand']} {v['model']} removed from saved vehicles.")
        else:
            render_info_toast("Sign in to save vehicles to your garage.")
        # Clear action param
        st.query_params["action"] = ""

    if action == "compare":
        ids = st.session_state.get("compare_ids", [])
        if vehicle_id in ids:
            ids.remove(vehicle_id)
            render_info_toast(f"{v['brand']} {v['model']} removed from comparison.")
        elif len(ids) < 3:
            ids.append(vehicle_id)
            render_success_toast(f"{v['brand']} {v['model']} added to comparison.")
        else:
            render_info_toast("You can compare up to 3 vehicles at a time.")
        st.session_state["compare_ids"] = ids
        st.query_params["action"] = ""

    # ── Spec grid ──
    specs = [
        ("ti-engine",      "Engine",       v.get("engine")),
        ("ti-bolt",        "Power",        v.get("power")),
        ("ti-gyroscope",   "Torque",       v.get("torque")),
        ("ti-settings-2",  "Transmission", v.get("transmission")),
        ("ti-droplet",     "Fuel Type",    v.get("fuel")),
        ("ti-gauge",       "Mileage",      f'{v["mileage"]} km/l' if v.get("mileage") else None),
        ("ti-car",         "Body Type",    v.get("body_type")),
        ("ti-palette",     "Colour",       v.get("color")),
    ]
    spec_cards = "".join(render_specification(i, l, val) for i, l, val in specs if val)
    _html(f"""
    <div style="padding:32px 40px">
      <div class="ae-eyebrow" style="margin-bottom:20px">Specifications</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px">
        {spec_cards}
      </div>
    </div>""")

    # ── Description ──
    if v.get("description"):
        _html(f"""
        <div style="padding:0 40px 32px">
          <div style="background:var(--card-bg);border:1px solid var(--card-border);
                      border-radius:12px;padding:28px">
            <div class="ae-eyebrow" style="margin-bottom:12px">About This Vehicle</div>
            <p style="font-size:15px;color:var(--light);line-height:1.75;margin:0">
              {v['description']}
            </p>
          </div>
        </div>""")

    # ── Price & EMI summary ──
    _html(f"""
    <div style="padding:0 40px 32px">
      <div style="background:var(--charcoal);border:1px solid var(--card-border);
                  border-radius:14px;padding:28px;display:grid;
                  grid-template-columns:1fr 1fr 1fr;gap:24px">
        <div>
          <div class="ae-eyebrow" style="margin-bottom:6px">Vehicle Price</div>
          <div style="font-family:'Playfair Display',serif;font-size:28px;
                      font-weight:700;color:var(--accent)">{price}</div>
          <div style="font-size:12px;color:var(--gray);margin-top:4px">On-road price varies by city</div>
        </div>
        <div>
          <div class="ae-eyebrow" style="margin-bottom:6px">Estimated EMI</div>
          <div style="font-family:'Playfair Display',serif;font-size:28px;
                      font-weight:700;color:var(--white)">{emi_fmt}<span style="font-size:14px;font-weight:400;color:var(--gray)">/mo</span></div>
          <div style="font-size:12px;color:var(--gray);margin-top:4px">80% loan · 8.5% p.a. · 5 years</div>
        </div>
        <div style="display:flex;align-items:flex-end">
          <a href="?page=financing"
             style="display:inline-flex;align-items:center;gap:6px;padding:10px 20px;
                    border:1px solid var(--card-border);border-radius:8px;color:var(--gray);
                    font-size:13px;text-decoration:none">
            <i class="ti ti-calculator"></i> Full Calculator
          </a>
        </div>
      </div>
    </div>""")

    # ── Test Drive inline form ──
    if action == "testdrive":
        _html('<div style="padding:0 40px 32px">')
        _html("""
        <div style="background:var(--card-bg);border:1px solid rgba(200,168,75,.2);
                    border-radius:14px;padding:28px;max-width:560px">
          <div class="ae-eyebrow" style="margin-bottom:6px">Book a Test Drive</div>
          <h3 style="font-size:22px;font-weight:600;color:var(--white);margin-bottom:20px">
            Schedule Your Experience
          </h3>""")
        with st.form("td_form"):
            c1, c2 = st.columns(2)
            with c1:
                td_name  = st.text_input("Full Name *")
                td_phone = st.text_input("Phone *")
            with c2:
                td_date = st.date_input("Preferred Date *")
                td_time = st.selectbox("Time Slot *",
                    ["10:00 AM","11:00 AM","12:00 PM","2:00 PM",
                     "3:00 PM","4:00 PM","5:00 PM"])
            td_email = st.text_input("Email (optional)")
            td_notes = st.text_input("Notes (optional)", placeholder="Any special requests…")
            submitted = st.form_submit_button("Confirm Test Drive", use_container_width=True)
            if submitted:
                if not td_name or not td_phone:
                    st.error("Please enter your name and phone number.")
                else:
                    book_test_drive({
                        "user_id":    user_id or None,
                        "vehicle_id": vehicle_id,
                        "name":       td_name,
                        "phone":      td_phone,
                        "email":      td_email,
                        "drive_date": str(td_date),
                        "time_slot":  td_time,
                        "notes":      td_notes,
                    })
                    render_success_toast(
                        f"Test drive confirmed for {v['brand']} {v['model']} "
                        f"on {td_date} at {td_time}. We'll send a reminder."
                    )
                    st.query_params["action"] = ""
        _html("</div></div>")

    # ── Quote inline form ──
    if action == "quote":
        _html('<div style="padding:0 40px 32px">')
        _html("""
        <div style="background:var(--card-bg);border:1px solid rgba(200,168,75,.2);
                    border-radius:14px;padding:28px;max-width:560px">
          <div class="ae-eyebrow" style="margin-bottom:6px">Request a Quote</div>
          <h3 style="font-size:22px;font-weight:600;color:var(--white);margin-bottom:20px">
            Get Personalised Pricing
          </h3>""")
        with st.form("quote_form"):
            c1, c2 = st.columns(2)
            with c1:
                q_name  = st.text_input("Full Name *")
                q_phone = st.text_input("Phone *")
            with c2:
                q_email = st.text_input("Email *")
                q_fin   = st.selectbox("Financing Interest",
                    ["Interested in financing","Paying outright","Undecided"])
            q_msg = st.text_area("Message", placeholder="Any specific requirements…", height=80)
            submitted = st.form_submit_button("Submit Request", use_container_width=True)
            if submitted:
                if not q_name or not q_phone or not q_email:
                    st.error("Please fill in all required fields.")
                else:
                    create_enquiry({
                        "user_id":    user_id or None,
                        "vehicle_id": vehicle_id,
                        "type":       "Quote",
                        "name":       q_name,
                        "phone":      q_phone,
                        "email":      q_email,
                        "message":    q_msg,
                        "financing":  q_fin,
                    })
                    render_success_toast(
                        "Quote request submitted! Our team will contact you within 4 hours."
                    )
                    st.query_params["action"] = ""
        _html("</div></div>")

    _html('<div style="padding:0 40px 48px">')
    _html(f"""
    <div style="background:var(--charcoal);border:1px solid var(--card-border);
                border-radius:12px;padding:24px;display:flex;align-items:center;
                justify-content:space-between;flex-wrap:wrap;gap:16px">
      <div>
        <div style="font-size:15px;font-weight:600;color:var(--white)">
          Interested in {v['brand']} {v['model']}?
        </div>
        <div style="font-size:13px;color:var(--gray);margin-top:4px">
          Call us: <strong style="color:var(--accent)">+91 80 4567 8900</strong>
          · Mon–Sat 9am–7pm
        </div>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a href="?page=detail&vid={v['id']}&action=testdrive"
           style="display:inline-flex;align-items:center;gap:6px;padding:11px 20px;
                  background:var(--accent);color:var(--black);border-radius:8px;
                  font-weight:600;font-size:13px;text-decoration:none">
          Book Test Drive
        </a>
        <a href="?page=compare"
           style="display:inline-flex;align-items:center;gap:6px;padding:10px 18px;
                  border:1px solid var(--card-border);color:var(--gray);border-radius:8px;
                  font-size:13px;text-decoration:none">
          Compare Vehicles
        </a>
      </div>
    </div>""")
    _html("</div>")

    render_footer()
