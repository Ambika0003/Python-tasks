from pydantic import BaseModel


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
    poster_url: str
    theater_location: str
    movie_format: str


class Booking(BaseModel):

    customer_name: str
    phone_number: str
    tickets: int
    seat_type: str
    selected_seats: list[str]