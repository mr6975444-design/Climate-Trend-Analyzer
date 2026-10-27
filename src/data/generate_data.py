"""
Synthetic Climate Dataset Generator

Creates a realistic-looking monthly climate dataset for the
Climate Trend Analyzer project.

Output:
    data/raw/synthetic_climate_data.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

START_DATE = "2010-01-01"
END_DATE = "2025-12-01"
RANDOM_SEED = 42

OUTPUT_PATH = Path("data/raw/synthetic_climate_data.csv")


# -------------------------------------------------------------------
# Dataset generation
# -------------------------------------------------------------------

def generate_climate_data() -> pd.DataFrame:
    """Generate synthetic monthly climate observations."""

    rng = np.random.default_rng(RANDOM_SEED)

    dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="MS",
    )

    n = len(dates)

    # Time index measured in years from the beginning of the dataset.
    years_from_start = np.arange(n) / 12

    # Month number: January = 1, December = 12.
    month = dates.month.to_numpy()

    # ---------------------------------------------------------------
    # 1. Temperature
    # ---------------------------------------------------------------
    # Seasonal temperature cycle + long-term warming trend + noise.

    seasonal_temperature = (
        4.5 * np.sin(2 * np.pi * (month - 1) / 12)
    )

    warming_trend = 0.035 * years_from_start

    temperature = (
        25.0
        + seasonal_temperature
        + warming_trend
        + rng.normal(0, 0.7, n)
    )

    # Add a few unusual temperature events.
    anomaly_indices = rng.choice(n, size=8, replace=False)
    temperature[anomaly_indices] += rng.choice(
        [-2.5, 2.5, 3.0],
        size=len(anomaly_indices),
    )

    # ---------------------------------------------------------------
    # 2. Rainfall
    # ---------------------------------------------------------------
    # Seasonal rainfall pattern + random variability.

    rainfall_seasonal = (
        120
        + 70 * np.sin(2 * np.pi * (month - 2) / 12)
    )

    rainfall = (
        rainfall_seasonal
        + rng.normal(0, 35, n)
    )

    rainfall = np.clip(rainfall, 5, None)

    # ---------------------------------------------------------------
    # 3. Humidity
    # ---------------------------------------------------------------
    # Humidity is partly related to rainfall and temperature.

    humidity = (
        68
        + 0.035 * (rainfall - rainfall.mean())
        - 0.7 * (temperature - temperature.mean())
        + rng.normal(0, 4, n)
    )

    humidity = np.clip(humidity, 35, 95)

    # ---------------------------------------------------------------
    # 4. Atmospheric CO2
    # ---------------------------------------------------------------
    # Approximate long-term upward trend.

    co2 = (
        390
        + 2.4 * years_from_start
        + rng.normal(0, 1.5, n)
    )

    # ---------------------------------------------------------------
    # 5. Sea level
    # ---------------------------------------------------------------
    # Gradual upward trend with small random fluctuations.

    sea_level = (
        0.0
        + 3.4 * years_from_start
        + rng.normal(0, 0.8, n)
    )

    # ---------------------------------------------------------------
    # Build DataFrame
    # ---------------------------------------------------------------

    climate_data = pd.DataFrame(
        {
            "date": dates,
            "year": dates.year,
            "month": dates.month,
            "temperature_c": temperature,
            "rainfall_mm": rainfall,
            "humidity_percent": humidity,
            "co2_ppm": co2,
            "sea_level_mm": sea_level,
        }
    )

    # Round numeric values for cleaner CSV output.
    numeric_columns = [
        "temperature_c",
        "rainfall_mm",
        "humidity_percent",
        "co2_ppm",
        "sea_level_mm",
    ]

    climate_data[numeric_columns] = climate_data[numeric_columns].round(2)

    return climate_data


# -------------------------------------------------------------------
# Save dataset
# -------------------------------------------------------------------

def save_dataset(data: pd.DataFrame) -> None:
    """Save the generated dataset to the raw-data directory."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Dataset saved to: {OUTPUT_PATH}")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":
    climate_data = generate_climate_data()

    save_dataset(climate_data)

    print("\nFirst 5 rows:")
    print(climate_data.head())

    print("\nDataset information:")
    print(climate_data.info())

    print("\nSummary statistics:")
    print(climate_data.describe())