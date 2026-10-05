"""
AutoElite — Database Layer
SQLite-backed persistence for vehicles, users, bookings, enquiries, favourites.
All functions return plain dicts / lists of dicts so pages stay decoupled from SQL.
"""

import sqlite3
import streamlit as st
import hashlib
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "autoelite.db")
_DB_INITIALIZED = False


# ── Connection helper ─────────────────────────────────────────────────────────
def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ── Schema ────────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    email       TEXT    UNIQUE NOT NULL,
    phone       TEXT,
    password    TEXT    NOT NULL,
    role        TEXT    NOT NULL DEFAULT 'customer',   -- 'customer' | 'admin'
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS vehicles (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    brand        TEXT    NOT NULL,
    model        TEXT    NOT NULL,
    variant      TEXT    NOT NULL,
    year         INTEGER NOT NULL,
    price        INTEGER NOT NULL,
    fuel         TEXT    NOT NULL,
    transmission TEXT    NOT NULL,
    body_type    TEXT    NOT NULL,
    engine       TEXT,
    power        TEXT,
    torque       TEXT,
    mileage      REAL,
    km_driven    INTEGER DEFAULT 0,
    color        TEXT,
    status       TEXT    NOT NULL DEFAULT 'Available',  -- Available|Reserved|Sold|Coming Soon
    featured     INTEGER NOT NULL DEFAULT 0,
    description  TEXT,
    image_url    TEXT,
    stock        INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS favourites (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, vehicle_id)
);

