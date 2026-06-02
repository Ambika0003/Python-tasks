from database import get_db_connection
from gemini import ask_gemini
from utils.security import (
    is_restricted_request,
    get_restricted_response
)


class MovieChatbot:

    def process_message(self, user_message):

        # Block dangerous requests
        if is_restricted_request(user_message):
            return get_restricted_response()

        message = user_message.lower()

        # Show movies
        if any(word in message for word in [
            "movies",
            "movie list",
            "available movies",
            "show movies"
        ]):
            return self.get_movies()

        # Show theaters
        if "theater" in message or "theatre" in message:
            return self.get_theaters()

        # Show timings
        if "showtime" in message or "timing" in message:
            return self.get_showtimes()

        # Otherwise ask Gemini
        return ask_gemini(
            f"""
            You are a Movie Booking AI Assistant.

            Only answer questions related to:
            - movies
            - theaters
            - showtimes
            - bookings

            User Question:
            {user_message}
            """
        )

    def get_movies(self):

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT title, genre, rating
                FROM movies
                LIMIT 10
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            if not rows:
                return "No movies found."

            response = "🎬 Available Movies:\n\n"

            for movie in rows:
                response += (
                    f"Title: {movie[0]}\n"
                    f"Genre: {movie[1]}\n"
                    f"Rating: {movie[2]}\n\n"
                )

            return response

        except Exception as e:
            return f"Database Error: {str(e)}"

    def get_theaters(self):

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, city
                FROM theaters
                LIMIT 10
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            if not rows:
                return "No theaters found."

            response = "🏢 Available Theaters:\n\n"

            for theater in rows:
                response += (
                    f"{theater[0]} - {theater[1]}\n"
                )

            return response

        except Exception as e:
            return f"Database Error: {str(e)}"

    def get_showtimes(self):

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT theater,
                       show_date,
                       show_time,
                       language
                FROM showtimes
                LIMIT 10
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            if not rows:
                return "No showtimes found."

            response = "🕒 Show Timings:\n\n"

            for row in rows:
                response += (
                    f"Theater: {row[0]}\n"
                    f"Date: {row[1]}\n"
                    f"Time: {row[2]}\n"
                    f"Language: {row[3]}\n\n"
                )

            return response

        except Exception as e:
            return f"Database Error: {str(e)}"