import re

def extract_number(text, default=50):
    numbers = re.findall(r'\d+', str(text))
    if numbers:
        return int(numbers[0])
    return default


def generate_health_score(
    risk_score,
    investor_score,
    shark_score,
    business_score=60
):

    health_score = (
        business_score * 0.30 +
        investor_score * 10 * 0.25 +
        shark_score * 0.25 -
        risk_score * 10 * 0.20
    )

    health_score = max(0, min(100, int(health_score)))

    if health_score >= 80:
        status = "Excellent"

    elif health_score >= 60:
        status = "Good"

    elif health_score >= 40:
        status = "Moderate"

    else:
        status = "High Risk"

    return {
        "health_score": health_score,
        "status": status
    }