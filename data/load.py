
import pandas as pd
from database import create_connection


def load_tennis_data():

    # 1. Read cleaned tennis data
    df = pd.read_csv("data/tennis_cleaned.csv")

    print("Total records found:", len(df))

    conn = None
    cursor = None

    try:
        # 2. Connect to MySQL
        conn = create_connection()
        cursor = conn.cursor()

        # 3. Remove previous records
        cursor.execute("DELETE FROM competitor_rankings")
        cursor.execute("DELETE FROM competitors")

        # 4. Insert each player and ranking
        for _, row in df.iterrows():

            competitor_id = row["player_id"]

            # Insert player details
            cursor.execute(
                """
                INSERT INTO competitors
                (competitor_id, name, country, country_code, abbreviation)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    competitor_id,
                    row["player_name"],
                    row["country"],
                    row["country_code"],
                    None
                )
            )

            # Insert ranking details
            cursor.execute(
                """
                INSERT INTO competitor_rankings
                (`rank`, movement, points, competitions_played,
                 competitor_id, tour, gender, ranking_year, ranking_week)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(row["rank"]),
                    int(row["movement"]),
                    int(row["points"]),
                    int(row["competitions_played"]),
                    competitor_id,
                    row["tour"],
                    row["gender"],
                    int(row["year"]),
                    int(row["week"])
                )
            )

        # 5. Save all records
        conn.commit()

        print("Tennis data inserted successfully!")
        print("Total players inserted:", len(df))
        print("Total rankings inserted:", len(df))

    except Exception as error:

        if conn:
            conn.rollback()

        print("Database Error:", error)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    load_tennis_data()
