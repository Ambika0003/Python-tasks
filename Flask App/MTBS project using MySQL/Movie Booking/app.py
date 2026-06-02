from datetime import datetime, timedelta

from flask import Flask, render_template, session

from config import Config
from db import close_db, init_database
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_database(app)

    @app.template_filter("format_time")
    def format_time(value):
        if value is None:
            return ""
        if hasattr(value, "strftime"):
            return value.strftime("%I:%M %p")
        if isinstance(value, timedelta):
            hours, remainder = divmod(int(value.total_seconds()), 3600)
            minutes = remainder // 60
            return datetime(2000, 1, 1, hours, minutes).strftime("%I:%M %p")
        return str(value)

    @app.template_filter("format_date")
    def format_date(value, fmt="%A, %B %d, %Y"):
        if value is None:
            return ""
        if hasattr(value, "strftime"):
            return value.strftime(fmt)
        if isinstance(value, str) and len(value) >= 10:
            try:
                parsed = datetime.strptime(value[:10], "%Y-%m-%d")
                return parsed.strftime(fmt)
            except ValueError:
                pass
        return str(value)

    @app.template_filter("inr")
    def format_inr(value):
        if value is None:
            return "₹0"
        return f"₹{float(value):,.0f}"

    @app.template_filter("date_input")
    def date_input(value):
        if value is None:
            return ""
        if hasattr(value, "isoformat"):
            return value.isoformat()[:10]
        if isinstance(value, str):
            return value[:10]
        return str(value)

    @app.template_filter("time_input")
    def time_input(value):
        if value is None:
            return ""
        if hasattr(value, "strftime"):
            return value.strftime("%H:%M")
        if isinstance(value, timedelta):
            total = int(value.total_seconds())
            hours, remainder = divmod(total, 3600)
            minutes = remainder // 60
            return f"{hours:02d}:{minutes:02d}"
        if isinstance(value, str):
            return value[:5] if len(value) >= 5 else value
        return str(value)[:5]

    # ✅ FIXED IMPORT (IMPORTANT CHANGE)
    import utils.images as images

    @app.context_processor
    def inject_globals():
        return {
            "is_admin": session.get("is_admin", False),

            # image helpers (FIXED)
            "movie_poster_src": images.movie_poster_src,
            "cast_photo_src": images.cast_photo_src,
            "movie_poster_hint": images.movie_poster_hint,
            "cast_photo_hint": images.cast_photo_hint,
        }

    app.teardown_appcontext(close_db)
    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)