-- SQLite schema (local dev without MySQL)

CREATE TABLE users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username VARCHAR(50) NOT NULL UNIQUE,

    email VARCHAR(100) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



CREATE TABLE theaters (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    screen_number VARCHAR(50) NOT NULL,

    mall_name VARCHAR(150) NOT NULL,

    city VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (screen_number, mall_name, city)

);



CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    poster_url VARCHAR(255),
    duration INTEGER NOT NULL,
    genre VARCHAR(50),
    rating REAL DEFAULT 0.0,
    status VARCHAR(20) NOT NULL DEFAULT 'now_showing',
    format_type VARCHAR(20) NOT NULL DEFAULT '2D',
    dolby_cinema INTEGER NOT NULL DEFAULT 0,
    dolby_audio INTEGER NOT NULL DEFAULT 0,
    certification VARCHAR(20) NOT NULL DEFAULT 'UA16+',
    release_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movie_cast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    actor_name VARCHAR(120) NOT NULL,
    character_name VARCHAR(120),
    photo_url VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

CREATE TABLE showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,

    theater_id INTEGER NULL,

    theater VARCHAR(200) NOT NULL,

    language VARCHAR(50) NOT NULL DEFAULT 'Hindi',

    show_date DATE NOT NULL,

    show_time TEXT NOT NULL,

    price REAL NOT NULL,

    price_prime REAL NOT NULL DEFAULT 150.00,

    price_gold REAL NOT NULL DEFAULT 250.00,

    price_recliner REAL NOT NULL DEFAULT 450.00,

    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,

    FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE SET NULL

);



CREATE TABLE seats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    showtime_id INTEGER NOT NULL,

    row_label CHAR(1) NOT NULL,

    seat_number INTEGER NOT NULL,

    category TEXT NOT NULL DEFAULT 'gold',

    status TEXT DEFAULT 'available',

    UNIQUE (showtime_id, row_label, seat_number),

    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE

);



CREATE TABLE bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    showtime_id INTEGER NOT NULL,

    total_amount REAL NOT NULL,

    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status TEXT DEFAULT 'confirmed',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE

);



CREATE TABLE booking_seats (

    booking_id INTEGER NOT NULL,

    seat_id INTEGER NOT NULL,

    PRIMARY KEY (booking_id, seat_id),

    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,

    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE

);



CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'general',
    message TEXT NOT NULL,
    user_id INTEGER NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

INSERT INTO movies (title, description, poster_url, duration, genre, rating, status, format_type, dolby_cinema, dolby_audio, certification, release_date) VALUES
('Inception', 'A thief who steals corporate secrets through dream-sharing technology is offered a chance at redemption.', 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLF5jka.jpg', 148, 'Sci-Fi', 8.8, 'now_showing', '2D', 1, 1, 'UA16+', NULL),
('The Dark Knight', 'Batman must accept one of the greatest psychological tests to fight injustice.', 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg', 152, 'Action', 9.0, 'now_showing', '2D', 1, 1, 'UA16+', NULL),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 169, 'Sci-Fi', 8.6, 'now_showing', 'IMAX', 1, 1, 'UA', NULL),
('Avengers: Endgame', 'After the devastating events, the Avengers assemble once more to reverse Thanos actions.', 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', 181, 'Action', 8.4, 'now_showing', '2D', 0, 1, 'UA13+', NULL),
('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between two families.', 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1WAMztklWmI0jM.jpg', 132, 'Thriller', 8.5, 'coming_soon', '2D', 1, 1, 'UA16+', date('now', '+21 days'));



INSERT INTO theaters (screen_number, mall_name, city) VALUES

('Screen 1', 'PVR Forum Mall', 'Bangalore'),

('Screen 2', 'INOX Garuda Mall', 'Bangalore'),

('Screen 3', 'Cinepolis Nexus', 'Mumbai');



INSERT INTO showtimes (movie_id, theater_id, theater, language, show_date, show_time, price, price_prime, price_gold, price_recliner) VALUES

(1, 1, 'Screen 1 · PVR Forum Mall · Bangalore', 'Hindi', date('now', '+1 day'), '10:00:00', 250, 150, 250, 450),

(1, 1, 'Screen 1 · PVR Forum Mall · Bangalore', 'English', date('now', '+1 day'), '14:30:00', 250, 150, 250, 450),

(1, 2, 'Screen 2 · INOX Garuda Mall · Bangalore', 'Tamil', date('now', '+1 day'), '18:00:00', 300, 150, 300, 500),

(2, 1, 'Screen 1 · PVR Forum Mall · Bangalore', 'English', date('now', '+1 day'), '20:30:00', 300, 150, 300, 500),

(2, 2, 'Screen 2 · INOX Garuda Mall · Bangalore', 'Hindi', date('now', '+2 day'), '11:00:00', 250, 150, 250, 450),

(3, 1, 'Screen 1 · PVR Forum Mall · Bangalore', 'English', date('now', '+2 day'), '15:00:00', 250, 150, 250, 450),

(4, 3, 'Screen 3 · Cinepolis Nexus · Mumbai', 'Hindi', date('now', '+2 day'), '19:00:00', 300, 150, 300, 500),

(5, 2, 'Screen 2 · INOX Garuda Mall · Bangalore', 'English', date('now', '+3 day'), '13:00:00', 250, 150, 250, 450);

