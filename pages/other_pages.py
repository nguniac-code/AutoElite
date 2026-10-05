"""
AutoElite — Compare / Financing / Services / About pages
"""

import streamlit as st
from components.ui import (
    _html, render_page_header, render_section_header, render_booking_step,
    render_empty_state, render_success_toast, render_info_toast,
    render_footer, calc_emi,
)
from utils.database import (
    get_vehicle, get_all_vehicles, get_brands,
    book_test_drive, create_enquiry, _fmt_price,
)


# ── COMPARE PAGE ──────────────────────────────────────────────────────────────
def render_compare_page() -> None:
    render_page_header(
        "Side by Side", "Compare Vehicles",
        "Make an informed decision. Add up to 3 vehicles from any listing.",
    )

    compare_ids = st.session_state.get("compare_ids", [])
    vehicles    = [get_vehicle(vid) for vid in compare_ids if get_vehicle(vid)]

    if not vehicles:
        _html('<div style="padding:0 40px 64px">')
        render_empty_state(
            "ti-scale",
            "No vehicles selected for comparison",
            "Browse our collection and tap Compare on up to 3 vehicles, "
            "then come back here to see them side by side.",
            "Browse Vehicles", "?page=cars",
        )
        _html("</div>")
        render_footer()
        return

    # Build comparison table
    specs = [
        ("Year",         lambda v: str(v["year"])),
        ("Price",        lambda v: _fmt_price(v["price"])),
        ("Fuel",         lambda v: v["fuel"]),
        ("Transmission", lambda v: v["transmission"]),
        ("Body Type",    lambda v: v["body_type"]),
        ("Engine",       lambda v: v.get("engine") or "—"),
        ("Power",        lambda v: v.get("power") or "—"),
        ("Torque",       lambda v: v.get("torque") or "—"),
        ("Mileage",      lambda v: f'{v["mileage"]} km/l' if v.get("mileage") else "—"),
        ("Status",       lambda v: v["status"]),
    ]

    # Best-value logic (lower price = best, higher power/mileage = best)
    def is_best(spec_label: str, value: str, all_vals: list[str]) -> bool:
        try:
            if spec_label == "Price":
                nums = [float(v.replace("₹","").replace("L","").replace("Cr","").replace(",",""))
                        for v in all_vals if v != "—"]
                cur  = float(value.replace("₹","").replace("L","").replace("Cr","").replace(",",""))
                return cur == min(nums)
            if spec_label == "Mileage":
                nums = [float(v.replace(" km/l","")) for v in all_vals if v != "—"]
                cur  = float(value.replace(" km/l",""))
                return cur == max(nums)
            if spec_label == "Power":
                nums = [int(v.replace(" HP","")) for v in all_vals if v != "—" and "HP" in v]
                cur  = int(value.replace(" HP",""))
                return cur == max(nums)
        except Exception:
            pass
        return False

    header_row = "".join(
        f"""<th style="text-align:left;padding:20px 24px;background:var(--dark);
                      border-bottom:1px solid var(--card-border)">
              <div style="font-size:13px;font-weight:600;color:var(--white)">
                {v['brand']}
              </div>
              <div style="font-size:12px;color:var(--gray);margin-top:2px">
                {v['model']} {v['variant']}
              </div>
              <div style="font-size:20px;font-weight:700;color:var(--accent);
                          font-family:'Playfair Display',serif;margin-top:6px">
                {_fmt_price(v['price'])}
              </div>
            </th>"""
        for v in vehicles
    )

    rows_html = ""
    for spec_label, getter in specs:
        vals    = [getter(v) for v in vehicles]
        row_tds = "".join(
            f'<td style="padding:13px 24px;border-bottom:1px solid rgba(42,42,53,.5);'
            f'font-size:14px;'
            f'{"color:var(--accent);font-weight:700" if is_best(spec_label,val,vals) else "color:var(--light)"}">'
            f'{val}'
            f'{"<span style=\"font-size:10px;margin-left:6px;color:var(--accent)\">★ BEST</span>" if is_best(spec_label,val,vals) else ""}'
            f'</td>'
            for val in vals
        )
        rows_html += (
            f'<tr>'
            f'<td style="padding:13px 24px;border-bottom:1px solid rgba(42,42,53,.5);'
            f'font-size:12px;color:var(--gray);text-transform:uppercase;'
            f'letter-spacing:.5px;font-weight:500;background:var(--dark)">'
            f'{spec_label}</td>'
            f'{row_tds}'
            f'</tr>'
        )

    _html(f"""
    <div style="padding:0 40px 32px;overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                    border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
        <thead>
          <tr>
            <th style="padding:20px 24px;background:var(--dark);
                       border-bottom:1px solid var(--card-border);
                       font-size:12px;color:var(--gray);text-transform:uppercase;
                       letter-spacing:1px;font-weight:600;text-align:left;
                       width:160px">Specification</th>
            {header_row}
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""")

    # Remove buttons
    _html('<div style="padding:0 40px 16px;display:flex;gap:12px;flex-wrap:wrap">')
    for v in vehicles:
        if st.button(f"✕  Remove {v['brand']} {v['model']}", key=f"rm_{v['id']}"):
            st.session_state["compare_ids"] = [
                i for i in compare_ids if i != v["id"]
            ]
            st.rerun()
    if st.button("＋  Add another vehicle", key="cmp_add"):
        st.query_params["page"] = "cars"
        st.rerun()
    _html("</div>")

    render_footer()


# ── FINANCING PAGE ────────────────────────────────────────────────────────────
def render_financing_page() -> None:
    render_page_header(
        "Financial Planning", "EMI Calculator",
        "Estimate your monthly payments and plan your ownership journey.",
    )

    _html('<div style="padding:0 40px 64px">')

    col_left, col_right = st.columns(2, gap="large")

    # ── Left: sliders ──
    with col_left:
        _html('<div class="ae-finance-panel">')
        _html('<div class="ae-eyebrow" style="margin-bottom:24px">Loan Parameters</div>')

        price   = st.slider("Vehicle Price (₹)",
                            500_000, 20_000_000, 5_000_000, 100_000,
                            format="₹%d", key="fin_price")
        down    = st.slider("Down Payment (₹)",
                            0, min(price, 8_000_000), min(1_000_000, price // 5), 50_000,
                            format="₹%d", key="fin_down")
        rate    = st.slider("Interest Rate (% p.a.)",
                            5.0, 20.0, 8.5, 0.5,
                            format="%.1f%%", key="fin_rate")
        tenure  = st.slider("Loan Tenure (years)",
                            1, 7, 5, 1,
                            format="%d yr", key="fin_tenure")

        principal  = max(0, price - down)
        emi_val    = calc_emi(principal, rate, tenure)
        total_pay  = emi_val * tenure * 12
        interest   = total_pay - principal
        processing = principal * 0.005

        st.divider()
        _html('<div class="ae-form-divider" style="margin-top:0">Your Details</div>')
        with st.form("fin_form"):
            fin_name  = st.text_input("Full Name")
            fin_phone = st.text_input("Phone Number")
            fin_city  = st.selectbox("City", [
                "Bangalore", "Mumbai", "Delhi", "Chennai",
                "Hyderabad", "Pune", "Kolkata", "Other",
            ])
            submitted = st.form_submit_button(
                "Request Financing", use_container_width=True
            )
            if submitted:
                if fin_name and fin_phone:
                    create_enquiry({
                        "user_id":  st.session_state.get("user_id"),
                        "type":     "Financing",
                        "name":     fin_name,
                        "phone":    fin_phone,
                        "message":  f"City: {fin_city}. Price: {_fmt_price(price)}",
                    })
                    render_success_toast(
                        "Financing request submitted! Our advisor will call you within 24 hours."
                    )
                else:
                    st.error("Please enter your name and phone number.")
        _html("</div>")

    # ── Right: results ──
    with col_right:
        _html('<div class="ae-finance-panel">')
        _html(f"""
        <div class="ae-emi-display">
          <div class="ae-emi-label">Monthly EMI</div>
          <div class="ae-emi-amount">₹{int(emi_val):,}</div>
          <div class="ae-emi-period">per month for {tenure} year{'s' if tenure > 1 else ''}</div>
        </div>
        <div style="margin-bottom:24px">
          <div class="ae-breakdown-row">
            <span class="ae-breakdown-label">Principal amount</span>
            <span class="ae-breakdown-val">{_fmt_price(principal)}</span>
          </div>
          <div class="ae-breakdown-row">
            <span class="ae-breakdown-label">Total interest</span>
            <span class="ae-breakdown-val">{_fmt_price(int(interest))}</span>
          </div>
          <div class="ae-breakdown-row">
            <span class="ae-breakdown-label">Processing fee (0.5%)</span>
            <span class="ae-breakdown-val">{_fmt_price(int(processing))}</span>
          </div>
          <div class="ae-breakdown-row" style="border-top:1px solid var(--card-border);
               padding-top:16px;margin-top:4px">
            <span style="font-size:15px;font-weight:600;color:var(--light)">
              Total payable
            </span>
            <span style="font-size:18px;font-weight:700;color:var(--accent)">
              {_fmt_price(int(total_pay + processing))}
            </span>
          </div>
        </div>""")

        # Visual breakdown bar
        if principal > 0:
            p_pct = int(principal / (principal + interest) * 100)
            i_pct = 100 - p_pct
            _html(f"""
            <div>
              <div style="font-size:11px;color:var(--gray);text-transform:uppercase;
                          letter-spacing:1px;font-weight:500;margin-bottom:12px">
                Payment Breakdown
              </div>
              <div style="display:flex;gap:4px;height:10px;border-radius:6px;overflow:hidden">
                <div style="flex:{p_pct};background:var(--accent);opacity:.85"></div>
                <div style="flex:{i_pct};background:var(--mid)"></div>
              </div>
              <div style="display:flex;gap:20px;margin-top:10px">
                <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--gray)">
                  <div style="width:10px;height:10px;border-radius:2px;background:var(--accent);opacity:.85"></div>
                  Principal ({p_pct}%)
                </div>
                <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--gray)">
                  <div style="width:10px;height:10px;border-radius:2px;background:var(--mid)"></div>
                  Interest ({i_pct}%)
                </div>
              </div>
            </div>""")

        _html("""
        <div class="ae-finance-note" style="margin-top:24px">
          These figures are estimates and may vary based on lender terms and credit profile.
        </div>
        </div>""")  # close ae-finance-panel

    _html("</div>")  # close padding wrapper

    # Partner logos strip
    _html("""
    <div style="padding:0 40px 64px">
      <div style="background:var(--charcoal);border:1px solid var(--card-border);
                  border-radius:12px;padding:28px">
        <div class="ae-eyebrow" style="text-align:center;margin-bottom:20px">
          Financing Partners
        </div>
        <div style="display:flex;gap:32px;justify-content:center;align-items:center;flex-wrap:wrap">
          <span style="font-size:16px;font-weight:700;color:var(--gray)">HDFC Bank</span>
          <span style="font-size:16px;font-weight:700;color:var(--gray)">ICICI Bank</span>
          <span style="font-size:16px;font-weight:700;color:var(--gray)">Axis Bank</span>
          <span style="font-size:16px;font-weight:700;color:var(--gray)">Kotak Mahindra</span>
          <span style="font-size:16px;font-weight:700;color:var(--gray)">SBI</span>
        </div>
      </div>
    </div>""")

    render_footer()


# ── SERVICES PAGE ─────────────────────────────────────────────────────────────
def render_services_page() -> None:
    render_page_header(
        "What We Offer", "Our Services",
        "Everything you need for a seamless vehicle ownership experience.",
    )
    _html('<div style="padding:0 40px 64px">')

    # Service cards grid
    svcs = [
        ("ti-credit-card",  "Vehicle Financing",
         "Competitive interest rates from 7.9% p.a. Loan up to 90% of vehicle value. "
         "Flexible tenure from 12 to 84 months.",
         "?page=financing", "Calculate EMI"),
        ("ti-key",          "Test Drive",
         "Experience the vehicle at your nearest AutoElite showroom or opt for an "
         "at-home test drive in select cities. Available 7 days a week.",
         None, "Book Below"),
        ("ti-refresh",      "Trade-In Program",
         "Get a fair market valuation for your current vehicle. Apply the value "
         "directly toward your next AutoElite purchase.",
         None, "Request Below"),
        ("ti-shield",       "Insurance",
         "Comprehensive and third-party insurance from leading providers. "
         "Zero depreciation and add-on cover options available.",
         None, "Coming Soon"),
        ("ti-tool",         "Annual Maintenance",
         "Prepaid service packages covering scheduled maintenance at authorised "
         "service centres across India.",
         None, "At Showroom"),
        ("ti-truck",        "Home Delivery",
         "Complete paperwork online and have your vehicle delivered to your "
         "doorstep in select metros. Available in 12 cities.",
         None, "At Checkout"),
    ]

    c1, c2, c3 = st.columns(3, gap="medium")
    cols = [c1, c2, c3]
    for i, (icon, title, text, href, btn) in enumerate(svcs):
        with cols[i % 3]:
            link = href or "#"
            _html(f"""
            <div class="ae-svc-card" style="margin-bottom:20px">
              <div class="ae-svc-icon"><i class="ti {icon}"></i></div>
              <div class="ae-svc-title">{title}</div>
              <p class="ae-svc-text">{text}</p>
              <a href="{link}" style="display:inline-flex;align-items:center;gap:6px;
                 padding:9px 18px;border-radius:8px;font-size:13px;font-weight:600;
                 text-decoration:none;background:var(--accent);color:var(--black);
                 margin-top:auto">
                {btn} <i class="ti ti-arrow-right"></i>
              </a>
            </div>""")
    _html("</div>")

    # ── Test drive booking ──
    _html('<div style="background:var(--charcoal);padding:64px 40px">')
    render_section_header(
        "Step by Step", "Book a Test Drive",
        "Simple. Fast. On your schedule.",
    )

    vehicles_list = get_all_vehicles(status_filter="Available")
    vehicle_options = {
        f"{v['brand']} {v['model']} {v['variant']} ({v['year']})": v["id"]
        for v in vehicles_list
    }

    col_steps, col_form = st.columns([1, 1], gap="large")

    with col_steps:
        render_booking_step("1", "Select a Vehicle",
                            "Browse and choose the car you want to experience.", "done")
        render_booking_step("2", "Choose a Date & Time",
                            "Pick a slot that works for you.", "active")
        render_booking_step("3", "Your Details",
                            "We need your contact info to confirm the booking.", "active")
        render_booking_step("4", "Confirm",
                            "We'll send a confirmation within 2 hours.", "pending")

    with col_form:
        with st.form("svc_td_form"):
            vehicle_label = st.selectbox("Select Vehicle *", list(vehicle_options.keys()))
            c1, c2 = st.columns(2)
            with c1:
                td_name  = st.text_input("Full Name *")
                td_date  = st.date_input("Preferred Date *")
            with c2:
                td_phone = st.text_input("Phone *")
                td_time  = st.selectbox("Time Slot *", [
                    "10:00 AM","11:00 AM","12:00 PM",
                    "2:00 PM","3:00 PM","4:00 PM","5:00 PM",
                ])
            td_email  = st.text_input("Email (optional)")
            td_notes  = st.text_area("Notes (optional)", height=80)
            submitted = st.form_submit_button(
                "Confirm Test Drive Booking", use_container_width=True
            )
            if submitted:
                if not td_name or not td_phone:
                    st.error("Please enter your name and phone number.")
                else:
                    book_test_drive({
                        "user_id":    st.session_state.get("user_id"),
                        "vehicle_id": vehicle_options[vehicle_label],
                        "name":       td_name,
                        "phone":      td_phone,
                        "email":      td_email,
                        "drive_date": str(td_date),
                        "time_slot":  td_time,
                        "notes":      td_notes,
                    })
                    render_success_toast(
                        f"Test drive booked for {vehicle_label} on {td_date} at {td_time}. "
                        "We'll confirm within 2 hours."
                    )
    _html("</div>")

    # ── Trade-in enquiry ──
    _html('<div style="padding:64px 40px">')
    render_section_header("Turn Your Car Into Value", "Trade-In Valuation")

    col_info, col_form = st.columns([1, 1], gap="large")
    with col_info:
        _html("""
        <div style="display:flex;flex-direction:column;gap:16px">
          <div class="ae-why-card">
            <div class="ae-why-icon"><i class="ti ti-clock"></i></div>
            <div class="ae-why-title">Quick Valuation</div>
            <p class="ae-why-text">Get a fair market estimate in under 24 hours.</p>
          </div>
          <div class="ae-why-card">
            <div class="ae-why-icon"><i class="ti ti-currency-rupee"></i></div>
            <div class="ae-why-title">Best Market Price</div>
            <p class="ae-why-text">We offer competitive valuations backed by real-time market data.</p>
          </div>
          <div class="ae-why-card">
            <div class="ae-why-icon"><i class="ti ti-check"></i></div>
            <div class="ae-why-title">Hassle-Free Process</div>
            <p class="ae-why-text">Zero paperwork stress. We handle the transfer end to end.</p>
          </div>
        </div>""")

    with col_form:
        with st.form("tradein_form"):
            ti_name   = st.text_input("Your Name *")
            ti_phone  = st.text_input("Phone *")
            ti_brand  = st.text_input("Current Vehicle Brand *", placeholder="e.g. Toyota")
            ti_model  = st.text_input("Model & Year *", placeholder="e.g. Fortuner 2022")
            ti_km     = st.number_input("Kilometres Driven", min_value=0, step=1000)
            ti_cond   = st.selectbox("Condition", [
                "Excellent — no damage", "Good — minor wear", "Fair — some repairs needed",
            ])
            submitted = st.form_submit_button("Request Valuation", use_container_width=True)
            if submitted:
                if ti_name and ti_phone and ti_brand and ti_model:
                    create_enquiry({
                        "user_id": st.session_state.get("user_id"),
                        "type":    "TradeIn",
                        "name":    ti_name,
                        "phone":   ti_phone,
                        "message": f"{ti_brand} {ti_model} · {ti_km:,} km · {ti_cond}",
                    })
                    render_success_toast(
                        "Trade-in request submitted! Our team will send a valuation within 24 hours."
                    )
                else:
                    st.error("Please fill in all required fields.")
    _html("</div>")

    render_footer()


# ── ABOUT PAGE ────────────────────────────────────────────────────────────────
def render_about_page() -> None:
    # Mini hero
    _html("""
    <div class="ae-hero" style="min-height:300px">
      <div class="ae-hero-bg"></div>
      <div style="position:relative;z-index:2;max-width:600px">
        <div class="ae-hero-eyebrow">Our Story</div>
        <h1 class="ae-hero-title" style="font-size:44px">
          About <em>AutoElite</em>
        </h1>
        <p class="ae-hero-sub" style="font-size:16px">
          A decade of redefining automotive retail in India.
        </p>
      </div>
    </div>""")

    _html('<div style="padding:64px 40px">')
    col_story, col_stats = st.columns([3, 2], gap="large")

    with col_story:
        _html("""
        <h2 style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
                   color:var(--white);margin-bottom:20px">
          Premium automotive retail, reimagined.
        </h2>
        <p style="font-size:15px;color:var(--gray);line-height:1.8;margin-bottom:16px">
          AutoElite was founded on a simple belief: buying a premium car should feel as
          exceptional as driving one. We built every part of our platform — from our
          120-point inspection protocol to our transparent pricing model — around that conviction.
        </p>
        <p style="font-size:15px;color:var(--gray);line-height:1.8;margin-bottom:16px">
          Today we serve discerning buyers across India with an inventory of over 120 verified
          vehicles, no-surprise pricing, and a team that genuinely loves cars.
        </p>
        <p style="font-size:15px;color:var(--gray);line-height:1.8;margin-bottom:28px">
          Whether you're buying your first luxury vehicle or upgrading to something extraordinary,
          our specialists are here to guide every step — from discovery to delivery.
        </p>
        <a href="?page=cars"
           style="display:inline-flex;align-items:center;gap:8px;padding:13px 26px;
                  background:var(--accent);color:var(--black);border-radius:8px;
                  font-weight:600;font-size:14px;text-decoration:none">
          Browse Our Collection <i class="ti ti-arrow-right"></i>
        </a>""")

    with col_stats:
        milestones = [
            ("2014", "Founded in Bangalore",
             "Started with 12 vehicles and a vision for honest automotive retail."),
            ("120+", "Verified vehicles",
             "Every car inspected, every price verified, every claim substantiated."),
            ("842",  "Happy owners",
             "Customers who drove away satisfied and came back to recommend us."),
            ("12",   "Cities served",
             "Showrooms and delivery partners across metropolitan India."),
        ]
        for val, title, text in milestones:
            _html(f"""
            <div class="ae-why-card" style="margin-bottom:14px">
              <div style="font-size:32px;font-weight:700;color:var(--accent);
                          font-family:'Playfair Display',serif;margin-bottom:4px">{val}</div>
              <div class="ae-why-title" style="margin-bottom:4px">{title}</div>
              <div class="ae-why-text">{text}</div>
            </div>""")

    _html("</div>")

    # Team philosophy
    _html("""
    <div style="background:var(--charcoal);padding:64px 40px">
      <div style="text-align:center;max-width:600px;margin:0 auto 48px">
        <div class="ae-eyebrow" style="text-align:center;margin-bottom:12px">Our Philosophy</div>
        <h2 class="ae-section-title" style="text-align:center">Driven by Values</h2>
        <p class="ae-section-sub" style="text-align:center;margin:12px auto 0">
          Every decision we make is guided by three commitments.
        </p>
      </div>
    </div>""")

    _html('<div style="background:var(--charcoal);padding:0 40px 64px">')
    c1, c2, c3 = st.columns(3, gap="medium")
    values = [
        ("ti-heart", "Integrity",
         "We never hide a cost, overlook a defect, or push a vehicle that isn't right for you. "
         "Our business is built on long-term trust, not short-term sales."),
        ("ti-bulb", "Excellence",
         "From the vehicles we list to the experience we deliver, we hold ourselves to "
         "standards that exceed what the industry asks of us."),
        ("ti-users", "Partnership",
         "We see every customer as a long-term partner. Your second car should be as good "
         "an experience as your first — and your third even better."),
    ]
    for col, (icon, title, text) in zip([c1, c2, c3], values):
        with col:
            _html(f"""
            <div class="ae-why-card">
              <div class="ae-why-icon"><i class="ti {icon}"></i></div>
              <div class="ae-why-title">{title}</div>
              <p class="ae-why-text">{text}</p>
            </div>""")
    _html("</div>")

    # Contact
    _html('<div style="padding:64px 40px">')
    render_section_header("Get in Touch", "Contact Us")
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    contacts = [
        ("ti-phone",   "Call Us",
         "+91 80 4567 8900", "Mon–Sat, 9am–7pm"),
        ("ti-mail",    "Email Us",
         "hello@autoelite.in", "Response within 4 hours"),
        ("ti-map-pin", "Bangalore Showroom",
         "Indiranagar, Bangalore", "Open 7 days 9am–7pm"),
        ("ti-map-pin", "Mumbai Showroom",
         "Bandra West, Mumbai", "Open 7 days 9am–7pm"),
    ]
    for col, (icon, title, line1, line2) in zip([c1, c2, c3, c4], contacts):
        with col:
            _html(f"""
            <div class="ae-why-card" style="text-align:center">
              <div class="ae-why-icon" style="text-align:center">
                <i class="ti {icon}"></i>
              </div>
              <div class="ae-why-title">{title}</div>
              <div style="font-size:14px;color:var(--light);margin-bottom:4px">{line1}</div>
              <div style="font-size:12px;color:var(--gray)">{line2}</div>
            </div>""")
    _html("</div>")

    # Contact form
    _html('<div style="background:var(--charcoal);padding:0 40px 64px">')
    _html("""
    <div style="max-width:600px;margin:0 auto">
      <h3 style="font-size:24px;font-weight:600;color:var(--white);
                 margin-bottom:24px;padding-top:64px">Send us a message</h3>""")
    with st.form("contact_form"):
        c1, c2 = st.columns(2)
        with c1:
            ct_name  = st.text_input("Full Name *")
            ct_phone = st.text_input("Phone")
        with c2:
            ct_email = st.text_input("Email *")
            ct_subj  = st.selectbox("Subject", [
                "General Inquiry", "Vehicle Enquiry",
                "Test Drive", "Financing", "Trade-In", "Complaint",
            ])
        ct_msg = st.text_area("Message *", height=100)
        submitted = st.form_submit_button("Send Message", use_container_width=True)
        if submitted:
            if ct_name and ct_email and ct_msg:
                create_enquiry({
                    "user_id": st.session_state.get("user_id"),
                    "type":    "General",
                    "name":    ct_name,
                    "phone":   ct_phone,
                    "email":   ct_email,
                    "message": f"[{ct_subj}] {ct_msg}",
                })
                render_success_toast("Message sent! We'll get back to you within 4 hours.")
            else:
                st.error("Please fill in your name, email, and message.")
    _html("</div></div>")

    render_footer()
