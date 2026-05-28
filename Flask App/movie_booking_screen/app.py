import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from functools import wraps
from config import Config

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-SQLAlchemy extension
db = SQLAlchemy(app)

# ==========================================
# DATABASE MODELS
# ==========================================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    poster_url = db.Column(db.String(255))
    duration_minutes = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50))
    rating = db.Column(db.String(10))
    rating_score = db.Column(db.Float, default=4.5)
    release_date = db.Column(db.Date)

class Screen(db.Model):
    __tablename__ = 'screens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_rows = db.Column(db.Integer, nullable=False)
    total_cols = db.Column(db.Integer, nullable=False)

class Seat(db.Model):
    __tablename__ = 'seats'
    id = db.Column(db.Integer, primary_key=True)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.id', ondelete='CASCADE'), nullable=False)
    row_name = db.Column(db.String(1), nullable=False)
    col_number = db.Column(db.Integer, nullable=False)
    seat_type = db.Column(db.String(20), default='Prime') # 'Prime', 'Gold', 'Recliner'

class Showtime(db.Model):
    __tablename__ = 'showtimes'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id', ondelete='CASCADE'), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='confirmed') # 'confirmed', 'cancelled'

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id', ondelete='CASCADE'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id', ondelete='CASCADE'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seats.id', ondelete='CASCADE'), nullable=False)


# ==========================================
# AUTHENTICATION DECORATORS
# ==========================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# PUBLIC PAGES ROUTES
# ==========================================

@app.route('/')
def welcome():
    """Welcome Landing Page."""
    return render_template('welcome.html')

@app.route('/movies')
def index():
    """Homepage: lists all movies now showing."""
    movies = Movie.query.order_by(Movie.release_date.desc()).all()
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    """Movie details and dynamically grouped showtimes for the next 5 days."""
    movie = Movie.query.get_or_404(movie_id)
    
    # Generate next 5 dates starting from today
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dates = []
    for i in range(5):
        day = today + timedelta(days=i)
        date_key = day.strftime('%Y-%m-%d')
        label_day = day.strftime('%A') if i > 0 else 'Today'
        label_date = day.strftime('%b %d')
        dates.append((date_key, label_day, label_date))
    
    # Query showtimes starting from now, up to 5 days in the future
    future_limit = today + timedelta(days=5)
    showtimes_raw = db.session.execute(
        text("""
            SELECT s.id, s.start_time, s.ticket_price, s.screen_id, sc.name AS screen_name
            FROM showtimes s
            JOIN screens sc ON s.screen_id = sc.id
            WHERE s.movie_id = :movie_id 
              AND s.start_time >= :now 
              AND s.start_time < :future_limit
            ORDER BY s.start_time ASC
        """),
        {"movie_id": movie_id, "now": datetime.now(), "future_limit": future_limit}
    ).fetchall()
    
    # Group showtimes by YYYY-MM-DD
    showtimes_by_date = {date[0]: [] for date in dates}
    for row in showtimes_raw:
        st_date_str = row.start_time.strftime('%Y-%m-%d')
        if st_date_str in showtimes_by_date:
            showtimes_by_date[st_date_str].append(row)
            
    return render_template('movie_details.html', movie=movie, dates=dates, showtimes_by_date=showtimes_by_date)

# ==========================================
# USER BOOKING WORKFLOW ROUTES
# ==========================================

