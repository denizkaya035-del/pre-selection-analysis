import pandas as pd

# Daten laden
df = pd.read_csv("output/preselection_merged.csv")

# Länder ausschließen, in denen Whatnot bereits aktiv ist
existing_markets = [
    "France",
    "Germany",
    "Netherlands",
    "Belgium",
    "Austria"
]

df = df[~df["country"].isin(existing_markets)].copy()

# -----------------------------
# STUFE 1: Mindestanforderungen
# Bottom Quartile bei Population und E-Commerce ausschließen
# -----------------------------
pop_q1 = df["population_2024"].quantile(0.25)
ecom_q1 = df["ecommerce_penetration_2025"].quantile(0.25)

filtered_df = df[
    (df["population_2024"] > pop_q1) &
    (df["ecommerce_penetration_2025"] > ecom_q1)
].copy()

# -----------------------------
# STUFE 2: Vier-Stufen-Scoring (0–3)
# Q1 = 25%, Q2 = 50%, Q3 = 75%
# -----------------------------
def four_level_score(series):
    q1 = series.quantile(0.25)
    q2 = series.quantile(0.50)
    q3 = series.quantile(0.75)

    def score(x):
        if x <= q1:
            return 0
        elif x <= q2:
            return 1
        elif x <= q3:
            return 2
        else:
            return 3

    return series.apply(score)

filtered_df["population_score"] = four_level_score(filtered_df["population_2024"])
filtered_df["ecommerce_score"] = four_level_score(filtered_df["ecommerce_penetration_2025"])
filtered_df["gdp_score"] = four_level_score(filtered_df["gdp_per_capita_2024"])

# -----------------------------
# Gewichteter Gesamtscore
# Population und E-Commerce höher gewichten
# -----------------------------
filtered_df["total_score"] = (
    filtered_df["population_score"] * 0.4 +
    filtered_df["ecommerce_score"] * 0.4 +
    filtered_df["gdp_score"] * 0.2
)

# Nach Score sortieren
filtered_df = filtered_df.sort_values(by="total_score", ascending=False)

# Ausgabe
print(filtered_df[[
    "country",
    "population_2024",
    "ecommerce_penetration_2025",
    "gdp_per_capita_2024",
    "population_score",
    "ecommerce_score",
    "gdp_score",
    "total_score"
]])

# Speichern
filtered_df.to_csv("output/preselection_ranked_4level.csv", index=False)

print("\nSaved to output/preselection_ranked_4level.csv")
print(f"Remaining countries after exclusion and filtering: {len(filtered_df)}")
filtered_df.to_excel("output/preselection_full_table.xlsx", index=False)