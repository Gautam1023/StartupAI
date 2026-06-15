from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    timeout=60
)

response = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4-pro",
    messages=[
        {
            "role": "user",
            "content": "Give 5 startup risks for an AI SaaS company."
        }
    ],
    max_tokens=100
)

print(response.choices[0].message.content)