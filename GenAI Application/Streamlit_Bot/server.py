import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

# Gemini Client
client = genai.Client(api_key=api_key)

# Request Model
class ChatRequest(BaseModel):
    question: str

# API Endpoint
@app.post("/ask")
async def ask_gemini(request: ChatRequest):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.question
        )

        return {
            "response": response.text
        }

    except Exception as e:

        return {
            "response": f"Error: {str(e)}"
        }


@app.get("/")
def home():

    return {
        "message": "Gemini Chatbot Backend Running"
    }