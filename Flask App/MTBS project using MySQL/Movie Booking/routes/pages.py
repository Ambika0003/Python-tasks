from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from db import execute, query_all, query_one
from utils import theater_display_sql

pages_bp = Blueprint("pages", __name__)

_MIN_QUERY_LEN = 1


def _table_columns(table):
    backend = current_app.config.get("DB_BACKEND", "sqlite").lower()
    if backend == "sqlite":
        rows = query_all(f"PRAGMA table_info({table})")
        return {row["name"] for row in rows}
    rows = query_all(f"SHOW COLUMNS FROM `{table}`")
    return {row["Field"] for row in rows}


def _search_theaters(term):
    cols = _table_columns("theaters")
    if "screen_number" in cols and "mall_name" in cols and "city" in cols:
        return query_all(
            """
            SELECT id, screen_number, mall_name, city, name, location
            FROM theaters
            WHERE COALESCE(screen_number, '') LIKE %s
               OR COALESCE(mall_name, '') LIKE %s
               OR COALESCE(city, '') LIKE %s
               OR COALESCE(name, '') LIKE %s
               OR COALESCE(location, '') LIKE %s
            ORDER BY city, mall_name, screen_number
            LIMIT 24
            """,
            (term, term, term, term, term),
        )
    return query_all(
        """
        SELECT id, name, location
        FROM theaters
        WHERE COALESCE(name, '') LIKE %s OR COALESCE(location, '') LIKE %s
        ORDER BY name
        LIMIT 24
        """,
        (term, term),
    )


def _search_showtimes(term):
    tcols = _table_columns("theaters")
    has_modern_theaters = "screen_number" in tcols and "mall_name" in tcols
    theater_filters = "s.theater LIKE %s"
    params = [term]
    if has_modern_theaters:
        theater_filters += """
            OR COALESCE(t.screen_number, '') LIKE %s
            OR COALESCE(t.mall_name, '') LIKE %s
            OR COALESCE(t.city, '') LIKE %s
        """
        params.extend([term] * 3)
    if "name" in tcols:
        theater_filters += " OR COALESCE(t.name, '') LIKE %s"
        params.append(term)

    scols = _table_columns("showtimes")
    lang_filter = " OR s.language LIKE %s" if "language" in scols else ""
    lang_select = ", s.language" if "language" in scols else ""

    sql = f"""
        SELECT s.id, m.id AS movie_id, m.title AS movie_title, m.poster_url,
               {theater_display_sql()}, s.show_date, s.show_time,
               s.price_prime, s.price_gold, s.price_recliner{lang_select}
        FROM showtimes s
        JOIN movies m ON m.id = s.movie_id
        LEFT JOIN theaters t ON t.id = s.theater_id
        WHERE s.show_date >= CURDATE()
          AND (
            m.title LIKE %s
            OR m.genre LIKE %s
            OR {theater_filters}
            {lang_filter}
          )
        ORDER BY s.show_date, s.show_time
        LIMIT 36
    """
    all_params = [term, term] + params
    if lang_filter:
        all_params.append(term)
    rows = query_all(sql, tuple(all_params))
    if "language" not in scols:
        for row in rows:
            row.setdefault("language", "")
    return rows


def _search_term():
    return request.args.get("q", "").strip()


@pages_bp.route("/search")
def search():
    q = _search_term()
    movies = []
    theaters = []
    showtimes = []

    if len(q) >= _MIN_QUERY_LEN:
        term = f"%{q}%"
        movies = query_all(
            """
            SELECT id, title, poster_url, genre, rating, duration
            FROM movies
            WHERE title LIKE %s OR genre LIKE %s OR description LIKE %s
            ORDER BY title
            LIMIT 24
            """,
            (term, term, term),
        )
        theaters = _search_theaters(term)
        showtimes = _search_showtimes(term)

    return render_template(
        "search.html",
        q=q,
        movies=movies,
        theaters=theaters,
        showtimes=showtimes,
        has_results=bool(movies or theaters or showtimes),
    )


CONTACT_CATEGORIES = [
    ("general", "General enquiry"),
    ("booking", "Booking issue"),
    ("payment", "Payment / refund"),
    ("technical", "Technical problem"),
    ("other", "Other"),
]


@pages_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        subject = request.form.get("subject", "").strip()
        category = request.form.get("category", "general").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not subject or not message:
            flash("Please fill in all required fields.", "error")
        elif "@" not in email or len(email) < 5:
            flash("Please enter a valid email address.", "error")
        elif len(message) < 10:
            flash("Please describe your issue in at least 10 characters.", "error")
        else:
            valid_cats = {c[0] for c in CONTACT_CATEGORIES}
            if category not in valid_cats:
                category = "general"
            user_id = session.get("user_id")
            execute(
                """
                INSERT INTO contact_messages
                    (name, email, subject, category, message, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, email, subject, category, message, user_id),
            )
            flash(
                "Thank you! We received your message and will get back to you soon.",
                "success",
            )
            return redirect(url_for("pages.contact"))

    user_email = ""
    user_name = ""
    if session.get("user_id"):
        row = query_one(
            "SELECT username, email FROM users WHERE id = %s",
            (session["user_id"],),
        )
        if row:
            user_email = row.get("email", "")
            user_name = row.get("username", "")

    return render_template(
        "contact.html",
        categories=CONTACT_CATEGORIES,
        default_name=user_name,
        default_email=user_email,
    )
