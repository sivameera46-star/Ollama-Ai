import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

st.set_page_config(
    page_title="Nova AI",
    page_icon="✦",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #e0e7ff 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #dbeafe 0%, transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1050px;
    padding-top: 35px;
    padding-bottom: 100px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Chat message */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,0.15);
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 30px rgba(15,23,42,0.05);
    margin-bottom: 12px;
}

/* Chat input */
[data-testid="stChatInput"] > div {
    border-radius: 18px !important;
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 10px 35px rgba(15,23,42,0.10) !important;
}

/* Clear button */
.stButton button {
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    background: white;
}

</style>
""", unsafe_allow_html=True)


# ---------------- Session ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- Header ----------------

st.html("""
<div style="
    background:rgba(255,255,255,0.75);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.9);
    border-radius:24px;
    padding:22px 26px;
    margin-bottom:25px;
    box-shadow:0 15px 45px rgba(15,23,42,0.08);
">

<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
">

<div style="
    display:flex;
    align-items:center;
    gap:15px;
">

<div style="
    width:48px;
    height:48px;
    border-radius:15px;
    background:linear-gradient(135deg,#111827,#6366f1);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:23px;
    font-weight:700;
">
✦
</div>

<div>

<div style="
    font-size:23px;
    font-weight:700;
    color:#0f172a;
">
Nova AI
</div>

<div style="
    font-size:13px;
    color:#64748b;
    margin-top:3px;
">
Private local AI assistant
</div>

</div>
</div>

<div style="
    padding:8px 13px;
    border-radius:30px;
    background:#ecfdf5;
    color:#15803d;
    font-size:12px;
    font-weight:600;
">
● Ollama Online
</div>

</div>
</div>
""")


# ---------------- Welcome ----------------

if not st.session_state.messages:

    st.html("""
<div style="
    text-align:center;
    padding:70px 20px 45px;
">

<div style="
    font-size:45px;
    margin-bottom:18px;
">
✦
</div>

<div style="
    font-size:38px;
    font-weight:700;
    color:#0f172a;
    letter-spacing:-1px;
">
How can I help you?
</div>

<div style="
    margin-top:10px;
    font-size:15px;
    color:#64748b;
">
Ask anything. Your conversation runs locally through Ollama.
</div>

<div style="
    display:flex;
    justify-content:center;
    gap:12px;
    margin-top:35px;
    flex-wrap:wrap;
">

<div style="
    padding:12px 18px;
    border-radius:14px;
    background:white;
    border:1px solid #e2e8f0;
    color:#475569;
    font-size:13px;
">
⚡ Fast local AI
</div>

<div style="
    padding:12px 18px;
    border-radius:14px;
    background:white;
    border:1px solid #e2e8f0;
    color:#475569;
    font-size:13px;
">
🔒 Private
</div>

<div style="
    padding:12px 18px;
    border-radius:14px;
    background:white;
    border:1px solid #e2e8f0;
    color:#475569;
    font-size:13px;
">
✦ Llama 3.2 1B
</div>

</div>

</div>
""")


# ---------------- Chat History ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- Chat Input ----------------

prompt = st.chat_input("Ask Nova anything...")


if prompt:

    # User
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI
    with st.chat_message("assistant"):

        with st.spinner("Nova is thinking..."):

            try:

                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "messages": st.session_state.messages,
                        "stream": False
                    },
                    timeout=300
                )

                response.raise_for_status()

                result = response.json()

                answer = result["message"]["content"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.ConnectionError:

                st.error(
                    "Ollama is not running. "
                    "Please start Ollama and try again."
                )

            except Exception as e:

                st.error(f"Error: {e}")


# ---------------- Clear ----------------

if st.session_state.messages:

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Clear conversation"):

        st.session_state.messages = []

        st.rerun()
