
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
    overflow-wrap: break-word !important;
    line-height: 1.3 !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD MAIN DATA
# ==========================================

@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "data" / "tennis_cleaned.csv"

    if not file_path.exists():
        raise FileNotFoundError("tennis_cleaned.csv not found in data folder.")

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "name": "player_name",
        "competitor_id": "player_id"
    })

    required_columns = [
        "rank", "player_name", "country", "points", "movement"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["player_name"] = df["player_name"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    if "country_code" not in df.columns:
        df["country_code"] = "Unknown"

    if "tour" not in df.columns:
        df["tour"] = "Unknown"

    if "competitions_played" not in df.columns:
        df["competitions_played"] = 0

    df["tour"] = df["tour"].astype(str).str.upper().str.strip()

    for col in ["rank", "points", "movement"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["competitions_played"] = pd.to_numeric(
        df["competitions_played"], errors="coerce"
    ).fillna(0)

    df = df.dropna(subset=["rank", "points"])
    df = df[df["tour"].isin(["ATP", "WTA"])]

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# ==========================================
# 4. DASHBOARD HEADER
# ==========================================

st.title("🎾 Tennis Analytics Dashboard")

st.markdown(
    '<p class="subtitle">Professional Tennis Player Rankings | '
    'Performance Analysis | Global Insights</p>',
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

countries = sorted(filtered_df["country"].dropna().unique().tolist())

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
st.sidebar.caption(f"Records available: {len(filtered_df):,}")

if filtered_df.empty:
    st.warning("No records found for selected filters.")
    st.stop()


# ==========================================
# 6. KEY PERFORMANCE INDICATORS
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

col1.metric("Total Player Records", f"{total_players:,}")
col2.metric("Countries", f"{total_countries:,}")
col3.metric("Average Ranking Points", f"{average_points:,.0f}")
col4.metric("Top Ranked Player", top_player)

st.divider()


# ==========================================
# 7. TOP 10 PLAYERS
# ==========================================

st.subheader("🏆 Top 10 Ranked Players")

top_players = (
    filtered_df.sort_values(
        ["rank", "points"],
        ascending=[True, False]
    ).head(10)
)

fig1 = px.bar(
    top_players.sort_values("points", ascending=True),
    x="points",
    y="player_name",
    orientation="h",
    color="tour",
    text="points",
    hover_data=["rank", "country", "movement"],
    title="Top 10 Players by Ranking Points",
    labels={
        "player_name": "Player Name",
        "points": "Ranking Points",
        "tour": "Tennis Tour"
    },
    color_discrete_sequence=["#38bdf8", "#f97316"]
)

fig1.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside",
    cliponaxis=False
)

fig1.update_layout(
    template="plotly_dark",
    height=470,
    margin=dict(l=20, r=70, t=70, b=35),
    yaxis_title="",
    xaxis_title="Ranking Points",
    legend_title_text="Tour"
)

st.plotly_chart(fig1, use_container_width=True,
                config={"displayModeBar": False})

st.divider()


# ==========================================
# 8. COUNTRY-WISE PLAYER DISTRIBUTION
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
    country_data.sort_values("players", ascending=True),
    x="players",
    y="country_display",
    orientation="h",
    color="players",
    text="players",
    title="Top 10 Countries by Player Count",
    labels={
        "country_display": "Country",
        "players": "Number of Players"
    },
    color_continuous_scale="Blues"
)

fig2.update_traces(textposition="outside", cliponaxis=False)

fig2.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(l=20, r=55, t=70, b=35),
    yaxis_title="",
    xaxis_title="Number of Players",
    coloraxis_showscale=False
)

st.plotly_chart(fig2, use_container_width=True,
                config={"displayModeBar": False})

st.divider()


# ==========================================
# 9. PLAYER RANKINGS TABLE
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
        "tour", "rank", "player_name", "country",
        "points", "movement", "competitions_played"
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
# 10. BIGGEST RANKING IMPROVEMENTS
# ==========================================

st.divider()
st.subheader("🚀 Biggest Ranking Improvements")

improved_players = (
    filtered_df[filtered_df["movement"] > 0]
    .sort_values("movement", ascending=False)
    .head(10)
)

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

    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})
else:
    st.info("No ranking improvements found in this selection.")


# ==========================================
# 11. DOWNLOAD MAIN DATA
# ==========================================

st.divider()
st.subheader("📥 Download Your Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset (CSV)",
    data=csv_data,
    file_name="tennis_filtered_data.csv",
    mime="text/csv"
)


# ==========================================
# 12. LOAD ADDITIONAL DATA
# ==========================================

@st.cache_data
def load_extra_data():

    base = Path(__file__).parent / "data"

    categories = pd.read_csv(base / "categories.csv")
    competitions = pd.read_csv(base / "competitions.csv")
    complexes = pd.read_csv(base / "complexes.csv")
    venues = pd.read_csv(base / "venues.csv")
    doubles = pd.read_csv(base / "doubles_rankings.csv")

    return categories, competitions, complexes, venues, doubles