CREATE TABLE IF NOT EXISTS test_drives (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    name       TEXT NOT NULL,
    phone      TEXT NOT NULL,
    email      TEXT,
    drive_date TEXT NOT NULL,
    time_slot  TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'Pending',   -- Pending|Confirmed|Cancelled|Completed
    notes      TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS enquiries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE SET NULL,
    type       TEXT NOT NULL,   -- Quote|Financing|TradeIn|General
    name       TEXT NOT NULL,
    email      TEXT,
    phone      TEXT NOT NULL,
    message    TEXT,
    financing  TEXT,
    status     TEXT NOT NULL DEFAULT 'New',   -- New|InProgress|Resolved|Closed
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_vehicles_status  ON vehicles(status);
CREATE INDEX IF NOT EXISTS idx_vehicles_brand   ON vehicles(brand);
CREATE INDEX IF NOT EXISTS idx_vehicles_featured ON vehicles(featured);
CREATE INDEX IF NOT EXISTS idx_favs_user        ON favourites(user_id);
CREATE INDEX IF NOT EXISTS idx_td_user          ON test_drives(user_id);
CREATE INDEX IF NOT EXISTS idx_enq_user         ON enquiries(user_id);
"""


# ── Seed data ─────────────────────────────────────────────────────────────────
SEED_VEHICLES = [
    ("BMW", "3 Series", "330i M Sport", 2025, 5200000, "Petrol", "Automatic", "Sedan",
     "2.0L Turbo", "258 HP", "400 Nm", 15.3, 12000, "Alpine White", "Available", 1,
     "The benchmark sports sedan, now sharper than ever with M Sport aerodynamics and a turbocharged heart.",
     "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80"),

    ("Mercedes-Benz", "C-Class", "C 220d AMG Line", 2025, 5800000, "Diesel", "Automatic", "Sedan",
     "2.0L CDI", "194 HP", "440 Nm", 18.2, 8000, "Obsidian Black", "Available", 1,
     "Exquisite engineering meets timeless elegance in the new C-Class AMG Line.",
     "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80"),

    ("Audi", "Q5", "40 TDI quattro", 2025, 6700000, "Diesel", "Automatic", "SUV",
     "2.0L TDI", "204 HP", "400 Nm", 14.8, 5000, "Daytona Gray", "Available", 1,
     "Quattro all-wheel drive meets refined SUV luxury. The Q5 sets the standard in its class.",
     "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80"),

    ("Porsche", "Cayenne", "S Coupe", 2024, 13500000, "Petrol", "Automatic", "SUV",
     "2.9L Biturbo V6", "440 HP", "550 Nm", 11.2, 18000, "Carrara White", "Available", 0,
     "Where sports car thrills meet SUV versatility. The Cayenne S Coupe defies categories.",
     "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800&q=80"),

    ("Tesla", "Model S", "Long Range AWD", 2025, 9800000, "Electric", "Automatic", "Sedan",
     "Dual Motor", "670 HP", "1050 Nm", None, 2000, "Midnight Silver", "Available", 0,
     "Zero emissions. Zero compromises. The Model S Long Range redefines what a sedan can be.",
     "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80"),

    ("Land Rover", "Range Rover", "Autobiography", 2025, 21000000, "Hybrid", "Automatic", "SUV",
     "3.0L MHEV", "400 HP", "550 Nm", 13.5, 3000, "Santorini Black", "Reserved", 0,
     "The definitive luxury SUV, perfected over five decades of continuous refinement.",
     "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800&q=80"),

    ("BMW", "X5", "xDrive40i", 2025, 8700000, "Petrol", "Automatic", "SUV",
     "3.0L Inline-6", "340 HP", "450 Nm", 12.8, 9500, "Mineral White", "Available", 0,
     "Power and poise in perfect proportion. The X5 xDrive40i commands every road.",
     "https://images.unsplash.com/photo-1543465077-db45d34b88a5?w=800&q=80"),

    ("Volvo", "XC90", "Ultimate B6 AWD", 2025, 9900000, "Hybrid", "Automatic", "SUV",
     "2.0L Mild Hybrid", "300 HP", "420 Nm", 16.4, 4500, "Crystal White", "Coming Soon", 0,
     "Scandinavian safety philosophy and award-winning design, elevated to its ultimate expression.",
     "https://images.unsplash.com/photo-1612544070802-cd6a1ac38b20?w=800&q=80"),

    ("Audi", "A6", "45 TFSI quattro", 2024, 6400000, "Petrol", "Automatic", "Sedan",
     "2.0L TFSI", "245 HP", "370 Nm", 14.1, 14000, "Floret Silver", "Available", 0,
     "The executive sedan that never stops surprising. Sport and comfort, perfectly balanced.",
     "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=800&q=80"),

    ("Mercedes-Benz", "GLE", "400d 4MATIC", 2025, 10500000, "Diesel", "Automatic", "SUV",
     "3.0L CDI V6", "330 HP", "700 Nm", 13.8, 7000, "Selenite Grey", "Available", 0,
     "Commanding presence. Effortless performance. The GLE 400d is built for those who lead.",
     "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=800&q=80"),

    ("Jaguar", "F-Pace", "P400 R-Dynamic HSE", 2024, 8900000, "Petrol", "Automatic", "SUV",
     "3.0L Supercharged", "400 HP", "550 Nm", 11.8, 11000, "Fuji White", "Available", 0,
     "British performance DNA in a sports utility form. The F-Pace R-Dynamic is unmistakably Jaguar.",
     "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80"),

    ("Lexus", "LC 500", "Sport+", 2025, 15200000, "Petrol", "Automatic", "Coupe",
     "5.0L V8", "471 HP", "540 Nm", 10.5, 1500, "Sonic Titanium", "Available", 1,
     "A grand touring coupe that elevates every journey. The LC 500 is art in motion.",
     "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80"),
]

SEED_USERS = [
    ("Admin User", "admin@autoelite.in",  "+91 98765 00001",
     hashlib.sha256("admin123".encode()).hexdigest(), "admin"),
    ("Arjun Mehta",  "arjun@example.com", "+91 98765 43210",
     hashlib.sha256("password123".encode()).hexdigest(), "customer"),
    ("Priya Sharma", "priya@example.com", "+91 91234 56789",
     hashlib.sha256("password123".encode()).hexdigest(), "customer"),
]


def init_db() -> None:
    """Create schema and seed data once per Streamlit process."""
    global _DB_INITIALIZED
    if _DB_INITIALIZED:
        return
    with _get_conn() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(SCHEMA)
        # Seed vehicles only if table is empty
        if conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO vehicles
                   (brand,model,variant,year,price,fuel,transmission,body_type,
                    engine,power,torque,mileage,km_driven,color,status,featured,
                    description,image_url)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                SEED_VEHICLES,
            )
        # Seed users only if table is empty
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO users (name,email,phone,password,role)
                   VALUES (?,?,?,?,?)""",
                SEED_USERS,
            )
        conn.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────
    _DB_INITIALIZED = True

