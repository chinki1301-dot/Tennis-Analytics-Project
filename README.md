# 🎾 Tennis Analytics Project

## Project Overview
This project analyzes professional tennis player rankings using the SportRadar Tennis API, Python, Pandas, Plotly and Streamlit. It provides an interactive dashboard to explore player performance, ranking points and country-wise tennis statistics.

## Objectives
- Fetch tennis ranking data using the SportRadar API.
- Clean and analyze player ranking data using Python.
- Design relational database tables and perform SQL-based analysis using MySQL.
- Build an interactive Streamlit dashboard.
- Visualize ATP and WTA player rankings and performance.

## Technologies Used
- Python
- Pandas
- MySQL
- SQL
- Streamlit
- Plotly
- SportRadar API

## Project Features
- 1,000 player ranking records analyzed.
- ATP and WTA tour filters.
- Country-wise player distribution.
- Top 10 ranked players visualization.
- Interactive player rankings table.
- Ranking movement analysis.
- CSV data download.
- Data cleaning and performance analysis.

## Dashboard KPIs
- **Total Player Records:** 1,000
- **Countries:** 79
- **Average Ranking Points:** 539
- **Top Ranked Player:** Alexander Zverev

## Project Structure

```text
Tennis-Analytics-Project/
│
├── data/
│   ├── analysis.py
│   ├── load.py
│   ├── rankings_raw.json
│   ├── tennis_cleaned.csv
│   └── tennis_rankings.csv
│
├── app.py
├── database.py
├── fetch_data.py
├── performance_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/chinki1301-dot/Tennis-Analytics-Project.git
```

2. Open the project folder:

```bash
cd Tennis-Analytics-Project
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Add your SportRadar API key to a local `.env` file if fetching fresh data.

5. Run the dashboard:

```bash
python -m streamlit run app.py
```

## Live Dashboard

[Open Tennis Analytics Dashboard](https://tennis-analytics-project-awx4gizgjahmrkywhu5gz.streamlit.app/)

## Author
**Chinki**

Data Analytics Portfolio Project

GitHub: [chinki1301-dot](https://github.com/chinki1301-dot)
## SQL Analysis

This project includes 20 SQL queries covering:

- Competition Analysis
- Venue Analysis
- Doubles Rankings Analysis

[View SQL Queries](tennis_analytics_queries.sql)