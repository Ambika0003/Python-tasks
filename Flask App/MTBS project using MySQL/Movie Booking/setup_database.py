"""
Create the movie_booking database and tables.
Run once: python setup_database.py
"""
import os
import re
import sys

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get("MYSQL_HOST", "localhost")
USER = os.environ.get("MYSQL_USER", "root")
PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
PORT = int(os.environ.get("MYSQL_PORT", 3306))
DB_NAME = os.environ.get("MYSQL_DB", "movie_booking")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def main():
    print(f"Connecting to MySQL at {HOST}:{PORT} as {USER}...")

    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT,
        )
    except mysql.connector.Error as e:
        print(f"\nConnection failed: {e}")
        print("\nCheck that:")
        print("  1. MySQL Server is running (MySQL Workbench: Server > Start)")
        print("  2. Username and password in .env are correct")
        sys.exit(1)

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        sql = f.read()

    # Split on semicolons; skip comments-only chunks
    statements = []
    for part in re.split(r";\s*\n", sql):
        lines = [
            line
            for line in part.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]
        if lines:
            statements.append("\n".join(lines))

    cursor = conn.cursor()
    for i, stmt in enumerate(statements, 1):
        preview = stmt.strip().split("\n")[0][:60]
        try:
            cursor.execute(stmt)
            if stmt.strip().upper().startswith("SELECT"):
                for row in cursor.fetchall():
                    print(" ", row)
            else:
                print(f"  OK [{i}]: {preview}...")
        except mysql.connector.Error as e:
            print(f"\nFailed on statement {i}: {preview}...")
            print(f"Error: {e}")
            cursor.close()
            conn.close()
            sys.exit(1)

    conn.commit()
    cursor.execute(f"SHOW TABLES FROM `{DB_NAME}`")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    print(f"\nDone! Database '{DB_NAME}' is ready.")
    print(f"Tables: {', '.join(tables) if tables else '(none — check schema.sql)'}")
    print("\nRefresh schemas in MySQL Workbench (click refresh next to 'Schemas').")


if __name__ == "__main__":
    main()
