
from pathlib import Path
import sys

import pandas as pd
import streamlit as st
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_data import load_climate_data
from src.analysis.climate_analysis import (
    calculate_yearly_averages,
    calculate_temperature_trend,
    detect_temperature_anomalies,
)

st.set_page_config(
    page_title="Climate Trend Analyzer",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Climate Trend Analyzer")
st.write(
    "Explore temperature trends, rainfall, climate indicators, "
    "and unusual temperature observations."
)

st.info(
    "This dashboard uses synthetic data for demonstration. "
    "It does not represent actual climate observations."
)

try:
    data = load_climate_data()
except Exception as error:
    st.error(f"Could not load the climate data: {error}")
    st.stop()

yearly = calculate_yearly_averages(data)
trend = calculate_temperature_trend(data)
anomalies = detect_temperature_anomalies(data)

st.sidebar.header("Dashboard Filters")

years = sorted(data["year"].unique())
selected_years = st.sidebar.slider(
    "Select year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years))),
)

filtered = data[
    data["year"].between(selected_years[0], selected_years[1])
].copy()

filtered_anomalies = anomalies[
    anomalies["date"].dt.year.between(
        selected_years[0], selected_years[1]
    )
]

st.subheader("Key Climate Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average temperature",
    f"{filtered['temperature_c'].mean():.2f} °C",
)

col2.metric(
    "Average rainfall",
    f"{filtered['rainfall_mm'].mean():.1f} mm",
)

col3.metric(
    "Unusual temperature observations",
    len(filtered_anomalies),
)

st.caption(
    "The temperature trend below is calculated across the full dataset, "
    "not just the selected year range."
)

col4, col5 = st.columns(2)

col4.metric(
    "Estimated trend",
    f"{trend['slope_c_per_decade']:.3f} °C/decade",
)

col5.metric(
    "Trend p-value",
    f"{trend['p_value']:.4f}",
)

st.divider()
st.subheader("Temperature Over Time")

fig_temp = px.line(
    filtered,
    x="date",
    y="temperature_c",
    title="Monthly Temperature",
    labels={
        "date": "Date",
        "temperature_c": "Temperature (°C)",
    },
)

st.plotly_chart(fig_temp, use_container_width=True)

st.subheader("Yearly Climate Trends")

filtered_yearly = yearly[
    yearly["year"].between(selected_years[0], selected_years[1])
]

fig_yearly = px.line(
    filtered_yearly,
    x="year",
    y="temperature_c",
    markers=True,
    title="Yearly Average Temperature",
    labels={
        "year": "Year",
        "temperature_c": "Average temperature (°C)",
    },
)

st.plotly_chart(fig_yearly, use_container_width=True)

col6, col7 = st.columns(2)

with col6:
    fig_rain = px.bar(
        filtered_yearly,
        x="year",
        y="rainfall_mm",
        title="Yearly Average Rainfall",
        labels={
            "year": "Year",
            "rainfall_mm": "Rainfall (mm)",
        },
    )
    st.plotly_chart(fig_rain, use_container_width=True)

with col7:
    fig_co2 = px.line(
        filtered_yearly,
        x="year",
        y="co2_ppm",
        markers=True,
        title="Yearly Average CO₂",
        labels={
            "year": "Year",
            "co2_ppm": "CO₂ (ppm)",
        },
    )
    st.plotly_chart(fig_co2, use_container_width=True)

st.subheader("Temperature Anomalies")

if filtered_anomalies.empty:
    st.write("No anomalies were detected in this year range.")
else:
    st.dataframe(
        filtered_anomalies,
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Explore the Data")

with st.expander("View monthly climate data"):
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

st.download_button(
    label="Download filtered climate data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_climate_data.csv",
    mime="text/csv",
)

st.caption(
    "Climate Trend Analyzer | Educational data science project"
)
