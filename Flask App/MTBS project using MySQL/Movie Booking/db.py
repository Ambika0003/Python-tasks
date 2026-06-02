import os
import re
import sqlite3
from contextlib import contextmanager

from flask import current_app, g
from werkzeug.security import generate_password_hash

_SCHEMA_SQLITE = os.path.join(os.path.dirname(__file__), "schema_sqlite.sql")
_ADMIN_USERNAME = "admin"


def _backend():
    return current_app.config.get("DB_BACKEND", "sqlite").lower()


def _adapt_sql(sql):
    if _backend() == "sqlite":
        sql = sql.replace("CURDATE()", "date('now')")
        sql = sql.replace("%s", "?")
    return sql


def _row_to_dict(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)


def get_db():
    if "db" not in g:
        if _backend() == "sqlite":
            path = current_app.config["SQLITE_PATH"]
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            conn = sqlite3.connect(path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            g.db = conn
        else:
            import mysql.connector

            g.db = mysql.connector.connect(
                host=current_app.config["MYSQL_HOST"],
                user=current_app.config["MYSQL_USER"],
                password=current_app.config["MYSQL_PASSWORD"],
                database=current_app.config["MYSQL_DB"],
                port=current_app.config["MYSQL_PORT"],
            )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def _execute_cursor(db, sql, params):
    sql = _adapt_sql(sql)
    params = params or ()
    if _backend() == "sqlite":
        cur = db.execute(sql, params)
        return cur
    cursor = db.cursor()
    cursor.execute(sql, params)
    return cursor


def query_one(sql, params=None):
    if _backend() == "sqlite":
        cur = _execute_cursor(get_db(), sql, params)
        return _row_to_dict(cur.fetchone())
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(sql, params or ())
    row = cursor.fetchone()
    cursor.close()
    return row


def query_all(sql, params=None):
    if _backend() == "sqlite":
        cur = _execute_cursor(get_db(), sql, params)
        return [_row_to_dict(r) for r in cur.fetchall()]
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    return rows


def execute(sql, params=None):
    db = get_db()
    cur = _execute_cursor(db, sql, params)
    db.commit()
    if _backend() == "sqlite":
        return cur.lastrowid
    last_id = cur.lastrowid
    cur.close()
    return last_id


def execute_in_tx(db, sql, params=None):
    cur = _execute_cursor(db, sql, params)
    if _backend() != "sqlite":
        return cur
    return cur


@contextmanager
def transaction():
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


def table_columns(table):
    """Return column names for the active DB backend (requires app context)."""
    backend = current_app.config.get("DB_BACKEND", "sqlite").lower()
    if backend == "sqlite":
        rows = query_all(f"PRAGMA table_info({table})")
        return {row["name"] for row in rows}
    return _mysql_table_columns(table)


def _mysql_table_columns(table):
    return {row["Field"] for row in query_all(f"SHOW COLUMNS FROM `{table}`")}


def _mysql_exec(sql):
    """Run DDL on MySQL; ignore duplicate column/table errors."""
    import mysql.connector

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except mysql.connector.Error as e:
        db.rollback()
        if e.errno not in (1050, 1060, 1061):
            raise
    finally:
        cur.close()


def _migrate_mysql_schema():
    """Add columns/tables missing from older MySQL installs."""
    movie_cols = _mysql_table_columns("movies")
    if "status" not in movie_cols:
        _mysql_exec(
            "ALTER TABLE movies ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'now_showing'"
        )
    if "format_type" not in movie_cols:
        _mysql_exec(
            "ALTER TABLE movies ADD COLUMN format_type VARCHAR(20) NOT NULL DEFAULT '2D'"
        )
    if "dolby_cinema" not in movie_cols:
        _mysql_exec(
            "ALTER TABLE movies ADD COLUMN dolby_cinema TINYINT(1) NOT NULL DEFAULT 0"
        )
    if "dolby_audio" not in movie_cols:
        _mysql_exec(
            "ALTER TABLE movies ADD COLUMN dolby_audio TINYINT(1) NOT NULL DEFAULT 0"
        )
    if "certification" not in movie_cols:
        _mysql_exec(
            "ALTER TABLE movies ADD COLUMN certification VARCHAR(20) NOT NULL DEFAULT 'UA16+'"
        )
    if "release_date" not in movie_cols:
        _mysql_exec("ALTER TABLE movies ADD COLUMN release_date DATE NULL")

    showtime_cols = _mysql_table_columns("showtimes")
    if "language" not in showtime_cols:
        _mysql_exec(
            "ALTER TABLE showtimes ADD COLUMN language VARCHAR(50) NOT NULL DEFAULT 'Hindi'"
        )

    exists = query_one(
        """
        SELECT 1 AS ok FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = 'movie_cast'
        """
    )
    if not exists:
        _mysql_exec(
            """
            CREATE TABLE movie_cast (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT NOT NULL,
                actor_name VARCHAR(120) NOT NULL,
                character_name VARCHAR(120) DEFAULT NULL,
                photo_url VARCHAR(500) DEFAULT NULL,
                sort_order INT DEFAULT 0,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
            )
            """
        )

    _migrate_mysql_theaters()

    if "price_prime" not in showtime_cols:
        _mysql_exec(
            """
            ALTER TABLE showtimes
            ADD COLUMN price_prime DECIMAL(8, 2) NOT NULL DEFAULT 150.00,
            ADD COLUMN price_gold DECIMAL(8, 2) NOT NULL DEFAULT 250.00,
            ADD COLUMN price_recliner DECIMAL(8, 2) NOT NULL DEFAULT 450.00
            """
        )

    seat_cols = _mysql_table_columns("seats")
    if "category" not in seat_cols:
        _mysql_exec(
            """
            ALTER TABLE seats
            ADD COLUMN category ENUM('prime', 'gold', 'recliner') NOT NULL DEFAULT 'gold'
            """
        )
        execute("UPDATE seats SET category = 'prime' WHERE row_label IN ('A', 'B')")
        execute("UPDATE seats SET category = 'gold' WHERE row_label IN ('C', 'D', 'E', 'F')")
        execute("UPDATE seats SET category = 'recliner' WHERE row_label IN ('G', 'H')")


def _migrate_mysql_theaters():
    """Add screen/mall/city columns and backfill from legacy name/location."""
    theater_cols = _mysql_table_columns("theaters")
    if "screen_number" not in theater_cols:
        _mysql_exec("ALTER TABLE theaters ADD COLUMN screen_number VARCHAR(50)")
        _mysql_exec("ALTER TABLE theaters ADD COLUMN mall_name VARCHAR(150)")
        _mysql_exec("ALTER TABLE theaters ADD COLUMN city VARCHAR(100)")

    cities = {
        "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Delhi",
        "Kolkata", "Pune", "Kochi", "Ahmedabad",
    }
    defaults = [
        ("Screen 1", "PVR Forum Mall", "Bangalore"),
        ("Screen 2", "INOX Garuda Mall", "Bangalore"),
        ("Screen 3", "Cinepolis Nexus", "Mumbai"),
    ]

    rows = query_all(
        "SELECT id, name, location, screen_number FROM theaters"
    )
    for row in rows:
        if row.get("screen_number"):
            continue
        idx = (row["id"] - 1) % len(defaults)
        screen, mall, city = defaults[idx]
        name, loc = row.get("name") or screen, row.get("location")
        if name:
            screen = name
        if loc in cities:
            city = loc
        elif loc and loc not in ("Main Hall", "Premium Wing"):
            mall = loc
        execute(
            """
            UPDATE theaters SET screen_number = %s, mall_name = %s, city = %s
            WHERE id = %s
            """,
            (screen, mall, city, row["id"]),
        )

    for row in query_all(
        """
        SELECT s.id, t.screen_number, t.mall_name, t.city, t.name, t.location, s.theater
        FROM showtimes s
        LEFT JOIN theaters t ON t.id = s.theater_id
        """
    ):
        label = _theater_label(
            row.get("screen_number"),
            row.get("mall_name"),
            row.get("city"),
            row.get("name"),
            row.get("location"),
        )
        if label and label != row.get("theater"):
            execute("UPDATE showtimes SET theater = %s WHERE id = %s", (label, row["id"]))


def _ensure_contact_table():
    backend = current_app.config.get("DB_BACKEND", "sqlite").lower()
    if backend == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            subject VARCHAR(200) NOT NULL,
            category VARCHAR(50) NOT NULL DEFAULT 'general',
            message TEXT NOT NULL,
            user_id INTEGER NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            subject VARCHAR(200) NOT NULL,
            category VARCHAR(50) NOT NULL DEFAULT 'general',
            message TEXT NOT NULL,
            user_id INT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
    db = get_db()
    if backend == "sqlite":
        db.execute(sql)
        db.commit()
    else:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()


def init_database(app):
    """Create SQLite DB + sample data + admin user when using sqlite."""
    with app.app_context():
        _ensure_contact_table()
        if app.config.get("DB_BACKEND", "sqlite").lower() == "mysql":
            _migrate_mysql_schema()
            _ensure_admin_user(app)

    if app.config.get("DB_BACKEND", "sqlite").lower() != "sqlite":
        return

    path = app.config["SQLITE_PATH"]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    if os.path.exists(path) and os.path.getsize(path) > 0:
        _migrate_sqlite_schema(path)
        with app.app_context():
            _ensure_admin_user(app)
        return

    with open(_SCHEMA_SQLITE, encoding="utf-8") as f:
        sql = f.read()

    statements = []
    for part in re.split(r";\s*\n", sql):
        lines = [
            line
            for line in part.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]
        if lines:
            statements.append("\n".join(lines))

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    for stmt in statements:
        conn.execute(stmt)
    conn.commit()
    conn.close()

    with app.app_context():
        _ensure_admin_user(app)


def _theater_label(screen, mall, city, name=None, location=None):
    if screen and mall and city:
        return f"{screen} · {mall} · {city}"
    if name:
        return f"{name} · {location}" if location else name
    return ""


def _migrate_sqlite_schema(path):
    """Add theater fields + showtime language; migrate existing rows."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    theater_cols = {row[1] for row in cur.execute("PRAGMA table_info(theaters)")}
    if "mall_name" not in theater_cols:
        cur.execute("ALTER TABLE theaters ADD COLUMN screen_number VARCHAR(50)")
        cur.execute("ALTER TABLE theaters ADD COLUMN mall_name VARCHAR(150)")
        cur.execute("ALTER TABLE theaters ADD COLUMN city VARCHAR(100)")

        cities = {
            "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Delhi",
            "Kolkata", "Pune", "Kochi", "Ahmedabad",
        }
        defaults = [
            ("Screen 1", "PVR Forum Mall", "Bangalore"),
            ("Screen 2", "INOX Garuda Mall", "Bangalore"),
            ("Screen 3", "Cinepolis Nexus", "Mumbai"),
        ]
        for row in cur.execute(
            "SELECT id, name, location, screen_number FROM theaters"
        ):
            if row["screen_number"]:
                continue
            idx = (row["id"] - 1) % len(defaults)
            screen, mall, city = defaults[idx]
            name, loc = row["name"] or screen, row["location"]
            if name:
                screen = name
            if loc in cities:
                city = loc
            elif loc and loc not in ("Main Hall", "Premium Wing"):
                mall = loc
            cur.execute(
                "UPDATE theaters SET screen_number=?, mall_name=?, city=? WHERE id=?",
                (screen, mall, city, row["id"]),
            )

    showtime_cols = {row[1] for row in cur.execute("PRAGMA table_info(showtimes)")}
    if "language" not in showtime_cols:
        cur.execute(
            "ALTER TABLE showtimes ADD COLUMN language VARCHAR(50) DEFAULT 'Hindi'"
        )
        sample_langs = [
            "Hindi", "English", "Tamil", "Telugu",
            "Hindi", "English", "Hindi", "English",
        ]
        for row in cur.execute("SELECT id FROM showtimes"):
            lang = sample_langs[(row["id"] - 1) % len(sample_langs)]
            cur.execute("UPDATE showtimes SET language=? WHERE id=?", (lang, row["id"]))

    cities = {
        "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Delhi",
        "Kolkata", "Pune", "Kochi", "Ahmedabad",
    }
    defaults = [
        ("Screen 1", "PVR Forum Mall", "Bangalore"),
        ("Screen 2", "INOX Garuda Mall", "Bangalore"),
        ("Screen 3", "Cinepolis Nexus", "Mumbai"),
    ]
    for row in cur.execute(
        "SELECT id, name, location FROM theaters WHERE screen_number IS NULL OR screen_number = ''"
    ):
        idx = (row["id"] - 1) % len(defaults)
        screen, mall, city = defaults[idx]
        name, loc = row["name"], row["location"]
        if name:
            screen = name
        if loc in cities:
            city = loc
        elif loc and loc not in ("Main Hall", "Premium Wing"):
            mall = loc
        cur.execute(
            "UPDATE theaters SET screen_number=?, mall_name=?, city=? WHERE id=?",
            (screen, mall, city, row["id"]),
        )
        if "name" in theater_cols:
            cur.execute(
                "UPDATE theaters SET name=?, location=? WHERE id=?",
                (screen, city, row["id"]),
            )

    for row in cur.execute(
        """
        SELECT s.id, t.screen_number, t.mall_name, t.city, t.name, t.location, s.theater
        FROM showtimes s
        LEFT JOIN theaters t ON t.id = s.theater_id
        """
    ):
        label = _theater_label(
            row["screen_number"],
            row["mall_name"],
            row["city"],
            row["name"],
            row["location"],
        )
        if label and label != row["theater"]:
            cur.execute("UPDATE showtimes SET theater=? WHERE id=?", (label, row["id"]))

    movie_cols = {row[1] for row in cur.execute("PRAGMA table_info(movies)")}
    if "status" not in movie_cols:
        cur.execute(
            "ALTER TABLE movies ADD COLUMN status VARCHAR(20) DEFAULT 'now_showing'"
        )
        cur.execute(
            "ALTER TABLE movies ADD COLUMN format_type VARCHAR(20) DEFAULT '2D'"
        )
        cur.execute(
            "ALTER TABLE movies ADD COLUMN dolby_cinema INTEGER DEFAULT 0"
        )
        cur.execute(
            "ALTER TABLE movies ADD COLUMN dolby_audio INTEGER DEFAULT 0"
        )
        cur.execute(
            "ALTER TABLE movies ADD COLUMN certification VARCHAR(20) DEFAULT 'UA16+'"
        )
        cur.execute("ALTER TABLE movies ADD COLUMN release_date DATE")

        movie_meta = {
            1: ("now_showing", "2D", 1, 1, "UA16+"),
            2: ("now_showing", "2D", 1, 1, "UA16+"),
            3: ("now_showing", "IMAX", 1, 1, "UA"),
            4: ("now_showing", "2D", 0, 1, "UA13+"),
            5: ("coming_soon", "2D", 1, 1, "UA16+"),
        }
        for mid, (status, fmt, dolby_c, dolby_a, cert) in movie_meta.items():
            if status == "coming_soon":
                cur.execute(
                    """
                    UPDATE movies SET status=?, format_type=?, dolby_cinema=?,
                    dolby_audio=?, certification=?,
                    release_date=date('now', '+21 days') WHERE id=?
                    """,
                    (status, fmt, dolby_c, dolby_a, cert, mid),
                )
            else:
                cur.execute(
                    """
                    UPDATE movies SET status=?, format_type=?, dolby_cinema=?,
                    dolby_audio=?, certification=? WHERE id=?
                    """,
                    (status, fmt, dolby_c, dolby_a, cert, mid),
                )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS movie_cast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            actor_name VARCHAR(120) NOT NULL,
            character_name VARCHAR(120),
            photo_url VARCHAR(500),
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
        )
        """
    )
    if not cur.execute("SELECT 1 FROM movie_cast LIMIT 1").fetchone():
        sample_cast = [
            (1, "Leonardo DiCaprio", "Cobb", "https://image.tmdb.org/t/p/w185/5Brcq6ifCnDLVNPKazAlIq6y4F.jpg", 1),
            (1, "Joseph Gordon-Levitt", "Arthur", "https://image.tmdb.org/t/p/w185/4UdmMdEpR1Y2lW6BLVUPUW1o1bn.jpg", 2),
            (1, "Ellen Page", "Ariadne", "https://image.tmdb.org/t/p/w185/9V5NpCiuzLIEbE6dOP1G5Z6MTY4.jpg", 3),
            (1, "Tom Hardy", "Eames", "https://image.tmdb.org/t/p/w185/njeMzUf5IoDHRbhP1GDioQs2YJ.jpg", 4),
            (2, "Christian Bale", "Bruce Wayne / Batman", "https://image.tmdb.org/t/p/w185/4N3kFUBRO6usORs0Gr38dVON1O.jpg", 1),
            (2, "Heath Ledger", "Joker", "https://image.tmdb.org/t/p/w185/5YBFHtCHybaB4GJOtbpr7mT2FBK.jpg", 2),
            (2, "Aaron Eckhart", "Harvey Dent", "https://image.tmdb.org/t/p/w185/6yIBOwqJiJ8d9pMaIBlEwbqYqH.jpg", 3),
            (3, "Matthew McConaughey", "Cooper", "https://image.tmdb.org/t/p/w185/fjd1ge4yTsV6aIZHLk3jfnop1QX.jpg", 1),
            (3, "Anne Hathaway", "Brand", "https://image.tmdb.org/t/p/w185/rxDWZ10VBlaQk0bFWv4UEukagcs.jpg", 2),
            (4, "Robert Downey Jr.", "Tony Stark", "https://image.tmdb.org/t/p/w185/1YjsN4tONlXXBSHjo08rEYXQMp.jpg", 1),
            (4, "Chris Evans", "Steve Rogers", "https://image.tmdb.org/t/p/w185/3bOGNsHlrswhy79ruvI9yiLzFj2.jpg", 2),
            (4, "Scarlett Johansson", "Natasha Romanoff", "https://image.tmdb.org/t/p/w185/6NsMbJXRlD8DJxveDvk8pBignot.jpg", 3),
        ]
        for movie_id, actor, role, photo, order in sample_cast:
            cur.execute(
                """
                INSERT INTO movie_cast (movie_id, actor_name, character_name, photo_url, sort_order)
                VALUES (?, ?, ?, ?, ?)
                """,
                (movie_id, actor, role, photo, order),
            )

    conn.commit()
    conn.close()


def _ensure_admin_user(app):
    """Create or sync admin login for ADMIN_EMAIL (runs on sqlite and mysql)."""
    admin_email = app.config.get("ADMIN_EMAIL", "")
    if not admin_email:
        return

    password_hash = generate_password_hash(
        app.config.get("ADMIN_PASSWORD", "Ambika@2003")
    )
    existing = query_one("SELECT id FROM users WHERE email = %s", (admin_email,))
    if existing:
        execute(
            "UPDATE users SET username = %s, password_hash = %s WHERE email = %s",
            (_ADMIN_USERNAME, password_hash, admin_email),
        )
    else:
        execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (_ADMIN_USERNAME, admin_email, password_hash),
        )
