
import pandas as pd

# Load cleaned data
df = pd.read_csv("data/tennis_cleaned.csv")

# 1. Top 10 players
print("\n--- TOP 10 PLAYERS ---")
print(df.sort_values("rank")[["rank", "player_name", "country", "points"]].head(10).to_string(index=False))

# 2. Country distribution
print("\n--- TOP COUNTRIES ---")
print(df["country"].value_counts().head(10))

# 3. Highest points
print("\n--- TOP POINTS ---")
print(df.nlargest(10, "points")[["player_name", "points"]].to_string(index=False))

# 4. Average ranking by country
print("\n--- COUNTRY AVERAGE RANKING ---")
print(df.groupby("country")["rank"].mean().sort_values().head(10))

# 5. Biggest ranking improvement
print("\n--- BIGGEST IMPROVEMENT ---")
improved = df[df["movement"] > 0]
print(improved.nlargest(10, "movement")[["player_name", "movement", "rank"]].to_string(index=False))

print("\nPerformance analysis completed!")
