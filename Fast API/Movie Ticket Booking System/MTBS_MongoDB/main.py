# ============================================================
# 🎬 Movie Ticket Booking System
# FastAPI + MongoDB Atlas + MongoEngine
# ============================================================

# Install Packages:
# pip install fastapi uvicorn mongoengine pymongo certifi

# Run Server:
# uvicorn main:app --reload

# Swagger UI:
# http://127.0.0.1:8000/docs

# ============================================================
# 📦 Imports
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongoengine import (
    connect,
    Document,
    IntField,
    StringField,
    FloatField
)

import certifi

# ============================================================
# 🚀 FastAPI App
# ============================================================

app = FastAPI()

# ============================================================
# 🌐 MongoDB Atlas Connection
# ============================================================

MONGO_URL = "mongodb+srv://smambika869_db_user:I7n2zwZWtnkw9ZpU@ambika.obcayra.mongodb.net/movie_booking_db?retryWrites=true&w=majority"

connect(
    host=MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)

# ============================================================
# 🧱 MongoDB Models
# ============================================================

class MovieDB(Document):

    movie_id = IntField(primary_key=True)
    movie_name = StringField(required=True)
    theater_name = StringField(required=True)
    show_time = StringField(required=True)
    ticket_price = FloatField(required=True)
    available_seats = IntField(required=True)
    language = StringField(required=True)
    rating = FloatField(required=True)
    meta = {
        "collection": "movies"
    }


class BookingDB(Document):

    booking_id = IntField(primary_key=True)
    movie_id = IntField(required=True)
    customer_name = StringField(required=True)
    tickets = IntField(required=True)
    total_amount = FloatField(required=True)
    booking_status = StringField(default="Booked")
    meta = {
        "collection": "bookings"
    }

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
        "message": "Movie Ticket Booking System Using MongoDB 🚀"
    }

# ============================================================
# ✅ 1. ADD MOVIE
# ============================================================

@app.post("/movies")
def add_movie(movie: Movie):

    existing_movie = MovieDB.objects(
        movie_id=movie.movie_id
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

    new_movie.save()

    return {
        "message": "Movie added successfully"
    }

# ============================================================
# ✅ 2. GET ALL MOVIES
# ============================================================

@app.get("/movies")
def get_movies():

    movies = MovieDB.objects()

    data = []

    for movie in movies:

        data.append({

            "movie_id": movie.movie_id,
            "movie_name": movie.movie_name,
            "theater_name": movie.theater_name,
            "show_time": movie.show_time,
            "ticket_price": movie.ticket_price,
            "available_seats": movie.available_seats,
            "language": movie.language,
            "rating": movie.rating
        })

    return data

# ============================================================
# ✅ 3. GET MOVIE BY ID
# ============================================================

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    movie = MovieDB.objects(
        movie_id=movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {

        "movie_id": movie.movie_id,
        "movie_name": movie.movie_name,
        "theater_name": movie.theater_name,
        "show_time": movie.show_time,
        "ticket_price": movie.ticket_price,
        "available_seats": movie.available_seats,
        "language": movie.language,
        "rating": movie.rating
    }

# ============================================================
# ✅ 4. UPDATE MOVIE
# ============================================================

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):

    movie = MovieDB.objects(
        movie_id=movie_id
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

    movie.save()

    return {
        "message": "Movie updated successfully"
    }

# ============================================================
# ✅ 5. DELETE MOVIE
# ============================================================

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):

    movie = MovieDB.objects(
        movie_id=movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    movie.delete()

    return {
        "message": "Movie deleted successfully"
    }

# ============================================================
# ✅ 6. BOOK MOVIE TICKET
# ============================================================

@app.post("/book-ticket/{movie_id}")
def book_ticket(movie_id: int, booking: Booking):

    movie = MovieDB.objects(
        movie_id=movie_id
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

        booking_id=booking.booking_id,
        movie_id=movie.movie_id,
        customer_name=booking.customer_name,
        tickets=booking.tickets,
        total_amount=total_amount,
        booking_status="Booked"
    )

    # Reduce seats
    movie.available_seats -= booking.tickets

    movie.save()

    new_booking.save()

    return {

        "message": "Ticket booked successfully",

        "total_amount": total_amount
    }

# ============================================================
# ✅ 7. CANCEL TICKET
# ============================================================

@app.post("/cancel-ticket/{booking_id}")
def cancel_ticket(booking_id: int):

    booking = BookingDB.objects(
        booking_id=booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    movie = MovieDB.objects(
        movie_id=booking.movie_id
    ).first()

    # Restore seats
    movie.available_seats += booking.tickets

    movie.save()

    # Delete booking
    booking.delete()

    return {
        "message": "Ticket cancelled successfully"
    }

# ============================================================
# ✅ 8. GET AVAILABLE SHOWS
# ============================================================

@app.get("/available-shows")
def available_shows():

    shows = MovieDB.objects(
        available_seats__gt=0
    )

    data = []

    for movie in shows:

        data.append({

            "movie_name": movie.movie_name,
            "theater_name": movie.theater_name,
            "show_time": movie.show_time,
            "available_seats": movie.available_seats
        })

    return data

# ============================================================
# ✅ 9. GET ALL BOOKINGS
# ============================================================

@app.get("/bookings")
def get_bookings():

    bookings = BookingDB.objects()

    data = []

    for booking in bookings:

        data.append({

            "booking_id": booking.booking_id,
            "movie_id": booking.movie_id,
            "customer_name": booking.customer_name,
            "tickets": booking.tickets,
            "total_amount": booking.total_amount,
            "booking_status": booking.booking_status
        })

    return data

# ============================================================
# ✅ 10. SEARCH MOVIE BY NAME
# ============================================================

@app.get("/search-movie/{name}")
def search_movie(name: str):

    movies = MovieDB.objects(
        movie_name__icontains=name
    )

    if not movies:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    data = []

    for movie in movies:

        data.append({

            "movie_id": movie.movie_id,
            "movie_name": movie.movie_name,
            "theater_name": movie.theater_name,
            "show_time": movie.show_time,
            "ticket_price": movie.ticket_price,
            "available_seats": movie.available_seats,
            "language": movie.language,
            "rating": movie.rating
        })

    return data