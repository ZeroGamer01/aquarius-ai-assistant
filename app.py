
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Aquarius AI",
    page_icon="🌌",
    layout="wide"
)

# Aquarius design
st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
    color: white;
}
h1 {
    color: #8ab4ff;
}
[data-testid="stChatMessage"] {
    background-color: #151e35;
    border-radius: 14px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌌 Aquarius")
st.caption("Your Personal AI Assistant")

# Sidebar
with st.sidebar:
    st.title("🌌 Aquarius")
    st.write("Your AI workspace")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Powered by Gemini AI")

# Chat memory for current session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen
if not st.session_state.messages:
    st.markdown("## Hello! Welcome to Aquarius 👋")
    st.write("How can I help you today?")
    
    st.markdown("""
    - 💡 Ask me anything
    - ✍️ Write and create
    - 💻 Help with coding
    - 📚 Learn something new
    - 🔍 Research and analyse
    """)

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask Aquarius anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            history = [
                {
                    "role": m["role"],
                    "parts": [{"text": m["content"]}]
                }
                for m in st.session_state.messages
            ]

            with st.spinner("Aquarius is thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=history
                )

            answer = response.text or "I couldn't generate a response."
            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")
