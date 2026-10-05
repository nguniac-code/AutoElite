# AutoElite 🚘
### Premium Automotive Dealership Platform

> *Drive Your Ambition.*

A full-stack automotive retail web application built with **Python + Streamlit**,
featuring a luxury dark-mode UI, SQLite persistence, and a complete dealership CRM.

---

## Project Structure

```
autoelite/
├── app.py                        ← Entry point — run this
├── requirements.txt
├── autoelite.db                  ← Auto-created on first run
│
├── .streamlit/
│   └── config.toml               ← Theme & server config
│
├── components/
│   ├── styles.py                 ← All CSS (single source of truth)
│   └── ui.py                     ← Reusable HTML component functions
│
├── utils/
│   └── database.py               ← SQLite schema, seed data, all CRUD
│
└── pages/
    ├── home.py                   ← Home page (hero, search, featured, CTA)
    ├── cars.py                   ← Cars listing + vehicle detail
    ├── other_pages.py            ← Compare, Financing, Services, About
    ├── dashboard.py              ← Customer dashboard, Favourites, Auth
    └── admin.py                  ← Admin CRM (KPIs, analytics, inventory)
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Demo Accounts

| Role     | Email                    | Password     |
|----------|--------------------------|--------------|
| Admin    | admin@autoelite.in       | admin123     |
| Customer | arjun@example.com        | password123  |
| Customer | priya@example.com        | password123  |

---

## Features

### Customer-facing
| Feature            | Description                                               |
|--------------------|-----------------------------------------------------------|
| **Home**           | Cinematic hero, smart search, featured & popular grids    |
| **Vehicle Listing**| Filter by brand, fuel, body type, status; sort options    |
| **Vehicle Detail** | Full specs, gallery, inline test-drive & quote forms      |
| **Compare**        | Side-by-side table for up to 3 vehicles, best highlighted |
| **EMI Calculator** | Live sliders, principal/interest breakdown, bar chart     |
| **Services**       | Test drive booking, trade-in enquiry, service overview    |
| **Favourites**     | Save and retrieve shortlisted vehicles                    |
| **Dashboard**      | View test drives, saved vehicles, enquiries               |
| **Auth**           | Register, login, session management                       |

### Admin CRM
| Feature             | Description                                              |
|---------------------|----------------------------------------------------------|
| **KPI Overview**    | Revenue, vehicle count, customers, test drives, leads    |
| **Analytics**       | Bar chart (monthly), donut (status), line (revenue)      |
| **Inventory**       | Search/filter table, edit vehicle, delete with confirm   |
| **Add Vehicle**     | Full form — all fields including image URL               |
| **Test Drives**     | All bookings, confirm/cancel actions                     |
| **Enquiries**       | All enquiries, status update dropdown                    |
| **Users**           | User listing with roles                                  |

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | Streamlit + Custom CSS (Inter + Playfair Display) |
| Charts      | Plotly (bar, donut, line)         |
| Database    | SQLite via Python `sqlite3`       |
| Auth        | SHA-256 password hashing          |
| Icons       | Tabler Icons (CDN)                |
| Fonts       | Google Fonts (CDN)                |

---

## Navigation

The app uses `?page=` query parameters for routing:

| URL                         | Page              |
|-----------------------------|-------------------|
| `?page=home`                | Home              |
| `?page=cars`                | Vehicle Listing   |
| `?page=detail&vid=1`        | Vehicle Detail    |
| `?page=compare`             | Compare           |
| `?page=financing`           | EMI Calculator    |
| `?page=services`            | Services          |
| `?page=about`               | About / Contact   |
| `?page=favorites`           | Saved Vehicles    |
| `?page=dashboard`           | Customer Dashboard|
| `?page=admin`               | Admin CRM         |

---

## Design System

All CSS lives in `components/styles.py` (`get_css()`).
Key CSS variables:

```css
--black:   #0A0A0B   /* page background      */
--charcoal:#1A1A1F   /* sections, panels      */
--dark:    #22222A   /* inputs, card hover    */
--accent:  #C8A84B   /* gold — primary accent */
--card-bg: #1E1E26   /* vehicle & KPI cards   */
```

Button variants are applied via wrapper `<div>` classes:
- `.btn-ghost-wrap` — ghost/secondary buttons
- `.btn-danger-wrap` — destructive actions

---

## Database Schema

```
users         — id, name, email, phone, password (SHA-256), role
vehicles      — id, brand, model, variant, year, price, fuel, transmission,
                body_type, engine, power, torque, mileage, km_driven, color,
                status, featured, description, image_url, stock
favourites    — user_id → vehicle_id (unique pair)
test_drives   — vehicle_id, name, phone, email, drive_date, time_slot, status
enquiries     — vehicle_id, type, name, phone, email, message, financing, status
```

---

## BTech Viva Notes

1. **Architecture** — Single-file entry (`app.py`) routes via query params.
   Each page is a separate module. Components and DB are fully decoupled.

2. **Database** — SQLite with `PRAGMA foreign_keys=ON` and `WAL` journal mode.
   All queries use parameterised statements (no SQL injection risk).

3. **Auth** — SHA-256 hashing stored in `users.password`. Sessions via
   `st.session_state`. No plain-text passwords anywhere.

4. **CSS isolation** — All 500+ lines of CSS are in one `get_css()` function,
   injected once at startup. Streamlit's default theme is overridden completely.

5. **Responsive** — `@media (max-width:768px)` breakpoints stack columns and
   adjust padding across all sections.

---

*© 2026 AutoElite. Built as a BTech final-year project.*
