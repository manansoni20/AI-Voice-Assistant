import os
import wave
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

OUTPUT_DIR = "recordings"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "input.wav")


def record_audio():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("🎤 Recording... Speak now!")

    frames = []

    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        frames.append(stream.read(CHUNK))

    print("✅ Recording finished!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(OUTPUT_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    record_audio()