from taipy.gui import Gui
from audio.recorder import record_audio
from speech.deepgram_stt import transcribe_audio
from llm.openai_client import get_response
from tts.elevenlabs_tts import speak

conversation = "🤖 AI Voice Assistant Ready!\n\nClick the button to start."


def start_assistant(state):
    global conversation

    conversation = "🎤 Recording...\n"

    record_audio()

    conversation += "📝 Transcribing...\n"

    transcript = transcribe_audio()

    if not transcript:
        conversation += "❌ No transcript generated."
        return

    conversation += f"\n👤 You: {transcript}\n"

    response = get_response(transcript)

    conversation += f"\n🤖 Assistant: {response}\n"

    speak(response)


page = """
# 🤖 AI Voice Assistant

<|Start Assistant|button|on_action=start_assistant|>

<|{conversation}|text|>
"""

Gui(page).run(title="AI Voice Assistant")