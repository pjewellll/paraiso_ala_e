from __future__ import annotations

import os
import re
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import psycopg
from psycopg.rows import dict_row
from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - python-dotenv is installed in requirements.txt
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env")


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _int_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


# Supabase uses PostgreSQL. Set DATABASE_URL in Render using the Supabase connection string.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# Optional fallback variables for local PostgreSQL development.
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = _int_env("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")

# PostgreSQL hosting platforms such as Supabase already provide the database,
# so database creation should normally stay disabled.
DB_CREATE_IF_MISSING = _bool_env("DB_CREATE_IF_MISSING", False)
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = _int_env("PORT", _int_env("APP_PORT", 5000))
APP_DEBUG = _bool_env("APP_DEBUG", _bool_env("FLASK_DEBUG", False))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")


ROOM_RATES = {
    "Open Cottage": 2000,
    "Kubo": 2500,
    "Villa Room": 8000,
    "Modern Kubo": 9000,
    "Family Room": 5000,
    "Cottage": 2000,
    "Gazebo": 1800,
    "Poolside Cabana": 2000,
    "Tent Pitching": 300,
    "Table Rental": 500,
    "Karaoke Rental": 1000,
}

ENTRANCE_FEE_PER_GUEST = 200
DOWN_PAYMENT_RATE = 0.50

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def _normalize_database_url(database_url: str) -> str:
    """Return a psycopg-compatible PostgreSQL URL.

    Supabase sometimes displays URLs as postgres://. psycopg accepts
    postgresql://. We also add sslmode=require for hosted databases when the
    URL does not already include an sslmode parameter.
    """
    if database_url.startswith("postgres://"):
        database_url = "postgresql://" + database_url[len("postgres://"):]

    parsed_url = urlparse(database_url)
    query_items = parse_qsl(parsed_url.query, keep_blank_values=True)
    query_keys = {key.lower() for key, _ in query_items}

    is_local_host = parsed_url.hostname in {"localhost", "127.0.0.1", "::1"}
    if "sslmode" not in query_keys and not is_local_host:
        query_items.append(("sslmode", DB_SSLMODE))
        parsed_url = parsed_url._replace(query=urlencode(query_items))
        database_url = urlunparse(parsed_url)

    return database_url


def get_postgres_connection_info() -> dict[str, Any]:
    connect_timeout = _int_env("DB_CONNECTION_TIMEOUT", 10)

    if DATABASE_URL:
        return {
            "conninfo": _normalize_database_url(DATABASE_URL),
            "connect_timeout": connect_timeout,
        }

    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "dbname": DB_NAME,
        "sslmode": DB_SSLMODE,
        "connect_timeout": connect_timeout,
    }


class PostgresDatabase:
    def __init__(self) -> None:
        self.connection = psycopg.connect(
            **get_postgres_connection_info(),
            row_factory=dict_row,
        )
        self.cursor = self.connection.cursor()

    def execute(self, query: str, params: tuple | list = ()):  # Flask app uses ? placeholders.
        self.cursor.execute(query.replace("?", "%s"), params or ())
        return self.cursor

    def executemany(self, query: str, params: list[tuple]):
        self.cursor.executemany(query.replace("?", "%s"), params)
        return self.cursor

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        try:
            self.cursor.close()
        finally:
            self.connection.close()


def create_database_if_missing() -> None:
    # Supabase/PostgreSQL providers create the database for you. The app only
    # creates tables inside the existing database.
    return


def get_db() -> PostgresDatabase:
    if "db" not in g:
        g.db = PostgresDatabase()
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()


def _safe_identifier(name: str) -> str:
    if not name.replace("_", "").isalnum():
        raise ValueError(f"Unsafe database identifier: {name}")
    return f'"{name}"'


