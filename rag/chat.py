from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

query = input("Ask StartupAI: ")

results = vectordb.similarity_search(query, k=3)

context = "\n\n".join([doc.page_content for doc in results])

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{query}
"""

response = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4-pro",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=500
)

print("\nStartupAI Answer:\n")
print(response.choices[0].message.content)