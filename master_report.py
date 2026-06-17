
import json
import os

from agents.risk_agent import generate_risk_report
from agents.investor_agent import generate_investor_report
from agents.business_agent import generate_business_report
from agents.sharktank_agent import generate_shark_report
from agents.swot_agent import generate_swot_report
from ML.startup_predictor import predict_success

# -------------------------
# User Input
# -------------------------

idea = input("Startup Idea: ")
funding = input("Funding Available: ")
team = input("Team Size: ")

# -------------------------
# Generate Reports
# -------------------------

print("\nGenerating Risk Report...")
risk_report = generate_risk_report(
    idea,
    funding,
    team
)

print("Generating Investor Report...")
investor_report = generate_investor_report(
    idea,
    funding,
    team
)

print("Generating Business Report...")
business_report = generate_business_report(
    idea,
    funding,
    team
)

print("Generating Shark Tank Report...")
shark_report = generate_shark_report(
    idea,
    funding,
    team
)

print("Generating SWOT Report...")
swot_report = generate_swot_report(
    idea,
    funding,
    team
)

print("Generating Success Prediction...")
success_prediction = predict_success(
    idea,
    funding,
    team
)

# -------------------------
# Combined Report
# -------------------------

report = {
    "startup_idea": idea,
    "funding": funding,
    "team_size": team,

    "success_prediction": success_prediction,

    "risk_report": risk_report,
    "investor_report": investor_report,
    "business_report": business_report,
    "shark_report": shark_report,
    "swot_report": swot_report
}

# -------------------------
# Save JSON
# -------------------------

os.makedirs("reports", exist_ok=True)

with open(
    "reports/startup_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        report,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nReport Saved Successfully!")
print("reports/startup_report.json")