def column_exists(db: PostgresDatabase, table_name: str, column_name: str) -> bool:
    cursor = db.execute(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = ?
          AND column_name = ?
        LIMIT 1
        """,
        (table_name, column_name),
    )
    return cursor.fetchone() is not None


def add_column_if_missing(
    db: PostgresDatabase,
    table_name: str,
    column_name: str,
    column_type: str,
) -> None:
    if not column_exists(db, table_name, column_name):
        db.execute(
            f"ALTER TABLE {_safe_identifier(table_name)} "
            f"ADD COLUMN {_safe_identifier(column_name)} {column_type}"
        )


def execute_sql_script(db: PostgresDatabase, schema_path: Path) -> None:
    sql_text = schema_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql_text.split(";") if statement.strip()]

    for statement in statements:
        db.execute(statement)


def init_db() -> None:
    try:
        create_database_if_missing()
        db = PostgresDatabase()
    except psycopg.Error as err:
        raise RuntimeError(
            "PostgreSQL/Supabase connection failed. Check DATABASE_URL, DB_SSLMODE, and your Supabase database password."
        ) from err

    schema_path = BASE_DIR / "database" / "schema.sql"

    if schema_path.exists():
        execute_sql_script(db, schema_path)
    else:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                room_name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                capacity INT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(150) NOT NULL,
                email VARCHAR(150) NOT NULL,
                phone VARCHAR(30) NOT NULL,
                checkin_date DATE NOT NULL,
                checkout_date DATE NOT NULL,
                room_type VARCHAR(100) NOT NULL,
                guests INT NOT NULL,
                notes TEXT,
                status VARCHAR(30) NOT NULL DEFAULT 'Pending',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                email VARCHAR(150) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    admin = db.execute(
        "SELECT id FROM admins WHERE username = ?",
        ("admin",),
    ).fetchone()

    if admin is None:
        db.execute(
            "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("admin123")),
        )

    room_count = db.execute("SELECT COUNT(*) AS count FROM rooms").fetchone()["count"]

    if room_count == 0:
        rooms = [
            ("Open Cottage", "Good for day tour and group shelter.", 2000.00, 10),
            ("Kubo", "Traditional Filipino-style cottage.", 2500.00, 10),
            ("Villa Room", "Spacious room for family and group stays.", 8000.00, 10),
            ("Modern Kubo", "Modern kubo with aircon and comfort room.", 9000.00, 16),
        ]

        db.executemany(
            """
            INSERT INTO rooms (room_name, description, price, capacity)
            VALUES (?, ?, ?, ?)
            """,
            rooms,
        )

    extra_rooms = [
        (
            "Gazebo",
            "Open shaded gazebo ideal for family gatherings, dining, and relaxing by the resort.",
            1800.00,
            8,
        ),
        (
            "Poolside Cabana",
            "A relaxing shaded cabana near the pool, perfect for families and small groups.",
            2000.00,
            6,
        ),
        (
            "Tent Pitching",
            "Designated camping space for guests who want an outdoor overnight experience.",
            300.00,
            6,
        ),
        (
            "Table Rental",
            "Rental table option for picnics, dining, birthdays, and small group activities.",
            500.00,
            1,
        ),
        (
            "Karaoke Rental",
            "Karaoke setup rental for entertainment, celebrations, and group bonding.",
            1000.00,
            1,
        ),
    ]

    for room_name, description, price, capacity in extra_rooms:
        existing_room = db.execute(
            "SELECT id FROM rooms WHERE room_name = ?",
            (room_name,),
        ).fetchone()

        if existing_room is None:
            db.execute(
                """
                INSERT INTO rooms (room_name, description, price, capacity)
                VALUES (?, ?, ?, ?)
                """,
                (room_name, description, price, capacity),
            )
        else:
            db.execute(
                """
                UPDATE rooms
                SET description = ?, price = ?, capacity = ?
                WHERE room_name = ?
                """,
                (description, price, capacity, room_name),
            )

    add_column_if_missing(db, "bookings", "guest_name", "VARCHAR(150)")
    add_column_if_missing(db, "bookings", "contact_number", "VARCHAR(30)")
    add_column_if_missing(db, "bookings", "special_requests", "TEXT")
    add_column_if_missing(db, "bookings", "payment_method", "VARCHAR(50)")
    add_column_if_missing(db, "bookings", "nights", "INT DEFAULT 0")
    add_column_if_missing(db, "bookings", "room_rate", "DECIMAL(10,2) DEFAULT 0")
    add_column_if_missing(db, "bookings", "accommodation_total", "DECIMAL(10,2) DEFAULT 0")
    add_column_if_missing(db, "bookings", "entrance_total", "DECIMAL(10,2) DEFAULT 0")
    add_column_if_missing(db, "bookings", "total_amount", "DECIMAL(10,2) DEFAULT 0")
    add_column_if_missing(db, "bookings", "down_payment", "DECIMAL(10,2) DEFAULT 0")
    add_column_if_missing(db, "bookings", "remaining_balance", "DECIMAL(10,2) DEFAULT 0")

    db.commit()
    db.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "admin_id" not in session:
            return redirect(url_for("admin_login"))

        return view(**kwargs)

    return wrapped_view


def user_login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Please login first before booking.", "error")
            return redirect(url_for("login", next=request.path))

        return view(**kwargs)

    return wrapped_view


def get_room_rate(room_type: str) -> float:
    db = get_db()

    room = db.execute(
        "SELECT price FROM rooms WHERE room_name = ?",
        (room_type,),
    ).fetchone()

    if room:
        return float(room["price"])

    return float(ROOM_RATES.get(room_type, 0))


def can_modify_booking(booking) -> bool:
    if booking is None or not booking["created_at"]:
        return False

    created_at_value = booking["created_at"]

    if isinstance(created_at_value, datetime):
        created_at = created_at_value
    else:
        created_at_text = str(created_at_value)
        try:
            created_at = datetime.strptime(created_at_text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            created_at = datetime.fromisoformat(created_at_text)

    time_limit = created_at + timedelta(hours=24)
    return datetime.now() <= time_limit


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/rooms")
def rooms():
    db = get_db()
    rooms_data = db.execute(
        """
        SELECT * FROM rooms
        ORDER BY
            CASE room_name
                WHEN 'Gazebo' THEN 1
                WHEN 'Poolside Cabana' THEN 2
                WHEN 'Open Cottage' THEN 3
                WHEN 'Kubo' THEN 4
                WHEN 'Villa Room' THEN 5
                WHEN 'Modern Kubo' THEN 6
                WHEN 'Table Rental' THEN 7
                WHEN 'Tent Pitching' THEN 8
                WHEN 'Karaoke Rental' THEN 9
                ELSE 10
            END,
            room_name ASC
        """
    ).fetchall()

    return render_template("rooms.html", rooms=rooms_data)


@app.route("/booking", methods=["GET", "POST"])
@user_login_required
def booking():
    db = get_db()
    rooms_data = db.execute("SELECT * FROM rooms ORDER BY room_name ASC").fetchall()

    if request.method == "POST":
        form = request.form

        guest_name = form.get("guest_name", "").strip()
        email = form.get("email", "").strip()
        contact_number = form.get("contact_number", "").strip()
        room_type = form.get("room_type", "").strip()
        checkin_date = form.get("checkin_date", "").strip()
        checkout_date = form.get("checkout_date", "").strip()
        guests = int(form.get("guests", 1))
        special_requests = form.get("special_requests", "").strip()
        payment_method = form.get("payment_method", "").strip()

        if not guest_name or not email or not contact_number or not room_type:
            flash("Please complete all required fields.", "error")
            return redirect(url_for("booking"))

        try:
            checkin = datetime.strptime(checkin_date, "%Y-%m-%d")
            checkout = datetime.strptime(checkout_date, "%Y-%m-%d")
        except ValueError:
            flash("Please select valid check-in and check-out dates.", "error")
            return redirect(url_for("booking"))

        nights = (checkout - checkin).days

        if nights <= 0:
            flash("Check-out date must be after check-in date.", "error")
            return redirect(url_for("booking"))

        room_rate = get_room_rate(room_type)

        accommodation_total = room_rate * nights
        entrance_total = guests * ENTRANCE_FEE_PER_GUEST
        total_amount = accommodation_total + entrance_total
        down_payment = total_amount * DOWN_PAYMENT_RATE
        remaining_balance = total_amount - down_payment

        cursor = db.execute(
            """
            INSERT INTO bookings (
                fullname,
                email,
                phone,
                checkin_date,
                checkout_date,
                room_type,
                guests,
                notes,
                status,
                guest_name,
                contact_number,
                special_requests,
                payment_method,
                nights,
                room_rate,
                accommodation_total,
                entrance_total,
                total_amount,
                down_payment,
                remaining_balance
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            """,
            (
                guest_name,
                email,
                contact_number,
                checkin_date,
                checkout_date,
                room_type,
                guests,
                special_requests,
                "Pending",
                guest_name,
                contact_number,
                special_requests,
                payment_method,
                nights,
                room_rate,
                accommodation_total,
                entrance_total,
                total_amount,
                down_payment,
                remaining_balance,
            ),
        )

        booking_id = cursor.fetchone()["id"]
        db.commit()

        session["last_booking_id"] = booking_id
        flash("Booking submitted successfully.", "success")
        return redirect(url_for("booking_summary", booking_id=booking_id))

    return render_template("booking.html", rooms=rooms_data)


@app.route("/booking-summary/<int:booking_id>")
def booking_summary(booking_id: int):
    db = get_db()

    booking_data = db.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,),
    ).fetchone()

    if booking_data is None:
        flash("Booking not found.", "error")
        return redirect(url_for("home"))

    can_modify = can_modify_booking(booking_data)

    session["last_booking_id"] = booking_id

    return render_template(
        "booking_summary.html",
        booking=booking_data,
        can_modify=can_modify,
    )


@app.route("/booking-edit/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id: int):
    db = get_db()

    booking_data = db.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,),
    ).fetchone()

    if booking_data is None:
        flash("Booking not found.", "error")
        return redirect(url_for("home"))

    if not can_modify_booking(booking_data):
        flash("This booking can no longer be edited because it is over 24 hours old.", "error")
        return redirect(url_for("booking_summary", booking_id=booking_id))

    rooms_data = db.execute("SELECT * FROM rooms ORDER BY room_name ASC").fetchall()

    if request.method == "POST":
        form = request.form

        guest_name = form.get("guest_name", "").strip()
        email = form.get("email", "").strip()
        contact_number = form.get("contact_number", "").strip()
        room_type = form.get("room_type", "").strip()
        checkin_date = form.get("checkin_date", "").strip()
        checkout_date = form.get("checkout_date", "").strip()
        guests = int(form.get("guests", 1))
        special_requests = form.get("special_requests", "").strip()
        payment_method = form.get("payment_method", "").strip()

        if not guest_name or not email or not contact_number or not room_type:
            flash("Please complete all required fields.", "error")
            return redirect(url_for("edit_booking", booking_id=booking_id))

        try:
            checkin = datetime.strptime(checkin_date, "%Y-%m-%d")
            checkout = datetime.strptime(checkout_date, "%Y-%m-%d")
        except ValueError:
            flash("Please select valid check-in and check-out dates.", "error")
            return redirect(url_for("edit_booking", booking_id=booking_id))

        nights = (checkout - checkin).days

        if nights <= 0:
            flash("Check-out date must be after check-in date.", "error")
            return redirect(url_for("edit_booking", booking_id=booking_id))

        room_rate = get_room_rate(room_type)

        accommodation_total = room_rate * nights
        entrance_total = guests * ENTRANCE_FEE_PER_GUEST
        total_amount = accommodation_total + entrance_total
        down_payment = total_amount * DOWN_PAYMENT_RATE
        remaining_balance = total_amount - down_payment

        db.execute(
            """
            UPDATE bookings
            SET
                fullname = ?,
                email = ?,
                phone = ?,
                checkin_date = ?,
                checkout_date = ?,
                room_type = ?,
                guests = ?,
                notes = ?,
                guest_name = ?,
                contact_number = ?,
                special_requests = ?,
                payment_method = ?,
                nights = ?,
                room_rate = ?,
                accommodation_total = ?,
                entrance_total = ?,
                total_amount = ?,
                down_payment = ?,
                remaining_balance = ?
            WHERE id = ?
            """,
            (
                guest_name,
                email,
                contact_number,
                checkin_date,
                checkout_date,
                room_type,
                guests,
                special_requests,
                guest_name,
                contact_number,
                special_requests,
                payment_method,
                nights,
                room_rate,
                accommodation_total,
                entrance_total,
                total_amount,
                down_payment,
                remaining_balance,
                booking_id,
            ),
        )

        db.commit()

        flash("Booking updated successfully.", "success")
        return redirect(url_for("booking_summary", booking_id=booking_id))

    return render_template(
        "edit_booking.html",
        booking=booking_data,
        rooms=rooms_data,
    )


@app.route("/booking-delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id: int):
    db = get_db()

    booking_data = db.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,),
    ).fetchone()

    if booking_data is None:
        flash("Booking not found.", "error")
        return redirect(url_for("home"))

    if not can_modify_booking(booking_data):
        flash("This booking can no longer be deleted because it is over 24 hours old.", "error")
        return redirect(url_for("booking_summary", booking_id=booking_id))

    db.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,),
    )

    db.commit()

    session.pop("last_booking_id", None)

    flash("Booking deleted successfully.", "success")
    return redirect(url_for("booking"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form = request.form
        db = get_db()

        db.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (
                form["name"].strip(),
                form["email"].strip(),
                form["message"].strip(),
            ),
        )

        db.commit()

        flash("Your message has been sent.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        db = get_db()

        admin = db.execute(
            "SELECT * FROM admins WHERE username = ?",
            (username,),
        ).fetchone()

        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]

            flash("Welcome back, admin.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    db = get_db()

    total_bookings = db.execute(
        "SELECT COUNT(*) AS count FROM bookings"
    ).fetchone()["count"]

    pending_bookings = db.execute(
        "SELECT COUNT(*) AS count FROM bookings WHERE status = 'Pending'"
    ).fetchone()["count"]

    confirmed_bookings = db.execute(
        "SELECT COUNT(*) AS count FROM bookings WHERE status = 'Confirmed'"
    ).fetchone()["count"]

    cancelled_bookings = db.execute(
        "SELECT COUNT(*) AS count FROM bookings WHERE status = 'Cancelled'"
    ).fetchone()["count"]

    total_contacts = db.execute(
        "SELECT COUNT(*) AS count FROM contacts"
    ).fetchone()["count"]

    bookings = db.execute(
        "SELECT * FROM bookings ORDER BY created_at DESC, id DESC LIMIT 50"
    ).fetchall()

    contacts = db.execute(
        "SELECT * FROM contacts ORDER BY created_at DESC, id DESC LIMIT 10"
    ).fetchall()

    stats = {
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_contacts": total_contacts,
    }

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        bookings=bookings,
        contacts=contacts,
    )


@app.route("/admin/update-booking/<int:booking_id>", methods=["POST"])
@login_required
def update_booking_status(booking_id: int):
    new_status = request.form["status"]

    if new_status not in {"Pending", "Confirmed", "Cancelled"}:
        flash("Invalid status selected.", "error")
        return redirect(url_for("admin_dashboard"))

    db = get_db()

    db.execute(
        "UPDATE bookings SET status = ? WHERE id = ?",
        (new_status, booking_id),
    )

    db.commit()

    flash("Booking status updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/cancel-booking/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id: int):
    db = get_db()

    booking_data = db.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,),
    ).fetchone()

    if booking_data is None:
        flash("Booking not found.", "error")
        return redirect(url_for("admin_dashboard"))

    if booking_data["status"] == "Cancelled":
        flash("Booking is already cancelled.", "error")
        return redirect(url_for("admin_dashboard"))

    db.execute(
        "UPDATE bookings SET status = 'Cancelled' WHERE id = ?",
        (booking_id,),
    )

    db.commit()

    flash("Booking cancelled successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/send-reply", methods=["POST"])
@login_required
def send_reply():
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not email or not subject or not message:
        flash("Please complete all reply fields.", "error")
        return redirect(url_for("admin_dashboard") + "#messages")

    flash(f"Reply prepared for {email}. Subject: {subject}", "success")

    return redirect(url_for("admin_dashboard") + "#messages")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/booked-dates")
def booked_dates():
    db = get_db()

    rows = db.execute(
        """
        SELECT checkin_date
        FROM bookings
        WHERE status != 'Cancelled'
        """
    ).fetchall()

    dates = [
        row["checkin_date"].isoformat() if hasattr(row["checkin_date"], "isoformat") else str(row["checkin_date"])
        for row in rows
    ]

    return {
        "booked_dates": dates
    }

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json() or {}

    message = (data.get("message") or "").lower().strip()
    language = data.get("language", "en")

    is_tagalog = language == "tl"

    if not message:
        reply = (
            "Pakilagay ang iyong tanong tungkol sa resort, booking, kuwarto, presyo, o serbisyo."
            if is_tagalog
            else "Please enter your question about the resort, booking, rooms, prices, or services."
        )
        return jsonify({"reply": reply})

    if any(word in message for word in ["room", "rooms", "kuwarto", "kwarto", "tuluyan", "villa", "kubo"]):
        reply = (
            "Mayroon kaming mga tuluyan tulad ng Gazebo, Kubo, Open Cottage, Villa Room, Modern Kubo, at Poolside Cabana. Maaari mong tingnan ang Mga Kuwarto page para sa kapasidad at presyo."
            if is_tagalog
            else "We have stay options such as Gazebo, Kubo, Open Cottage, Villa Room, Modern Kubo, and Poolside Cabana. You can check the Rooms page for capacity and prices."
        )

    elif any(word in message for word in ["book", "booking", "reserve", "reservation", "mag-book", "magbook", "pareserba"]):
        reply = (
            "Para mag-book, pindutin ang Mag-book Ngayon, punan ang guest details, piliin ang kuwarto o serbisyo, check-in at check-out date, mode of payment, at isumite ang booking."
            if is_tagalog
            else "To book, click Book Now, fill out your guest details, choose your room or service, select check-in and check-out dates, payment method, and submit your booking."
        )

    elif any(word in message for word in ["price", "presyo", "rate", "bayad", "payment", "downpayment", "fee"]):
        reply = (
            "Makikita ang presyo sa bawat kuwarto o serbisyo sa Rooms page. Sa booking form, automatic na lalabas ang estimated total, entrance fee, required down payment, at remaining balance."
            if is_tagalog
            else "Prices are shown for each room or service on the Rooms page. In the booking form, the estimated total, entrance fee, required down payment, and remaining balance are computed automatically."
        )

    elif any(word in message for word in ["location", "address", "direksyon", "saan", "where", "calatagan"]):
        reply = (
            "Ang Paraiso Ala Eh Garden Resort ay nasa Calatagan, Batangas. Maaari mong buksan ang Contact page para sa location details at directions."
            if is_tagalog
            else "Paraiso Ala Eh Garden Resort is located in Calatagan, Batangas. You may open the Contact page for location details and directions."
        )

    elif any(word in message for word in ["contact", "message", "email", "phone", "number", "tawag", "mensahe"]):
        reply = (
            "Maaari kang makipag-ugnayan gamit ang Contact page. Doon ka puwedeng magpadala ng mensahe o tingnan ang contact details ng resort."
            if is_tagalog
            else "You can contact the resort through the Contact page. You can send a message there or check the resort contact details."
        )

    elif any(word in message for word in ["service", "rental", "rent", "table", "tent", "karaoke", "videoke", "serbisyo"]):
        reply = (
            "Mayroon ding pinaparentang serbisyo tulad ng Table Rental, Tent Pitching, at Videoke/Karaoke Rental para sa activities, celebration, at bonding."
            if is_tagalog
            else "We also offer rental services such as Table Rental, Tent Pitching, and Karaoke/Videoke Rental for activities, celebrations, and bonding."
        )

    elif any(word in message for word in ["check in", "check-in", "checkout", "check out", "date", "petsa"]):
        reply = (
            "Sa booking form, pumili ng check-in date at check-out date. Hindi dapat mas maaga o kapareho ng check-in date ang check-out date."
            if is_tagalog
            else "In the booking form, select your check-in and check-out dates. The check-out date should not be earlier than or the same as the check-in date."
        )

    else:
        reply = (
            "Pasensya na, hindi ko pa sigurado ang sagot diyan. Maaari kang magtanong tungkol sa kuwarto, booking, presyo, rental services, location, o contact details."
            if is_tagalog
            else "Sorry, I am not sure about that yet. You can ask me about rooms, booking, prices, rental services, location, or contact details."
        )

    return jsonify({"reply": reply})


@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next") or request.form.get("next") or url_for("home")

    if not next_page.startswith("/"):
        next_page = url_for("home")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if re.fullmatch(EMAIL_PATTERN, email):
            session.clear()
            session["user_id"] = email
            session["user_email"] = email
            session["user_name"] = email.split("@", 1)[0]

            flash("Login successful!", "success")
            return redirect(next_page)

        flash("Please enter a valid email address.", "error")

    return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    if _bool_env("AUTO_INIT_DB", True):
        init_db()
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)