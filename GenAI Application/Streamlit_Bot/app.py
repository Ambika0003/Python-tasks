# ============================================================
# 🚀 Streamlit GPT Style Chat UI
# ============================================================

# Install Packages:
# pip install streamlit requests

import streamlit as st
import requests

# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="Gemini GPT Chat",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# FastAPI Backend URL
# ============================================================

FASTAPI_URL = "http://127.0.0.1:8000/ask"

# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp{
        background-color: #0f172a;
        color: white;
    }

    .title{
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        padding: 20px;
    }

    .user-msg{
        background-color: #2563eb;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        width: fit-content;
        max-width: 70%;
        margin-left: auto;
        color: white;
    }

    .bot-msg{
        background-color: #1e293b;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        width: fit-content;
        max-width: 70%;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Title
# ============================================================

st.markdown(
    '<div class="title">🤖 Gemini GPT Chat</div>',
    unsafe_allow_html=True
)

# ============================================================
# Display Messages
# ============================================================

for chat in st.session_state.messages:
    print(chat)
    if chat["role"] == "user":

        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-end;">
                <div class="user-msg">
                    👤  {chat['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-start;">
                <div class="bot-msg">
                    🤖 {chat['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# Chat Input
# ============================================================

question = st.chat_input(
    "Ask something...",
    disabled=st.session_state.processing
)

# ============================================================
# Process Question
# ============================================================

if question:

    # ========================================================
    # Disable Input
    # ========================================================

    st.session_state.processing = True

    # ========================================================
    # Add User Message
    # ========================================================

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # ========================================================
    # Rerun to Show User Message Instantly
    # ========================================================

    st.rerun()

# ============================================================
# Generate Response
# ============================================================

if st.session_state.processing:

    last_message = st.session_state.messages[-1]

    if last_message["role"] == "user":

        with st.spinner("Gemini is thinking..."):

            try:

                response = requests.post(
                    FASTAPI_URL,
                    json={
                        "question": last_message["content"]
                    }
                )

                data = response.json()

                answer = data.get(
                    "response",
                    "No response generated."
                )

            except Exception as e:

                answer = str(e)

        # ====================================================
        # Add Bot Response
        # ====================================================

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        # ====================================================
        # Enable Input
        # ====================================================

        st.session_state.processing = False

        st.rerun()
