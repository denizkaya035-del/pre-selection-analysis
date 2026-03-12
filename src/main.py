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

# ----------------------------------
# Quartile EINMAL berechnen
# ----------------------------------
pop_q1 = df["population_2024"].quantile(0.25)
pop_q2 = df["population_2024"].quantile(0.50)
pop_q3 = df["population_2024"].quantile(0.75)

ecom_q1 = df["ecommerce_penetration_2025"].quantile(0.25)
ecom_q2 = df["ecommerce_penetration_2025"].quantile(0.50)
ecom_q3 = df["ecommerce_penetration_2025"].quantile(0.75)

gdp_q1 = df["gdp_per_capita_2024"].quantile(0.25)
gdp_q2 = df["gdp_per_capita_2024"].quantile(0.50)
gdp_q3 = df["gdp_per_capita_2024"].quantile(0.75)

# ----------------------------------
# STUFE 1: Mindestanforderungen
# Raus, wenn Population ODER E-Commerce im unteren Quartil ist
# ----------------------------------
filtered_df = df[
    (df["population_2024"] > pop_q1) &
    (df["ecommerce_penetration_2025"] > ecom_q1)
].copy()

# ----------------------------------
# STUFE 2: Vier-Stufen-Scoring mit FESTEN Quartilen
# ----------------------------------
def score_with_fixed_quartiles(x, q1, q2, q3):
    if x <= q1:
        return 0
    elif x <= q2:
        return 1
    elif x <= q3:
        return 2
    else:
        return 3

filtered_df["population_score"] = filtered_df["population_2024"].apply(
    lambda x: score_with_fixed_quartiles(x, pop_q1, pop_q2, pop_q3)
)

filtered_df["ecommerce_score"] = filtered_df["ecommerce_penetration_2025"].apply(
    lambda x: score_with_fixed_quartiles(x, ecom_q1, ecom_q2, ecom_q3)
)

filtered_df["gdp_score"] = filtered_df["gdp_per_capita_2024"].apply(
    lambda x: score_with_fixed_quartiles(x, gdp_q1, gdp_q2, gdp_q3)
)

# ----------------------------------
# Gewichteter Gesamtscore
# ----------------------------------
filtered_df["total_score"] = (
    filtered_df["population_score"] * 0.35 +
    filtered_df["ecommerce_score"] * 0.35 +
    filtered_df["gdp_score"] * 0.30
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
]].to_string(index=False))

# Speichern
filtered_df.to_csv("output/preselection_ranked_4level.csv", index=False)
filtered_df.to_excel("output/preselection_full_table.xlsx", index=False)

print("\nSaved to output/preselection_ranked_4level.csv")
print(f"Remaining countries after exclusion and filtering: {len(filtered_df)}")