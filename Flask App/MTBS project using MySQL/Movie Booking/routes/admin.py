from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import execute, query_all, query_one, table_columns
from routes.auth import admin_required
from utils import (
    AVAILABLE_LANGUAGES,
    MOVIE_CERTIFICATIONS,
    MOVIE_FORMATS,
    MOVIE_STATUSES,
    format_theater_label,
    theater_display_sql,
    theaters_list_sql,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _theater_options():
    return query_all(theaters_list_sql())


def _fetch_theater(theater_id):
    cols = table_columns("theaters")
    if "screen_number" in cols:
        return query_one(
            """
            SELECT id, screen_number, mall_name, city, name, location
            FROM theaters WHERE id = %s
            """,
            (theater_id,),
        )
    return query_one(
        """
        SELECT id, name, location,
               name AS screen_number, '' AS mall_name, location AS city
        FROM theaters WHERE id = %s
        """,
        (theater_id,),
    )


def _parse_theater_form():
    return {
        "screen_number": request.form.get("screen_number", "").strip(),
        "mall_name": request.form.get("mall_name", "").strip(),
        "city": request.form.get("city", "").strip(),
    }


def _theater_columns():
    return table_columns("theaters")


def _insert_theater(data):
    cols = _theater_columns()
    if "name" in cols:
        execute(
            """
            INSERT INTO theaters (screen_number, mall_name, city, name, location)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["screen_number"],
                data["mall_name"],
                data["city"],
                data["screen_number"],
                data["city"],
            ),
        )
    else:
        execute(
            """
            INSERT INTO theaters (screen_number, mall_name, city)
            VALUES (%s, %s, %s)
            """,
            (data["screen_number"], data["mall_name"], data["city"]),
        )


def _update_theater(theater_id, data):
    cols = _theater_columns()
    if "name" in cols:
        execute(
            """
            UPDATE theaters SET screen_number=%s, mall_name=%s, city=%s,
            name=%s, location=%s WHERE id=%s
            """,
            (
                data["screen_number"],
                data["mall_name"],
                data["city"],
                data["screen_number"],
                data["city"],
                theater_id,
            ),
        )
    else:
        execute(
            """
            UPDATE theaters SET screen_number=%s, mall_name=%s, city=%s
            WHERE id=%s
            """,
            (data["screen_number"], data["mall_name"], data["city"], theater_id),
        )


def _theater_exists(screen_number, mall_name, city, exclude_id=None):
    sql = """
        SELECT id FROM theaters
        WHERE screen_number = %s AND mall_name = %s AND city = %s
    """
    params = [screen_number, mall_name, city]
    if exclude_id:
        sql += " AND id != %s"
        params.append(exclude_id)
    return query_one(sql, tuple(params))


def _sync_showtime_theater_labels(theater_id):
    theater = _fetch_theater(theater_id)
    if not theater:
        return
    label = format_theater_label(theater)
    execute("UPDATE showtimes SET theater = %s WHERE theater_id = %s", (label, theater_id))


def _movie_options():
    return query_all("SELECT id, title FROM movies ORDER BY title")


def _parse_movie_form():
    return {
        "title": request.form.get("title", "").strip(),
        "description": request.form.get("description", "").strip(),
        "poster_url": request.form.get("poster_url", "").strip(),
        "duration": int(request.form.get("duration") or 120),
        "genre": request.form.get("genre", "").strip(),
        "rating": float(request.form.get("rating") or 0),
        "status": request.form.get("status", "now_showing"),
        "format_type": request.form.get("format_type", "2D"),
        "dolby_cinema": 1 if request.form.get("dolby_cinema") else 0,
        "dolby_audio": 1 if request.form.get("dolby_audio") else 0,
        "certification": request.form.get("certification", "UA16+").strip(),
        "release_date": request.form.get("release_date", "").strip() or None,
    }


def _movie_insert_params(data):
    return (
        data["title"],
        data["description"],
        data["poster_url"],
        data["duration"],
        data["genre"],
        data["rating"],
        data["status"],
        data["format_type"],
        data["dolby_cinema"],
        data["dolby_audio"],
        data["certification"],
        data["release_date"],
    )


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = query_one(
        """
        SELECT
            (SELECT COUNT(*) FROM movies) AS movies,
            (SELECT COUNT(*) FROM theaters) AS theaters,
            (SELECT COUNT(*) FROM showtimes) AS showtimes,
            (SELECT COALESCE(SUM(total_amount), 0) FROM bookings WHERE status = 'confirmed') AS revenue
        """
    )
    return render_template("admin/dashboard.html", stats=stats, active="dashboard")


@admin_bp.route("/revenue")
@admin_required
def revenue():
    summary = query_one(
        """
        SELECT
            COALESCE(SUM(CASE WHEN status = 'confirmed' THEN total_amount END), 0) AS total_revenue,
            COUNT(CASE WHEN status = 'confirmed' THEN 1 END) AS confirmed_count,
            COALESCE(SUM(CASE WHEN status = 'cancelled' THEN total_amount END), 0) AS cancelled_value,
            COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled_count
        FROM bookings
        """
    )
    by_movie = query_all(
        """
        SELECT m.title, COUNT(b.id) AS booking_count,
               COALESCE(SUM(b.total_amount), 0) AS revenue
        FROM bookings b
        JOIN showtimes s ON s.id = b.showtime_id
        JOIN movies m ON m.id = s.movie_id
        WHERE b.status = 'confirmed'
        GROUP BY m.id, m.title
        ORDER BY revenue DESC
        """
    )
    recent = query_all(
        """
        SELECT b.id, b.total_amount, b.booking_date, b.status,
               u.username, m.title AS movie_title
        FROM bookings b
        JOIN users u ON u.id = b.user_id
        JOIN showtimes s ON s.id = b.showtime_id
        JOIN movies m ON m.id = s.movie_id
        ORDER BY b.booking_date DESC
        LIMIT 20
        """
    )
    return render_template(
        "admin/revenue.html",
        summary=summary,
        by_movie=by_movie,
        recent=recent,
        active="revenue",
    )


# ——— Movies ———

@admin_bp.route("/movies")
@admin_required
def movies_list():
    movies = query_all("SELECT * FROM movies ORDER BY title")
    return render_template("admin/movies.html", movies=movies, active="movies")


@admin_bp.route("/movies/add", methods=["GET", "POST"])
@admin_required
def movie_add():
    if request.method == "POST":
        data = _parse_movie_form()
        if not data["title"]:
            flash("Title is required.", "error")
        else:
            movie_id = execute(
                """
                INSERT INTO movies (
                    title, description, poster_url, duration, genre, rating,
                    status, format_type, dolby_cinema, dolby_audio, certification, release_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                _movie_insert_params(data),
            )
            flash("Movie added. You can add cast members below.", "success")
            return redirect(url_for("admin.movie_edit", movie_id=movie_id))
    return render_template(
        "admin/movie_form.html",
        movie=None,
        formats=MOVIE_FORMATS,
        certifications=MOVIE_CERTIFICATIONS,
        statuses=MOVIE_STATUSES,
        active="movies",
    )


@admin_bp.route("/movies/<int:movie_id>/edit", methods=["GET", "POST"])
@admin_required
def movie_edit(movie_id):
    movie = query_one("SELECT * FROM movies WHERE id = %s", (movie_id,))
    if not movie:
        return render_template("404.html"), 404

    if request.method == "POST":
        data = _parse_movie_form()
        if not data["title"]:
            flash("Title is required.", "error")
        else:
            execute(
                """
                UPDATE movies SET title=%s, description=%s, poster_url=%s,
                duration=%s, genre=%s, rating=%s, status=%s, format_type=%s,
                dolby_cinema=%s, dolby_audio=%s, certification=%s, release_date=%s
                WHERE id=%s
                """,
                (*_movie_insert_params(data), movie_id),
            )
            flash("Movie updated.", "success")
            return redirect(url_for("admin.movie_edit", movie_id=movie_id))

    cast = _movie_cast(movie_id)
    return render_template(
        "admin/movie_form.html",
        movie=movie,
        cast=cast,
        formats=MOVIE_FORMATS,
        certifications=MOVIE_CERTIFICATIONS,
        statuses=MOVIE_STATUSES,
        active="movies",
    )


def _movie_cast(movie_id):
    return query_all(
        """
        SELECT id, actor_name, character_name, photo_url, sort_order
        FROM movie_cast WHERE movie_id = %s
        ORDER BY sort_order, id
        """,
        (movie_id,),
    )


@admin_bp.route("/movies/<int:movie_id>/cast/add", methods=["POST"])
@admin_required
def cast_add(movie_id):
    if not query_one("SELECT id FROM movies WHERE id = %s", (movie_id,)):
        return render_template("404.html"), 404

    actor_name = request.form.get("actor_name", "").strip()
    character_name = request.form.get("character_name", "").strip()
    photo_url = ""
    sort_order = int(request.form.get("sort_order") or 0)

    if not actor_name:
        flash("Actor name is required.", "error")
    else:
        execute(
            """
            INSERT INTO movie_cast (movie_id, actor_name, character_name, photo_url, sort_order)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (movie_id, actor_name, character_name or None, photo_url or None, sort_order),
        )
        flash("Cast member added.", "success")
    return redirect(url_for("admin.movie_edit", movie_id=movie_id))


@admin_bp.route("/movies/<int:movie_id>/cast/<int:cast_id>/delete", methods=["POST"])
@admin_required
def cast_delete(movie_id, cast_id):
    execute(
        "DELETE FROM movie_cast WHERE id = %s AND movie_id = %s",
        (cast_id, movie_id),
    )
    flash("Cast member removed.", "success")
    return redirect(url_for("admin.movie_edit", movie_id=movie_id))


@admin_bp.route("/movies/<int:movie_id>/delete", methods=["POST"])
@admin_required
def movie_delete(movie_id):
    execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    flash("Movie deleted.", "success")
    return redirect(url_for("admin.movies_list"))


# ——— Theaters ———

@admin_bp.route("/theaters")
@admin_required
def theaters_list():
    theaters = query_all(theaters_list_sql())
    return render_template("admin/theaters.html", theaters=theaters, active="theaters")


@admin_bp.route("/theaters/add", methods=["GET", "POST"])
@admin_required
def theater_add():
    if request.method == "POST":
        data = _parse_theater_form()
        if not all(data.values()):
            flash("Screen number, theatre/mall name, and city are required.", "error")
        elif _theater_exists(data["screen_number"], data["mall_name"], data["city"]):
            flash("This screen already exists at that mall and city.", "error")
        else:
            _insert_theater(data)
            flash("Theater added.", "success")
            return redirect(url_for("admin.theaters_list"))
    return render_template("admin/theater_form.html", theater=None, active="theaters")


@admin_bp.route("/theaters/<int:theater_id>/edit", methods=["GET", "POST"])
@admin_required
def theater_edit(theater_id):
    theater = _fetch_theater(theater_id)
    if not theater:
        return render_template("404.html"), 404

    if request.method == "POST":
        data = _parse_theater_form()
        if not all(data.values()):
            flash("Screen number, theatre/mall name, and city are required.", "error")
        elif _theater_exists(
            data["screen_number"], data["mall_name"], data["city"], theater_id
        ):
            flash("This screen already exists at that mall and city.", "error")
        else:
            _update_theater(theater_id, data)
            _sync_showtime_theater_labels(theater_id)
            flash("Theater updated.", "success")
            return redirect(url_for("admin.theaters_list"))

    return render_template("admin/theater_form.html", theater=theater, active="theaters")


@admin_bp.route("/theaters/<int:theater_id>/delete", methods=["POST"])
@admin_required
def theater_delete(theater_id):
    used = query_one(
        "SELECT id FROM showtimes WHERE theater_id = %s LIMIT 1", (theater_id,)
    )
    if used:
        flash("Cannot delete: theater is used by showtimes.", "error")
    else:
        execute("DELETE FROM theaters WHERE id = %s", (theater_id,))
        flash("Theater deleted.", "success")
    return redirect(url_for("admin.theaters_list"))


# ——— Showtimes ———

def _parse_showtime_form():
    return {
        "movie_id": int(request.form.get("movie_id") or 0),
        "theater_id": int(request.form.get("theater_id") or 0),
        "language": request.form.get("language", "Hindi").strip(),
        "show_date": request.form.get("show_date", ""),
        "show_time": request.form.get("show_time", ""),
        "price_prime": float(request.form.get("price_prime") or 150),
        "price_gold": float(request.form.get("price_gold") or 250),
        "price_recliner": float(request.form.get("price_recliner") or 450),
    }


@admin_bp.route("/showtimes")
@admin_required
def showtimes_list():
    showtimes = query_all(
        f"""
        SELECT s.id, s.show_date, s.show_time, s.language, s.price_prime, s.price_gold, s.price_recliner,
               m.title AS movie_title, {theater_display_sql()}
        FROM showtimes s
        JOIN movies m ON m.id = s.movie_id
        LEFT JOIN theaters t ON t.id = s.theater_id
        ORDER BY s.show_date DESC, s.show_time
        """
    )
    return render_template("admin/showtimes.html", showtimes=showtimes, active="showtimes")


@admin_bp.route("/showtimes/add", methods=["GET", "POST"])
@admin_required
def showtime_add():
    movies = _movie_options()
    theaters = _theater_options()
    if not movies or not theaters:
        flash("Add at least one movie and one theater first.", "warning")

    if request.method == "POST":
        data = _parse_showtime_form()
        theater = _fetch_theater(data["theater_id"])
        if (
            not data["movie_id"]
            or not theater
            or not data["show_date"]
            or not data["show_time"]
            or not data["language"]
        ):
            flash("All fields are required.", "error")
        else:
            execute(
                """
                INSERT INTO showtimes (movie_id, theater_id, theater, language, show_date, show_time,
                    price, price_prime, price_gold, price_recliner)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["movie_id"],
                    data["theater_id"],
                    format_theater_label(theater),
                    data["language"],
                    data["show_date"],
                    data["show_time"],
                    data["price_gold"],
                    data["price_prime"],
                    data["price_gold"],
                    data["price_recliner"],
                ),
            )
            flash("Showtime added.", "success")
            return redirect(url_for("admin.showtimes_list"))

    return render_template(
        "admin/showtime_form.html",
        showtime=None,
        movies=movies,
        theaters=theaters,
        languages=AVAILABLE_LANGUAGES,
        active="showtimes",
    )


@admin_bp.route("/showtimes/<int:showtime_id>/edit", methods=["GET", "POST"])
@admin_required
def showtime_edit(showtime_id):
    showtime = query_one("SELECT * FROM showtimes WHERE id = %s", (showtime_id,))
    if not showtime:
        return render_template("404.html"), 404

    movies = _movie_options()
    theaters = _theater_options()

    if request.method == "POST":
        data = _parse_showtime_form()
        theater = _fetch_theater(data["theater_id"])
        if (
            not data["movie_id"]
            or not theater
            or not data["show_date"]
            or not data["show_time"]
            or not data["language"]
        ):
            flash("All fields are required.", "error")
        else:
            execute(
                """
                UPDATE showtimes SET movie_id=%s, theater_id=%s, theater=%s, language=%s,
                show_date=%s, show_time=%s, price=%s, price_prime=%s, price_gold=%s, price_recliner=%s
                WHERE id=%s
                """,
                (
                    data["movie_id"],
                    data["theater_id"],
                    format_theater_label(theater),
                    data["language"],
                    data["show_date"],
                    data["show_time"],
                    data["price_gold"],
                    data["price_prime"],
                    data["price_gold"],
                    data["price_recliner"],
                    showtime_id,
                ),
            )
            flash("Showtime updated.", "success")
            return redirect(url_for("admin.showtimes_list"))

    return render_template(
        "admin/showtime_form.html",
        showtime=showtime,
        movies=movies,
        theaters=theaters,
        languages=AVAILABLE_LANGUAGES,
        active="showtimes",
    )


@admin_bp.route("/showtimes/<int:showtime_id>/delete", methods=["POST"])
@admin_required
def showtime_delete(showtime_id):
    execute("DELETE FROM showtimes WHERE id = %s", (showtime_id,))
    flash("Showtime deleted.", "success")
    return redirect(url_for("admin.showtimes_list"))


@admin_bp.route("/contacts")
@admin_required
def contacts_list():
    messages = query_all(
        """
        SELECT id, name, email, subject, category, message, created_at
        FROM contact_messages
        ORDER BY created_at DESC
        LIMIT 100
        """
    )
    return render_template(
        "admin/contacts.html", messages=messages, active="contacts"
    )