@app.route('/book/<int:showtime_id>', methods=['GET', 'POST'])
@login_required
def book_seats(showtime_id):
    """Allows selecting seats on the screen layout and executes ticket bookings."""
    # Retrieve showtime information
    showtime = db.session.execute(
        text("""
            SELECT s.id, s.start_time, s.ticket_price, s.movie_id, m.title AS movie_title, 
                   s.screen_id, sc.name AS screen_name, sc.total_rows, sc.total_cols
            FROM showtimes s
            JOIN movies m ON s.movie_id = m.id
            JOIN screens sc ON s.screen_id = sc.id
            WHERE s.id = :showtime_id
        """),
        {"showtime_id": showtime_id}
    ).fetchone()
    
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        # Process Booking Request
        seat_ids_raw = request.form.get('seat_ids')
        if not seat_ids_raw:
            flash('No seats selected. Please choose seats to complete your booking.', 'error')
            return redirect(url_for('book_seats', showtime_id=showtime_id))
            
        seat_ids = [int(sid) for sid in seat_ids_raw.split(',') if sid.strip()]
        
        # Start transaction to prevent race conditions
        try:
            # 1. Double check seat availability for this showtime
            already_booked = db.session.execute(
                text("""
                    SELECT seat_id FROM tickets 
                    WHERE showtime_id = :showtime_id AND seat_id IN :seat_ids
                """),
                {"showtime_id": showtime_id, "seat_ids": tuple(seat_ids)}
            ).fetchall()
            
            if already_booked:
                flash('Some of your selected seats were already booked by another customer. Please choose other seats.', 'error')
                return redirect(url_for('book_seats', showtime_id=showtime_id))
                
            # 2. Fetch seats details to calculate pricing
            seats_details = db.session.execute(
                text("SELECT id, seat_type FROM seats WHERE id IN :seat_ids"),
                {"seat_ids": tuple(seat_ids)}
            ).fetchall()
            
            # Base price details
            base_price = float(showtime.ticket_price)
            service_fee = 15.00
            subtotal = 0.0
            
            for seat in seats_details:
                if seat.seat_type == 'Gold':
                    subtotal += base_price + 4.00
                elif seat.seat_type == 'Recliner':
                    subtotal += base_price + 8.00
                else:
                    subtotal += base_price
            
            total_amount = subtotal + (len(seat_ids) * service_fee)
            
            # 3. Create Booking Header
            result = db.session.execute(
                text("""
                    INSERT INTO bookings (user_id, showtime_id, total_amount, status) 
                    VALUES (:user_id, :showtime_id, :total, 'confirmed')
                """),
                {
                    "user_id": session['user_id'],
                    "showtime_id": showtime_id,
                    "total": total_amount
                }
            )
            booking_id = result.lastrowid
            
            # 4. Insert Tickets (Booked seats)
            for sid in seat_ids:
                db.session.execute(
                    text("INSERT INTO tickets (booking_id, showtime_id, seat_id) VALUES (:bid, :sid, :seat_id)"),
                    {"bid": booking_id, "sid": showtime_id, "seat_id": sid}
                )
                
            db.session.commit()
            flash('Booking confirmed successfully!', 'success')
            return redirect(url_for('confirmation', booking_id=booking_id))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Booking transaction failed: {e}")
            flash('An error occurred while placing your booking. Please try again.', 'error')
            return redirect(url_for('book_seats', showtime_id=showtime_id))
            
    # GET Request: Fetch seats map configuration
    all_seats = db.session.execute(
        text("SELECT id, row_name, col_number, seat_type FROM seats WHERE screen_id = :screen_id ORDER BY row_name, col_number"),
        {"screen_id": showtime.screen_id}
    ).fetchall()
    
    # Group seats by row for template rendering
    seats_by_row = {}
    for seat in all_seats:
        if seat.row_name not in seats_by_row:
            seats_by_row[seat.row_name] = []
        seats_by_row[seat.row_name].append(seat)
        
    # Get list of already booked seat IDs for this showtime
    booked_seats_raw = db.session.execute(
        text("SELECT seat_id FROM tickets WHERE showtime_id = :showtime_id"),
        {"showtime_id": showtime_id}
    ).fetchall()
    booked_seat_ids = {row.seat_id for row in booked_seats_raw}
    
    return render_template(
        'book_seats.html', 
        showtime=showtime, 
        seats_by_row=seats_by_row, 
        booked_seat_ids=booked_seat_ids
    )

