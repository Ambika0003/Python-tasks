from flask import request, jsonify, render_template
from config import client, MODEL_NAME

# Gemini Response Function
def stream_gemini_response(question: str):

    try:

        response_stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=question,
        )

        full_response = ""

        for chunk in response_stream:

            if chunk.text:
                full_response += chunk.text

        return full_response

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:
            return "Gemini quota exceeded. Try again later."

        elif "503" in error_message:
            return "Gemini server busy. Try again later."

        return f"Error: {error_message}"


def register_routes(app):

    # Frontend Page
    @app.route("/")
    def home():
        return render_template("index.html")


    # Ask Gemini API
    @app.route("/ask", methods=["POST"])
    def ask_gemini():

        data = request.get_json()

        question = data.get("question")

        answer = stream_gemini_response(question)

        return jsonify({
            "question": question,
            "answer": answer
        })