try:
    categories, competitions, complexes, venues, doubles = load_extra_data()

    # --------------------------------------
    # COMPETITION EXPLORER
    # --------------------------------------

    st.divider()
    st.header("🏟️ Competition Explorer")

    competition_view = competitions.merge(
        categories,
        on="category_id",
        how="left"
    )

    c1, c2 = st.columns(2)
    c1.metric("Total Competitions", f"{len(competitions):,}")
    c2.metric("Competition Categories", f"{len(categories):,}")

    types = sorted(competition_view["type"].dropna().unique())

    selected_type = st.selectbox(
        "Filter by Competition Type",
        ["All"] + types,
        key="competition_type"
    )

    if selected_type != "All":
        competition_view = competition_view[
            competition_view["type"] == selected_type
        ]

    competition_columns = [
        c for c in [
            "competition_name", "type", "gender",
            "category_name", "parent_id"
        ]
        if c in competition_view.columns
    ]

    st.dataframe(
        competition_view[competition_columns],
        use_container_width=True,
        hide_index=True,
        height=420
    )

    # --------------------------------------
    # GLOBAL VENUE EXPLORER
    # --------------------------------------

    st.divider()
    st.header("📍 Global Venue Explorer")

    venue_view = venues.merge(
        complexes,
        on="complex_id",
        how="left"
    )

    v1, v2 = st.columns(2)
    v1.metric("Total Venues", f"{len(venues):,}")
    v2.metric("Countries", f"{venues['country_name'].nunique():,}")

    venue_countries = sorted(
        venues["country_name"].dropna().unique()
    )

    selected_venue_country = st.selectbox(
        "Select Venue Country",
        ["All Countries"] + venue_countries,
        key="venue_country"
    )

    if selected_venue_country != "All Countries":
        venue_view = venue_view[
            venue_view["country_name"] == selected_venue_country
        ]

    venue_columns = [
        c for c in [
            "venue_name", "city_name", "country_name",
            "country_code", "timezone", "complex_name"
        ]
        if c in venue_view.columns
    ]

    st.dataframe(
        venue_view[venue_columns],
        use_container_width=True,
        hide_index=True,
        height=420
    )

    venue_chart = (
        venues.groupby("country_name")
        .size()
        .reset_index(name="venues")
        .sort_values("venues", ascending=False)
        .head(10)
    )

    fig_venue = px.bar(
        venue_chart.sort_values("venues", ascending=True),
        x="venues",
        y="country_name",
        orientation="h",
        text="venues",
        title="Top 10 Countries by Tennis Venues",
        labels={
            "country_name": "Country",
            "venues": "Number of Venues"
        },
        template="plotly_dark"
    )

    fig_venue.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig_venue.update_layout(
        height=450,
        margin=dict(l=20, r=55, t=70, b=35),
        yaxis_title="",
        xaxis_title="Number of Venues"
    )

    st.plotly_chart(
        fig_venue,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # --------------------------------------
    # DOUBLES RANKINGS ANALYSIS
    # --------------------------------------

    st.divider()
    st.header("👥 Doubles Rankings Analysis")

    doubles.columns = doubles.columns.str.strip().str.lower()

    for col in ["rank", "points", "movement"]:
        doubles[col] = pd.to_numeric(
            doubles[col], errors="coerce"
        )

    doubles = doubles.dropna(subset=["rank", "points"])

    d1, d2, d3 = st.columns(3)

    d1.metric("Doubles Ranking Records", f"{len(doubles):,}")
    d2.metric("Countries", f"{doubles['country'].nunique():,}")
    d3.metric("Average Points", f"{doubles['points'].mean():,.0f}")

    doubles_tours = sorted(doubles["tour"].dropna().unique())

    selected_doubles_tour = st.selectbox(
        "Select Doubles Tour",
        ["All"] + doubles_tours,
        key="doubles_tour"
    )

    doubles_view = doubles.copy()

    if selected_doubles_tour != "All":
        doubles_view = doubles_view[
            doubles_view["tour"] == selected_doubles_tour
        ]

    top_doubles = (
        doubles_view.sort_values(
            ["rank", "points"],
            ascending=[True, False]
        ).head(10)
    )

    fig_doubles = px.bar(
        top_doubles.sort_values("points", ascending=True),
        x="points",
        y="player_name",
        orientation="h",
        color="tour",
        text="points",
        hover_data=["rank", "country", "movement"],
        title="Top 10 Doubles Players by Ranking Points",
        labels={
            "player_name": "Player / Team",
            "points": "Ranking Points",
            "tour": "Tour"
        },
        template="plotly_dark"
    )

    fig_doubles.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig_doubles.update_layout(
        height=470,
        margin=dict(l=20, r=70, t=70, b=35),
        yaxis_title="",
        xaxis_title="Ranking Points",
        legend_title_text="Tour"
    )

    st.plotly_chart(
        fig_doubles,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.subheader("Complete Doubles Rankings")

    doubles_columns = [
        c for c in [
            "tour", "gender", "year", "week", "rank",
            "player_name", "country", "country_code",
            "points", "movement", "competitions_played"
        ]
        if c in doubles_view.columns
    ]

    st.dataframe(
        doubles_view[doubles_columns].sort_values(["tour", "rank"]),
        use_container_width=True,
        hide_index=True,
        height=480
    )

    doubles_csv = doubles_view.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Doubles Rankings CSV",
        doubles_csv,
        "doubles_rankings.csv",
        "text/csv"
    )

except Exception as e:
    st.error(f"Additional analytics could not load: {e}")


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
