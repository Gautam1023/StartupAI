import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv("../../startup data.csv")

# Target
df["status"] = df["status"].map({
    "acquired": 1,
    "closed": 0
})

features = [
    'age_first_funding_year',
    'age_last_funding_year',
    'relationships',
    'funding_rounds',
    'funding_total_usd',
    'milestones',
    'has_VC',
    'has_angel',
    'has_roundA',
    'has_roundB',
    'has_roundC',
    'has_roundD',
    'avg_participants',
    'is_top500'
]

X = df[features]
y = df["status"]

X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

with open("success_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model Saved")