def _row_to_dict(row) -> dict:
    return dict(row) if row else {}


def _rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _fmt_price(price: int) -> str:
    if price >= 10_000_000:
        return f"₹{price/10_000_000:.2f} Cr"
    if price >= 100_000:
        return f"₹{price/100_000:.1f}L"
    return f"₹{price:,}"


# ── Vehicle CRUD ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def get_all_vehicles(status_filter: str = "",
                     brand_filter: str = "",
                     fuel_filter: str = "",
                     body_filter: str = "",
                     sort: str = "default",
                     budget_max: int = 0,
                     search_term: str = "") -> list[dict]:
    sql = "SELECT * FROM vehicles WHERE 1=1"
    params: list = []
    if status_filter:
        sql += " AND status = ?"; params.append(status_filter)
    if brand_filter:
        sql += " AND brand = ?";  params.append(brand_filter)
    if fuel_filter:
        sql += " AND fuel = ?";   params.append(fuel_filter)
    if body_filter:
        sql += " AND body_type = ?"; params.append(body_filter)
    if budget_max:
        sql += " AND price <= ?"; params.append(budget_max)
    if search_term:
        term = f"%{search_term}%"
        sql += " AND (brand LIKE ? OR model LIKE ? OR variant LIKE ? OR description LIKE ?)"
        params.extend([term, term, term, term])

    order = {
        "price_asc":  "price ASC",
        "price_desc": "price DESC",
        "year_desc":  "year DESC",
        "default":    "featured DESC, id ASC",
    }.get(sort, "featured DESC, id ASC")
    sql += f" ORDER BY {order}"

    with _get_conn() as conn:
        return _rows_to_list(conn.execute(sql, params).fetchall())


def get_vehicle(vehicle_id: int) -> dict:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,)).fetchone()
        return _row_to_dict(row)


@st.cache_data(ttl=30, show_spinner=False)
def get_featured_vehicles(limit: int = 4) -> list[dict]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM vehicles WHERE featured=1 ORDER BY id LIMIT ?", (limit,)
        ).fetchall()
        return _rows_to_list(rows)


@st.cache_data(ttl=30, show_spinner=False)
def get_popular_vehicles(limit: int = 4) -> list[dict]:
    """Return non-featured vehicles as 'popular'."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM vehicles WHERE featured=0 AND status!='Sold' ORDER BY id LIMIT ?",
            (limit,),
        ).fetchall()
        return _rows_to_list(rows)


def add_vehicle(data: dict) -> int:
    sql = """INSERT INTO vehicles
             (brand,model,variant,year,price,fuel,transmission,body_type,
              engine,power,torque,mileage,km_driven,color,status,featured,
              description,image_url,stock)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    vals = (
        data["brand"], data["model"], data["variant"], data["year"],
        data["price"], data["fuel"], data["transmission"], data["body_type"],
        data.get("engine", "—"), data.get("power", "—"), data.get("torque", "—"),
        data.get("mileage"), data.get("km_driven", 0), data.get("color", "—"),
        data.get("status", "Available"), int(data.get("featured", False)),
        data.get("description", ""), data.get("image_url", ""),
        data.get("stock", 1),
    )
    with _get_conn() as conn:
        cur = conn.execute(sql, vals)
        conn.commit()
        result = cur.lastrowid
    _clear_vehicle_caches()
    return result


