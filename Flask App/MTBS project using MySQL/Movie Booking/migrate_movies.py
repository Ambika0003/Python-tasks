"""
Add movie listing columns (status, format, dolby, etc.) to an existing MySQL database.
Run once if needed: python migrate_movies.py
"""
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

CONN = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DB", "movie_booking"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
}

MIGRATIONS = [
    "ALTER TABLE movies ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'now_showing'",
    "ALTER TABLE movies ADD COLUMN format_type VARCHAR(20) NOT NULL DEFAULT '2D'",
    "ALTER TABLE movies ADD COLUMN dolby_cinema TINYINT(1) NOT NULL DEFAULT 0",
    "ALTER TABLE movies ADD COLUMN dolby_audio TINYINT(1) NOT NULL DEFAULT 0",
    "ALTER TABLE movies ADD COLUMN certification VARCHAR(20) NOT NULL DEFAULT 'UA16+'",
    "ALTER TABLE movies ADD COLUMN release_date DATE NULL",
    "ALTER TABLE showtimes ADD COLUMN language VARCHAR(50) NOT NULL DEFAULT 'Hindi'",
]


def main():
    print("Migrating movies table for listing features...")
    conn = mysql.connector.connect(**CONN)
    cursor = conn.cursor()

    for sql in MIGRATIONS:
        try:
            cursor.execute(sql)
            conn.commit()
            print("  OK:", sql[:70], "...")
        except mysql.connector.Error as e:
            if e.errno == 1060:
                print("  Skip (already exists):", e.msg[:60])
                conn.rollback()
            else:
                print("  Error:", e)
                cursor.close()
                conn.close()
                raise

    cursor.close()
    conn.close()
    print("\nDone! Restart the Flask app.")


if __name__ == "__main__":
    main()
