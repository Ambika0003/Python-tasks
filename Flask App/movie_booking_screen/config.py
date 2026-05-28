import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default-dev-secret-key-9988')

    # Database Configurations
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'movie_booking_db')

    # Prefer SQLite for local development when no usable MySQL credentials are provided.
    # Set USE_SQLITE=false to force the MySQL URI instead.
    USE_SQLITE = os.environ.get('USE_SQLITE', 'true').lower() in ('1', 'true', 'yes', 'on')

    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    elif USE_SQLITE and not DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///movie_booking.db'
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
