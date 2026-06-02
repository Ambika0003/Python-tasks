from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import execute, query_one

auth_bp = Blueprint("auth", __name__)


def _set_user_session(user):
    session.permanent = True
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    admin_email = current_app.config.get("ADMIN_EMAIL", "")
    session["is_admin"] = bool(
        admin_email and user.get("email", "").lower() == admin_email.lower()
    )


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        if not session.get("is_admin"):
            flash("Admin access only.", "error")
            return redirect(url_for("movies.index"))
        return f(*args, **kwargs)

    return decorated


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        elif query_one("SELECT id FROM users WHERE username = %s", (username,)):
            flash("Username already taken.", "error")
        elif query_one("SELECT id FROM users WHERE email = %s", (email,)):
            flash("Email already registered.", "error")
        else:
            password_hash = generate_password_hash(password)
            execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash),
            )
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next") or request.form.get("next") or url_for("movies.index")

    if "user_id" in session:
        return redirect(next_url)

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = query_one(
            "SELECT id, username, email, password_hash FROM users WHERE email = %s",
            (email,),
        )
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            _set_user_session(user)
            if session.get("is_admin") and next_url == url_for("movies.index"):
                return redirect(url_for("admin.dashboard"))
            return redirect(next_url)

        flash("Invalid email or password.", "error")

    return render_template("login.html", next_url=next_url)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("movies.index"))
