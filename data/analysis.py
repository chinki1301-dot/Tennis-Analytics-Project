
import pandas as pd

# Step 1: Load the dataset
df = pd.read_csv("data/tennis_rankings.csv")

# Step 2: Display basic information
print("\n--- DATASET OVERVIEW ---")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))

# Step 3: Check column names
print("\n--- COLUMNS ---")
print(df.columns.tolist())

# Step 4: Display first 10 players
print("\n--- TOP 10 PLAYERS ---")
print(df[["rank", "player_name", "country", "points"]].head(10).to_string(index=False))

# Step 5: Country-wise player count
print("\n--- TOP 10 COUNTRIES ---")
print(df["country"].value_counts().head(10))

# Step 6: Highest ranking points
print("\n--- HIGHEST POINTS ---")
print(df.nlargest(10, "points")[["player_name", "country", "points"]].to_string(index=False))

# Step 7: Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())



# STEP 8: DATA CLEANING

# Remove duplicate records
print("\n--- DUPLICATE RECORDS ---")
print("Duplicates:", df.duplicated().sum())

df = df.drop_duplicates()

# Fill missing country codes
df["country_code"] = df["country_code"].fillna("Unknown")

# Check missing values again
print("\n--- AFTER DATA CLEANING ---")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("data/tennis_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")

