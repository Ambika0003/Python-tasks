from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from db import execute_in_tx, query_all, query_one, transaction
from routes.auth import login_required
from utils import ensure_seats_for_showtime, theater_display_sql, tier_prices_from_showtime

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/book/<int:showtime_id>")
@login_required
def select_seats(showtime_id):
    showtime = query_one(
        f"""
        SELECT s.*, {theater_display_sql()},
               m.title AS movie_title, m.poster_url
        FROM showtimes s
        JOIN movies m ON m.id = s.movie_id
        LEFT JOIN theaters t ON t.id = s.theater_id
        WHERE s.id = %s
        """,
        (showtime_id,),
    )
    if not showtime:
        return render_template("404.html"), 404

    ensure_seats_for_showtime(showtime_id)
    seats = query_all(
        """
        SELECT id, row_label, seat_number, category, status
        FROM seats
        WHERE showtime_id = %s
        ORDER BY row_label, seat_number
        """,
        (showtime_id,),
    )
    prices = tier_prices_from_showtime(showtime)
    return render_template(
        "seats.html",
        showtime=showtime,
        seats=seats,
        tier_prices=prices,
    )


@booking_bp.route("/api/seats/<int:showtime_id>")
@login_required
def api_seats(showtime_id):
    ensure_seats_for_showtime(showtime_id)
    seats = query_all(
        """
        SELECT id, row_label, seat_number, category, status
        FROM seats WHERE showtime_id = %s
        ORDER BY row_label, seat_number
        """,
        (showtime_id,),
    )
    return jsonify(seats)


@booking_bp.route("/api/book", methods=["POST"])
@login_required
def api_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    showtime_id = data.get("showtime_id")
    seat_ids = data.get("seat_ids", [])

    if not showtime_id or not seat_ids:
        return jsonify({"error": "Showtime and seats are required"}), 400

    showtime = query_one(
        """
        SELECT id, price_prime, price_gold, price_recliner
        FROM showtimes WHERE id = %s
        """,
        (showtime_id,),
    )
    if not showtime:
        return jsonify({"error": "Showtime not found"}), 404

    prices = tier_prices_from_showtime(showtime)
    placeholders = ",".join(["%s"] * len(seat_ids))
    seats = query_all(
        f"""
        SELECT id, status, category
        FROM seats
        WHERE showtime_id = %s AND id IN ({placeholders})
        """,
        (showtime_id, *seat_ids),
    )

    if len(seats) != len(seat_ids):
        return jsonify({"error": "Some seats are invalid"}), 400

    if any(s["status"] == "booked" for s in seats):
        return jsonify({"error": "One or more seats are already booked"}), 409

    total = sum(prices[s["category"]] for s in seats)

    try:
        with transaction() as db:
            cur = execute_in_tx(
                db,
                "INSERT INTO bookings (user_id, showtime_id, total_amount) VALUES (%s, %s, %s)",
                (session["user_id"], showtime_id, total),
            )
            booking_id = cur.lastrowid

            for seat in seats:
                cur = execute_in_tx(
                    db,
                    "UPDATE seats SET status = 'booked' WHERE id = %s AND status = 'available'",
                    (seat["id"],),
                )
                if cur.rowcount == 0:
                    db.rollback()
                    return jsonify({"error": "Seat no longer available"}), 409
                execute_in_tx(
                    db,
                    "INSERT INTO booking_seats (booking_id, seat_id) VALUES (%s, %s)",
                    (booking_id, seat["id"]),
                )
    except Exception:
        raise

    return jsonify({
        "booking_id": booking_id,
        "redirect": url_for("booking.confirmation", booking_id=booking_id),
    })


@booking_bp.route("/booking/<int:booking_id>")
@login_required
def confirmation(booking_id):
    booking = query_one(
        f"""
        SELECT b.*, s.show_date, s.show_time, s.language,
               {theater_display_sql()},
               m.id AS movie_id, m.title AS movie_title, m.poster_url, m.duration
        FROM bookings b
        JOIN showtimes s ON s.id = b.showtime_id
        JOIN movies m ON m.id = s.movie_id
        LEFT JOIN theaters t ON t.id = s.theater_id
        WHERE b.id = %s AND b.user_id = %s
        """,
        (booking_id, session["user_id"]),
    )
    if not booking:
        return render_template("404.html"), 404

    seats = query_all(
        """
        SELECT st.row_label, st.seat_number, st.category
        FROM booking_seats bs
        JOIN seats st ON st.id = bs.seat_id
        WHERE bs.booking_id = %s
        ORDER BY st.row_label, st.seat_number
        """,
        (booking_id,),
    )
    seat_labels = [f"{s['row_label']}{s['seat_number']}" for s in seats]
    return render_template(
        "confirmation.html",
        booking=booking,
        seat_labels=seat_labels,
        seats=seats,
    )


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = query_all(
        f"""
        SELECT b.id, b.total_amount, b.booking_date, b.status,
               m.title AS movie_title, s.show_date, s.show_time, s.language,
               {theater_display_sql()}
        FROM bookings b
        JOIN showtimes s ON s.id = b.showtime_id
        JOIN movies m ON m.id = s.movie_id
        LEFT JOIN theaters t ON t.id = s.theater_id
        WHERE b.user_id = %s
        ORDER BY b.booking_date DESC
        """,
        (session["user_id"],),
    )
    return render_template("my_bookings.html", bookings=bookings)


@booking_bp.route("/booking/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = query_one(
        """
        SELECT id, status, showtime_id
        FROM bookings
        WHERE id = %s AND user_id = %s
        """,
        (booking_id, session["user_id"]),
    )
    if not booking:
        flash("Booking not found.", "error")
        return redirect(url_for("booking.my_bookings"))

    if booking["status"] != "confirmed":
        flash("This ticket is already cancelled or cannot be cancelled.", "warning")
        return redirect(url_for("booking.my_bookings"))

    seat_rows = query_all(
        "SELECT seat_id FROM booking_seats WHERE booking_id = %s",
        (booking_id,),
    )
    if not seat_rows:
        flash("No seats found for this booking.", "error")
        return redirect(url_for("booking.my_bookings"))

    with transaction() as db:
        cur = execute_in_tx(
            db,
            "UPDATE bookings SET status = 'cancelled' WHERE id = %s AND status = 'confirmed'",
            (booking_id,),
        )
        if cur.rowcount == 0:
            db.rollback()
            flash("Could not cancel this booking.", "error")
            return redirect(url_for("booking.my_bookings"))

        for row in seat_rows:
            execute_in_tx(
                db,
                "UPDATE seats SET status = 'available' WHERE id = %s",
                (row["seat_id"],),
            )

    flash("Your ticket has been cancelled. Seats are available again.", "success")
    return redirect(url_for("booking.my_bookings"))
