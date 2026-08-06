import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

URL = "https://api.deepgram.com/v1/listen"


def transcribe_audio(audio_path="recordings/input.wav"):
    print("📂 Opening audio file...")

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "audio/wav",
    }

    params = {
        "model": "nova-3",
        "smart_format": "true",
    }

    try:
        with open(audio_path, "rb") as audio:
            audio_data = audio.read()

        print(f" Audio loaded ({len(audio_data)} bytes)")
        print("📤 Uploading to Deepgram...")

        response = requests.post(
            URL,
            headers=headers,
            params=params,
            data=audio_data,
            timeout=60,
        )

        print(f"HTTP Status: {response.status_code}")

        if response.status_code != 200:
            print(response.text)
            return None

        result = response.json()

        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]

        print("\n=========================")
        print("Transcript")
        print("=========================")
        print(transcript)

        return transcript

    except Exception as e:
        print("❌ Exception:")
        print(e)
        return None


if __name__ == "__main__":
    transcribe_audio()