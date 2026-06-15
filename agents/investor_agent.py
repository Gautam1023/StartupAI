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
funding_needed = input("Funding Required: ")
team = input("Team Size: ")

query = f"""
Startup Idea: {idea}
Funding Required: {funding_needed}
Team Size: {team}
Investor Analysis
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
You are StartupAI Investor Agent.

Knowledge:
{context}

Startup Idea: {idea}
Funding Required: {funding_needed}
Team Size: {team}

Act like a venture capitalist.

Generate:

1. Investor Interest Score (1-10)
2. Investment Decision (Invest / Pass)
3. Startup Strengths
4. Startup Weaknesses
5. Questions Investors Will Ask
6. Funding Readiness
7. Suggested Valuation Range
8. Key Risks Before Investment

Be realistic and professional.
"""

# -------------------------
# Gemini
# -------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n===== STARTUPAI INVESTOR REPORT =====\n")
print(response.text)