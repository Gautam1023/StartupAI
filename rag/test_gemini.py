from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

print("1")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("2")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

print("3")

print(response.text)