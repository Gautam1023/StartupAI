
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
# Business Agent Function
# -------------------------

def generate_business_report(idea, funding, team):

    query = f"""
    Startup Idea: {idea}
    Funding: {funding}
    Team Size: {team}
    Business Analysis
    """

    results = vectordb.similarity_search(query, k=5)

    context = "\n\n".join(
        [doc.page_content[:500] for doc in results]
    )

    prompt = f"""
    You are StartupAI Business Agent.

    Knowledge:
    {context}

    Startup Idea: {idea}
    Funding Available: {funding}
    Team Size: {team}

    Generate:

    1. Business Model Analysis
    2. Target Customers
    3. Revenue Streams
    4. Product-Market Fit Assessment
    5. Go-To-Market Strategy
    6. Growth Strategy
    7. Key Business Risks
    8. Recommendations

    Provide practical startup advice.
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

    report = generate_business_report(
        idea,
        funding,
        team
    )

    print("\n===== STARTUPAI BUSINESS REPORT =====\n")
    print(report)

