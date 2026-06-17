
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
# Embeddings
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------
# ChromaDB
# -------------------------

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

# -------------------------
# Shark Tank Agent Function
# -------------------------

def generate_shark_report(idea, funding, team):

    query = f"""
    Startup Idea: {idea}
    Funding Required: {funding}
    Team Size: {team}
    Shark Tank Analysis
    """

    results = vectordb.similarity_search(query, k=5)

    context = "\n\n".join(
        [doc.page_content[:500] for doc in results]
    )

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -------------------------
# Standalone Run
# -------------------------

if __name__ == "__main__":

    idea = input("Startup Idea: ")
    funding = input("Funding Required: ")
    team = input("Team Size: ")

    report = generate_shark_report(
        idea,
        funding,
        team
    )

    print("\n===== STARTUPAI SHARK TANK REPORT =====\n")
    print(report)

