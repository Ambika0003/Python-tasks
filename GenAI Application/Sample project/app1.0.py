# To run this code you need to install the following dependencies:
# pip install google-genai python-dotenv
 
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
 
load_dotenv()
 
def generate(question: str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
 
    model = "gemini-2.5-flash"
 
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=question,
    ):
        if text := chunk.text:
            print(text, end="")
 
if __name__ == "__main__":
    question = input("Enter your question: ")
    generate(question)