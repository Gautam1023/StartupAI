import pandas as pd

df = pd.read_csv("../../startup data.csv")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nStatus Counts:")
print(df["status"].value_counts())