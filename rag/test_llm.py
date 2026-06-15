from openai import OpenAI
from dotenv import load_dotenv
import os

print("1")

load_dotenv()

print("2")

api_key = os.getenv("NVIDIA_API_KEY")

print("KEY FOUND:", api_key is not None)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
    timeout=30
)

print("3")

try:
    response = client.chat.completions.create(
        model="deepseek-ai/deepseek-v4-pro",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ],
        temperature=0.1,
        max_tokens=50,
        stream=False
    )

    print("4")
    print("\nMODEL RESPONSE:\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nERROR:")
    print(e)