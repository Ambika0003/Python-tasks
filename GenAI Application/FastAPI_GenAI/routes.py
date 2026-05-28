from fastapi import APIRouter
from pydantic import BaseModel

from config import client, MODEL_NAME

router = APIRouter()

# Request Body Model
class QuestionRequest(BaseModel):
    question: str


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


# Home Route
@router.get("/")
def home():

    return {
        "message": "FastAPI Gemini Running"
    }


# Ask Gemini Route
@router.post("/ask")
def ask_gemini(data: QuestionRequest):

    answer = stream_gemini_response(data.question)

    return {
        "question": data.question,
        "answer": answer
    }