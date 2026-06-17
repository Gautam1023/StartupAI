
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

print("1 - Starting")

# -------------------------
# Gemini
# -------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("2 - Gemini Ready")

# -------------------------
# Embeddings
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("3 - Embeddings Loaded")

# -------------------------
# ChromaDB
# -------------------------

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

print("4 - ChromaDB Loaded")


# -------------------------
# Risk Agent Function
# -------------------------

def generate_risk_report(idea, funding, team):

    print("5 - Inputs Received")

    query = f"""
    Startup Idea: {idea}
    Funding: {funding}
    Team Size: {team}
    Startup Risks
    """

    results = vectordb.similarity_search(query, k=5)

    print("6 - Retrieval Complete")

    context = "\n\n".join(
        [doc.page_content[:500] for doc in results]
    )

    print("7 - Context Built")
    print("Context Length:", len(context))

    prompt = f"""
    You are StartupAI Risk Agent.

    Use the startup knowledge below when analyzing.

    Knowledge:
    {context}

    Startup Idea:
    {idea}

    Funding:
    {funding}

    Team Size:
    {team}

    Generate:

    1. Risk Score (1-10)
    2. Market Risk
    3. Funding Risk
    4. Execution Risk
    5. Competition Risk
    6. Recommendations
    7. Mention relevant startup failure lessons from the knowledge provided.

    Be detailed and practical.
    """

    print("8 - Prompt Ready")
    print("Prompt Length:", len(prompt))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("9 - Gemini Response Received")

    return response.text


# -------------------------
# Standalone Run
# -------------------------

if __name__ == "__main__":

    idea = input("Startup Idea: ")
    funding = input("Funding Available: ")
    team = input("Team Size: ")

    report = generate_risk_report(
        idea,
        funding,
        team
    )

    print("\n===== STARTUPAI RISK REPORT =====\n")
    print(report)

