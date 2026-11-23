
import pandas as pd
from database import create_connection


def clean(value):
    if pd.isna(value):
        return None
    return value


def load_tennis_data():

    conn = None
    cursor = None

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Read all CSV files
        categories = pd.read_csv("data/categories.csv")
        competitions = pd.read_csv("data/competitions.csv")
        complexes = pd.read_csv("data/complexes.csv")
        venues = pd.read_csv("data/venues.csv")

        singles = pd.read_csv("data/tennis_cleaned.csv")
        doubles = pd.read_csv("data/doubles_rankings.csv")

        # Clear old records in child-to-parent order
        cursor.execute("DELETE FROM competitor_rankings")
        cursor.execute("DELETE FROM competitors")
        cursor.execute("DELETE FROM venues")
        cursor.execute("DELETE FROM competitions")
        cursor.execute("DELETE FROM complexes")
        cursor.execute("DELETE FROM categories")

        # 1. Categories
        for _, r in categories.iterrows():
            cursor.execute("""
                INSERT INTO categories (category_id, category_name)
                VALUES (%s, %s)
            """, (clean(r.category_id), clean(r.category_name)))

        # 2. Complexes
        for _, r in complexes.iterrows():
            cursor.execute("""
                INSERT INTO complexes (complex_id, complex_name)
                VALUES (%s, %s)
            """, (clean(r.complex_id), clean(r.complex_name)))

        # 3. Competitions
        for _, r in competitions.iterrows():
            cursor.execute("""
                INSERT INTO competitions
                (competition_id, competition_name, parent_id,
                 type, gender, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                clean(r.competition_id),
                clean(r.competition_name),
                clean(r.parent_id),
                clean(r.type),
                clean(r.gender),
                clean(r.category_id)
            ))

        # 4. Venues
        for _, r in venues.iterrows():
            cursor.execute("""
                INSERT INTO venues
                (venue_id, venue_name, city_name, country_name,
                 country_code, timezone, complex_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                clean(r.venue_id),
                clean(r.venue_name),
                clean(r.city_name),
                clean(r.country_name),
                clean(r.country_code),
                clean(r.timezone),
                clean(r.complex_id)
            ))

        # 5. Combine singles and doubles competitors
        all_players = {}

        for _, r in singles.iterrows():
            all_players[clean(r["player_id"])] = (
                clean(r["player_name"]),
                clean(r["country"]),
                clean(r["country_code"]),
                None
            )

        for _, r in doubles.iterrows():
            all_players[clean(r["player_id"])] = (
                clean(r["player_name"]),
                clean(r["country"]),
                clean(r["country_code"]),
                clean(r["abbreviation"])
            )

        all_players.pop(None, None)

        for player_id, details in all_players.items():
            cursor.execute("""
                INSERT INTO competitors
                (competitor_id, name, country, country_code, abbreviation)
                VALUES (%s, %s, %s, %s, %s)
            """, (player_id, *details))

        # 6. Insert singles and doubles rankings
        ranking_count = 0

        for df in [singles, doubles]:
            for _, r in df.iterrows():

                player_id = clean(r["player_id"])

                if player_id is None:
                    continue

                cursor.execute("""
                    INSERT INTO competitor_rankings
                    (`rank`, movement, points, competitions_played,
                     competitor_id, tour, gender, ranking_year, ranking_week)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(r["rank"]),
                    int(r["movement"]),
                    int(r["points"]),
                    int(r["competitions_played"]),
                    player_id,
                    clean(r["tour"]),
                    clean(r["gender"]),
                    int(r["year"]),
                    int(r["week"])
                ))

                ranking_count += 1

        conn.commit()

        print("\nALL DATA LOADED SUCCESSFULLY!")
        print("Categories:", len(categories))
        print("Competitions:", len(competitions))
        print("Complexes:", len(complexes))
        print("Venues:", len(venues))
        print("Unique competitors:", len(all_players))
        print("Total rankings:", ranking_count)

    except Exception as error:
        if conn:
            conn.rollback()
        print("DATABASE ERROR:", error)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_tennis_data()
