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
# Chroma
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

# -------------------------
# Master Agent
# -------------------------

def generate_master_report(
    idea,
    funding,
    team
):

    query = f"""
    Startup Idea: {idea}
    Funding: {funding}
    Team Size: {team}
    Startup Analysis
    """

    results = vectordb.similarity_search(
        query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content[:500] for doc in results]
    )

    prompt = f"""
You are StartupAI Master Agent.

Use the startup knowledge below.

Knowledge:
{context}

Startup Idea: {idea}
Funding Available: {funding}
Team Size: {team}

Generate a complete startup evaluation.

Return:

# Executive Summary

# Success Probability

# Risk Analysis

# Investor Analysis

# Business Analysis

# SWOT Analysis

# Shark Tank Verdict

# Funding Recommendation

# Growth Strategy

# Final Verdict

Be realistic and detailed.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -------------------------
# Standalone Testing
# -------------------------

if __name__ == "__main__":

    idea = input("Startup Idea: ")
    funding = input("Funding: ")
    team = input("Team Size: ")

    report = generate_master_report(
        idea,
        funding,
        team
    )

    print("\n===== MASTER REPORT =====\n")

    print(report)