def update_vehicle(vehicle_id: int, data: dict) -> bool:
    fields = []
    vals = []
    allowed = ["brand","model","variant","year","price","fuel","transmission",
               "body_type","engine","power","torque","mileage","km_driven",
               "color","status","featured","description","image_url","stock"]
    for k, v in data.items():
        if k in allowed:
            fields.append(f"{k}=?")
            vals.append(v)
    if not fields:
        return False
    vals.append(vehicle_id)
    with _get_conn() as conn:
        conn.execute(f"UPDATE vehicles SET {','.join(fields)} WHERE id=?", vals)
        conn.commit()
    _clear_vehicle_caches()
    return True


def delete_vehicle(vehicle_id: int) -> bool:
    with _get_conn() as conn:
        conn.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
        conn.commit()
    _clear_vehicle_caches()
    return True


@st.cache_data(ttl=30, show_spinner=False)
def get_brands() -> list[str]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT brand FROM vehicles ORDER BY brand"
        ).fetchall()
        return [r["brand"] for r in rows]


@st.cache_data(ttl=30, show_spinner=False)
def get_body_types() -> list[str]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT body_type FROM vehicles ORDER BY body_type"
        ).fetchall()
        return [r["body_type"] for r in rows]


def _clear_vehicle_caches() -> None:
    for name in ("get_all_vehicles", "get_featured_vehicles", "get_popular_vehicles", "get_brands", "get_body_types"):
        fn = globals().get(name)
        if fn is not None and hasattr(fn, "clear"):
            try:
                fn.clear()
            except Exception:
                pass


def get_vehicle_count() -> int:
    with _get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]


# ── User / Auth ───────────────────────────────────────────────────────────────
def register_user(name: str, email: str, phone: str, password: str) -> tuple[bool, str]:
    try:
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO users (name,email,phone,password) VALUES (?,?,?,?)",
                (name, email.lower().strip(), phone, _hash(password)),
            )
            conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."


def login_user(email: str, password: str) -> Optional[dict]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email.lower().strip(), _hash(password)),
        ).fetchone()
        return _row_to_dict(row)


def get_user(user_id: int) -> dict:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return _row_to_dict(row)


def get_all_users() -> list[dict]:
    with _get_conn() as conn:
        return _rows_to_list(
            conn.execute("SELECT id,name,email,phone,role,created_at FROM users ORDER BY id").fetchall()
        )


def get_user_count() -> int:
    with _get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


# ── Favourites ────────────────────────────────────────────────────────────────
def toggle_favourite(user_id: int, vehicle_id: int) -> bool:
    """Returns True if now favourite, False if removed."""
    with _get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM favourites WHERE user_id=? AND vehicle_id=?",
            (user_id, vehicle_id),
        ).fetchone()
        if existing:
            conn.execute("DELETE FROM favourites WHERE user_id=? AND vehicle_id=?",
                         (user_id, vehicle_id))
            conn.commit()
            return False
        else:
            conn.execute("INSERT INTO favourites (user_id,vehicle_id) VALUES (?,?)",
                         (user_id, vehicle_id))
            conn.commit()
            return True


def get_favourites(user_id: int) -> list[dict]:
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT v.* FROM vehicles v
               JOIN favourites f ON f.vehicle_id = v.id
               WHERE f.user_id = ?
               ORDER BY f.created_at DESC""",
            (user_id,),
        ).fetchall()
        return _rows_to_list(rows)


def is_favourite(user_id: int, vehicle_id: int) -> bool:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM favourites WHERE user_id=? AND vehicle_id=?",
            (user_id, vehicle_id),
        ).fetchone()
        return row is not None


def get_favourite_count(user_id: int) -> int:
    with _get_conn() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM favourites WHERE user_id=?", (user_id,)
        ).fetchone()[0]


# ── Test Drives ───────────────────────────────────────────────────────────────
def book_test_drive(data: dict) -> int:
    sql = """INSERT INTO test_drives
             (user_id,vehicle_id,name,phone,email,drive_date,time_slot,notes,status)
             VALUES (?,?,?,?,?,?,?,?,?)"""
    vals = (
        data.get("user_id"), data["vehicle_id"], data["name"],
        data["phone"], data.get("email", ""),
        data["drive_date"], data["time_slot"],
        data.get("notes", ""), "Confirmed",
    )
    with _get_conn() as conn:
        cur = conn.execute(sql, vals)
        conn.commit()
        return cur.lastrowid


def get_test_drives(user_id: int = 0) -> list[dict]:
    with _get_conn() as conn:
        if user_id:
            rows = conn.execute(
                """SELECT td.*, v.brand, v.model, v.variant
                   FROM test_drives td
                   JOIN vehicles v ON v.id = td.vehicle_id
                   WHERE td.user_id = ?
                   ORDER BY td.drive_date DESC""",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT td.*, v.brand, v.model, v.variant
                   FROM test_drives td
                   JOIN vehicles v ON v.id = td.vehicle_id
                   ORDER BY td.created_at DESC""",
            ).fetchall()
        return _rows_to_list(rows)


