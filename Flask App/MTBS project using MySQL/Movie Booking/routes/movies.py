from flask import Blueprint, render_template, request

from db import query_all, query_one
from utils import theater_display_sql

movies_bp = Blueprint("movies", __name__)

_MOVIE_FIELDS = """
    id, title, poster_url, genre, rating, duration, description,
    status, format_type, dolby_cinema, dolby_audio, certification, release_date
"""


@movies_bp.route("/")
def index():
    now_showing = query_all(
        f"""
        SELECT {_MOVIE_FIELDS}
        FROM movies
        WHERE COALESCE(status, 'now_showing') = 'now_showing'
        ORDER BY title
        """
    )
    coming_soon = query_all(
        f"""
        SELECT {_MOVIE_FIELDS}
        FROM movies
        WHERE status = 'coming_soon'
        ORDER BY release_date, title
        """
    )
    return render_template(
        "index.html",
        now_showing=now_showing,
        coming_soon=coming_soon,
    )


@movies_bp.route("/movies/<int:movie_id>")
def detail(movie_id):
    movie = query_one("SELECT * FROM movies WHERE id = %s", (movie_id,))
    if not movie:
        return render_template("404.html"), 404

    is_coming_soon = movie.get("status") == "coming_soon"
    showtimes = []
    languages = []
    lang_filter = ""

    if not is_coming_soon:
        lang_filter = request.args.get("lang", "").strip()
        languages = query_all(
            """
            SELECT DISTINCT s.language
            FROM showtimes s
            WHERE s.movie_id = %s AND s.show_date >= CURDATE()
            ORDER BY s.language
            """,
            (movie_id,),
        )
        languages = [row["language"] for row in languages if row.get("language")]

        sql = f"""
            SELECT s.id, s.language, {theater_display_sql()},
                   s.show_date, s.show_time,
                   s.price_prime, s.price_gold, s.price_recliner
            FROM showtimes s
            LEFT JOIN theaters t ON t.id = s.theater_id
            WHERE s.movie_id = %s AND s.show_date >= CURDATE()
        """
        params = [movie_id]
        if lang_filter:
            sql += " AND s.language = %s"
            params.append(lang_filter)
        sql += " ORDER BY s.show_date, s.show_time"
        showtimes = query_all(sql, tuple(params))

    cast = query_all(
        """
        SELECT actor_name, character_name, photo_url
        FROM movie_cast
        WHERE movie_id = %s
        ORDER BY sort_order, id
        """,
        (movie_id,),
    )

    return render_template(
        "movie_detail.html",
        movie=movie,
        cast=cast,
        showtimes=showtimes,
        languages=languages,
        selected_language=lang_filter,
        is_coming_soon=is_coming_soon,
    )
