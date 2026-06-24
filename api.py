
from flask import Flask, request, jsonify
from flask_cors import CORS

from agents.master_agent import generate_master_report
from ML.startup_predictor import predict_success

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {
        "message": "StartupAI API Running"
    }


@app.route("/evaluate", methods=["POST"])
def evaluate():

    data = request.json

    idea = data.get("idea")
    funding = data.get("funding")
    team = data.get("team")

    # -------------------------
    # Success Predictor
    # -------------------------

    try:

        success_prediction = predict_success(
            idea,
            funding,
            team
        )

    except Exception as e:

        success_prediction = {
            "error": str(e)
        }

    # -------------------------
    # Master Agent
    # -------------------------

    try:

        print("Generating Master Report...")

        master_report = generate_master_report(
            idea,
            funding,
            team
        )

    except Exception as e:

        master_report = f"Master Agent Error: {str(e)}"

    # -------------------------
    # Final Response
    # -------------------------

    return jsonify({

        "startup_idea": idea,

        "funding": funding,

        "team_size": team,

        "success_prediction": success_prediction,

        "master_report": master_report

    })


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )

