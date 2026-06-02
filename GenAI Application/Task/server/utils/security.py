FORBIDDEN_KEYWORDS = [
    "add",
    "insert",
    "create",
    "update",
    "delete",
    "remove",
    "drop",
    "truncate",
    "alter"
]


def is_restricted_request(user_message):
    """
    Check if user is trying to modify data.
    """
    user_message = user_message.lower()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in user_message:
            return True

    return False


def get_restricted_response():
    """
    Professional response for restricted actions.
    """
    return (
        "I can assist with movie booking information, showtimes, "
        "theaters, and booking-related queries. "
        "However, I cannot perform create, update, delete, or "
        "administrative database operations."
    )