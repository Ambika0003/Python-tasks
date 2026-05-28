from fastapi import FastAPI
from fastapi import HTTPException

from sql_db import engine
from sql_db import SessionLocal

from models import Base
from models import MovieDB
from models import BookingDB

from schemas import Movie
from schemas import Booking


app = FastAPI()

Base.metadata.create_all(bind=engine)


# ============================================================
# HOME ROUTE
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Movie Ticket Booking System Using MySQL 🚀"
    }


# ============================================================
# ADD MOVIE
# ============================================================

@app.post("/movies", tags=["Movies"])
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
        rating=movie.rating,
        poster_url=movie.poster_url,
        theater_location=movie.theater_location,
        movie_format=movie.movie_format
    )

    db.add(new_movie)

    db.commit()

    db.close()

    return {
        "message": "Movie added successfully"
    }


# ============================================================
# GET ALL MOVIES
# ============================================================

@app.get("/movies", tags=["Movies"])
def get_movies():

    db = SessionLocal()

    movies = db.query(MovieDB).all()

    db.close()

    return movies


# ============================================================
# GET MOVIE BY ID
# ============================================================

@app.get("/movies/{movie_id}", tags=["Movies"])
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

    db.close()

    return movie


# ============================================================
# UPDATE MOVIE
# ============================================================

@app.put("/movies/{movie_id}", tags=["Movies"])
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

    db.close()

    return {
        "message": "Movie updated successfully"
    }


# ============================================================
# DELETE MOVIE
# ============================================================

@app.delete("/movies/{movie_id}", tags=["Movies"])
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

    db.close()

    return {
        "message": "Movie deleted successfully"
    }


# ============================================================
# BOOK MOVIE TICKET
# ============================================================

@app.post("/book-ticket/{movie_id}", tags=["Bookings"])
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

    if booking.tickets != len(booking.selected_seats):

        raise HTTPException(
            status_code=400,
            detail="Tickets count and selected seats count must match"
        )

    ticket_price = movie.ticket_price

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

    total_amount = booking.tickets * final_ticket_price

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

    movie.available_seats -= booking.tickets

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    db.close()

    return {

        "message": "Ticket booked successfully",

        "booking_id": new_booking.booking_id,

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


# ============================================================
# CANCEL TICKET
# ============================================================

@app.post("/cancel-ticket/{booking_id}", tags=["Bookings"])
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

    movie.available_seats += booking.tickets

    booking.booking_status = "Cancelled"

    db.commit()

    db.close()

    return {
        "message": "Ticket cancelled successfully"
    }


# ============================================================
# GET BOOKINGS
# ============================================================

@app.get("/bookings", tags=["Bookings"])
def get_bookings():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()

    db.close()

    return bookings


# ============================================================
# SEARCH MOVIE
# ============================================================

@app.get("/search-movie/{name}", tags=["Movies"])
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

    db.close()

    return movies


# ============================================================
# TOTAL REVENUE
# ============================================================

@app.get("/total-revenue", tags=["Analytics"])
def total_revenue():

    db = SessionLocal()

    bookings = db.query(BookingDB).all()

    revenue = sum(b.total_amount for b in bookings)

    db.close()

    return {
        "total_revenue": revenue
    }


# ============================================================
# CUSTOMER BOOKINGS
# ============================================================

@app.get("/customer-bookings/{customer_name}", tags=["Bookings"])
def customer_bookings(customer_name: str):

    db = SessionLocal()

    bookings = db.query(BookingDB).filter(
        BookingDB.customer_name == customer_name
    ).all()

    db.close()

    return bookings


# ============================================================
# TOP RATED MOVIES
# ============================================================

@app.get("/top-rated-movies", tags=["Movies"])
def top_rated_movies():

    db = SessionLocal()

    movies = db.query(MovieDB).order_by(
        MovieDB.rating.desc()
    ).all()

    db.close()

    return movies


# ============================================================
# REMAINING SEATS
# ============================================================

@app.get("/remaining-seats/{movie_id}", tags=["Bookings"])
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

    db.close()

    return {

        "movie_name": movie.movie_name,

        "remaining_seats": movie.available_seats
    }


# ============================================================
# BOOKING SUMMARY
# ============================================================

@app.get("/booking-summary", tags=["Analytics"])
def booking_summary():

    db = SessionLocal()

    total_movies = db.query(MovieDB).count()

    total_bookings = db.query(BookingDB).count()

    db.close()

    return {

        "total_movies": total_movies,

        "total_bookings": total_bookings
    }


# ============================================================
# BOOKED SEATS
# ============================================================

@app.get("/booked-seats/{movie_id}", tags=["Bookings"])
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


# ============================================================
# MOVIES BY GENRE
# ============================================================

@app.get("/movies/genre/{genre}", tags=["Movies"])
def movies_by_genre(genre: str):

    db = SessionLocal()

    movies = db.query(MovieDB).filter(
        MovieDB.genre == genre
    ).all()

    db.close()

    return movies


# ============================================================
# MOVIES BY LANGUAGE
# ============================================================

@app.get("/movies/language/{language}", tags=["Movies"])
def movies_by_language(language: str):

    db = SessionLocal()

    movies = db.query(MovieDB).filter(
        MovieDB.language == language
    ).all()

    db.close()

    return movies


# ============================================================
# NOW SHOWING
# ============================================================

@app.get("/now-showing", tags=["Movies"])
def now_showing():

    db = SessionLocal()

    movies = db.query(MovieDB).filter(
        MovieDB.available_seats > 0
    ).all()

    db.close()

    return movies


# ============================================================
# BOOKING DETAILS
# ============================================================

@app.get("/booking/{booking_id}", tags=["Bookings"])
def booking_details(booking_id: int):

    db = SessionLocal()

    booking = db.query(BookingDB).filter(
        BookingDB.booking_id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    db.close()

    return booking


# ============================================================
# THEATER MOVIES
# ============================================================

@app.get("/theater/{theater_name}", tags=["Movies"])
def theater_movies(theater_name: str):

    db = SessionLocal()

    movies = db.query(MovieDB).filter(
        MovieDB.theater_name == theater_name
    ).all()

    db.close()

    return movies