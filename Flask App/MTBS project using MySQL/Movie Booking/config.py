import os

from dotenv import load_dotenv

load_dotenv()

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 days

    # sqlite = local file DB (no MySQL). mysql = when MySQL is installed later.
    DB_BACKEND = os.environ.get("DB_BACKEND", "sqlite").strip().lower()
    SQLITE_PATH = os.environ.get(
        "SQLITE_PATH", os.path.join(_BASE_DIR, "instance", "movie_booking.db")
    )

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "movie_booking")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Ambika@2003")

    SEAT_TIER_ROWS = {
        "prime": ["A", "B"],
        "gold": ["C", "D", "E", "F"],
        "recliner": ["G", "H"],
    }
    SEAT_TIER_LABELS = {
        "prime": "Prime",
        "gold": "Gold",
        "recliner": "Recliners",
    }
    SEAT_TIER_ORDER = ["prime", "gold", "recliner"]

    ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
    SEATS_PER_ROW = 10
