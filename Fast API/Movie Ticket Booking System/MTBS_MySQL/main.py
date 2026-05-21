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
    Float,
    DateTime
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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
    screen_number = Column(Integer)
    show_time = Column(String(50))
    duration_minutes = Column(Integer)
    genre = Column(String(50))
    ticket_price = Column(Float)
    available_seats = Column(Integer)
    language = Column(String(50))
    rating = Column(Float)

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
    screen_number: int
    show_time: str
    duration_minutes: int
    genre: str
    ticket_price: float
    available_seats: int
    language: str
    rating: float


class Booking(BaseModel):

    customer_name: str
    phone_number: str
    tickets: int
    seat_type: str
    selected_seats: list[str]

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
        screen_number=movie.screen_number,
        show_time=movie.show_time,
        duration_minutes=movie.duration_minutes,
        genre=movie.genre,
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
    db.close()
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
    movie.screen_number = updated_movie.screen_number
    movie.show_time = updated_movie.show_time
    movie.duration_minutes = updated_movie.duration_minutes
    movie.genre = updated_movie.genre
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

    # Check movie exists
    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Check available seats
    if movie.available_seats < booking.tickets:

        raise HTTPException(
            status_code=400,
            detail="Not enough seats available"
        )

    # Check tickets count matches selected seats
    if booking.tickets != len(booking.selected_seats):

        raise HTTPException(
            status_code=400,
            detail="Tickets count and selected seats count must match"
        )

    # Base ticket price from movie
    ticket_price = movie.ticket_price

    # Seat type price increase
    if booking.seat_type == "Silver":
        final_ticket_price = ticket_price

    elif booking.seat_type == "Gold":
        final_ticket_price = ticket_price + 100

    elif booking.seat_type == "Platinum":
        final_ticket_price = ticket_price + 200

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid seat type"
        )

    # Calculate total amount
    total_amount = booking.tickets * final_ticket_price

    # Create booking
    new_booking = BookingDB(

        movie_id=movie.movie_id,

        customer_name=booking.customer_name,
        phone_number=booking.phone_number,

        tickets=booking.tickets,
        seat_type=booking.seat_type,
        selected_seats=",".join(booking.selected_seats),
        total_amount=total_amount,
        booking_status="Booked"
    )

    # Reduce available seats
    movie.available_seats -= booking.tickets

    # Save booking
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {

        "message": "Ticket booked successfully",
        "customer_name": booking.customer_name,
        "movie_name": movie.movie_name,
        "tickets_booked": booking.tickets,
        "seat_type": booking.seat_type,
        "selected_seats": booking.selected_seats,
        "price_per_ticket": final_ticket_price,
        "total_amount": total_amount,
        "remaining_seats": movie.available_seats,
        "booking_status": "Booked"
    }

    db.close()
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

    if booking.booking_status == "Cancelled":

        raise HTTPException(
            status_code=400,
            detail="Ticket already cancelled"
        )

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == booking.movie_id
    ).first()

    # Restore seats
    movie.available_seats += booking.tickets

    # Update booking status
    booking.booking_status = "Cancelled"

    db.commit()

    db.close()

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

# ============================================================
# ✅ 11. REVENUE
# ============================================================

@app.get("/total-revenue")
def total_revenue():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()

    revenue = sum(b.total_amount for b in bookings)

    return {
        "total_revenue": revenue
    }

# ============================================================
# ✅ 12. CUSTOMER BOOKING
# ============================================================

@app.get("/customer-bookings/{customer_name}")
def customer_bookings(customer_name: str):

    db = SessionLocal()

    bookings = db.query(BookingDB).filter(
        BookingDB.customer_name == customer_name
    ).all()

    return bookings

# ============================================================
# ✅ 13. TOP RATED MOVIES
# ============================================================

@app.get("/top-rated-movies")
def top_rated_movies():

    db = SessionLocal()

    movies = db.query(MovieDB).order_by(MovieDB.rating.desc()).all()

    db.close()

    return movies

# ============================================================
# ✅ 14. REMAINING SEATS
# ============================================================

@app.get("/remaining-seats/{movie_id}")
def remaining_seats(movie_id: int):

    db = SessionLocal()

    movie = db.query(MovieDB).filter(
        MovieDB.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {

        "movie_name": movie.movie_name,

        "remaining_seats": movie.available_seats
    }

# ============================================================
# ✅ 15. BOOKING SUMMARY
# ============================================================

@app.get("/booking-summary")
def booking_summary():

    db = SessionLocal()

    total_movies = db.query(MovieDB).count()

    total_bookings = db.query(BookingDB).count()

    return {

        "total_movies": total_movies,

        "total_bookings": total_bookings
    }

# ============================================================
# ✅ 16. ALL CUSTOMER BOOKING HISTORY
# ============================================================

@app.get("/all-booking-history")
def all_booking_history():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()
    movies = db.query(MovieDB).all()

    movie_map = {movie.movie_id: movie for movie in movies}

    history = []

    for booking in bookings:

        movie = movie_map.get(booking.movie_id)

        history.append({
            "booking_id": booking.booking_id,
            "customer_name": booking.customer_name,
            "movie_name": movie.movie_name,
            "theater_name": movie.theater_name,
            "tickets": booking.tickets,
            "seat_type": booking.seat_type,
            "total_amount": booking.total_amount,
            "booking_status": booking.booking_status,
            "booking_time": booking.booking_time
        })

    db.close()

    return history

# ============================================================
# ✅ 17. VIEW BOOKED SEATS
# ============================================================

@app.get("/booked-seats/{movie_id}")
def booked_seats(movie_id: int):

    db = SessionLocal()

    bookings = db.query(BookingDB).filter(
        BookingDB.movie_id == movie_id,
        BookingDB.booking_status == "Booked"
    ).all()

    seats = []

    for booking in bookings:

        booked = booking.selected_seats.split(",")

        seats.extend(booked)

    db.close()

    return {

        "movie_id": movie_id,

        "booked_seats": seats
    }


