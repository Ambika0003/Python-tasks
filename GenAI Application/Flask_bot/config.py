import os
from dotenv import load_dotenv
from google import genai

# Load Environment Variables
load_dotenv()

# API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Gemini Client
client = genai.Client(api_key=api_key)

# Gemini Model
MODEL_NAME = "gemini-2.5-flash"