import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================================
# Question Classifier
# ==========================================================

def is_python_related(question):

    prompt = f"""
    You are a strict classifier.

    Return ONLY YES or NO.

    Return YES only if the question is related to:

    - Python
    - Flask
    - FastAPI
    - APIs
    - Programming
    - Artificial Intelligence
    - Machine Learning
    - Data Science

    Return NO for:

    - Greetings
    - Personal conversation
    - Sports
    - Movies
    - Politics
    - Random text
    - Unrelated topics

    Examples:

    Question: What is Python?
    Answer: YES

    Question: Explain FastAPI
    Answer: YES

    Question: What is Machine Learning?
    Answer: YES

    Question: Hi
    Answer: NO

    Question: How are you?
    Answer: NO

    Question:
    {question}

    Answer:
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    answer = response.text.strip().upper()

    return answer == "YES"

# ==========================================================
# Generate Response
# ==========================================================

def generate(question):

    if not is_python_related(question):

        return """
⚠️ I am currently designed to answer only:

• Python
• Flask
• FastAPI
• APIs
• Programming
• AI / ML

Please ask a technical learning-related question.
"""

    system_prompt = """
You are an AI Learning Assistant.

Rules:

1. Answer only technical questions.
2. Be beginner friendly.
3. Explain concepts clearly.
4. Give examples whenever possible.
5. Format answers neatly.
6. Keep responses professional.
"""

    full_prompt = f"""
{system_prompt}

User Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text