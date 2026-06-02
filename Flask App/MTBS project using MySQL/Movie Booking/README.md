# CineBook — Movie Ticket Booking System

A full-stack movie ticket booking application built with **Python Flask**, **MySQL**, **HTML**, **CSS**, and **JavaScript**.

## Features

- User registration and login (session-based auth with hashed passwords)
- Movie listing with posters, ratings, and genres
- Showtime selection per movie
- Interactive seat map (8 rows × 10 seats)
- Real-time seat booking with conflict handling
- Booking confirmation and booking history

## Project Structure

```
Movie Booking/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── db.py                  # MySQL connection helpers
├── utils.py               # Seat initialization utilities
├── schema.sql             # Database schema + sample data
├── requirements.txt
├── routes/
│   ├── auth.py            # Login, register, logout
│   ├── movies.py          # Movie listing and details
│   └── booking.py         # Seat selection and booking API
├── templates/             # Jinja2 HTML templates
├── static/
│   ├── css/style.css      # Responsive UI styles
│   └── js/                # main.js, booking.js
└── README.md
```

## Prerequisites

- Python 3.10+
- MySQL 8.0+ (or MariaDB)

## Setup

### 1. Create the database

```bash
mysql -u root -p < schema.sql
```

Or open MySQL Workbench and run the contents of `schema.sql`.

### 2. Configure environment (optional)

Copy `.env.example` to `.env` and set your MySQL credentials. By default, the app uses:

- Host: `localhost`
- User: `root`
- Password: *(empty)*
- Database: `movie_booking`

You can also set environment variables directly:

```powershell
$env:MYSQL_PASSWORD="your_password"
$env:SECRET_KEY="a-long-random-secret"
```

### 3. Install dependencies

```bash
cd "Movie Booking"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Usage Flow

1. **Register** a new account or **log in**
2. Browse **movies** on the home page
3. Click **Book Now** → choose a **showtime**
4. **Select seats** on the interactive map
5. Click **Confirm Booking** to complete your reservation
6. View tickets under **My Bookings**

## Database Schema

| Table          | Description                          |
|----------------|--------------------------------------|
| `users`        | Registered users                     |
| `movies`       | Movie catalog                        |
| `showtimes`    | Screening times and pricing          |
| `seats`        | Per-showtime seat inventory          |
| `bookings`     | User booking records                 |
| `booking_seats`| Seats linked to each booking         |

Seats are auto-generated (rows A–H, 1–10) the first time a showtime is opened.

## API Endpoints

| Method | Route                      | Description              |
|--------|----------------------------|--------------------------|
| GET    | `/`                        | Movie listing            |
| GET/POST | `/login`, `/register`    | Authentication           |
| GET    | `/movies/<id>`             | Movie detail + showtimes |
| GET    | `/book/<showtime_id>`      | Seat selection page      |
| GET    | `/api/seats/<showtime_id>` | Seat status JSON         |
| POST   | `/api/book`                | Create booking           |
| GET    | `/booking/<id>`            | Confirmation page        |
| GET    | `/my-bookings`             | User booking history     |

## License

MIT — free to use for learning and projects.
