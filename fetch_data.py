
# ==========================================
# PROJECT: TENNIS GAME ANALYTICS
# TASK: FETCH ATP AND WTA WORLD RANKINGS
# ==========================================

import os
import requests
import pandas as pd
from dotenv import load_dotenv

# STEP 1: Load API key from .env file
load_dotenv()

API_KEY = os.getenv("SPORTRADAR_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

# STEP 2: Set SportRadar API URL
url = "https://api.sportradar.com/tennis/trial/v3/en/rankings.json"

# STEP 3: Set request headers
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

# STEP 4: Send request to SportRadar
print("Connecting to SportRadar...")

response = requests.get(url, headers=headers, timeout=30)

# STEP 5: Check API response
if response.status_code == 200:

    print("Data fetched successfully!")

    data = response.json()

    # Save original API response
    os.makedirs("data", exist_ok=True)

    with open("data/rankings_raw.json", "w", encoding="utf-8") as file:
        import json
        json.dump(data, file, indent=4, ensure_ascii=False)

    # STEP 6: Extract ATP and WTA rankings
    records = []

    for ranking in data.get("rankings", []):

        for item in ranking.get("competitor_rankings", []):

            player = item.get("competitor", {})

            records.append({
                "tour": ranking.get("name"),
                "gender": ranking.get("gender"),
                "year": ranking.get("year"),
                "week": ranking.get("week"),
                "rank": item.get("rank"),
                "movement": item.get("movement"),
                "points": item.get("points"),
                "competitions_played": item.get("competitions_played"),
                "player_id": player.get("id"),
                "player_name": player.get("name"),
                "country": player.get("country"),
                "country_code": player.get("country_code")
            })

    # STEP 7: Convert data into a DataFrame
    df = pd.DataFrame(records)

    if df.empty:
        print("No ranking records were returned.")
    else:
        # STEP 8: Save data as CSV
        df.to_csv("data/tennis_rankings.csv", index=False)

        print("\nTotal players collected:", len(df))
        print("\nFirst 10 players:")
        print(df.head(10).to_string(index=False))

        print("\nCSV saved successfully!")
        print("Location: data/tennis_rankings.csv")

elif response.status_code == 403:
    print("Access denied. Check API key and trial access.")

elif response.status_code == 429:
    print("API request limit reached. Please wait before retrying.")

else:
    print("API Error:", response.status_code)
    print(response.text[:1000])