def get_test_drive_count(user_id: int = 0) -> int:
    with _get_conn() as conn:
        if user_id:
            return conn.execute(
                "SELECT COUNT(*) FROM test_drives WHERE user_id=?", (user_id,)
            ).fetchone()[0]
        return conn.execute("SELECT COUNT(*) FROM test_drives").fetchone()[0]


def update_test_drive_status(td_id: int, status: str) -> None:
    with _get_conn() as conn:
        conn.execute("UPDATE test_drives SET status=? WHERE id=?", (status, td_id))
        conn.commit()


# ── Enquiries ─────────────────────────────────────────────────────────────────
def create_enquiry(data: dict) -> int:
    sql = """INSERT INTO enquiries
             (user_id,vehicle_id,type,name,email,phone,message,financing,status)
             VALUES (?,?,?,?,?,?,?,?,?)"""
    vals = (
        data.get("user_id"), data.get("vehicle_id"), data["type"],
        data["name"], data.get("email", ""), data["phone"],
        data.get("message", ""), data.get("financing", ""),
        "New",
    )
    with _get_conn() as conn:
        cur = conn.execute(sql, vals)
        conn.commit()
        return cur.lastrowid


def get_enquiries(user_id: int = 0) -> list[dict]:
    with _get_conn() as conn:
        if user_id:
            rows = conn.execute(
                """SELECT e.*, v.brand, v.model
                   FROM enquiries e
                   LEFT JOIN vehicles v ON v.id = e.vehicle_id
                   WHERE e.user_id = ?
                   ORDER BY e.created_at DESC""",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT e.*, v.brand, v.model
                   FROM enquiries e
                   LEFT JOIN vehicles v ON v.id = e.vehicle_id
                   ORDER BY e.created_at DESC""",
            ).fetchall()
        return _rows_to_list(rows)


def get_enquiry_count(user_id: int = 0) -> int:
    with _get_conn() as conn:
        if user_id:
            return conn.execute(
                "SELECT COUNT(*) FROM enquiries WHERE user_id=?", (user_id,)
            ).fetchone()[0]
        return conn.execute("SELECT COUNT(*) FROM enquiries").fetchone()[0]


def update_enquiry_status(enq_id: int, status: str) -> None:
    with _get_conn() as conn:
        conn.execute("UPDATE enquiries SET status=? WHERE id=?", (status, enq_id))
        conn.commit()


# ── Analytics helpers (admin dashboard) ───────────────────────────────────────
def get_monthly_booking_counts() -> list[dict]:
    """Returns last 12 months of test-drive bookings for the chart."""
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT strftime('%Y-%m', drive_date) AS month, COUNT(*) AS cnt
               FROM test_drives
               GROUP BY month
               ORDER BY month DESC
               LIMIT 12"""
        ).fetchall()
        return _rows_to_list(rows)


def get_status_distribution() -> dict:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) AS cnt FROM vehicles GROUP BY status"
        ).fetchall()
        return {r["status"]: r["cnt"] for r in rows}


def get_revenue_estimate() -> int:
    """Rough revenue: sum of sold vehicle prices."""
    with _get_conn() as conn:
        result = conn.execute(
            "SELECT COALESCE(SUM(price),0) FROM vehicles WHERE status='Sold'"
        ).fetchone()[0]
        # Add a realistic base for the demo
        return result + 24_800_000
