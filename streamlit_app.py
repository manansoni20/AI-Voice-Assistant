import streamlit as st

from audio.recorder import record_audio
from speech.deepgram_stt import transcribe_audio
from llm.openai_client import get_response
from tts.elevenlabs_tts import speak


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
)


# ---------------- CSS ----------------

def load_css():
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# ---------------- SESSION ----------------

if "history" not in st.session_state:
    st.session_state.history = []

if "status" not in st.session_state:
    st.session_state.status = "🟢 Ready"

if "messages" not in st.session_state:
    st.session_state.messages = 0


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("# ⚙️ AI Status")

    st.success("🎤 Recorder Ready")
    st.success("📝 Deepgram Connected")
    st.success("🤖 Gemini Connected")
    st.success("🔊 ElevenLabs Ready")

    st.divider()

    st.metric(
        "💬 Conversations",
        len(st.session_state.history) // 2
    )

    st.metric(
        "🟢 Status",
        st.session_state.status
    )

    st.metric(
        "⚡ Model",
        "Gemini 3.5 Flash"
    )

    st.metric(
        "🎤 Voice",
        "ElevenLabs"
    )


# ---------------- HERO ----------------

st.markdown("""

<div class="hero">

<div style="display:flex;align-items:center;gap:35px;">

<div class="mic-circle">

🎤

</div>

<div>

<div class="hero-title">

AI Voice Assistant

</div>

<div class="hero-sub">

Speak naturally. Think intelligently.

</div>

<div style="margin-top:20px;font-size:20px;color:#d7d7d7;">
Powered by <b>Deepgram</b> • <b>Gemini</b> • <b>ElevenLabs</b>
</div>

""", unsafe_allow_html=True)


# ---------------- STATUS ----------------

st.success(st.session_state.status)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------- LAYOUT ----------------

left, right = st.columns([0.9, 2.6], gap="large")

# ===========================
# LEFT PANEL
# ===========================

with left:

    st.markdown("""

<div class="glass-card">

<h2>

🎤 Voice Input

</h2>

<p>

Click the button below and start speaking.

</p>

</div>

""", unsafe_allow_html=True)

    if st.button(
        "🎙️ Start Voice Conversation",
        use_container_width=True
    ):

        st.session_state.status = "🎤 Listening..."

        with st.spinner("Listening..."):

            record_audio()

        st.session_state.status = "📝 Transcribing..."

        with st.spinner("Deepgram is transcribing..."):

            transcript = transcribe_audio()

        if transcript:

            st.session_state.history.append(
                ("You", transcript)
            )

            st.session_state.messages += 1

            st.session_state.status = "🤖 Gemini Thinking..."

            with st.spinner("Gemini is thinking..."):

                response = get_response(
                    transcript
                )

            st.session_state.history.append(
                ("Assistant", response)
            )

            st.session_state.messages += 1

            st.session_state.status = "🔊 Speaking..."

            with st.spinner("Generating voice..."):

                speak(response)

            st.session_state.status = "🟢 Ready"

        else:

            st.error(
                "No speech detected."
            )

            st.session_state.status = "🟢 Ready"
            st.rerun()

            # ===========================
# RIGHT PANEL
# ===========================

with right:

    st.markdown("""
    <div class="glass-card">
    <h2>💬 Recent Conversation</h2>
    """, unsafe_allow_html=True)

    chat_container = st.container(height=540)

    with chat_container:

        if len(st.session_state.history) == 0:

            st.info(
                "👋 Welcome!\n\nClick **Start Voice Conversation** and begin speaking."
            )

        else:

            for speaker, message in st.session_state.history:

                if speaker == "You":

                    with st.chat_message(
                        "user",
                        avatar="🧑"
                    ):
                        st.markdown(message)

                else:

                    with st.chat_message(
                        "assistant",
                        avatar="🤖"
                    ):
                        st.markdown(message)

    st.markdown("</div>", unsafe_allow_html=True)


# ===========================
# BOTTOM ACTIONS
# ===========================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.history = []
        st.session_state.messages = 0
        st.session_state.status = "🟢 Ready"

        st.rerun()

with col2:

    chat = ""

    for speaker, message in st.session_state.history:

        chat += f"{speaker}: {message}\n\n"

    st.download_button(
        label="📄 Download Chat",
        data=chat,
        file_name="conversation.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ===========================
# QUICK STATS
# ===========================

st.markdown("<br>", unsafe_allow_html=True)

a, b, c = st.columns(3)

with a:
    st.metric(
        "Messages",
        len(st.session_state.history)
    )

with b:
    st.metric(
        "Assistant",
        "Online"
    )

with c:
    st.metric(
        "Voice",
        "Ready"
    )


# ===========================
# FOOTER
# ===========================

# ===========================
# FOOTER
# ===========================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

<h3>🚀 AI Voice Assistant</h3>

<p>Real-Time AI Voice Assistant</p>

<p>
Powered by
<b>Deepgram</b> •
<b>Gemini</b> •
<b>ElevenLabs</b> •
<b>Streamlit</b>
</p>

<p style="opacity:0.7;">
Version 1.0
</p>

</div>
""", unsafe_allow_html=True)