@app.route('/booking-confirmation/<int:booking_id>')
@login_required
def confirmation(booking_id):
    """Invoice / receipt checkout stub view."""
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure this booking belongs to the current user
    if booking.user_id != session['user_id']:
        flash('Unauthorized booking query.', 'error')
        return redirect(url_for('index'))
        
    showtime = db.session.execute(
        text("SELECT s.id, s.start_time, s.movie_id, s.screen_id FROM showtimes s WHERE s.id = :sid"),
        {"sid": booking.showtime_id}
    ).fetchone()
    
    movie = Movie.query.get(showtime.movie_id)
    screen = Screen.query.get(showtime.screen_id)
    
    # Fetch seats details for this booking
    tickets = db.session.execute(
        text("""
            SELECT t.seat_id, s.row_name, s.col_number 
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            WHERE t.booking_id = :bid
        """),
        {"bid": booking.id}
    ).fetchall()
    
    return render_template('confirmation.html', booking=booking, showtime=showtime, movie=movie, screen=screen, tickets=tickets)

# ==========================================
# USER PROFILE & DASHBOARD ROUTES
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User profile overview showing booking reservations history."""
    user = db.session.get(User, session['user_id'])
    
    # Fetch user's bookings joined with movie details
    bookings_raw = db.session.execute(
        text("""
            SELECT b.id, b.booking_time, b.total_amount, b.status, s.start_time, 
                   m.title AS movie_title, m.poster_url, sc.name AS screen_name,
                   GROUP_CONCAT(CONCAT(se.row_name, se.col_number)) AS seats_csv
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN movies m ON s.movie_id = m.id
            JOIN screens sc ON s.screen_id = sc.id
            JOIN tickets t ON t.booking_id = b.id
            JOIN seats se ON t.seat_id = se.id
            WHERE b.user_id = :user_id
            GROUP BY b.id
            ORDER BY b.booking_time DESC
        """),
        {"user_id": session['user_id']}
    ).fetchall()
    
    return render_template('dashboard.html', email=user.email, bookings=bookings_raw, current_time=datetime.now())

@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancels booking: frees up seats and updates status."""
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check
    if booking.user_id != session['user_id']:
        flash('Unauthorized booking query.', 'error')
        return redirect(url_for('dashboard'))
        
    showtime = Showtime.query.get(booking.showtime_id)
    if showtime.start_time <= datetime.now():
        flash('Cannot cancel bookings for shows that have already started or passed.', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        # Update status
        booking.status = 'cancelled'
        
        # Free up the seats from the tickets table (so they can be booked by others)
        db.session.execute(
            text("DELETE FROM tickets WHERE booking_id = :bid"),
            {"bid": booking.id}
        )
        
        db.session.commit()
        flash('Booking cancelled successfully. The refund process was initiated.', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Cancellation failed: {e}")
        flash('An error occurred during cancellation. Please try again.', 'error')
        
    return redirect(url_for('dashboard'))

# ==========================================
# AUTHENTICATION ROUTING SYSTEM
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allows signing up new users."""
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        
        # Validate unique username/email
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username is already taken. Please choose another.', 'error')
            return redirect(url_for('register'))
            
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email is already registered.', 'error')
            return redirect(url_for('register'))
            
        # Create User
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, role='user')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles logging in users and administrators."""
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # Register session variables
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs out and invalidates user session."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

# ==========================================
# ADMINISTRATIVE CONTROL PANEL ROUTES
# ==========================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin Dashboard Home: lists metrics and ticketing transaction history."""
    # Compute Analytics Metrics
    total_rev = db.session.execute(
        text("SELECT COALESCE(SUM(total_amount), 0) AS total FROM bookings WHERE status = 'confirmed'")
    ).fetchone().total
    
    tix_count = db.session.execute(
        text("SELECT COUNT(t.id) AS count FROM tickets t JOIN bookings b ON t.booking_id = b.id WHERE b.status = 'confirmed'")
    ).fetchone().count
    
    movies_count = Movie.query.count()
    bookings_count = Booking.query.count()
    
    metrics = {
        "total_revenue": float(total_rev),
        "tickets_sold": tix_count,
        "total_movies": movies_count,
        "total_bookings": bookings_count
    }
    
    # Query bookings history
    bookings_list = db.session.execute(
        text("""
            SELECT b.id, u.username, m.title AS movie_title, s.start_time, b.total_amount, b.status,
                   GROUP_CONCAT(CONCAT(se.row_name, se.col_number)) AS seats_csv
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN showtimes s ON b.showtime_id = s.id
            JOIN movies m ON s.movie_id = m.id
            JOIN tickets t ON t.booking_id = b.id
            JOIN seats se ON t.seat_id = se.id
            GROUP BY b.id
            ORDER BY b.booking_time DESC
        """)
    ).fetchall()
    
    screens = Screen.query.all()
    
    return render_template('admin/dashboard.html', metrics=metrics, bookings=bookings_list, screens=screens)

@app.route('/admin/movies')
@admin_required
def admin_movies():
    """Admin Page: lists active movies."""
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('admin/movies.html', movies=movies)

@app.route('/admin/movies/add', methods=['POST'])
@admin_required
def add_movie():
    """Admin Action: schedules new movies in database."""
    title = request.form['title'].strip()
    description = request.form['description'].strip()
    genre = request.form['genre'].strip()
    duration = int(request.form['duration'])
    rating = request.form['rating']
    rel_date_str = request.form['release_date']
    poster_url = request.form['poster_url'].strip() or None
    
    release_date = datetime.strptime(rel_date_str, '%Y-%m-%d').date()
    
    new_movie = Movie(
        title=title, description=description, genre=genre, 
        duration_minutes=duration, rating=rating, release_date=release_date,
        poster_url=poster_url
    )
    db.session.add(new_movie)
    db.session.commit()
    flash(f"Movie '{title}' was added successfully.", 'success')
    return redirect(url_for('admin_movies'))

@app.route('/admin/movies/delete/<int:movie_id>', methods=['POST'])
@admin_required
def delete_movie(movie_id):
    """Admin Action: removes a movie from the catalog."""
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash(f"Movie '{movie.title}' was deleted successfully.", 'success')
    return redirect(url_for('admin_movies'))

@app.route('/admin/showtimes')
@admin_required
def admin_showtimes():
    """Admin Page: manages showtimes scheduler."""
    showtimes = db.session.execute(
        text("""
            SELECT s.id, s.start_time, s.ticket_price, m.title AS movie_title, sc.name AS screen_name
            FROM showtimes s
            JOIN movies m ON s.movie_id = m.id
            JOIN screens sc ON s.screen_id = sc.id
            ORDER BY s.start_time DESC
        """)
    ).fetchall()
    
    movies = Movie.query.order_by(Movie.title).all()
    screens = Screen.query.order_by(Screen.name).all()
    
    return render_template('admin/showtimes.html', showtimes=showtimes, movies=movies, screens=screens)

@app.route('/admin/showtimes/add', methods=['POST'])
@admin_required
def add_showtime():
    """Admin Action: Schedules a movie showtime slot."""
    movie_id = int(request.form['movie_id'])
    screen_id = int(request.form['screen_id'])
    start_time_str = request.form['start_time']
    ticket_price = float(request.form['ticket_price'])
    
    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
    
    new_showtime = Showtime(
        movie_id=movie_id, screen_id=screen_id, 
        start_time=start_time, ticket_price=ticket_price
    )
    db.session.add(new_showtime)
    db.session.commit()
    flash('New showtime was scheduled successfully.', 'success')
    return redirect(url_for('admin_showtimes'))

@app.route('/admin/showtimes/delete/<int:showtime_id>', methods=['POST'])
@admin_required
def delete_showtime(showtime_id):
    """Admin Action: Cancels a showtime and clears tickets."""
    showtime = Showtime.query.get_or_404(showtime_id)
    db.session.delete(showtime)
    db.session.commit()
    flash('Showtime was deleted successfully.', 'success')
    return redirect(url_for('admin_showtimes'))

@app.route('/admin/screens')
@admin_required
def admin_screens():
    """Admin Page: lists active screens (theaters)."""
    screens = Screen.query.order_by(Screen.name).all()
    return render_template('admin/screens.html', screens=screens)

@app.route('/admin/screens/add', methods=['POST'])
@admin_required
def add_screen():
    """Admin Action: schedules new screens/theaters in database and auto-populates seats."""
    name = request.form['name'].strip()
    rows = int(request.form['total_rows'])
    cols = int(request.form['total_cols'])
    
    # Create Screen
    new_screen = Screen(name=name, total_rows=rows, total_cols=cols)
    db.session.add(new_screen)
    db.session.commit()
    screen_id = new_screen.id
    
    # Auto generate seats (Prime, Gold, Recliner)
    import string
    for r_idx in range(rows):
        row_name = string.ascii_uppercase[r_idx] if r_idx < 26 else 'Z'
        
        # Define tier boundaries: 30% Prime, 40% Gold, 30% Recliner
        prime_limit = max(1, int(rows * 0.3))
        recliner_limit = rows - max(1, int(rows * 0.3))
        
        if r_idx < prime_limit:
            seat_type = 'Prime'
        elif r_idx >= recliner_limit:
            seat_type = 'Recliner'
        else:
            seat_type = 'Gold'
            
        for c in range(1, cols + 1):
            db.session.execute(
                text("INSERT INTO seats (screen_id, row_name, col_number, seat_type) VALUES (:sid, :row, :col, :stype)"),
                {"sid": screen_id, "row": row_name, "col": c, "stype": seat_type}
            )
            
    db.session.commit()
    flash(f"Theater hall '{name}' was added successfully with {rows * cols} seats generated.", 'success')
    return redirect(url_for('admin_screens'))

@app.route('/admin/screens/delete/<int:screen_id>', methods=['POST'])
@admin_required
def delete_screen(screen_id):
    """Admin Action: removes a theater screen hall and associated seats."""
    screen = Screen.query.get_or_404(screen_id)
    db.session.delete(screen)
    db.session.commit()
    flash(f"Theater '{screen.name}' was deleted successfully.", 'success')
    return redirect(url_for('admin_screens'))

# ==========================================
# APPLICATION LAUNCHER
# ==========================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Auto-seed default user/admin accounts if database is empty
        if User.query.count() == 0:
            print("Auto-seeding default admin and user accounts...")
            admin_pwd = generate_password_hash("admin123")
            user_pwd = generate_password_hash("user123")
            admin = User(username="admin", email="admin@cinema.com", password_hash=admin_pwd, role="admin")
            user = User(username="user", email="user@gmail.com", password_hash=user_pwd, role="user")
            db.session.add_all([admin, user])
            db.session.commit()
            print("Admin (admin/admin123) and User (user/user123) seeded.")
            
        # Auto-seed screens and seats if none exist
        if Screen.query.count() == 0:
            print("Auto-seeding default theaters (screens)...")
            screen1 = Screen(name="IMAX Grand Theater", total_rows=8, total_cols=12)
            screen2 = Screen(name="Dolby Atmos Lounge", total_rows=6, total_cols=10)
            db.session.add_all([screen1, screen2])
            db.session.commit()
            
            # Generate seats for Screen 1 (IMAX)
            import string
            for r_idx, row in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
                if row in ['A', 'B']:
                    seat_type = 'Prime'
                elif row in ['C', 'D', 'E', 'F']:
                    seat_type = 'Gold'
                else:
                    seat_type = 'Recliner'
                for col in range(1, 13):
                    db.session.execute(
                        text("INSERT INTO seats (screen_id, row_name, col_number, seat_type) VALUES (:sid, :row, :col, :stype)"),
                        {"sid": screen1.id, "row": row, "col": col, "stype": seat_type}
                    )
            
            # Generate seats for Screen 2 (Dolby)
            for r_idx, row in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
                if row in ['A', 'B']:
                    seat_type = 'Prime'
                elif row in ['C', 'D']:
                    seat_type = 'Gold'
                else:
                    seat_type = 'Recliner'
                for col in range(1, 11):
                    db.session.execute(
                        text("INSERT INTO seats (screen_id, row_name, col_number, seat_type) VALUES (:sid, :row, :col, :stype)"),
                        {"sid": screen2.id, "row": row, "col": col, "stype": seat_type}
                    )
            db.session.commit()
            print("Theaters and seats seeded successfully.")
            
    # Run the development server
    app.run(host='127.0.0.1', port=5000, debug=True)
