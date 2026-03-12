import pandas as pd
import matplotlib.pyplot as plt

# Datei laden
df = pd.read_csv("output/preselection_ranked_4level.csv")

# Top 3 Länder festlegen
top3_countries = ["Sweden", "Spain", "Denmark"]

# Nach Score sortieren, damit der Plot sauber aussieht
df = df.sort_values("total_score", ascending=True)

# Farben setzen
colors = ["green" if country in top3_countries else "lightgray" for country in df["country"]]

# Plot
plt.figure(figsize=(11, 8))
bars = plt.barh(df["country"], df["total_score"], color=colors)

plt.title("Country Pre-Selection Scoring Results")
plt.xlabel("Total Score")
plt.ylabel("Country")
plt.grid(axis="x", linestyle="--", alpha=0.4)

# Scorewerte rechts an die Balken schreiben
for bar, score in zip(bars, df["total_score"]):
    plt.text(
        bar.get_width() + 0.03,
        bar.get_y() + bar.get_height() / 2,
        f"{score:.1f}",
        va="center",
        fontsize=9
    )

plt.tight_layout()

# Optional speichern
plt.savefig("output/preselection_plot_top3_highlighted.png", dpi=300, bbox_inches="tight")

plt.show()