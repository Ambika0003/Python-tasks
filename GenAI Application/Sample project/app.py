import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Chat Function
def generate_response(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )

    return response.text

# Main Program
if __name__ == "__main__":
    print("🤖 Gemini AI Chatbot")
    print("Type 'exit' to quit\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Chatbot Closed")
            break

        answer = generate_response(question)

        print("\nGemini:", answer)
        print()