from flask import Blueprint, request, jsonify
from chatbot import MovieChatbot

chatbot_bp = Blueprint("chatbot", __name__)

bot = MovieChatbot()

@chatbot_bp.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    response = bot.process_message(user_message)

    return jsonify({
        "response": response
    })