"""
Create or update the admin user (uses DB_BACKEND from .env).
Run: py create_admin.py
"""
import argparse
import sys

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from app import create_app
from db import execute, query_one

DEFAULT_ADMIN_PASSWORD = "Ambika@2003"
ADMIN_USERNAME = "admin"


def main():
    parser = argparse.ArgumentParser(description="Create or update the admin user.")
    parser.add_argument("--password", default=DEFAULT_ADMIN_PASSWORD)
    args = parser.parse_args()

    app = create_app()
    admin_email = app.config.get("ADMIN_EMAIL", "")
    if not admin_email:
        print("Set ADMIN_EMAIL in .env before running this script.")
        sys.exit(1)

    with app.app_context():
        app.config["ADMIN_PASSWORD"] = args.password
        from db import _ensure_admin_user

        _ensure_admin_user(app)
        print(f"Admin ready: {admin_email}")

    print(f"Username: {ADMIN_USERNAME}")
    print("Log in at /login, then open Admin Panel from the nav or /admin")


if __name__ == "__main__":
    main()
