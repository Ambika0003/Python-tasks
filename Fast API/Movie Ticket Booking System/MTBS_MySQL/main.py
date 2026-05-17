# ============================================================
# 🎬 Movie Ticket Booking System
# FastAPI + MySQL + SQLAlchemy
# ============================================================

# Install Packages:
# pip install fastapi uvicorn sqlalchemy pymysql

# Run Server:
# uvicorn main:app --reload

# Swagger UI:
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
# 🌐 MySQL Connection
# ============================================================

DATABASE_URL = "mysql+pymysql://root:root@localhost/movie_booking_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================================================
# 🧱 MySQL Models
# ============================================================

class MovieDB(Base):

    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(100))
    theater_name = Column(String(100))
    show_time = Column(String(50))
    ticket_price = Column(Float)
    available_seats = Column(Integer)
    language = Column(String(50))
    rating = Column(Float)


class BookingDB(Base):

    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer)
    customer_name = Column(String(100))
    tickets = Column(Integer)
    total_amount = Column(Float)
    booking_status = Column(String(50))

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

    customer_name: str
    tickets: int

# ============================================================
# 🏠 Home Route
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Movie Ticket Booking System Using MySQL 🚀"
    }

# ============================================================
# ✅ 1. ADD MOVIE
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
            detail="Movie ID already exists"
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
# ✅ 2. GET ALL MOVIES
# ============================================================

@app.get("/movies")
def get_movies():

    db = SessionLocal()

    movies = db.query(MovieDB).all()

    return movies

# ============================================================
# ✅ 3. GET MOVIE BY ID
# ============================================================

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    db = SessionLocal()

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie

# ============================================================
# ✅ 4. UPDATE MOVIE
# ============================================================

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):

    db = SessionLocal()

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    movie.movie_name = updated_movie.movie_name
    movie.theater_name = updated_movie.theater_name
    movie.show_time = updated_movie.show_time
    movie.ticket_price = updated_movie.ticket_price
    movie.available_seats = updated_movie.available_seats
    movie.language = updated_movie.language
    movie.rating = updated_movie.rating

    db.commit()

    return {
        "message": "Movie updated successfully"
    }

# ============================================================
# ✅ 5. DELETE MOVIE
# ============================================================

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):

    db = SessionLocal()

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    db.delete(movie)

    db.commit()

    return {
        "message": "Movie deleted successfully"
    }

# ============================================================
# ✅ 6. BOOK MOVIE TICKET
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
            detail="Not enough seats available"
        )

    total_amount = booking.tickets * movie.ticket_price

    new_booking = BookingDB(

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
# ✅ 7. CANCEL TICKET
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

    # Restore seats
    movie.available_seats += booking.tickets

    # Delete booking
    db.delete(booking)

    db.commit()

    return {
        "message": "Ticket cancelled successfully"
    }

# ============================================================
# ✅ 8. GET AVAILABLE SHOWS
# ============================================================

@app.get("/available-shows")
def available_shows():

    db = SessionLocal()

    shows = db.query(MovieDB).filter(
        MovieDB.available_seats > 0
    ).all()

    return shows

# ============================================================
# ✅ 9. GET ALL BOOKINGS
# ============================================================

@app.get("/bookings")
def get_bookings():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()

    return bookings

# ============================================================
# ✅ 10. SEARCH MOVIE BY NAME
# ============================================================

@app.get("/search-movie/{name}")
def search_movie(name: str):

    db = SessionLocal()

    movies = db.query(MovieDB).filter(
        MovieDB.movie_name.ilike(f"%{name}%")
    ).all()

    if not movies:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movies