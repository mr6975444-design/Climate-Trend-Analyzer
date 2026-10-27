import sys
from pathlib import Path

import pandas as pd
from scipy.stats import linregress

# Find the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Allow Python to import files from the project
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_data import load_climate_data


def calculate_yearly_averages(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate yearly averages."""

    yearly = (
        data.groupby("year")
        .agg(
            temperature_c=("temperature_c", "mean"),
            rainfall_mm=("rainfall_mm", "mean"),
            humidity_percent=("humidity_percent", "mean"),
            co2_ppm=("co2_ppm", "mean"),
            sea_level_mm=("sea_level_mm", "mean"),
        )
        .reset_index()
    )

    return yearly


def calculate_temperature_trend(data: pd.DataFrame) -> dict:
    """Calculate the long-term temperature trend."""

    # Sort the data by date
    monthly = data.sort_values("date").copy()

    # Find the average temperature for each month
    month_means = (
        monthly.groupby("month")["temperature_c"]
        .transform("mean")
    )

    # Remove the normal seasonal pattern
    monthly["seasonally_adjusted_c"] = (
        monthly["temperature_c"] - month_means
    )

    # Calculate the number of years since the first date
    elapsed_years = (
        (monthly["date"] - monthly["date"].min()).dt.days / 365.25
    )

    # Calculate the temperature trend
    result = linregress(
        elapsed_years,
        monthly["seasonally_adjusted_c"]
    )

    return {
        "slope_c_per_year": result.slope,
        "slope_c_per_decade": result.slope * 10,
        "r_squared": result.rvalue ** 2,
        "p_value": result.pvalue,
    }


def detect_temperature_anomalies(
    data: pd.DataFrame,
    threshold: float = 2.0
) -> pd.DataFrame:
    """Find unusually high or low temperatures."""

    monthly = data.copy()

    month_mean = (
        monthly.groupby("month")["temperature_c"]
        .transform("mean")
    )

    month_std = (
        monthly.groupby("month")["temperature_c"]
        .transform("std")
    )

    monthly["anomaly_score"] = (
        (monthly["temperature_c"] - month_mean) / month_std
    )

    monthly["is_anomaly"] = (
        monthly["anomaly_score"].abs() >= threshold
    )

    anomalies = monthly[monthly["is_anomaly"]].copy()

    return anomalies[
        [
            "date",
            "temperature_c",
            "anomaly_score",
            "is_anomaly",
        ]
    ]


def calculate_correlations(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlations between climate variables."""

    columns = [
        "temperature_c",
        "rainfall_mm",
        "humidity_percent",
        "co2_ppm",
        "sea_level_mm",
    ]

    return data[columns].corr()


def run_analysis() -> None:
    """Run the complete climate analysis."""

    print("=" * 60)
    print("CLIMATE TREND ANALYZER")
    print("=" * 60)

    # Load data
    data = load_climate_data()

    # --------------------------------------------------
    # YEARLY AVERAGES
    # --------------------------------------------------

    yearly_averages = calculate_yearly_averages(data)

    yearly_output = (
        PROJECT_ROOT
        / "outputs"
        / "reports"
        / "yearly_climate_averages.csv"
    )

    yearly_averages.to_csv(
        yearly_output,
        index=False
    )

    print("\nYEARLY CLIMATE AVERAGES")
    print(yearly_averages.to_string(index=False))

    # --------------------------------------------------
    # TEMPERATURE TREND
    # --------------------------------------------------

    trend = calculate_temperature_trend(data)

    print("\n" + "=" * 60)
    print("LINEAR TEMPERATURE TREND")
    print("=" * 60)

    print(
        f"Slope: {trend['slope_c_per_year']:.4f} °C/year"
    )

    print(
        f"Decadal trend: {trend['slope_c_per_decade']:.4f} °C/decade"
    )

    print(
        f"R-squared: {trend['r_squared']:.4f}"
    )

    print(
        f"P-value: {trend['p_value']:.4f}"
    )

    # --------------------------------------------------
    # TEMPERATURE ANOMALIES
    # --------------------------------------------------

    anomalies = detect_temperature_anomalies(data)

    anomaly_output = (
        PROJECT_ROOT
        / "outputs"
        / "reports"
        / "temperature_anomalies.csv"
    )

    anomalies.to_csv(
        anomaly_output,
        index=False
    )

    print("\n" + "=" * 60)
    print("TEMPERATURE ANOMALIES")
    print("=" * 60)

    if anomalies.empty:
        print("No temperature anomalies detected.")
    else:
        print(anomalies.to_string(index=False))

    print(
        f"\nTotal anomalies detected: {len(anomalies)}"
    )

    # --------------------------------------------------
    # CORRELATIONS
    # --------------------------------------------------

    correlations = calculate_correlations(data)

    correlation_output = (
        PROJECT_ROOT
        / "outputs"
        / "reports"
        / "climate_correlations.csv"
    )

    correlations.to_csv(
        correlation_output
    )

    print("\n" + "=" * 60)
    print("CLIMATE VARIABLE CORRELATIONS")
    print("=" * 60)

    print(correlations.round(3).to_string())

    # --------------------------------------------------
    # FINISHED
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    print(
        f"\nReports saved in: "
        f"{PROJECT_ROOT / 'outputs' / 'reports'}"
    )


if __name__ == "__main__":
    run_analysis()