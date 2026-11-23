
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


# ==========================================
# ADDITIONAL REQUIRED API DATA EXTRACTION
# ==========================================

def fetch_and_save(endpoint, filename):
    url = f"https://api.sportradar.com/tennis/trial/v3/en/{endpoint}.json"

    print(f"\nFetching {endpoint}...")

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"Failed: {endpoint} | Status: {response.status_code}")
            print(response.text[:300])
            return None

        result = response.json()

        with open(f"data/{filename}.json", "w", encoding="utf-8") as f:
            import json
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Saved: data/{filename}.json")
        return result

    except requests.RequestException as e:
        print("Request error:", e)
        return None


# 1. COMPETITIONS API
competition_data = fetch_and_save("competitions", "competitions_raw")

if competition_data:
    competitions = []
    categories = {}

    for item in competition_data.get("competitions", []):
        category = item.get("category") or {}

        if category.get("id"):
            categories[category["id"]] = {
                "category_id": category.get("id"),
                "category_name": category.get("name")
            }

        competitions.append({
            "competition_id": item.get("id"),
            "competition_name": item.get("name"),
            "parent_id": item.get("parent_id"),
            "type": item.get("type"),
            "gender": item.get("gender"),
            "category_id": category.get("id")
        })

    pd.DataFrame(categories.values()).to_csv(
        "data/categories.csv", index=False
    )
    pd.DataFrame(competitions).to_csv(
        "data/competitions.csv", index=False
    )

    print("Categories:", len(categories))
    print("Competitions:", len(competitions))


# 2. COMPLEXES AND VENUES API
complex_data = fetch_and_save("complexes", "complexes_raw")

if complex_data:
    complexes = []
    venues = []

    for item in complex_data.get("complexes", []):
        complex_id = item.get("id")

        complexes.append({
            "complex_id": complex_id,
            "complex_name": item.get("name")
        })

        for venue in item.get("venues", []):
            venues.append({
                "venue_id": venue.get("id"),
                "venue_name": venue.get("name"),
                "city_name": venue.get("city_name"),
                "country_name": venue.get("country_name"),
                "country_code": venue.get("country_code"),
                "timezone": venue.get("timezone"),
                "complex_id": complex_id
            })

    pd.DataFrame(complexes).to_csv(
        "data/complexes.csv", index=False
    )
    pd.DataFrame(venues).to_csv(
        "data/venues.csv", index=False
    )

    print("Complexes:", len(complexes))
    print("Venues:", len(venues))


# 3. DOUBLES COMPETITOR RANKINGS API
doubles_data = fetch_and_save(
    "double_competitors_rankings",
    "doubles_rankings_raw"
)

if doubles_data:
    doubles = []

    for ranking in doubles_data.get("rankings", []):
        for item in ranking.get("competitor_rankings", []):
            player = item.get("competitor", {})

            doubles.append({
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
                "country_code": player.get("country_code"),
                "abbreviation": player.get("abbreviation")
            })

    pd.DataFrame(doubles).to_csv(
        "data/doubles_rankings.csv", index=False
    )

    print("Doubles ranking records:", len(doubles))

print("\nADDITIONAL API EXTRACTION FINISHED!")
