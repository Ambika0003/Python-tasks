from flask import current_app

from db import execute, query_all, table_columns

MOVIE_FORMATS = ["2D", "3D", "IMAX", "4DX"]
MOVIE_CERTIFICATIONS = ["U", "UA", "UA13+", "UA16+", "A", "S"]
MOVIE_STATUSES = ["now_showing", "coming_soon"]

AVAILABLE_LANGUAGES = [
    "Hindi",
    "English",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Marathi",
]


def theater_display_sql(table_alias="t", fallback="s.theater"):
    """SQL expression for theatre label; adapts to legacy and modern schemas."""
    backend = current_app.config.get("DB_BACKEND", "sqlite").lower()
    cols = table_columns("theaters")

    if "screen_number" in cols and "mall_name" in cols and "city" in cols:
        if backend == "sqlite":
            modern = (
                f"{table_alias}.screen_number || ' · ' || "
                f"{table_alias}.mall_name || ' · ' || {table_alias}.city"
            )
        else:
            modern = (
                f"CONCAT({table_alias}.screen_number, ' · ', "
                f"{table_alias}.mall_name, ' · ', {table_alias}.city)"
            )
        parts = [modern]
        if "name" in cols:
            parts.append(f"{table_alias}.name")
        parts.append(fallback)
        return f"COALESCE({', '.join(parts)}) AS theater"

    if "name" in cols and "location" in cols:
        if backend == "sqlite":
            legacy = f"{table_alias}.name || ' · ' || {table_alias}.location"
        else:
            legacy = f"CONCAT({table_alias}.name, ' · ', {table_alias}.location)"
        return f"COALESCE({legacy}, {table_alias}.name, {fallback}) AS theater"

    return f"COALESCE({fallback}) AS theater"


def theaters_list_sql():
    """SELECT for theatre rows; works before and after schema migration."""
    cols = table_columns("theaters")
    if "screen_number" in cols and "mall_name" in cols and "city" in cols:
        return """
            SELECT id, screen_number, mall_name, city, name, location
            FROM theaters
            ORDER BY city, mall_name, screen_number
        """
    return """
        SELECT id, name, location,
               name AS screen_number, '' AS mall_name, location AS city
        FROM theaters
        ORDER BY name
        """


def format_theater_label(theater):
    if not theater:
        return ""
    if theater.get("screen_number") and theater.get("mall_name") and theater.get("city"):
        return f"{theater['screen_number']} · {theater['mall_name']} · {theater['city']}"
    if theater.get("name"):
        loc = theater.get("location")
        return f"{theater['name']} · {loc}" if loc else theater["name"]
    return theater.get("theater", "")


def theater_option_label(theater):
    return format_theater_label(theater)


def row_category(row_label):
    tiers = current_app.config["SEAT_TIER_ROWS"]
    for category, rows in tiers.items():
        if row_label in rows:
            return category
    return "gold"


def ensure_seats_for_showtime(showtime_id):
    existing = query_all(
        "SELECT id FROM seats WHERE showtime_id = %s LIMIT 1", (showtime_id,)
    )
    if existing:
        return

    rows = current_app.config["ROWS"]
    seats_per_row = current_app.config["SEATS_PER_ROW"]
    for row in rows:
        category = row_category(row)
        for num in range(1, seats_per_row + 1):
            execute(
                """
                INSERT INTO seats (showtime_id, row_label, seat_number, category, status)
                VALUES (%s, %s, %s, %s, 'available')
                """,
                (showtime_id, row, num, category),
            )


def tier_prices_from_showtime(showtime):
    return {
        "prime": float(showtime["price_prime"]),
        "gold": float(showtime["price_gold"]),
        "recliner": float(showtime["price_recliner"]),
    }
