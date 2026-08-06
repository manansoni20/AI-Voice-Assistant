import pyttsx3

engine = pyttsx3.init()

# Voice settings
engine.setProperty("rate", 170)   # Speed
engine.setProperty("volume", 1.0) # Max volume

def speak(text):
    print("\n🔊 Assistant Speaking...\n")
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Hello Manan. Your AI Voice Assistant is working perfectly.")