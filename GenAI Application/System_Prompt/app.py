# ============================================================
# Install Packages:
# pip install google-genai python-dotenv
# ============================================================

import os
from google import genai
from dotenv import load_dotenv

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Check Question Relevance
# ============================================================

def is_python_related(question: str) -> bool:

    prompt = f"""
    You are a strict classifier.

    Return ONLY YES or NO.

    Return YES only if the question is clearly related to:
    - Python
    - Python Programming
    - FastAPI
    - Flask
    - AI/ML

    Return NO for:
    - Greetings
    - Random text
    - Gibberish
    - Unclear inputs
    - Personal conversation
    - Non-technical topics

    Examples:

    Question: What is a Python dictionary?
    Answer: YES

    Question: Explain FastAPI dependency injection
    Answer: YES

    Question: hi
    Answer: NO

    Question: defin java and its use cases or other programning languages
    Answer: NO

    Question:
    {question}

    Answer:
    """

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "temperature": 0
        }
    )

    answer = response.text.strip().upper()

    return answer == "YES"

# ============================================================
# Generate Response
# ============================================================

def generate(question: str):

    # Restrict Non-Technical Questions
    if not is_python_related(question):

        print(
            "\n⚠️ I'm currently designed to provide responses only for python platform-related learning queries.\n"
            "Please contact the administration team for further assistance.\n"
        )

        return

    # Gemini Client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"

    # System Prompt
    system_prompt = """
    You are an AI learning assistant.
    Respond to the user's question with clear, concise, and beginner-friendly explanations if the question is related to Python, programming, development, APIs, AI/ML, or technical concepts.

    Rules:
    - Respond only to valid learning/platform-related queries.
    - Be clear and beginner friendly.
    - If a question is unrelated, politely deny it.
    - Keep responses clean and structured.
    """

    full_prompt = f"""
    {system_prompt}

    User Question:
    {question}
    """

    # Streaming Response
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=full_prompt,
    ):
        if chunk.text:
            print(chunk.text, end="")

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    question = input("Enter your question: ")

    generate(question)