from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.booking import booking_bp
from routes.pages import pages_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(admin_bp)
