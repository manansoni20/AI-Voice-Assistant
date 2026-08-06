from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_response(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_input,
        )

        return response.text

    except Exception as e:
        print("\n❌ Gemini Error:")
        print(e)
        return "Sorry, I couldn't process your request."


if __name__ == "__main__":
    text = input("You: ")
    print("\n🤖 Assistant:\n")
    print(get_response(text))