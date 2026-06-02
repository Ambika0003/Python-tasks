"""
Upgrade existing database for seat tiers and INR pricing.
Run once: python migrate_tiers.py
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
    """
    ALTER TABLE showtimes
    ADD COLUMN price_prime DECIMAL(8, 2) NOT NULL DEFAULT 350.00 AFTER price,
    ADD COLUMN price_gold DECIMAL(8, 2) NOT NULL DEFAULT 250.00 AFTER price_prime,
    ADD COLUMN price_recliner DECIMAL(8, 2) NOT NULL DEFAULT 450.00 AFTER price_gold
    """,
    """
    UPDATE showtimes SET
        price_gold = CASE WHEN price < 50 THEN price * 20 ELSE price END,
        price_prime = CASE WHEN price < 50 THEN price * 28 ELSE price * 1.4 END,
        price_recliner = CASE WHEN price < 50 THEN price * 35 ELSE price * 1.75 END
    """,
    """
    ALTER TABLE seats
    ADD COLUMN category ENUM('prime', 'gold', 'recliner') NOT NULL DEFAULT 'gold' AFTER seat_number
    """,
    "UPDATE seats SET category = 'prime' WHERE row_label IN ('A', 'B')",
    "UPDATE seats SET category = 'gold' WHERE row_label IN ('C', 'D', 'E', 'F')",
    "UPDATE seats SET category = 'recliner' WHERE row_label IN ('G', 'H')",
]


def main():
    print("Migrating database for seat tiers and INR pricing...")
    conn = mysql.connector.connect(**CONN)
    cursor = conn.cursor()

    for sql in MIGRATIONS:
        try:
            cursor.execute(sql)
            conn.commit()
            print("  OK:", sql.strip().split("\n")[0][:70], "...")
        except mysql.connector.Error as e:
            if e.errno == 1060:  # duplicate column
                print("  Skip (already applied):", e.msg[:80])
                conn.rollback()
            else:
                print("  Error:", e)
                cursor.close()
                conn.close()
                raise

    cursor.close()
    conn.close()
    print("\nDone! Restart the Flask app and refresh the seat selection page.")


if __name__ == "__main__":
    main()
