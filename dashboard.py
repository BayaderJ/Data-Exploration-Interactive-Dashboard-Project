import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Traffic Insights Dashboard",
    layout="wide"
)
pastel_colors = ["#A3C1AD", "#395F38", "#247765", "#995477", "#B5EAEA"]
# Load data with caching
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

# Sidebar - Dataset description and Filters
st.sidebar.header("Dataset description")
st.sidebar.markdown(
    """
    This traffic dataset includes real-time and historical information such as traffic indexes, jam counts, delays (in minutes), and jam lengths (in kilometers).
    It provides you with clear insights into overall traffic conditions!
    """
)

st.sidebar.header("Filters")
cities = sorted(df["city"].unique())
selected_cities = st.sidebar.multiselect("Select Cities", cities, default=cities[:2])

date_min, date_max = df["datetime"].min().date(), df["datetime"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

hour_filter = st.sidebar.slider("Hour of Day", 0, 23, (6, 20))

day_type = st.sidebar.selectbox(
    "Day Type", ["All Days", "Weekdays Only", "Weekends Only"], index=0
)

# Filter data accordingly
filtered_df = df[
    (df["city"].isin(selected_cities)) &
    (df["datetime"].dt.date.between(date_range[0], date_range[1])) &
    (df["hour"].between(hour_filter[0], hour_filter[1]))
]
if day_type == "Weekdays Only":
    filtered_df = filtered_df[~filtered_df["is_weekend"]]
elif day_type == "Weekends Only":
    filtered_df = filtered_df[filtered_df["is_weekend"]]

st.title("Traffic Insights Dashboard")
st.caption(f"Showing data for {len(filtered_df):,} observations based on your filters.")

if filtered_df.empty:
    st.info("No data available for selected filters. Please adjust filters.")
    st.stop()

# KPIs 
col1, col2, col3, col4 = st.columns(4)

peak_index = filtered_df["traffic_index_live"].max()
avg_index = filtered_df["traffic_index_live"].mean()
col1.metric(
    "Peak Traffic Index",
    f"{peak_index:.0f}",
    delta=f"Average: {avg_index:.1f}"
)

avg_delay = filtered_df["jams_delay"].mean()
total_delay_min = filtered_df["jams_delay"].sum()
total_delay_hr = total_delay_min / 60
col2.metric(
    "Average Jam Delay (Min)",
    f"{avg_delay:.1f}",
    delta=f"Total Delay: {total_delay_hr:,.1f} hours"
)

total_jam_length = filtered_df["jams_length"].sum()
avg_jam_length = filtered_df["jams_length"].mean()
col3.metric(
    "Total Jam Length (km)",
    f"{total_jam_length:,.0f}",
    delta=f"Average: {avg_jam_length:.2f} km"
)

congestion_pct = (filtered_df["travel_ratio"] > 1).mean() * 100
col4.metric(
    "Time in Congestion (%)",
    f"{congestion_pct:.0f}%",
)

st.markdown("---")

# Tabs for Data preview, Summary Stats, Visualizations
tab1, tab2, tab3 = st.tabs(["Data Preview", "Summary Statistics", "Visual Insights"])

with tab1:
    st.subheader("Sample of Filtered Data")
    st.dataframe(filtered_df.sort_values("datetime").head(100), use_container_width=True)
    # Insight section 
    st.markdown("## Key Insights")
    peak_hour = filtered_df.groupby("hour")["traffic_index_live"].mean().idxmax()
    peak_city = filtered_df.groupby("city")["traffic_index_live"].mean().idxmax()
    st.markdown(f"""
- Highest average traffic index among selected city/cities is in **{peak_city}**.
- Congestion happens approximately **{congestion_pct:.0f}%** of the time in the filtered dataset.
"""  )

with tab2:
    st.subheader("Summary Statistics (Filtered Data)")
    desc_cols = ["traffic_index_live", "jams_count", "jams_delay", "jams_length", "traffic_index_week_ago", "travel_time_historic", "travel_time_live"]
    desc_stats = filtered_df[desc_cols].describe().T.round(2)
    st.dataframe(desc_stats, use_container_width=True)

    st.write("Average Metrics by City")
    city_summary = (
        filtered_df.groupby("city")
        .agg({
            "traffic_index_live": "mean",
            "jams_delay": "mean",
            "jams_length": "mean",
            "travel_ratio": lambda x: (x > 1).mean() * 100
        })
        .rename(columns={
            "traffic_index_live": "Avg Traffic Index",
            "jams_delay": "Avg Jam Delay (min)",
            "jams_length": "Avg Jam Length (km)",
            "travel_ratio": "Congestion Percentage (%)"
        })
        .round(2)
        .reset_index()
    )
    st.dataframe(city_summary, use_container_width=True)

with tab3:
    st.subheader("Traffic Over Time")
    fig1 = px.line(
        filtered_df.sort_values("datetime"),
        x="datetime",
        y="traffic_index_live",
        color="city",
        title="Live Traffic Index Over Time",
        line_shape="spline",
        color_discrete_sequence=pastel_colors
    )
    fig1.update_layout(height=450, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Average Jam Delay by Hour")
    hourly_stats = (
        filtered_df.groupby("hour")
        .agg(avg_jam_delay=("jams_delay", "mean"))
        .reset_index()
    )
    fig2 = px.bar(
        hourly_stats,
        x="hour",
        y="avg_jam_delay",
        labels={"hour": "Hour of Day", "avg_jam_delay": "Average Jam Delay (minutes)"},
        title="Average Jam Delay by Hour",
        color_discrete_sequence=pastel_colors
        
        
    )
    fig2.update_layout(height=350, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

