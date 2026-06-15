from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------
# Gemini
# -------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -------------------------
# ChromaDB
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

# -------------------------
# Inputs
# -------------------------

idea = input("Startup Idea: ")
funding = input("Funding Required: ")
team = input("Team Size: ")

query = f"""
Startup Idea: {idea}
Funding Required: {funding}
Team Size: {team}
Shark Tank Analysis
"""

# -------------------------
# Retrieve Context
# -------------------------

results = vectordb.similarity_search(query, k=5)

context = "\n\n".join(
    [doc.page_content[:500] for doc in results]
)

# -------------------------
# Prompt
# -------------------------

prompt = f"""
You are StartupAI Shark Tank Panel.

Use the startup knowledge below.

Knowledge:
{context}

Startup Idea: {idea}
Funding Required: {funding}
Team Size: {team}

Simulate 3 Sharks:

1. Investor Shark
2. Risk Shark
3. Business Shark

Generate:

1. Deal Score (1-100)
2. Investor Shark Verdict
3. Risk Shark Verdict
4. Business Shark Verdict
5. Most Attractive Strength
6. Most Dangerous Weakness
7. Recommended Funding
8. Suggested Equity %
9. Final Verdict (INVEST or PASS)

Be realistic like Shark Tank.
"""

# -------------------------
# Gemini
# -------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n===== STARTUPAI SHARK TANK REPORT =====\n")
print(response.text)