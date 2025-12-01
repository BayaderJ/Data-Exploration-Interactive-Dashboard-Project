import streamlit as st 
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Traffic Insights Dashboard",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_traffic_index_gcc.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()
    df["travel_ratio"] = df["travel_time_live"] / df["travel_time_historic"]
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Dataset Info")
st.sidebar.markdown(
    """
- Our traffic dataset contains real-time and historical traffic
 information collected across major cities in the region.
"""
)

st.sidebar.header("Filters")
cities = sorted(df["city"].unique())
selected_cities = st.sidebar.multiselect("Select Cities", cities, default=cities[:2])

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["datetime"].min().date(), df["datetime"].max().date()),
    min_value=df["datetime"].min().date(),
    max_value=df["datetime"].max().date()
)

hour_filter = st.sidebar.slider("Hour of Day", 0, 23, (6, 20))
show_weekend = st.sidebar.checkbox("Show Weekend Patterns", value=False)

# Filter data
filtered_df = df[
    (df["city"].isin(selected_cities)) &
    (df["datetime"].dt.date.between(date_range[0], date_range[1])) &
    (df["hour"].between(hour_filter[0], hour_filter[1]))
]

if show_weekend:
    filtered_df = filtered_df[filtered_df["is_weekend"]]

# KPI Metrics
st.title("Traffic Dashboard")
if filtered_df.empty:
    st.info("No data available for selected filters.")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peak Traffic Index", f"{filtered_df['traffic_index_live'].max():.0f}", 
                delta=f"{filtered_df['traffic_index_live'].mean():.0f} avg")
    col2.metric("Avg Jam Delay (min)", f"{filtered_df['jams_delay'].mean():.1f}", 
                delta=f"{filtered_df['jams_delay'].sum():.0f} total")
    col3.metric("Total Jam Length (km)", f"{filtered_df['jams_length'].sum():.0f}")
    congestion_pct = (filtered_df['travel_ratio'] > 1).mean() * 100
    col4.metric("Congestion %", f"{congestion_pct:.0f}%")

# Main Chart
if not filtered_df.empty:
    fig = px.line(
        filtered_df, x="datetime", y="traffic_index_live",
        color="city", title="Live Traffic Index",
        line_shape='spline', color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
