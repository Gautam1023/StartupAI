import pickle
import pandas as pd

with open("success_model.pkl", "rb") as f:
    model = pickle.load(f)

sample = pd.DataFrame([{
    'age_first_funding_year': 2,
    'age_last_funding_year': 5,
    'relationships': 10,
    'funding_rounds': 3,
    'funding_total_usd': 5000000,
    'milestones': 4,
    'has_VC': 1,
    'has_angel': 1,
    'has_roundA': 1,
    'has_roundB': 1,
    'has_roundC': 0,
    'has_roundD': 0,
    'avg_participants': 3,
    'is_top500': 1
}])

prediction = model.predict(sample)[0]
probability = model.predict_proba(sample)[0]

print("Prediction:", prediction)

if prediction == 1:
    print("Startup Status: Acquired (Success)")
else:
    print("Startup Status: Closed (Failure)")

print("Success Probability:", round(probability[1] * 100, 2), "%")