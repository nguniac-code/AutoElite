"""
AutoElite — Customer Dashboard, Favourites & Auth Pages
"""

import streamlit as st
from components.ui import (
    _html, render_page_header, render_vehicle_grid, render_empty_state,
    render_status_badge, render_success_toast, render_info_toast,
    render_footer,
)
from utils.database import (
    get_favourites, get_test_drives, get_enquiries,
    get_favourite_count, get_test_drive_count, get_enquiry_count,
    toggle_favourite, login_user, register_user, _fmt_price,
)


# ── AUTH ──────────────────────────────────────────────────────────────────────
def render_auth_page() -> None:
    _html("""
    <div style="min-height:80vh;display:flex;align-items:center;justify-content:center;
                padding:40px">
      <div style="width:100%;max-width:440px">
        <div style="text-align:center;margin-bottom:32px">
          <div style="font-family:'Playfair Display',serif;font-size:28px;
                      font-weight:700;color:var(--white);margin-bottom:4px">
            AUTO<span style="color:var(--accent)">ELITE</span>
          </div>
          <div style="font-size:13px;color:var(--gray)">Drive Your Ambition.</div>
        </div>
    """)

    tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

    # ── Login ──
    with tab_login:
        _html('<div style="padding:8px 0">')
        with st.form("login_form"):
            email    = st.text_input("Email address",    placeholder="name@email.com")
            password = st.text_input("Password",         type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                if email and password:
                    user = login_user(email, password)
                    if user:
                        st.session_state["user_id"]   = user["id"]
                        st.session_state["user_name"]  = user["name"]
                        st.session_state["user_role"]  = user["role"]
                        st.session_state["user_email"] = user["email"]
                        # Load favourites
                        favs = get_favourites(user["id"])
                        st.session_state["favourites"] = [v["id"] for v in favs]
                        render_success_toast(f"Welcome back, {user['name']}!")
                        st.query_params["page"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")
                else:
                    st.error("Please enter your email and password.")

        _html("""
        <div style="margin-top:16px;padding:14px;background:var(--dark);
                    border-radius:8px;border:1px solid var(--card-border)">
          <div style="font-size:11px;color:var(--accent);text-transform:uppercase;
                      letter-spacing:1px;font-weight:600;margin-bottom:8px">Demo Accounts</div>
          <div style="font-size:12px;color:var(--gray);line-height:1.8">
            <strong style="color:var(--light)">Admin:</strong>
            admin@autoelite.in / admin123<br>
            <strong style="color:var(--light)">Customer:</strong>
            arjun@example.com / password123
          </div>
        </div>
        </div>""")

    # ── Register ──
    with tab_register:
        _html('<div style="padding:8px 0">')
        with st.form("register_form"):
            reg_name  = st.text_input("Full Name *")
            reg_email = st.text_input("Email *")
            reg_phone = st.text_input("Phone *")
            reg_pass  = st.text_input("Password *", type="password")
            reg_pass2 = st.text_input("Confirm Password *", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted:
                if not all([reg_name, reg_email, reg_phone, reg_pass, reg_pass2]):
                    st.error("Please fill in all fields.")
                elif reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                elif len(reg_pass) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    ok, msg = register_user(reg_name, reg_email, reg_phone, reg_pass)
                    if ok:
                        render_success_toast(
                            "Account created! Please sign in with your credentials."
                        )
                    else:
                        st.error(msg)
        _html("</div>")

    _html("</div></div>")


# ── CUSTOMER DASHBOARD ────────────────────────────────────────────────────────
def render_dashboard_page() -> None:
    user_id   = st.session_state.get("user_id", 0)
    user_name = st.session_state.get("user_name", "Guest")

    if not user_id:
        render_auth_page()
        return

    fav_count   = get_favourite_count(user_id)
    drive_count = get_test_drive_count(user_id)
    enq_count   = get_enquiry_count(user_id)

    # Header
    _html(f"""
    <div style="padding:40px 40px 32px;border-bottom:1px solid var(--card-border)">
      <div class="ae-eyebrow" style="margin-bottom:8px">Customer Portal</div>
      <h1 style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;
                 color:var(--white);margin-bottom:4px">
        Welcome back, {user_name.split()[0]}.
      </h1>
      <p style="font-size:15px;color:var(--gray)">Manage your AutoElite experience.</p>
    </div>""")

    # Stat row
    _html('<div style="padding:28px 40px">')
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        _html(f"""
        <div class="ae-kpi-card">
          <div class="ae-kpi-label">Saved Vehicles</div>
          <div class="ae-kpi-val" style="color:var(--accent)">{fav_count}</div>
        </div>""")
    with c2:
        _html(f"""
        <div class="ae-kpi-card">
          <div class="ae-kpi-label">Test Drives</div>
          <div class="ae-kpi-val">{drive_count}</div>
        </div>""")
    with c3:
        _html(f"""
        <div class="ae-kpi-card">
          <div class="ae-kpi-label">Enquiries</div>
          <div class="ae-kpi-val">{enq_count}</div>
        </div>""")
    with c4:
        _html("""
        <div class="ae-kpi-card">
          <div class="ae-kpi-label">Account</div>
          <div style="font-size:14px;color:var(--light);margin-top:8px">Premium Member</div>
          <div style="font-size:12px;color:var(--gray);margin-top:4px">Since 2024</div>
        </div>""")
    _html("</div>")

    # Tabs
    _html('<div style="padding:0 40px 64px">')
    tab_drives, tab_saved, tab_enq, tab_account = st.tabs([
        "Test Drives", "Saved Vehicles", "Enquiries", "Account"
    ])

    # ── Test drives tab ──
    with tab_drives:
        drives = get_test_drives(user_id)
        if not drives:
            render_empty_state(
                "ti-calendar",
                "No upcoming test drives",
                "Book a test drive and experience your shortlisted vehicles first-hand.",
                "Book a Test Drive", "?page=services",
            )
        else:
            _html("""
            <div style="overflow-x:auto;margin-top:16px">
            <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                          border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
              <thead>
                <tr>
                  <th style="padding:14px 20px;text-align:left;font-size:11px;color:var(--gray);
                             text-transform:uppercase;letter-spacing:1px;
                             background:var(--dark);border-bottom:1px solid var(--card-border)">
                    Vehicle</th>
                  <th style="padding:14px 20px;text-align:left;font-size:11px;color:var(--gray);
                             text-transform:uppercase;letter-spacing:1px;
                             background:var(--dark);border-bottom:1px solid var(--card-border)">
                    Date</th>
                  <th style="padding:14px 20px;text-align:left;font-size:11px;color:var(--gray);
                             text-transform:uppercase;letter-spacing:1px;
                             background:var(--dark);border-bottom:1px solid var(--card-border)">
                    Time</th>
                  <th style="padding:14px 20px;text-align:left;font-size:11px;color:var(--gray);
                             text-transform:uppercase;letter-spacing:1px;
                             background:var(--dark);border-bottom:1px solid var(--card-border)">
                    Status</th>
                </tr>
              </thead>
              <tbody>""")
            for d in drives:
                badge = render_status_badge(d.get("status", "Confirmed").replace("Confirmed", "Available"))
                _html(f"""
                <tr>
                  <td style="padding:14px 20px;font-size:14px;color:var(--white);font-weight:500;
                             border-bottom:1px solid rgba(42,42,53,.5)">
                    {d.get('brand','')} {d.get('model','')} {d.get('variant','')}
                  </td>
                  <td style="padding:14px 20px;font-size:14px;color:var(--light);
                             border-bottom:1px solid rgba(42,42,53,.5)">{d['drive_date']}</td>
                  <td style="padding:14px 20px;font-size:14px;color:var(--light);
                             border-bottom:1px solid rgba(42,42,53,.5)">{d['time_slot']}</td>
                  <td style="padding:14px 20px;border-bottom:1px solid rgba(42,42,53,.5)">
                    {badge}</td>
                </tr>""")
            _html("</tbody></table></div>")

    # ── Saved vehicles tab ──
    with tab_saved:
        favs_list = get_favourites(user_id)
        fav_ids   = {v["id"] for v in favs_list}
        if not favs_list:
            render_empty_state(
                "ti-heart",
                "Your garage is waiting",
                "Save vehicles you love and find them here whenever you're ready.",
                "Browse Vehicles", "?page=cars",
            )
        else:
            st.write("")
            render_vehicle_grid(favs_list, favourites=fav_ids, cols=3)

    # ── Enquiries tab ──
    with tab_enq:
        enqs = get_enquiries(user_id)
        if not enqs:
            render_empty_state(
                "ti-message",
                "No enquiries yet",
                "Your quote requests and enquiries will appear here.",
            )
        else:
            _html("""
            <div style="overflow-x:auto;margin-top:16px">
            <table style="width:100%;border-collapse:collapse;background:var(--card-bg);
                          border:1px solid var(--card-border);border-radius:12px;overflow:hidden">
              <thead>
                <tr>""")
            for h in ["Type", "Vehicle", "Date", "Status"]:
                _html(f"""
                  <th style="padding:14px 20px;text-align:left;font-size:11px;color:var(--gray);
                             text-transform:uppercase;letter-spacing:1px;
                             background:var(--dark);border-bottom:1px solid var(--card-border)">
                    {h}</th>""")
            _html("</tr></thead><tbody>")
            for e in enqs:
                status_map = {"New": "Available", "InProgress": "Reserved",
                              "Resolved": "Available", "Closed": "Sold"}
                badge = render_status_badge(status_map.get(e["status"], "Available"))
                vehicle_str = f"{e.get('brand','')} {e.get('model','')}".strip() or "General"
                _html(f"""
                <tr>
                  <td style="padding:14px 20px;font-size:14px;color:var(--white);font-weight:500;
                             border-bottom:1px solid rgba(42,42,53,.5)">{e['type']}</td>
                  <td style="padding:14px 20px;font-size:14px;color:var(--light);
                             border-bottom:1px solid rgba(42,42,53,.5)">{vehicle_str}</td>
                  <td style="padding:14px 20px;font-size:14px;color:var(--light);
                             border-bottom:1px solid rgba(42,42,53,.5)">{e['created_at'][:10]}</td>
                  <td style="padding:14px 20px;border-bottom:1px solid rgba(42,42,53,.5)">
                    {badge}</td>
                </tr>""")
            _html("</tbody></table></div>")

    # ── Account tab ──
    with tab_account:
        _html(f"""
        <div style="max-width:480px;margin-top:16px">
          <div style="background:var(--card-bg);border:1px solid var(--card-border);
                      border-radius:12px;padding:28px;margin-bottom:20px">
            <div class="ae-eyebrow" style="margin-bottom:16px">Account Details</div>
            <div style="display:flex;flex-direction:column;gap:14px">
              <div>
                <div style="font-size:11px;color:var(--gray);text-transform:uppercase;
                            letter-spacing:1px;margin-bottom:4px">Name</div>
                <div style="font-size:15px;color:var(--white);font-weight:500">
                  {st.session_state.get('user_name','')}
                </div>
              </div>
              <div>
                <div style="font-size:11px;color:var(--gray);text-transform:uppercase;
                            letter-spacing:1px;margin-bottom:4px">Email</div>
                <div style="font-size:15px;color:var(--white)">
                  {st.session_state.get('user_email','')}
                </div>
              </div>
              <div>
                <div style="font-size:11px;color:var(--gray);text-transform:uppercase;
                            letter-spacing:1px;margin-bottom:4px">Role</div>
                <div style="font-size:15px;color:var(--accent);font-weight:600;text-transform:capitalize">
                  {st.session_state.get('user_role','customer')}
                </div>
              </div>
            </div>
          </div>""")

        if st.button("Sign Out", key="signout_btn"):
            for key in ["user_id","user_name","user_role","user_email","favourites"]:
                st.session_state.pop(key, None)
            render_success_toast("You've been signed out successfully.")
            st.query_params["page"] = "home"
            st.rerun()

        _html("</div>")

    _html("</div>")
    render_footer()


# ── FAVOURITES PAGE ───────────────────────────────────────────────────────────
def render_favourites_page() -> None:
    user_id = st.session_state.get("user_id", 0)

    render_page_header(
        "Your Garage", "Saved Vehicles",
        "Vehicles you've shortlisted for closer consideration.",
    )

    _html('<div style="padding:0 40px 64px">')

    if not user_id:
        render_empty_state(
            "ti-lock",
            "Sign in to see your saved vehicles",
            "Create a free account to save vehicles, book test drives, "
            "and track your enquiries.",
            "Sign In", "?page=dashboard",
        )
    else:
        favs    = get_favourites(user_id)
        fav_ids = {v["id"] for v in favs}
        if not favs:
            render_empty_state(
                "ti-heart",
                "Your garage is waiting",
                "Save vehicles you love and find them here whenever you're ready.",
                "Browse Vehicles", "?page=cars",
            )
        else:
            _html(f'<div style="margin-bottom:20px;font-size:13px;color:var(--gray)">'
                  f'{len(favs)} saved vehicle{"s" if len(favs)!=1 else ""}</div>')
            render_vehicle_grid(favs, favourites=fav_ids, cols=3)

    _html("</div>")
    render_footer()
