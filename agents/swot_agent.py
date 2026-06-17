
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
# SWOT Agent Function
# -------------------------

def generate_swot_report(idea, funding, team):

    query = f"""
    Startup Idea: {idea}
    Funding Available: {funding}
    Team Size: {team}
    SWOT Analysis
    """

    results = vectordb.similarity_search(query, k=5)

    context = "\n\n".join(
        [doc.page_content[:500] for doc in results]
    )

    prompt = f"""
    You are StartupAI SWOT Agent.

    Use the startup knowledge below.

    Knowledge:
    {context}

    Startup Idea: {idea}
    Funding Available: {funding}
    Team Size: {team}

    Generate a detailed SWOT Analysis.

    1. Strengths
    2. Weaknesses
    3. Opportunities
    4. Threats

    Give practical startup insights.
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
    funding = input("Funding Available: ")
    team = input("Team Size: ")

    report = generate_swot_report(
        idea,
        funding,
        team
    )

    print("\n===== STARTUPAI SWOT REPORT =====\n")
    print(report)

