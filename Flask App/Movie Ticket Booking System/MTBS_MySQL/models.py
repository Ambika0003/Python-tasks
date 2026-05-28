from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from sql_db import Base


class MovieDB(Base):

    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)

    movie_name = Column(String(100))
    theater_name = Column(String(100))
    screen_number = Column(Integer)
    show_time = Column(String(50))
    duration_minutes = Column(Integer)
    genre = Column(String(50))
    ticket_price = Column(Float)
    available_seats = Column(Integer)
    language = Column(String(50))
    rating = Column(Float)
    booking_status = Column(String(50))
    poster_url = Column(String(500))
    theater_location = Column(String(100))
    movie_format = Column(String(50))


class BookingDB(Base):

    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer)
    customer_name = Column(String(100))
    phone_number = Column(String(15))
    tickets = Column(Integer)
    seat_type = Column(String(50))
    selected_seats = Column(String(200))
    total_amount = Column(Float)
    booking_status = Column(String(50))
    booking_time = Column(DateTime, default=datetime.utcnow)