import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

df = pd.read_csv("../../startup data.csv")

features = [
    'age_first_funding_year',
    'age_last_funding_year',
    'relationships',
    'funding_rounds',
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

X = df[features].fillna(0)

y = df["funding_total_usd"].fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, pred))
print("R2 Score:", r2_score(y_test, pred))

with open("funding_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Funding Model Saved")