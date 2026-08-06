from audio.recorder import record_audio
from speech.deepgram_stt import transcribe_audio
from llm.openai_client import get_response
from tts.elevenlabs_tts import speak


def main():

    print("=" * 50)
    print("🤖 AI Voice Assistant Started")
    print("=" * 50)

    # Record voice
    record_audio()

    # Speech to Text
    transcript = transcribe_audio()

    if not transcript:
        print("No transcript generated.")
        return

    # LLM
    response = get_response(transcript)

    # Speak
    speak(response)


if __name__ == "__main__":
    main()