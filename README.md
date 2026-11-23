
# 🎾 Tennis Analytics Project

## Project Overview
This project analyzes professional tennis player rankings using SportRadar Tennis API, Python, MySQL and Streamlit.

## Objectives
- Fetch tennis ranking data using SportRadar API.
- Clean and analyze player ranking data.
- Store player and ranking information in MySQL.
- Perform SQL-based analysis.
- Build an interactive Streamlit dashboard.

## Technologies Used
- Python
- Pandas
- MySQL
- SQL
- Streamlit
- Plotly
- SportRadar API

## Project Features
- 1,000 player records stored in MySQL.
- 1,000 ranking records stored in MySQL.
- ATP and WTA tour filters.
- Country-wise player distribution.
- Top 10 ranked players.
- Player ranking table.
- Ranking movement analysis.
- CSV data download.

## Dashboard KPIs
- Total Player Records: 1,000
- Countries: 79
- Average Ranking Points: 539
- Top Ranked Player: Alexander Zverev

## Project Structure
```text
Game Analytics Project/
│
├── data/
│   ├── analysis.py
│   ├── load.py
│   ├── tennis_cleaned.csv
│   └── rankings_raw.json
│
├── app.py
├── database.py
├── fetch_data.py
├── performance_analysis.py
├── .env
└── .gitignore
```

## How to Run
1. Install the required packages.
2. Add your SportRadar API key and MySQL credentials to `.env`.
3. Run the data extraction script.
4. Load the data into MySQL.
5. Start the dashboard:

```bash
python -m streamlit run app.py
```

## Author
Data Analytics Portfolio Project
