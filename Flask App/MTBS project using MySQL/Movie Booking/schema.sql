-- Movie Ticket Booking System - MySQL Schema
CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE theaters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    screen_number VARCHAR(50) NOT NULL,
    mall_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_screen (screen_number, mall_name, city)
);

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    poster_url VARCHAR(255),
    duration INT NOT NULL COMMENT 'Duration in minutes',
    genre VARCHAR(50),
    rating DECIMAL(2, 1) DEFAULT 0.0,
    status VARCHAR(20) NOT NULL DEFAULT 'now_showing',
    format_type VARCHAR(20) NOT NULL DEFAULT '2D',
    dolby_cinema TINYINT(1) NOT NULL DEFAULT 0,
    dolby_audio TINYINT(1) NOT NULL DEFAULT 0,
    certification VARCHAR(20) NOT NULL DEFAULT 'UA16+',
    release_date DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movie_cast (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    actor_name VARCHAR(120) NOT NULL,
    character_name VARCHAR(120) DEFAULT NULL,
    photo_url VARCHAR(500) DEFAULT NULL,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

CREATE TABLE showtimes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    theater_id INT NULL,
    theater VARCHAR(200) NOT NULL,
    language VARCHAR(50) NOT NULL DEFAULT 'Hindi',
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    price DECIMAL(8, 2) NOT NULL COMMENT 'Legacy; use tier prices',
    price_prime DECIMAL(8, 2) NOT NULL DEFAULT 150.00,
    price_gold DECIMAL(8, 2) NOT NULL DEFAULT 250.00,
    price_recliner DECIMAL(8, 2) NOT NULL DEFAULT 450.00,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE SET NULL
);

CREATE TABLE seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    showtime_id INT NOT NULL,
    row_label CHAR(1) NOT NULL,
    seat_number INT NOT NULL,
    category ENUM('prime', 'gold', 'recliner') NOT NULL DEFAULT 'gold',
    status ENUM('available', 'booked') DEFAULT 'available',
    UNIQUE KEY unique_seat (showtime_id, row_label, seat_number),
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('confirmed', 'cancelled') DEFAULT 'confirmed',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE
);

CREATE TABLE booking_seats (
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    PRIMARY KEY (booking_id, seat_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE
);

CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'general',
    message TEXT NOT NULL,
    user_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Sample movies
INSERT INTO movies (title, description, poster_url, duration, genre, rating) VALUES
('Inception', 'A thief who steals corporate secrets through dream-sharing technology is offered a chance at redemption.', 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLF5jka.jpg', 148, 'Sci-Fi', 8.8),
('The Dark Knight', 'Batman must accept one of the greatest psychological tests to fight injustice.', 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg', 152, 'Action', 9.0),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 169, 'Sci-Fi', 8.6),
('Avengers: Endgame', 'After the devastating events, the Avengers assemble once more to reverse Thanos actions.', 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', 181, 'Action', 8.4),
('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between two families.', 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1WAMztklWmI0jM.jpg', 132, 'Thriller', 8.5);

INSERT INTO theaters (name, location) VALUES
('Screen 1', 'Main Hall'),
('Screen 2', 'Main Hall'),
('Screen 3', 'Premium Wing');

-- Sample showtimes (next 7 days)
INSERT INTO showtimes (movie_id, theater_id, theater, show_date, show_time, price, price_prime, price_gold, price_recliner) VALUES
(1, 1, 'Screen 1', CURDATE() + INTERVAL 1 DAY, '10:00:00', 250, 150, 250, 450),
(1, 1, 'Screen 1', CURDATE() + INTERVAL 1 DAY, '14:30:00', 250, 150, 250, 450),
(1, 2, 'Screen 2', CURDATE() + INTERVAL 1 DAY, '18:00:00', 300, 150, 300, 500),
(2, 1, 'Screen 1', CURDATE() + INTERVAL 1 DAY, '20:30:00', 300, 150, 300, 500),
(2, 2, 'Screen 2', CURDATE() + INTERVAL 2 DAY, '11:00:00', 250, 150, 250, 450),
(3, 1, 'Screen 1', CURDATE() + INTERVAL 2 DAY, '15:00:00', 250, 150, 250, 450),
(4, 3, 'Screen 3', CURDATE() + INTERVAL 2 DAY, '19:00:00', 300, 150, 300, 500),
(5, 2, 'Screen 2', CURDATE() + INTERVAL 3 DAY, '13:00:00', 250, 150, 250, 450);
