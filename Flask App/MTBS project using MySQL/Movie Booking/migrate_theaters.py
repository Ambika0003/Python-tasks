"""
Add theaters table and link showtimes. Run once: python migrate_theaters.py
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


def run(cursor, sql):
    try:
        cursor.execute(sql)
        print("  OK:", sql.strip().split("\n")[0][:70])
        return True
    except mysql.connector.Error as e:
        if e.errno in (1050, 1060, 1061):
            print("  Skip:", e.msg[:70])
            return False
        raise


def main():
    print("Migrating theaters...")
    conn = mysql.connector.connect(**CONN)
    cursor = conn.cursor()

    run(
        cursor,
        """
        CREATE TABLE IF NOT EXISTS theaters (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            location VARCHAR(150) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )
    conn.commit()

    for col_sql in [
        "ALTER TABLE theaters ADD COLUMN screen_number VARCHAR(50)",
        "ALTER TABLE theaters ADD COLUMN mall_name VARCHAR(150)",
        "ALTER TABLE theaters ADD COLUMN city VARCHAR(100)",
    ]:
        run(cursor, col_sql)
    conn.commit()

    cursor.execute("SELECT DISTINCT theater FROM showtimes WHERE theater IS NOT NULL")
    for (name,) in cursor.fetchall():
        cursor.execute(
            "INSERT IGNORE INTO theaters (name) VALUES (%s)",
            (name,),
        )
    conn.commit()

    run(
        cursor,
        "ALTER TABLE showtimes ADD COLUMN theater_id INT NULL AFTER movie_id",
    )
    conn.commit()

    cursor.execute(
        """
        UPDATE showtimes s
        JOIN theaters t ON t.name = s.theater
        SET s.theater_id = t.id
        WHERE s.theater_id IS NULL
        """
    )
    conn.commit()

    cursor.close()
    conn.close()
    print("\nDone! Restart Flask and use Admin Panel.")


if __name__ == "__main__":
    main()
