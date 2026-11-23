
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Tennis Analytics Dashboard",
    page_icon="🎾",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 1.5rem;
}

[data-testid="stMetric"] {
    background-color: #1c2533;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #34445c;
}

h1, h2, h3 {
    color: #ffffff;
}

.subtitle {
    color: #aab7c4;
    font-size: 16px;
}

div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"] > div {
    display: flex !important;
}

div[data-testid="stHorizontalBlock"] > div
[data-testid="stMetric"] {
    min-height: 120px !important;
    height: 120px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(4)
[data-testid="stMetricValue"] {
    font-size: 26px !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    overflow-wrap: break-word !important;
    line-height: 1.3 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD DATA FROM CSV
# ==========================================

@st.cache_data
def load_data():

    file_path = Path(__file__).parent / "data" / "tennis_cleaned.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "tennis_cleaned.csv not found inside the data folder."
        )

    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename columns if required
    rename_columns = {
        "name": "player_name",
        "competitor_id": "player_id"
    }

    df = df.rename(columns=rename_columns)

    # Required columns
    required_columns = [
        "rank",
        "player_name",
        "country",
        "points",
        "movement"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns in CSV: {missing}"
        )

    # Handle missing values
    df["player_name"] = df["player_name"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    if "country_code" not in df.columns:
        df["country_code"] = "Unknown"

    if "tour" not in df.columns:
        df["tour"] = "Unknown"

    if "competitions_played" not in df.columns:
        df["competitions_played"] = 0

    # Standardize tour names
    df["tour"] = (
        df["tour"].astype(str).str.upper().str.strip()
    )

    # Convert numeric columns
    for col in ["rank", "points", "movement"]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    df["competitions_played"] = pd.to_numeric(
        df["competitions_played"], errors="coerce"
    ).fillna(0)

    # Remove invalid records
    df = df.dropna(subset=["rank", "points"])

    # Keep ATP and WTA records
    df = df[df["tour"].isin(["ATP", "WTA"])]

    return df


# Load dataset
try:
    df = load_data()

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.info(
        "Please check whether data/tennis_cleaned.csv exists "
        "and contains the required columns."
    )
    st.stop()


# ==========================================
# 4. DASHBOARD HEADER
# ==========================================

st.title("🎾 Tennis Analytics Dashboard")

st.markdown(
    '<p class="subtitle">Professional Tennis Player '
    'Rankings | Performance Analysis | Global Insights</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 5. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎯 Dashboard Filters")

tour_options = {
    "All Tours": "All",
    "ATP (Men's Professional Tennis)": "ATP",
    "WTA (Women's Professional Tennis)": "WTA"
}

selected_tour = st.sidebar.selectbox(
    "Select Tennis Tour",
    list(tour_options.keys())
)

tour_value = tour_options[selected_tour]

if tour_value == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["tour"] == tour_value].copy()

countries = sorted(
    filtered_df["country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + countries
)

if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ].copy()

st.sidebar.divider()

st.sidebar.caption("Data Source: SportRadar Tennis API")
st.sidebar.caption(
    f"Records available: {len(filtered_df):,}"
)


# ==========================================
# 6. CHECK FILTERED DATA
# ==========================================

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# ==========================================
# 7. KEY PERFORMANCE INDICATORS
# ==========================================

st.subheader("📊 Key Performance Indicators")

total_players = len(filtered_df)

total_countries = filtered_df["country"].nunique()

average_points = filtered_df["points"].mean()

top_player = (
    filtered_df.sort_values(
        ["rank", "points"],
        ascending=[True, False]
    ).iloc[0]["player_name"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Player Records",
    f"{total_players:,}"
)

col2.metric(
    "Countries",
    f"{total_countries:,}"
)

col3.metric(
    "Average Ranking Points",
    f"{average_points:,.0f}"
)

col4.metric(
    "Top Ranked Player",
    top_player,
    help=f"Full player name: {top_player}"
)

st.divider()


# ==========================================
# 8. TOP 10 PLAYERS
# ==========================================

st.subheader("🏆 Top 10 Ranked Players")

top_players = (
    filtered_df.sort_values(
        ["rank", "points"],
        ascending=[True, False]
    )
    .head(10)
)

fig1 = px.bar(
    top_players,
    x="player_name",
    y="points",
    color="tour",
    hover_data=["rank", "country", "movement"],
    title="Top 10 Players by Ranking Points",
    labels={
        "player_name": "Player Name",
        "points": "Ranking Points",
        "tour": "Tennis Tour"
    },
    color_discrete_sequence=["#38bdf8", "#f97316"]
)

fig1.update_layout(
    template="plotly_dark",
    xaxis_tickangle=-35,
    height=450
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()


# ==========================================
# 9. COUNTRY-WISE PLAYER DISTRIBUTION
# ==========================================

st.subheader("🌍 Country-wise Player Distribution")

country_data = (
    filtered_df.assign(
        country_display=filtered_df["country"].replace({
            "Neutral": "Unclassified"
        })
    )
    .groupby("country_display")
    .size()
    .reset_index(name="players")
    .sort_values("players", ascending=False)
    .head(10)
)

fig2 = px.bar(
    country_data,
    x="country_display",
    y="players",
    color="players",
    title="Top 10 Countries by Player Count",
    labels={
        "country_display": "Country",
        "players": "Number of Players"
    },
    color_continuous_scale="Blues"
)

fig2.update_layout(
    template="plotly_dark",
    height=430
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()


# ==========================================
# 10. PLAYER RANKINGS TABLE
# ==========================================

st.subheader("📋 Complete Player Rankings")

ranking_table = filtered_df.copy()

ranking_table["tour"] = pd.Categorical(
    ranking_table["tour"],
    categories=["ATP", "WTA"],
    ordered=True
)

display_columns = [
    col for col in [
        "tour",
        "rank",
        "player_name",
        "country",
        "points",
        "movement",
        "competitions_played"
    ]
    if col in ranking_table.columns
]

ranking_table = (
    ranking_table[display_columns]
    .sort_values(
        ["tour", "rank", "points"],
        ascending=[True, True, False]
    )
    .reset_index(drop=True)
)

st.dataframe(
    ranking_table,
    use_container_width=True,
    hide_index=True,
    height=450
)


# ==========================================
# 11. BIGGEST RANKING IMPROVEMENTS
# ==========================================

st.divider()

st.subheader("🚀 Biggest Ranking Improvements")

improved_players = filtered_df[
    filtered_df["movement"] > 0
].sort_values(
    "movement",
    ascending=False
).head(10)

if not improved_players.empty:

    fig3 = px.bar(
        improved_players,
        x="player_name",
        y="movement",
        color="tour",
        hover_data=["rank", "country", "points"],
        title="Players with Biggest Ranking Improvements",
        labels={
            "player_name": "Player Name",
            "movement": "Ranking Movement"
        },
        color_discrete_sequence=["#34d399", "#60a5fa"]
    )

    fig3.update_layout(
        template="plotly_dark",
        xaxis_tickangle=-35,
        height=420
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("No ranking improvements found in this selection.")


# ==========================================
# 12. DOWNLOAD DATA
# ==========================================

st.divider()

st.subheader("📥 Download Your Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset (CSV)",
    data=csv_data,
    file_name="tennis_filtered_data.csv",
    mime="text/csv"
)


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94a3b8;">
        <p>🎾 Tennis Analytics Dashboard</p>
        <p>Developed using Python, Pandas, Plotly & Streamlit</p>
        <p>Data Analytics Portfolio Project</p>
    </div>
    """,
    unsafe_allow_html=True
)
