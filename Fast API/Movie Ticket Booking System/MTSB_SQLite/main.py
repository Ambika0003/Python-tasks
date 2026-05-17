# ============================================================
# 🎬 Movie Ticket Booking System
# FastAPI + SQLite
# ============================================================

# Run:
# uvicorn main:app --reload

# Swagger:
# http://127.0.0.1:8000/docs

# ============================================================
# 📦 Imports
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ============================================================
# 🚀 FastAPI App
# ============================================================

app = FastAPI()

# ============================================================
# 🌐 SQLite Connection
# ============================================================

DATABASE_URL = "sqlite:///movie_booking.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================================================
# 🧱 Database Models
# ============================================================

class MovieDB(Base):

    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String)
    theater_name = Column(String)
    show_time = Column(String)
    ticket_price = Column(Float)
    available_seats = Column(Integer)
    language = Column(String)
    rating = Column(Float)


class BookingDB(Base):

    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer)
    customer_name = Column(String)
    tickets = Column(Integer)
    total_amount = Column(Float)
    booking_status = Column(String)

# ============================================================
# 🛠 Create Tables
# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================
# 🧾 Pydantic Schemas
# ============================================================

class Movie(BaseModel):

    movie_id: int
    movie_name: str
    theater_name: str
    show_time: str
    ticket_price: float
    available_seats: int
    language: str
    rating: float


class Booking(BaseModel):

    booking_id: int
    customer_name: str
    tickets: int

# ============================================================
# 🏠 Home Route
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Movie Booking System Using SQLite 🚀"
    }

# ============================================================
# ✅ ADD MOVIE
# ============================================================

@app.post("/movies")
def add_movie(movie: Movie):

    db = SessionLocal()

    existing_movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie.movie_id
    ).first()

    if existing_movie:

        raise HTTPException(
            status_code=400,
            detail="Movie already exists"
        )

    new_movie = MovieDB(

        movie_id=movie.movie_id,
        movie_name=movie.movie_name,
        theater_name=movie.theater_name,
        show_time=movie.show_time,
        ticket_price=movie.ticket_price,
        available_seats=movie.available_seats,
        language=movie.language,
        rating=movie.rating
    )

    db.add(new_movie)

    db.commit()

    return {
        "message": "Movie added successfully"
    }

# ============================================================
# ✅ GET ALL MOVIES
# ============================================================

@app.get("/movies")
def get_movies():

    db = SessionLocal()

    movies = db.query(MovieDB).all()

    return movies

# ============================================================
# ✅ BOOK TICKET
# ============================================================

@app.post("/book-ticket/{movie_id}")
def book_ticket(movie_id: int, booking: Booking):

    db = SessionLocal()

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    if movie.available_seats < booking.tickets:

        raise HTTPException(
            status_code=400,
            detail="Not enough seats"
        )

    total_amount = booking.tickets * movie.ticket_price

    new_booking = BookingDB(

        booking_id=booking.booking_id,
        movie_id=movie.movie_id,
        customer_name=booking.customer_name,
        tickets=booking.tickets,
        total_amount=total_amount,
        booking_status="Booked"
    )

    movie.available_seats -= booking.tickets

    db.add(new_booking)

    db.commit()

    return {

        "message": "Ticket booked successfully",

        "total_amount": total_amount
    }

# ============================================================
# ✅ GET BOOKINGS
# ============================================================

@app.get("/bookings")
def get_bookings():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()

    return bookings

# ============================================================
# ✅ CANCEL TICKET
# ============================================================

@app.post("/cancel-ticket/{booking_id}")
def cancel_ticket(booking_id: int):

    db = SessionLocal()

    booking = db.query(BookingDB).filter(
        BookingDB.booking_id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == booking.movie_id
    ).first()

    movie.available_seats += booking.tickets

    db.delete(booking)

    db.commit()

    return {
        "message": "Ticket cancelled successfully"
    }