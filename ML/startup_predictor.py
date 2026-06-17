
def predict_success(idea, funding, team):

    score = 50

    # Funding Score
    funding_num = int(
        ''.join(filter(str.isdigit, funding))
        or 0
    )

    team_num = int(team)

    if funding_num >= 5000000:
        score += 20

    elif funding_num >= 1000000:
        score += 15

    elif funding_num >= 500000:
        score += 10

    # Team Score
    if team_num >= 10:
        score += 15

    elif team_num >= 5:
        score += 10

    elif team_num >= 3:
        score += 5

    # Industry Score
    idea_lower = idea.lower()

    if "ai" in idea_lower:
        score += 5

    if "saas" in idea_lower:
        score += 10

    if "fintech" in idea_lower:
        score += 10

    if "health" in idea_lower:
        score += 10

    score = max(0, min(100, score))

    if score >= 80:
        verdict = "High Success Potential"

    elif score >= 60:
        verdict = "Moderate Success Potential"

    else:
        verdict = "High Risk"

    return {
        "success_probability": score,
        "verdict": verdict
    }

